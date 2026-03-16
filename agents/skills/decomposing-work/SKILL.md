---
name: decomposing-work
description: >
  Decomposes large engineering work into parallelizable, sequenceable chunks
  with minimum friction. Produces dependency DAGs, critical paths, walking
  skeletons, and interface contracts. Use when breaking down epics, features,
  projects, or large tickets into tasks. Triggers: "decompose", "break down",
  "split this work", "parallelize", "task breakdown", "work decomposition",
  "what can we parallelize", "dependency graph", "critical path", "story map",
  "slice this", "plan the work", "break this into tasks".
---

# Decomposing Work

Break large engineering work into small, parallelizable, independently deliverable chunks with explicit dependencies and minimum coordination cost.

## Contents

- [Core Process](#core-process) — The 7-step decomposition workflow
- [Key Heuristics](#key-heuristics) — Rules of thumb
- [Friction Reduction Checklist](#friction-reduction-checklist) — Verify before finalizing
- [Reference Guides](#reference-guides) — Deep-dive materials

## Core Process

### Step 1: Map the work

Lay out the user journey or system flow left-to-right as a **backbone** (sequence of high-level activities). Decompose each activity into stories/tasks below it, ordered by priority (essential at top, nice-to-have at bottom).

The top horizontal slice across all columns is the **walking skeleton** — the thinnest end-to-end path through the system.

If the work is purely backend/infrastructure with no user journey, map the **data flow** or **request lifecycle** instead.

### Step 2: Slice vertically

Each work item must cut through all necessary layers for a single narrow capability. Never split by technical layer ("build all the DB migrations, then all the API handlers, then all the tests") — that creates serial dependencies and defers integration risk.

Apply **SPIDR** to find split points:

| | Technique | Split when... |
|---|---|---|
| **S** | Spike | Uncertainty exists — separate research from implementation |
| **P** | Paths | Multiple user flows exist — each path is a separate slice |
| **I** | Interfaces | Multiple platforms/consumers — ship for one first |
| **D** | Data | Different data types — handle each separately |
| **R** | Rules | Business rules can be layered — start with happy path |

Additional split patterns: workflow steps, CRUD operations, simple/complex variants, defer performance optimization.

**Target size**: each slice = 1 acceptance test = 1-3 days of work.

**Litmus test**: "Can I demo this slice to someone?" If no, it is not a real slice.

For detailed splitting techniques, see [references/slicing-techniques.md](references/slicing-techniques.md).

### Step 3: Build the walking skeleton first

A tiny end-to-end implementation linking all major architectural components. It compiles, runs, deploys — but does almost nothing useful.

**Purpose:**
1. Validate integration assumptions before teams diverge
2. Define all interfaces (types, API shapes, message formats) as real code
3. Establish the CI pipeline so parallel contributors get immediate feedback
4. Break the largest dependency — without the skeleton most tasks are blocked; with it everyone can attach work in parallel

The skeleton is NOT an MVP. It has no real features. It provides attachment points for parallel work.

**Without skeleton:** A -> B -> D, A -> C -> D (serial chains, critical path = A+B+D)
**With skeleton:** S first, then B | C | D all in parallel (critical path = S + max(B,C))

### Step 4: Define contracts at every boundary

Before implementing, agree on the **interface** between components. The contract is the synchronization point — everything behind it is independent work.

Concrete forms: Go interfaces, OpenAPI specs, protobuf schemas, TypeScript types, shared type definitions, test fixtures.

Generate mocks/stubs from contracts so no team blocks another. This converts "B waits for A to finish" into "A and B work in parallel against a shared contract."

### Step 5: Build the dependency DAG

For each slice, ask: *"What must exist before this can start?"*

Draw the directed acyclic graph. Be rigorous — if two slices share no data, API, or state, they have **no dependency**. Do not add false dependencies based on intuition; only hard technical prerequisites count.

### Step 6: Identify the critical path and assign work

- **Critical path** = longest path through the DAG = minimum completion time regardless of parallelism
- **Slack** = how long a non-critical task can slip without affecting end date
- Use **topological sort**: find all tasks with zero in-degree (no blockers) — these start immediately in parallel
- As each completes, recompute available tasks
- **Always prioritize critical-path tasks** — they have zero slack

**Fast-tracking**: re-examine the critical path for tasks that can overlap (start B before A fully completes if B only needs A's interface, not its implementation).

### Step 7: Right-size granularity

| Coordination cost | Granularity | Example |
|---|---|---|
| High (distributed team, complex merges) | Coarser slices (3-5 days) | Distributed team across time zones |
| Low (co-located, strong CI, clear interfaces) | Finer slices (1-2 days) | Single team, trunk-based development |

**8/80 rule**: no work package under 1 day or over 2 weeks.

## Key Heuristics

1. **"Interfaces before implementations."** The single most effective parallelization technique.
2. **"If you can't demo it, it's not a slice."**
3. **"One acceptance test per story."** More than one? Split further.
4. **"Walking skeleton first."** End-to-end before depth.
5. **"Slice by business value, not by technology layer."**
6. **"Defer complexity, not value."** Happy path first, edge cases later.
7. **"Replace human coordination with automated verification."** Every machine-checkable contract is a conversation that doesn't need to happen.
8. **"Merge conflict probability grows super-linearly with branch lifetime."** Halving branch lifetime cuts conflicts by more than half.

## Friction Reduction Checklist

Before finalizing a decomposition, verify:

- [ ] Each slice is independently deployable and testable
- [ ] No slice requires more than 2 teams to coordinate
- [ ] Interfaces/contracts defined before implementation begins
- [ ] Walking skeleton identified and scheduled first
- [ ] Critical path tasks explicitly marked and prioritized
- [ ] Shared mutable files (config, routes, registries) minimized or eliminated
- [ ] Feature flags or branch-by-abstraction planned for overlapping work
- [ ] Branch lifetime target set (ideally 1-3 days)

## Reference Guides

- **Slicing techniques**: See [references/slicing-techniques.md](references/slicing-techniques.md) for story mapping, SPIDR detail, Richard Lawrence's 10 splitting patterns, Elephant Carpaccio, and Killick's slicing heuristic
- **Parallelism patterns**: See [references/parallelism-patterns.md](references/parallelism-patterns.md) for contract-first development, feature flags, branch-by-abstraction, strangler fig, walking skeletons, merge conflict avoidance, and trunk-based development
- **Theory and foundations**: See [references/theory.md](references/theory.md) for Conway's Law, Brooks's Law, DAG scheduling, critical path method, deep modules, Team Topologies, and the granularity tradeoff
