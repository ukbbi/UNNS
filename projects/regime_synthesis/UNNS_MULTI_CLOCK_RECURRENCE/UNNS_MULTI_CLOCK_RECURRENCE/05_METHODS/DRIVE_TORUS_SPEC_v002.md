# SOURCE-DEFINED DRIVE TORUS + COUPLING DIAGNOSTIC v002

## Status

**DIAGNOSTIC ONLY.** No admission threshold, no verdict, no frozen grammar.

## Scientific target

Test whether multi-clock organization becomes cleaner when the torus is defined from the **external drives themselves** rather than inferred from the measured observable, and keep coupling as an independent structural axis.

## Scope

Only the six Luo Fig. 3 entanglement-entropy trajectories are used:

- low-frequency aperiodic control: `f_L = 1.00`
- intermediate DTQC regime: `f_L = 2.00`
- high-frequency decoupled control: `f_L = 3.34`
- each at `N = 12` and `N = 32`

The source fixes `f_R/f_L = phi = (1+sqrt(5))/2`.

The canonical source-time columns scale as left-drive-cycle coordinates: `time_end/f_L` is approximately constant across the three Fig. 3 regimes and `2*pi*(time_end/f_L)` is approximately the published evolution time 500. Therefore the drive phases can be represented directly on the source coordinate x as

`theta_L = 2*pi*x`

`theta_R = 2*pi*phi*x`.

This interpretation uses source-axis scaling and the published drive relation; it does not use an observed response frequency.

## d-fold drive cover

For cover depth `d = 1,2,3,4`, the minimal first-order source-defined basis is:

Axis terms:

- `1/d`
- `phi/d`

Mixed terms:

- `|phi-1|/d`
- `(phi+1)/d`

in cycles per source-time unit.

The basis is deliberately restricted to first order. Higher-order integer combinations are not admitted in v002 because a dense irrational lattice can fit broad/chaotic spectra too easily, as seen in the v001 bake-off.

## Cross-validated torus organization

For each frequency, sine and cosine coordinates are used. A deterministic five-fold contiguous block cross-validation fits a linear Fourier chart and reports:

- `axis_r2_cv`: predictability from the two independent drive axes only
- `full_r2_cv`: predictability after adding the two lowest-order mixed drive modes
- `mixed_interaction_gain = full_r2_cv - axis_r2_cv`

The best cover depth is selected by maximum `full_r2_cv`. No depth is pre-assigned.

## Coupling axis

The entanglement entropy `S(t)` is retained in source units as the physical coupling-sensitive observable. v002 reports:

- mean S
- median S
- standard deviation S
- final S

No cross-regime normalization and no composite scalar are defined.

The intended object is therefore a structural vector, not a score:

`(source-torus organization, mixed interaction gain, coupling level)`.

## Robustness

At the automatically selected depth, diagnostics are repeated under fixed, predeclared perturbations:

- downsample x5
- downsample x10
- retain first 75% of the trajectory
- add fixed-seed Gaussian noise with sigma = 0.02 * std(S)

Depth is not re-selected under perturbation.

## Firewall

- C003 is not loaded.
- ZHU_2026 is not loaded.
- MOON_2025 is not loaded.
- Luo m(t) and F(t) are not loaded because their exact drive parameter is not yet represented in the canonical metadata; v002 does not infer it from the observed response.
- No threshold or verdict is emitted.
- No publisher FFT is used.

## Source

Luo et al., “Discrete time quasi-crystals in Rydberg atomic chain,” Communications Physics 9, 141 (2026), DOI 10.1038/s42005-026-02572-0.

The paper states that `f_R/f_L = (1+sqrt(5))/2`; Fig. 3 uses `f_L = 1.00, 2.00, 3.34` for the low, intermediate-DTQC, and high-frequency regimes, respectively, and identifies the high-frequency regime with progressive subsystem decoupling.
