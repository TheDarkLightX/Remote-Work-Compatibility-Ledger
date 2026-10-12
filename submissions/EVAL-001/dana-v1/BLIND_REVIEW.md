# EVAL-001: Low-anchoring manual review protocol

**Status: review aid only; no human judgments recorded.**

Review these ten cases in order: `cu-006`, `cu-007`, `so-001`, `so-002`, `fg-002`, `if-001`, `rc-001`, `ta-001`, `cu-001`, `cu-002`.

For each case, open `evals.jsonl` and the two matching rows in `responses.jsonl` first. Without checking the draft labels or grader results, decide whether each response satisfies the stated criterion, or whether the policy is too ambiguous to permit a binary label. Record the specific semantic reason, then compare with `gold.jsonl`, `results/report.md`, and the automated grader.

Put all actual judgments in `human-review.md`. Preserve `PENDING HUMAN REVIEW` until the candidate personally performs each step. This checklist does not constitute a completed review.

Once these ten cases are reviewed, proceed to the other 27 gold records. Then finish the unaided oral defense, the bounded decision memo and the clean-checkout replay before assigning a final score.

**Why this protocol:** reading automated verdicts before deciding independently can anchor reviewers and conceal systematic lexical-grader errors. Separate an independent semantic first pass from evaluator comparison.
