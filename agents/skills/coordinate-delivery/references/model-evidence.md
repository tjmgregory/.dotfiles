# Model evidence

Refresh: 2026-09-08. Availability supplied by Theo: Claude Code (Fable 5.1, Opus 5, Sonnet 5, Haiku 4.5); Codex (gpt-6-astra, gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna, gpt-5.5, gpt-5.3-codex-spark). All are considered below. Availability is not independently rechecked.

## Comparable harness runs

A1 and C1 use AA Coding Agent Index v1.4 components: DeepSWE (D), Terminal-Bench v2.1 (T), SWE-Atlas-QnA (Q). Scores below are rounded percentages. The evaluator reports 113/89/124 tasks respectively, three attempts each; pass@1 is averaged across attempts, not best-of-three. Per-row confidence intervals, run dates, harness versions, and full execution budgets were not exposed in the collected table. Comparisons are provisional point estimates. [Method](https://artificialanalysis.ai/methodology/coding-agents-benchmarking/).

Cost is AA's token-usage-based API cost at retrieval prices. Minutes measure active agent wall time, excluding setup and verifier/judge overhead. Both are pooled across the suite, not measured cost to eventual success or a specific task-family quote. These costs MUST NOT be converted to subscription credits.

A1: [Claude Code runs](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-grok-build), retrieved 2026-09-08.

| Model / effort | D | T | Q | USD/task | Minutes/task |
|---|---:|---:|---:|---:|---:|
| Fable 5.1 max, with fallback | 66 | 89 | 56 | 9.18 | 24.0 |
| Opus 5 xhigh | 60 | 89 | 55 | 8.17 | 23.7 |
| Opus 5 max | 63 | 89 | 49 | 8.94 | 24.2 |
| Opus 5 high | 61 | 87 | 49 | 3.92 | 14.0 |
| Opus 5 medium | 63 | 85 | 44 | 3.17 | 12.2 |

C1: [Codex runs](https://artificialanalysis.ai/agents/coding-agents/comparisons/codex-vs-grok-build), retrieved 2026-09-08.

| Model / effort | D | T | Q | USD/task | Minutes/task |
|---|---:|---:|---:|---:|---:|
| GPT-6 Astra max | 67 | 83 | 51 | 4.72 | 26.8 |
| GPT-5.6 Sol max | 69 | 83 | 43 | 5.00 | 10.2 |
| GPT-5.6 Sol high | 65 | 82 | 45 | 3.00 | 6.2 |
| GPT-5.6 Sol xhigh | 67 | 80 | 43 | 3.74 | 7.3 |
| GPT-5.6 Sol medium | 64 | 81 | 40 | 2.19 | 5.0 |
| GPT-5.6 Terra max | 67 | 78 | 36 | 1.93 | 8.2 |
| GPT-5.6 Luna max | 63 | 75 | 33 | 0.29 | 8.0 |
| GPT-5.6 Luna medium | 37 | 62 | 27 | 0.09 | 3.2 |
| GPT-5.5 xhigh | 64 | 83 | 36 | 4.75 | 10.2 |

## Gaps and supporting evidence

- Sonnet 5: no exact row in A1. [AA model page](https://artificialanalysis.ai/models/claude-sonnet-5) reports Intelligence Index 38 at max, USD 5.09 per index task. This is model-evaluation fallback evidence, not Claude Code task cost. [Vendor page](https://www.anthropic.com/research/claude-sonnet-5) supplies USD 2/10 per million input/output tokens. Conserve scoped-builder use is a prior-policy seed at default effort, not a max-effort benchmark conclusion.
- Haiku 4.5: no exact row in A1. [Anthropic](https://www.anthropic.com/news/claude-haiku-4-5) reports SWE-bench Verified 73.3%, 500 tasks, 50 trials, 128K thinking budget, bash/file-editor scaffold. Vendor-reported, different harness; task cost and duration unknown. USD 1/5 per million input/output tokens. Retain the mechanical seed; do not compare this score with D/T/Q.
- Spark: no exact row in C1. [OpenAI's release](https://openai.com/index/introducing-gpt-5-3-codex-spark/) describes targeted interactive coding, text-only 128K context, and over 1,000 tokens/second. Numeric benchmark chart scores were not extracted; comparable cost, duration, effort, and harness version are unknown. Tests must be requested explicitly. It remains an opt-in latency candidate, not a proven cheapest route.
- [TUA-Bench](https://github.com/facebookresearch/TUA-Bench): 120 terminal tasks; Codex GPT-5.5 high success rate 0.642 ± 0.007 versus xhigh 0.647 ± 0.007. Different metric and suite from C1, so it does not override C1 or prove equivalence.
- [Terminal-Bench 2.1](https://www.tbench.ai/news/terminal-bench-2-1) includes Claude Code and Codex pairs, but the collected current leaderboard redirect did not expose all supplied-model rows. Use the extracted AA component rows, not search snippets. The 2.1 release changed 28 tasks; 2.0 scores are not comparable.
- [AA's Astra report](https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra), dated September 3, compares a historical Intelligence Index version. Current model pages show v4.3. Do not merge those scores. Its aggregate coding improvement also hides Sol's higher implementation component in C1.

## API price context

USD per million tokens, standard short-context input/output. These are unit prices, not routing ranks or credit estimates. Budget calculations MUST check linked cache, context, and service-tier terms. Retrieved 2026-09-08.

| Model | Input / output | Source |
|---|---:|---|
| Fable 5.1 | 10 / 50 | [Anthropic](https://www.anthropic.com/claude/fable) |
| Opus 5 | 5 / 25 | [Anthropic](https://www.anthropic.com/news/claude-opus-5) |
| Sonnet 5 | 2 / 10 | Vendor page above |
| Haiku 4.5 | 1 / 5 | Vendor page above |
| GPT-6 Astra | 10 / 50 | [OpenAI](https://developers.openai.com/api/docs/models/gpt-6-astra) |
| GPT-5.6 Sol | 4 / 20 | [OpenAI](https://developers.openai.com/api/docs/models/gpt-5.6-sol) |
| GPT-5.6 Terra | 2 / 12 | [OpenAI](https://developers.openai.com/api/docs/models/gpt-5.6-terra) |
| GPT-5.6 Luna | 0.20 / 1.20 | [OpenAI](https://developers.openai.com/api/docs/models/gpt-5.6-luna) |
| GPT-5.5 | 5 / 30 | [OpenAI](https://developers.openai.com/api/docs/models/gpt-5.5) |
| GPT-5.3-Codex-Spark | Unknown | No price extracted |

## Refresh validation

The process was committed first, then used to build these tables. Collection and independent replay produced these process fixes:

- Hidden chart rows: use AA comparison pages; bound searches.
- Changing indices: record version and retrieval date; compare components.
- Ambiguous time: distinguish active wall time from decode estimates.
- Aggregate winners: route by task metric, with explicit tie-breaks.
- No incumbent: label initial seeds; do not invent quality floors.
- Fable recursion: one lead, no nested Fable, shared retry budget.
- Ambiguous “extract”: distinguish reading a constant from refactoring.
- Defaults/selectors: define omitted effort and unsupported-selector handling.
- Missing time/self-escalation: skip missing tie-breaks; cap each route's attempts.

No internal evals yet. Future records MUST identify source (public/internal), execution (Claude Code/Codex/direct API/other), model, effort, task-set version, scoring, attempts, uncertainty, cost basis, duration kind, and date. No internal runner is prescribed.

## Replay cases

Synthetic cases below validate routing logic, not model performance. An independent agent replayed both harnesses and all modes after the fixes and RFC rewrite; selections matched the rules. Current routes are first-run seeds where no incumbent existed; no statistically proven equivalence is claimed.

| Request | Expected route / refresh decision |
|---|---|
| Codex: save credits, implement a specified parser fix | Luna max; one correction then Sol max |
| Codex: balanced, same scoped fix | Terra max; D=67 at 1.93 versus Sol xhigh D=67 at 3.74 |
| Codex: burn, hard cross-module bug | Sol max; highest collected D, and tied highest T |
| Codex: burn, explain unknown repository behaviour | Astra max; highest collected Q |
| Claude: conserve, known small edit | Sonnet 5 default, provisional seed; Fable lead escalation |
| Claude: balanced, known small edit | Opus 5 medium; D tie with max, lower pooled cost/time |
| Claude: burn, execute a terminal plan | Opus 5 xhigh; T tie with Fable, lower cost/time |
| Either harness: burn, read and report a named constant's literal value without edits | Mechanical route unchanged |
| Claude: burn, refactor repeated literals into a named constant | Scoped implementation: Opus 5 medium |
| New candidate: same relevant scores, lower measured cost | Replace qualifying Conserve/Balanced incumbent; Burn also replaces if time ties or is missing, but retains a faster incumbent; label uncertainty |
| New candidate: only direct API results | Supporting evidence; retain harness incumbent provisionally |
| New candidate: better aggregate, worse primary task metric | Do not promote from the aggregate alone |
| New candidate: no usable measurements | Inventory entry with gap; retain incumbent |
| Escalation would exceed Theo's hard cap | Pause; mode does not authorise exceeding the cap |
| Strongest route fails its initial attempt and its one correction | Narrow/report blocker; do not spawn another same-route agent |
| A Fable lead's worker fails | One shared correction, then blocker; no nested lead or fresh retry budget |

Workspace task costs, rework rates, and elapsed-time forecasts remain uncalibrated. AA averages inform tradeoffs; they are not task estimates.
