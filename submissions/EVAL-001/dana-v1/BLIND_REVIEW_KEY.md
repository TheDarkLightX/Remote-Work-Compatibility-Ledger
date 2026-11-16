# EVAL-001 — Response identity key for ten-case packet

**STOP: do not read before completing the independent first pass** in [BLIND_REVIEW_PACKET.md](BLIND_REVIEW_PACKET.md). Revealing model identities early would weaken the intended low-anchoring review. This key reveals identity only; it contains **no** provisional labels or machine grades.

Source: PR #2 head `455c7be5bdc067049587c01b3c2e2c9c75a776b7`. Verify the source fixtures remain unchanged before trusting this mapping. After independent judgments, consult this table, then `gold.jsonl` and `results/report.md` to analyze disagreements. All model outputs are synthetic.

| Case | Response 1 | Response 2 |
| --- | --- | --- |
| `cu-006` | `model_B` | `model_A` |
| `cu-007` | `model_A` | `model_B` |
| `so-001` | `model_B` | `model_A` |
| `so-002` | `model_A` | `model_B` |
| `fg-002` | `model_B` | `model_A` |
| `if-001` | `model_A` | `model_B` |
| `rc-001` | `model_B` | `model_A` |
| `ta-001` | `model_A` | `model_B` |
| `cu-001` | `model_B` | `model_A` |
| `cu-002` | `model_A` | `model_B` |
