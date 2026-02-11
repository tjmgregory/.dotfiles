#!/usr/bin/env bash
#
# Fetch all PR data: info, diff, and comments (with pagination)
# Usage: fetch_pr_data.sh <pr_url_or_number> [--diff-only|--comments-only|--info-only]
#
# Outputs JSON with sections: info, diff, review_comments, issue_comments
# Handles pagination automatically via gh --paginate

set -euo pipefail

usage() {
    echo "Usage: $0 <pr_url_or_number> [--diff-only|--comments-only|--info-only]"
    echo ""
    echo "Examples:"
    echo "  $0 123                    # Fetch all data for PR #123"
    echo "  $0 https://github.com/owner/repo/pull/123"
    echo "  $0 123 --diff-only        # Fetch only the diff"
    echo "  $0 123 --comments-only    # Fetch only comments"
    exit 1
}

# Require at least one argument
if [[ $# -lt 1 ]]; then
    usage
fi

PR_REF="$1"
MODE="${2:-all}"

# Extract owner/repo from current directory or PR URL
if [[ "$PR_REF" =~ github\.com/([^/]+)/([^/]+)/pull/([0-9]+) ]]; then
    OWNER="${BASH_REMATCH[1]}"
    REPO="${BASH_REMATCH[2]}"
    PR_NUM="${BASH_REMATCH[3]}"
else
    # Assume we're in a git repo and PR_REF is just a number
    PR_NUM="$PR_REF"
    REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")

    if [[ -z "$REMOTE_URL" ]]; then
        echo "Error: Not in a git repository and no full PR URL provided" >&2
        exit 1
    fi

    # Extract owner/repo from remote URL (handles both HTTPS and SSH, with or without .git suffix)
    if [[ "$REMOTE_URL" =~ github\.com[:/]([^/]+)/(.+) ]]; then
        OWNER="${BASH_REMATCH[1]}"
        REPO="${BASH_REMATCH[2]}"
        REPO="${REPO%.git}"  # Strip .git suffix if present
    else
        echo "Error: Could not parse GitHub owner/repo from remote: $REMOTE_URL" >&2
        exit 1
    fi
fi

# Validate PR number
if ! [[ "$PR_NUM" =~ ^[0-9]+$ ]]; then
    echo "Error: Invalid PR number: $PR_NUM" >&2
    exit 1
fi

fetch_info() {
    echo "Fetching PR info..." >&2
    gh pr view "$PR_NUM" --repo "$OWNER/$REPO" \
        --json number,title,body,headRefName,baseRefName,author,additions,deletions,changedFiles,url,state,mergeable
}

fetch_diff() {
    echo "Fetching PR diff..." >&2
    gh pr diff "$PR_NUM" --repo "$OWNER/$REPO" 2>/dev/null || echo ""
}

fetch_review_comments() {
    echo "Fetching review comments (with pagination)..." >&2
    gh api --paginate "repos/$OWNER/$REPO/pulls/$PR_NUM/comments" 2>/dev/null || echo "[]"
}

fetch_issue_comments() {
    echo "Fetching issue comments (with pagination)..." >&2
    gh api --paginate "repos/$OWNER/$REPO/issues/$PR_NUM/comments" 2>/dev/null || echo "[]"
}

# Execute based on mode
case "$MODE" in
    --diff-only)
        fetch_diff
        ;;
    --comments-only)
        echo "{"
        echo "  \"review_comments\": $(fetch_review_comments),"
        echo "  \"issue_comments\": $(fetch_issue_comments)"
        echo "}"
        ;;
    --info-only)
        fetch_info
        ;;
    all|*)
        # Build complete JSON output
        INFO=$(fetch_info)
        DIFF=$(fetch_diff)
        REVIEW_COMMENTS=$(fetch_review_comments)
        ISSUE_COMMENTS=$(fetch_issue_comments)

        # Use jq to build proper JSON if available, otherwise manual construction
        if command -v jq &>/dev/null; then
            jq -n \
                --argjson info "$INFO" \
                --arg diff "$DIFF" \
                --argjson review_comments "$REVIEW_COMMENTS" \
                --argjson issue_comments "$ISSUE_COMMENTS" \
                '{
                    info: $info,
                    diff: $diff,
                    review_comments: $review_comments,
                    issue_comments: $issue_comments
                }'
        else
            # Fallback: output sections separately (less ideal but works)
            echo "=== PR INFO ==="
            echo "$INFO"
            echo ""
            echo "=== DIFF ==="
            echo "$DIFF"
            echo ""
            echo "=== REVIEW COMMENTS ==="
            echo "$REVIEW_COMMENTS"
            echo ""
            echo "=== ISSUE COMMENTS ==="
            echo "$ISSUE_COMMENTS"
        fi
        ;;
esac

echo "Done fetching PR data." >&2
