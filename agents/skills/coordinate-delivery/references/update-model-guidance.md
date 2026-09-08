# Update model guidance

Run this process when Theo supplies new models, asks for a refresh, or reports a material harness or price change. Accept his model list as available. Do not verify account access. Update only the affected harness references.

## Collect

1. Preserve the current files in Git before changing recommendations. Record the refresh date and supplied model list in model-evidence.md.
2. Search each exact model name in the sources below. Open the source page; a search snippet is a lead, not a measurement. Record missing results explicitly. Never substitute another model or translate an alias without evidence.
3. Prefer relevant runs in the target harness. Use other-harness or direct API results when those are missing, and label the mismatch. Record source, execution mode, model, effort, harness version if reported, benchmark version, score, sample size, uncertainty, measured cost and duration. Unknown fields stay unknown.
4. Use Terminal-Bench and Artificial Analysis's Coding Agent Index components first: DeepSWE for implementation, SWE-Atlas-QnA for exploration, Terminal-Bench for terminal work. Use TUA-Bench as supporting evidence. Use SWE-bench common-harness results and Artificial Analysis model evaluations as fallbacks. Use official vendor documentation for prices and vendor-reported evals, clearly labelled. Internal evals may use the same record format; record execution as Claude Code, Codex, direct API, or other.

## Decide

5. Compare only the same benchmark version, scoring rule, task set, and compatible budgets. Never average unrelated scores or count an index and its components as independent evidence. Prefer same-harness evidence when relevance and comparison quality are otherwise equal. Missing results mean unknown, not poor.
6. Map evidence to exploration, scoped implementation, unclear bugs/cross-module work, planning/architecture, and review/validation. Terminal execution scores do not establish review or planning quality; label such transfers provisional.
7. Use Balanced by default. Conserve chooses the cheapest qualifying option; Balanced chooses the best supported cost to a verified result; Burn prioritises success and critical-path speed. Do not assume the largest model wins. Include retries and verification in cost when measured. Do not convert API prices into subscription credits.
8. A model qualifies when relevant evidence meets the task's quality floor. If Theo has supplied a tolerated loss, apply it in that benchmark's units. Otherwise require no observed score loss to call a cheaper model comparable. Small differences and overlapping intervals do not prove equivalence. With conflicting or absent evidence, retain the current choice as provisional; for a new harness use an explicitly labelled seed choice, not a claimed benchmark winner.
9. Record exact model and effort in each route. Use a harness default when effort is not controlled, recording that fact. Keep all supplied models in the inventory even when no routing cell selects them. Explain exclusions briefly.

## Validate and feed back

10. Check every supplied model has an evidence disposition and every routing choice has a source or a provisional reason. Check links, settings, mode rules, and escalation paths. Do not invent cost or time ranges: report uncalibrated until comparable task runs support them.
11. Replay realistic requests for each mode and each harness, including missing evidence, a cheaper comparable candidate, conflicting results, and a direct-API-only result. Record the selected route and why. A second reader should reach the same result from the same records.
12. When replay exposes ambiguity, amend this process first, then regenerate the affected guidance and replay it. Record the ambiguity and resolution in the refresh notes within model-evidence.md. Keep runtime tables short; retain only evidence needed to explain current choices.

Sources: [Terminal-Bench](https://www.tbench.ai/), [Artificial Analysis agents](https://artificialanalysis.ai/agents/coding-agents), [AA methodology](https://artificialanalysis.ai/methodology/coding-agents-benchmarking/), [TUA-Bench](https://github.com/facebookresearch/TUA-Bench), [SWE-bench](https://www.swebench.com/), [AA models](https://artificialanalysis.ai/).
