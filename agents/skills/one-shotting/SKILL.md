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

## Workflow

### Phase 1: Understand the Work

1. **Load the ticket** using the `using-beads` skill. Read the ticket's title, description, design notes, acceptance criteria, and comments. Mark it `in_progress`.
2. **Run the specs cascade** using the `cascading-specs` skill. Discover existing specs, identify gaps in the cascade (Vision → Requirements → Use Cases → Entity Model → Architecture → Tests → Code). Fill any gaps top-down before proceeding — no code without something to trace to.

### Phase 2: Plan

3. **Enter plan mode.** Explore the codebase, understand existing patterns, and design the implementation approach. The plan must include:
   - Files to modify/create
   - Test IDs and what they verify (tests are written first)
   - Trace references to requirements/use cases
   - Implementation order: tests first, domain before adapters, layer by layer
4. **Get user approval** on the plan before proceeding.

### Phase 3: Implement (TDD)

5. **Write failing tests first** — unit, integration, and acceptance tests as specified in the plan. Verify they fail for the right reasons.
6. **Write production code** to make the tests pass. Follow existing project conventions. Domain layer first, then ports, use cases, adapters.
7. **Verify all tests pass** — both new and existing. Fix any regressions.

### Phase 4: Ship

8. **Create a PR** using `gh pr create`. Include a summary of changes and test plan.

### Phase 5: Sub-Agent Review & Fix Loop

This is the critical quality gate. Reviews always happen in a **sub-agent with fresh context** so they evaluate the PR objectively, not through the lens of having just written the code.

9. **Launch a sub-agent** to invoke `/reviewing-prs` against the PR. Pass the original ticket description to the sub-agent so it can evaluate whether the implementation matches the requirements — but give it no implementation context. It reviews the diff cold, like an external reviewer who read the spec. It posts inline comments on the diff.
10. **Fix the review comments** by invoking `/fixing-pr-comments`. This fetches all posted comments, assesses each, makes code changes, commits, pushes, and replies to every thread.
11. **Launch another sub-agent** to invoke `/reviewing-prs` again. Pass the original ticket description again. Fresh context — it reads the ticket, PR, diff, and comment threads from scratch to verify all issues were addressed and no new issues were introduced.
12. **Repeat steps 10-11** if the verification review finds new issues. Stop when the review pass is clean.

### Phase 6: Merge

13. **Resolve merge conflicts** with the base branch if any exist. Run all tests after resolution.
14. **Fix any CI failures** (lint, tests). Push fixes.
15. **Squash merge** the PR using the `squash-merge` skill.
16. **Close the ticket** using the `using-beads` skill with a completion reason.

## Key Principles

- **Tests before code** — always. Write them, watch them fail, then implement.
- **Sub-agent reviews are non-negotiable** — never review your own code in the same context. Fresh eyes catch what familiarity hides.
- **Specs drive code, not reverse** — if there's no requirement to trace to, add one before writing code.
- **Record progress** — add beads comments at phase boundaries so context survives compaction.
