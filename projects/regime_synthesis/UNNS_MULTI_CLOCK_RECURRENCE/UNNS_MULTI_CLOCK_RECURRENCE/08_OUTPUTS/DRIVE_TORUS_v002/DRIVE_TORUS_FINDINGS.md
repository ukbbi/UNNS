# DRIVE_TORUS_COUPLING v002 — FINDINGS

## Status

**DIAGNOSTIC ONLY — NO GRAMMAR FROZEN**

Six Luo Fig. 3 entanglement trajectories were evaluated with the two external drive clocks defining the torus. No response-derived clock, classification threshold, or verdict was used.

## Finding 1 — Source-defined phases reverse the v001 failure

At N=32, the automatically selected best cover is d=2 for all three regimes, but the quality of organization is sharply different:

| Regime | Full source-torus R2 | Axis-only R2 | Mixed interaction gain | Mean entanglement S |
|---|---:|---:|---:|---:|
| Low-frequency aperiodic | 0.1213 | 0.0697 | 0.0515 | 0.5853 |
| Intermediate DTQC | **0.9409** | 0.7167 | **0.2242** | 0.2425 |
| High-frequency decoupled | 0.6976 | 0.5972 | 0.1004 | 0.0719 |

In v001, an observable-derived torus incorrectly favored the low and high controls. Anchoring the chart to the independently specified drives changes the ordering: the proper DTQC regime is now the strongest source-torus organization.

## Finding 2 — Cover depth d=2 is real but not DTQC-specific

All six records select d=2 automatically from d=1..4.

This is important but not sufficient. The high-frequency decoupled regime also retains a strong two-cover signature because it becomes approximately two independent period-doubled DTCs. The low-frequency regime also shows a weak d=2 preference.

Therefore:

**two-cover recurrence is not equivalent to coupled DTQC organization.**

This is the multi-clock analogue of the earlier TIME-CRYSTAL-I lesson that recurrence depth alone is not enough.

## Finding 3 — Mixed drive organization carries new specificity

The mixed interaction gain measures how much predictive structure is added by the two first-order joint modes beyond the two independent drive axes.

At N=32:

- DTQC: 0.2242
- high-frequency decoupled: 0.1004
- low-frequency aperiodic: 0.0515

The DTQC mixed gain is about 2.23x the decoupled control and 4.35x the low-frequency control.

This supports a genuine **joint-drive organization axis** rather than a mere presence-of-two-clocks detector.

## Finding 4 — Coupling remains an independent axis

The mean entanglement S orders the same regimes in the opposite physical direction:

- low-frequency aperiodic: 0.5853
- DTQC: 0.2425
- high-frequency decoupled: 0.0719

Thus high coupling alone is not DTQC structure: the low-frequency control is the most entangled but poorly organized on the source torus. Conversely, strong torus organization alone is not enough: the high-frequency control remains substantially torus-organized while its entanglement collapses toward decoupling.

The DTQC occupies an intermediate-coupling / high-joint-organization region.

This is why v002 does **not** collapse the result into one scalar.

## Finding 5 — The result is effectively system-size invariant here

N=12 and N=32 produce nearly identical values within each regime for source-torus R2, mixed interaction gain, and mean S.

The separation is therefore not an obvious finite-size artifact of these paired records.

## Finding 6 — Basic robustness checks preserve the ordering

The ordering DTQC > high-frequency decoupled > low-frequency aperiodic in source-torus organization survives:

- downsampling by 5
- downsampling by 10
- 2% rms additive noise
- truncation to the first 75% of the trajectory

The mixed-interaction ordering also remains DTQC > high > low under all declared perturbations.

## Structural interpretation

The first defensible multi-clock object emerging from the development corpus is not a scalar score but a vector:

`M = (T_source, J_mixed, S_coupling)`

where:

- `T_source` = cross-validated organization on the source-defined drive torus
- `J_mixed` = gain from joint drive modes beyond independent axis modes
- `S_coupling` = physical bipartite coupling observable retained in source units

The present Luo development data occupy three qualitatively different regions:

- low-frequency: high coupling, weak torus organization
- DTQC: finite/intermediate coupling, strong joint torus organization
- high-frequency: weak coupling, substantial but more axis-dominated torus organization

This is the first result in the new branch that cleanly exposes the mechanism the v001 bake-off could not resolve.

## What is NOT established

- No universal DTQC threshold has been found.
- No admissibility verdict is defined.
- d=2 is not claimed to be DTQC-specific.
- The source irrational ratio is not claimed to be distinguishable from arbitrarily close rational approximants over a finite trajectory.
- The result is so far demonstrated on one numerical physical platform and must be validated independently before freeze.

## Next scientific step

Do not tune v002 into a classifier.

Next, validate the structural vector on an independent multi-clock dataset. If Moon remains inaccessible, the preferred route is to locate another public DTQC/quasiperiodic candidate-control corpus while keeping Zhu 2026 protected as the holdout.
