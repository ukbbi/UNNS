# Refinement Plan

## 1. Purpose

The central claim of this project is not merely that a structural boundary appears, but that it **survives refinement**.

A candidate vacuum boundary is therefore not accepted on a single grid, lattice spacing, operator basis, or ladder length.

## 2. Refinement axes

The project distinguishes several independent refinement axes.

### R1 — Lattice-spacing refinement

\[
a_1 > a_2 > a_3 > \cdots \rightarrow 0.
\]

This is the primary continuum-oriented refinement axis.

### R2 — Physical-volume refinement

Increase physical volume or compare volumes at matched lattice spacing to separate finite-volume effects from vacuum-boundary behavior.

### R3 — Ladder-resolution refinement

Increase the number of ordered samples or use nested sampling sets while preserving the same physical observable and interval.

### R4 — Operator-basis refinement

For correlator/spectral data, compare compatible gauge-invariant operators or variational bases that target the same physical channel.

### R5 — Representation refinement

Compare different but physically linked gauge-invariant representations, for example:

- correlator vs effective-mass ladder;
- Wilson-loop vs static-force representation;
- profile vs integrated profile coordinate.

## 3. Common-refinement logic

Whenever two ladder encodings resolve the same underlying observable on different grids, define a common refinement that preserves the original sample points where possible.

The test is not whether interpolated numbers become identical. It is whether the canonical structural classification and the inferred vacuum-boundary behavior are compatible after both ladders are represented on a common refinement.

## 4. Precedence rule

Refinement transformations must be defined **before** inspection of whether they improve the desired structural separation.

If more than one mathematically reasonable interpolation/aggregation method exists, all preregistered methods are retained and compared.

## 5. Boundary tracking

For each refinement level `r`, estimate a boundary coordinate `b_r` in the chosen physical gap proxy or adversarial control parameter.

The strong pattern is one of:

- convergence: `b_r -> b_* > 0`;
- stable plateau: `b_r` remains bounded away from zero within uncertainty;
- conservative lower bound: `inf_r b_r > 0` over the validated refinement range.

The following patterns count against the strong hypothesis:

- `b_r -> 0`;
- monotone erosion with increasing refinement;
- sign/classification reversals without convergence;
- dependence on one arbitrary interpolation choice.

## 6. Physical-branch control

At every refinement level used for the gapless adversary, run the matched physical branch through the identical pipeline.

If both branches destabilize together, the run diagnoses numerical or representational instability rather than vacuum non-crossability.

## 7. Finite-size separation

Whenever data permit, hold the relevant physical scale approximately fixed while changing volume.

A candidate boundary must not be identified with a finite-size spectral floor.

## 8. Uncertainty

Boundary uncertainty should include, where available:

- measurement uncertainty;
- bootstrap/jackknife variation;
- ladder subsampling variation;
- interpolation/refinement variation;
- null-family variation.

The project should report the components separately before combining them.

## 9. Minimum refinement standard for Level B evidence

A Level B result requires:

- at least three ordered refinement levels on one primary axis when available;
- at least one second independent refinement axis;
- matched physical/adversarial processing;
- a frozen canonical chamber;
- explicit boundary-tracking output.

## 10. Continuum extrapolation discipline

A continuum extrapolation is a physical/mathematical model, not a cosmetic curve fit.

Any extrapolation used in YM-3 must specify:

- assumed scaling form;
- fit range;
- uncertainty model;
- sensitivity to excluding coarse levels;
- whether the result is an interpolation or an actual `a -> 0` extrapolation.

The UNNS conclusion must be reported separately from the extrapolation model that supports it.
