# Codex model routing

Updated 2026-09-08. Use only for Codex. Balanced SHOULD be the default. Names expand to the selectors below. Effort is explicit. P marks a provisional task transfer or seed, not a measured win.

| Task | Conserve | Balanced | Burn | Escalation |
|---|---|---|---|---|
| Mechanical lookup | Luna medium P | Luna medium P | Luna medium P | Sol high |
| Repository exploration | Luna max | Sol high | Astra max | Astra max |
| Scoped implementation | Luna max | Terra max | Sol max | Sol max |
| Unclear bug / cross-module change | Terra max | Sol high | Sol max | Sol max |
| Terminal execution with a known plan | Luna max | Sol high | Sol max | Sol max |
| Planning / architecture | Sol medium P | Sol high P | Astra max P | Astra max P |
| Review / validation judgment | Terra max P | Sol high P | Astra max P | Astra max P |

These are initial routes, not claims that Conserve matches Burn. [Evidence C1](model-evidence.md) supports task tradeoffs. Terra max matches Sol xhigh's DeepSWE score at lower measured task cost; Sol max leads implementation; Astra max leads repository Q&A but is slower than Sol. Mechanical, planning, and review routes remain provisional because no direct eval was collected.

| Short name | Exact selector | Current use |
|---|---|---|
| Astra | `gpt-6-astra` | Exploration and judgment escalation |
| Sol | `gpt-5.6-sol` | Complex work and high-quality implementation |
| Terra | `gpt-5.6-terra` | Scoped implementation value at max |
| Luna | `gpt-5.6-luna` | Low-cost work with clear verification |
| 5.5 | `gpt-5.5` | Retained; Sol high beats its xhigh implementation/Q&A at lower cost, but not terminal |
| Spark | `gpt-5.3-codex-spark` | Opt-in for latency-sensitive, small text-only tasks; provisional, default effort, tests required |

All six were supplied by Theo. Spark lacks comparable cost and score, so MUST NOT displace a default route. If its runtime selector is absent, MUST report the tool limit and MUST NOT silently substitute.

When spawning, MUST pass `model` and MUST pass `reasoning_effort` for explicit settings. `default` means omit the effort override and record the effective setting, or `unknown` if hidden. If full-history forks reject overrides, MUST use `fork_turns: "none"` or a supported bounded fork and brief the needed context. Corrections MUST reuse the agent. If its model cannot change for escalation, MAY hand notes and worktree to one replacement; MUST retain one owner per file.

Burn MUST use saved settings, not automatic `ultra` or hidden multi-agent compute. This evidence does not validate a four-agent setup. Concurrency MUST stay within runtime and repository rules. API prices and benchmark durations are context in [model evidence](model-evidence.md); workspace forecasts remain uncalibrated.
