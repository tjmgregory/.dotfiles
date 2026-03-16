#!/usr/bin/env python3
"""
Post multiple PR comment replies in parallel.

Usage (JSON array via stdin):
    post_replies_batch.py <<'EOF'
    [
        {"pr": "123", "comment_id": 456, "role": "Author", "model": "claude-sonnet-4-6", "body": "Reply"},
        {"pr": "123", "issue_comment_id": 789, "role": "Author", "model": "claude-sonnet-4-6", "body": "Reply"},
        {"pr": "123", "review_id": 101, "role": "Author", "model": "claude-sonnet-4-6", "body": "Reply"}
    ]
    EOF

Each item uses the same fields as post_reply.py.
Outputs a JSON array of results in input order.
Exit code: 0 if all succeeded, 1 if any failed.
"""

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
POST_REPLY = SCRIPT_DIR / "post_reply.py"
MAX_WORKERS = 8


def post_one(item: dict) -> dict:
    """Invoke post_reply.py for a single reply item."""
    try:
        result = subprocess.run(
            [sys.executable, str(POST_REPLY)],
            input=json.dumps(item),
            capture_output=True,
            text=True
        )
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        if result.stdout.strip():
            return json.loads(result.stdout)
        return {"error": "No output from post_reply.py", "item": item}
    except json.JSONDecodeError as e:
        return {"error": f"Could not parse post_reply.py output: {e}", "raw": result.stdout}
    except Exception as e:
        return {"error": str(e), "item": item}


def main() -> int:
    if sys.stdin.isatty():
        print("Error: JSON array required via stdin", file=sys.stderr)
        print("Usage: post_replies_batch.py <<'EOF'", file=sys.stderr)
        print('[{"pr": "123", "comment_id": 456, "body": "reply"}, ...]', file=sys.stderr)
        print("EOF", file=sys.stderr)
        return 1

    try:
        items = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        return 1

    if not isinstance(items, list):
        print("Error: Input must be a JSON array", file=sys.stderr)
        return 1

    if not items:
        print(json.dumps([]))
        return 0

    print(f"Posting {len(items)} replies in parallel...", file=sys.stderr)

    results = [None] * len(items)
    workers = min(len(items), MAX_WORKERS)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_index = {executor.submit(post_one, item): i for i, item in enumerate(items)}
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            results[idx] = future.result()

    print(json.dumps(results, indent=2))

    errors = [r for r in results if r and r.get("error")]
    if errors:
        print(f"\n{len(errors)} reply(ies) failed.", file=sys.stderr)
        return 1

    print(f"All {len(items)} replies posted successfully.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
