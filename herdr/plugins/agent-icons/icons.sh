#!/usr/bin/env bash
# Sets the visible agent name to Nerd Font glyphs: an optional machine glyph
# followed by the agent glyph, with no separator. Glyphs are UTF-8 byte
# escapes so this file stays ASCII-safe. Edit the tables below to change them.
H="${HERDR_BIN_PATH:-herdr}"
machine_glyph() {
  case "$(hostname -s 2>/dev/null)" in
    M1-*|m1*) printf '\xef\x88\xb3' ;;  # U+F233 nf-fa-server
    *)        printf '' ;;              # laptop: nothing
  esac
}
agent_glyph() {
  case "$1" in
    claude) printf '\xef\x81\xa9' ;;   # U+F069 nf-fa-asterisk
    codex)  printf '\xef\x84\xa0' ;;   # U+F120 nf-fa-terminal
    *)      printf '\xef\x8b\x9b' ;;   # U+F2DB nf-fa-microchip
  esac
}
apply() { # pane_id agent
  [ -n "$1" ] && [ -n "$2" ] || return 0
  "$H" pane report-metadata "$1" --source agent-icons --agent "$2" \
    --display-agent "$(machine_glyph)$(agent_glyph "$2")" >/dev/null 2>&1 || true
}
if [ "$1" = "all" ]; then
  "$H" agent list 2>/dev/null | jq -r '.result.agents[] | "\(.pane_id)\t\(.agent)"' | while IFS=$'\t' read -r pane agent; do apply "$pane" "$agent"; done
else
  pane="${HERDR_PANE_ID:-}"; agent=""
  if [ -n "${HERDR_PLUGIN_EVENT_JSON:-}" ]; then
    [ -n "$pane" ] || pane=$(printf '%s' "$HERDR_PLUGIN_EVENT_JSON" | jq -r '[.. | objects | .pane_id? // empty][0] // empty')
    agent=$(printf '%s' "$HERDR_PLUGIN_EVENT_JSON" | jq -r '[.. | objects | .agent? // empty | strings][0] // empty')
  fi
  [ -n "$agent" ] || agent=$("$H" agent list 2>/dev/null | jq -r --arg p "$pane" '.result.agents[] | select(.pane_id==$p) | .agent' | head -1)
  apply "$pane" "$agent"
fi
