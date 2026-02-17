#!/usr/bin/env python3
"""
Post a GitHub PR review with inline comments. Summary body is optional.

Usage (JSON via stdin):
    post_review.py <<'EOF'
    {
        "pr": "123",
        "event": "COMMENT",
        "role": "Reviewer",
        "model": "Opus 4.6",
        "body": "Optional summary",
        "comments": [
            {"path": "src/file.ts", "line": 42, "body": "Your comment"}
        ]
    }
    EOF

JSON input fields:
    pr/pr_ref: PR number or URL (required)
    event: APPROVE, REQUEST_CHANGES, or COMMENT (required unless reply_to)
    body: Review summary body (optional)
    comments: Array of inline comments (optional)
    reply_to: Comment ID to reply to (alternative to posting review)
    role: Agent role prefix (default: "Reviewer")
    model: Model name for prefix (default: "Claude")

Outputs JSON to stdout:
    Success: {"status": "ok", "review_id": 123, "action": "posted|replied"}
    Error:   {"error": "message"}

Exit codes:
    0 - Success
    1 - Invalid arguments
    2 - GitHub API error
    3 - JSON parsing error
"""

import json
import subprocess
import sys
import re


def output_json(data: dict) -> None:
    """Output structured JSON to stdout."""
    print(json.dumps(data))


def add_prefix(body: str, role: str, model: str) -> str:
    """Add [🤖 {role} - {model}]: prefix to body if not already prefixed."""
    if body.strip().startswith("[🤖"):
        return body
    return f"[🤖 {role} - {model}]: {body}"


def parse_pr_reference(pr_ref: str) -> tuple[str, str, str]:
    """
    Parse PR reference to extract owner, repo, and PR number.

    Args:
        pr_ref: Either a PR number (requires being in a git repo) or full GitHub URL

    Returns:
        Tuple of (owner, repo, pr_number)

    Raises:
        ValueError: If unable to parse the reference
    """
    # Try to parse as GitHub URL
    url_match = re.match(r'https?://github\.com/([^/]+)/([^/]+)/pull/(\d+)', pr_ref)
    if url_match:
        return url_match.group(1), url_match.group(2), url_match.group(3)

    # Assume it's a PR number - get owner/repo from git remote
    if not pr_ref.isdigit():
        raise ValueError(f"Invalid PR reference: {pr_ref}")

    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True, text=True, check=True
        )
        remote_url = result.stdout.strip()
    except subprocess.CalledProcessError:
        raise ValueError("Not in a git repository and no full PR URL provided")

    # Parse remote URL (handles HTTPS and SSH, with or without .git suffix)
    remote_match = re.search(r'github\.com[:/]([^/]+)/(.+?)(?:\.git)?$', remote_url)
    if not remote_match:
        raise ValueError(f"Could not parse GitHub owner/repo from remote: {remote_url}")

    return remote_match.group(1), remote_match.group(2), pr_ref


def validate_comment(comment: dict, index: int) -> None:
    """Validate a single comment object."""
    required_fields = ['path', 'line', 'body']
    for field in required_fields:
        if field not in comment:
            raise ValueError(f"Comment {index}: missing required field '{field}'")

    if not isinstance(comment['line'], int) or comment['line'] < 1:
        raise ValueError(f"Comment {index}: 'line' must be a positive integer")

    if not comment['body'].strip():
        raise ValueError(f"Comment {index}: 'body' cannot be empty")


def post_review(owner: str, repo: str, pr_num: str, body: str, event: str,
                comments: list[dict] | None = None) -> dict:
    """
    Post a review to a GitHub PR.

    Args:
        owner: Repository owner
        repo: Repository name
        pr_num: Pull request number
        body: Review summary body
        event: Review event (APPROVE, REQUEST_CHANGES, COMMENT)
        comments: Optional list of inline comments

    Returns:
        API response as dict

    Raises:
        RuntimeError: If the API call fails
    """
    # Validate comments if provided
    if comments:
        for i, comment in enumerate(comments):
            validate_comment(comment, i)

    # Build request payload as JSON (required for arrays to work correctly)
    payload = {
        'event': event,
        'body': body,
    }
    if comments:
        payload['comments'] = comments

    # Use --input to pass JSON payload via stdin (--field stringifies arrays incorrectly)
    cmd = [
        'gh', 'api',
        f'repos/{owner}/{repo}/pulls/{pr_num}/reviews',
        '-X', 'POST',
        '--input', '-',
    ]

    print(f"Posting {event} review to {owner}/{repo}#{pr_num}...", file=sys.stderr)

    try:
        result = subprocess.run(
            cmd,
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            check=True
        )
        response = json.loads(result.stdout) if result.stdout else {}
        print(f"Review posted successfully. Review ID: {response.get('id', 'unknown')}",
              file=sys.stderr)
        return response

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Unknown error"
        print(f"Error posting review: {error_msg}", file=sys.stderr)

        # Provide helpful guidance for common errors
        if "404" in error_msg:
            print("Hint: Check that the PR exists and you have access to it.", file=sys.stderr)
        elif "422" in error_msg:
            print("Hint: Check comment line numbers are within the diff.", file=sys.stderr)
        elif "401" in error_msg or "403" in error_msg:
            print("Hint: Check your GitHub authentication (gh auth status).", file=sys.stderr)

        raise RuntimeError(f"GitHub API error: {error_msg}")


def reply_to_comment(owner: str, repo: str, pr_num: str,
                     comment_id: int, body: str) -> dict:
    """
    Reply to an existing review comment thread.

    Args:
        owner: Repository owner
        repo: Repository name
        pr_num: Pull request number
        comment_id: ID of the comment to reply to
        body: Reply body

    Returns:
        API response as dict
    """
    cmd = [
        'gh', 'api',
        f'repos/{owner}/{repo}/pulls/{pr_num}/comments',
        '-X', 'POST',
        '--field', f'body={body}',
        '--field', f'in_reply_to={comment_id}',
    ]

    print(f"Replying to comment {comment_id}...", file=sys.stderr)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        response = json.loads(result.stdout) if result.stdout else {}
        print(f"Reply posted successfully.", file=sys.stderr)
        return response

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Unknown error"
        raise RuntimeError(f"GitHub API error: {error_msg}")


def parse_args():
    """Parse arguments from stdin JSON."""
    if sys.stdin.isatty():
        print("Error: This script requires JSON input via stdin", file=sys.stderr)
        print("Usage: post_review.py <<'EOF'", file=sys.stderr)
        print('{"pr": "123", "event": "COMMENT", "comments": [...]}', file=sys.stderr)
        print("EOF", file=sys.stderr)
        output_json({"error": "This script requires JSON input via stdin"})
        sys.exit(1)

    try:
        data = json.load(sys.stdin)
        pr_ref = data.get("pr") or data.get("pr_ref")

        if not pr_ref:
            print("Error: Missing required field 'pr' or 'pr_ref'", file=sys.stderr)
            output_json({"error": "Missing required field 'pr' or 'pr_ref'"})
            sys.exit(1)

        class Args:
            pass
        args = Args()
        args.pr_ref = pr_ref
        args.body = data.get("body", "")
        args.event = data.get("event")
        args.comments = data.get("comments")
        args.reply_to = data.get("reply_to")
        args.role = data.get("role", "Reviewer")
        args.model = data.get("model", "Claude")
        return args
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        output_json({"error": f"Invalid JSON input: {e}"})
        sys.exit(1)


def main():
    args = parse_args()

    # Parse PR reference
    try:
        owner, repo, pr_num = parse_pr_reference(args.pr_ref)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        output_json({"error": str(e)})
        return 1

    # Handle reply mode
    if args.reply_to:
        if not args.body:
            print("Error: 'body' is required when using reply_to", file=sys.stderr)
            output_json({"error": "'body' is required when using reply_to"})
            return 1
        try:
            body = add_prefix(args.body, args.role, args.model)
            response = reply_to_comment(owner, repo, pr_num, args.reply_to, body)
            output_json({
                "status": "ok",
                "action": "replied",
                "comment_id": response.get("id"),
                "in_reply_to": args.reply_to
            })
            return 0
        except RuntimeError as e:
            output_json({"error": str(e)})
            return 2

    # Validate event is provided for non-reply mode
    if not args.event:
        print("Error: 'event' is required (unless using reply_to)", file=sys.stderr)
        output_json({"error": "'event' is required (unless using reply_to)"})
        return 1

    comments = args.comments

    # Auto-prefix comment bodies and review body
    if comments:
        for comment in comments:
            comment['body'] = add_prefix(comment['body'], args.role, args.model)
    body = add_prefix(args.body, args.role, args.model) if args.body else args.body

    # Post the review
    try:
        response = post_review(owner, repo, pr_num, body, args.event, comments)
        output_json({
            "status": "ok",
            "action": "posted",
            "review_id": response.get("id"),
            "event": args.event
        })
        return 0
    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        output_json({"error": str(e)})
        return 1
    except RuntimeError as e:
        output_json({"error": str(e)})
        return 2


if __name__ == '__main__':
    sys.exit(main())
