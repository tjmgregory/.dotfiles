---
name: coordinate-delivery
description: Coordinate whole deliveries through model-pinned subagents, from planning through implementation, validation, and merge. Use when asked to coordinate or delegate an entire delivery.
---

# Coordinate Delivery

MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this skill and its references follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

## Role and routing

The coordinator MUST delegate implementation, deployment, and feedback loops. It MAY inspect key files during initial planning and verify results; it MUST return missed goals to agents with corrections rather than take over their work.

Before planning or spawning, the coordinator MUST read the active harness reference: [Claude Code](references/claude-code.md) or [Codex](references/codex.md). It MUST pin every new agent's model and use the saved routes. It SHOULD use Balanced unless Theo chooses Conserve or Burn. Explicit model choices and budgets take precedence. Burn MUST NOT automatically select the largest model.

A lookup is read-only with a checkable answer. A scoped change has a known approach and acceptance checks. Unknown causes, cross-module effects, and consequential changes MUST use the complex row. Overlapping tasks MUST use the more demanding row.

Each route MAY make one attempt and one correction, then MUST use a distinct saved escalation or report the blocker. Self-escalation MUST NOT restart the route. Lead and workers MUST share this budget. Escalation MUST NOT exceed Theo's spending cap.

Plans MUST state mode, model, effort, and reason. Cost/time forecasts MUST remain uncalibrated until comparable task records exist. Estimates MUST include retries and verification, and use the dependency path for elapsed time. API prices MUST NOT be presented as subscription credits or benchmark averages as task quotes.

Model refreshes MUST follow [the update process](references/update-model-guidance.md) before changing routes. [Model evidence](references/model-evidence.md) records measurements, gaps, and replay results; delivery agents MAY read it to explain or challenge a route.

## Delivery

1. The coordinator MUST define work items, dependencies, ownership, and model choices before delegation. It SHOULD use the cheapest sufficient investigation: its own brief reads, one pinned investigator, or narrowly briefed parallel investigators.
2. Before spawning, it MUST present the breakdown for confirmation and wait unless Theo has already authorised that plan. Parallel agents MUST have distinct scopes and pinned models.
3. Agents MUST own their tests, review fixes, CI, and merge within the authorised scope. The coordinator MUST check results against goals and return specific corrections on a miss.
4. Before reporting completion, the coordinator MUST verify the requested outcome from real state.

## Shared work

Shared scaffolding MUST be identified upfront and landed before dependent builders start. At each builder's completion, the coordinator MUST compare its diff-stat with active siblings for substantive duplicate work.

On substantial overlap, it MUST pause affected builders, land one shared version, and have the others rebase and remove duplicates. Shared imports or incidental config edits SHOULD remain in normal review.

## Infrastructure faults

On a transient 500, 529, or interrupted server response, the coordinator MUST resume the same agent with its context and worktree. It MUST explain the interruption and resume point. It MUST NOT change models, replace the agent, take over its role, or restructure delegation solely because of the fault. It SHOULD wait for load to clear.

## Verification

Before accepting an agent's completion claim, the coordinator MUST check applicable artefacts: pushed commit, merged PR, CI against the current head, and intended content on origin/main. A duplicate pending workflow MUST NOT count as failure.

Agents waiting on a watcher with no notification path MUST be resumed to poll the actual operation to a terminal state. Builders MUST prove live-path wiring with a check that fails when the wiring is removed; reviewers MUST verify invocation, not just component existence.
