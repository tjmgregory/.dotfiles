#!/usr/bin/env python3
"""
Post a reply to a PR comment thread with duplicate prevention.

Usage:
    # Reply to a review comment (inline on code)
    post_reply.py <pr> --comment-id 123456 --name Claude --body "Your reply"

    # Reply to an issue comment (general PR discussion)
    post_reply.py <pr> --issue-comment-id 789 --name Claude --body "Your reply"

    # Check if an agent already replied (dry run)
    post_reply.py <pr> --comment-id 123456 --check-only

The script automatically formats replies as: [🤖 {name}]: {body}

Exit codes:
    0 - Success (or already replied in check mode)
    1 - Invalid arguments
    2 - GitHub API error
    3 - Already replied (duplicate prevention triggered)
"""

import argparse
import json
import subprocess
import sys
import re


def parse_pr_reference(pr_ref: str) -> tuple[str, str, str]:
    """Parse PR reference to extract owner, repo, and PR number."""
    url_match = re.match(r'https?://github\.com/([^/]+)/([^/]+)/pull/(\d+)', pr_ref)
    if url_match:
        return url_match.group(1), url_match.group(2), url_match.group(3)

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

    remote_match = re.search(r'github\.com[:/]([^/]+)/(.+?)(?:\.git)?$', remote_url)
    if not remote_match:
        raise ValueError(f"Could not parse GitHub owner/repo from remote: {remote_url}")

    return remote_match.group(1), remote_match.group(2), pr_ref


def format_reply(name: str, body: str) -> str:
    """Format reply with robot emoji and agent name prefix."""
    return f"[🤖 {name}]: {body}"


def get_thread_replies(owner: str, repo: str, pr_num: str, comment_id: int) -> list[dict]:
    """Fetch all replies in a review comment thread."""
    cmd = [
        'gh', 'api', '--paginate',
        f'repos/{owner}/{repo}/pulls/{pr_num}/comments'
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        all_comments = json.loads(result.stdout) if result.stdout else []

        # Find replies to this comment (in_reply_to_id matches)
        thread = [c for c in all_comments
                  if c.get('id') == comment_id or c.get('in_reply_to_id') == comment_id]
        return thread
    except subprocess.CalledProcessError:
        return []


def has_agent_replied(thread: list[dict]) -> bool:
    """Check if any comment in thread has the robot agent prefix."""
    for comment in thread:
        body = comment.get('body', '')
        # Match [🤖 anything]: pattern
        if body.strip().startswith('[🤖'):
            return True
    return False


def post_review_comment_reply(owner: str, repo: str, pr_num: str,
                               comment_id: int, body: str) -> dict:
    """Post a reply to a review comment thread."""
    cmd = [
        'gh', 'api',
        f'repos/{owner}/{repo}/pulls/{pr_num}/comments',
        '-X', 'POST',
        '--field', f'body={body}',
        '--field', f'in_reply_to={comment_id}',
    ]

    print(f"Posting reply to review comment {comment_id}...", file=sys.stderr)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        response = json.loads(result.stdout) if result.stdout else {}
        print(f"Reply posted. Comment ID: {response.get('id', 'unknown')}", file=sys.stderr)
        return response
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Unknown error"
        if "404" in error_msg:
            print("Hint: Comment may not exist or PR is inaccessible.", file=sys.stderr)
        raise RuntimeError(f"GitHub API error: {error_msg}")


def post_issue_comment(owner: str, repo: str, pr_num: str, body: str) -> dict:
    """Post a general issue comment (not inline on code)."""
    cmd = [
        'gh', 'api',
        f'repos/{owner}/{repo}/issues/{pr_num}/comments',
        '-X', 'POST',
        '-f', f'body={body}',
    ]

    print(f"Posting issue comment...", file=sys.stderr)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        response = json.loads(result.stdout) if result.stdout else {}
        print(f"Comment posted. ID: {response.get('id', 'unknown')}", file=sys.stderr)
        return response
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Unknown error"
        raise RuntimeError(f"GitHub API error: {error_msg}")


def main():
    parser = argparse.ArgumentParser(
        description='Post a reply to a PR comment with duplicate prevention.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('pr_ref', help='PR number or full GitHub PR URL')
    parser.add_argument('--comment-id', type=int,
                        help='Review comment ID to reply to (inline comments)')
    parser.add_argument('--issue-comment-id', type=int,
                        help='Issue comment ID (for general PR discussion replies)')
    parser.add_argument('--name', default='Claude',
                        help='Agent name for reply prefix (default: Claude)')
    parser.add_argument('--body', help='Reply message (prefix added automatically)')
    parser.add_argument('--check-only', action='store_true',
                        help='Only check if an agent already replied, do not post')
    parser.add_argument('--force', action='store_true',
                        help='Post even if an agent already replied')

    args = parser.parse_args()

    if not args.comment_id and not args.issue_comment_id:
        print("Error: Must specify --comment-id or --issue-comment-id", file=sys.stderr)
        return 1

    if not args.check_only and not args.body:
        print("Error: --body is required unless using --check-only", file=sys.stderr)
        return 1

    try:
        owner, repo, pr_num = parse_pr_reference(args.pr_ref)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Check for existing agent reply (review comments only - has threading)
    if args.comment_id:
        thread = get_thread_replies(owner, repo, pr_num, args.comment_id)
        if has_agent_replied(thread):
            if args.check_only:
                print("An agent has already replied to this thread.", file=sys.stderr)
                return 0
            if not args.force:
                print("Error: An agent already replied to this thread. Use --force to reply anyway.",
                      file=sys.stderr)
                return 3
            print("Warning: Posting duplicate reply (--force used).", file=sys.stderr)

        if args.check_only:
            print("No existing agent reply found.", file=sys.stderr)
            return 0

    # Format the reply with prefix
    formatted_body = format_reply(args.name, args.body)

    # Post the reply
    try:
        if args.comment_id:
            post_review_comment_reply(owner, repo, pr_num, args.comment_id, formatted_body)
        else:
            post_issue_comment(owner, repo, pr_num, formatted_body)
        return 0
    except RuntimeError:
        return 2


if __name__ == '__main__':
    sys.exit(main())
