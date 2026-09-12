# TC_COLLECTIVE_v001 — Method

## Research question

Can the UNNS time-crystal branch move beyond trajectory recurrence by adding a
genuinely collective / many-body structural sector?

The stage deliberately separates three kinds of evidence:

1. **collective pair order and finite-size scaling**;
2. **many-site correlation propagation**;
3. **many-body spectral/eigenstate breadth via quantum typicality**.

The purpose is not to invent another weighted score.

## Frozen temporal sector

Temporal closure is imported from `TC_EXT_MI_v001`, which was computed using the
unchanged metric from `TC_CLOSURE_LOCK_v001`.

The lock SHA-256 is verified:

`06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553`

## A. Spin-glass collective order — Fig. 5

The Mi data file `fig_5.csv` contains the experimental Edwards–Anderson
spin-glass order parameter for:

`L = 8, 12, 16, 20`

at each drive value g.

For every g we fit:

`chi_SG(L) ~ L^alpha`

by linear regression of `log chi` on `log L`.

The first sign change of alpha from non-positive to positive is reported as a
grid-level finite-size crossing interval. No interpolation toward the published
transition is used.

This is a genuinely collective pair-correlation measurement, but not by itself
a uniquely quantum signature.

## B. Correlation propagation — Fig. 3d

The released MBL and prethermal matrices contain the relative response to a
single-site perturbation as a function of qubit position and successive
time windows.

For the late-time spatial profile:

`p_i = |zeta_i| / sum_j |zeta_j|`

we calculate:

`IPR = sum_i p_i^2`

`N_eff = 1/IPR`

and the RMS spatial radius around the maximal-response site.

Higher IPR / lower N_eff means a more spatially localized perturbation.

## C. Broad initial-state order — Fig. 3b

The released data contain 500 random bit-string initial-state autocorrelator
values for MBL-DTC and prethermal dynamics.

For the absolute values we report:

- mean;
- standard deviation;
- coefficient of variation;
- 5%, 50%, 95% quantiles.

This tests whether late-time order extends broadly across initial states rather
than being carried by a few special states.

## D. Quantum typicality / spectral breadth — Fig. 4d and Supplementary Fig. 10

This is the first coordinate in the project that is operationally
quantum-many-body rather than merely a trajectory property.

The experiment prepares highly scrambled, entangled states with increasing
scrambling depth K and measures the autocorrelator distribution over 500
states.

We process:

- MBL-DTC: `fig_4d.csv`, K = 0, 2, 20
- prethermal: `fig_s10_b.csv`, K = 0, 5, 20
- thermal: `fig_s10_d.csv`, K = 0, 5, 20

For each distribution we report mean absolute autocorrelator, standard
deviation, coefficient of variation and quantiles.

The primary spectral-breadth observable is the final K=20 mean |A_psi|.

## E. Classical falsification controls

Two lower collective observables can be mimicked classically.

### Pair order counterexample

For a deterministic classical sign-flip two-cycle with z_i=±1, the same
mathematical Edwards–Anderson pair-order form is extensive:

`chi_cl = L - 3`

under the same interior-site counting convention.

Therefore extensive pair order alone is not DTC-specific.

### Localization counterexample

For an uncoupled classical map:

`X_(t+1) = -X_t`

a perturbation to one coordinate stays exactly there forever:

`IPR = 1`, `N_eff = 1`.

Therefore perturbation localization alone is not DTC-specific.

## Domain-qualified conclusion

The Hilbert-space typicality coordinate is different.

An ordinary classical periodic attractor does not possess the same operational
object: a highly entangled Haar-typical state sampling an exponentially large
many-body Hilbert space.

For that reason the classical control is **N/A** on this coordinate, not zero.

The stage therefore permits the statement:

`temporal closure + many-body spectral order`

separates MBL-DTC from the thermal and prethermal **quantum** controls in the Mi
dataset.

It does **not** permit a universal scalar classification in which a classical
periodic attractor is assigned an arbitrary failure value on a quantum-only
coordinate.
