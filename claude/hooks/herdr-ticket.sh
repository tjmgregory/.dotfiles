#!/usr/bin/env bash
# PostToolUse hook for Claude Code and Codex. When a command claims a Linear ticket
# (linear issue update TSE-123 ...) or enters a worktree named after one
# (worktrees/TSE-123-...), report it to Herdr as the $ticket token on this
# workspace and pane. Always exits 0.
[ "${HERDR_ENV:-}" = "1" ] || exit 0
[ -n "${HERDR_WORKSPACE_ID:-}" ] || exit 0
H="${HERDR_BIN_PATH:-herdr}"
text=$(jq -r '[.. | strings] | join(" ")' 2>/dev/null) || exit 0
id=$(printf '%s' "$text" | grep -oE '(linear issue update|worktrees/)[ /]*[A-Z][A-Z0-9]{1,9}-[0-9]+' | grep -oE '[A-Z][A-Z0-9]{1,9}-[0-9]+' | head -1)
[ -n "$id" ] || exit 0
"$H" workspace report-metadata "$HERDR_WORKSPACE_ID" --source ticket --token ticket="$id" >/dev/null 2>&1 || true
[ -n "${HERDR_PANE_ID:-}" ] && "$H" pane report-metadata "$HERDR_PANE_ID" --source ticket --token ticket="$id" >/dev/null 2>&1 || true
exit 0
