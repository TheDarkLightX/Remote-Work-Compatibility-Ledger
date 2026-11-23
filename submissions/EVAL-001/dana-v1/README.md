# EVAL-001 — LLM Regression Sentinel (`dana-v1`)

> **Status: DRAFT / IN PROGRESS.** The machine-build substrate is present, but
> Dana Edwards has not yet completed the required gold review, manual case
> inspection, final decision, unaided oral defense, clean-checkout replay, or
> final rubric assessment. This submission is not yet portfolio-ready.

This submission implements a dependency-light Python evaluation harness for
comparing two response sets, `model_A` and `model_B`, over a fixed evaluation
suite. It validates all three JSONL inputs before scoring, applies transparent
deterministic graders, reports paired changes by capability dimension and
failure type, and keeps machine measurement separate from human judgment.

All 37 cases and both response sets are **synthetic fixtures drafted with
OpenAI Codex**. The names `model_A` and `model_B` are fixture labels, not named
production models. The generated numbers therefore exercise the evaluation
infrastructure; they do not estimate real-world model quality.

## Measured synthetic result

| Metric | `model_A` | `model_B` | B − A |
| --- | ---: | ---: | ---: |
| Deterministic pass rate | 30/36 (83.33%) | 30/36 (83.33%) | +0.00 pp |
| Structured output | 6/6 (100.00%) | 4/6 (66.67%) | **−33.33 pp** |
| Calibrated uncertainty | 4/6 (66.67%) | 6/6 (100.00%) | **+33.33 pp** |
| Pending manual cases | 1 | 1 | n/a |

The aggregate tie hides material movement. The synthetic fixture contains six
B regressions and six B improvements. Its clearest planted regression is the
two-case structured-output drop (`so-001`, `so-002`); its clearest improvement
is the two-case calibrated-uncertainty gain (`cu-001`, `cu-002`). The structured
failures are marked critical at the **case level**; that is distinct from a
rubric-level critical failure.

The evaluator audit also exposes its own limits:

- `cu-006`: the substring grader passes `model_B` because it sees the required
  phrase, while the AI-drafted provisional label flags negation and an
  unsupported causal claim. This is an audit signal, not a human-verified
  correction.
- `cu-007`: the undefined policy term `material` makes deterministic grading
  unsupported, so both outputs are excluded from score denominators and routed
  to human review.

No ship / do-not-ship / insufficient-evidence decision has been made. Dana must
make that decision after the required human review.

## Run from the repository root

The harness uses the Python standard library and has no third-party runtime
dependency.

```bash
python -m sentinel evaluate \
  --evals submissions/EVAL-001/dana-v1/evals.jsonl \
  --responses submissions/EVAL-001/dana-v1/responses.jsonl \
  --gold submissions/EVAL-001/dana-v1/gold.jsonl \
  --out submissions/EVAL-001/dana-v1/results
```

Expected terminal result:

```text
PASS: validated 37 cases; model_A=30/36, model_B=30/36, delta=+0.000000
```

Run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

Validate the conservative provenance receipt:

```bash
python verifiers/validate_receipt.py submissions/EVAL-001/dana-v1/receipt.json
```

These commands are same-worktree reproduction instructions. They are not a
claim that Dana has completed the required clean-checkout replay.

## What the machine build contains

| Artifact | Purpose |
| --- | --- |
| `evals.jsonl` | 37 synthetic cases across six dimensions, each with an explicit grader and success criterion |
| `responses.jsonl` | Exactly one hash-bound synthetic `model_A` and `model_B` response per case |
| `gold.jsonl` | Response-bound AI-drafted provisional labels, all visibly `PENDING HUMAN REVIEW` |
| `results/summary.json` | Deterministic per-case, per-dimension, aggregate, transition, taxonomy, and evaluator-audit data |
| `results/report.md` | Generated measurement memo with the final human decision left null/pending |
| `human-review.md` | Candidate-owned review queue and blank decision record |
| `oral-defense.md` | Questions and blank answer/evaluation fields for an unaided defense |
| `receipt.json` | Mode-A AI-use disclosure and conservative provenance state |
| `sentinel/` | Strict input contracts, deterministic graders, scoring, and report generation |
| `tests/` | Positive, adversarial, fail-closed, determinism, and evaluator-self-audit tests |

The implemented grader types are exact match, required/forbidden substring,
valid JSON, constrained JSON structure, numeric tolerance, set membership,
regex, and explicit human-review routing. A recruiter can manually recompute
representative cases directly from the declared conditions and response text.

Automated metrics and gold-authoritative metrics are separate. The latter stay
`null` until every gold record is marked `HUMAN REVIEWED`, carries reviewer
metadata, has no pending judgment, and still matches the SHA-256 of the exact
response reviewed.

Input handling fails closed on malformed JSON/JSONL, blank lines, duplicate
JSON keys, duplicate IDs, unknown fields, unknown or missing cases, missing or
duplicated model outputs, invalid model names, response-ID mismatch, and stale
or swapped case hashes. Output keys and case ordering are deterministic.

## Known engineering and evidence limitations

- The suite is small, synthetic, deliberately constructed, and not a random
  sample of production traffic.
- Deterministic surface checks can be gamed and can miss semantics, negation,
  pragmatic meaning, and otherwise acceptable answer variants.
- The expected conditions, outputs, and provisional gold labels were
  AI-drafted; 0/37 gold records have been approved by Dana.
- The overall pass rate weights every automatically scorable case equally;
  application-specific severity or dimension weights are not modeled.
- The paired sign test is descriptive only because cases were hand-constructed;
  it does not support population-level inference.
- Static hashes detect ordinary swaps and stale records, not coordinated
  falsification of content and provenance.
- Live model sampling, latency, cost, repeated-run variance, data drift, and
  inter-rater reliability are outside this version's measurement scope.
- Clean-checkout reproducibility and external verification remain unconfirmed.
- This machine-build CLI intentionally leaves the final decision null and has
  no human-interpretation input yet. A later human-owned completion change must
  bind Dana's decision and claim boundary into the final generated memo rather
  than hand-editing a file that CI expects the harness to reproduce.

## Gold-finalization procedure — Dana only

For each line of `gold.jsonl`, Dana must personally inspect the bound eval and
both bound response records, then:

1. approve or correct each model's `outcome`, `failure_type`, and `rationale`;
2. remove the literal `PENDING HUMAN REVIEW` marker from reviewed rationales;
3. set `review_status` to `HUMAN REVIEWED`;
4. set `reviewed_by` to the actual reviewer and `reviewed_at` to the actual
   review timestamp;
5. leave each `response_sha256` unchanged unless the response itself changes.

If a response changes, its existing gold judgment is intentionally invalidated
and that response must be rebound and reviewed again. Do not bypass the hash
failure. After all 37 records are reviewed, rerun the evaluation command. The
harness will either fail closed on incomplete/stale review metadata or emit a
separate `authoritative_gold_scoring` result. This recorded state is still not
external verification.

## AI-use disclosure

OpenAI Codex was used substantially to implement and debug the package, CLI,
validation, deterministic graders, metrics, report generator, synthetic
fixtures, provisional labels, tests, and documentation scaffolding. AI use is
recorded in `receipt.json`. No candidate-attested unaided implementation claim
is made.

## Human-owned completion gates

Dana Edwards must personally complete every item below before claiming that
EVAL-001 is completed, replayed, scored, or portfolio-ready:

- [ ] Review and approve or correct every expected condition and gold label.
- [ ] Manually inspect at least 10 disagreement, regression, improvement, or
      boundary cases in `human-review.md`.
- [ ] Identify at least one case where automation was misleading or
      insufficient and record the reasoning.
- [ ] Decide `ship model B`, `do not ship`, or `evidence insufficient`.
- [ ] State the strongest defensible claim and its limitations.
- [ ] Answer the questions in `oral-defense.md` without AI assistance.
- [ ] Reproduce the committed artifacts from a clean checkout and record the
      exact commit SHA and replay evidence.
- [ ] Score the submission conservatively against the rubric and approve or
      reject final portfolio status.

**Governing principle: Candidate claims. Work decides.**
