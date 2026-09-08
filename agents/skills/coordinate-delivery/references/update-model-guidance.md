# Update model guidance

Same policy and snapshot MUST produce byte-identical tables and decisions. A live refresh MAY change results because evidence changed. Availability comes from Theo; MUST NOT recheck account access.

## Inputs

`data/policy.json` MUST hold exact model-name mappings, allowed configurations, task metrics, frozen quality floors, incumbents, and pinned provisional routes. Floors initially come from the previous table's measured incumbent scores, not invented tolerances. A policy edit is a visible judgment change.

`data/evidence.json` MUST hold parsed measurements and source provenance. Scores use percentage points; money uses USD; time uses seconds. Missing values MUST remain null. Comparisons MUST use one explicit comparison group (source, harness, benchmark/scoring/task-set/budget context). Unknown setup details MUST remain marked provisional, never asserted equal to another dataset.

## Refresh

1. MUST commit current guidance before edits. Add Theo's models to policy mappings; MUST NOT guess aliases or settings.
2. MUST collect configured source URLs, saving raw responses under the task's agent-logs directory. The parser MUST require expected headers, version, row shapes, valid numbers, and unique configurations. Schema drift MUST fail before replacing evidence. Missing listed models MUST remain explicit gaps.
3. MUST freeze normalized evidence with retrieval date, URL, and raw SHA-256. Re-parsing the same bytes and metadata MUST reproduce it. Generation MUST work offline.
4. MUST generate both routing tables and decision records. MUST inspect changes before adopting evidence. New benchmark versions require comparison-group and floor review; MUST NOT compare them with old floors.
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
