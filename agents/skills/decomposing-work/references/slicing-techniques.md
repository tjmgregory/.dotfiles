# Slicing Techniques

Detailed reference for decomposing large work items into thin, deliverable slices.

## Contents

- [Story Mapping](#story-mapping)
- [SPIDR in Depth](#spidr-in-depth)
- [Richard Lawrence's 10 Splitting Patterns](#richard-lawrences-10-splitting-patterns)
- [Elephant Carpaccio](#elephant-carpaccio)
- [Killick's Slicing Heuristic](#killicks-slicing-heuristic)
- [Vertical vs Horizontal Slicing](#vertical-vs-horizontal-slicing)

## Story Mapping

Jeff Patton's story mapping creates a two-dimensional view of a backlog:

- **X-axis (Backbone)**: Sequence of user activities in narrative order
- **Y-axis**: Decomposition from epics to stories, ordered by priority (essential at top)

### How to build one

1. **Tell the big story left-to-right** — create the backbone of high-level user activities in the order they happen. These are the steps you cannot prioritize away.
2. **Break each backbone item into specific stories** below it — concrete implementations of that activity.
3. **Prioritize vertically** — most essential stories at the top of each column.
4. **Draw release slice lines** horizontally — everything above line 1 is Release 1.
5. **The walking skeleton** is the first release slice — minimal implementations of each backbone step that make the system "minimally functional."

### Example

```
Backbone:  [Register] → [Search] → [Select] → [Pay] → [Confirm]
              |            |          |          |         |
Slice 1:   email/pw    keyword     view item   card     email
Slice 2:   OAuth       filters     compare     PayPal   SMS
Slice 3:   SSO         saved       wishlist    crypto   push
```

Slice 1 is the walking skeleton. Slices 2 and 3 add depth. Each column can be worked on in parallel once the skeleton's interfaces are defined.

### When to use

- Starting a new product or major feature
- When the backlog feels like an unordered pile
- When teams struggle to understand how stories relate to each other
- When you need to identify what to build first

## SPIDR in Depth

Mike Cohn's five splitting techniques, ordered by preference (try P-I-D-R first, Spike as last resort):

### Paths

Split by different routes through the same feature.

**Before**: "As a user, I can pay for my order"
**After**:
- "...pay with credit card"
- "...pay with Apple Pay"
- "...pay with bank transfer"

Each path is independently valuable and independently testable.

### Interfaces

Split by platform, device, or consumer.

**Before**: "As a user, I can view my dashboard"
**After**:
- "...view dashboard on web"
- "...view dashboard on mobile"
- "...view dashboard via API"

Ship for one interface first. Others follow.

### Data

Split by data type, source, or format.

**Before**: "As an admin, I can import user data"
**After**:
- "...import from CSV"
- "...import from Excel"
- "...import from API"

Each data variant is a separate slice.

### Rules

Split by business rule complexity. Start with the common/simple case, layer in constraints.

**Before**: "As a user, I can book a room"
**After**:
- "...book a room (basic reservation)"
- "...with date validation (no past dates)"
- "...with capacity limits"
- "...with blackout date handling"

### Spike

Separate research from implementation when uncertainty is too high to estimate.

**Before**: "As a user, I can get real-time notifications"
**After**:
- Spike: "Evaluate WebSocket vs SSE vs polling for our stack" (timeboxed, 1-2 days)
- "Implement real-time notifications using [chosen approach]"

Use spikes as a last resort — try the other four first.

## Richard Lawrence's 10 Splitting Patterns

A decision flowchart for splitting stories. Walk through in order:

| # | Pattern | Heuristic |
|---|---|---|
| 1 | **Workflow steps** | Split by steps in the user's workflow |
| 2 | **Business rule variations** | Each rule becomes a separate story |
| 3 | **Major effort** | Identify the biggest chunk and separate it out |
| 4 | **Simple/complex** | Do the simple version first, add complexity later |
| 5 | **Data variations** | Different data types handled separately |
| 6 | **Data entry methods** | Each input method is a story |
| 7 | **Defer performance** | Make it work first, make it fast later |
| 8 | **Operations (CRUD)** | Create, Read, Update, Delete as separate stories |
| 9 | **Break out a spike** | Separate research from implementation |
| 10 | **Happy path vs edge cases** | Ship the happy path first |

### Using the flowchart

Start at pattern 1. If it applies, split. If not, try the next. Most stories can be split with patterns 1-5. Patterns 6-10 are for stubborn stories.

Three one-hour practice sessions is typically enough for a team to become fluent with this flowchart.

## Elephant Carpaccio

Alistair Cockburn's exercise for practicing extreme thin-slicing.

### Core insight

All slicing decisions are based on the **business situation**, not the technology. The question is never "what technical component should I build?" but "what is the thinnest business-valuable behavior I can deliver?"

### The exercise

Teams build a simple calculator application in 40 minutes across 5 iterations of 8 minutes each. Constraints:

- Each iteration must produce a working, demonstrable increment
- Each increment must deliver user-visible value
- Target: 15-20 slices for what seems like a 1-story feature

### What teams learn

- Features that seem atomic ("calculate total with tax") can usually be split into 10+ nano-increments
- The first slice is always simpler than expected ("display a hardcoded result")
- Thin slices surface integration problems immediately instead of at the end
- Feedback loops tighten dramatically with thinner slices

## Killick's Slicing Heuristic

Neil Killick's approach replaces estimation with empirical measurement.

### The heuristic

Define an explicit policy for how thin to slice, then measure actual cycle times. If stories consistently take longer than 3 days, the heuristic is not slicing thinly enough.

### The "1 acceptance test" rule

A story should correspond to roughly **1 acceptance test**. This has been found empirically effective across domains for producing an average cycle time of ~3 days.

**Why it works**: A single acceptance test naturally scopes a story to one demonstrable behavior. Multiple acceptance tests signal that the story covers multiple behaviors and should be split.

### Applying it

1. Write the acceptance criteria for a story
2. Count the acceptance tests
3. If more than 1-2, split along test boundaries
4. Measure cycle times
5. Adjust the heuristic if cycle times drift above 3 days

## Vertical vs Horizontal Slicing

### Horizontal (anti-pattern for parallelism)

```
Phase 1: Build entire database layer
Phase 2: Build entire API layer
Phase 3: Build entire UI layer
Phase 4: Integration testing
```

**Problems**: No demonstrable progress until the end. Integration risk backloaded. Phase N+1 blocks on Phase N completing. Testing deferred until all layers exist.

### Vertical (enables parallelism)

```
Slice A: Login (UI + API + DB for login)
Slice B: Search (UI + API + DB for search)
Slice C: Checkout (UI + API + DB for checkout)
```

**Benefits**: Each slice is independently deployable, testable, and demoable. Different teams work on different slices simultaneously. Integration tested continuously. Feedback received from day 1.

### When horizontal is acceptable

- Pure infrastructure work (setting up CI, provisioning databases)
- Cross-cutting concerns that genuinely span all features (auth middleware, logging)
- Spikes and research

Even in these cases, prefer vertical slices where possible. "Set up CI" can be sliced into "CI for build" → "CI for tests" → "CI for deploy."
