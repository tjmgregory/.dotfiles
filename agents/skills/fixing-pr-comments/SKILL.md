---
name: fixing-pr-comments
description: Addresses GitHub PR review comments by assessing each one, making code changes where valid, and replying to every thread. Use when asked to "fix PR comments", "address review feedback", "respond to PR review", "handle PR comments", or given a PR with unaddressed reviewer comments.
---

# Fixing PR Comments

Address PR review comments: assess validity, make changes, reply to each thread.

**Process**: Fetch comments → Assess each → Plan edits → Edit code → Commit → Push → Update PR → Reply to all

## Workflow

### 1. Fetch PR and Comments

```bash
scripts/fetch_comments.sh <pr_url_or_number>
```

Returns JSON with:
- `info` — PR metadata (title, branch, head SHA)
- `review_comments` — Inline comments on code (have file path + line)
- `issue_comments` — General PR discussion

### 2. Assess Each Comment

Categorize before acting. See [references/reply-templates.md](references/reply-templates.md) for examples.

| Assessment | Action | Reply |
|------------|--------|-------|
| Valid & actionable | Make change | Confirm what changed |
| Valid, disagree | No change | Technical rationale |
| Invalid / N/A | No change | Explain why |
| Unclear | No change | Ask clarifying question |

**Skip threads where Claude already replied** (look for `[Claude]:` prefix) unless someone followed up after.

### 3. Plan All Changes

List changes BEFORE editing — line numbers shift after edits.

For each comment requiring code changes:
1. Note file path and line number (`line` field = line in PR head branch)
2. Read the file to understand context
3. Plan the specific edit

### 4. Edit Code and Commit

Make all planned edits, then:

```bash
git add <specific-files>
git commit -m "Address PR review comments"
```

### 5. Push Changes

```bash
git push
```

### 6. Update PR Description

```bash
scripts/update_pr_description.py <pr> --summary "- Fixed X\n- Added Y"
```

Keep summary brief — one line per change made.

### 7. Reply to Each Thread

For review comments (inline on code):
```bash
scripts/post_reply.py <pr> --comment-id <id> --name Claude --body "Your reply"
```

For issue comments (general discussion):
```bash
scripts/post_reply.py <pr> --issue-comment-id <id> --name Claude --body "Your reply"
```

The script:
- Adds `[🤖 {name}]:` prefix automatically
- Prevents double-replies (use `--force` to override)

## Rules

- **Reply to ALL comments** — every thread gets a response
- **Push before replying** — ensures code changes are visible when reviewer reads reply
- **Plan before editing** — avoids line number drift issues
- **Never skip unclear comments** — ask for clarification instead
