# EVAL-001 Automated Measurement Report

> **SYNTHETIC FIXTURES — MACHINE MEASUREMENT ONLY.** The expected conditions and
> provisional labels were drafted with AI and remain **PENDING HUMAN REVIEW**. These
> results do not measure named production models.

## Decision status

**Dana's final decision: PENDING HUMAN REVIEW.** The harness does not choose `ship B`,
`do not ship`, or `evidence insufficient` on Dana's behalf.

## Measured result

| Metric | model_A | model_B | B − A |
| --- | ---: | ---: | ---: |
| Deterministic pass rate | 30/36 (83.33%) | 30/36 (83.33%) | +0.00 pp |
| Pending manual cases | 1 | 1 | n/a |

The suite contains **37 cases** across **6 dimensions**. 36 cases are automatically scorable and 1 is explicitly excluded pending human judgment.

## Dimension movement

| Dimension | Cases (scored) | model_A | model_B | B − A |
| --- | ---: | ---: | ---: | ---: |
| `calibrated_uncertainty` | 7 (6) | 4/6 (66.67%) | 6/6 (100.00%) | +33.33 pp |
| `factuality_grounding` | 6 (6) | 5/6 (83.33%) | 5/6 (83.33%) | +0.00 pp |
| `instruction_following` | 6 (6) | 5/6 (83.33%) | 5/6 (83.33%) | +0.00 pp |
| `reasoning_consistency` | 6 (6) | 5/6 (83.33%) | 5/6 (83.33%) | +0.00 pp |
| `structured_output` | 6 (6) | 6/6 (100.00%) | 4/6 (66.67%) | -33.33 pp |
| `tool_api_arguments` | 6 (6) | 5/6 (83.33%) | 5/6 (83.33%) | +0.00 pp |

## Paired changes

- B regressions (A pass → B fail): **6** — `fg-002`, `if-001`, `rc-001`, `so-001`, `so-002`, `ta-001`
- B improvements (A fail → B pass): **6** — `cu-001`, `cu-002`, `fg-003`, `if-002`, `rc-002`, `ta-002`
- Both pass: **24**
- Both fail: **0**
- Needs human review: **1**

The exact paired sign test is descriptive only: p = 1.000000 across 12 discordant pairs. Because these fixtures were deliberately constructed rather than randomly sampled, this is not evidence about a production population.

## Planted critical case failures

- `so-001` / `model_B` — `invalid_json` in `structured_output`; grader cause `invalid_json`. Criterion: The object has exactly ok:boolean with ok=true. Observed: invalid JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
- `so-002` / `model_B` — `wrong_json_type` in `structured_output`; grader cause `json_type_constraint_failure`. Criterion: The object has exactly id:string and count:integer. Observed: wrong types: count (expected integer, got string)

These are case-level severity flags in the synthetic fixture, not rubric-level critical failures.

## Declared domain failure taxonomy

| Model | Failure type | Count |
| --- | --- | ---: |
| `model_A` | `arithmetic_error` | 1 |
| `model_A` | `missing_required_argument` | 1 |
| `model_A` | `overconfidence` | 1 |
| `model_A` | `regex_format_violation` | 1 |
| `model_A` | `source_conflict_ignored` | 1 |
| `model_A` | `uncertainty_not_expressed` | 1 |
| `model_B` | `arithmetic_error` | 1 |
| `model_B` | `exact_format_violation` | 1 |
| `model_B` | `invalid_json` | 1 |
| `model_B` | `unsupported_factual_claim` | 1 |
| `model_B` | `wrong_argument_value` | 1 |
| `model_B` | `wrong_json_type` | 1 |

## Observed grader-failure causes

This second taxonomy records what the deterministic check actually observed; it is kept separate from the case author's declared domain failure category.

| Model | Grader cause | Count |
| --- | --- | ---: |
| `model_A` | `json_key_constraint_failure` | 1 |
| `model_A` | `numeric_out_of_tolerance` | 1 |
| `model_A` | `regex_mismatch` | 1 |
| `model_A` | `set_membership_failure` | 1 |
| `model_A` | `substring_constraint_failure` | 2 |
| `model_B` | `exact_mismatch` | 3 |
| `model_B` | `invalid_json` | 1 |
| `model_B` | `json_type_constraint_failure` | 1 |
| `model_B` | `numeric_out_of_tolerance` | 1 |

## Evaluator audit

The deterministic grader and AI-drafted provisional labels were comparable on 72 model/case judgments. They disagreed on **1**. This is draft consistency—not human judge agreement.

- `cu-006` / `model_B`: deterministic grader measured **pass**, reference label says **fail**. AI-drafted provisional label: the required phrase is negated and followed by an unsupported causal claim; the lexical grader is misleading here. PENDING HUMAN REVIEW.

Manual-only boundaries:

- `cu-007` (`calibrated_uncertainty`): Undefined policy term makes deterministic pass/fail unsupported.

`judge_agreement` remains `null`: 0/37 gold records are human-reviewed.

### Gold-authoritative result

Withheld: every response-bound gold record must be human-reviewed first. Automated pass rates above are measurements, not the final gold-authoritative score.

## Known engineering limitations

- The suite is small, synthetic, and deliberately balanced; it does not estimate real-model quality.
- Deterministic graders test declared surface conditions and can miss semantics, negation, or gaming.
- The expected conditions, outputs, and provisional labels were AI-drafted; Dana has not approved them.
- Static SHA-256 bindings catch ordinary swaps/staleness, but not coordinated falsification of IDs, hashes, and provenance at the source.
- Regex grader configurations are trusted inputs; Python regular expressions have no timeout and should not accept arbitrary untrusted patterns in a hosted service.
- No latency, cost, repeated-sampling variance, data drift, or live model API behavior is measured.
- A same-worktree deterministic rerun is not a candidate-confirmed clean-checkout replay.

## Human-owned decision checkpoint

Dana must personally complete these before any completion or portfolio-ready claim:

- [ ] Review and approve or correct every expected condition and gold label.
- [ ] Inspect at least 10 disagreement, regression, improvement, or boundary cases.
- [ ] Identify at least one case where automation was misleading or insufficient.
- [ ] Decide: `ship model B`, `do not ship`, or `evidence insufficient`.
- [ ] State the strongest defensible claim and its limitations.
- [ ] Complete the oral defense without AI assistance.
- [ ] Confirm reproduction from a clean checkout.
- [ ] Approve the final rubric score and portfolio status.

---

Generated deterministically by the Sentinel harness from the committed JSONL inputs. No timestamp is embedded so identical inputs produce identical bytes.
