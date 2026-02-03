---
name: squash-merge
description: Squash merge a GitHub PR using the gh API, crafting the perfect commit message that summarizes all changes on the branch. Use when merging PRs, finishing feature branches, or when user says "squash merge", "merge PR", "finish this PR", or "land this branch". Follows the repo's commit conventions.
---

# Squash Merge PR

Squash merge a GitHub PR with a well-crafted commit message following the repo's conventions.

## Workflow

### 1. Gather Context

```bash
# PR details
gh pr view --json number,title,body,baseRefName,headRefName

# All commits on the branch
gh pr view --json commits --jq '.commits[] | "\(.oid[:7]) \(.messageHeadline)"'

# Full diff
gh pr diff
```

### 2. Detect Commit Convention

```bash
# Check for commitlint config
ls commitlint.config.* .commitlintrc* 2>/dev/null

# Sample recent commits on base branch
git log origin/$(gh pr view --json baseRefName -q .baseRefName) --oneline -15
```

Use Conventional Commits if the repo uses it, otherwise match existing style.

### 3. Craft the Commit Message

**Subject line:**
- Primary change type (feat, fix, refactor, etc.)
- Optional scope from affected area
- Imperative summary of overall change
- Under 70 characters

**Body:**
- What changed and why (not how)
- Summarize key changes from all commits
- Reference PR number

**Structure:**
```
<type>(<scope>): <summary>

<motivation and context>

<bullet points if multiple significant changes>

PR: #<number>
```

### 4. Execute Squash Merge

```bash
gh pr merge <PR_NUMBER> --squash --delete-branch \
  --subject "<type>(<scope>): <summary>" \
  --body "$(cat <<'EOF'
<body content>

PR: #<PR_NUMBER>
EOF
)"
```

### 5. Verify

```bash
gh pr view <PR_NUMBER> --json state,mergedAt
```

## Type Selection

| Type | Use for |
|------|---------|
| `feat` | New user functionality |
| `fix` | Bug fix |
| `refactor` | Code restructuring, no behavior change |
| `perf` | Performance improvement |
| `docs` | Documentation only |
| `test` | Test changes only |
| `build` | Build system or deps |
| `ci` | CI configuration |
| `chore` | Maintenance |

Choose the type representing the **overall** change. If mixed, use the most significant.

## Examples

**Feature:**
```
feat(auth): Add OAuth2 login with Google and GitHub

Enable users to sign in using existing Google or GitHub accounts.
Includes session management and account linking.

PR: #142
```

**Bug fix:**
```
fix(api): Prevent race condition in concurrent requests

Multiple simultaneous requests could corrupt shared state.
Add mutex lock around critical section.

PR: #89
```

**Refactor:**
```
refactor(validation): Extract shared validation to core module

Consolidate duplicate validation from 5 endpoints into reusable
validators. No behavior change.

PR: #201
```
