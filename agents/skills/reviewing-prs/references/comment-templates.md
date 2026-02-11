# Comment Templates

Use these templates for consistent, well-structured review comments. Always prefix with `[Claude]:`.

## Reporting Issues

**Bug or logic error:**
```
[Claude]: This could cause [problem] when [condition]. Consider:
```suggestion
[fixed code]
```
```

**Security concern:**
```
[Claude]: Security: [vulnerability type] risk here. [Explanation of attack vector]. Fix:
```suggestion
[secure code]
```
```

**Performance issue:**
```
[Claude]: Performance: [operation] is O(n^2) due to [reason]. Consider [alternative approach].
```

## Asking Questions

**Clarifying intent:**
```
[Claude]: What happens if [edge case]? Should this handle [scenario]?
```

**Understanding design:**
```
[Claude]: Is [pattern] intentional here? It differs from [other_file] which uses [other_pattern].
```

## Suggestions

**Optional improvement:**
```
[Claude]: Optional: [improvement] would [benefit].
```

**Refactoring suggestion:**
```
[Claude]: Consider extracting [logic] into a helper—it's duplicated in [other_location].
```

## Minor Feedback

**Style nit:**
```
[Claude]: Nit: [observation]
```

**Naming suggestion:**
```
[Claude]: Nit: `[current_name]` might be clearer as `[suggested_name]` since it [reason].
```

## Thread Replies

**Agreeing with a point:**
```
[Claude]: +1 — [brief reason why this is a good point]
```

**Adding context:**
```
[Claude]: To add context: [relevant information about the code/pattern]
```

**Answering a question:**
```
[Claude]: [Direct answer]. This is because [explanation]. See [reference] for more details.
```

**Respectful disagreement:**
```
[Claude]: I see it differently — [alternative perspective]. [Supporting reasoning]. What do you think?
```
