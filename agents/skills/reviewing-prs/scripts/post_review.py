#!/usr/bin/env python3
"""
Post a GitHub PR review with inline comments. Summary body is optional.

Usage:
    # Inline comments only (preferred)
    post_review.py <pr> --event COMMENT --comments-file comments.json

    # With optional summary
    post_review.py <pr> --event COMMENT --comments-file comments.json --body "Optional summary"

    # Reply to existing thread
    post_review.py <pr> --reply-to 123456 --body "Your reply"

    # Approve/request changes
    post_review.py <pr> --event APPROVE
    post_review.py <pr> --event REQUEST_CHANGES --body "Blocking issues" --comments-file comments.json

Comments file format (JSON array):
    [
        {"path": "src/file.ts", "line": 42, "body": "[Claude]: Your comment"},
        {"path": "src/other.ts", "line": 10, "body": "[Claude]: Another comment"}
    ]

Exit codes:
    0 - Success
    1 - Invalid arguments
    2 - GitHub API error
    3 - JSON parsing error
"""

import argparse
import json
import subprocess
import sys
import re
from pathlib import Path


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

    # Parse remote URL (handles HTTPS and SSH)
    remote_match = re.search(r'github\.com[:/]([^/]+)/([^/.]+)', remote_url)
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
    # Build the gh api command
    cmd = [
        'gh', 'api',
        f'repos/{owner}/{repo}/pulls/{pr_num}/reviews',
        '-X', 'POST',
        '--field', f'body={body}',
        '--field', f'event={event}',
    ]

    # Add comments if provided
    if comments:
        # Validate each comment
        for i, comment in enumerate(comments):
            validate_comment(comment, i)

        # gh api --field expects JSON for array values
        cmd.extend(['--field', f'comments={json.dumps(comments)}'])

    print(f"Posting {event} review to {owner}/{repo}#{pr_num}...", file=sys.stderr)

    try:
        result = subprocess.run(
            cmd,
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


def main():
    parser = argparse.ArgumentParser(
        description='Post a GitHub PR review with proper error handling.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('pr_ref', help='PR number or full GitHub PR URL')
    parser.add_argument('--body', default='', help='Review summary body (optional for inline-only reviews)')
    parser.add_argument('--event', required=True,
                        choices=['APPROVE', 'REQUEST_CHANGES', 'COMMENT'],
                        help='Review event type')
    parser.add_argument('--comments-file', type=Path,
                        help='JSON file containing inline comments')
    parser.add_argument('--reply-to', type=int,
                        help='Comment ID to reply to (instead of posting review)')

    args = parser.parse_args()

    # Parse PR reference
    try:
        owner, repo, pr_num = parse_pr_reference(args.pr_ref)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Handle reply mode
    if args.reply_to:
        if not args.body:
            print("Error: --body is required when using --reply-to", file=sys.stderr)
            return 1
        try:
            reply_to_comment(owner, repo, pr_num, args.reply_to, args.body)
            return 0
        except RuntimeError:
            return 2

    # Load comments from file if provided
    comments = None
    if args.comments_file:
        if not args.comments_file.exists():
            print(f"Error: Comments file not found: {args.comments_file}", file=sys.stderr)
            return 1

        try:
            comments = json.loads(args.comments_file.read_text())
            if not isinstance(comments, list):
                print("Error: Comments file must contain a JSON array", file=sys.stderr)
                return 3
        except json.JSONDecodeError as e:
            print(f"Error parsing comments file: {e}", file=sys.stderr)
            return 3

    # Post the review
    try:
        post_review(owner, repo, pr_num, args.body, args.event, comments)
        return 0
    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 1
    except RuntimeError:
        return 2


if __name__ == '__main__':
    sys.exit(main())
