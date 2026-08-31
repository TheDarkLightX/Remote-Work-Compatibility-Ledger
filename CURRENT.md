# Current Career-Training Goal

## Active project: EVAL-001 — LLM Regression Sentinel

**Status:** planned / ready to build  
**Track:** AI evaluation, model QA, applied-AI reliability  
**Evidence modes:** A (AI-augmented) + V (AI verification/supervision)  
**Benchmark:** [`benchmarks/EVAL-001/README.md`](benchmarks/EVAL-001/README.md)  
**Rubric:** [`rubrics/EVAL-001.md`](rubrics/EVAL-001.md)

This project remains the active goal until its definition of done is met. A new week does not replace it.

## Why this is the current goal

The current market scan found a recurring cluster of tasks across remote AI evaluation/quality work:

- turn fuzzy quality requirements into explicit evaluation criteria;
- build datasets and adversarial cases;
- compare model versions;
- detect hallucinations, regressions, and specification failures;
- distinguish model failure from data/evaluator/harness failure;
- produce structured metrics and a concise decision memo;
- explain and defend the result.

EVAL-001 covers this cluster in one reusable artifact and also exercises Python, QA, data handling, research judgment, metrics, and technical communication.

See [`market/2026-08-31.md`](market/2026-08-31.md) for the selection evidence.

## Goal

Build a compact evaluation harness that can compare `model_A` and `model_B` across a human-reviewed eval set, identify regressions by capability dimension, catch malformed or misleading evaluation inputs, and produce a defensible ship / do-not-ship / insufficient-evidence decision.

## Task checklist

Work through these in whatever order is efficient. There is no daily schedule.

- [ ] Create the `sentinel` Python package and runnable CLI.
- [ ] Define at least 30 evaluation cases across at least five dimensions.
- [ ] Produce paired `model_A` / `model_B` responses for every case.
- [ ] Create and personally review the gold labels/rationales.
- [ ] Implement schema/input validation and deterministic ordering.
- [ ] Implement per-case, per-dimension, and aggregate comparison metrics.
- [ ] Implement a failure taxonomy.
- [ ] Include at least one deterministic non-LLM grader.
- [ ] Detect missing outputs, duplicate IDs, malformed JSONL, and ID misalignment.
- [ ] Add self-tests containing planted regressions and at least one deliberately corrupted evaluator/scoring condition.
- [ ] Generate machine-readable `results/summary.json`.
- [ ] Generate a short `results/report.md` with a ship/no-ship/insufficient-evidence recommendation.
- [ ] Manually inspect at least 10 disagreement/boundary cases and write `human-review.md`.
- [ ] Record substantive AI/Codex use accurately in `receipt.json`.
- [ ] Run the complete project from a clean checkout and record the reproduction commands.
- [ ] Complete the short unaided oral-defense questions in `oral-defense.md`.
- [ ] Score the submission conservatively against `rubrics/EVAL-001.md`.

## Definition of done

EVAL-001 is complete only when:

1. every required deliverable in the benchmark exists;
2. the harness passes its self-tests;
3. the committed result reproduces from a clean checkout;
4. the gold set has been human-reviewed;
5. AI use is disclosed;
6. the report makes a bounded decision backed by the output;
7. no unresolved critical rubric failure remains;
8. the work can be defended without relying on AI during the defense.

If these are not true at the next weekly check-in, this project simply carries forward.

## What Codex / AI should do

Use AI aggressively for mechanical leverage:

- scaffold the Python package and CLI;
- write parsers, schemas, tests, and fixtures;
- generate candidate adversarial eval cases for human review;
- create synthetic `model_A` / `model_B` outputs with explicitly planted regressions;
- implement metrics and report-generation plumbing;
- refactor and document code;
- propose edge cases and ways to attack the evaluator itself.

A ready-to-use Codex handoff is in [`benchmarks/EVAL-001/CODEX_WORK_ORDER.md`](benchmarks/EVAL-001/CODEX_WORK_ORDER.md).

## What the candidate must personally own

Do not outsource these judgments blindly:

- what each evaluation dimension means;
- what counts as success/failure;
- final review of the gold labels;
- whether the metrics actually support the report's recommendation;
- inspection of disagreement and boundary cases;
- identification of at least one way the evaluator itself can mislead;
- the final claim boundary;
- live explanation of representative cases and design choices.

## Capability evidence unlocked

A strong completion can upgrade evidence for:

- AI evaluation / model QA;
- software QA and adversarial testing;
- structured data handling;
- experiment/evaluation design;
- AI supervision and error detection;
- technical decision writing;
- AI-augmented engineering with explicit human verification.

It does **not** automatically prove employer-specific experience, clearance eligibility, domain credentials, or external verification.

## Carryover rule

**Incomplete project → continue it next week.**  
**Completed and verified project → graduate it, update the capability map, then research the next highest-value gap.**
