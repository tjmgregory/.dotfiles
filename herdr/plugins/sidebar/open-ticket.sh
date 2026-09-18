#!/usr/bin/env bash
# Plugin action: open the Linear ticket attached to the active pane (or its
# workspace) in the browser. Ticket ids arrive as the $ticket metadata token,
# reported by claude/hooks/herdr-ticket.sh.
H="${HERDR_BIN_PATH:-herdr}"
LINEAR_WORKSPACE="${LINEAR_WORKSPACE:-the-software-engineer}"
id=""
if [ -n "${HERDR_PANE_ID:-}" ]; then
  id=$("$H" pane get "$HERDR_PANE_ID" 2>/dev/null | jq -r '.result.pane.tokens.ticket // empty')
fi
if [ -z "$id" ] && [ -n "${HERDR_WORKSPACE_ID:-}" ]; then
  id=$("$H" workspace get "$HERDR_WORKSPACE_ID" 2>/dev/null | jq -r '.result.workspace.tokens.ticket // .result.workspace.metadata.ticket // empty')
fi
if [ -z "$id" ]; then
  "$H" notification show "No ticket" --body "This pane has no Linear ticket yet" >/dev/null 2>&1 || true
  exit 0
fi
url="https://linear.app/$LINEAR_WORKSPACE/issue/$id"
if command -v open >/dev/null; then open "$url"; else xdg-open "$url"; fi
