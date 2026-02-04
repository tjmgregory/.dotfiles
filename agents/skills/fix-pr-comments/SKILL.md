---
name: fix-pr-comments
description: Address comments on a GitHub PR. Reply directly to comment threads where possible. Fetches all comments, plans changes, makes code changes, commits, and replies to each thread.
---

# Fix PR Comments

Address GitHub PR comments by assessing each one, making valid changes, and replying with rationale.

## Workflow

1. **Fetch PR info and ALL comments** (use `--paginate` for all pages):
   ```bash
   gh pr view --json number,headRepositoryOwner,headRepository
   gh api repos/{owner}/{repo}/pulls/{pr}/comments --paginate
   gh api repos/{owner}/{repo}/issues/{pr}/comments --paginate
   ```

2. **Assess each comment** using this framework:

   | Assessment | Action | Reply |
   |------------|--------|-------|
   | **Valid & clear** | Make the change | Brief summary of change |
   | **Valid but disagree** | No change | Technical rationale for current approach |
   | **Invalid/incorrect** | No change | Explain why suggestion doesn't apply |
   | **Unclear** | No change | Ask clarifying question |

3. **For comments with line numbers**: Fetch file at the referenced commit (line numbers are commit-specific):
   ```bash
   git show {commit_id}:{file_path}
   ```

4. **Plan ALL changes before editing** — line numbers shift once you start editing.

5. **Make changes, commit, push**:
   ```bash
   git add <specific-files>
   git commit -m "Address PR review comments"
   git push
   ```

6. **Reply to EACH comment thread** using the correct endpoint:
   ```bash
   # For review comments (have pull_request_review_id):
   gh api repos/{owner}/{repo}/pulls/{pr}/comments -X POST \
     --field body="[🤖 YourName]: Your reply" \
     --field in_reply_to={comment_id}

   # For issue comments (general PR comments):
   gh api repos/{owner}/{repo}/issues/{pr}/comments -X POST \
     -f body="[🤖 YourName]: Your reply"
   ```

## Reply Templates

Use `[🤖 YourName]:` prefix where "YourName" is your AI model name (e.g., Claude, GPT, Gemini).

**Change made:**
```
[🤖 YourName]: Done — updated X to use Y as suggested.
```

**Valid but disagree:**
```
[🤖 YourName]: Keeping the current approach because [technical reason].
The suggestion would [tradeoff/issue]. Happy to discuss further.
```

**Invalid/doesn't apply:**
```
[🤖 YourName]: No change made — [explain why suggestion doesn't apply,
e.g., "this code path only handles X case" or "Y is already handled at line Z"].
```

**Need clarification:**
```
[🤖 YourName]: Could you clarify [specific question]?
I want to make sure I address this correctly.
```

## Critical Rules

- **`[🤖 YourName]:`** prefix on EVERY reply — substitute your AI name (Claude, GPT, etc.)
- **Reply to ALL comments** — each gets its own API call
- **Push before replying** — changes must be committed first
- **Use `--field in_reply_to`** for review comments (not `/replies` endpoint)
