# Update model guidance

Use this process when Theo supplies models, requests a refresh, or reports a material harness or price change. Treat his list as available; MUST NOT verify access. Update only affected harness references.

## Collect

1. Before edits, MUST preserve current files in Git. Record refresh date and supplied models in `model-evidence.md`.
2. MUST search each exact model name in the priority sources below and open the source page. Search snippets are leads, not measurements. MUST record missing results. MUST NOT substitute models or translate aliases without evidence.
3. SHOULD prefer target-harness runs. Other-harness or direct-API results MAY fill gaps only when labelled as mismatches. Each record MUST include source, execution mode, model, effort, harness and benchmark versions, score, sample size, uncertainty, measured cost and duration when reported; unknown fields MUST remain unknown.
4. SHOULD prefer Terminal-Bench and Artificial Analysis Coding Agent Index components: DeepSWE for implementation, SWE-Atlas-QnA for exploration, Terminal-Bench for terminal work. TUA-Bench MAY support them. SWE-bench common-harness results, AA model evaluations, and vendor evals are fallbacks. Vendor prices and evals MUST be labelled. Internal evals MUST use the same record shape and name execution as Claude Code, Codex, direct API, or other.

For each model, inspect the two priority sources, one relevant fallback, and its official model or release page. Shared pages MAY cover several models. SHOULD use AA agent comparison pages before dated articles when charts hide variants. If values remain hidden, try linked data or one evaluator article, then record the gap. Search another source only to resolve a route-changing conflict.

MUST record evaluation and retrieval dates separately. MUST preserve historical index versions. Duration MUST say measured wall time, agent wall time, or estimated decode time. Cost MUST say observed usage repriced at a date, vendor estimate, or unknown. MUST keep single-agent, multi-agent, and fallback-model results distinct.

## Decide

5. MUST compare only matching benchmark version, scoring, task set, and compatible budgets. MUST NOT average unrelated scores or count an index and its components independently. SHOULD prefer relevant same-harness evidence. Missing results mean unknown, not poor.
6. Map SWE-Atlas to exploration, DeepSWE to scoped implementation, DeepSWE then Terminal-Bench to unclear bugs and cross-module work, and Terminal-Bench to known-plan terminal work. Planning and review transfers MUST remain provisional until direct evidence exists.
7. Balanced SHOULD be the default. Conserve MUST choose the cheapest qualifying option. Balanced MUST choose the best supported cost to a verified result. Burn MUST prioritise success, then critical-path speed. MUST NOT assume the largest model wins, convert API prices to credits, or omit measured retries and verification from cost.
8. A candidate qualifies only at the task quality floor. Apply Theo's tolerated loss in that benchmark's units; otherwise, no observed loss is required for cheaper-model comparability. Small differences or overlapping intervals MUST NOT be called equivalent. Conflicting or absent evidence MUST retain the incumbent provisionally. A new harness MUST use a labelled seed, not a claimed winner.
9. Routes MUST state exact model and effort. When effort is uncontrolled, `default` means omit the override and record the effective setting, or `unknown` when the harness does not expose it. MUST keep every supplied model in inventory and briefly explain exclusions.

For deterministic refreshes, each route's incumbent and cited primary metrics define its floor unless Theo sets another. Candidates MUST meet each primary metric's floor, including Theo's allowed loss. Conserve minimises comparable task cost among qualifiers. Balanced retains the incumbent unless a candidate has no observed loss and lower task cost, or a higher score at no greater cost. Burn maximises relevant score; ties use measured wall time, then task cost, then incumbent. If a tie-break field is missing, MUST skip it and continue to the next. Uncertainty makes the result provisional. Token-price-only cost choices MUST be provisional. First runs MUST use explicit evidence-backed or inherited seeds without invented floors. No model has a route quota.

At runtime, MUST use the saved table. Overlaps use the more demanding row. Unknown cause, cross-module effects, and consequential or hard-to-reverse changes are complex. A mechanical lookup is read-only, named, and objectively checkable. Any edit is scoped implementation or complex work. A scoped implementation has a known approach and clear acceptance checks. A hard spending cap MUST block escalation beyond it.

Each route allows one initial attempt and one correction by the same agent. After the correction, MUST escalate. A compound route gets the same two total attempts, not a new retry allowance per worker. If escalation is the same strongest route, MUST stop retrying and narrow the problem or report the blocker.

## Validate and feed back

10. MUST verify every supplied model has an evidence disposition and every route has evidence or a provisional reason. MUST check links, settings, modes, escalation, and whether the runtime tool can express each selector. This tool check MUST NOT recheck user-supplied access. MUST NOT invent cost or time ranges.
11. MUST replay each mode and harness, including missing evidence, a cheaper equal candidate, conflicting results, direct-API-only results, strongest-route failure, and compound-route correction. Record route and reason so another reader can reproduce it.
12. If replay exposes ambiguity, MUST amend this process first, regenerate guidance, and replay. Record the ambiguity and fix in `model-evidence.md`. Runtime tables SHOULD retain only evidence needed for current choices.

Sources: [Terminal-Bench](https://www.tbench.ai/), [Artificial Analysis agents](https://artificialanalysis.ai/agents/coding-agents), [AA methodology](https://artificialanalysis.ai/methodology/coding-agents-benchmarking/), [TUA-Bench](https://github.com/facebookresearch/TUA-Bench), [SWE-bench](https://www.swebench.com/), [AA models](https://artificialanalysis.ai/).
