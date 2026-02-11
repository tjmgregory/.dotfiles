# Script Best Practices

## Structured Output for AI Consumption

Scripts consumed by AI agents should output structured JSON by default. This prevents AIs from attempting fragile text parsing or constructing jq pipelines on the fly.

**Key principles:**

1. **Output JSON to stdout** - The script handles JSON construction internally
2. **Progress messages to stderr** - Human-readable status updates go to stderr
3. **Errors as JSON** - Return `{"error": "message"}` rather than just printing and exiting
4. **Optional format flag** - Add `--format=json|text` if human readability is also needed

**Good** - Script outputs structured JSON:
```bash
#!/usr/bin/env bash
echo "Fetching data..." >&2  # Progress to stderr

RESULT=$(some_command)
if [[ $? -ne 0 ]]; then
    echo '{"error": "Failed to fetch data"}'  # Error as JSON
    exit 1
fi

# Structured output to stdout
jq -n --arg data "$RESULT" '{"status": "ok", "data": $data}'
```

**Bad** - AI must parse text or pipe through jq:
```bash
#!/usr/bin/env bash
echo "=== RESULTS ==="
echo "Found 3 items:"
echo "- item1"
echo "- item2"
echo "- item3"
# AI now has to parse this text format
```

**Bad** - Raw JSON that AI must process:
```bash
#!/usr/bin/env bash
gh api /repos/owner/repo/issues  # Raw API response, AI pipes through jq
```

For a complete example, see `fixing-pr-comments/scripts/fetch_comments.sh` which outputs structured JSON with progress messages to stderr.

## Structured Input for AI Permissioning

Scripts should accept JSON input via stdin only — do not provide CLI argument fallbacks. AI permission systems struggle with complex CLI arguments that require quoting, escaping, or special characters.

**Why JSON-only via stdin:**
- Permission prompts display the command being run
- Complex CLI arguments with quotes/escapes are hard to parse and validate
- JSON input is unambiguous and self-documenting
- Easier for AIs to construct correctly
- CLI fallbacks encourage the wrong pattern — if it exists, AI may use it
- Humans can still use heredocs for manual testing

**Good** - JSON-only via stdin:
```python
#!/usr/bin/env python3
import sys
import json

def main():
    if sys.stdin.isatty():
        print("Error: This script requires JSON input via stdin", file=sys.stderr)
        print("Usage: script.py <<'EOF'", file=sys.stderr)
        print('{"pr": "123", "body": "Your message"}', file=sys.stderr)
        print("EOF", file=sys.stderr)
        sys.exit(1)

    data = json.load(sys.stdin)
    pr_ref = data["pr"]
    body = data["body"]
```

**Usage:**
```bash
# Heredoc with JSON (command first, multiline support, no escaping)
./post_reply.py <<'EOF'
{
  "pr": "123",
  "body": "Fixed the issue.\nAdded tests too."
}
EOF
```

**Bad** - CLI arguments (even as fallback):
```bash
# Hard to permission, easy to get quoting wrong
./post_reply.py 123 --body "He said \"hello\" and it's working"
```

**Why heredocs:**
- Command appears first (easier to scan permission prompts)
- Multiline JSON is natural, no `\n` escaping needed
- `<<'EOF'` prevents shell variable expansion (safe for arbitrary content)
- Works for both AI and human callers

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
