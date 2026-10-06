# YM3B_BUILD_RECORD.md

## UNNS Yang-Mills Gap - YM-3B SS23 Class B input build

**Build:** `YM3B-SS23-BUILD v0.1.0`  
**Date:** 2026-09-30  
**Source:** Sakai & Sasaki (2023), Phys. Rev. D 107, 034510  
**Evidence class:** B - published effective-mass trajectories  
**Frozen chamber:** CORR-I v0.1.2  
**Scientific CORR-I batch run:** **NO**

## Built sequence

Four `A1++ / 0++` ground-state trajectories were digitized from the publication:

| beta | Figure | digitized M_eff points | r0/a | published aM | fit range | admission |
|---:|---:|---:|---:|---:|---:|---|
| 6.20 | 9 | 9 | 7.38 | 0.5198 | [2, 8] | **ADMIT** |
| 6.40 | 10 | 11 | 9.74 | 0.4025 | [3, 8] | **ADMIT** |
| 6.71 | 11 | 13 | 14.49 | 0.2664 | [3, 10] | **ADMIT** |
| 6.93 | 12 | 17 | 19.48 | 0.197 | [3, 12] | **ADMIT** |

## Digitization method

The source PDF was rendered at 300 dpi. The publication itself is vector-based, so the digitization
uses the vector geometry of the rendered source to locate the open-circle ground-state markers and
their vertical error bars. Coordinates are recorded both in native PDF points and in corresponding
300-dpi pixel coordinates. No OCR and no smoothing were used.

The exact plot frames and axis ranges are frozen in `data/derived/corr_i/ym3b/ss23/calibration/`.

## Reconstruction

For each beta:

`lambda(0) = 1`

`lambda(t+1) = lambda(t) * exp[-M_eff(t)]`

The resulting normalized variational-eigenvalue proxy is stored under `native/`.

The primary common physical coordinate is:

`u = t / (r0/a)`

with the preregistered seven-point grid:

`u = 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61`.

Primary interpolation is piecewise-linear interpolation of `log(lambda)`.
The first common-grid point is renormalized to `C_B(u0)=1`.

PCHIP versions are built separately for the preregistered interpolation sensitivity test.

## Admission verification

All four beta levels:

- cover the complete seven-point common grid;
- produce finite positive common-grid correlator proxies;
- reconstruct plateau scales consistent with the published Table-VII masses.

For transparency, the plateau check uses an inverse-graphical-variance weighted mean over the
published fit window as a **descriptive no-covariance check**. The observed differences from the
published correlated-fit masses are:

- beta 6.20: Δ/σ_comb = -0.747
- beta 6.40: Δ/σ_comb = 0.079
- beta 6.71: Δ/σ_comb = -1.002
- beta 6.93: Δ/σ_comb = 0.198

All four lie within approximately 1.01 combined standard deviations of the published values.

This does not replace the authors' correlated fits and is used only as an admission/verification
check on the publication digitization.

## Status

\[
oxed{	extbf{SS23\_B4 CLASS B INPUTS BUILT; 4/4 LEVELS ADMITTED}}
\]

No CORR-I scientific result has been inspected or generated in this package.

## Next action

Construct the preregistered beta-matched Gamma controls (`p=0.5,1,2,4,8`), verify the frozen
CORR-I chamber hash, and then execute the complete four-beta YM-3B batch without inspecting
partial beta results.
