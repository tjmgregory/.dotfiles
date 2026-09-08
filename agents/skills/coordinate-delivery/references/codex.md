# Codex model routing

Updated 2026-09-08. Use only for Codex. Balanced SHOULD be the default. Names expand to the selectors below. Effort is explicit.

Before choosing agents, MUST read the [generated routing table](codex-routes.md). Its cells come from the frozen [policy](../data/policy.json) and [snapshot](../data/evidence.json); MUST NOT edit them by hand. [Evidence notes](model-evidence.md) explain gaps and limits. P marks pinned or otherwise provisional choices.

| Short name | Exact selector |
|---|---|
| Astra | `gpt-6-astra` |
| Sol | `gpt-5.6-sol` |
| Terra | `gpt-5.6-terra` |
| Luna | `gpt-5.6-luna` |
| 5.5 | `gpt-5.5` |
| Spark | `gpt-5.3-codex-spark` |

All six were supplied by Theo. Spark remains a pinned opt-in for small, text-only, latency-sensitive tasks until policy review admits comparable evidence. Its brief MUST request tests. If its runtime selector is absent, MUST report the tool limit and MUST NOT silently substitute.

When spawning, MUST pass `model` and MUST pass `reasoning_effort` for explicit settings. `default` means omit the effort override and record the effective setting, or `unknown` if hidden. If full-history forks reject overrides, MUST use `fork_turns: "none"` or a supported bounded fork and brief the needed context. Corrections MUST reuse the agent. If its model cannot change for escalation, MAY hand notes and worktree to one replacement; MUST retain one owner per file.

Burn MUST use saved settings, not automatic `ultra` or hidden multi-agent compute. This evidence does not validate a four-agent setup. Concurrency MUST stay within runtime and repository rules. API prices and benchmark durations are context in [model evidence](model-evidence.md); workspace forecasts remain uncalibrated.
