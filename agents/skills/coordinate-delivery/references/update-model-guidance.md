# Update model guidance

The same committed script, policy, and snapshot MUST produce byte-identical tables and decisions. A live refresh MAY change results because evidence changed. Availability comes from Theo; MUST NOT recheck account access.

## Inputs

`data/policy.json` MUST hold exact model-name mappings, allowed configurations, task metrics, frozen quality floors, incumbents, and pinned provisional routes. Floors initially come from the previous table's measured incumbent scores, not invented tolerances. A policy edit is a visible judgment change.

`data/evidence.json` MUST hold parsed measurements and source provenance. Scores use percentage points; money uses USD; time uses seconds. Missing values MUST remain null. Comparisons MUST use one explicit comparison group (source, harness, benchmark/scoring/task-set/budget context). Unknown setup details MUST remain marked provisional, never asserted equal to another dataset.

## Refresh

1. MUST commit current guidance before edits. Add Theo's models to policy mappings; MUST NOT guess aliases or settings.
2. MUST collect configured source URLs, saving raw responses under the task's agent-logs directory. The parser MUST require expected visible version, headers, mapped model labels, row shapes, valid numbers, and unique configurations. Offline generation MUST validate snapshot schema, configured source URL, SHA-256 format, timezone-aware retrieval timestamp, and required source fields before selection. Valid but different comparison groups or index versions MUST retain saved routes. Schema drift MUST fail before replacing evidence. Missing listed models MUST remain explicit gaps.
3. MUST freeze normalized evidence with retrieval date, URL, and raw SHA-256. Re-parsing the same bytes and metadata MUST reproduce it. Generation MUST work offline.
4. MUST generate both routing tables and decision records. MUST inspect changes before adopting evidence. New benchmark versions require matching source and floor-origin versions/groups after explicit floor review; MUST NOT compare them with old floors.
5. MUST run parser/selector tests and generate twice into separate directories. Outputs MUST match byte for byte. MUST check harness references point to generated tables.

## Selection

For metric j, a candidate qualifies when score_j >= floor_j - allowed_loss_j. Allowed loss defaults to zero. MUST use decimal arithmetic; MUST NOT combine unrelated scores into an invented index.

- Conserve: lowest comparable task cost among qualifiers.
- Balanced: incumbent unless a qualifying candidate has no score loss and lower cost, or improves a primary score at no greater cost. Among improvements: lowest cost, then lexicographically highest task scores.
- Burn: lexicographically highest task scores, then lowest comparable wall time, then cost.

Remaining ties MUST prefer the incumbent, then stable configuration ID. A missing tie-break field MUST disable that tie-break for the entire tied set, avoiding pairwise order dependence. A cost-based mode MUST retain its incumbent if its own comparable cost is unknown; candidates with unknown cost cannot prove savings.

No qualifier, missing incumbent, mismatched comparison group, or pinned task MUST retain the saved route with an explicit reason. A numerical tie is not proof of equivalence. Pooled benchmark costs/times MUST NOT become workspace completion estimates or credit conversions.

Mechanical, planning, review, and compound Fable routes remain pinned provisional policy until suitable evals exist. MUST NOT force every model into a route. Fable lead-only and concurrency rules remain in the Claude Code reference.

## Other evidence

The first adapter targets AA's agent comparison table. Other public sources or internal evals MAY supply the normalized format, but MUST name execution mode and comparison group. Direct API/other-harness evidence MUST NOT silently replace target-harness records. New adapters need fixtures and tests; no fuzzy matching or LLM extraction.

If replay finds a gap, MUST change this process first, then implementation and tests. Runtime agents MUST read saved tables, not scrape during delivery.

## Commands

From the skill directory (`LOG` is the task's agent-logs directory):

```sh
python3 -B scripts/model_guidance.py collect --policy data/policy.json --raw-dir "$LOG/sources" --output "$LOG/candidate.json"
python3 -B scripts/model_guidance.py generate --policy data/policy.json --snapshot "$LOG/candidate.json" --output-dir "$LOG/generated"
python3 -B -m unittest discover -s scripts -p 'test_*.py'
```

For offline replay, use `parse --policy data/policy.json --html <raw-file> --retrieved-at <saved-timestamp> --output <snapshot>`, then `generate` twice with that snapshot. Reviewed adoption MUST copy the candidate snapshot to `data/evidence.json` and its generated Markdown/JSON outputs to `references/` in the same commit. Incumbents and floors MUST NOT change automatically after generation: that would make the next replay a different policy. Raw capture hashes and generated decision diffs MUST identify evidence changes separately from policy changes.
