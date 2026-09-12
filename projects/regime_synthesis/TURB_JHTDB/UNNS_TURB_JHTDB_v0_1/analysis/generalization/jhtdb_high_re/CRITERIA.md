# JHTDB High-Re Spatial Generalization — Criteria v0.1

## Primary samples

- `isotropic8192`: snapshots `0..4`, central native-grid `256^3` cube.
- `isotropic32768`: snapshot `0`, central native-grid `256^3` cube.

## Prespecified contrast

- `isotropic8192`: snapshot `5` (`Re_lambda ~610`), same cube.

## Quality gates

A sample is analyzable only if:

1. source HDF5 SHA-256 is recorded;
2. velocity shape is exactly `[256,256,256,3]` in `zyxc` order;
3. coordinate arrays have length `256` on every axis and isotropic spacing;
4. scale factors `[1,2,4,8,16]` all divide the cube dimensions;
5. at least one eligible scale relation exists;
6. the 100-null ensemble has mean mobility `>=0.01`, unique-graph fraction `>=0.10`, and real-match fraction `<=0.90`.

## Primary classification labels

`PILOT_A_SCALE_REGIME_RECURRENCE`:

- >=4/5 of isotropic8192 high-Re snapshots are STRUC-I `Structural Instability / Random Structure`; and
- isotropic32768 is also `Structural Instability / Random Structure`.

`HIGH_RE_SCALE_STABILIZATION`:

- >=4/5 of isotropic8192 high-Re snapshots are STRUC-I `Geometric Persistence`; and
- isotropic32768 is also `Geometric Persistence`.

`MIXED_HIGH_RE_SCALE_REGIME`:

- neither primary pattern is satisfied, with all required samples analyzable.

`UNDERRESOLVED`:

- one or more required primary samples fail quality gates in a way that prevents classification.

## Canonical chamber handling

- STRUC-I: 2,000 MC; rerun at 10,000 MC iff mean A_kappa is within 0.01 of a regime boundary.
- STRUC-PERC-I: report all outputs; treat connectivity as inferential only when gap vertices >=100 after exact-value deduplication.
- Giant ratio >=0.95 is the prespecified giant-component support threshold.
