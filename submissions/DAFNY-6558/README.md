# Dafny #6558 — Prove numeric conversion round trips

**Dana Edwards / TheDarkLightX · A — AI-augmented · merged upstream · unscored**

Evidence checked: 2026-10-27.

Added reusable proofs that formatting then parsing a number returns the original
value, accepted in [Dafny PR #6558][pr]. Demonstrates contract design, inductive
proofs, compatibility judgment, response to maintainer review, and measurement
of solver resource use. Conversion algorithms were unchanged.

**Acceptance:** authored by TheDarkLightX; [approved by fabiomadge][approval]
and merged into upstream `master` on **2026-10-25 at 11:39:21 UTC**, commit
[`de36f2ec1f9c530080eff7929ae28229f45da069`][merge]. The merge credits
Fabio Madge as co-author. This records upstream acceptance, not release inclusion.

## Problem, contracts, and proof design

[Issue #4795][issue] identified a specification gap: the underlying
`LittleEndianNat` library proved numeric round trips, but `Strings` did not
expose the corresponding guarantees to callers. The [merged source][source]
and [usage examples][examples] add:

| Contract | Conditions and parsing guarantees |
| --- | --- |
| `ToNat(OfNat(n)) == n` for every `n: nat` | Generated characters satisfy the parser's digit predicate. |
| `ToInt(OfInt(i)) == i` for every `i: int` | Generated output is not a bare minus sign; the existing `OfInt` postcondition supplies `IsNumberStr`. |
| Generic alphabet round trips | Base `|chars| > 1`; require `DigitCharsConsistent()`: for every valid index `d`, `chars[d]` is mapped and `charToDigit[chars[d]] == d`. Parsing aliases remain allowed. |
| Generic/hexadecimal signed round trips | Additionally require `minus !in charToDigit`; decimal wrappers discharge the conditions for `'-'`. |

The proof proceeds from digit sequences (`LemmaOfDigitsToNat`, explicit
recursion on the tail), through naturals (reuse `LemmaNatSeqNat`, with a zero
case), to integers (split on sign). Decimal and hexadecimal wrappers establish
the alphabet premise. Hexadecimal `CharsConsistent()` now has a proof in place
of its previous axiom. A binary refinement demonstrates premise discharge.

## Maintainer feedback and compatibility

fabiomadge [proposed strengthening `CharsConsistent()`][proposal] to reduce API
duplication, and suggested shorter proofs, fewer isolation attributes, and a
usage lemma instead of redundant runtime tests. Those proof/example
simplifications were incorporated.

The [author's boundary diagnostic][boundary] showed why the stronger law was
not silently added: `chars = "00"` with `map['0' := 0]` satisfies the old
character law but fails the indexed digit law. Strengthening the public contract
would impose new obligations on external refinements; the review also identified
an existing JSON alphabet/axiom issue requiring separate work. The final design
keeps the new premise explicit. fabiomadge [accepted deferring the contract
change][accepted] and then approved the PR.

## Reported validation and resource improvements

The [PR report][pr] and [proof][proof-results]/[example][example-results] review
replies report checks of
[`16f82c91df5e400c9f95fab05739635665bd9589`][tested], using checkout-built
**Dafny 4.11.1+b3324a3, Z3 4.16.0, .NET SDK 8.0.408, Linux**.
GitHub blob identities confirm that `Strings.dfy`, `StringsExamples.dfy`, and
the core `.doo` package match the final merge; the [last PR commit][last]
changed documentation only. These are reported executions, not new local replays.

| Completed scope | Reported result |
| --- | --- |
| Focused Strings, seeds 0–9 | **550/550 assertion batches**; peak 555,132 resources, limit 5,000,000. |
| Package-backed examples/refinement, seeds 0–9 in fresh processes | **130/130 batches**; peak 194,774, limit 1,000,000; warnings enabled. |
| Verified core package generation | **2,347 verified units, zero errors**; 7,963 passed CSV batches. Six target-specific packages also verified and matched their checked-in unpacked contents. |
| Focused runtime tests | **40 successful executions**: eight existing tests each on Python, JavaScript, Go, Java, and C#; C# workaround below. |
| Contract boundary and documentation | Repeated-character refinement and `!DigitCharsConsistent()` verified; a generic lemma call without its premise was rejected. Markdown example, formatting, and diff checks passed. |

Median **total verification resource counts per seed**, comparing inspected
[`b3324a3ba77803d3ff5daa22d876b639bcc1147f`][baseline] with the tested revision:

| Scope | Before | After | Reduction |
| --- | ---: | ---: | ---: |
| Strings | 3,565,984.5 | 3,181,073.5 | **10.8%** |
| Focused examples | 5,457,251.5 | 766,086 | **86.0%** |

The same ten seeds and unchanged limits were used. These are solver-resource
measurements across revised proofs/examples, including removal of redundant
tests and isolation attributes; they are not wall-clock speedups, runtime
performance claims, or an independently scored benchmark.

## Replay, AI disclosure, and limits

See [REPLAY.md](REPLAY.md) for the pinned checkout, build prerequisites, seeded
verification, package checks, runtime commands, expected outcomes, and resource
aggregation method. This entry validates source references and evidence
consistency; it does **not** attest that those Dafny checks were rerun here.

**AI disclosure:** AI generated the code. Dana reviewed the generated code and
Fabio Madge's additions, accepted selected changes, and directed the AI to follow
the maintainer's preferences and repository conventions. This workflow account
is supplied by Dana; OpenAI Codex prepared this case study and replay recipe.

- Package generation is a different command path from full `make verify`.
  Its CSV included a 33,732,720-resource peak in an unchanged Base64 proof;
  it does not establish a bounded full-library verification pass.
- `dafny test -t:cs` encountered a nested SDK `Process.GetStat` failure.
  Directly building the generated C# project succeeded with 51 warnings and
  zero errors; running its assembly passed the eight tests.
- Full compiler integration and language-server suites were not run. The
  earlier `make verify` remained interrupted; historical 716/303 execution
  counts and the earlier multi-mutation warning diagnostic are not final-revision
  passes. The pre-existing JSON issue was not fixed by this contribution.
- No benchmark score, external certification, or `externally-verified` receipt
  is assigned. Acceptance and scoped results do not certify whole-system
  soundness or general competence. [EVAL-001 remains the active goal][current].

[pr]: https://github.com/dafny-lang/dafny/pull/6558
[issue]: https://github.com/dafny-lang/dafny/issues/4795
[merge]: https://github.com/dafny-lang/dafny/commit/de36f2ec1f9c530080eff7929ae28229f45da069
[source]: https://github.com/dafny-lang/dafny/blob/de36f2ec1f9c530080eff7929ae28229f45da069/Source/DafnyStandardLibraries/src/Std/Strings.dfy
[examples]: https://github.com/dafny-lang/dafny/blob/de36f2ec1f9c530080eff7929ae28229f45da069/Source/DafnyStandardLibraries/examples/StringsExamples.dfy
[proposal]: https://github.com/dafny-lang/dafny/pull/6558#discussion_r4230772973
[boundary]: https://github.com/dafny-lang/dafny/pull/6558#discussion_r4369221565
[accepted]: https://github.com/dafny-lang/dafny/pull/6558#discussion_r4370628304
[approval]: https://github.com/dafny-lang/dafny/pull/6558#pullrequestreview-5642922765
[proof-results]: https://github.com/dafny-lang/dafny/pull/6558#discussion_r4369224993
[example-results]: https://github.com/dafny-lang/dafny/pull/6558#discussion_r4369225823
[tested]: https://github.com/dafny-lang/dafny/commit/16f82c91df5e400c9f95fab05739635665bd9589
[baseline]: https://github.com/dafny-lang/dafny/commit/b3324a3ba77803d3ff5daa22d876b639bcc1147f
[last]: https://github.com/dafny-lang/dafny/commit/27e41b755fec3899324c162574d96d39d9ac8e5a
[current]: ../../CURRENT.md
