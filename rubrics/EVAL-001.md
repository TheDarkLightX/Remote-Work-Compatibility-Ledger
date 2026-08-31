# Rubric — EVAL-001 LLM Regression Sentinel

Total: **100 points**

A portfolio-ready pass is **80+** with no critical failure.

## 1. Evaluation design — 20

- 0–5: objective is vague; cases do not map to stated quality dimensions.
- 6–10: basic dimensions and cases exist but coverage is narrow or redundant.
- 11–15: clear dimensions, representative cases, adversarial coverage, and explicit success criteria.
- 16–20: strong experimental design, good boundary cases, careful claim scope, and evidence that the suite can distinguish meaningful failure classes.

## 2. Harness correctness and reproducibility — 20

- 0–5: fragile/manual workflow; results cannot be reproduced reliably.
- 6–10: runnable but weak validation or nondeterministic behavior.
- 11–15: clean CLI, deterministic outputs, schema checks, useful tests.
- 16–20: fail-closed behavior, strong self-tests, clear provenance, and clean-clone reproducibility.

## 3. Metrics and regression analysis — 15

- 0–4: only an unexamined aggregate score.
- 5–8: useful per-dimension metrics but weak interpretation.
- 9–12: paired comparison, appropriate denominators, useful uncertainty or sensitivity analysis.
- 13–15: metrics are well justified, limitations are explicit, and conclusions do not exceed what the sample supports.

## 4. Failure taxonomy and diagnosis — 15

- 0–4: failures are listed without meaningful categories.
- 5–8: sensible categories and examples.
- 9–12: taxonomy reveals actionable patterns and separates model/data/harness issues.
- 13–15: strong root-cause reasoning, boundary cases, and evidence that taxonomy changes what the team should do next.

## 5. Human verification / AI supervision — 15

- 0–4: accepts automated judgements without checking them.
- 5–8: manual review exists but is shallow.
- 9–12: disagreement analysis identifies false positives/negatives and corrects them.
- 13–15: demonstrates calibrated distrust of automation and explains when human judgment remains necessary.

## 6. Communication — 10

- 0–3: reviewer must reverse-engineer the conclusion.
- 4–6: understandable summary but weak prioritization.
- 7–8: concise decision memo with representative evidence.
- 9–10: a technical and nontechnical reviewer can both understand the decision, evidence, limitations, and next action quickly.

## 7. Provenance and AI-use disclosure — 5

- 0: missing or materially misleading.
- 1–2: partial disclosure.
- 3–4: clear tools/models/commands and authorship boundaries.
- 5: unusually clear provenance, including limitations of what can and cannot be proven from repository history.

# Critical failures

Any of the following blocks a portfolio-ready pass regardless of point total:

- materially falsified or misleading provenance;
- synthetic outputs represented as real measurements of a named production model;
- result cannot be reproduced from the committed artifacts and instructions;
- evaluation silently drops malformed or missing records in a way that changes the result;
- IDs can be misaligned without detection;
- only an LLM judge is used, with no deterministic check or calibration against human-reviewed labels;
- final recommendation contradicts the reported evidence without explaining why;
- generated gold labels are accepted without the required human review.

# Suggested badge language

Use only after the corresponding evidence exists:

- **Completed** — required artifacts exist.
- **Replayed** — clean-clone commands reproduced the committed result.
- **Portfolio-ready** — score >=80 and no critical failure.
- **Externally verified** — an identified third party independently evaluated or proctored the work.

Do not use `verified` as a synonym for `completed`.
