# Remote Work Compatibility Ledger

A public, replayable catalogue of work capabilities.

The purpose is simple: reduce the distance between **"I can do this work"** and **evidence a reviewer can inspect quickly**.

Instead of treating a resume, title, degree, or employer brand as the primary signal, this ledger stores task-level evidence: task, constraints, submitted output, AI-use policy, scoring rubric, verifier, receipt, limitations, and result.

## Current training goal

See **[`CURRENT.md`](CURRENT.md)**.

There is one active project at a time. If it is not finished during a calendar week, it remains the active goal next week. The system is a training routine, not a deadline machine.

The first active track is **EVAL-001 — LLM Regression Sentinel**, chosen from a current-market scan of recurring AI-evaluation/model-QA task primitives.

- Benchmark: [`benchmarks/EVAL-001/README.md`](benchmarks/EVAL-001/README.md)
- Rubric: [`rubrics/EVAL-001.md`](rubrics/EVAL-001.md)
- Codex work order: [`benchmarks/EVAL-001/CODEX_WORK_ORDER.md`](benchmarks/EVAL-001/CODEX_WORK_ORDER.md)
- Machine-built draft: [`submissions/EVAL-001/dana-v1/README.md`](submissions/EVAL-001/dana-v1/README.md) — human checkpoints pending
- Selection evidence: [`market/2026-08-31.md`](market/2026-08-31.md)
- Routine: [`TRAINING_ROUTINE.md`](TRAINING_ROUTINE.md)

## Evidence modes

Every scored submission declares one of three modes.

| Mode | Meaning | What it demonstrates |
| --- | --- | --- |
| **U — Unaided** | Candidate completes the task without generative-AI assistance. | Independent task competence. |
| **A — AI-augmented** | Candidate may use AI and automation, with the workflow disclosed. | Ability to turn AI into reliable productive leverage. |
| **V — AI verification / supervision** | Candidate evaluates, repairs, or rejects AI-produced work. | Judgment, error detection, QA, and model supervision. |

`U` is candidate-attested unless an external proctor is listed. Git history is not treated as proof that AI was absent.

## Recruiter path

A reviewer should be able to evaluate a capability in roughly 30–90 seconds:

1. Open [`capabilities.json`](capabilities.json).
2. Pick a capability relevant to the role.
3. Open one linked benchmark/submission or existing artifact.
4. Read the score, limitations, and failure analysis if a scored result exists.
5. Run the verifier/replay when one exists.
6. Ask the candidate to defend or reproduce a representative part live.

The deeper engineering/research portfolio remains at <https://www.danaedwards.info/>. Its recruiter-facing adapter is <https://www.danaedwards.info/capabilities.html>.

## Portfolio signal-to-noise

```text
Portfolio SNR =
  (role relevance × verifiability × difficulty × independence × recency)
  / reviewer time
```

A difficult artifact that takes an hour to understand can be weaker hiring evidence than a smaller task that maps directly to paid work and has an objective replay path.

## Repository structure

```text
CURRENT.md          One active career-training goal and checklist
benchmarks/         Public task specifications and Codex work orders
submissions/        Candidate work products and receipts
rubrics/            Public scoring rules
schemas/            Machine-readable evidence formats
verifiers/          Deterministic checks
market/             Evidence for why a benchmark is currently valuable
capabilities.json   Recruiter-facing capability index
TRAINING_ROUTINE.md Flexible weekly career-training protocol
```

## Benchmark design rules

A benchmark should:

- map to task primitives appearing in plausible paid remote work;
- be compact enough to inspect quickly;
- have explicit success/failure criteria;
- separate objective verification from subjective judgment;
- record whether AI was allowed and how it was used;
- preserve inputs so the task is replayable;
- include adversarial or ambiguous cases where the real work requires judgment;
- test the evaluator/harness as well as the candidate output where relevant;
- never manufacture a credential or external-verification claim.

## Capability status

Use conservative states:

- `planned`
- `in progress`
- `completed`
- `replayed`
- `portfolio-ready`
- `externally verified`

A file existing is not enough to call it verified.

## Weekly training loop

```text
Is current project complete?
        │
   no ──┴── yes
   │          │
carry forward  research current market
   │          │
next tasks     choose one highest-value gap
   └──────┬───┘
          ↓
AI-augmented construction
          ↓
human judgment + verification
          ↓
replayable evidence + live defense
          ↓
capability map
```

The objective is **career value per unit of human attention**, not project count.

## Verification infrastructure

Receipts use [`schemas/receipt-v1.schema.json`](schemas/receipt-v1.schema.json) and can be checked with:

```bash
python verifiers/validate_receipt.py submissions/EVAL-001/TEMPLATE/receipt.json
```

GitHub Actions validates committed receipts when relevant evidence files change.

## Principle

**Candidate claims. Work decides.**
