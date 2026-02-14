#!/usr/bin/env bash
#
# Fetch PR info and all comments (review + issue + review bodies) with pagination.
# Usage: fetch_comments.sh <pr_url_or_number>
#
# Outputs JSON: { info, review_comments, issue_comments, reviews }
# Review comments have line numbers; issue comments are general PR discussion;
# reviews are the top-level body submitted with each review (approve/request changes/comment).

set -euo pipefail

usage() {
    echo "Usage: $0 <pr_url_or_number>"
    echo ""
    echo "Examples:"
    echo "  $0 123"
    echo "  $0 https://github.com/owner/repo/pull/123"
    exit 1
}

if [[ $# -lt 1 ]]; then
    usage
fi

PR_REF="$1"

# Extract owner/repo/number from URL or infer from git remote
if [[ "$PR_REF" =~ github\.com/([^/]+)/([^/]+)/pull/([0-9]+) ]]; then
    OWNER="${BASH_REMATCH[1]}"
    REPO="${BASH_REMATCH[2]}"
    PR_NUM="${BASH_REMATCH[3]}"
else
    PR_NUM="$PR_REF"
    REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")

    if [[ -z "$REMOTE_URL" ]]; then
        echo "Error: Not in a git repository and no full PR URL provided" >&2
        exit 1
    fi

    if [[ "$REMOTE_URL" =~ github\.com[:/]([^/]+)/(.+) ]]; then
        OWNER="${BASH_REMATCH[1]}"
        REPO="${BASH_REMATCH[2]}"
        REPO="${REPO%.git}"
    else
        echo "Error: Could not parse GitHub owner/repo from remote: $REMOTE_URL" >&2
        exit 1
    fi
fi

if ! [[ "$PR_NUM" =~ ^[0-9]+$ ]]; then
    echo "Error: Invalid PR number: $PR_NUM" >&2
    exit 1
fi

echo "Fetching PR #$PR_NUM from $OWNER/$REPO..." >&2

# Fetch all data
INFO=$(gh pr view "$PR_NUM" --repo "$OWNER/$REPO" \
    --json number,title,body,headRefName,baseRefName,headRefOid,author,url,state 2>/dev/null)

echo "Fetching review comments..." >&2
REVIEW_COMMENTS=$(gh api --paginate "repos/$OWNER/$REPO/pulls/$PR_NUM/comments" 2>/dev/null || echo "[]")

echo "Fetching issue comments..." >&2
ISSUE_COMMENTS=$(gh api --paginate "repos/$OWNER/$REPO/issues/$PR_NUM/comments" 2>/dev/null || echo "[]")

echo "Fetching reviews..." >&2
REVIEWS=$(gh api --paginate "repos/$OWNER/$REPO/pulls/$PR_NUM/reviews" 2>/dev/null || echo "[]")

# Output structured JSON
if command -v jq &>/dev/null; then
    jq -n \
        --argjson info "$INFO" \
        --argjson review_comments "$REVIEW_COMMENTS" \
        --argjson issue_comments "$ISSUE_COMMENTS" \
        --argjson reviews "$REVIEWS" \
        --arg owner "$OWNER" \
        --arg repo "$REPO" \
        '{
            owner: $owner,
            repo: $repo,
            info: $info,
            review_comments: $review_comments,
            issue_comments: $issue_comments,
            reviews: [$reviews[] | select(.body != null and .body != "")]
        }'
else
    echo "=== PR INFO ==="
    echo "$INFO"
    echo ""
    echo "=== REVIEW COMMENTS ==="
    echo "$REVIEW_COMMENTS"
    echo ""
    echo "=== ISSUE COMMENTS ==="
    echo "$ISSUE_COMMENTS"
    echo ""
    echo "=== REVIEWS ==="
    echo "$REVIEWS"
fi

echo "Done." >&2
