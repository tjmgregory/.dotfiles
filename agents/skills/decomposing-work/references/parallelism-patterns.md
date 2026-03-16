# Parallelism Patterns

Concrete techniques for maximizing parallel work while minimizing friction, merge conflicts, and coordination overhead.

## Contents

- [Contract-First Development](#contract-first-development)
- [Walking Skeleton](#walking-skeleton)
- [Feature Flags](#feature-flags)
- [Branch by Abstraction](#branch-by-abstraction)
- [Strangler Fig Pattern](#strangler-fig-pattern)
- [Merge Conflict Avoidance](#merge-conflict-avoidance)
- [Trunk-Based Development](#trunk-based-development)
- [The Parallelism Playbook](#the-parallelism-playbook)

## Contract-First Development

Define the interface contract before any implementation begins. The contract is the synchronization point — once agreed, all teams proceed independently.

### Steps

1. **Design the contract together** — all consuming and producing teams in one room or one PR
2. **Express the contract as executable tests** — contract tests are the "unit test of an API"
3. **Generate mocks from the contract** — WireMock, Specmatic, or hand-rolled mocks
4. **Teams diverge and implement in parallel** — each codes against the contract, running tests locally
5. **Integration becomes validation, not discovery** — when teams converge, contract tests already guarantee compatibility

### Concrete forms by language/stack

| Stack | Contract artifact |
|---|---|
| Go | Interface types + test doubles |
| TypeScript | Type definitions + mock implementations |
| REST APIs | OpenAPI spec + generated mocks |
| gRPC | Protobuf definitions + generated stubs |
| Events | JSON Schema or Avro for message formats |
| Databases | Migration files + shared test fixtures |

### Postel's Law for contracts

"Be conservative in what you send, be liberal in what you accept." Design contracts with forward-compatibility in mind — add fields without breaking consumers, ignore unknown fields.

### Contract testing tools

- **Pact** — consumer-driven contract testing (defines contracts from consumer perspective)
- **Specmatic** — API contract testing from OpenAPI specs
- Go compiler — interface satisfaction is a compile-time contract

## Walking Skeleton

A tiny end-to-end implementation that links all major architectural components. It is the **prerequisite** for parallel work.

### Characteristics of a good skeleton

- **Compiles and runs** — even if it does nothing useful
- **Defines all major interfaces** — types, function signatures, API shapes, message formats
- **Has a working CI pipeline** — parallel contributors get immediate feedback
- **Is deliberately boring** — no clever abstractions, no premature optimization, just connection points
- **Evolves** — as parallel work lands, the skeleton grows into the real system

### How it breaks dependencies

```
Without skeleton:
  Define interface → Implement service A → Integration test
  Define interface → Implement service B → Integration test
  Critical path: sequential, long

With skeleton:
  Build skeleton (defines all interfaces, stubs everything) [1-2 days]
  Then in parallel:
    Implement service A against skeleton interface
    Implement service B against skeleton interface
    Write integration tests against skeleton (evolving as services deliver)
  Critical path: skeleton + max(A, B)
```

### What the skeleton includes

- Entry points (CLI, HTTP handler, message consumer) with stub implementations
- Core domain types/interfaces with no-op implementations
- Data layer interfaces with in-memory or hardcoded implementations
- Build and CI configuration
- A single passing end-to-end test

### What it does NOT include

- Real business logic
- Production data stores
- Performance optimization
- Error handling beyond basic structure
- Any feature a user would care about

## Feature Flags

Allow incomplete code to be merged to main while keeping it inactive.

### How flags enable parallelism

- Developers commit to main continuously — no long-lived branches, no merge conflicts
- Incomplete features are hidden behind flags — main is always deployable
- Multiple teams work on overlapping areas because changes are toggled independently
- QA can test features in production while development continues

### Best practices

- Flags should be **short-lived** — remove within days/weeks of full rollout
- Name flags after the **feature**, not the team or ticket
- Default to **off** for new features
- Use a flag management system (LaunchDarkly, Unleash, environment variables, or a config map)
- Treat flag cleanup as real work — schedule it

### Implementation patterns

**Simple boolean flag:**
```go
if featureFlags.IsEnabled("new-checkout-flow") {
    return newCheckoutHandler(r)
}
return legacyCheckoutHandler(r)
```

**Percentage rollout:**
```go
if featureFlags.IsEnabledForUser("new-search", userID) {
    return newSearch(query)
}
return legacySearch(query)
```

## Branch by Abstraction

For large refactors that would otherwise require a long-lived branch.

### The five steps

1. **Introduce an abstraction** around the code to be replaced. Commit to trunk.
2. **Build the new implementation** behind the abstraction, initially off/unused.
3. **Flip the switch** — route traffic to the new implementation.
4. **Remove the old implementation.**
5. **Remove the abstraction layer** (optional — may be useful as a testing seam).

### Key property

At no point does the build break, and at no point does any other developer need to wait. The old and new implementations coexist peacefully behind the abstraction.

### Example

Replacing a synchronous email sender with an async queue:

```go
// Step 1: Introduce abstraction
type EmailSender interface {
    Send(ctx context.Context, msg Email) error
}

// Step 2: New implementation exists alongside old
type syncSender struct{ /* existing code */ }
type asyncSender struct{ /* new queue-based code */ }

// Step 3: Flip the switch (feature flag or config)
func NewEmailSender(cfg Config) EmailSender {
    if cfg.UseAsyncEmail {
        return &asyncSender{queue: cfg.Queue}
    }
    return &syncSender{smtp: cfg.SMTP}
}

// Step 4: Remove syncSender after validation
// Step 5: Optionally remove interface if only one impl remains
```

## Strangler Fig Pattern

For migrating from legacy systems while continuing parallel feature development.

### Steps

1. **Place a facade (proxy)** in front of the legacy system
2. **Build new components** that handle specific routes/features
3. **Route traffic incrementally** from legacy to new components
4. **Old and new coexist** during the transition

### Why it enables parallelism

Feature development on both legacy and new system proceeds simultaneously. Teams working on the new system do not block teams maintaining the legacy system. Migration and feature development are decoupled.

## Merge Conflict Avoidance

### Structural strategies (prevent by design)

| Strategy | Effect |
|---|---|
| **Vertical slicing** | Each feature touches its own files |
| **Directory-per-feature** | Features isolated in separate directories |
| **Small, focused files** | 500-line files conflict far less than 5000-line files |
| **CODEOWNERS** | Makes ownership explicit, reduces accidental overlap |
| **Auto-discovery over registration** | Avoid single central files everyone edits (route tables, plugin registries). Use directory scanning or convention-based loading instead |

### Process strategies (reduce conflict window)

| Strategy | Effect |
|---|---|
| **Short-lived branches (1-3 days max)** | Smaller divergence window |
| **Trunk-based development** | Eliminates long-lived branch divergence entirely |
| **Daily rebase from main** | Detect conflicts early when they are small |
| **Small PRs** | Exponentially fewer conflict surfaces |
| **CI on every push** | Catch conflicting changes before they reach mainline |

### The math

Merge conflict probability increases **super-linearly** with branch lifetime and number of parallel branches. Halving branch lifetime reduces conflicts by more than half. The optimal strategy is: commit early, commit often, integrate continuously.

### The #1 conflict source

**Shared mutable files**: configuration files, route registrations, dependency lock files, and central registries. These are edited by every feature branch and conflict constantly.

**Solutions:**
- Use auto-discovery (scan directories) instead of manual registration
- Split configuration by feature or domain
- Use dependency management tools that handle lock file merges intelligently

## Trunk-Based Development

All developers commit to a single shared branch (trunk/main). Feature isolation is achieved through **code-level mechanisms** (feature flags, branch-by-abstraction) rather than **branch-level mechanisms** (long-lived feature branches).

### Prerequisites

- Strong CI/CD — every commit is built and tested automatically
- Feature flags — incomplete work can be merged safely
- Contract/interface testing — integration issues caught at commit time
- Team discipline around small, frequent commits

### Why it maximizes parallelism

- No merge conflicts from divergent branches
- No integration surprises from long-lived feature branches
- Every developer always has the latest code
- Deployment is always possible from trunk

### When branches are still appropriate

- Short-lived feature branches (1-3 days) for code review purposes
- Release branches for hotfix isolation (if needed)
- Experimental spikes that may be discarded entirely

Even with branches, the trunk-based mindset applies: branches should be short-lived and merged frequently.

## The Parallelism Playbook

Ordered by impact — do the top items first:

1. **Start with a walking skeleton** — end-to-end integration before teams diverge
2. **Define interfaces/contracts first** — the contract is the sync point, everything after it is parallel
3. **Slice vertically** — each work stream owns its own files and directories
4. **Use feature flags on trunk** — eliminate long-lived branches entirely
5. **Apply branch-by-abstraction** for large refactors
6. **Use CODEOWNERS** to make file ownership explicit
7. **Keep branches short-lived** (1-3 days) when branches are necessary
8. **Use contract tests** as automated anti-entropy that catches integration drift
9. **Structure teams as stream-aligned** — each owns a complete value stream
10. **Apply strangler fig** when migrating systems, to keep legacy and new development running in parallel
