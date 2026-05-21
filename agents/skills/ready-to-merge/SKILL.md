---
name: ready-to-merge
description: Drives a PR to a fully ready-to-merge state — pushes the branch and opens a PR if needed, then loops the fixing-prs skill until every AI reviewer has done a fresh pass with no new comments, every comment thread is replied to, the entire CI pipeline is green, and the branch is up to date with its base. Use when the user says "ready to merge", "drive this to merge", "land this PR", "babysit until green", or asks for an autonomous PR-to-mergeable loop. Composes fixing-prs.
---

# Ready To Merge

Drives the current branch to a *fully mergeable* state. Loops the `fixing-prs` skill until the PR is stable: clean reviewer pass, every thread replied to, all checks green, base branch fully merged in.

This skill does **not** merge the PR — it leaves it in a state where a human (or `squash-merge`) can.

## Termination criteria

The loop exits only when **all four** are true on the same iteration:

1. **Quiet AI pass** — every AI/bot reviewer (Copilot, Claude review, CodeRabbit, Cursor bugbot, etc.) has had a chance to comment on the current HEAD SHA *after* the last fix push, and posted nothing new.
2. **All threads addressed** — every `review_comment`, `issue_comment`, and `review` body has an agent reply (the `[🤖` marker) unless a human posted after that reply.
3. **CI fully green** — `gh pr checks` reports every required check as `pass` (no `pending`, no `fail`, no `skipping`).
4. **Up to date with base** — `gh pr view --json mergeStateStatus` returns `CLEAN` (or `HAS_HOOKS`/`UNSTABLE` only when blocked solely by branch protection humans must clear).

If any of (1)–(4) is false, run another iteration.

## Workflow

### Step 1 — Ensure a PR exists

```bash
gh pr view --json url,number,headRefName,baseRefName,headRefOid,mergeStateStatus,mergeable
```

If this errors with "no pull requests found":
- Commit any uncommitted work (invoke the `commit` skill).
- `git push -u origin HEAD` to publish the branch.
- `gh pr create --fill --head <branch>` — `--fill` seeds the PR body from the commit history; the user can refine later. From a worktree, `--head` is mandatory.

Capture the PR number, base branch, and head SHA into variables for the loop.

### Step 2 — Loop until stable

Set `MAX_ITERATIONS=8` as a safety cap. For each iteration:

#### 2a. Sync with base

```bash
git fetch origin <base>
```

If the branch is behind base, rebase (preferred) or merge in. After resolving any conflicts, run the project's test/lint commands locally before pushing. Push with `git push` (or `git push --force-with-lease` if rebased).

#### 2b. Snapshot the current state

Note the *current* HEAD SHA — this is the SHA AI reviewers will comment against this round. Use the `fixing-prs` skill's fetcher to capture the comment set:

```bash
~/.claude/skills/fixing-prs/scripts/fetch_comments.sh <pr_number> > /tmp/rtm-before.json
```

#### 2c. Wait for AI reviewers to weigh in

AI reviewers (Copilot, Claude code review, CodeRabbit, Cursor bugbot, etc.) trigger on push and take 1–10 minutes. Poll every 60 seconds for new comments authored after the snapshot until either:
- A new comment from a bot/AI author appears (author login matches `*[bot]` or known AI account), OR
- 10 minutes elapse with no new bot comments (treat as "no bot will comment this round").

Also poll `gh pr checks <pr>` in the same loop — if every check has reached a terminal state and no new bot comments arrived, exit the wait.

#### 2d. Invoke `/fixing-prs`

Invoke the **fixing-prs** skill against the PR number. It will:
- Fetch all comments (including any that arrived during 2c).
- Assess, edit, commit, push, and reply to every thread.
- Watch CI and fix lint/test failures itself.

When `fixing-prs` finishes, control returns here.

#### 2e. Check termination criteria

After `fixing-prs` returns, re-fetch the PR state and evaluate all four criteria:

```bash
# Comment freshness
~/.claude/skills/fixing-prs/scripts/fetch_comments.sh <pr_number> > /tmp/rtm-after.json
# Compare: any comment created_at > push-time of current HEAD that lacks an agent reply?

# CI status
gh pr checks <pr_number> --json name,state,conclusion

# Mergeability
gh pr view <pr_number> --json mergeStateStatus,mergeable,headRefOid
```

A round counts as **stable** (loop exits) when:
- The "after" snapshot has zero comment threads without an agent reply *and* no new bot/human comments arrived after the latest fix-push SHA, AND
- Every check entry has `conclusion: success` (or `neutral`/`skipped`), AND
- `mergeStateStatus == "CLEAN"`.

Otherwise, increment the iteration counter and loop back to 2a.

### Step 3 — Final report

When the loop exits stable, report to the user:
- PR URL and number
- HEAD SHA at exit
- Total iterations
- Bot reviewers that participated (so the user can see who passed)
- Any threads where the agent disagreed with the reviewer (these may want human attention)

When the loop exits because `MAX_ITERATIONS` was hit, report what's still red and **do not** claim success.

## Rules

- **Never merge** — this skill prepares a PR for merge; the user (or `squash-merge`) does the actual merge.
- **Never force-push to base** — only force-push the feature branch, and only with `--force-with-lease`.
- **Push before reading reviewer state** — bot reviewers comment on the latest SHA; checking before pushing risks acting on stale comments.
- **Identify bots by login pattern** — anything ending in `[bot]`, plus the known accounts `copilot-pull-request-reviewer`, `coderabbitai`, `claude`, `cursor[bot]`. When in doubt, treat any account that has never posted human-like prose as a bot.
- **Resolve conflicts; don't bypass them** — if rebase introduces conflicts, resolve them. Never `--theirs`/`--ours` blanket-resolve without inspecting each file.
- **Do not skip a fixing-prs round** — even if criteria look met going in, run one final `fixing-prs` after the last reviewer pass to make sure replies exist.
- **Stop and ask** if the base branch has been force-pushed, the PR has been closed, or required reviews from humans (not bots) remain outstanding — those need a human decision, not another loop iteration.

## When NOT to use

- The PR is a draft and the user wants it to stay draft — this skill expects a ready-for-review PR.
- The work isn't actually ready to ship (failing tests the agent doesn't know how to fix, scope still open). Finish the work first, then invoke this.
- The repo has no AI reviewers configured *and* no CI — there's nothing to wait on; just push and call `fixing-prs` directly if any comments exist.
