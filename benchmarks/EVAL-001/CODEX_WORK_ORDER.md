# Codex Work Order — EVAL-001

Use this file as the implementation brief for the current career-training project.

## Objective

Implement the core of **LLM Regression Sentinel**, a small reproducible Python evaluation harness that compares two candidate model versions over a fixed evaluation set and makes regressions visible by capability dimension and failure type.

Do not mark the benchmark complete, invent scores, or claim human review has occurred. Leave human-owned checkpoints explicitly pending.

## Repository contract

Read first:

- `benchmarks/EVAL-001/README.md`
- `rubrics/EVAL-001.md`
- `schemas/receipt-v1.schema.json`
- `CURRENT.md`

Create the working submission under:

```text
submissions/EVAL-001/dana-v1/
```

## Minimum implementation

Build a small Python package with a CLI that can run from the repository root, for example:

```bash
python -m sentinel evaluate \
  --evals submissions/EVAL-001/dana-v1/evals.jsonl \
  --responses submissions/EVAL-001/dana-v1/responses.jsonl \
  --gold submissions/EVAL-001/dana-v1/gold.jsonl \
  --out submissions/EVAL-001/dana-v1/results
```

The exact package layout may vary, but keep it easy to understand and dependency-light.

### Required behavior

1. Parse and validate JSONL inputs.
2. Reject malformed records and duplicate case IDs.
3. Require exactly one `model_A` and one `model_B` response per expected case.
4. Detect missing, unknown, swapped, or misaligned IDs.
5. Support at least five evaluation dimensions.
6. Compute per-case outcomes, per-dimension metrics, and aggregate model scores.
7. Produce a failure taxonomy/counts.
8. Compare A vs B and report deltas.
9. Use deterministic output ordering.
10. Write machine-readable `results/summary.json`.
11. Write a concise generated `results/report.md` skeleton containing measured results but leaving the final human ship/no-ship interpretation clearly reviewable.

## Deterministic grading

Implement at least one non-LLM evaluator. Prefer several simple deterministic grader types, such as:

- exact match;
- required/forbidden substring;
- valid JSON;
- JSON schema/key constraints;
- numeric tolerance;
- set membership;
- regex/format constraint.

Design the case schema so individual evals declare which grader applies and its expected condition.

Do not rely solely on an LLM judge.

## Dataset scaffolding

Create at least 30 candidate eval cases across five or more dimensions. They may be synthetic, but clearly label them synthetic.

Suggested dimensions:

- factuality/grounding;
- instruction following;
- structured-output correctness;
- calibrated uncertainty;
- reasoning/consistency;
- tool/API argument correctness.

Plant a small number of known A/B differences so the harness can be tested, including:

- at least one structured-output regression in B;
- at least one improvement in B;
- at least one subtle failure that an aggregate score could hide;
- at least one boundary case requiring later human review.

AI may draft the dataset and gold labels, but mark all gold judgements as **PENDING HUMAN REVIEW** where appropriate. Do not represent them as independently human-authored until they actually are.

## Tests

Add automated tests proving the harness catches:

- malformed JSON/JSONL;
- duplicate case IDs;
- missing model output;
- unexpected case ID;
- model/case misalignment;
- planted structured-output regression;
- deliberately corrupted expected value or scoring condition.

At least one test must show a plausible way the evaluator itself can fail or mislead, plus a check that exposes the problem.

## Results and provenance

Create:

```text
submissions/EVAL-001/dana-v1/
  README.md
  evals.jsonl
  responses.jsonl
  gold.jsonl
  human-review.md
  oral-defense.md
  receipt.json
  results/
    summary.json
    report.md
```

`README.md` should state that the submission is **in progress** until all human checkpoints and clean replay are complete.

Populate `receipt.json` conservatively. Record Codex/AI as used. Leave commit SHA, elapsed time, human-review status, replay status, and final score unset/null/pending until they are known.

## Quality requirements

- Prefer standard library or a very small dependency set.
- Include a reproducible test command.
- Fail loudly on invalid inputs rather than silently skipping them.
- Keep scoring transparent enough that a reviewer can manually recompute a few cases.
- Do not hide important logic behind an opaque LLM call.
- Separate measured outputs from human interpretation.
- Keep generated artifacts stable across repeated runs on the same inputs.

## Human checkpoints — do not complete these automatically

Leave clear TODOs for the candidate to personally perform:

1. review every gold label;
2. manually inspect at least 10 disagreement/boundary cases;
3. identify a case where the automation was misleading or insufficient;
4. decide the final ship/do-not-ship/insufficient-evidence recommendation;
5. state the strongest defensible claim and important limitations;
6. answer the oral-defense questions without AI assistance;
7. perform/confirm a clean-checkout replay.

## Acceptance test

Before handing work back, Codex should be able to report truthfully:

```text
[ ] package imports successfully
[ ] CLI runs on the committed synthetic dataset
[ ] tests pass
[ ] invalid/misaligned data fails closed
[ ] deterministic grader is exercised
[ ] summary.json is generated deterministically
[ ] report.md is generated from measured results
[ ] AI/provenance disclosure is present
[ ] human checkpoints remain visibly pending
```

The purpose is not to make the repository look finished. The purpose is to hand the candidate a solid machine-built substrate on which **human evaluation judgment** can be demonstrated and defended.
