# Primality–Refinement Result Report

## Result

For the commutative cancellative systems used in this project:

```text
x primal
iff
all endpoint equalities containing x are 2x2-refinable.
```

Therefore:

```text
D_R=1 equality
=> every one of its four corner positions is non-primal.
```

Conversely, every non-primal element occurs as a corner of some `D_R=1` equality.

## Corpus conversion

`FAILURE_CERTIFICATES.csv` was generated reproducibly from the already-established failure corpora.

- rank-one canonical failures: **513**
- positive-affine explicit failures: **4**
- total exact failure certificates: **517**

Every retained row is an exact no-refinement equality and therefore certifies non-primality at all four corner positions.

## Significance for the Conway comparison

This localizes the common structural property identified in `CONWAY_STRUCTURAL_SPINE.md`.

Global route closure is not only equivalent to every-element primality at the monoid level. Element by element, primality is exactly the statement that no endpoint equality involving that element can generate a refinement defect.

The next project question is therefore local and concrete:

> How is primal/non-primal route traceability distributed inside systems that fail global refinement, and what mechanism drives that distribution to all-primal in the omnific candidate proof?

No new SRS/PDS unification is needed for this step.
