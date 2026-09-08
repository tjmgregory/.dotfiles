# claude-code routes

Source: [Artificial Analysis](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex), Coding Agent Index v1.4. Public benchmark results are provisional routing evidence, not completion estimates.

| Task | Conserve | Balanced | Burn | Escalation |
|---|---|---|---|---|
| Mechanical lookup | P Haiku 4.5 default | P Haiku 4.5 default | P Haiku 4.5 default | Opus 5 high |
| Repository exploration | Opus 5 (none) | P Opus 5 (xhigh) | Fable 5.1 (max) (with fallback) | Fable 5.1 max |
| Scoped implementation | P Sonnet 5 default | P Opus 5 (medium) | Opus 5 (medium) | Fable lead P |
| Unclear bug / cross-module change | Opus 5 (medium) | P Opus 5 (high) | P Fable lead | Fable lead P |
| Terminal execution with a known plan | Opus 5 (high) | P Opus 5 (high) | Opus 5 (xhigh) | Fable lead P |
| Planning / architecture | P Opus 5 high | P Opus 5 high | P Fable 5.1 max | Fable 5.1 max P |
| Review / validation judgment | P Opus 5 high | P Opus 5 xhigh | P Fable 5.1 max | Fable 5.1 max P |
