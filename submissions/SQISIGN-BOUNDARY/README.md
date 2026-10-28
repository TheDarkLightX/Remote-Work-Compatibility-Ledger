# SQIsign — Cryptographic implementation security research

**Dana Edwards / TheDarkLightX · Published research · Unscored**

Evidence checked: **2026-10-28**.

**Capability:** Post-quantum cryptographic implementation security research:
reproducible analysis of signature-verification boundaries, sanitizer testing,
API contract enforcement, candidate-repair evaluation, and responsible disclosure.

The [August 2026 publication and artifacts][release] document two implementation
problems at [`dd133d7aca576c361a270c8e6434832535b42ecc`][original-source]:
undersized inputs reached fixed-size signature decoding, and overlong detached
signatures were accepted despite the intended exact-length contract.

## Evidence and attribution

- **Original study — Dana Edwards:** 2,656 tested undersized calls produced
  AddressSanitizer findings; candidate guards converted them to clean
  rejections. All 1,200 tested detached suffix aliases were rejected after
  the candidate repair, while all 600 exact KAT signatures remained accepted.
  These are the original publication's results at its pinned revision.
- **Corrections — SQIsign team:** as recorded in [official issue #23][issue],
  the team had independently developed equivalent private guards before
  receiving the report. That private source was not audited. Public Round 3,
  tag `nist-v3` at [`6d017708db403bf83977fa70770fc4f7f9e9ff21`][round3-source],
  rejects detached inputs unless `siglen == SIGNATURE_BYTES`, and signed
  messages when `smlen < SIGNATURE_BYTES`, before decoding. `open` treats
  bytes after the signature as the message.
- **Independent C validation — yui9696:** [reported][c-report] 300/300 valid
  detached signatures and 300/300 valid signed messages accepted, with all
  4,200 negative cases rejected across three parameter sets. A smaller ASan
  campaign reported no findings; disabling the detached-length guard produced
  a heap-buffer-overflow in a control case. These are third-party measurements,
  not new tests by Dana or executions for this capability entry.
- **Independent Rust implementation — trancee:** [documented][rust-report]
  exact signature and public-key length checks before decoding, with
  [regression tests][rust-tests] across all three parameter levels at
  `c52ab76c7d4e336572f8364d3e1d672c4a04f5c6`. This is a separately developed
  implementation, not code authored by Dana.

## Reviewer path and limits

Start with the [published preprint and evidence archive][release], then inspect
the [frozen replay transcript][transcript], [harness material][harness], and
[asset hashes][hashes]. The two comments above supply the later independent
reports; the C comment does not include a standalone harness or complete raw
run log. The [versioned Round 3 addendum][addendum] records the later source
revision, guard behavior, full case breakdown, and reproducibility limits.

The work supports implementation-security and research capabilities. It does
not establish a mathematical weakness in SQIsign, forgery, key recovery,
remote code execution, a SUF-CMA break, or universal parser safety. It does not
claim authorship of the team's independent corrections or the Rust port.

**AI and validation disclosure:** OpenAI Codex prepared this capability entry
and checked its sources and attribution. The linked original publication is
the authority for the historical experiments. This entry adds no runtime
test results, benchmark score, unaided/proctored claim, or external-certification
receipt. The capability's A/V modes describe assisted work and verification;
Git history alone is not evidence of unaided authorship.

This records existing research evidence. [EVAL-001 remains the active
training goal](../../CURRENT.md).

[release]: https://github.com/TheDarkLightX/sqisign-verification-boundary/releases/tag/v0.1.0
[original-source]: https://github.com/SQISign/the-sqisign/blob/dd133d7aca576c361a270c8e6434832535b42ecc/src/sqisign.c
[issue]: https://github.com/SQISign/the-sqisign/issues/23
[round3-source]: https://github.com/SQISign/the-sqisign/blob/6d017708db403bf83977fa70770fc4f7f9e9ff21/src/sqisign.c#L80-L133
[c-report]: https://github.com/SQISign/the-sqisign/issues/23#issuecomment-5506722786
[rust-report]: https://github.com/SQISign/the-sqisign/issues/23#issuecomment-6468164363
[rust-tests]: https://github.com/trancee/the-sqisign/blob/c52ab76c7d4e336572f8364d3e1d672c4a04f5c6/rust/crates/sqisign/tests/verify_reject.rs#L88-L118
[transcript]: https://github.com/TheDarkLightX/sqisign-verification-boundary/blob/v0.1.0/artifact/evidence/command-transcript.log
[harness]: https://github.com/TheDarkLightX/sqisign-verification-boundary/blob/v0.1.0/artifact/evidence/harness-material.tar
[hashes]: https://github.com/TheDarkLightX/sqisign-verification-boundary/blob/v0.1.0/SHA256SUMS
[addendum]: https://github.com/TheDarkLightX/sqisign-verification-boundary/blob/8039f3c0544ac44954c696d41ad9415aea28b734/addenda/round-3-validation-v0.2.0.md
