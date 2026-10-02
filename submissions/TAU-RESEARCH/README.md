# Tau Language — independent research experiments

**Dana Edwards / TheDarkLightX · existing, unscored research evidence**  
Source snapshot: [TauLang-Experiments @ `65ef69bd`][repo]; checked 2026-10-02.

Built a public research collection connecting **formal semantics, executable
reference models, neuro-symbolic evidence gates, and measured implementation
experiments**. Its distinctive contribution is the construction and integration
of these artifacts with explicit acceptance and failure boundaries. No
literature-wide priority claim is made for the underlying mathematical laws.

## Research map

| Research contribution | Inspectable evidence | Scope and limitation |
| --- | --- | --- |
| Safe finite/infinite table semantics | [Safe syntax][safe], [select/revision extension][revision], and [negative boundary proofs][boundary] | Lean artifacts connect restricted syntax to monotone, omega-continuous updates and fixed points. Current-state guards and unrestricted complement/recurrence remain outside the safe fragment; no full Tau runtime proof. |
| Exact symbolic filtering after neural proposals | [qNS design][qns], [Lean partition/no-leak laws][qnsproof], [EML certificate/memory workflow][eml] | Finite `qns8/qns64` carriers check masks; host checks establish the evidence bits. Default memory demo uses fixtures; live Ollama is optional. No proof of neural extraction or cryptographic attestation. |
| Bounded game/mechanism tables | [Game model and three Lean packets][game] | Listed-game checker, model-coverage bridge, and certified deviation pruning. Completeness depends on listed players/profiles/deviations; no general game-theory solution. |
| Incremental execution | [Reference-model script][incremental] | Read-set-guided recomputation and dependency-index controls over a four-cell Boolean-algebra expression model. This model is not a native Tau runtime optimization. |
| Normalization and QE experiments | [Equality-aware simplification][equality], [fragment-routing research][qe], [current experiment summary][overview] | Feature-gated experiments preserve semantic checks and record negative results. Corpus-specific reductions and internal-path timings do not establish a default or universal speedup. |
| Native execution and proof-checker optimization | [VM compact-memory package][memory], [TauFold execution/proving package][taufold] | Source-pinned builds, independent output comparisons, recorded receipts and mutation checks. Experimental work; [Tau #199][issue199] remains open. |

The pinned repository contains **10 Lean proof source packets**: six for
infinite-table semantics/boundaries, three for bounded games, and one for qNS.
These are scoped proof artifacts with replay instructions, not a formal
verification of Tau's C++ implementation. Lean was not run in this audit.

## Measured evidence worth inspecting

The public [VM memory package][memory] records 531 output checks per source and
identical loaded-formula hashes after the record-equality rewrite. Five-run
medians show sampled RSS falling from 1,074.8 to 554.8 MiB and setup from 3.451
to 1.962 seconds, against the already shared-lookup source. Sampled RSS is not
peak RSS; these are results for the bundled VM.

The [TauFold package][taufold] records 1,932 native transition comparisons and
4.96–9.20× speedups in setup plus native step calls across three applications for the
**combined** retained-evaluator/source route. Its prepared checker records
60.3–65.7% fewer guest cycles and separate-process verification of nine real
receipts across three checker versions. These are source-reported experiments,
not fresh replays here. Native timings exclude proving and host checks;
single-run proof timings are not treated as stable speed estimates. The
prepared checker changes the guest identity and requires an explicit verifier
pin update.

## Fresh bounded model replay

On 2026-10-02, Codex ran the exact two public Python source blobs at the pinned
snapshot using Python 3.12.14. Their Git blob hashes matched upstream.

- **Game model:** nine profiles; certified profitable-deviation pruning retained
  three; the sole desired safe profile, `contribute/reward`, was preserved.
  Python model check passed; Tau equivalence was explicitly skipped.
- **Incremental model:** all six cases passed; full residual reevaluation counted
  193 unique nodes versus 31 recomputed nodes. Dependency-plan and delta checks
  passed. The 83.938% figure is a **node-count reduction**, not a wall-clock
  speedup.

[Replay summary and source hashes](replay-summary.json) records this limited
execution. To reproduce from the public snapshot:

```bash
git clone https://github.com/TheDarkLightX/TauLang-Experiments.git tau-research
cd tau-research
git checkout --detach 65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1
python3 scripts/run_game_table_demo.py --out results/local/game-table-demo.json
python3 scripts/run_incremental_execution_demo.py --out results/local/incremental-execution-demo.json
```

For the qNS proof, follow its pinned Lean toolchain:

```bash
cd proofs/lean/qns_semantic_ba_v001
lake env lean Proofs.lean
```

Native Tau and proving replay prerequisites are in the linked packages. The
Python replays do not substitute for either.

## Provenance and limits

This index and its two local replays were Codex-assisted (A mode). Historical
research includes AI/proof-tool workflows, including Aristotle-labeled packets;
the public artifacts do not fully attest the human/AI task split. No unaided
performance or candidate live defense is claimed.

Upstream adoption is recorded in the separate [contribution inventory](../TAU-UPSTREAM/README.md).
Research patches, successful finite tests and repository-reported proof checks
are not automatically upstream acceptance. No benchmark score or
`externally-verified` ledger receipt is assigned.

[repo]: https://github.com/TheDarkLightX/TauLang-Experiments/tree/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1
[overview]: https://github.com/TheDarkLightX/TauLang-Experiments/blob/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/README.md
[safe]: https://github.com/TheDarkLightX/TauLang-Experiments/blob/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/proofs/lean/infinite_tables/safe_table_syntax/README.md
[revision]: https://github.com/TheDarkLightX/TauLang-Experiments/blob/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/proofs/lean/infinite_tables/safe_table_select_revision/README.md
[boundary]: https://github.com/TheDarkLightX/TauLang-Experiments/tree/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/proofs/lean/infinite_tables/operation_safety_boundary
[qns]: https://github.com/TheDarkLightX/TauLang-Experiments/blob/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/docs/neuro-symbolic-boolean-algebras.md
[qnsproof]: https://github.com/TheDarkLightX/TauLang-Experiments/blob/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/proofs/lean/qns_semantic_ba_v001/Proofs.lean
[eml]: https://github.com/TheDarkLightX/TauLang-Experiments/blob/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/docs/eml-qns-symbolic-regression.md
[game]: https://github.com/TheDarkLightX/TauLang-Experiments/blob/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/docs/game-theory-tables.md
[incremental]: https://github.com/TheDarkLightX/TauLang-Experiments/blob/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/scripts/run_incremental_execution_demo.py
[equality]: https://github.com/TheDarkLightX/TauLang-Experiments/blob/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/docs/equality-aware-path-simplification.md
[qe]: https://github.com/TheDarkLightX/TauLang-Experiments/blob/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/docs/qelim-epiplexity-routing.md
[memory]: https://github.com/TheDarkLightX/TauLang-Experiments/blob/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/results/vm-compact-memory-2026-09-30/compact-memory-replay/README.md
[taufold]: https://github.com/TheDarkLightX/TauLang-Experiments/blob/65ef69bdc5e6f1e479236d9dfb4d9b6d2e5302d1/results/taufold-execution-and-proving-2026-10-01/taufold-replay/README.md
[issue199]: https://github.com/IDNI/tau-lang/issues/199
