# Tau Language — upstream contributions

**Dana Edwards / TheDarkLightX · existing, unscored evidence**  
Audit date: 2026-10-02. Scope: authored issues in `IDNI/tau-lang`.

**32 issue reports have maintainer-confirmed upstream fixes.** The complete
[authored-issue search][search] returned 41 issues: 34 closed and seven open.
Of the closed issues, #46 duplicates an earlier report and #192 preserves the
existing input contract; neither is counted as a new fix. Counts are issue
threads, not distinct bugs, commits, or authored pull requests.

The work demonstrates semantic debugging, deterministic oracles, regression
design, performance investigation, and collaboration through maintainer review.
Integration was commonly through maintainer commits. The table below credits
the report, diagnosis, proposed patch, and accepted result separately.

## Fast recruiter path

- [#139][r139]: upstream isolated the read-set patch, confirmed byte-identical
  outputs, measured approximately 10× improvement on two lookback workloads,
  and accepted it with one early return. Controls were within noise.
- [#135][r135]: an active-definition filter was incorporated with refinements.
  The maintainer measured 4.7× end-to-end improvement on the nested-defs-128
  case; caller-first ordering showed no gain.
- [#134][r134]: submitted memoization entered a combined DAG-processing fix.
  The maintainer found **no benefit from that memo alone on stock devel**;
  the combined result must not be attributed to the memo in isolation.
- [#197][r197]: a witness table and the distinction between atomic and atomless
  algebras informed a scoped fix; the submitted cases became regressions.
  The maintainer reported 2,660/2,660 default, 2,004/2,004 bv-only, and
  1,562/1,562 no-bv tests passing for that fix.
- [#193][r193]: the proposed macOS enum rename was applied. Upstream simulated
  the SDK macros in a portable regression; it did not rebuild on macOS.

These are **maintainer-reported measurements/checks at the linked revisions**,
not fresh local replays or general performance guarantees. #138 is also useful
review evidence: upstream retained the parser optimization only after fixing
conjunctive-grammar counterexamples and adding a GC fallback.

## Complete fixed-issue inventory

Each outcome links the maintainer's explanation and exact upstream commit(s).
Recent outcomes explicitly identify `devel`; inclusion in `main` or a release
is not inferred. #187–#189 share one commit.

<details>
<summary>Inspect all 32 confirmed fixed reports</summary>

| Issue | Contribution and adoption boundary | Maintainer evidence and source |
| --- | --- | --- |
| [#54](https://github.com/IDNI/tau-lang/issues/54) | Bug report; parser fix credited to pt7k and follow-up to castrod. | [Outcome](https://github.com/IDNI/tau-lang/issues/54#issuecomment-3797422955); [c9444cb2](https://github.com/IDNI/tau-lang/commit/c9444cb279137c7c59109cc2702cb06957556703), [d20986ba](https://github.com/IDNI/tau-lang/commit/d20986baaa177e21d1a3d336cdad6dfa80cc7d6d) |
| [#58](https://github.com/IDNI/tau-lang/issues/58) | File-stream/type report; upstream repaired stream storage and typing. | [Outcome](https://github.com/IDNI/tau-lang/issues/58#issuecomment-3797427893); [91187610](https://github.com/IDNI/tau-lang/commit/911876108d53986cb2709172a5ef6af4eaa0c88e), [393bf2f9](https://github.com/IDNI/tau-lang/commit/393bf2f98d79c34fa98667bf746b69f5a803e86c), [c702d8be](https://github.com/IDNI/tau-lang/commit/c702d8bee9983077ce27e6847ac87f47558544b5) |
| [#129](https://github.com/IDNI/tau-lang/issues/129) | Truth tables and diagnosis; XOR-lowering proposal adopted. | [Outcome](https://github.com/IDNI/tau-lang/issues/129#issuecomment-5792607766); [1a272fbd](https://github.com/IDNI/tau-lang/commit/1a272fbd55cc66ae313b9ad8e02f394a06f82274) |
| [#130](https://github.com/IDNI/tau-lang/issues/130) | Failure report; upstream supplied the minimal case and a different terminating fix. | [Outcome](https://github.com/IDNI/tau-lang/issues/130#issuecomment-5792608360); [20948938](https://github.com/IDNI/tau-lang/commit/20948938d7b45cf7430fb915b907081426c52a4f) |
| [#131](https://github.com/IDNI/tau-lang/issues/131) | Formula-input contract proposal adopted and aligned with realizable. | [Outcome](https://github.com/IDNI/tau-lang/issues/131#issuecomment-5792608830); [48b29d8b](https://github.com/IDNI/tau-lang/commit/48b29d8be85027bd27168f18c84296be07ca22b0) |
| [#132](https://github.com/IDNI/tau-lang/issues/132) | Formula gate adopted at the shared API layer, with a defensive fast-path check. | [Outcome](https://github.com/IDNI/tau-lang/issues/132#issuecomment-5792609374); [744a6d2c](https://github.com/IDNI/tau-lang/commit/744a6d2c8cc197ae945398e7a798a0c17ec84f13) |
| [#133](https://github.com/IDNI/tau-lang/issues/133) | Measurements and two patches; upstream chose asynchronous subprocesses with lifecycle controls. | [Outcome](https://github.com/IDNI/tau-lang/issues/133#issuecomment-5792609964); [31592194](https://github.com/IDNI/tau-lang/commit/31592194ca771fe23dbd91bac9fa78edab27f301) |
| [#134](https://github.com/IDNI/tau-lang/issues/134) | Memos and dependence skip incorporated into a combined shared-DAG fix. | [Outcome](https://github.com/IDNI/tau-lang/issues/134#issuecomment-5822465423); [af98abe5](https://github.com/IDNI/tau-lang/commit/af98abe52b4a3b8ec0b9293663c2b8f91b649aa2) |
| [#135](https://github.com/IDNI/tau-lang/issues/135) | Active-rule filter adopted with head-extraction and update refinements. | [Outcome](https://github.com/IDNI/tau-lang/issues/135#issuecomment-5822465981); [20ad15fc](https://github.com/IDNI/tau-lang/commit/20ad15fc010337a88a646e0f5359bfcf4bb6e147) |
| [#136](https://github.com/IDNI/tau-lang/issues/136) | Error-handling proposal adopted; upstream also repaired concrete witness generation. | [Outcome](https://github.com/IDNI/tau-lang/issues/136#issuecomment-5822466616); [be89453b](https://github.com/IDNI/tau-lang/commit/be89453b1e9c90fa4f44c9ee4644076dcf1a8d68) |
| [#137](https://github.com/IDNI/tau-lang/issues/137) | Temporal-semantics diagnosis and sound gate; equivalent upstream gate adopted. | [Outcome](https://github.com/IDNI/tau-lang/issues/137#issuecomment-5822467104); [fee72ba5](https://github.com/IDNI/tau-lang/commit/fee72ba591ee93df5b4f8a9e6c9c1932a2dd5e24) |
| [#138](https://github.com/IDNI/tau-lang/issues/138) | Parser optimization retained after upstream corrected conjunct handling and GC fallback. | [Outcome](https://github.com/IDNI/tau-lang/issues/138#issuecomment-5822789862); [fd536d56](https://github.com/IDNI/tau-lang/commit/fd536d56e00f12187cbed123c67a735a6964c660) |
| [#139](https://github.com/IDNI/tau-lang/issues/139) | Read-set optimization accepted with an additional input-free early return. | [Outcome](https://github.com/IDNI/tau-lang/issues/139#issuecomment-5822467539); [36b701bf](https://github.com/IDNI/tau-lang/commit/36b701bf1f57a172f843859fdbdb0d4e14993ad9) |
| [#140](https://github.com/IDNI/tau-lang/issues/140) | Model-validity report and diagnosis; upstream added a joint order solver and model checks. | [Outcome](https://github.com/IDNI/tau-lang/issues/140#issuecomment-5822468249); [9bc370da](https://github.com/IDNI/tau-lang/commit/9bc370dac9568e21928a1e7d4a203158cfafac8b) |
| [#141](https://github.com/IDNI/tau-lang/issues/141) | Wrong-verdict evidence; upstream added fail-closed handling and scoped decisions. | [Outcome](https://github.com/IDNI/tau-lang/issues/141#issuecomment-5822468641); [efe7e5b9](https://github.com/IDNI/tau-lang/commit/efe7e5b9f9e7f5a8876561b46a847dcc9c4dc6c2) |
| [#142](https://github.com/IDNI/tau-lang/issues/142) | Capacity-exhaustion report; upstream implemented checked overflow propagation. | [Outcome](https://github.com/IDNI/tau-lang/issues/142#issuecomment-5822469078); [b638fc9c](https://github.com/IDNI/tau-lang/commit/b638fc9c5e6438bfd091504151705d01b0ecb25a) |
| [#148](https://github.com/IDNI/tau-lang/issues/148) | Pinned-value diagnosis and follow-up rule; upstream landed scoped elimination fixes. | [Outcome](https://github.com/IDNI/tau-lang/issues/148#issuecomment-5885189439); [e47e43c0](https://github.com/IDNI/tau-lang/commit/e47e43c0dfb63a2ee936a2d623f72e60780fe2c4), [9579437b](https://github.com/IDNI/tau-lang/commit/9579437be1721eb55d9ac3535d10dc14ea010bac) |
| [#149](https://github.com/IDNI/tau-lang/issues/149) | Binder-capture diagnosis; upstream took a narrower evaluation/renaming fix. | [Outcome](https://github.com/IDNI/tau-lang/issues/149#issuecomment-5885189973); [7d061497](https://github.com/IDNI/tau-lang/commit/7d061497ca1c4e7c24714d54c7f110b07aa1c6aa) |
| [#150](https://github.com/IDNI/tau-lang/issues/150) | Warm-up report, control and patch; upstream repaired a second uncovered path too. | [Outcome](https://github.com/IDNI/tau-lang/issues/150#issuecomment-5937345414); [3bd46027](https://github.com/IDNI/tau-lang/commit/3bd4602714a13b0dd2f6b102c63abd88a5a59e50) |
| [#181](https://github.com/IDNI/tau-lang/issues/181) | Extremum report/source pointer; returned-value regression oracle adopted. | [Outcome](https://github.com/IDNI/tau-lang/issues/181#issuecomment-5887055342); [f960222f](https://github.com/IDNI/tau-lang/commit/f960222fe80e9a2520abc3d4992efd621966cad8) |
| [#183](https://github.com/IDNI/tau-lang/issues/183) | Arithmetic/QE diagnosis confirmed; guard fixed and minimal examples checked. | [Outcome](https://github.com/IDNI/tau-lang/issues/183#issuecomment-5887056077); [d99d3a19](https://github.com/IDNI/tau-lang/commit/d99d3a196dcb1db5f8d836e53b072945b63ef51b) |
| [#185](https://github.com/IDNI/tau-lang/issues/185) | Grammar patch matched; printer and definition/fallback follow-ups also fixed. | [Outcome](https://github.com/IDNI/tau-lang/issues/185#issuecomment-5888421840); [378ccf21](https://github.com/IDNI/tau-lang/commit/378ccf214f05cdc7b24485d780b23a6ab0d47038), [8c78610d](https://github.com/IDNI/tau-lang/commit/8c78610da95f5ea0cca5bf32e3d5c7246c1585a4) |
| [#186](https://github.com/IDNI/tau-lang/issues/186) | Exact-endpoint report; upstream replaced rounded qint endpoints. | [Outcome](https://github.com/IDNI/tau-lang/issues/186#issuecomment-5885188988); [c7e87400](https://github.com/IDNI/tau-lang/commit/c7e8740064af64f6388faa88e7e9b3f3fd75c7f9) |
| [#187](https://github.com/IDNI/tau-lang/issues/187) | Interval-collector diagnosis; unsupported compound shapes now retain their binder. | [Outcome](https://github.com/IDNI/tau-lang/issues/187#issuecomment-5868690284); [f2eafe30](https://github.com/IDNI/tau-lang/commit/f2eafe3039f131037c55888e3c24d9a972f3ef47) |
| [#188](https://github.com/IDNI/tau-lang/issues/188) | Domain inconsistency report; endpoint handling aligned across paths. | [Outcome](https://github.com/IDNI/tau-lang/issues/188#issuecomment-5868690997); [f2eafe30](https://github.com/IDNI/tau-lang/commit/f2eafe3039f131037c55888e3c24d9a972f3ef47) |
| [#189](https://github.com/IDNI/tau-lang/issues/189) | Witness table; closed-conjunct handling fixed and cases made regression tests. | [Outcome](https://github.com/IDNI/tau-lang/issues/189#issuecomment-5868691684); [f2eafe30](https://github.com/IDNI/tau-lang/commit/f2eafe3039f131037c55888e3c24d9a972f3ef47) |
| [#190](https://github.com/IDNI/tau-lang/issues/190) | Replay package and printer correction adopted. | [Outcome](https://github.com/IDNI/tau-lang/issues/190#issuecomment-5890257437); [48a5e304](https://github.com/IDNI/tau-lang/commit/48a5e304079a7e100ecb62886ce335773a99e065) |
| [#193](https://github.com/IDNI/tau-lang/issues/193) | SDK/header diagnosis; submitted rename applied with a macro-collision regression. | [Outcome](https://github.com/IDNI/tau-lang/issues/193#issuecomment-5934551146); [fc973291](https://github.com/IDNI/tau-lang/commit/fc97329163c0a44587c5f0ddb9025b4601955158) |
| [#194](https://github.com/IDNI/tau-lang/issues/194) | Test-only budget correction applied; default runtime budget unchanged. | [Outcome](https://github.com/IDNI/tau-lang/issues/194#issuecomment-5890258010); [dd5a841a](https://github.com/IDNI/tau-lang/commit/dd5a841ac1e8ee80aec73939239225a88f53f056) |
| [#195](https://github.com/IDNI/tau-lang/issues/195) | Typed-argument diagnosis confirmed; extraction fixed with mismatch controls. | [Outcome](https://github.com/IDNI/tau-lang/issues/195#issuecomment-5890258803); [d67356b4](https://github.com/IDNI/tau-lang/commit/d67356b4167806f7e4dcb81a8efa6ff1d62a2193) |
| [#196](https://github.com/IDNI/tau-lang/issues/196) | Three-way control comparison exposed expansion and false-verdict defects; both fixed. | [Outcome](https://github.com/IDNI/tau-lang/issues/196#issuecomment-5932520417); [c1299605](https://github.com/IDNI/tau-lang/commit/c1299605bdf426b1b36c67a2be75da7ca197320e), [38a85814](https://github.com/IDNI/tau-lang/commit/38a85814d125c23fc9b76fa948360f600f9d1533) |
| [#197](https://github.com/IDNI/tau-lang/issues/197) | Witness table, semantic lead and patch; cases adopted, broader cell rule excluded. | [Outcome](https://github.com/IDNI/tau-lang/issues/197#issuecomment-5940898869); [30c40849](https://github.com/IDNI/tau-lang/commit/30c40849393033545d89d38474f9f46f7308baee) |

</details>

## Other closed and open work

- [#46][duplicate] was identified as the same left-shift issue as #42; excluded
  from the fix total.
- [#192][contract] clarified demand-driven file-input consumption. Upstream
  kept existing behavior; excluded from the fix total.

The seven open proposals are preserved as pending work:

- [#151](https://github.com/IDNI/tau-lang/issues/151) — Prune contradictory clauses during quantifier-elimination distribution.
- [#152](https://github.com/IDNI/tau-lang/issues/152) — Fold same-type disequation alternatives before CQE distribution.
- [#180](https://github.com/IDNI/tau-lang/issues/180) — Reuse existing miniscoping before public API quantifier elimination.
- [#182](https://github.com/IDNI/tau-lang/issues/182) — Use graph propagation for closed modular bit-vector sum equations.
- [#184](https://github.com/IDNI/tau-lang/issues/184) — Bounded BDD decision reduces time on quantified bit-vector examples.
- [#191](https://github.com/IDNI/tau-lang/issues/191) — Search-limit help and API comments still describe an undecided result as unsatisfiable.
- [#199](https://github.com/IDNI/tau-lang/issues/199) — Reuse translated bit-vector expressions across concrete VM steps.

## Replay and disclosure

For each row, the commit diff identifies the changed implementation and tests,
and the outcome gives the recorded validation scope. One fixed-revision
qualification route, after the [pinned build prerequisites][build], is:

```bash
git clone https://github.com/IDNI/tau-lang.git tau-evidence
cd tau-evidence
git checkout --detach 30c40849393033545d89d38474f9f46f7308baee
git submodule update --init --recursive
./dev preset release-tests run
```

The [#197 regression source][tests197] is pinned to that patched revision.
No native Tau build or test suite was run for this ledger audit.

This compilation used Codex (A mode). The historical issue bodies do not
consistently disclose AI tools or the human/AI task split; no unaided claim or
invented per-issue attribution is made. The public comments, commits and test
sources support upstream impact. No ledger score, proctored assessment,
whole-language correctness claim, or `externally-verified` receipt is assigned.

Independent research is indexed separately in [Tau research](../TAU-RESEARCH/README.md).

[search]: https://github.com/IDNI/tau-lang/issues?q=is%3Aissue%20author%3ATheDarkLightX
[r139]: https://github.com/IDNI/tau-lang/issues/139#issuecomment-5822467539
[r135]: https://github.com/IDNI/tau-lang/issues/135#issuecomment-5822465981
[r134]: https://github.com/IDNI/tau-lang/issues/134#issuecomment-5822465423
[r197]: https://github.com/IDNI/tau-lang/issues/197#issuecomment-5940898869
[r193]: https://github.com/IDNI/tau-lang/issues/193#issuecomment-5934551146
[duplicate]: https://github.com/IDNI/tau-lang/issues/46#issuecomment-3650235315
[contract]: https://github.com/IDNI/tau-lang/issues/192#issuecomment-5890334715
[build]: https://github.com/IDNI/tau-lang/blob/30c40849393033545d89d38474f9f46f7308baee/README.md#compiling-the-source-code
[tests197]: https://github.com/IDNI/tau-lang/blob/30c40849393033545d89d38474f9f46f7308baee/tests/repl/commands/test_repl-normalize_cmd.cmake
