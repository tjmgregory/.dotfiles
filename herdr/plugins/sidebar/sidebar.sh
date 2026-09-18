#!/usr/bin/env bash
# Herdr sidebar plugin.
#  - display-agent: Nerd Font glyphs (machine glyph on the M1 + agent glyph)
#  - $area token: which root folder the agent runs in, from areas.json
#    (longest matching path wins; unmatched panes use their top-level folder)
#  - Agents view: sorted by area name, then attention, then latest change
# Glyphs are UTF-8 byte escapes so this file stays ASCII-safe.
H="${HERDR_BIN_PATH:-herdr}"
ROOT="${HERDR_PLUGIN_ROOT:-$(cd "$(dirname "$0")" && pwd)}"
SOURCE="plugin:theo.sidebar"

machine_glyph() {
  case "$(hostname -s 2>/dev/null)" in
    M1-*|m1*) printf '\xef\x88\xb3' ;;  # U+F233 nf-fa-server
    *)        printf '' ;;
  esac
}
agent_glyph() {
  case "$1" in
    claude) printf '\xef\x81\xa9' ;;   # U+F069 nf-fa-asterisk
    codex)  printf '\xef\x84\xa0' ;;   # U+F120 nf-fa-terminal
    *)      printf '\xef\x8b\x9b' ;;   # U+F2DB nf-fa-microchip
  esac
}
area_for() { # cwd -> area name
  jq -r --arg cwd "$1" --arg home "$HOME" '
    [ to_entries[] | .key as $k | .value[] | sub("^~"; $home) as $p
      | select($cwd == $p or ($cwd | startswith($p + "/"))) | {k: $k, n: ($p | length)} ]
    | sort_by(-.n) | .[0].k // empty' "$ROOT/areas.json" 2>/dev/null
}
fallback_area() { # top-level folder under $HOME, or "~"
  case "$1" in
    "$HOME") echo "~" ;;
    "$HOME"/*) printf '%s' "${1#$HOME/}" | cut -d/ -f1 ;;
    *) basename "$1" ;;
  esac
}
stamp() { # pane_id agent cwd
  [ -n "$1" ] && [ -n "$2" ] || return 0
  local area; area=$(area_for "$3"); [ -n "$area" ] || area=$(fallback_area "$3")
  "$H" pane report-metadata "$1" --source theo.sidebar --agent "$2" \
    --display-agent "$(machine_glyph)$(agent_glyph "$2")" --token area="$area" >/dev/null 2>&1 || true
}
apply_view() {
  [ -n "${HERDR_SOCKET_PATH:-}" ] || return 0
  python3 - "$HERDR_SOCKET_PATH" "$SOURCE" <<'PY'
import socket, sys, json
s = socket.socket(socket.AF_UNIX); s.settimeout(5); s.connect(sys.argv[1])
req = {"id": "sidebar_view", "method": "agent.view.set", "params": {
    "source": sys.argv[2], "label": "areas",
    "sort": [
        {"field": {"token": "area"}, "order": "asc"},
        {"field": "attention", "order": "desc"},
        {"field": "state_change_seq", "order": "desc"},
    ]}}
s.sendall((json.dumps(req) + "\n").encode())
print(s.recv(65536).decode().strip())
PY
}
stamp_all() {
  "$H" agent list 2>/dev/null | jq -r '.result.agents[] | "\(.pane_id)\t\(.agent)\t\(.foreground_cwd // .cwd)"' \
    | while IFS=$'\t' read -r pane agent cwd; do stamp "$pane" "$agent" "$cwd"; done
}
case "$1" in
  startup|all) stamp_all; apply_view ;;
  view) apply_view ;;
  *)
    pane="${HERDR_PANE_ID:-}"; agent=""
    if [ -n "${HERDR_PLUGIN_EVENT_JSON:-}" ]; then
      [ -n "$pane" ] || pane=$(printf '%s' "$HERDR_PLUGIN_EVENT_JSON" | jq -r '[.. | objects | .pane_id? // empty][0] // empty')
      agent=$(printf '%s' "$HERDR_PLUGIN_EVENT_JSON" | jq -r '[.. | objects | .agent? // empty | strings][0] // empty')
    fi
    read -r agent2 cwd < <("$H" agent list 2>/dev/null | jq -r --arg p "$pane" '.result.agents[] | select(.pane_id==$p) | "\(.agent) \(.foreground_cwd // .cwd)"' | head -1)
    [ -n "$agent" ] || agent="$agent2"
    stamp "$pane" "$agent" "$cwd" ;;
esac
