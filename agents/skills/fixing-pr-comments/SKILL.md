---
name: fixing-pr-comments
description: Addresses GitHub PR review comments by assessing each one, making code changes where valid, and replying to every thread. Use when asked to "fix PR comments", "address review feedback", "respond to PR review", "handle PR comments", or given a PR with unaddressed reviewer comments.
---

# Fixing PR Comments

Address PR review comments: assess validity, make changes, reply to each thread.

**Process**: Fetch comments → Assess each → Plan edits → Edit code → Commit → Push → Reply to all

## Workflow

### 1. Fetch PR and Comments

```bash
scripts/fetch_comments.sh <pr_url_or_number>
```

Returns JSON with:
- `info` — PR metadata (title, branch, head SHA)
- `review_comments` — Inline comments on code (have file path + line)
- `issue_comments` — General PR discussion
- `reviews` — Review body comments (the top-level message submitted with approve/request changes/comment, filtered to non-empty bodies)

### 2. Assess Each Comment

Process all three comment types: `review_comments` (inline on code), `issue_comments` (general discussion), and `reviews` (review body comments). Prioritize inline comments first, then review bodies, then general discussion.

Categorize before acting. See [references/reply-templates.md](references/reply-templates.md) for examples.

| Assessment | Action | Reply |
|------------|--------|-------|
| Valid & actionable | Make change | Confirm what changed |
| Valid, disagree | No change | Technical rationale |
| Invalid / N/A | No change | Explain why |
| Unclear | No change | Ask clarifying question |

**Skip threads where an agent already replied** (look for `[🤖` prefix) unless someone followed up after.

### 3. Plan All Changes

List changes BEFORE editing — line numbers shift after edits.

For inline review comments requiring code changes:
1. Note file path and line number (`line` field = line in PR head branch)
2. Read the file to understand context
3. Plan the specific edit

For review bodies and issue comments requiring code changes:
1. Identify which files/code the comment refers to (may need to search)
2. Read the relevant files to understand context
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

### 6. Reply to Each Thread

For review comments (inline on code):
```bash
scripts/post_reply.py <<'EOF'
{"pr": "123", "comment_id": 456, "role": "Author", "model": "<your model name>", "body": "Your reply"}
EOF
```

For issue comments (general discussion):
```bash
scripts/post_reply.py <<'EOF'
{"pr": "123", "issue_comment_id": 789, "role": "Author", "model": "<your model name>", "body": "Your reply"}
EOF
```

For review bodies (submitted with approve/request changes/comment):
```bash
scripts/post_reply.py <<'EOF'
{"pr": "123", "review_id": 101, "role": "Author", "model": "<your model name>", "body": "Your reply"}
EOF
```
Posts as an issue comment (no "reply to review" API). Duplicate detection compares the review's `submitted_at` against issue comments to avoid double-replying.

The script:
- Adds `[🤖 {role} - {model}]:` prefix automatically
- Prevents double-replies (add `"force": true` to override)

## Re-runs

If invoked again on the same PR (e.g. to check for new comments after addressing previous ones):
1. Re-run `scripts/fetch_comments.sh` to get the full fresh data
2. Read the JSON output directly to identify any new/unaddressed comments
3. **Do NOT pipe the output through inline python3 or jq filters** — just use the fetch script and read the result

## Rules

- **Reply to ALL comments** — every inline thread and top-level comment gets a response
- **Inline first, then root** — prioritize inline review comments, then address top-level PR comments
- **Push before replying** — ensures code changes are visible when reviewer reads reply
- **Plan before editing** — avoids line number drift issues
- **Never skip unclear comments** — ask for clarification instead
- **Never use `!=` in inline Bash commands** — zsh escapes `!` to `\!` inside double-quoted strings, breaking python3 -c, jq, and similar inline scripts. Use the provided scripts or heredocs with single-quoted delimiters instead
