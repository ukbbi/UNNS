# TC_RIGIDITY_v001 — Method

## Research question

Does the **geometry and breadth of the closure family across perturbations and
initial states** distinguish MBL-DTC order from ordinary classical period
doubling?

This stage is deliberately allowed to return a negative answer.

## Inputs

The package consumes four already-frozen/reproducible stages:

- `TC_CLOSURE_LOCK_v001`
- `TC_CLOSURE_v001`
- `TC_EXT_MI_v001`
- `TC_CTRL_v001`

Each input may be an extracted folder or a ZIP archive.

## Firewall

Before any rigidity comparison:

1. `TC_CLOSURE_LOCK_v001` is SHA-256 verified.
2. The Mi external-validation output is required to report the same metric SHA.
3. The ordinary-control output is required to report the same metric SHA.

No lower-level closure metric is altered.

Expected frozen metric SHA-256:

`06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553`

## Rigidity vector

No weighted scalar is invented in v001.

Instead the system is represented by a vector:

`R = (C, F, S, U, B)`

where:

### C — closure strength

Frozen closure at the automatically detected recurrence depth q0.

### F — recurrence-family contrast

The frozen family contrast associated with q0.

### S — temporal-order significance

`S = 1 - p_shuffle`

using the frozen 200-surrogate shuffle test.

### U — initial-state universality

For a set of family-contrast values across initial-state pairs/variants:

`U = clip(1 - SD/|mean|, 0, 1)`

This is intentionally scale-free.

For Mi et al., the already exported pairwise MBL and prethermal family-contrast
mean and standard deviation are used.

For an ordinary classical counterexample, v001 adds the deterministic map:

`X_(t+1) = -X_t`

for three very different 20-coordinate initial states.

This is not a time crystal. Every initial state is simply an exact classical
two-cycle.

### B — dimensionless basin-retention geometry

The frozen `plateau_exit_boundary` rule is applied without modification.

Inside the detected basin, family contrast is divided by its seed-baseline and
the perturbation coordinate is rescaled from 0 to 1.

`B` is the trapezoidal area under that normalized curve.

This permits a comparison of basin **shape** without equating the physical
units of epsilon, additive noise sigma, and damping gamma.

The compared basins are:

- Frey–Rachel MBL-DTC drive-imperfection basin;
- ordinary exact 2T plus additive noise;
- ordinary exact 2T plus exponential damping.

## Closure-family geometry

The 10-dimensional vector:

`G = [C(1), C(2), ..., C(10)]`

is compared between systems using:

- cosine similarity;
- RMS distance after max-normalization.

This explicitly tests whether the closure-family geometry itself is unique.

## Dominance test

A simple Pareto test is used instead of tuning a classifier.

If an ordinary non-DTC control is greater than or equal to an MBL-DTC on every
monotone rigidity axis under comparison, then no monotone scalar reweighting of
those axes can be justified as a DTC-specific identifier.

Two decisive tests are made:

1. exact classical 2T versus site-resolved Mi MBL-DTC on `(C,F,S)`;
2. classical sign-flip initial-state family versus Mi MBL initial-state data on
   `(C,F,S,U)`.

## Interpretation rule

Possible strong result:

`DTC_SPECIFICITY_ESTABLISHED`

only if the MBL-DTC occupies a rigidity region not reachable by the ordinary
period-doubled controls.

Possible negative but scientifically useful result:

`DTC_SPECIFICITY_NOT_ESTABLISHED`

if ordinary classical two-cycle dynamics overlap or dominate the DTC on these
trajectory-level rigidity axes.

In that case, the next stage must add a genuinely many-body/collective
structural observable rather than inventing new weights for the same recurrence
quantities.
