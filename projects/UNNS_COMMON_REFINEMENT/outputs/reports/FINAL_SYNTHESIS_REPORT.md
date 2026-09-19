# Final Synthesis Report

## Result

The project now separates the Conway/UNNS question into two exact layers.

### Algebraic invariant

`global four-factor refinement <=> every element primal`

in the relevant cancellative commutative setting.

### Mechanism-level sufficient principle

A new narrow proposition has been proved:

`primal base + exact ambient routed block + strictly lower well-founded residual rank`

`=> every element primal => four-factor refinement`.

This is recorded in:

`05_UNNS/definitions/ROUTE_CLOSURE_INDUCTION.md`.

## Cross-regime result

- Positive integers eliminate the potential route defect immediately by gcd/coprime routing; the residual may be taken as the unit.
- Rank-one failure systems have a finite non-primal obstruction core but a cofinal primal tail.
- Higher-rank affine failure systems with `ARD>0` contain a persistent non-primal affine ray.
- The audited Conway candidate mechanism repairs an occupied support-class block, forces the unresolved residual to strictly smaller support-class order type, terminates in a finite-class primal base, and reconstructs the result in the ambient structure.

## Final interpretation

The surviving property is **primal/pre-Schreier factor traceability**.

The cross-regime UNNS contribution is not to rename that property, but to isolate the difference
between:

`finite residual defect`,

`persistent rank-preserving defect propagation`, and

`exact repair with forced well-founded residual descent`.

This directly answers the original project question without reviving the superseded generic SRS/PDS
abstraction branch.

## Scope

The route-closure induction proposition is sufficient, not claimed necessary.
The Conway realization remains source-locked to commit
`264445c93b78554c408e99e4e7f663693b4e91ab` and depends on the concrete hypotheses audited in the
source-level documents.
