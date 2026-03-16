# Theory and Foundations

The conceptual and mathematical foundations behind work decomposition. Consult this when you need to explain *why* a technique works or make trade-off decisions.

## Contents

- [Dependency DAGs and Topological Sort](#dependency-dags-and-topological-sort)
- [Critical Path Method](#critical-path-method)
- [Conway's Law](#conways-law)
- [Brooks's Law](#brookss-law)
- [Ousterhout's Deep Modules](#ousterhouts-deep-modules)
- [Team Topologies](#team-topologies)
- [The Granularity Tradeoff](#the-granularity-tradeoff)
- [Work Breakdown Structure](#work-breakdown-structure)

## Dependency DAGs and Topological Sort

Tasks and their dependencies form a Directed Acyclic Graph (DAG).

- **Nodes** = tasks/work packages
- **Edges** = dependencies (A -> B means B cannot start until A finishes)
- **Critical path** = longest path through the DAG, determining minimum project duration
- **Slack/Float** = Late Start - Early Start for a task. Zero slack = on the critical path.

### Identifying parallelism

1. Build the DAG of all tasks and dependencies
2. Compute the critical path (longest path)
3. Any task NOT on the critical path has slack and can be parallelized with critical-path tasks
4. Use topological sort to find all tasks with in-degree zero — these are immediately parallelizable
5. As tasks complete, recompute in-degrees; new zero-in-degree tasks become available

### Kahn's Algorithm (BFS topological sort)

```
1. Compute in-degree for every node
2. Enqueue all nodes with in-degree 0
3. While queue is not empty:
   a. Dequeue node n (this task can start now)
   b. For each neighbor m of n:
      - Decrement in-degree of m
      - If in-degree of m becomes 0, enqueue m
4. All nodes dequeued at the same "wave" can execute in parallel
```

This naturally produces **waves of parallelism**: Level 0 = all nodes with no deps, Level 1 = all nodes whose deps are all in Level 0, etc. All nodes at the same level can execute simultaneously.

### Maximum parallelism

The **width** of the DAG at any level (number of tasks with no mutual dependencies) determines the maximum parallelism at that point. The critical path length determines the theoretical minimum completion time regardless of worker count.

## Critical Path Method

The critical path is the **longest sequence of dependent tasks** from start to finish. It determines the minimum possible project duration.

### Computing it

1. **Forward pass**: compute Earliest Start (ES) and Earliest Finish (EF) for each task, starting from time 0
2. **Backward pass**: compute Latest Start (LS) and Latest Finish (LF) for each task, starting from the project end date
3. **Slack** = LS - ES (or LF - EF). Tasks with slack = 0 are on the critical path.

### Practical implications

- **Critical-path tasks must be prioritized** — any delay directly extends the project
- **Non-critical tasks have float** — they can be delayed, rescheduled, or done by less-senior engineers
- **Shortening the critical path** is the only way to shorten the project timeline (adding workers to non-critical tasks has zero effect on delivery date)

### Schedule compression techniques

- **Fast-tracking**: overlap tasks on the critical path that were assumed sequential (e.g., start B before A finishes if B only needs A's interface)
- **Crashing**: add resources to critical-path tasks to shorten their duration
- **Dependency breaking**: restructure tasks to eliminate unnecessary sequential dependencies (define the interface first so implementation proceeds in parallel)

### Adapting CPM for agile

Rather than planning the entire project's critical path upfront, compute it for the next 2-4 weeks of work. Re-derive each iteration as new information emerges. At the end of each sprint planning, take 5 minutes to look ahead and identify inter-team dependencies.

## Conway's Law

> "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations." — Melvin Conway, 1967

Software architecture inevitably mirrors team structure. Teams that interact easily produce tightly coupled code; teams separated by boundaries produce modular systems.

### The Inverse Conway Maneuver

Deliberately restructure teams to produce the architecture you want:

- Want independently deployable microservices? Create small autonomous teams aligned to business capabilities.
- Want a clean modular monolith? Organize teams around bounded contexts.
- Want parallel feature delivery? Create stream-aligned teams that own a complete value stream end-to-end.

### Practical implications

- Before decomposing tasks for parallel work, align team boundaries to system component boundaries
- Avoid activity-oriented teams (frontend team, backend team, QA team) — they create handoff queues
- Use DDD's Bounded Contexts to define team groupings around shared language
- Organizational structure and codebase must evolve together — changing one without the other creates friction
- Account for communication barriers (time zones, org silos) when designing system boundaries

### Key insight for decomposition

Decompose work along the same boundaries as your team structure. If two pieces of work would require the same person to context-switch, they are effectively sequential even if they have no technical dependency.

## Brooks's Law

> "Adding manpower to a late software project makes it later." — Fred Brooks, 1975

### The math

Communication channels = **n(n-1)/2** where n = number of people.

| Team size | Channels |
|---|---|
| 5 | 10 |
| 10 | 45 |
| 20 | 190 |
| 50 | 1,225 |

Doubling team size **quadruples** communication overhead.

### Two factors

1. **Ramp-up time** — new members must learn the codebase, conventions, and context before contributing
2. **Communication overhead** — coordination time grows with interfaces between code written by different people

### Mitigation strategies

| Strategy | Effect |
|---|---|
| Small teams (5-8 people) | Keeps channels manageable |
| Well-defined interfaces | Not everyone needs to talk to everyone |
| Async communication (ADRs, RFCs, specs) | Replace synchronous meetings |
| Automated verification (CI, linters, contract tests) | Catch interface violations without human communication |
| Good documentation and naming | Reduce ramp-up cost |

### Key insight

Brooks's Law applies when work is **tightly coupled**. It applies much less when work is **decomposed into independent pieces with well-defined interfaces**. The goal of decomposition is to convert a tightly-coupled problem into loosely-coupled sub-problems that can be parallelized without quadratic communication cost.

## Ousterhout's Deep Modules

From "A Philosophy of Software Design" by John Ousterhout.

### Deep vs shallow modules

- A **deep module** provides powerful functionality behind a simple interface
- A **shallow module** has a complex interface but little functionality

Deep modules are the key to enabling parallel work: they hide complexity so that consumers (other teams/modules) have minimal surface area to understand.

### Information hiding

Each module encapsulates implementation details; only the interface is visible. This reduces complexity in two ways:
1. Simplifies the interface consumers must understand
2. Reduces dependencies so changes are localized

### Application to decomposition

- Create tasks whose outputs are deep modules — simple interfaces hiding complex implementations
- The interface IS the coordination mechanism between parallel workers
- Implementation behind the interface is fully independent
- "Pick the structure that results in the best information hiding, the fewest dependencies, and the deepest interfaces"

### Relationship to contracts-first development

Ousterhout's deep modules are the theoretical justification for contracts-first development. The contract (interface) is agreed upon first, then implementation (the "deep" part) proceeds independently on both sides. The simpler the interface, the less coordination required.

## Team Topologies

From Matthew Skelton and Manuel Pais's "Team Topologies."

### Four team types

1. **Stream-aligned teams** — deliver value end-to-end along a business stream. Primary value-creating units. Can ship independently without coordinating with other teams.
2. **Platform teams** — provide self-service internal services (CI/CD, observability, databases) that reduce cognitive load on stream-aligned teams.
3. **Enabling teams** — temporarily boost capabilities of other teams, then move on.
4. **Complicated subsystem teams** — own areas requiring deep specialist knowledge.

### Three interaction modes

1. **Collaboration** — high-bandwidth joint work (expensive, use temporarily for discovery)
2. **X-as-a-Service** — clear provider/consumer boundary (cheap, the steady-state goal)
3. **Facilitation** — one team coaches another (temporary)

### Cognitive load as the constraint

Teams become ineffective when cognitive load exceeds capacity. The primary purpose of platform teams is to absorb cross-cutting complexity so stream-aligned teams stay focused.

**Application**: when decomposing work, ensure no single worker must hold more context than they can handle. If a task requires understanding 5 different subsystems, it is too broadly scoped — split it.

### Key principle

Evolve toward X-as-a-Service interactions everywhere, minimizing expensive Collaboration mode. This maps directly to reducing coordination costs in decomposed work.

## The Granularity Tradeoff

From parallel computing research.

### The inverse relationship

There is an inverse relationship between **degree of concurrency** and **task granularity**:

- **Fine-grained** (many small tasks): Maximum parallelism, but high coordination overhead
- **Coarse-grained** (few large tasks): Low coordination overhead, but less parallelism

### Communication cost determines optimal granularity

For software teams, "communication cost" includes: code review, interface negotiation, merge conflicts, integration testing, context switching, and status meetings.

| Communication cost | Optimal granularity |
|---|---|
| Very low (AI agents with shared codebase, strong CI) | Fine-grained (hours) |
| Low (co-located team, trunk-based dev, strong CI) | Fine-grained (1-2 days) |
| Medium (distributed team, PRs, async review) | Medium (2-5 days) |
| High (cross-org, different codebases, manual integration) | Coarse (1-2 weeks) |

### The sweet spot

The optimal granularity minimizes the sum of:
- **Idle time** (workers waiting for dependencies) — reduced by finer granularity
- **Coordination overhead** (merging, reviewing, communicating) — reduced by coarser granularity

Most engineering teams find the sweet spot at 1-3 day slices with well-defined interfaces and strong CI.

## Work Breakdown Structure

The classical PMI decomposition method.

### Core principles

- **100% Rule**: The WBS captures 100% of scope at every level. Sum of children = parent. Nothing missing, nothing extraneous.
- **8/80 Rule**: Work packages should require between 8 and 80 hours of effort. Below 8h is micromanagement; above 80h is too coarse.
- **Deliverable-oriented**: Each node is a deliverable or outcome, not a task verb. This prevents scope creep.
- **Levels**: Typically 2-4 levels deep. Level 1 = major deliverables, Level 2 = sub-deliverables, Level 3 = work packages.

### When to use

WBS is most useful for large, well-understood projects where scope completeness matters. For exploratory or agile work, story mapping and vertical slicing are usually more effective — but the 100% Rule and 8/80 Rule remain universally applicable heuristics.
