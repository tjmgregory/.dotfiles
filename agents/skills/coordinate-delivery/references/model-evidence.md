# Model evidence

The [score table](model-scores.md), [Claude routes](claude-code-routes.md), and [Codex routes](codex-routes.md) are generated. They MUST NOT be edited by hand.

Reproduction inputs: [policy](../data/policy.json), [snapshot](../data/evidence.json). [Decisions](decisions.json) record selections and rejection reasons. The snapshot records source URL, retrieval date, and raw-response hash. Raw captures live in the refresh task's agent-logs directory.

## Meaning

AA Coding Agent Index v1.4 supplies DeepSWE, Terminal-Bench v2.1, and SWE-Atlas-QnA. Costs are API token costs pooled across that suite. Time is active agent wall time, excluding setup and verification. [Method](https://artificialanalysis.ai/methodology/coding-agents-benchmarking/).

Run dates, individual budgets, harness versions, and uncertainty are not published in the scraped table. Choices therefore remain provisional point-estimate comparisons. Frozen floors preserve the preceding policy's measured standard; they are not statistical guarantees. Table generations MUST NOT mix benchmark versions or assume independent retries to estimate eventual success.

Mechanical, planning, review, and compound Fable choices are pinned policy. New measurements alone MUST NOT rewrite these judgments. Unknown evidence remains unknown; every supplied model stays in the inventory.

## Supporting sources

These are context, not inputs to automatic selection:

- [Sonnet 5](https://artificialanalysis.ai/models/claude-sonnet-5): model-level evaluation, not a substitute for Claude Code measurements.
- [Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5): vendor coding results from another scaffold.
- [Spark](https://openai.com/index/introducing-gpt-5-3-codex-spark/): interactive coding; tests must be requested explicitly.
- [TUA-Bench](https://github.com/facebookresearch/TUA-Bench): different tasks and scoring; needs its own adapter/comparison group.

Internal evals MAY use the normalized format with explicit source, execution, metrics, costs, duration, and comparison group. No internal runner is prescribed. Workspace cost, credits, rework, and duration forecasts remain uncalibrated.

## Validation

The first scripted refresh parsed 28 configurations, with gaps for Sonnet 5, Haiku 4.5, and Spark. Re-parsing the saved raw response reproduced the normalized snapshot byte for byte. Two offline generations produced identical route tables, score tables, and decisions.

Using all source variants changed two cells from the manual table: Conserve Claude exploration selects Opus 5 none; Burn Codex terminal execution selects GPT-5.5 xhigh. Both follow the frozen floors and tie-breaks. Existing judgment-only routes remain pinned.
