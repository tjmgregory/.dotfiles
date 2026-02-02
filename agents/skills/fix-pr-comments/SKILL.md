---
name: fix-pr-comments
description: Address comments on a GitHub PR. Reply directly to comment threads where possible. Fetches all comments, plans changes, makes code changes, commits, and replies to each thread.
license: MIT
metadata:
  version: "1.0.0"
---

# Fix PR Comments

Address comments on a GitHub PR. Reply directly to comment threads where possible.

## Important Instructions

1. **Reply directly to comment threads**: Use the GitHub API to reply DIRECTLY to each review comment thread. NEVER create new PR-level comments as responses to line comments.

2. **MANDATORY: Prefix ALL comments**: EVERY comment you write MUST be prefixed with "[Claude]: " to distinguish from human comments.

3. **Complete workflow for addressing PR comments**:

   a. **Get PR details**:
      ```bash
      gh pr view --json number,headRepositoryOwner,headRepository -q '{number: .number, owner: .headRepositoryOwner.login, repo: .headRepository.name}'
      ```

   b. **Fetch ALL comments** (CRITICAL: GitHub API is paginated - you MUST get ALL pages):
      - Review comments: `gh api repos/{owner}/{repo}/pulls/{pull_number}/comments --paginate`
      - PR issue comments: `gh api repos/{owner}/{repo}/issues/{pull_number}/comments --paginate`
      - Review threads: `gh api repos/{owner}/{repo}/pulls/{pull_number}/reviews --paginate`

      **PAGINATION WARNING**:
      - The GitHub API returns max 100 items per page by default
      - Use `--paginate` flag to automatically fetch ALL pages
      - **You MUST ensure you have ALL comments before proceeding**

   c. **CRITICAL: Get original context and create a complete plan BEFORE making ANY changes**:
      - Read EVERY comment carefully - DO NOT MISS ANY
      - **For comments with line numbers**:
        - Each comment includes a `commit_id` or `original_commit_id` field
        - Line numbers refer to the file at THAT specific commit, NOT the current file
        - You MUST fetch the file content from that commit:
          ```bash
          gh api repos/{owner}/{repo}/contents/{path}?ref={commit_sha}
          # OR use git to check out that specific version:
          git show {commit_sha}:{file_path}
          ```
      - For each comment, assess your understanding:
        - **Fully understand**: Proceed with planning the change
        - **Any confusion**: Do NOT attempt the change. Instead, reply asking for clarification and leave unresolved
      - Note the exact line numbers and file paths referenced in each comment AT THE COMMIT THEY REFERENCE
      - Plan out all changes needed for comments you understand
      - Use TodoWrite tool to track each change you need to make
      - **WARNING**: Once you start editing files, line numbers will shift! You MUST understand all changes before starting

   d. **Make the requested code changes**: Execute your plan by addressing each comment systematically

   e. **Commit and push changes**:
      ```bash
      git add -A
      git commit -m "Address PR review comments"
      git push
      ```

   f. **Reply to EACH comment thread individually** after pushing:

      **CRITICAL**: You MUST reply DIRECTLY to each review comment thread. The correct approach depends on the comment type:

      **For Review Comments (comments with `pull_request_review_id`):**
      - Use: `gh api repos/{owner}/{repo}/pulls/{pull_number}/comments -X POST --field body="[Claude]: Your reply here" --field in_reply_to={comment_id}`
      - This creates proper threaded replies within the review comment discussion
      - Each reply will show `"in_reply_to_id": {original_comment_id}` in the response

      **For Standalone Comments (comments without `pull_request_review_id`):**
      - Use: `gh api repos/{owner}/{repo}/pulls/comments/{comment_id}/replies -X POST -f body="[Claude]: Your reply here"`
      - This is rare - most PR comments are review comments

      **NEVER use `/issues/{issue_number}/comments`** - this creates general PR comments, not threaded replies!

      **Reply Examples:**
      - Simple changes: `[Claude]: Done`
      - Complex changes: `[Claude]: Refactored the validation logic to handle edge cases as requested`
      - Confusion: `[Claude]: I need clarification on this comment. Could you please elaborate on [specific confusion]?`

   **IMPORTANT**:
   - Make a SEPARATE API call for EACH comment thread
   - ALWAYS check if you got ALL comments by counting them and verifying none are missed
   - The `--field` parameter properly handles data types (use `--field` not `-f`)

4. **Address all types of comments**:
   - Line-specific comments (review comments)
   - File-level comments
   - PR-wide review comments
   - General PR comments (issue comments)

5. **Critical requirements**:
   - **ALWAYS push your changes** before replying to comments (only for comments you understood and addressed)
   - **Reply to EVERY SINGLE comment individually IN ITS THREAD**:
     - Use the correct API endpoint for the comment type
     - Make separate API calls for each comment - no batching!
     - Simple changes: Just reply "[Claude]: Done"
     - Complex changes: "[Claude]: " + explanation of what you changed
     - Confused: "[Claude]: " + ask for clarification and don't make changes
   - **Never skip comments** - either address them or ask for clarification
   - **Don't over-explain** - simple fixes don't need explanations
   - **VERIFY you replied to ALL comments** - missing even one comment is unacceptable

6. **Debugging GitHub API Issues**:
   - If `/pulls/comments/{id}/replies` returns 404, the comment is likely a review comment (has `pull_request_review_id`)
   - Review comments need the `in_reply_to` approach: `/pulls/{pull_number}/comments` with `--field in_reply_to={comment_id}`
   - Use `--field` instead of `-f` for proper data type handling
   - Always check the response for `"in_reply_to_id"` to confirm proper threading

## Workflow Summary

1. Fetch ALL comments (use --paginate to get every page!)
2. **PLAN all changes** (before any edits, while line numbers are still accurate!)
3. Make all code changes according to your plan
4. Commit and push
5. Reply to each comment individually using the correct API endpoint

**NEVER MISS A COMMENT**: PRs can have 100+ comments across multiple pages. Missing even one comment is unacceptable.

**ALWAYS IDENTIFY YOURSELF**: Every single comment MUST start with "[Claude]: " - no exceptions!

**USE CORRECT API ENDPOINTS**: Review comments (most common) need `--field in_reply_to={comment_id}` approach, not `/replies`.
