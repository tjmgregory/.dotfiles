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
- `line`: the line number **in the diff** (not the original file)
- `body`: your comment, prefixed with `[Claude]:`

### 3. Post Inline Comments

Submit all inline comments in a single review:

```bash
scripts/post_review.py <pr_url_or_number> \
  --event COMMENT \
  --comments-file /tmp/comments.json
```

The comments file format:
```json
[
  {"path": "src/auth.ts", "line": 42, "body": "[Claude]: This null check won't catch undefined"},
  {"path": "src/api.ts", "line": 18, "body": "[Claude]: SQL injection risk—use parameterized query"}
]
```

**Review events:**
| Event | When to use |
|-------|-------------|
| `COMMENT` | Default—inline feedback only |
| `APPROVE` | No issues found, ready to merge |
| `REQUEST_CHANGES` | Blocking issues that must be fixed |

**Skip the summary body** unless there's cross-cutting feedback that doesn't belong on any specific line.

### 4. Reply to Existing Threads

Review each existing comment thread and reply where valuable:

| Thread state | Action |
|--------------|--------|
| Unanswered question | Answer if you can help |
| Ongoing discussion | Add perspective if useful |
| Resolved/agreed | Skip |

Reply to each thread individually:
```bash
scripts/post_review.py <pr_url_or_number> \
  --reply-to <comment_id> \
  --body "[Claude]: Your reply here" \
  --event COMMENT
```

### 5. Verify

Confirm your comments posted:
```bash
gh pr view <pr_number> --comments
```

## Writing Inline Comments

**Prefix with `[Claude]:`** — identifies automated feedback.

**Be specific** — reference the exact issue and suggest a fix:
```
[Claude]: This could throw if `user` is null. Consider:
```suggestion
if (user?.email) {
```
```

**Prioritize** — distinguish blockers from suggestions:
```
[Claude]: Blocker: This exposes the API key in logs.
```
```
[Claude]: Nit: Could rename to `fetchUserData` for clarity.
```

**Ask questions** when intent is unclear:
```
[Claude]: What happens if this returns an empty array? Should we handle that case?
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
- **Don't duplicate** — check existing threads before commenting
- **Read before commenting** — understand context before critiquing
