---
name: reviewing-prs
description: Reviews GitHub PRs by analyzing diffs file-by-file and posting inline comments directly on diff lines. Use when asked to "review PR", "review this PR", "give feedback on PR", or when given a PR URL/number to review.
---

# Reviewing PRs

Review PRs file-by-file, posting inline comments directly on diff lines. Inline comments are the primary output—they're actionable, trackable, and tied to specific code. Summary comments are rarely needed.

**Process**: Fetch data → Review each file → Post inline comments → Reply to threads → Verify

## Workflow

### 1. Fetch PR Data

```bash
scripts/fetch_pr_data.sh <pr_url_or_number>
```

This returns PR info, the full diff, and all existing comment threads.

### 2. Review Each File

Go through the diff **file by file**. For each changed file:

1. **Read the diff hunk** — understand what changed
2. **Read base branch context if needed** — when the diff references code you can't see:
   ```bash
   gh api repos/{owner}/{repo}/contents/{path}?ref={base_branch} | jq -r .content | base64 --decode
   ```
3. **Identify issues** — bugs, security holes, performance problems, missing edge cases
4. **Note the exact diff line numbers** for each issue (these go in your inline comments)

Build up a list of inline comments as you go. Each comment needs:
- `path`: the file path
- `line`: the line number in the **new version** of the file (the `+` lines in the diff)
- `body`: your comment (the script auto-prefixes with `[🤖 Reviewer - <model>]:`)

**Do NOT manually add a prefix** — the `post_review.py` script injects `[🤖 {role} - {model}]:` automatically.

### 3. Post Inline Comments

Submit all inline comments in a single review via JSON stdin. Pass `role` and `model` so the script auto-prefixes each comment:

```bash
scripts/post_review.py <<'EOF'
{
  "pr": "<pr_url_or_number>",
  "event": "COMMENT",
  "role": "Reviewer",
  "model": "<your model name>",
  "comments": [
    {"path": "src/auth.ts", "line": 42, "body": "This null check won't catch undefined"},
    {"path": "src/api.ts", "line": 18, "body": "SQL injection risk—use parameterized query"}
  ]
}
EOF
```

**Review events:**
| Event | When to use |
|-------|-------------|
| `COMMENT` | Default—inline feedback only |
| `APPROVE` | No issues found, ready to merge |
| `REQUEST_CHANGES` | Blocking issues that must be fixed |

**Skip the summary body** unless there's cross-cutting feedback that doesn't belong on any specific line.

### 4. Reply to Existing Threads

**First, check for threads awaiting your input.** Look for:
- Threads where the last comment mentions the reviewer or asks a question
- Threads where someone replied to a previous `[🤖` prefixed comment
- Unresolved discussions that could benefit from technical input

**Then, avoid double-replying.** Before replying to any thread:
1. Check if any comment in that thread starts with `[🤖`
2. If an agent already replied AND no one asked a follow-up → skip
3. If someone replied after the agent's comment → consider responding

| Thread state | Action |
|--------------|--------|
| Question directed at agent | Reply |
| Follow-up after agent's comment | Reply if asked or helpful |
| Agent already replied, no follow-up | Skip |
| Resolved/agreed | Skip |

Reply to each thread individually (the script auto-prefixes the body):
```bash
scripts/post_review.py <<'EOF'
{
  "pr": "<pr_url_or_number>",
  "reply_to": <comment_id>,
  "role": "Reviewer",
  "model": "<your model name>",
  "body": "Your reply here"
}
EOF
```

### 5. Verify

Confirm your comments posted:
```bash
gh pr view <pr_number> --comments
```

## Writing Inline Comments

The `post_review.py` script **automatically prefixes** each comment with `[🤖 Reviewer - <model>]:`. Write comment bodies without any prefix.

**Be specific** — reference the exact issue and suggest a fix:
```
This could throw if `user` is null. Consider:
```suggestion
if (user?.email) {
```
```

**Prioritize** — distinguish blockers from suggestions:
```
Blocker: This exposes the API key in logs.
```
```
Nit: Could rename to `fetchUserData` for clarity.
```

**Ask questions** when intent is unclear:
```
What happens if this returns an empty array? Should we handle that case?
```

See [references/comment-templates.md](references/comment-templates.md) for more templates.

## Handle Errors

| Error | Cause | Fix |
|-------|-------|-----|
| 422 Unprocessable | Line number not in diff | Use diff line numbers, not file line numbers |
| 404 Not Found | PR doesn't exist or no access | Check PR URL and permissions |
| 401/403 | Auth issue | Run `gh auth status` |

## Rules

- **Inline comments are primary** — put feedback on specific lines, not in summary
- **One review submission** — batch all new comments together
- **Reply individually** — each thread reply is a separate call
- **Never double-comment** — before posting, check existing comments for `[🤖` prefix on the same path/line
- **Never double-reply** — before replying, check if an agent already replied to that thread (look for `[🤖` prefix)
- **Prioritize awaiting threads** — respond to threads where someone asked a question or replied to an agent comment
- **Read before commenting** — understand context before critiquing
