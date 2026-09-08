# Claude Code model routing

Updated 2026-09-08. Use only for Claude Code. Balanced SHOULD be the default. Names identify Theo's supplied versions, not moving aliases.

Before choosing agents, MUST read the [generated routing table](claude-code-routes.md). Its cells come from the frozen [policy](../data/policy.json) and [snapshot](../data/evidence.json); MUST NOT edit them by hand. [Evidence notes](model-evidence.md) explain gaps and limits. P marks pinned or otherwise provisional choices.

Model names in the table are the exact versions supplied by Theo. A missing eval does not make a model unavailable. The updater MUST retain all supplied models in the inventory, including those selected by no route.

MUST pin the exact supplied version through the current Agent tool. A bare `fable`, `opus`, `sonnet`, or `haiku` MAY be used only when the session establishes its mapping to Theo's version. If exact mapping cannot be established, MUST leave the affected work pending and report the selector limit; MUST NOT invent a dated ID or substitute. `default` means omit the effort override and record the effective setting, or `unknown` if hidden. If requested effort is unsupported, MUST use the inherited setting, disclose the mismatch, and MUST NOT mutate a global setting. MUST NOT apply max-effort cost or scores to a default or mismatched route.

At most one Fable subagent MAY be active. A Fable lead is Fable 5.1 max running coordinate-delivery and delegating implementation to Opus 5 medium, or Opus 5 xhigh for terminal-heavy work. This compound route is unmeasured. It MUST use only one initial attempt and one correction across the compound route. The lead MUST diagnose the miss and revise the worker brief; the worker MUST NOT gain a separate retry allowance. If that correction fails, the lead MUST narrow or report the blocker. A Fable lead MUST NOT spawn another Fable lead. Direct Fable investigation, planning, and review are allowed; implementation MUST be delegated. Parallel builders MUST use Opus or cheaper tiers.

Corrections MUST reuse agents. If the harness cannot change the model for escalation, MAY hand notes and worktree to one replacement; MUST retain one owner per file. API errors MUST NOT trigger escalation. Cost and time forecasts remain uncalibrated; [model evidence](model-evidence.md) applies only to its measured benchmark context.
