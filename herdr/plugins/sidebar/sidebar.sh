#!/usr/bin/env bash
# Herdr sidebar plugin. For every agent pane it reports:
#  - $area  : which root folder the agent runs in, from areas.json
#             (longest matching path wins; unmatched panes use their top-level folder)
#  - $line  : "<marker><machine glyph><agent glyph> <ticket> <space name>", one token
#             so the whole line can take the area colour. The marker is an invisible
#             zero-width character per area that the config.toml colour rules match.
#             The agent's own title goes on the second sidebar row, from Herdr itself.
#  - display-agent glyphs, for any layout that still shows the agent token
# It also installs the Agents view: sorted by area, then attention, then latest change.
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
    [ to_entries[] | select(.key | startswith("_") | not) | .key as $k | .value.paths[] | sub("^~"; $home) as $p
      | select($cwd == $p or ($cwd | startswith($p + "/"))) | {k: $k, n: ($p | length)} ]
    | sort_by(-.n) | .[0].k // empty' "$ROOT/areas.json" 2>/dev/null
}
marker_for() { jq -r --arg a "$1" '.[$a].marker // empty' "$ROOT/areas.json" 2>/dev/null; }
fallback_area() {
  case "$1" in
    "$HOME") echo "~" ;;
    "$HOME"/*) printf '%s' "${1#$HOME/}" | cut -d/ -f1 ;;
    *) basename "$1" ;;
  esac
}
stamp() { # pane_id agent cwd ticket space_label
  [ -n "$1" ] && [ -n "$2" ] || return 0
  local area line; area=$(area_for "$3"); [ -n "$area" ] || area=$(fallback_area "$3")
  line="$(marker_for "$area")$(machine_glyph)$(agent_glyph "$2")"
  [ -n "$4" ] && line="$line $4"
  [ -n "$5" ] && line="$line $5"
  line=$(printf '%s' "$line" | cut -c1-80)
  "$H" pane report-metadata "$1" --source theo.sidebar --agent "$2" \
    --display-agent "$(machine_glyph)$(agent_glyph "$2")" \
    --token area="$area" --token line="$line" >/dev/null 2>&1 || true
}
stamp_pane() { # pane_id
  local pane="$1" agent cwd ticket wsid
  # unit separator, not tab: empty fields must not collapse under read
  IFS=$'\x1f' read -r agent cwd ticket wsid < <("$H" agent list 2>/dev/null \
    | jq -r --arg p "$pane" '.result.agents[] | select(.pane_id==$p)
        | [.agent, (.foreground_cwd // .cwd), (.tokens.ticket // ""), .workspace_id] | join("\u001f")' | head -1)
  local label; label=$("$H" workspace get "$wsid" 2>/dev/null | jq -r '.result.workspace.label // empty')
  stamp "$pane" "$agent" "$cwd" "$ticket" "$label"
}
stamp_all() {
  "$H" agent list 2>/dev/null | jq -r '.result.agents[].pane_id' | while read -r pane; do stamp_pane "$pane"; done
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
case "$1" in
  startup|all) stamp_all; apply_view ;;
  view) apply_view ;;
  pane) stamp_pane "$2" ;;
  *)
    pane="${HERDR_PANE_ID:-}"
    [ -n "$pane" ] || pane=$(printf '%s' "${HERDR_PLUGIN_EVENT_JSON:-}" | jq -r '[.. | objects | .pane_id? // empty][0] // empty')
    if [ -n "$pane" ]; then stamp_pane "$pane"; else stamp_all; fi ;;
esac
