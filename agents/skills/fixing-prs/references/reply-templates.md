# Reply Templates

The `post_reply.py` script automatically adds `[🤖 {role} - {model}]:` prefix (e.g. `[🤖 Author - Opus 4.6]:`). These templates show only the message body to pass via `body`.

## Assessment Categories

### Valid & Actionable

Reviewer identified a real issue with a clear fix. Make the change.

**Examples:**
- "This null check won't catch undefined" — Add undefined check
- "Missing error handling for network failures" — Add try/catch
- "SQL injection risk here" — Switch to parameterized query
- "This will throw if array is empty" — Add length check

**Reply template:**
```
Done — updated X to Y as suggested.
```

**With code suggestion:**
```
Fixed. Changed to:
```suggestion
const user = getUser()?.email ?? 'anonymous'
```
```

### Valid but Disagree

Technically correct suggestion, but current approach is intentional or preferable.

**Examples:**
- "Use lodash.get here" — Keeping native optional chaining to minimize dependencies
- "Extract this to a separate function" — Keeping inline for readability in this context
- "Add caching here" — Premature optimization; profiling shows this isn't a bottleneck
- "Use async/await instead of .then()" — Matching existing codebase style

**Reply template:**
```
Keeping the current approach because [specific technical reason].
The suggestion would [tradeoff]. Happy to discuss if you see it differently.
```

### Invalid / Not Applicable

Suggestion doesn't apply to this code or is based on a misunderstanding.

**Examples:**
- Concern about null when value is guaranteed non-null by type system
- Security concern about input that's already validated upstream
- Performance concern about code that only runs once at startup
- Suggesting a pattern that's incompatible with the framework version

**Reply template:**
```
No change — [explain why it doesn't apply].
[Optional: point to where the concern IS handled, e.g., "Validation happens at line X"]
```

### Unclear / Need Clarification

Can't determine what change is being requested.

**Examples:**
- "This seems wrong" (no specifics)
- "Consider refactoring" (no direction)
- Ambiguous pronoun references ("it should handle this")

**Reply template:**
```
Could you clarify [specific question]?
I want to make sure I address the right concern.
```

## Priority Markers

Use these prefixes in your message body to indicate severity:

| Prefix | Meaning |
|--------|---------|
| (none) | Standard feedback |
| **Blocker:** | Must fix before merge |
| **Nit:** | Minor/optional |

**Examples:**
```
Blocker: Fixed the SQL injection — now using parameterized queries.
```

```
Nit: Renamed to `fetchUserData` as suggested.
```

## Thread Replies

When replying to follow-up questions on previous agent comments:

**Answering a question:**
```
[Direct answer]. This is because [explanation].
```

**Acknowledging a point:**
```
Good point — updated to handle that case.
```

**Respectful disagreement:**
```
I see it differently — [alternative perspective].
[Supporting reasoning]. What do you think?
```
