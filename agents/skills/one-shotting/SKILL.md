---
name: one-shotting
description: >
  End-to-end ticket-to-merge workflow that takes a ticket ID and autonomously
  delivers merged code: specs cascade, plan, TDD implementation, PR creation,
  automated sub-agent review/fix loop, and squash merge. Use when user says
  "one-shot", "one-shotting", provides a ticket ID to implement end-to-end,
  or wants fully autonomous ticket completion. Requires: using-beads,
  cascading-specs, reviewing-prs, fixing-pr-comments, commit, squash-merge.
---

# One-Shotting: Ticket to Merged Code

Autonomous end-to-end delivery. Takes a ticket ID, delivers merged code on main.

## Arguments

`/one-shotting <ticket-id>` — the beads ticket ID to implement.

## Critical Rules

- **NEVER make changes on the main branch.** Always create a feature branch before any modifications. If on main, create and switch to a new branch immediately. No commits, no edits, nothing on main — ever.
- **Read and obey repo agent files.** Before any work, read all `AGENTS.md` and `agents.md` files in the repo (root and subdirectories). If they define worktree patterns, branch conventions, or workflow rules — follow them exactly. These override default assumptions.

## Workflow

### Phase 0: Prepare

1. **Read repo agent files.** Glob for `**/AGENTS.md` and `**/agents.md` in the repo. Read every match. Note any worktree patterns, branch naming conventions, protected branches, or workflow constraints. Adhere to all of them throughout the entire workflow.
2. **Ensure main is up to date.** Run `git fetch origin` and check if the local main branch is behind. If behind, pull latest. This must happen before any research or exploration.
3. **Create a feature branch.** Branch off main using the repo's naming convention (from agent files) or default to `feat/<ticket-id>`. Confirm you are NOT on main before proceeding.

### Phase 1: Understand the Work

4. **Load the ticket** using the `using-beads` skill. Read the ticket's title, description, design notes, acceptance criteria, and comments. Mark it `in_progress`.
5. **Run the specs cascade** using the `cascading-specs` skill. Discover existing specs, identify gaps in the cascade (Vision → Requirements → Use Cases → Entity Model → Architecture → Tests → Code). Fill any gaps top-down before proceeding — no code without something to trace to.

### Phase 2: Plan

6. **Enter plan mode.** Explore the codebase, understand existing patterns, and design the implementation approach. The plan must include:
   - Files to modify/create
   - Test IDs and what they verify (tests are written first)
   - Trace references to requirements/use cases
   - Implementation order: tests first, domain before adapters, layer by layer
7. **Get user approval** on the plan before proceeding.

### Phase 3: Implement (TDD)

8. **Write failing tests first** — unit, integration, and acceptance tests as specified in the plan. Verify they fail for the right reasons.
9. **Write production code** to make the tests pass. Follow existing project conventions. Domain layer first, then ports, use cases, adapters.
10. **Verify all tests pass** — both new and existing. Fix any regressions.

### Phase 4: Ship

11. **Create a PR** using `gh pr create`. Include a summary of changes and test plan.

### Phase 5: Sub-Agent Review & Fix Loop

This is the critical quality gate. Reviews always happen in a **sub-agent with fresh context** so they evaluate the PR objectively, not through the lens of having just written the code.

12. **Launch a sub-agent** to invoke `/reviewing-prs` against the PR. Pass the original ticket description to the sub-agent so it can evaluate whether the implementation matches the requirements — but give it no implementation context. It reviews the diff cold, like an external reviewer who read the spec. It posts inline comments on the diff.
13. **Fix the review comments** by invoking `/fixing-pr-comments`. This fetches all posted comments, assesses each, makes code changes, commits, pushes, and replies to every thread.
14. **Launch another sub-agent** to invoke `/reviewing-prs` again. Pass the original ticket description again. Fresh context — it reads the ticket, PR, diff, and comment threads from scratch to verify all issues were addressed and no new issues were introduced.
15. **Repeat steps 13-14** if the verification review finds new issues. Stop when the review pass is clean.

### Phase 6: Merge

16. **Resolve merge conflicts** with the base branch if any exist. Run all tests after resolution.
17. **Fix any CI failures** (lint, tests). Push fixes.
18. **Squash merge** the PR using the `squash-merge` skill.
19. **Close the ticket** using the `using-beads` skill with a completion reason.

## Key Principles

- **Never touch main** — all work happens on feature branches. If you find yourself on main, stop and branch immediately.
- **Repo agent files are law** — `AGENTS.md` rules on worktrees, branches, and workflows override everything else.
- **Tests before code** — always. Write them, watch them fail, then implement.
- **Sub-agent reviews are non-negotiable** — never review your own code in the same context. Fresh eyes catch what familiarity hides.
- **Specs drive code, not reverse** — if there's no requirement to trace to, add one before writing code.
- **Record progress** — add beads comments at phase boundaries so context survives compaction.
