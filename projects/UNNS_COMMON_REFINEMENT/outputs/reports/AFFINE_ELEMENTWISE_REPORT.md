# Affine Elementwise Route-Closure Report

## Result

The retained higher-rank affine controls have now been classified elementwise.

The queued question was whether the rank-one pattern

`finite non-primal core -> cofinal all-primal tail`

survives when independent atomic relations appear in higher rank.

It does not in any of the four retained affine failure controls.

## Exact classifications

- `NORMAL_PARITY`:
  - primal: `0` and `(2m,2n)` with `m,n>=1`;
  - non-primal: both boundary rays and the entire odd-odd congruence class.

- `NORMAL_CONE2`:
  - primal: `0` and points with `y` even, `y>=2`, `2x-y>=2`;
  - non-primal: both cone facets and every odd-`y` interior point.

- `NONNORMAL_2D`:
  - primal: `0` and `(2m,n)` with `m>=1,n>=2`;
  - non-primal: every odd-`x` point, the vertical axis, and the `y=0,1` even strips.

- `NORMAL_SQUARE3`:
  - primal: exactly `k(1,1,2)` for `k>=0`;
  - non-primal: every point off that central ray.

The three free controls remain all-primal.

## Exact conclusion

All four affine failure controls have an infinite, unbounded non-primal locus.
Therefore there is no higher-rank analogue, in this retained control corpus, of a scalar conductor
threshold beyond which route traceability becomes universal.

This is stronger than simply restating `ARD>0 -> global failure`: it identifies where the failure
lives elementwise and shows that the obstruction can propagate arbitrarily far through the monoid.

## Geometry of persistence

Three mechanisms are distinguished:

1. **congruence persistence** — `NORMAL_PARITY` / `NORMAL_CONE2`;
2. **lattice-hole persistence** — `NONNORMAL_2D`;
3. **non-simplicial relation persistence** — `NORMAL_SQUARE3`.

In the first three rank-2 controls, the primal locus still has full group rank, but only half of the
monoid survives asymptotically under the natural exhaustions used in the proof note.

In `NORMAL_SQUARE3`, the primal locus drops from ambient group rank 3 to rank 1; under grade
exhaustion its relative density tends to zero.

## Reproducibility

Generated files:

- `04_PROOF_MAP/output/AFFINE_ELEMENTWISE_PROFILE.md`
- `04_PROOF_MAP/output/AFFINE_ELEMENTWISE_SUMMARY.csv`
- `04_PROOF_MAP/output/AFFINE_UNBOUNDED_CERTIFICATES.csv`
- `outputs/records/AFFINE_ELEMENTWISE_RESULT.json`
- `scripts/BUILD_AFFINE_ELEMENTWISE.py`

The script records the exact proved formulas and validates 748 concrete instances of the parametric
non-refinement certificate families.  These finite checks are regression tests only; the exact
classifications are proved algebraically in `AFFINE_ELEMENTWISE_PROFILE.md`.

## Conway / UNNS consequence

The finite comparison now separates two ideas that previously looked similar:

- **rank-one saturation:** move beyond a finite gap obstruction;
- **global relation control:** prevent unbounded defect channels from surviving.

The omnific candidate proof must accomplish the second, not merely a transfinite version of the
first.  Its base primality + quotient refinement + strict descent + transport architecture is
therefore structurally stronger than a conductor-tail mechanism.

## Next theorem target

The control results suggest, but do not yet prove, the general statement:

`rank(H)>=2 and ARD(H)>0 -> the non-primal locus is unbounded`.

That is now the next exact mathematical question.
