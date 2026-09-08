# Claude Code model routing

Updated 2026-09-08. Use only for Claude Code. Balanced SHOULD be the default. Names identify Theo's supplied versions, not moving aliases. P marks a provisional transfer or inherited seed.

| Task | Conserve | Balanced | Burn | Escalation |
|---|---|---|---|---|
| Mechanical lookup | Haiku 4.5 default P | Haiku 4.5 default P | Haiku 4.5 default P | Opus 5 high |
| Repository exploration | Opus 5 high | Opus 5 xhigh | Fable 5.1 max | Fable 5.1 max |
| Scoped implementation | Sonnet 5 default P | Opus 5 medium | Opus 5 medium | Fable lead P |
| Unclear bug / cross-module change | Opus 5 medium | Opus 5 high | Fable lead P | Fable lead P |
| Terminal execution with a known plan | Opus 5 high | Opus 5 high | Opus 5 xhigh | Fable lead P |
| Planning / architecture | Opus 5 high P | Opus 5 high P | Fable 5.1 max P | Fable 5.1 max P |
| Review / validation judgment | Opus 5 high P | Opus 5 xhigh P | Fable 5.1 max P | Fable 5.1 max P |

[Evidence A1](model-evidence.md) supports Opus effort choices: medium and max tie on DeepSWE, with medium cheaper and faster; xhigh improves Q&A and terminal scores over high. Fable leads collected Q&A and implementation scores, but the policy below limits implementation use. Sonnet and Haiku keep inherited roles; missing target-harness data does not prove equal quality or lower whole-task cost.

| Model | Intended role | Evidence gap |
|---|---|---|
| Fable 5.1 | Hard investigations, planning, lead | Published result uses provider fallback; not pure-model |
| Opus 5 | Implementation and judgment | No direct architecture/review eval |
| Sonnet 5 | Conserve scoped builder | Target-harness scores and task cost missing |
| Haiku 4.5 | Mechanical work | Vendor coding eval used another scaffold |

MUST pin the exact supplied version through the current Agent tool. A bare `fable`, `opus`, `sonnet`, or `haiku` MAY be used only when the session establishes its mapping to Theo's version. If exact mapping cannot be established, MUST leave the affected work pending and report the selector limit; MUST NOT invent a dated ID or substitute. `default` means omit the effort override and record the effective setting, or `unknown` if hidden. If requested effort is unsupported, MUST use the inherited setting, disclose the mismatch, and MUST NOT mutate a global setting. MUST NOT apply max-effort cost or scores to a default or mismatched route.

At most one Fable subagent MAY be active. A Fable lead is Fable 5.1 max running coordinate-delivery and delegating implementation to Opus 5 medium, or Opus 5 xhigh for terminal-heavy work. This compound route is unmeasured. It MUST use only one initial attempt and one correction across the compound route. The lead MUST diagnose the miss and revise the worker brief; the worker MUST NOT gain a separate retry allowance. If that correction fails, the lead MUST narrow or report the blocker. A Fable lead MUST NOT spawn another Fable lead. Direct Fable investigation, planning, and review are allowed; implementation MUST be delegated. Parallel builders MUST use Opus or cheaper tiers.

Corrections MUST reuse agents. If the harness cannot change the model for escalation, MAY hand notes and worktree to one replacement; MUST retain one owner per file. API errors MUST NOT trigger escalation. Cost and time forecasts remain uncalibrated; [model evidence](model-evidence.md) applies only to its measured benchmark context.
