# Remote Work Compatibility Ledger

A public, replayable catalogue of work capabilities.

The purpose of this repository is simple: reduce the distance between **"I can do this work"** and **evidence that a reviewer can inspect quickly**.

Instead of treating a resume, title, degree, or employer brand as the primary signal, this ledger stores task-level evidence: the task, constraints, submitted output, AI-use policy, scoring rubric, verifier, and result.

## Evidence modes

Every scored submission declares one of three modes.

| Mode | Meaning | What it demonstrates |
| --- | --- | --- |
| **U — Unaided** | Candidate completes the task without generative-AI assistance. | Independent task competence. |
| **A — AI-augmented** | Candidate may use AI and automation, with the workflow disclosed. | Ability to turn AI into reliable productive leverage. |
| **V — AI verification / supervision** | Candidate evaluates, repairs, or rejects AI-produced work. | Judgment, error detection, QA, and model supervision. |

`U` is candidate-attested unless an external proctor is listed. The ledger never claims that a Git history can prove the absence of AI use.

## Recruiter path

A reviewer should be able to evaluate a capability in roughly 30–90 seconds:

1. Open [`capabilities.json`](capabilities.json).
2. Pick a capability relevant to the role.
3. Open the linked benchmark/submission.
4. Read the score and failure analysis.
5. Run the verifier when one exists.
6. Ask the candidate to defend or reproduce a small part live.

The deeper engineering/research portfolio remains available at <https://www.danaedwards.info/>. This repository is deliberately optimized for **task relevance and evaluation speed**.

## Portfolio SNR

The project uses a practical signal-to-noise objective:

```text
Portfolio SNR =
  (role relevance × verifiability × difficulty × independence × recency)
  / reviewer time
```

A difficult artifact that takes an hour to understand can be weaker hiring evidence than a smaller task that maps directly to a job and has an objective replay path.

## Repository structure

```text
benchmarks/          Public task specifications
submissions/         Candidate work products and receipts
rubrics/             Scoring rules
schemas/             Machine-readable formats
verifiers/           Deterministic checks where possible
market/              Evidence for why a benchmark is currently valuable
capabilities.json    Recruiter-facing capability index
```

## Benchmark design rules

A benchmark should:

- map to work that appears in current remote job descriptions;
- be small enough to inspect quickly;
- have explicit success/failure criteria;
- separate objective verification from subjective judgment;
- record whether AI was allowed;
- preserve inputs so the task is replayable;
- contain adversarial or ambiguous cases when the real job requires judgment;
- never manufacture a credential or claim external verification that did not occur.

## Scoring

Scores use a 0–100 scale. Each rubric names its dimensions and weights. Where applicable, the ledger records:

- quality score;
- critical-error count;
- false-positive rate;
- completion time;
- verifier result;
- AI mode (`U`, `A`, or `V`);
- disclosure/provenance notes;
- oral-defense status when tested.

A benchmark is not marked `verified` merely because a file exists. `verified` means the repository contains a reproducible check or an explicitly named external verifier/proctor.

## Weekly training loop

The catalogue is intended to grow from current market demand rather than a static curriculum:

```text
remote jobs → recurring task primitives → benchmark → training → submission → score → capability evidence
```

New projects should maximize expected career value per hour of candidate attention and AI/Codex usage. High-value projects are those that improve several employable capabilities at once and leave behind a compact, replayable artifact.

## Initial focus

The first track targets **AI evaluation / quality assurance** because it exercises a useful combination of research, judgment, specification following, adversarial testing, structured output, and AI supervision.

See [`benchmarks/EVAL-001/README.md`](benchmarks/EVAL-001/README.md).

## Principle

**Candidate claims. Work decides.**
