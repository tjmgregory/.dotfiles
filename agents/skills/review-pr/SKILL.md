---
name: review-pr
description: Review a GitHub PR that isn't your own. Fetches PR diff and all comments, analyzes code changes, posts new review comments, and replies to existing comment threads. Use when asked to "review PR", "review this PR", "give feedback on PR", or when given a PR URL/number to review.
---

# Review PR

Review a GitHub PR by analyzing the diff, posting feedback, and engaging with existing discussions.

## Workflow

1. **Fetch PR info and diff**:
   ```bash
   gh pr view <pr> --json number,title,body,headRefName,baseRefName,author,additions,deletions,changedFiles,url
   gh pr diff <pr>
   ```

2. **Fetch ALL existing comments** (use `--paginate`):
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr}/comments --paginate
   gh api repos/{owner}/{repo}/issues/{pr}/comments --paginate
   ```

3. **Analyze the diff** for:
   - Logic errors or bugs
   - Security concerns
   - Performance issues
   - Missing edge cases
   - Code clarity improvements
   - Inconsistencies with surrounding code style

4. **Read relevant context** when needed:
   ```bash
   gh api repos/{owner}/{repo}/contents/{path}?ref={base_branch} | jq -r .content | base64 -d
   ```

5. **Assess each existing comment thread** — reply where useful:

   | Thread State | Action |
   |--------------|--------|
   | Unanswered question | Answer if you can help |
   | Discussion ongoing | Add perspective if valuable |
   | Resolved/agreed | No reply needed |
   | Needs clarification | Ask follow-up question |

6. **Post new review with comments**:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr}/reviews -X POST \
     --field body="Review summary" \
     --field event="COMMENT" \
     --field comments='[{"path":"file.ts","line":42,"body":"[🤖 Claude]: Comment"}]'
   ```

7. **Reply to existing comment threads**:
   ```bash
   # For review comments (have pull_request_review_id):
   gh api repos/{owner}/{repo}/pulls/{pr}/comments -X POST \
     --field body="[🤖 Claude]: Your reply" \
     --field in_reply_to={comment_id}

   # For issue comments (general PR comments):
   gh api repos/{owner}/{repo}/issues/{pr}/comments -X POST \
     -f body="[🤖 Claude]: Your reply"
   ```

## Comment Guidelines

**Be constructive**: Focus on improvement, not criticism.

**Be specific**: Reference exact lines and suggest fixes.

**Prioritize**: Flag blockers vs. nice-to-haves.

**Ask questions**: When intent is unclear, ask rather than assume.

## Comment Templates

**Bug/issue:**
```
[🤖 Claude]: This could cause [problem] when [condition]. Consider:
\`\`\`suggestion
[fixed code]
\`\`\`
```

**Question:**
```
[🤖 Claude]: What happens if [edge case]? Should this handle [scenario]?
```

**Suggestion:**
```
[🤖 Claude]: Optional: [improvement] would [benefit].
```

**Style (minor):**
```
[🤖 Claude]: Nit: [observation]
```

**Reply agreeing:**
```
[🤖 Claude]: +1 — [brief reason why this is a good point]
```

**Reply with context:**
```
[🤖 Claude]: To add context: [relevant information about the code/pattern]
```

## Review Events

| Event | Use when |
|-------|----------|
| `APPROVE` | Changes look good, no blockers |
| `REQUEST_CHANGES` | Must-fix issues before merge |
| `COMMENT` | Feedback only, no approval/rejection |

## Critical Rules

- **`[🤖 Claude]:`** prefix on EVERY comment and reply
- **Read before reviewing** — understand the full context
- **One review submission** — batch new comments into single review
- **Reply individually** — each thread reply is a separate API call
- **Don't duplicate** — don't repeat points already made in threads
- **Respect author intent** — suggest, don't dictate style preferences
- **Use `--field in_reply_to`** for review comment replies (not `/replies` endpoint)
