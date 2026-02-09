# Script Best Practices

## Execution Intent Clarity

When referencing scripts in SKILL.md, clearly indicate whether Claude should execute or read them:

- **Execute** (most common): "Run `scripts/analyze_form.py` to extract fields"
- **Read as reference**: "See `scripts/analyze_form.py` for the extraction algorithm"

For most utility scripts, execution is preferred because it's more reliable and token-efficient.

## Solve, Don't Punt

Scripts should handle error conditions rather than failing and leaving Claude to figure it out.

**Good** - Handle errors explicitly:
```python
def process_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
```

**Bad** - Punt to Claude:
```python
def process_file(path):
    return open(path).read()  # Just fails, Claude must figure it out
```

## Justify Configuration Values

Avoid "voodoo constants" - all configuration values should be documented with justification:

**Good**:
```python
# HTTP requests typically complete within 30 seconds
# Longer timeout accounts for slow connections
REQUEST_TIMEOUT = 30
```

**Bad**:
```python
TIMEOUT = 47  # Why 47?
```

## MCP Tool References

If a skill uses MCP (Model Context Protocol) tools, always use fully qualified names:

**Format**: `ServerName:tool_name`

**Example**: "Use the `BigQuery:bigquery_schema` tool to retrieve table schemas."

Without the server prefix, Claude may fail to locate the tool.

## Feedback Loops

For skills where output quality is critical, implement the "validate → fix → repeat" pattern:

```markdown
## Document editing process

1. Make your edits to `word/document.xml`
2. **Validate immediately**: Run `scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild the document
```

This pattern catches errors early before they compound.
