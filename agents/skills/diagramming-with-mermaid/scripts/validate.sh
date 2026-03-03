#!/usr/bin/env bash
set -euo pipefail

# Validates Mermaid diagram syntax using mmdc (mermaid-cli).
# Input: JSON via stdin with "diagram" field containing raw Mermaid source.
# Output: JSON to stdout with validation result.
#
# Usage:
#   scripts/validate.sh <<'EOF'
#   {"diagram": "flowchart TD\n    A --> B"}
#   EOF

# --- Check dependencies ---
if ! command -v mmdc &>/dev/null; then
  echo '{"valid": false, "error": "mmdc not found. Install with: npm install -g @mermaid-js/mermaid-cli"}'
  exit 1
fi

if ! command -v jq &>/dev/null; then
  echo '{"valid": false, "error": "jq not found. Install with: brew install jq"}'
  exit 1
fi

# --- Read input ---
if [ -t 0 ]; then
  echo "Error: This script requires JSON input via stdin" >&2
  echo 'Usage: scripts/validate.sh <<'\''EOF'\''' >&2
  echo '{"diagram": "flowchart TD\n    A --> B"}' >&2
  echo 'EOF' >&2
  exit 1
fi

INPUT=$(cat)
DIAGRAM=$(echo "$INPUT" | jq -r '.diagram // empty')

if [ -z "$DIAGRAM" ]; then
  echo '{"valid": false, "error": "Missing required field: diagram"}'
  exit 1
fi

# --- Validate ---
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Write diagram to temp file, interpreting \n as newlines
printf '%b' "$DIAGRAM" > "$TMPDIR/diagram.mmd"

echo "Validating diagram..." >&2

MMDC_OUTPUT=$(mmdc -i "$TMPDIR/diagram.mmd" -o "$TMPDIR/diagram.svg" -q 2>&1) || true
EXIT_CODE=${PIPESTATUS[0]:-$?}

if [ -f "$TMPDIR/diagram.svg" ] && [ -s "$TMPDIR/diagram.svg" ]; then
  echo '{"valid": true}'
else
  # Extract the useful parse error, drop the stack trace noise
  PARSE_ERROR=$(echo "$MMDC_OUTPUT" | sed -n '/^Error:/,/^Expecting/p' | head -20)

  if [ -z "$PARSE_ERROR" ]; then
    # Fallback: return first 10 lines if no structured error found
    PARSE_ERROR=$(echo "$MMDC_OUTPUT" | head -10)
  fi

  jq -n --arg error "$PARSE_ERROR" '{"valid": false, "error": $error}'
fi
