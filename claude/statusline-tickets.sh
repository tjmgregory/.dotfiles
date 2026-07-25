#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# Active-ticket widget for ccstatusline (Custom Command)
# ──────────────────────────────────────────────────────────────────────────────
#
# Prints the ticket ID(s) you're actually working on, e.g. "TSE-412,VOC-88".
# Prints nothing when no ticket is credibly active — the widget then collapses.
#
# Extracted from the old tse/.claude/statusline.sh, which also rendered project,
# worktree, model and context-remaining. Those are all covered by native
# ccstatusline widgets now; this scoring logic had no equivalent, so it stayed.
#
# HOW IT WORKS
#   Grep the tail-window of the session transcript for every `<PREFIX>-<digits>`
#   token, then score each ticket with recency-weighted occurrences:
#       weight(pos) = exp(-ln(2) · (N - pos) / halflife)
#       halflife    = N / 2
#       score(id)   = Σ weight over all occurrences of id
#   N is the total number of ID matches in the window, pos is each match index
#   (1..N). A mention at the very end weighs 1.0, halfway back 0.5, oldest 0.25.
#   Keep IDs with score ≥1.5, sort by score desc, alphabetical tiebreak. Capped
#   at 5; 5th slot becomes "..." if more qualify.
#
#   Why halflife = N/2? "A mention halfway back counts for half" is the
#   intuition. Aggressive enough that the active ticket beats one that was busy
#   at session start; gentle enough that bursty older work still surfaces
#   (10 old hits × 0.25 = 2.5 ≈ 3 fresh hits × 1.0). N being match-count (not
#   bytes or wall-clock) means halflife scales with how ticket-heavy the
#   conversation is — recency is *relative to pace*, which matches intent.
#
#   Why floor = 1.5? In score units: 1 mention maxes at 1.0 (never qualifies —
#   drive-by); 2 fresh mentions ≈ 1.9 (qualifies, just); 3 fresh ≈ 2.7; 4 evenly
#   distributed ≈ 2.3 (qualifies). So 1.5 is "the lightest credible signal of
#   engagement". Early in a session the agent often scans adjacent tickets to
#   orient itself — those 1–2 hit mentions shouldn't crowd the status line. Real
#   work produces many mentions (CLI claim call, branch name, comments, PR refs).
#
# GOTCHAS
#   - Transcripts get LONG and this fires every render, so we `tail -c` a window
#     from the end rather than scanning start-to-end. Tune TAIL_BYTES if tickets
#     from earlier in the session drop off too eagerly.
#   - Stale tickets across sessions: the transcript persists, so yesterday's IDs
#     show until they fall off the window or decay below the floor. ~200kB of
#     tail is roughly "this session" in practice.
#   - Glance at a ticket once and that's the work? It won't appear. This is a
#     reflection, not a tracker.
#
# INPUT
#   Claude Code / ccstatusline JSON on stdin. Only `.transcript_path` is used.
# ──────────────────────────────────────────────────────────────────────────────

set -u

TAIL_BYTES=200000  # window of transcript bytes scanned from the end

# Ticket-ID shape. Prefix is >=3 chars because Paper MCP node IDs ("NZ-0",
# "NY-0") are 2-letter and otherwise score their way onto the status line —
# they appear hundreds of times in a design session. Every Linear team key in
# use is 3-4 chars (TSE, VOC, PNE, PENG, BUS2, FOUNDRY, ...). Override with
# CCSL_TICKET_RE if a 2-letter prefix ever matters.
# (assigned in two steps: a `}` inside ${VAR:-default} would close the
# expansion early)
TICKET_RE='\b[A-Z][A-Z0-9]{2,}-[0-9]+\b'
[[ -n "${CCSL_TICKET_RE:-}" ]] && TICKET_RE="$CCSL_TICKET_RE"

input="$(cat)"

if command -v jq >/dev/null 2>&1; then
  transcript="$(printf '%s' "$input" | jq -r '.transcript_path // empty')"
else
  transcript="$(printf '%s' "$input" | sed -n 's/.*"transcript_path":[[:space:]]*"\([^"]*\)".*/\1/p')"
fi

[[ -n "$transcript" && -f "$transcript" ]] || exit 0

tail_window="$(tail -c "$TAIL_BYTES" "$transcript" 2>/dev/null || true)"
[[ -n "$tail_window" ]] || exit 0

# First awk records count + every occurrence position per ID, then in END
# computes the exp-decay score. Output: "<score> <id>". Sort by score desc,
# alphabetical tiebreak. Final awk caps at 5, replacing the 5th slot with "..."
# when more qualify.
printf '%s' "$tail_window" \
  | grep -oE "$TICKET_RE" \
  | awk '
      { count[$0]++; pos[$0,count[$0]] = NR }
      END {
        N = NR
        if (N == 0) exit
        hl = N / 2; if (hl < 1) hl = 1
        k = log(2) / hl
        for (id in count) {
          s = 0
          for (i = 1; i <= count[id]; i++) s += exp(-k * (N - pos[id,i]))
          if (s >= 1.5) printf "%.6f %s\n", s, id
        }
      }' \
  | sort -k1,1nr -k2,2 \
  | awk '{ ids[NR]=$2 } END {
      if (NR <= 5) {
        for (i=1; i<=NR; i++) printf "%s%s", ids[i], (i<NR ? "," : "")
      } else {
        for (i=1; i<=4; i++) printf "%s,", ids[i]
        printf "..."
      }
    }'
