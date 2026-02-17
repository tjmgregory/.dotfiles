# Comment Templates

Templates for consistent, well-structured review comments. The `post_review.py` script **automatically adds** `[🤖 Reviewer - <model>]:` prefix — write comment bodies without it. These templates show the final rendered format for reference.

## Reporting Issues

**Bug or logic error:**
```
[🤖 Reviewer - <model>]: This could cause [problem] when [condition]. Consider:
```suggestion
[fixed code]
```
```

**Security concern:**
```
[🤖 Reviewer - <model>]: Security: [vulnerability type] risk here. [Explanation of attack vector]. Fix:
```suggestion
[secure code]
```
```

**Performance issue:**
```
[🤖 Reviewer - <model>]: Performance: [operation] is O(n^2) due to [reason]. Consider [alternative approach].
```

## Asking Questions

**Clarifying intent:**
```
[🤖 Reviewer - <model>]: What happens if [edge case]? Should this handle [scenario]?
```

**Understanding design:**
```
[🤖 Reviewer - <model>]: Is [pattern] intentional here? It differs from [other_file] which uses [other_pattern].
```

## Suggestions

**Optional improvement:**
```
[🤖 Reviewer - <model>]: Optional: [improvement] would [benefit].
```

**Refactoring suggestion:**
```
[🤖 Reviewer - <model>]: Consider extracting [logic] into a helper—it's duplicated in [other_location].
```

## Minor Feedback

**Style nit:**
```
[🤖 Reviewer - <model>]: Nit: [observation]
```

**Naming suggestion:**
```
[🤖 Reviewer - <model>]: Nit: `[current_name]` might be clearer as `[suggested_name]` since it [reason].
```

## Thread Replies

**Agreeing with a point:**
```
[🤖 Reviewer - <model>]: +1 — [brief reason why this is a good point]
```

**Adding context:**
```
[🤖 Reviewer - <model>]: To add context: [relevant information about the code/pattern]
```

**Answering a question:**
```
[🤖 Reviewer - <model>]: [Direct answer]. This is because [explanation]. See [reference] for more details.
```

**Respectful disagreement:**
```
[🤖 Reviewer - <model>]: I see it differently — [alternative perspective]. [Supporting reasoning]. What do you think?
```
