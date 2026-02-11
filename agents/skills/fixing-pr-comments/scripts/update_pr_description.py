#!/usr/bin/env python3
"""
Append a "Comments Addressed" section to a PR description.

Usage (CLI args):
    update_pr_description.py <pr> --summary "- Fixed null check\\n- Added error handling"

Usage (JSON stdin - preferred for AI agents):
    update_pr_description.py <<'EOF'
    {"pr": "123", "summary": "- Fixed null check\n- Added error handling"}
    EOF

JSON input fields:
    pr/pr_ref: PR number or URL (required)
    summary: Summary of changes made (required)
    replace: Boolean, replace existing section instead of appending

The script safely appends to existing PR body without overwriting.

Outputs JSON to stdout:
    Success: {"status": "ok", "action": "created|appended|replaced", "pr_number": 123}
    Error:   {"error": "message"}

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


def output_json(data: dict) -> None:
    """Output structured JSON to stdout."""
    print(json.dumps(data))


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


def parse_args():
    """Parse arguments from stdin JSON or CLI args."""
    # Check for JSON input via stdin (AI-friendly mode)
    if not sys.stdin.isatty():
        try:
            data = json.load(sys.stdin)
            pr_ref = data.get("pr") or data.get("pr_ref")
            summary = data.get("summary")

            # Validate required fields
            if not pr_ref:
                print("Error: Missing required field 'pr' or 'pr_ref'", file=sys.stderr)
                output_json({"error": "Missing required field 'pr' or 'pr_ref'"})
                sys.exit(1)
            if not summary:
                print("Error: Missing required field 'summary'", file=sys.stderr)
                output_json({"error": "Missing required field 'summary'"})
                sys.exit(1)

            # Create a namespace object to match argparse interface
            class Args:
                pass
            args = Args()
            args.pr_ref = pr_ref
            args.summary = summary
            args.replace = data.get("replace", False)
            return args
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
            output_json({"error": f"Invalid JSON input: {e}"})
            sys.exit(1)

    # Fallback to CLI args (human-friendly mode)
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

    return parser.parse_args()


def main():
    args = parse_args()

    try:
        owner, repo, pr_num = parse_pr_reference(args.pr_ref)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        output_json({"error": str(e)})
        return 1

    # Fetch current body
    try:
        current_body = get_pr_body(owner, repo, pr_num)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        output_json({"error": str(e)})
        return 2

    # Process summary (convert literal \n to newlines)
    summary = args.summary.replace('\\n', '\n')

    # Build the new section
    section_header = "## Comments Addressed"
    new_section = f"\n\n---\n{section_header}\n{summary}"

    # Check if section already exists
    section_existed = section_header in current_body
    if section_existed:
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
        action = "replaced" if (section_existed and args.replace) else "appended" if section_existed else "created"
        output_json({"status": "ok", "action": action, "pr_number": int(pr_num)})
        return 0
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        output_json({"error": str(e)})
        return 2


if __name__ == '__main__':
    sys.exit(main())
