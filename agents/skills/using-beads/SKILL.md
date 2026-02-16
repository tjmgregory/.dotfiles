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

# Epics with hierarchical children
bd create "Auth System" -t epic -p 1 --json         # Returns: bd-a3f8e9
bd create "Login UI" -p 1 --json                     # Auto-assigned: bd-a3f8e9.1

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

## Patterns

### Issue Creation Fields

| Field | Purpose | Example |
|-------|---------|---------|
| Title | Clear, specific, action-oriented | "Fix: auth token expires before refresh" |
| Description (`-d`) | Problem statement and context | Why this matters, what's broken |
| Design (`--design`) | Implementation approach (HOW) | "Use JWT with 1hr expiry, RS256 for rotation" |
| Acceptance (`--acceptance`) | Success criteria (WHAT) | "Tokens persist across sessions" |
| Comments | Progress notes, session handoffs | "Found root cause in validate()" |

**Design vs acceptance**: Design can change; acceptance should stay stable. If you rewrote the solution differently, would the criteria still apply? If not, it's a design note.

For complex multi-session work, add comments with enough context for a fresh Claude to resume — working code, API response samples, desired output format, research context.

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

## Resources

| Resource | When to read |
|----------|-------------|
| [TROUBLESHOOTING.md](resources/TROUBLESHOOTING.md) | Dependencies or status updates not working |
