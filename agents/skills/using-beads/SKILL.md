---
name: using-beads
description: >
  Tracks issues using the bd CLI for multi-session work with dependencies, labels,
  and persistent memory across conversation compaction. Use when work spans sessions,
  has blockers, needs context recovery after compaction, or when user mentions bd,
  beads, tickets, or issue tracking.
allowed-tools: "Read,Bash(bd:*)"
---

# Beads - Persistent Task Memory for AI Agents

Graph-based issue tracker that survives conversation compaction. Use `bd <command> --help` for any command. Always use `--json` flag.

**Decision test**: "Will I need this context in 2 weeks?" YES → bd. NO → TodoWrite.

| bd | TodoWrite |
|----|-----------|
| Multi-session work | Single-session tasks |
| Dependencies or blockers | Linear step-by-step |
| Needs to survive compaction | All context in conversation |

**Using both**: TodoWrite tracks what to do now, bd records what was learned and why. At milestones, `bd comments add <id> "..."` to persist outcomes. Transition TodoWrite → bd when you discover blockers, dependencies, or won't finish this session.

**Create issues directly** for clear bugs, obvious follow-up, discovered blockers. **Ask first** for fuzzy scope, multiple valid approaches, or potential duplicates.

Sync is handled automatically by the daemon — never run `bd sync` manually.

## Planning & Decomposition

**Think before creating.** Survey the landscape to avoid overlap and understand context:

```bash
# 1. Check what already exists
bd list --status open --json                         # All open work
bd search "<topic>" --status open --json             # Existing work in this area
bd list --label-any <relevant-labels> --json         # Related by label

# 2. Build an external-ref map to detect overlap
bd list --status open --json | jq -r '.[] | select(.external_ref != null) | "\(.id)\t\(.external_ref)\t\(.title)"'
```

**Before creating a ticket, verify**:
- No open bead already covers this work (`bd search`)
- No existing bead shares the same `--external-ref` (same requirement = same ticket)
- The scope is right — not so broad it should be an epic, not so narrow it should be a comment

**Splitting heuristics**:
- Can it be completed in one session? → single ticket
- Does it have 2+ independent deliverables? → epic with children
- Does step N block step N+1? → separate tickets with `blocks` deps
- Is it a different concern discovered mid-work? → `discovered-from`, not a child

### Decomposing Epics

1. Create the epic with clear acceptance criteria for the *whole* outcome
2. Split into children using `--parent` — they get `parent.X` IDs ordered by sequence
3. Add `blocks` deps between children where order is enforced, not just preferred
4. Set `--external-ref` on each child that traces to a specific requirement or use case
5. Verify: no two children share an external ref (overlap signal), every external ref from the parent's scope is covered (completeness signal)

```bash
# Epic with ordered subtasks (parent.X naming)
bd create "API Migration" -t epic -p 1 --json                    # → bd-c4d2e1
bd create "Audit existing endpoints" --parent bd-c4d2e1 --json   # → bd-c4d2e1.1
bd create "Write adapter layer" --parent bd-c4d2e1 --json        # → bd-c4d2e1.2
bd create "Migrate consumers" --parent bd-c4d2e1 --json          # → bd-c4d2e1.3
bd create "Remove legacy API" --parent bd-c4d2e1 --json          # → bd-c4d2e1.4
```

Nesting works to any depth — children of children get `parent.X.Y`:

```bash
# Decompose a subtask further
bd create "Migrate users service" --parent bd-c4d2e1.3 --json   # → bd-c4d2e1.3.1
bd create "Migrate billing service" --parent bd-c4d2e1.3 --json # → bd-c4d2e1.3.2
```

The ID `bd-c4d2e1.3.2` reads naturally: epic `c4d2e1`, phase 3, sub-part 2.

Benefits:
- **Visual ordering**: `.1`, `.2`, `.3` shows the natural sequence of work
- **Grouping**: all children sort together under their parent
- **Context at a glance**: `bd-c4d2e1.3.2` immediately tells you epic → phase 3 → part 2
- **Arbitrary depth**: decompose as finely as the work demands

Use `bd children <parent-id> --json` to list children, or `bd dep tree <parent-id>` for the full hierarchy.

### Issue Content & Traceability

| Field | Purpose | Example |
|-------|---------|---------|
| Title | Clear, specific, action-oriented | "Fix: auth token expires before refresh" |
| Description (`-d`) | Problem + impact + context | "Token expires mid-session causing data loss for users on slow connections" |
| Design (`--design`) | Implementation approach (HOW) | "Use JWT with 1hr expiry, RS256 for rotation" |
| Acceptance (`--acceptance`) | Success criteria (WHAT) | "Tokens persist across sessions; refresh triggers before expiry" |
| Notes (`--notes`) | Supplementary context, research findings | "See RFC 7519 §4.1 for registered claims" |
| External ref (`--external-ref`) | Traceability to external systems | `gh-42`, `jira-AUTH-123`, `linear-ENG-456` |
| Comments | Progress notes, session handoffs | "Found root cause in validate()" |

**Writing good descriptions**: State the problem, its impact, and enough context to act on it. Bad: "Auth is broken". Good: "Token expires before refresh window, causing 401s for users mid-session. Affects ~12% of requests over 45min."

**Formatting**: Use fenced code blocks for directory trees, file structures, or any indented content in descriptions — plain indentation does not render correctly in most viewers.

**Design vs acceptance**: Design can change; acceptance should stay stable. If you rewrote the solution differently, would the criteria still apply? If not, it's a design note.

**Traceability**: Link every issue to its origin. Use `--external-ref` for requirements, use cases, or tickets from external systems. Use `--deps discovered-from:<id>` for issues found while working on another bead. The goal: any issue can be traced back to *why* it exists.

```bash
# Full example with traceability
bd create "Fix token refresh race condition" \
  -t bug -p 1 \
  -d "Token expires before refresh window, causing 401s mid-session" \
  --acceptance "No 401s during active sessions; refresh triggers 5min before expiry" \
  --design "Add refresh buffer to token lifecycle; use sliding window" \
  --external-ref "gh-87" \
  --deps discovered-from:bd-a3f8e9.2 \
  --json
```

For complex multi-session work, add comments with enough context for a fresh Claude to resume — working code, API response samples, desired output format, research context.

## Find Work

```bash
bd ready --json                                           # Unblocked work
bd blocked --json                                         # What's stuck
bd stale --days 30 --json                                 # Not updated recently
```

## Create Issues

```bash
# Always quote titles and descriptions with double quotes
bd create "Issue title" -t bug|feature|task -p 0-4 -d "Description" --json
bd create "Issue title" -t bug -p 1 -l bug,critical --json    # With labels

# Epics with hierarchical children (parent.X naming)
bd create "Auth System" -t epic -p 1 --json         # Returns: bd-a3f8e9
bd create "Login UI" -p 1 --parent bd-a3f8e9 --json              # → bd-a3f8e9.1
bd create "Session Management" -p 1 --parent bd-a3f8e9 --json    # → bd-a3f8e9.2
bd create "Password Reset" -p 1 --parent bd-a3f8e9 --json        # → bd-a3f8e9.3

# Create and link discovered work (one command)
bd create "Found bug" -t bug -p 1 --deps discovered-from:<parent-id> --json

# Quick capture (outputs only the ID)
bd q "Fix login bug"
```

## Update / Close / Reopen

```bash
bd update <id> [<id>...] --status in_progress --json
bd update <id> [<id>...] --priority 1 --json
bd close <id> [<id>...] --reason "Done" --json
bd reopen <id> [<id>...] --reason "Reopening" --json
```

## View Issues

```bash
bd show <id> [<id>...] --json
bd dep tree <id>
```

## Comments

Comments are the primary way to record progress and context. They survive compaction and are critical for multi-session continuity.

```bash
bd comments add bd-123 "Found root cause: missing null check in validate()"
bd comments add bd-123 -f notes.txt
bd comments bd-123 --json                                 # List comments
```

## Dependencies & Labels

Four dependency types. Only `blocks` affects `bd ready`.

| Type | Purpose | Affects `bd ready`? |
|------|---------|---------------------|
| **blocks** | Hard blocker — B can't start until A completes | Yes |
| **related** | Soft link — informational only | No |
| **parent-child** | Hierarchy — epics and subtasks | No |
| **discovered-from** | Provenance — tracks where work was found | No |

```
Does A prevent B from starting?  → blocks
Is B a subtask of A?            → parent-child
Was B discovered while doing A?  → discovered-from
Otherwise                        → related
```

```bash
# Create + link in one command (preferred)
bd create "Issue title" -t bug -p 1 --deps discovered-from:<parent-id> --json

# Or link separately — direction: bd dep add <dependent> <depends-on>
bd dep add B A --type blocks              # B is blocked by A (A must complete before B)
bd dep add B A --type parent-child        # B is subtask of epic A
bd dep add B A --type discovered-from     # B was discovered while working on A
bd dep add A B --type related             # Informational link (direction doesn't matter)

# Labels (supports multiple IDs)
bd label add <id> [<id>...] <label> --json
bd label remove <id> [<id>...] <label> --json
```

**Don't use blocks for preferences** ("should do X first"). Use `related` or note it in the description. Closing a blocking issue automatically unblocks dependents.

**Traceability through deps**: `discovered-from` creates a provenance chain — trace any bug back to the work that uncovered it. Combine with `--external-ref` for full traceability from external requirement → bead → child beads → discovered work.

## Filtering & Search

```bash
bd list --status open --priority 1 --json
bd list --type bug --json
bd list --label bug,critical --json                       # AND: must have ALL
bd list --label-any frontend,backend --json               # OR: has ANY
bd list --title-contains "auth" --json
bd list --status open --priority 1 --label-any urgent,critical --no-assignee --json

bd search "authentication bug"
bd search "login" --status open --json
bd search "bug" --sort priority
```

## Issue Types & Priorities

Types: `bug`, `feature`, `task`, `epic`, `chore`

Priorities: `0` critical, `1` high, `2` medium, `3` low, `4` backlog

## Workflow Patterns

### Status Transitions

```
open → in_progress → closed
  ↓         ↓
blocked   blocked
```

### Session Workflow

```bash
bd ready --json                                           # Find work
bd update bd-42 --status in_progress --json               # Claim it
bd comments add bd-42 "Found root cause in auth.ts:42"    # Record progress
bd close bd-42 --reason "Fixed auth validation" --json    # Complete
```

### Side Quest Handling

When you discover work during a task, create and link in one command:

```bash
bd create "Found auth bug" -t bug -p 1 --deps discovered-from:bd-100 --json
```

If the discovery blocks current work: `bd update bd-100 --status blocked`, work on the blocker. If deferrable: add a comment with context and continue.

### Compaction Recovery

After compaction, conversation history is lost but bd state survives:

1. `bd list --status in_progress --json` — Find what was active
2. `bd show <id> --json` — Read comments for context
3. Resume work based on the context in comments

### Batch Operations

```bash
bd update bd-41 bd-42 bd-43 --priority 0 --json
bd close bd-41 bd-42 bd-43 --reason "Batch completion" --json
bd label add bd-41 bd-42 bd-43 urgent --json
```

## References

| Resource | When to read |
|----------|-------------|
| [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) | Dependencies or status updates not working |
