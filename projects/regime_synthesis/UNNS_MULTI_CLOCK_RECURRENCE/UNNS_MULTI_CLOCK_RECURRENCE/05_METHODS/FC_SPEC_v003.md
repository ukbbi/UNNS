# FRACTIONAL COVER DIAGNOSTIC v003

## Status

**DIAGNOSTIC DEVELOPMENT ONLY.**

No admission threshold, no verdict, and no frozen multi-clock grammar are defined.

v003 is a principled successor to v002 after the locked Zhu external-transfer test showed:

- joint source-clock organization transferred,
- the v002 `argmax_d full_r2_cv(d)` cover-depth selector did not.

The locked v002 and Zhu validation records remain unchanged.

## Structural decomposition

Let the two source clocks have normalized frequencies

`1` and `r`,

where `r` is fixed by the external drive (`phi` for the present Luo/Zhu branch).

For a cover depth `d`, define the same restricted first-order basis used in v002:

Axis terms:

- `1/d`
- `r/d`

Mixed terms:

- `|r-1|/d`
- `(r+1)/d`

with sine and cosine coordinates for every term.

### 1. Integer parent lattice

`d = 1` is no longer allowed to compete with broken-symmetry cover depths.

It is interpreted explicitly as the **integer source/mixing parent lattice**:

`B_Z = B(1)`.

Reported parent quantities:

- `parent_axis_r2_cv`
- `parent_full_r2_cv`
- `parent_mixed_gain = parent_full_r2_cv - parent_axis_r2_cv`

### 2. Fractional cover sectors

Candidate fractional cover depths are restricted to

`d = 2,3,4`.

For each `d >= 2`, fit two nested charts:

`B_Z + A_d`

and

`B_Z + A_d + M_d`

where `A_d` are fractional axis terms and `M_d` are fractional mixed terms.

Report:

`frac_axis_gain(d) = R2(B_Z + A_d) - R2(B_Z)`

`frac_mixed_gain(d) = R2(B_Z + A_d + M_d) - R2(B_Z + A_d)`

`frac_total_gain(d) = R2(B_Z + A_d + M_d) - R2(B_Z)`

The descriptive fractional depth is

`d_frac = argmax_{d>=2} frac_total_gain(d)`.

This is not an admission criterion.

## Why this differs from v002

v002 asked which `d` explains the most total variance.

That allowed strong drive-synchronous or integer-mixing structure at `d=1` to defeat a
physically real fractional sector.

v003 first conditions on the integer parent lattice, then asks what additional
structure is contributed by each fractional cover.

The distinction is:

`parent organization` != `fractional cover organization`.

## Temporal structural vector

The portable temporal object is descriptive:

`T_v003 = (parent_full_r2, d_frac, frac_axis_gain, frac_mixed_gain, frac_total_gain)`.

No scalar score is formed.

## Collective / coupling sector

Collective evidence remains separate from the temporal chart.

For Luo entanglement records, source-native summaries of `S(t)` are reported:

- mean
- median
- standard deviation
- final value

They are not used to select `d_frac`.

For Zhu, no Luo-style entanglement surrogate is invented.

## Development and retrospective scope

### Official v003 development run

Only the six Luo Fig. 3 entanglement trajectories are used:

- low-frequency aperiodic control
- intermediate DTQC
- high-frequency decoupled control
- N = 12 and N = 32

### Zhu

Zhu is used only as a **retrospective implementation/diagnostic comparison**.

It cannot independently validate v003 because the v003 architecture was motivated by the
locked Zhu depth-selection failure.

A new independent dataset is required for external validation.

## Robustness

At the base-selected `d_frac`, repeat without re-selecting depth:

- downsample x5
- downsample x10
- first 75%
- additive Gaussian noise sigma = 0.02 * std(signal), seed 20260826

## Firewall

- C003 is not loaded.
- No C003-derived frequency, threshold, or adapter is used.
- Huang is not forced into this chart because the canonical ingest does not supply the same
  source-defined dual-clock coordinates.
- Moon remains unavailable.
- No target response frequency is injected.
- No publisher FFT is used as a metric input.
- No classification threshold or verdict is emitted.
