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
- **MANDATORY: Create the phase checklist FIRST.** Before doing ANY work, you MUST use `TaskCreate` to create one task per phase (Phases 0–6). This is non-negotiable. The task list survives context compaction — the skill instructions do not. Every phase must exist as a task you can check off. If you skip this step, you WILL forget later phases. See Phase 0, Step 1.

## Workflow

### Phase 0: Prepare

1. **Create the phase checklist using TaskCreate.** Before anything else — before reading files, before fetching, before exploring — create exactly these tasks using `TaskCreate`:
   - "Phase 0: Read repo agent files, fetch main, create feature branch"
   - "Phase 1: Load ticket via using-beads, run specs cascade"
   - "Phase 2: Enter plan mode, design implementation, get user approval"
   - "Phase 3: TDD — write failing tests, implement, verify all pass"
   - "Phase 4: Create PR via gh pr create"
   - "Phase 5: Sub-agent review/fix loop (reviewing-prs → fixing-pr-comments → repeat until clean)"
   - "Phase 6: Resolve conflicts, fix CI, squash-merge, close ticket"

   Include the full phase description (from this skill doc) in each task's `description` field so the instructions persist even after compaction. Mark Phase 0 as `in_progress` immediately. As you complete each phase, mark it `completed` and mark the next `in_progress`. **Check `TaskList` at every phase boundary** to confirm what comes next — never rely on memory alone.

2. **Read repo agent files.** Glob for `**/AGENTS.md` and `**/agents.md` in the repo. Read every match. Note any worktree patterns, branch naming conventions, protected branches, or workflow constraints. **If agent files specify worktrees, you MUST use worktrees** — do not fall back to regular branches. Adhere to all agent file rules throughout the entire workflow.
3. **Ensure main is up to date.** Run `git fetch origin` and check if the local main branch is behind. If behind, pull latest. This must happen before any research or exploration.
4. **Create a feature branch (or worktree).** Use the repo's convention from agent files. If agent files mandate worktrees, use `git worktree add`. Otherwise branch off main using the naming convention or default to `feat/<ticket-id>`. Confirm you are NOT on main before proceeding.

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

⚠️ **THIS PHASE IS MANDATORY — DO NOT SKIP IT.** If you are reading this from a task description after context compaction, this is the most important phase. The PR is NOT ready to merge until it has passed a sub-agent review. Check your `TaskList` — Phase 5 must be completed before Phase 6.

This is the critical quality gate. Reviews always happen in a **sub-agent with fresh context** so they evaluate the PR objectively, not through the lens of having just written the code.

12. **Check TaskList.** Confirm Phase 5 is your current task. Mark it `in_progress`. Read the task description to remind yourself of the full procedure.
13. **Launch a sub-agent** (using the `Task` tool) to invoke `/reviewing-prs` against the PR. Pass the original ticket description to the sub-agent so it can evaluate whether the implementation matches the requirements — but give it no implementation context. It reviews the diff cold, like an external reviewer who read the spec. It posts inline comments on the diff.
14. **Fix the review comments** by invoking `/fixing-pr-comments`. This fetches all posted comments, assesses each, makes code changes, commits, pushes, and replies to every thread.
15. **Launch another sub-agent** (using the `Task` tool) to invoke `/reviewing-prs` again. Pass the original ticket description again. Fresh context — it reads the ticket, PR, diff, and comment threads from scratch to verify all issues were addressed and no new issues were introduced.
16. **Repeat steps 14-15** if the verification review finds new issues. Stop when the review pass is clean.

### Phase 6: Merge

17. **Check TaskList.** Confirm Phase 6 is your current task. Mark it `in_progress`.
18. **Resolve merge conflicts** with the base branch if any exist. Run all tests after resolution.
19. **Fix any CI failures** (lint, tests). Push fixes.
20. **Squash merge** the PR using the `squash-merge` skill.
21. **Close the ticket** using the `using-beads` skill with a completion reason.
22. **Mark Phase 6 completed** in TaskList.

## Key Principles

- **The task list IS the workflow** — create it first, check it at every boundary, never rely on memory. Context compaction WILL erase these instructions; the task list survives.
- **Never touch main** — all work happens on feature branches (or worktrees if agent files require them). If you find yourself on main, stop and branch immediately.
- **Repo agent files are law** — `AGENTS.md` rules on worktrees, branches, and workflows override everything else. If they say worktrees, use worktrees.
- **Tests before code** — always. Write them, watch them fail, then implement.
- **Sub-agent reviews are non-negotiable** — never review your own code in the same context. Fresh eyes catch what familiarity hides. This is Phase 5. Do not skip it.
- **Specs drive code, not reverse** — if there's no requirement to trace to, add one before writing code.
- **Record progress** — add beads comments at phase boundaries so context survives compaction.
- **When in doubt, check TaskList** — if you're unsure what to do next, `TaskList` will tell you. Read the task description for full instructions.
