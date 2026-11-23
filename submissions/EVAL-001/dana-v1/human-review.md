# EVAL-001 Human Review — Dana Edwards

> **Status: PENDING HUMAN REVIEW.** This file is a review worksheet prepared by
> OpenAI Codex. None of the blank fields or unchecked boxes below records a
> review by Dana Edwards. Automated findings are context only.

## Review protocol

For each selected case, inspect the prompt, success criterion, grader
configuration, both responses, AI-drafted provisional gold judgments, and the
measured case result. Do not approve a label merely because the code and draft
gold agree. Record whether the rule measures the intended behavior, whether the
outputs deserve the assigned labels, and whether the failure taxonomy is
useful.

At least 10 cases from the concrete queue below must receive substantive review.
The queue intentionally includes regressions, improvements, a grader/gold
mismatch, and a manual-only boundary.

## Priority manual-review queue

### 1. `cu-006` — lexical grader may be misleading

Machine context: both outputs measured `pass`. The AI-drafted provisional gold
instead labels `model_B` a failure because its phrase “It is false that there
is insufficient evidence” negates the required phrase and then asserts definite
causation. This is a machine-generated audit candidate; Dana must independently
decide whether it is genuinely misleading.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Does the grader measure the intended behavior?
- Rationale:
- Gold/grader correction, if any:
- Is automation misleading or insufficient here? Why?

### 2. `cu-007` — manual-only policy boundary

Machine context: both outputs are `needs_human_review` and excluded from scoring.
The policy requires notice for a “material” UI change but never defines
`material`; `model_A` says no notice is required, while `model_B` says the
excerpt is insufficient and compliance interpretation is required.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Is a defensible gold label possible from the supplied policy alone?
- Rationale:
- Gold/grader correction, if any:
- Is automation misleading or insufficient here? Why?

### 3. `so-001` — planted JSON regression

Machine context: `model_A` returns `{"ok":true}` and passes; `model_B` returns
`{'ok': true}` and fails standards-compliant JSON parsing. Measured transition:
regression; fixture failure type: `invalid_json`; case-level critical flag: true.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Does the grader measure the intended behavior?
- Rationale:
- Gold/grader correction, if any:
- Product severity assessment:

### 4. `so-002` — planted JSON type regression

Machine context: `model_A` supplies integer `count: 2`; `model_B` supplies string
`count: "2"`. Measured transition: regression; fixture failure type:
`wrong_json_type`; case-level critical flag: true.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Does the grader measure the intended behavior?
- Rationale:
- Gold/grader correction, if any:
- Product severity assessment:

### 5. `fg-002` — source-grounding regression

Machine context: the synthetic source says 2012. `model_A` returns `2012` and
passes; `model_B` returns `2013` and fails exact match. Measured transition:
regression; fixture failure type: `unsupported_factual_claim`.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Does the grader measure the intended behavior?
- Rationale:
- Gold/grader correction, if any:
- Product severity assessment:

### 6. `if-001` — exact-format regression

Machine context: the instruction requires exactly `ACK`. `model_A` returns
`ACK`; `model_B` returns `ACK.`. Measured transition: regression; fixture
failure type: `exact_format_violation`.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Does the grader measure the intended behavior?
- Rationale:
- Gold/grader correction, if any:
- Product severity assessment:

### 7. `rc-001` — arithmetic regression

Machine context: the expected answer to 7 × 6 is 42. `model_A` returns `42`;
`model_B` returns `41`. Measured transition: regression; fixture failure type:
`arithmetic_error`.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Does the grader measure the intended behavior?
- Rationale:
- Gold/grader correction, if any:
- Product severity assessment:

### 8. `ta-001` — tool-argument regression

Machine context: the exact call requires `days: 3`. `model_A` supplies 3;
`model_B` supplies 5. Measured transition: regression; fixture failure type:
`wrong_argument_value`.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Does the grader measure the intended behavior?
- Rationale:
- Gold/grader correction, if any:
- Product severity assessment:

### 9. `cu-001` — calibrated-uncertainty improvement

Machine context: observational evidence cannot establish causation. `model_A`
uses definite causal language; `model_B` states there is insufficient evidence.
Measured transition: improvement; fixture failure type for the failed response:
`overconfidence`.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Does the grader measure the intended behavior?
- Rationale:
- Gold/grader correction, if any:
- Product value assessment:

### 10. `cu-002` — uncertainty-token improvement

Machine context: one coin toss cannot establish bias. `model_A` returns `fair`;
`model_B` returns `cannot determine`. Measured transition: improvement; fixture
failure type for the failed response: `uncertainty_not_expressed`.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Does the grader measure the intended behavior?
- Rationale:
- Gold/grader correction, if any:
- Product value assessment:

### 11. `fg-003` — source-conflict improvement

Machine context: sources give 12,000 and 14,000. `model_A` reports only 12,000;
`model_B` explicitly reports the conflict and both values. Measured transition:
improvement; fixture failure type for the failed response:
`source_conflict_ignored`.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Does the grader measure the intended behavior?
- Rationale:
- Gold/grader correction, if any:
- Product value assessment:

### 12. `if-002` — format improvement

Machine context: the required identifier is `ABC-0420`. `model_A` returns
lowercase `abc-0420`; `model_B` returns the required uppercase form. Measured
transition: improvement; fixture failure type for the failed response:
`regex_format_violation`.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Does the grader measure the intended behavior?
- Rationale:
- Gold/grader correction, if any:
- Product value assessment:

### 13. `rc-002` — numeric improvement and tolerance check

Machine context: the mean of 2 and 3 is 2.5 with absolute tolerance 0.001.
`model_A` returns `2.4`; `model_B` returns `2.5`. Measured transition:
improvement; fixture failure type for the failed response: `arithmetic_error`.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Is the declared tolerance justified?
- Rationale:
- Gold/grader correction, if any:
- Product value assessment:

### 14. `ta-002` — required tool-argument improvement

Machine context: the search call requires `tool`, `query`, and `limit` with
specified values. `model_A` omits `query`; `model_B` supplies all required
arguments. Measured transition: improvement; fixture failure type for the
failed response: `missing_required_argument`.

- [ ] Reviewed personally
- Dana outcome for `model_A`:
- Dana outcome for `model_B`:
- Does the grader measure the intended behavior?
- Rationale:
- Gold/grader correction, if any:
- Product value assessment:

## Every-gold-record review checklist

The detailed queue above does not replace review of all 37 AI-drafted gold
records. Check an item only after reviewing both provisional model judgments,
their rationales, and the corresponding expected condition.

### Factuality / grounding

- [ ] `fg-001`
- [ ] `fg-002`
- [ ] `fg-003`
- [ ] `fg-004`
- [ ] `fg-005`
- [ ] `fg-006`

### Instruction following

- [ ] `if-001`
- [ ] `if-002`
- [ ] `if-003`
- [ ] `if-004`
- [ ] `if-005`
- [ ] `if-006`

### Structured output

- [ ] `so-001`
- [ ] `so-002`
- [ ] `so-003`
- [ ] `so-004`
- [ ] `so-005`
- [ ] `so-006`

### Calibrated uncertainty

- [ ] `cu-001`
- [ ] `cu-002`
- [ ] `cu-003`
- [ ] `cu-004`
- [ ] `cu-005`
- [ ] `cu-006`
- [ ] `cu-007`

### Reasoning / consistency

- [ ] `rc-001`
- [ ] `rc-002`
- [ ] `rc-003`
- [ ] `rc-004`
- [ ] `rc-005`
- [ ] `rc-006`

### Tool / API arguments

- [ ] `ta-001`
- [ ] `ta-002`
- [ ] `ta-003`
- [ ] `ta-004`
- [ ] `ta-005`
- [ ] `ta-006`

## Required evaluator-failure finding

- [ ] Dana identified at least one case where automation was misleading or
      insufficient.

- Case ID:
- What the automation reported:
- What Dana concludes instead:
- Why the evaluator failed or was insufficient:
- Proposed correction, guardrail, or escalation rule:
- Does the correction change any measured score or final decision?

## Final interpretation — Dana only

- [ ] Every gold record has been approved or corrected.
- [ ] At least 10 queued cases have substantive review notes.
- [ ] The evaluator-failure finding above is complete.

- Final decision (`ship model B` / `do not ship` / `evidence insufficient`):
- Evidence supporting the decision:
- Strongest defensible claim:
- Important limitations and excluded claims:
- Follow-up evaluation required:
- Dana Edwards review date:
- Dana Edwards attestation/signature:

Until these fields are personally completed, `human_reviewed` must remain
false, `final_decision` must remain null, and no completion or portfolio-ready
claim is supported.

## Applying completed review to `gold.jsonl`

Only after the worksheet above is substantively complete, update every gold
record's two judgments, remove pending-review wording from reviewed rationales,
set `review_status` to `HUMAN REVIEWED`, and record the real `reviewed_by` and
`reviewed_at` values. Preserve the existing `response_sha256` bindings. If any
response text changes, treat its prior label as stale and rebind/review it; do
not work around the evaluator's alignment failure.

Then rerun the exact evaluate command from `README.md`. Gold-authoritative
metrics remain withheld unless the full set passes these checks. Finally,
update `receipt.json` only with facts Dana can personally attest; this file
does not by itself authorize setting the receipt to completed or replayed.
