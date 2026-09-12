# TC_CTRL_v001 — Method

## Purpose

Challenge the frozen temporal-closure metric with systems that are **not discrete
time crystals** but can nevertheless possess exact or approximate period-doubled
dynamics.

The objective is falsification-oriented:

> Does the frozen UNNS temporal-closure construction identify DTC order uniquely,
> or does it detect temporal recurrence more generally?

## Frozen metric

No closure formula is changed.

The package accepts either:

- `TC_CLOSURE_LOCK_v001\`
- `TC_CLOSURE_LOCK_v001.zip`

and verifies the exact frozen metric SHA-256 before execution:

`06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553`

The following locked functions are used unchanged:

- `closure_spectrum`
- `detect_fundamental_q`
- `family_contrast`
- `shuffle_null`

## Control A — exact period-2 recurrence

A deterministic 20-coordinate vector `A` alternates:

`A, -A, A, -A, ...`

This is deliberately not a time crystal. It is the strongest sanity check:
the metric should identify exact q=2 recurrence.

## Control B — noisy period-2 recurrence

The exact trajectory receives one fixed Gaussian noise realization scaled by:

`sigma = 0.00 ... 1.00`

The same noise field is scaled at every sigma, making the sweep nested and
fully reproducible.

This measures degradation of C(2) and the q=2 recurrence family.

## Control C — damped/transient period doubling

The exact period-2 state is multiplied by:

`exp(-gamma t)`

for:

`gamma = 0.00 ... 0.12`

This specifically tests the frozen support term. A transient can preserve
period-2 sign alternation while losing supported closure as its amplitude
collapses.

## Control D — classical nonlinear period doubling

A 20-member ensemble of the logistic map is evolved:

`x_(t+1) = r x_t (1 - x_t)`

after a 500-step burn-in.

Selected controls:

- `r = 3.20` — stable classical period-2 attractor
- `r = 3.50` — stable classical period-4 attractor
- `r = 4.00` — chaotic regime

A wider sweep from `r=3.05` to `4.00` is exported.

No quantum or Floquet-time-crystal mechanism exists in this model.

## Control E — IID random trajectory

A fixed-seed 51 × 20 Gaussian random trajectory is used as an aperiodic
negative control.

## Important diagnostic distinction

For the selected controls, the package reports both:

1. the recurrence family associated with the **automatically detected q0**;
2. the recurrence family associated specifically with **q=2**, because the
   synthetic period-2 controls are known by construction.

The latter is a control diagnostic, not a modification of the frozen metric.

## Preserved limitation: harmonic ambiguity

For a nearly exact period-2 signal, C(2), C(4), C(6), C(8), and C(10) can be
nearly degenerate. Small noise can make the frozen local-contrast q0 rule select
a higher even harmonic such as q=8 rather than the primitive q=2.

This behavior is reported as a limitation and is **not repaired in v001**.

## Interpretation rule

If ordinary classical period-2 dynamics produce strong, shuffle-significant
closure, then temporal closure is not DTC-specific.

That outcome does not invalidate the closure construction. It establishes its
proper level of meaning:

`C(q) = temporal recurrence structure`

The DTC-specific hypothesis must then move to higher-order structure:

- perturbation rigidity;
- universality across initial states and disorder realizations;
- collective persistence;
- width and stability of the recurrence-family basin.
