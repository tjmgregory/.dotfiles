# Model scores

Source: [Artificial Analysis](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex), Coding Agent Index v1.4. Public benchmark results are provisional routing evidence, not completion estimates.

| Harness | Model | Effort | DeepSWE | Terminal | QnA | Cost | Time |
|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | Fable 5.1 | max + fallback | 66 | 89 | 56 | $9.18 | 1440s |
| claude-code | Opus 5 | high | 61 | 87 | 49 | $3.92 | 840s |
| claude-code | Opus 5 | low | 57 | 82 | 39 | $2.3 | 600s |
| claude-code | Opus 5 | max | 63 | 89 | 49 | $8.94 | 1452s |
| claude-code | Opus 5 | medium | 63 | 85 | 44 | $3.17 | 732s |
| claude-code | Opus 5 | none | 44 | 82 | 52 | $3.53 | 708s |
| claude-code | Opus 5 | xhigh | 60 | 89 | 55 | $8.17 | 1422s |
| codex | 5.5 | medium | 57 | 79 | 31 | $2.65 | 384s |
| codex | 5.5 | xhigh | 64 | 83 | 36 | $4.75 | 612s |
| codex | Luna | high | 53 | 73 | 29 | $0.18 | 342s |
| codex | Luna | low | 10 | 50 | 15 | $0.04 | 102s |
| codex | Luna | max | 63 | 75 | 33 | $0.29 | 480s |
| codex | Luna | medium | 37 | 62 | 27 | $0.09 | 192s |
| codex | Luna | none | 6 | 33 | 17 | $0.07 | 132s |
| codex | Luna | xhigh | 57 | 71 | 31 | $0.24 | 414s |
| codex | Sol | high | 65 | 82 | 45 | $3 | 372s |
| codex | Sol | low | 53 | 78 | 34 | $1.29 | 210s |
| codex | Sol | max | 69 | 83 | 43 | $5 | 612s |
| codex | Sol | medium | 64 | 81 | 40 | $2.19 | 300s |
| codex | Sol | none | 35 | 60 | 34 | $1.09 | 198s |
| codex | Sol | xhigh | 67 | 80 | 43 | $3.74 | 438s |
| codex | Terra | high | 60 | 72 | 31 | $1.14 | 360s |
| codex | Terra | low | 30 | 63 | 23 | $0.39 | 156s |
| codex | Terra | max | 67 | 78 | 36 | $1.93 | 492s |
| codex | Terra | medium | 46 | 70 | 29 | $0.67 | 240s |
| codex | Terra | none | 13 | 37 | 19 | $0.29 | 90s |
| codex | Terra | xhigh | 58 | 77 | 33 | $1.36 | 402s |
| codex | Astra | max | 67 | 83 | 51 | $4.72 | 1608s |

Gaps:
- claude-code:haiku-4.5: mapped model absent from source table
- claude-code:sonnet-5: mapped model absent from source table
- codex:gpt-5.3-codex-spark: mapped model absent from source table
