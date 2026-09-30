# Upstream Target: Apalache #3477 — Function-set equality

Status: **live upstream correctness target**

Upstream issue: https://github.com/apalache-mc/apalache/issues/3477

## Why this target

This is not a cosmetic contribution. It is a semantic soundness bug in the equality encoding for finite function sets.

The current `LazyEquality.mkFunSetEq` reduces

```text
[S1 -> T1] = [S2 -> T2]
```

to equality of both domains and codomains. That is too strong in two degenerate cases.

The TLAPS characterization supplied by the upstream maintainer is:

```tla
([S1 -> T1] = [S2 -> T2]) <=>
  \/ (S1 = {} /\ S2 = {})
  \/ (S1 # {} /\ S2 # {} /\ T1 = {} /\ T2 = {})
  \/ (S1 = S2 /\ T1 = T2)
```

Interpretation:

1. Empty domains produce the singleton set containing the empty function, regardless of codomain.
2. Nonempty domains with empty codomains produce the empty function set, regardless of domain.
3. Otherwise the ordinary domain-and-codomain equality rule applies.

This maps well to a deterministic-oracle review style: the semantic oracle is the extensional definition of a function set, and the implementation can be checked against the three exhaustive cases.

## Exact implementation surface

File:

```text
tla-bmcmt/src/main/scala/at/forsyte/apalache/tla/bmcmt/LazyEquality.scala
```

Method:

```scala
private def mkFunSetEq(...)
```

Current rule:

```text
funSetEq <=> domEq && cdmEq
```

Proposed rule:

```text
dom1Empty && dom2Empty
OR
!dom1Empty && !dom2Empty && cdm1Empty && cdm2Empty
OR
domEq && cdmEq
```

The emptiness predicate should be generated from the arena's potential elements and membership guards, not from `getHas(...).isEmpty` alone, because a symbolically empty set may still have arena elements guarded by false membership conditions.

For a finite set cell `s` with potential elements `e_i`:

```text
Empty(s) := AND_i NOT(e_i \in s)
```

with the empty conjunction equal to `TRUE`.

## Regression tests

Extend:

```text
tla-bmcmt/src/test/scala/at/forsyte/apalache/tla/bmcmt/TestSymbStateRewriterFunSet.scala
```

Minimum cases:

```tla
[{} -> {1}] = [{} -> {2}]       \* TRUE
[{1} -> {}] = [{2} -> {}]       \* TRUE
[{} -> {1}] # [{1} -> {}]       \* TRUE
[{1} -> {1}] # [{2} -> {1}]     \* TRUE
```

Add at least one symbolic-emptiness case using an `IF guard THEN {} ELSE {1}` domain/codomain so the fix is not accidentally limited to syntactically empty sets.

## Contribution standard

A strong upstream submission should include:

- smallest semantic change in `mkFunSetEq`;
- regression tests for all three theorem disjuncts;
- a symbolic emptiness case;
- no new public abstraction unless repeated use justifies it;
- issue reference `Fixes #3477`;
- explanation that the implementation mirrors the already-posted TLAPS theorem.

## Evidence value

This contribution demonstrates:

- semantic debugging by reducing implementation behavior to a formal case split;
- independent deterministic oracle construction;
- awareness of symbolic-vs-static emptiness;
- high-assurance test design;
- ability to turn a formal theorem into a narrowly scoped production patch.

It is therefore a stronger hiring signal than a broad documentation or formatting PR.
