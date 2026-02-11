#!/usr/bin/env python3
"""
Append a "Comments Addressed" section to a PR description.

Usage:
    update_pr_description.py <pr> --summary "- Fixed null check\n- Added error handling"

The script safely appends to existing PR body without overwriting.

Exit codes:
    0 - Success
    1 - Invalid arguments
    2 - GitHub API error
"""

import argparse
import subprocess
import sys
import re
import json


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


def get_pr_body(owner: str, repo: str, pr_num: str) -> str:
    """Fetch current PR body."""
    cmd = ['gh', 'pr', 'view', pr_num, '--repo', f'{owner}/{repo}', '--json', 'body', '-q', '.body']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to fetch PR body: {e.stderr}")


def update_pr_body(owner: str, repo: str, pr_num: str, new_body: str) -> None:
    """Update PR body."""
    cmd = ['gh', 'pr', 'edit', pr_num, '--repo', f'{owner}/{repo}', '--body', new_body]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"PR description updated.", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to update PR body: {e.stderr}")


def main():
    parser = argparse.ArgumentParser(
        description='Append "Comments Addressed" section to PR description.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('pr_ref', help='PR number or full GitHub PR URL')
    parser.add_argument('--summary', required=True,
                        help='Summary of changes made (supports \\n for newlines)')
    parser.add_argument('--replace', action='store_true',
                        help='Replace existing "Comments Addressed" section instead of appending')

    args = parser.parse_args()

    try:
        owner, repo, pr_num = parse_pr_reference(args.pr_ref)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Fetch current body
    try:
        current_body = get_pr_body(owner, repo, pr_num)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    # Process summary (convert literal \n to newlines)
    summary = args.summary.replace('\\n', '\n')

    # Build the new section
    section_header = "## Comments Addressed"
    new_section = f"\n\n---\n{section_header}\n{summary}"

    # Check if section already exists
    if section_header in current_body:
        if args.replace:
            # Replace existing section (everything from header to next --- or end)
            pattern = rf'\n*---\n{re.escape(section_header)}.*?(?=\n---|\Z)'
            new_body = re.sub(pattern, new_section, current_body, flags=re.DOTALL)
        else:
            # Append to existing section
            pattern = rf'({re.escape(section_header)}.*?)(?=\n---|\Z)'
            match = re.search(pattern, current_body, flags=re.DOTALL)
            if match:
                existing = match.group(1)
                updated = f"{existing}\n{summary}"
                new_body = current_body.replace(existing, updated)
            else:
                new_body = current_body + new_section
    else:
        new_body = current_body + new_section

    # Update the PR
    try:
        update_pr_body(owner, repo, pr_num, new_body)
        return 0
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
