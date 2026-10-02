# Verus #3016 — Preserve source types in SpecFn lambda values

**Dana Edwards / TheDarkLightX · A — AI-augmented · merged upstream · unscored**  
Evidence checked: 2026-10-02.

Contributed a targeted Rust verifier fix and three regression tests, accepted in
[Verus PR #3016][pr]. Demonstrates source-type/SMT-encoding reasoning, regression
design, and a scoped upstream contribution.

## Problem and contribution

[Issue #3010][issue] reported that erasing closure parameter types could conflate
distinct source-level function values and admit invalid proofs. The patch carries
the source `SpecFn` type in the wrapper and replaces unconditional wrapper identity
with application agreement restricted to valid inputs. It also adjusts the
constructor-typing and function-height encoding. See the [four-file diff][commit]
and [regression tests][tests].

**Merge:** 2026-10-02 at 00:05:51 UTC, commit
[`919a72b358e996b8818959a06e781234c45d4d52`][commit], into upstream
`spec-fn-lambda-type-soundness`. This records that branch's acceptance; it does not
assert inclusion in `main` or a release. The PR addresses #3010; the issue was
still open when checked.

## Validation

[Upstream CI][ci] for PR head `b174ec84294ea1c304c176f4671a210c0bc9fde3`
records **PASS** for all three additions in `rust_verify_test::closures`:

- `spec_fn_lambda_parameter_type_soundness_3010`
- `spec_fn_lambda_parameter_type_quantifier_soundness_3010`
- `spec_fn_lambda_parameter_type_valid_3010`

The first two check rejection of invalid proofs; the third preserves valid
generic, zero-argument, and multi-argument closure use. CI tested the PR's
temporary merge, not the final squash-merge SHA.

The same full-test job remained **failed**: 804 passed, one failed, and 3,810 of
4,615 tests were not run because of fail-fast. The failure was
`examples_guide_assert_by_compute`. [Chris Hawblitzel clarified][clarification]
that the example used the wrong `spec_fn` closure to trigger a lemma. This
supports attributing that failure to the example, not this patch; it does not
turn the CI result into a full-suite pass.

## Replay the fixed revision

For Bash on Linux/macOS with Git and a recent rustup, follow the pinned
[build prerequisites][build] and [test instructions][contributing]. This selects
the **patched** revision (Rust 1.98.1; Z3 4.16.0):

```bash
set -eo pipefail
git clone https://github.com/verus-lang/verus.git verus-3016
cd verus-3016
git checkout --detach 919a72b358e996b8818959a06e781234c45d4d52
rustup toolchain install
cd source
./tools/get-z3.sh
source ../tools/activate
vargo build --release
vargo test --release -p rust_verify_test --test closures spec_fn_lambda_parameter_type_
```

Expected: all three selected tests pass, including the two expected-rejection
tests. This is a source-pinned replay recipe, **not a fresh local replay
attestation**. The upstream CI log is the recorded execution evidence.

## AI disclosure and limits

The upstream PR discloses `Assisted-by: OpenAI Codex Sol`. The public record does
not establish a detailed human/AI task split or unaided performance. This ledger
summary was prepared with Codex from the linked sources; it adds no candidate
review or live-defense attestation.

No benchmark score or `externally-verified` receipt is assigned: the existing
[receipt validator][validator] requires a score of at least 80 for that status.
Upstream acceptance and scoped test results are the evidence, not a proof of
whole-verifier soundness or a general competence certification.

[pr]: https://github.com/verus-lang/verus/pull/3016
[issue]: https://github.com/verus-lang/verus/issues/3010
[commit]: https://github.com/verus-lang/verus/commit/919a72b358e996b8818959a06e781234c45d4d52
[tests]: https://github.com/verus-lang/verus/blob/919a72b358e996b8818959a06e781234c45d4d52/source/rust_verify_test/tests/closures.rs#L149-L208
[ci]: https://github.com/verus-lang/verus/actions/runs/36812241773/job/110627554719
[clarification]: https://github.com/verus-lang/verus/pull/3016#issuecomment-5942934092
[build]: https://github.com/verus-lang/verus/blob/919a72b358e996b8818959a06e781234c45d4d52/BUILD.md
[contributing]: https://github.com/verus-lang/verus/blob/919a72b358e996b8818959a06e781234c45d4d52/CONTRIBUTING.md#running-tests-for-the-rust-to-vir-translation-and-inspecting-the-resulting-virairsmt
[validator]: ../../verifiers/validate_receipt.py
