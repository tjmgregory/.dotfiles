#!/usr/bin/env bash
# Popup: create a Space on a chosen machine. Asks machine, area (from areas.json)
# or a path, and a name, then creates the workspace there with focus.
# Herdr cannot switch the client's selected machine from a script, so after a
# remote create pick the new Space in the sidebar (prefix+w).
H="${HERDR_BIN_PATH:-herdr}"
ROOT="$(cd "$(dirname "$0")" && pwd)"

printf '\nMachine\n'
machines=("Local")
ids=("")
while IFS=$'\t' read -r id label target session enabled; do
  [ "$enabled" = "enabled" ] || continue
  machines+=("$label ($target)"); ids+=("$id")
done < <("$H" machine list 2>/dev/null)
for i in "${!machines[@]}"; do printf '  %d) %s\n' "$((i+1))" "${machines[$i]}"; done
read -r -p "> " m; m=${m:-1}
mid="${ids[$((m-1))]}"
mflag=(); [ -n "$mid" ] && mflag=(--machine "$mid")

printf '\nFolder (area number or a path)\n'
areas=(); paths=()
while IFS=$'\t' read -r a p; do areas+=("$a"); paths+=("$p"); done < <(jq -r '
  to_entries[] | select(.key | startswith("_") | not) | [.key, .value.paths[0]] | @tsv' "$ROOT/areas.json")
for i in "${!areas[@]}"; do printf '  %d) %-9s %s\n' "$((i+1))" "${areas[$i]}" "${paths[$i]}"; done
read -r -p "> " f
case "$f" in
  ''|*[!0-9]*) cwd="$f" ;;
  *) cwd="${paths[$((f-1))]}" ;;
esac
[ -n "$cwd" ] || cwd='~'

printf '\nName\n'
read -r -p "> " label
[ -n "$label" ] || label="$(basename "$cwd")"

out=$("$H" "${mflag[@]}" workspace create --cwd "$cwd" --label "$label" --focus 2>&1) || { printf '%s\n' "$out"; read -r -p "enter to close"; exit 1; }
printf '\ncreated %s on %s\n' "$label" "${machines[$((m-1))]}"
[ -n "$mid" ] && { printf 'select it in the sidebar (prefix+w)\n'; sleep 2; }
