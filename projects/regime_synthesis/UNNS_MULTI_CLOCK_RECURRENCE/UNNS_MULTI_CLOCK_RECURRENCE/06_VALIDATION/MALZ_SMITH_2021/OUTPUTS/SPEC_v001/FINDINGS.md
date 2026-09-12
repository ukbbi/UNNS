# MALZ–SMITH SPECIFICITY TEST v001

## Locked assessment

**PASS_STRONG_SPECIFICITY_CHALLENGE**

This independent non-DTQC two-clock experiment does **not** reproduce the Luo-DTQC
fractional-cover pattern.

## Source

The primary test uses all 12 experimental IBM-qubit datasets in the public source archive.

Each run provides 800 source tomography points. The neutral adapter uses the supplied
`corrected results` for X, Y and Z independently.

The source-native control parameter gives:

- 6 runs with `0 < M < 2`: topological `C = -1`
- 6 runs with `M > 2`: trivial `C = 0`

No simulation trajectory is used as primary evidence.

## Main structural result

### Integer parent lattice

The integer source/mixing parent is strongly represented in the topological regime.

Median `parent_full_r2_cv` by component:

| Component | Topological | Trivial |
|---|---:|---:|
| X | 0.863377 | 0.404665 |
| Y | 0.864897 | 0.310316 |
| Z | 0.899285 | -0.136661 |

Thus v003 is not blind to the system's native phase structure: the source-lattice coordinate
changes strongly as the experiment crosses from topological to trivial dynamics.

### Fractional cover

The crucial specificity result is the opposite of Luo DTQC and Zhu DTQC trajectories.

Median `frac_total_gain`:

| Component | Topological | Trivial |
|---|---:|---:|
| X | -0.004914 | -0.026201 |
| Y | -0.007267 | -0.029130 |
| Z | -0.008673 | -0.161759 |

The medians are near zero or negative, not strongly positive.

At base resolution only a small minority of the 36 component records have positive
fractional-total gain, and none forms a broad DTQC-like pattern.

The fractional depth selector also does not lock universally to d=2; selected depths vary
across components and regimes.

## Robustness

Under the frozen v003 perturbations:

- downsample x5
- downsample x10
- first 75 percent
- 2 percent RMS additive noise

the regime medians of fractional-total gain remain negative.

Therefore the absence of a strong fractional-cover signal is not a single-resolution accident.

The short source-defined frequency ramp was excluded in the primary adapter. Repeating the
base calculation with that ramp retained leaves the same qualitative conclusion.

## What this establishes

This is a strong specificity result:

`two incommensurate clocks` does not automatically generate the v003 fractional-cover
signature.

The Malz–Smith system is highly organized by the parent source torus, yet its extra
fractional-cover contribution is weak/absent.

This contrasts sharply with the Luo DTQC development regime, where d=2 fractional-total
gain is about +0.942 and fractional-mixed gain about +0.224, and with the retrospective
Zhu DTQC trajectories where d=2 fractional organization is also positive.

Therefore v003 is not behaving as a generic quasiperiodicity detector.

## Important limitation

This does NOT by itself prove that v003 is a DTQC classifier.

The present test establishes negative-domain specificity against one independent
two-clock non-DTQC physical system.

A fresh positive DTQC validation remains desirable before grammar freeze.

No thresholds or verdict rules were introduced.
C003 remains quarantined.
