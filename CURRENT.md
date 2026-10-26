# Current Career-Training Goal

## Active project: EVAL-001 — LLM Regression Sentinel

**Status:** machine build complete on draft PR #2; human review and completion gates pending  
**Track:** AI evaluation, model QA, applied-AI reliability  
**Evidence modes:** A (AI-augmented) + V (AI verification/supervision)  
**Benchmark:** [`benchmarks/EVAL-001/README.md`](benchmarks/EVAL-001/README.md)  
**Rubric:** [`rubrics/EVAL-001.md`](rubrics/EVAL-001.md)  
**Machine-build PR:** [#2 — Implement EVAL-001 LLM Regression Sentinel machine build](https://github.com/TheDarkLightX/Remote-Work-Compatibility-Ledger/pull/2)

This project remains the active goal until its definition of done is met. A new week does not replace it.

## Weekly checkpoint — 2026-10-26

**Decision: continue EVAL-001 unchanged.** Verified draft PR #2 is still open and unmerged; its machine-built harness is present, but `human-review.md` is still marked **PENDING HUMAN REVIEW**, all 37 `gold.jsonl` records still have `review_status = PENDING HUMAN REVIEW`, `oral-defense.md` is still **NOT STARTED / PENDING**, and `receipt.json` is still `draft` with a null score and no clean-checkout replay attestation. **No human completion or graduation is claimed.** The ten-case review gate remains the immediate bottleneck.

**Friction removed this week:** a [model-blind ten-case review packet](https://github.com/TheDarkLightX/Remote-Work-Compatibility-Ledger/blob/codex/eval-001-regression-sentinel/submissions/EVAL-001/dana-v1/BLIND_REVIEW_PACKET.md) and a [separate response identity key](https://github.com/TheDarkLightX/Remote-Work-Compatibility-Ledger/blob/codex/eval-001-regression-sentinel/submissions/EVAL-001/dana-v1/BLIND_REVIEW_KEY.md) were added to the existing PR branch. Their paired synthetic responses came from the branch's fixtures, but model identity, provisional gold labels, and grader outcomes are withheld from the first-pass packet. This is AI-prepared scaffolding, not human review. Open the identity key **only after** saving an independent verdict and rationale on each pair. Then record outcomes in `human-review.md`.

**Next human action:** judge `cu-006`, `cu-007`, `so-001`, `so-002`, `fg-002`, `if-001`, `rc-001`, `ta-001`, `cu-001`, and `cu-002`. For each, assess criterion adequacy, both responses, rationale, and deployment severity before comparing with the generator's expected labels. When these ten are settled, review the other 27 gold records, make the bounded release decision, complete unaided oral defense, perform clean-checkout replay, then apply the existing rubric. No new benchmark or score was created.

A [2026-10-26 market checkpoint](market/2026-10-26.md) confirms continued demand for evaluator calibration, rubric design, reproducible QA, regression diagnosis, and accountable technical decisions across remote roles and contract listings. Eligibility varies; no job fit or payment is guaranteed. EVAL-001 remains a better marginal portfolio investment than another infrastructure toy project. **Carryover is automatic and penalty-free.**

## Current evidence state

Codex completed the mechanical substrate on branch `codex/eval-001-regression-sentinel` at commit `2a84941d19d2445c08963a8e53aa40ddfd09f18e`.

The draft submission contains:

- a dependency-light `sentinel` Python CLI;
- 37 disclosed synthetic eval cases across six dimensions;
- paired synthetic `model_A` / `model_B` outputs;
- deterministic graders and strict fail-closed input/alignment checks;
- per-case, per-dimension, aggregate, transition, taxonomy, and evaluator-audit metrics;
- generated `results/summary.json` and `results/report.md`;
- adversarial/self-audit tests;
- conservative AI/provenance disclosure;
- human-review and oral-defense worksheets that remain explicitly pending.

The pull-request validation workflow passed. The branch README reports 39/39 local tests passing and byte-identical repeated result generation; that is machine-build evidence, not a clean-checkout replay attested by Dana.

The synthetic fixture currently measures `model_A` and `model_B` at 30/36 automatically scored cases each (83.33%), while hiding a −33.33 percentage-point structured-output regression in B and a +33.33 point calibrated-uncertainty improvement. These are synthetic harness measurements, not production-model results and not a final benchmark score.

### Weekly checkpoint — 2026-09-21

PR #2 remains an open draft at the same machine-build head commit, and `human-review.md` still shows all Dana-owned review fields and checkboxes pending. No evidence supports graduating the project yet. The benchmark and rubric remain fit for purpose; the bottleneck is execution of the human review, interpretation, replay, and defense gates rather than another specification rewrite.

## Why this remains the current goal

The original market scan selected this benchmark because remote AI evaluation/quality work repeatedly asks for:

- explicit evaluation criteria for ambiguous qualities;
- datasets and adversarial cases;
- regression and failure-mode diagnosis;
- separation of model failure from evaluator/harness/data failure;
- structured metrics and machine-readable outputs;
- concise technical decision communication.

A fresh market scan on **2026-09-21** again confirms these primitives in current remote and contract roles: LLM/agent evaluation pipelines, high-signal test-suite design, automated regression checks, golden-set / rubric design, human calibration, reproducible failure traces, model-vs-harness diagnosis, human-in-the-loop escalation, and deployment-quality gates. The machine work is already largely done, so the highest-value remaining work is the part that proves judgment rather than agent throughput: calibrating the gold set, attacking the evaluator, interpreting conflicting slice movement, bounding the claim, and defending the result.

See [`market/2026-08-31.md`](market/2026-08-31.md) for the original selection evidence, [`market/2026-09-14.md`](market/2026-09-14.md) for the prior refresh, and [`market/2026-09-21.md`](market/2026-09-21.md) for the September market check; see [`market/2026-10-26.md`](market/2026-10-26.md) for the newest checkpoint.

## Active goal

Convert the machine-built draft into a defensible human-reviewed evaluation artifact without weakening the provenance boundary.

## Highest-value remaining tasks

Work through these in whatever order is efficient. There is no daily schedule.

- [x] Create the `sentinel` Python package and runnable CLI on the draft branch.
- [x] Define at least 30 synthetic evaluation cases across at least five dimensions.
- [x] Produce paired synthetic `model_A` / `model_B` responses for every case.
- [x] Implement schema/input validation, deterministic ordering, metrics, failure taxonomy, deterministic graders, alignment checks, adversarial tests, and generated result artifacts.
- [ ] Personally review and approve/correct every expected condition and every provisional gold label in `gold.jsonl`.
- [ ] Complete substantive notes for at least 10 queued disagreement/regression/improvement/boundary cases in `human-review.md`.
- [ ] Independently decide whether `cu-006` really demonstrates a misleading lexical-grader pass; if not, identify another genuine evaluator failure or insufficiency.
- [ ] Decide whether the observed structured-output regression versus calibrated-uncertainty improvement supports `ship B`, `do not ship`, or `evidence insufficient`, and justify the weighting rather than relying on the aggregate tie.
- [ ] State the strongest defensible claim and the important exclusions/limitations.
- [ ] Apply the completed human judgments back into `gold.jsonl`, preserving response hash bindings, then rerun the evaluator so authoritative gold metrics are emitted rather than left null.
- [ ] Complete the oral-defense questions in `oral-defense.md` without AI assistance.
- [ ] Reproduce the committed artifacts from a clean checkout and record the exact commit SHA and commands/results.
- [ ] Update `receipt.json` only with facts personally established by the completed review/replay.
- [ ] Score the submission conservatively against `rubrics/EVAL-001.md`; portfolio-ready requires 80+ and no critical failure.
- [ ] Merge or otherwise graduate PR #2 only after the claim boundary and evidence state are accurate.

## Definition of done

EVAL-001 is complete only when:

1. every required deliverable exists in the committed submission;
2. the harness passes its self-tests;
3. the committed result reproduces from a clean checkout;
4. every gold record has been personally reviewed and appropriately bound;
5. at least 10 boundary/disagreement cases have substantive human notes;
6. at least one evaluator limitation/failure has been personally identified and explained;
7. AI use and authorship boundaries remain accurately disclosed;
8. the final report makes a bounded decision backed by the reviewed evidence;
9. the oral defense is completed without AI assistance;
10. the rubric score is at least 80 with no unresolved critical failure before any `portfolio-ready` claim.

If these are not true at the next weekly check-in, this project simply carries forward.

## What Codex / AI should handle now

Use agents for mechanical support, but not to substitute for the remaining judgment:

- present eval/prompt/response/gold/result tuples in a convenient review format;
- flag inconsistent rationales, stale hashes, missing metadata, or schema violations;
- apply edits to `gold.jsonl` exactly as directed after human review;
- rerun the harness and tests after review changes;
- regenerate deterministic outputs;
- automate a clean-checkout replay after Dana initiates/defines the replay environment;
- surface rubric evidence and missing fields without assigning Dana's final judgment for him.

## What Dana must personally understand or verify

The remaining evidence should demonstrate that Dana can explain and defend:

- why an aggregate tie can conceal deployment-relevant regressions;
- how each deterministic grader maps a response to an outcome;
- where lexical/structural graders can be semantically wrong;
- why `cu-007` is underdetermined from the supplied policy;
- how to distinguish model regression, input/data drift, labeling drift, and evaluator/harness error;
- what ID/SHA bindings establish and what stronger provenance claims they do not establish;
- why constructed synthetic cases do not support production-population inference;
- what additional evidence would most reduce uncertainty before a real deployment decision.

## Capability evidence unlocked when complete

A strong completion can upgrade evidence for:

- AI evaluation / model QA;
- software QA and adversarial testing;
- experiment and benchmark design;
- evaluator/harness validation;
- structured data handling and reproducible analysis;
- AI supervision and calibrated distrust of automation;
- technical decision writing;
- AI-augmented engineering with explicit human-owned claim boundaries.

It does **not** automatically prove employer-specific experience, production-model evaluation, external verification, clearance eligibility, or domain credentials.

## Carryover rule

**Incomplete project → continue it next week.**  
**Completed and verified project → graduate it, update the capability map, then research the next highest-value gap.**
