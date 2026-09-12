# ZHU EXTERNAL VALIDATION PROTOCOL v001

## Status

**PRE-ANALYSIS LOCK.**

This protocol is written before any v002 diagnostic score is computed on the Zhu et al. dataset.

## Purpose

Test whether the source-defined two-clock organization discovered in `MC_METHODS_v002`
transfers from the Luo numerical Rydberg-chain platform to the independent experimental
Rydberg-vapour DTQC dataset of Zhu et al. (2026), without changing the v002 basis,
cover-depth scan, cross-validation rule, or robustness settings.

This is an **external transfer validation**, not a blind identity test: the physical identity
of the Zhu dataset and its published DTQC interpretation are already known.

## Frozen method inherited from v002

The following are immutable for this validation:

- cover depths: `d = 1,2,3,4`
- first-order two-clock basis only
- axis modes: `1/d`, `r/d`
- mixed modes: `|r-1|/d`, `(r+1)/d`
- sine + cosine coordinates for every mode
- deterministic contiguous 5-fold cross-validation
- ridge alpha: `1e-9`
- selected depth: maximum `full_r2_cv`
- reported temporal quantities:
  - `axis_r2_cv`
  - `full_r2_cv`
  - `mixed_interaction_gain = full_r2_cv - axis_r2_cv`
- robustness:
  - downsample x5
  - downsample x10
  - first 75 percent of trajectory
  - additive Gaussian noise sigma = 0.02 * std(signal)
  - frozen seed `20260826`
- depth is not re-selected under perturbation
- no classification threshold
- no verdict

## Zhu source-defined clock adapter

Primary source-defined dual-drive setting:

- `f1 = 88 kHz`
- `f2 = 54.387 kHz`
- published ratio: maximally incommensurate, `f1/f2 ≈ phi`

For a source time coordinate `t` in milliseconds:

`x = f2[kHz] * t[ms]`

so `x` is the number of cycles of the lower-frequency source clock.

The v002 torus then uses:

`theta_2 = 2*pi*x`

`theta_1 = 2*pi*phi*x`

No response peak, fitted frequency, Fourier maximum, or target DTQC combination is used
to construct the torus.

## Primary external-transfer records

Use only the source time-domain records:

- `数据/fig1/fig1(c1).xlsx`
- `数据/fig1/fig1(c3).xlsx`

The paired `c2` and `c4` frequency-domain files are not metric inputs.

## Predeclared predictions

1. The automatically selected cover depth is expected to be `d = 2`.
   This is a descriptive prediction, not a sufficient DTQC criterion.
2. `full_r2_cv` should exceed `axis_r2_cv`.
3. Therefore `mixed_interaction_gain` should be positive.
4. The positive mixed contribution should survive the fixed v002 robustness perturbations.
5. No numerical threshold is introduced after observing Zhu.

## Falsification / weakening conditions

The v002 temporal mechanism is weakened if:

- the source-defined full torus does not outperform the axis-only model,
- mixed interaction gain is non-positive or disappears under basic robustness tests,
- results require changing the cover range, basis order, CV rule, source clocks, or
  robustness settings.

## Important scope limitation

The Luo v002 package also reported entanglement entropy as a source-native coupling-sensitive
axis. Zhu does not provide the same observable. It is therefore **not legitimate to fabricate
an entanglement surrogate**.

Accordingly, this first Zhu test validates only the portable **temporal two-clock sector**
of v002:

`(source-torus organization, mixed interaction gain, selected cover depth)`.

The Zhu paper's independently demonstrated rigidity / parameter-basin evidence may be cited
as physical context, but it is not converted into the Luo entanglement coordinate.

## Control limitation fixed before analysis

The public Zhu archive contains strong published spectral/phase controls (single-drive DTC,
relative-phase DTC-to-DTQC transitions, detuning and RF-amplitude phase diagrams), but the
identified primary v002 inputs are time-domain trajectories.

No inverse Fourier reconstruction, synthetic time trace, interpolation-based control, or
publisher-spectrum-to-time-series conversion is permitted.

Therefore this stage is an **external positive-transfer test**, not yet a complete matched
time-domain candidate/control validation.

## Firewall

- no C003 data
- no C003-derived threshold
- no Zhu-derived parameter tuning
- no synthetic evidence
- no target-frequency injection
- no publisher FFT as v002 input
- quantitative outputs must be written and hashed before interpretation
