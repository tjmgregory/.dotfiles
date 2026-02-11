---
name: reviewing-prs
description: Reviews GitHub PRs by analyzing diffs, posting inline comments, and engaging with existing comment threads. Use when asked to "review PR", "review this PR", "give feedback on PR", or when given a PR URL/number to review.
---

# Reviewing PRs

Analyze a GitHub PR's changes, post constructive feedback, and engage with existing discussions.

**Process overview**: Fetch data → Analyze diff → Read context → Assess threads → Post review → Verify success

## Workflow

### 1. Fetch PR Data

Run the fetch script to get PR info, diff, and all comment threads:

```bash
scripts/fetch_pr_data.sh <pr_url_or_number>
```

The script handles pagination automatically and outputs structured data.

### 2. Analyze the Diff

Review the diff for:
- Logic errors or bugs
- Security vulnerabilities
- Performance concerns
- Missing edge cases
- Code clarity issues
- Inconsistencies with surrounding code style

### 3. Read Base Branch Context

Read the base branch version of files when:
- Changed code references functions/classes not visible in the diff
- You need to understand the existing pattern being modified
- Comment threads reference code you haven't seen
- The change's impact is unclear without surrounding context

```bash
gh api repos/{owner}/{repo}/contents/{path}?ref={base_branch} | jq -r .content | base64 --decode
```

### 4. Assess Existing Comment Threads

Review each thread and decide whether to reply:

| Thread State | Action |
|--------------|--------|
| Unanswered question | Answer if you can help |
| Ongoing discussion | Add perspective if valuable |
| Resolved/agreed | Skip—no reply needed |
| Needs clarification | Ask follow-up question |

### 5. Post the Review

Use the post script to submit your review with inline comments:

```bash
# Create a comments file (JSON array)
cat > /tmp/review_comments.json << 'EOF'
[
  {"path": "src/file.ts", "line": 42, "body": "[Claude]: Your comment here"}
]
EOF

# Post the review
scripts/post_review.py <pr_url_or_number> \
  --body "Review summary here" \
  --event COMMENT \
  --comments-file /tmp/review_comments.json
```

**Review events** — default to `COMMENT` unless you have strong justification:

| Event | Use when |
|-------|----------|
| `COMMENT` | Feedback only (default—approval decisions need human judgment) |
| `APPROVE` | Changes are correct and ready to merge |
| `REQUEST_CHANGES` | Must-fix blockers before merge |

### 6. Reply to Existing Threads

Reply to each thread individually:

```bash
scripts/post_review.py <pr_url_or_number> \
  --reply-to <comment_id> \
  --body "[Claude]: Your reply" \
  --event COMMENT
```

### 7. Verify Success

After posting, confirm the review was submitted:

```bash
gh pr view <pr_number> --comments
```

Check that your comments appear. If any failed, review error messages and retry.

## Write Effective Comments

**Prefix every comment** with `[Claude]:` to identify automated feedback.

**Be constructive** — focus on improvement, not criticism.

**Be specific** — reference exact lines and suggest fixes.

**Prioritize** — distinguish blockers from nice-to-haves.

**Ask questions** — when intent is unclear, ask rather than assume.

**Respect author intent** — suggest, don't dictate style preferences.

See [references/comment-templates.md](references/comment-templates.md) for ready-to-use templates.

## Handle Errors

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| 404 Not Found | PR doesn't exist or no access | Verify PR URL and permissions |
| 401/403 | Authentication issue | Run `gh auth status` and re-authenticate |
| 422 Unprocessable | Comment line not in diff | Use line numbers from the diff, not the file |
| Rate limited | Too many API calls | Wait and retry, or batch comments |

## Follow These Rules

- **One review submission** — batch all new comments into a single review
- **Reply individually** — each thread reply is a separate API call
- **Don't duplicate** — skip points already made in existing threads
- **Read before reviewing** — understand full context before commenting
