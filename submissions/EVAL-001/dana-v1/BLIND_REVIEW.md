# EVAL-001: Low-anchoring manual review protocol

**Status: review aid only; no human judgments recorded.**

Review these ten cases in order: `cu-006`, `cu-007`, `so-001`, `so-002`, `fg-002`, `if-001`, `rc-001`, `ta-001`, `cu-001`, `cu-002`.

For each case, open `evals.jsonl` and the two matching rows in `responses.jsonl` first. Without checking the draft labels or grader results, decide whether each response satisfies the stated criterion, or whether the policy is too ambiguous to permit a binary label. Record the specific semantic reason, then compare with `gold.jsonl`, `results/report.md`, and the automated grader.

Put all actual judgments in `human-review.md`. Preserve `PENDING HUMAN REVIEW` until the candidate personally performs each step. This checklist does not constitute a completed review.

Once these ten cases are reviewed, proceed to the other 27 gold records. Then finish the unaided oral defense, the bounded decision memo and the clean-checkout replay before assigning a final score.

**Why this protocol:** reading automated verdicts before deciding independently can anchor reviewers and conceal systematic lexical-grader errors. Separate an independent semantic first pass from evaluator comparison.

## Ready-to-use review aids (added 2026-10-26)

- [Ten-case model-blind packet](BLIND_REVIEW_PACKET.md) — complete first-pass semantic judgments on paired, anonymized responses without provisional labels or grader verdicts.
- [Response identity key](BLIND_REVIEW_KEY.md) — **open only after** saving the independent first pass; then map the responses to `model_A` and `model_B` and compare results.

These aids reduce lookup and anchoring overhead. Both are machine-prepared and do **not** constitute human review. If underlying synthetic fixtures change, regenerate the packet and key with updated bindings before use.
