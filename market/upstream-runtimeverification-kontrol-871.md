# Upstream Target: Runtime Verification Kontrol #871 — stale lemma copies

Status: **live upstream correctness target**

Upstream issue: https://github.com/runtimeverification/kontrol/issues/871

## Finding

The open issue reports that updated lemmas are not picked up by a normal `kontrol build`; users need `--regen --rekompile`.

The current implementation in:

```text
src/kontrol/kompile.py
```

explains the failure mode.

Required K files are copied into the generated `requires/` directory only when:

```python
if regen or not req_path.exists():
    shutil.copy(req, req_path)
    regen = True
```

Later, the kompilation digest is computed from the **source** required files:

```python
k_files = list(options.requires) + [foundry.main_file]
```

So when a lemma source changes:

1. the source digest changes;
2. `should_rekompile()` correctly decides recompilation is needed;
3. but the pre-existing generated `requires/<lemma>` copy was never refreshed;
4. `foundry.k` continues to require the stale generated copy;
5. recompilation therefore recompiles stale lemma content.

This creates a split-brain cache invariant: the freshness oracle hashes one artifact while the compiler consumes another.

## Minimal patch

The copy predicate should detect content drift between each source required file and its generated copy.

Conceptually:

```python
requires_changed = (
    not req_path.exists()
    or req.read_bytes() != req_path.read_bytes()
)

if regen or requires_changed:
    shutil.copy(req, req_path)
    regen = True
```

A hash comparison is also reasonable if maintainers prefer not to compare bytes directly. The important invariant is:

```text
digest input for required K file == bytes consumed by kompilation
```

before the freshness decision is committed.

## Regression test

A targeted integration/unit test should:

1. create a temporary Foundry/Kontrol project with an auxiliary required K lemma;
2. build once;
3. change only the lemma source, leaving Solidity/contracts unchanged;
4. invoke normal build without `--regen` or `--rekompile`;
5. assert the generated `requires/<lemma>` bytes equal the new source;
6. assert the kompilation digest changes;
7. ideally verify the resulting definition/proof behavior observes the new lemma.

The strongest test uses two lemma bodies whose observable proof result differs. That prevents a test from passing merely because timestamps or digest metadata changed.

## Why this is a strong contribution

This is a high-assurance build correctness bug rather than a cosmetic cache bug. A verification tool that silently compiles stale proof lemmas can produce evidence about a different specification than the source tree the reviewer thinks was checked.

The underlying engineering pattern is directly reusable:

```text
freshness oracle must hash the exact artifact consumed by the verifier
```

This is a natural FCIS / deterministic-oracle contribution and a good Runtime Verification signal.

## Proposed PR scope

Keep the upstream patch deliberately small:

- refresh copied required K files on content drift;
- add a regression test covering lemma-only edits;
- avoid unrelated build refactors;
- PR body: `Fixes #871`;
- explain the stale-copy/source-digest mismatch in four or five lines.

## Permission boundary

The connected GitHub integration can inspect Runtime Verification's public repository but cannot write to it. Once a writable fork is connected, this patch is ready to implement and submit.
