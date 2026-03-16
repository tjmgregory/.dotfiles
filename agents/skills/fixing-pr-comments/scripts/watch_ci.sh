#!/usr/bin/env bash
#
# Watch GitHub Actions checks for a PR until all complete.
#
# Usage: watch_ci.sh <pr_url_or_number>
#
# Outputs JSON to stdout:
#   {
#     "conclusion": "success|failure",
#     "checks": [{"name": "...", "conclusion": "..."}],
#     "failed_runs": [123, 456]   <- use with: gh run view <id> --log-failed
#   }
#
# Exit codes: 0=all passed, 1=some failed, 3=error

set -euo pipefail

PR_REF="${1:-}"
[[ -z "$PR_REF" ]] && { echo "Usage: $0 <pr_url_or_number>" >&2; exit 3; }

echo "Watching CI checks for PR $PR_REF..." >&2

# Watch until all checks complete; show progress on stderr
gh pr checks "$PR_REF" --watch --interval 15 >&2 || true

# Collect structured results
CHECKS=$(gh pr checks "$PR_REF" --json name,conclusion,detailsUrl 2>/dev/null || echo "[]")

echo "$CHECKS" | jq '{
    conclusion: (
        if ([.[] | select(.conclusion | . != null and ascii_downcase != "success" and ascii_downcase != "skipped" and ascii_downcase != "neutral")] | length) > 0
        then "failure" else "success" end
    ),
    checks: [.[] | {name: .name, conclusion: .conclusion}],
    failed_runs: [
        .[]
        | select(.conclusion | . != null and ascii_downcase != "success" and ascii_downcase != "skipped" and ascii_downcase != "neutral")
        | (.detailsUrl // "") | split("/runs/")
        | if length > 1 then .[1] | split("/") | .[0] | tonumber? else empty end
    ] | map(select(. != null))
}'

CONCLUSION=$(echo "$CHECKS" | jq -r '
    if ([.[] | select(.conclusion | . != null and ascii_downcase != "success" and ascii_downcase != "skipped" and ascii_downcase != "neutral")] | length) > 0
    then "failure" else "success" end')
[[ "$CONCLUSION" == "success" ]] && exit 0 || exit 1
