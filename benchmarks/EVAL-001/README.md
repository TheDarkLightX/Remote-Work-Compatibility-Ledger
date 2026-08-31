# EVAL-001 — LLM Regression Sentinel

**Track:** AI evaluation / model QA / applied AI reliability  
**Recommended mode:** A (AI-augmented)  
**Secondary mode:** V (AI verification/supervision)  
**Target effort:** 6–10 focused hours  
**Primary artifact:** runnable evaluation harness + report  

## Why this project exists

Remote AI-quality roles increasingly ask for more than rating isolated answers. The higher-value work is to define measurable quality, build evaluation sets, identify regressions and failure modes, and communicate whether a problem comes from the model, the data, or the harness.

This benchmark asks you to build that capability once in a reusable form.

## Scenario

A team is replacing `model_A` with `model_B`. Aggregate quality appears similar, but users report that the new model sometimes follows formatting instructions worse and occasionally makes confident unsupported claims.

Your job is to build a small **Regression Sentinel** that can answer:

1. Did model quality improve or regress overall?
2. Which capability dimensions changed?
3. Are apparent regressions statistically/operationally meaningful?
4. Which concrete failure modes explain the movement?
5. Could the evaluation harness itself be producing a false alarm?
6. What should a product/research team do next?

## Required deliverables

Create a submission under `submissions/EVAL-001/<submission-id>/` containing:

### 1. `README.md`

A reviewer-facing summary that can be understood in under two minutes:

- what you built;
- how to run it;
- top-line result;
- strongest detected regression/improvement;
- known limitations;
- your AI-use disclosure.

### 2. `evals.jsonl`

At least **30 evaluation cases** across at least five dimensions. Include a mix of straightforward and adversarial cases.

Recommended dimensions:

- factuality / grounding;
- instruction following;
- structured-output correctness;
- reasoning consistency;
- calibrated uncertainty;
- tool/API argument correctness;
- retrieval fidelity;
- refusal/constraint compliance where appropriate.

Each case must have a stable ID and enough information for another evaluator to understand what success means.

### 3. `responses.jsonl`

Two candidate-model outputs per eval (`model_A`, `model_B`).

You may:

- use real model APIs;
- use local/open models;
- generate a synthetic pair with deliberately planted regressions;
- combine these approaches.

If outputs are synthetic or modified, disclose that clearly. Do not present synthetic results as measurements of a real production model.

### 4. `gold.jsonl`

A human-authored or human-reviewed reference judgement for every case. At minimum record:

- pass/fail or ordinal quality;
- failure category if applicable;
- short rationale.

The gold set is the authority for benchmark scoring. If AI drafted any labels, manually review them and disclose that fact.

### 5. Evaluation harness

Implement a runnable Python tool with a command similar to:

```bash
python -m sentinel evaluate \
  --evals evals.jsonl \
  --responses responses.jsonl \
  --gold gold.jsonl \
  --out results/
```

The exact CLI is up to you, but a clean clone must be able to reproduce the report.

The harness must include:

- schema/input validation;
- per-dimension scoring;
- model-level aggregate metrics;
- error/failure taxonomy;
- regression comparison between A and B;
- explicit handling of missing/malformed records;
- deterministic output ordering;
- machine-readable result output.

### 6. At least one deterministic grader

Do **not** build an evaluator that is only `LLM-as-a-judge`.

Include at least one non-LLM check such as:

- JSON/schema validation;
- exact constraint checking;
- reference-set membership;
- numeric tolerance checks;
- citation/source matching;
- tool-argument validation.

If you use an LLM judge, measure it against the human gold labels and report agreement/disagreement.

### 7. `results/summary.json`

Include at least:

```json
{
  "model_a": {"overall": 0.0},
  "model_b": {"overall": 0.0},
  "delta": 0.0,
  "dimensions": {},
  "critical_failures": [],
  "judge_agreement": null,
  "cases": 0
}
```

You may extend this structure.

### 8. `results/report.md`

Write a concise decision memo answering:

- ship B;
- do not ship B;
- or evidence insufficient.

Support the recommendation with numbers and representative failure cases.

### 9. Harness self-test

Include tests that deliberately prove the evaluator can catch at least these failures:

- malformed JSON/JSONL;
- duplicate case IDs;
- missing model output;
- swapped/misaligned IDs;
- a planted structured-output regression;
- a scoring bug or corrupted expected value.

At least one test should demonstrate that **the harness can be wrong**, and that the problem is detectable.

### 10. `receipt.json`

Use the repository submission schema. Record:

- benchmark ID;
- evidence mode;
- start/end or elapsed time if tracked;
- tools/models used;
- candidate-attested unaided portions, if any;
- commands needed to reproduce the result;
- commit SHA after completion.

## AI policy

**AI use is encouraged in A-mode.** This project is meant to measure whether you can use AI as leverage without surrendering evaluation judgment.

You may use Codex or other assistants for:

- scaffolding code;
- test generation;
- refactoring;
- documentation drafts;
- candidate failure-case generation;
- debugging.

You remain responsible for:

- defining the evaluation objective;
- reviewing the gold labels;
- checking metrics;
- deciding the final claim boundary;
- explaining failures live.

Record substantive AI use in the receipt rather than pretending the work was unaided.

## Required human checkpoint

Before marking the benchmark complete, manually inspect at least **10 disagreement or boundary cases** and write `human-review.md` explaining:

- what the automated evaluator said;
- whether you agree;
- what changed, if anything;
- one case where the automation was misleading or insufficient.

This is the highest-value part of the benchmark for AI-supervision roles.

## Optional stretch work

Choose at most two; breadth is less important than a polished core artifact.

- bootstrap confidence intervals for the model delta;
- paired significance/permutation test;
- small HTML dashboard;
- CI regression gate that fails on a configured threshold;
- pluggable evaluator interface;
- prompt/version provenance hashes;
- cost/latency accounting;
- inter-rater agreement between human, deterministic grader, and LLM judge.

## Scoring

See [`../../rubrics/EVAL-001.md`](../../rubrics/EVAL-001.md).

A strong submission should let a reviewer answer, quickly:

> Can this person turn a fuzzy AI-quality complaint into a defensible, reproducible evaluation?

## Oral defense after completion

A separate short defense should be performed without AI assistance. Expect questions such as:

- Why is your aggregate score trustworthy?
- What is one way your benchmark can be gamed?
- Show a false positive or false negative from an automated grader.
- If B improves 4% overall but regresses 20% on structured outputs, would you ship it?
- How would you tell model regression from data drift?

The defense should be recorded in the submission as `oral-defense.md` with the questions, concise answers, and evaluator score.
