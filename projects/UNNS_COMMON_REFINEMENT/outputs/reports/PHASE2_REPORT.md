# PHASE 2 RESULT — NON-REFINEMENT CONTROLS

## Exact flagship result

Use the additive monoid

`H=<2,3>={0,2,3,4,5,...}`

and its multiplicative monomial realization

`M_H={X^n:n∈H}`.

Then

`2+4=3+3=6`

so

`X^2·X^4 = X^3·X^3 = X^6`.

The complete ambient `N` witness list is:

1. `(0,2,3,1)`
2. `(1,1,2,2)`
3. `(2,0,1,3)`

Every witness uses the missing exponent `1`. Hence no witness lies entirely in `H`.

**Verdict: `D_R=1`.**

## Repair test

Adjoin `1`, so `<1,2,3>=N`.

The same equality becomes refinable immediately. Thus the failure is not endpoint equality; it is missing internal splitting capacity.

## Cross-system scan

Systems tested: **8**

Systems with an exact counterexample in the bounded search: **5**

Systems with no counterexample in the same search window: **H246, H369, N**

The no-failure controls include scaled free monoids, showing that "missing ambient integers" alone is not the operative criterion.

## Structural result

Phase 2 isolates a concrete defect:

`endpoint equality + insufficient splitting closure -> D_R=1`.

A useful diagnostic is the **blocking-hole set**: values that are absent from the monoid and required by every ambient refinement witness.

For the flagship `<2,3>` system:

`blocking holes = {1}`.

## Interpretation for UNNS

This gives the first exact instance of:

`same endpoint` but `no common structural ancestry`.

It is therefore a clean algebraic model of route-closure failure / stitching defect.

## Next question

Determine whether the operative ingredient is best formalized as:
- saturation relative to the generated group,
- residual closure,
- decomposition closure,
- or a more general refinement/interpolation property.

Phase 3 should not yet jump to omnific integers until this distinction is resolved.
