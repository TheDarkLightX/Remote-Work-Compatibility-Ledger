# Remote Work Training Routine

This is a standing capability-maintenance program for a labor market being reshaped by AI.

The objective is not to collect courses or toy projects. It is to maintain and expand the ability to perform valuable remote knowledge work, with and without AI, while continuously converting that ability into inspectable evidence.

## Weekly cycle

### Monday — Market selection

Choose exactly one project for the week from current remote-work demand.

Selection should maximize:

```text
Career Value =
  current demand
  × breadth across role families
  × fit with existing strengths
  × AI leverage
  × verifiability
  × reviewer signal-to-noise
  × durability of skill
  ÷ human time cost
```

Reject projects that are primarily tutorial consumption, resume decoration, generic CRUD demos, or redundant with stronger existing evidence.

Target project size: roughly 6–10 focused hours.

### Tuesday — Build I

Work on the highest-value core of the benchmark for 90–120 minutes.

Priority order:

1. task/data/specification quality;
2. minimal working implementation;
3. objective checks;
4. tests and failure cases;
5. presentation.

Use Codex/AI aggressively when the benchmark allows it, but keep a clear record of what it did and what the human reviewer personally checked.

### Thursday — Build II

Continue the project for another 90–120 minute block.

Prioritize the weakest rubric dimension, not the most entertaining feature.

At least one checkpoint in each week's project should require direct human judgment, explanation, or review rather than merely accepting generated output.

### Saturday — Verification + live defense

Treat the artifact as hostile.

- replay from a clean state;
- run tests and adversarial cases;
- inspect provenance and AI-use disclosure;
- look for a way the benchmark, grader, or metric could itself be wrong;
- fix the highest-severity issue;
- answer a short interview/oral-defense drill without AI assistance.

The goal is to make `I built this` defensible under questioning.

### Sunday — Scorecard

Score the work conservatively against the public rubric.

Record:

- what was actually completed;
- final or provisional score;
- strongest new capability signal;
- largest unresolved weakness;
- whether a clean replay succeeded;
- whether the artifact deserves `completed`, `replayed`, `portfolio-ready`, or no upgrade;
- one carryover item for next week.

Only then update `capabilities.json` or the personal-site capability page.

## Evidence modes

- **U — Unaided:** independent work, candidate-attested unless externally proctored.
- **A — AI-augmented:** AI/Codex permitted and disclosed; human remains responsible for correctness and claim scope.
- **V — AI verification/supervision:** evaluate, challenge, repair, or reject AI-produced work.

The long-run objective is not to maximize U-mode. Modern work often rewards intelligent tool use. The objective is to retain enough U-mode competence to understand and defend the work while becoming unusually strong in A- and V-mode.

## Training priorities

The default priority order is:

1. capabilities currently appearing in paid remote work;
2. capabilities that remain valuable as AI improves;
3. work involving verification, judgment, ownership, system integration, or accountability;
4. skills that can be demonstrated with compact replayable artifacts;
5. gaps that prevent access to several role families at once;
6. interview/live-defense competence around already demonstrated skills.

Avoid overinvesting in tasks whose economic value is being rapidly commoditized unless they are useful for immediate bridge income.

## Portfolio admission rule

A weekly project does not automatically go on the public-facing capabilities page.

Publish it as strong evidence only when it is:

- directly relevant to plausible work;
- understandable quickly;
- accurately disclosed;
- reproducible where applicable;
- adversarially tested;
- strong enough to survive a live defense.

Weak projects stay in training history rather than diluting the public signal.

## Long-run outcome

Over time, the ledger should become a time series of capability rather than a static resume:

```text
market demand
    ↓
weekly benchmark
    ↓
AI-augmented construction
    ↓
human verification
    ↓
live defense
    ↓
replayable evidence
    ↓
capability map
```

**Candidate claims. Work decides.**
