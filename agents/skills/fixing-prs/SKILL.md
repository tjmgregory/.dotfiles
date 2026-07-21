---
name: fixing-prs
description: Addresses GitHub PR review comments by assessing each one, making code changes where valid, and replying to every thread. Use when asked to "fix PR comments", "address review feedback", "respond to PR review", "handle PR comments", or given a PR with unaddressed reviewer comments.
---

# Fixing PR Comments

Address PR review comments: assess validity, make changes, reply to each thread.

**Process**: Fetch comments → Assess each → Plan edits → Edit code → Commit → Push → Watch CI → Reply to all

## Workflow

### 1. Fetch PR and Comments

```bash
scripts/fetch_comments.py <pr_url_or_number>
```

Uses the GraphQL reviewThreads API, so every thread arrives as a complete conversation (all replies, resolved/outdated state) with full pagination. Outputs a compact digest:

- Header: PR title, branch, head SHA, then `actionable:` and `hidden:` count lines
- `=== REVIEW THREADS ===` — inline code threads: `[comment:N] path:line | STATUS` header, then the conversation (root comment first, replies marked `↳`, comments newer than our last reply marked `● NEW`)
- `=== REVIEW BODIES ===` — top-level review messages: `[review:N] @author STATE | STATUS`
- `=== ISSUE COMMENTS ===` — general PR discussion: `[issue_comment:N] @author | STATUS`

**The `[kind:N]` label is the reply target**: reply to `[comment:N]` with `{"comment_id": N}` in `post_replies_batch.py`, `[review:N]` with `{"review_id": N}`, `[issue_comment:N]` with `{"issue_comment_id": N}` — no id lookup needed.

Cross-links: a thread header ends with `from review:N` when its root comment was submitted with a shown review body; review headers show `X threads (Y actionable)` so "actionable comments posted" claims reconcile against the thread list. Agent-authored comments have their `[🤖 Role - Model]` prefix lifted into the author line, e.g. `↳ @login (🤖 Author - Opus 4.6):`.

Statuses:
- `NEEDS REPLY` — no agent reply yet; must be assessed and replied to
- `FOLLOW-UP` — someone (human or reviewer bot) replied after our last reply; the `● NEW` comments are what needs re-assessing
- `HANDLED` / `(resolved)` — already dealt with; hidden by default (shown with `--all`), skip these
- `INFO` — housekeeping bot comments (ticket sync, rate-limit notices, walkthroughs); hidden by default, never need replies

Long bot boilerplate in `<details>` blocks is collapsed to `▸ summary [collapsed]` lines; the substance of a review always lives in its inline threads.

`--json` dumps the full structured data if the digest is ever insufficient.

### 2. Assess Each Comment

Every displayed item needs a response — the script already filtered out handled and resolved conversations. Prioritize review threads first, then review bodies, then issue comments.

Categorize before acting. See [references/reply-templates.md](references/reply-templates.md) for examples.

| Assessment | Action | Reply |
|------------|--------|-------|
| Valid & actionable | Make change | Confirm what changed |
| Valid, disagree | No change | Technical rationale |
| Invalid / N/A | No change | Explain why |
| Unclear | No change | Ask clarifying question |

### 3. Plan All Changes

List changes BEFORE editing — line numbers shift after edits.

For inline review comments requiring code changes:
1. Note file path and line number from the thread header (line = line in PR head branch; `(outdated)` threads reference an older diff — search for the code)
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

### 6. Watch CI and Fix Failures

After pushing, watch for check results:

```bash
scripts/watch_ci.sh <pr_url_or_number>
```

- Runs `gh pr checks --watch --interval 15` until all checks complete. Outputs JSON with each check's `conclusion` and `failed_runs` (GitHub run IDs).
- **Exit 0 (all passed)** → proceed to step 7
- **Exit 1 (failures)** → the JSON output shows which checks failed and their `run_id`s. Fix the code based on the check names — only fetch logs (`gh run view <run_id> --log-failed`) if the failure isn't obvious from the check name alone.

  **If the failure is a lint error**: always attempt automated fixes first before editing manually:
  1. Run the project's auto-fix command (e.g. `pnpm lint:fix`, `eslint --fix`, `prettier --write`, `ruff --fix`, `gofmt -w`, etc.)
  2. Check what remains unfixed, then manually fix only those residual errors
  3. Never manually edit lint errors that a tool can fix automatically

  Then:
  1. `git add <files>` and `git commit -m "Fix CI: <description>"`
  2. `git push`
  3. Re-run `scripts/watch_ci.sh` and repeat until passing
- **Exit 2 (timeout)** → proceed to step 7 anyway

### 7. Reply to All Threads

Collect all replies into a single JSON array and post them in parallel:

```bash
scripts/post_replies_batch.py <<'EOF'
[
  {"pr": "123", "comment_id": 456, "role": "Author", "model": "<your model name>", "body": "Your reply"},
  {"pr": "123", "issue_comment_id": 789, "role": "Author", "model": "<your model name>", "body": "Your reply"},
  {"pr": "123", "review_id": 101, "role": "Author", "model": "<your model name>", "body": "Your reply"}
]
EOF
```

Outputs a JSON array of results in input order. The script:
- Adds `[🤖 {role} - {model}]:` prefix automatically
- Prevents double-replies (add `"force": true` to override)
- Review body replies (`review_id`) post as issue comments (no "reply to review" API); duplicate detection uses a hidden marker

## Re-runs

If invoked again on the same PR (e.g. to check for new comments after addressing previous ones):
1. Re-run `scripts/fetch_comments.py` — anything displayed is new or reopened (`NEEDS REPLY` / `FOLLOW-UP`); handled conversations are hidden automatically
2. **Do NOT pipe the output through inline python3 or jq filters** — just run the fetch script and read the result

## Rules

- **Reply to ALL comments** — every inline thread and top-level comment gets a response
- **Inline first, then root** — prioritize inline review comments, then address top-level PR comments
- **Push before watching CI** — `watch_ci.sh` tracks the head SHA at push time
- **Push before replying** — ensures code changes are visible when reviewer reads reply
- **Batch replies** — collect all replies into one array and use `post_replies_batch.py` for parallel posting
- **Plan before editing** — avoids line number drift issues
- **Never skip unclear comments** — ask for clarification instead
- **Never use `!=` in inline Bash commands** — zsh escapes `!` to `\!` inside double-quoted strings, breaking python3 -c, jq, and similar inline scripts. Use the provided scripts or heredocs with single-quoted delimiters instead
