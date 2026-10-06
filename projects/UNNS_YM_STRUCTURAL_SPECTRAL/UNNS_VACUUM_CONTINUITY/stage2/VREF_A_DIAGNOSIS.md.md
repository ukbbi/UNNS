# VREF_A_DIAGNOSIS.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Branch:** VREF-I/A — refinement validation  
**Source:** `BAKER_2022_SU3`  
**Frozen run outcome:** **CALIBRATION-SENSITIVE**  
**Record type:** post-run diagnosis  
**Date:** 2026-09-30

---

## 1. Frozen result remains unchanged

The VREF-I/A run completed successfully and all mandatory source-integrity checks passed.

The frozen calibration verdict remains:

```text
CALIBRATION-SENSITIVE
```

This post-run diagnosis does not revise, soften, or replace that verdict.

VREF-I/A remains calibration-only and cannot be interpreted as either:

```text
CONTINUITY-SUPPORTED
ISOLATION-SUPPORTED
```

---

## 2. Main diagnostic finding

The sensitivity is **localized rather than global**.

Only window 3, beginning at

\[
u=0.375,
\]

changes qualitative classification between the frozen primary linear interpolation and the preregistered PCHIP sensitivity.

For that window:

### Linear

\[
R_{12}=0.042382842,
\]

\[
R_{23}=0.041820556,
\]

\[
C=\frac{R_{23}}{R_{12}}=0.98673318<1.
\]

### PCHIP

\[
R_{12}=0.040738,
\]

\[
R_{23}=0.042223,
\]

\[
C=1.036440>1.
\]

Thus the categorical flip occurs because the contraction ratio lies very close to the threshold

\[
C=1.
\]

A small interpolation-induced perturbation is sufficient to move the ratio from slightly below to slightly above unity.

This is a threshold-sensitive transition window, not a wholesale failure of the VREF-I representation.

---

## 3. Robust regions

### Inner windows

Windows 0, 1, and 2 satisfy

\[
C<1
\]

under both linear and PCHIP interpolation.

Thus the qualitative statement

> medium-to-fine discrepancy is smaller than coarse-to-medium discrepancy

is interpolation-robust through the inner and intermediate common-profile region.

### Outermost window

Window 4 gives

\[
C_{\rm linear}=1.4850755,
\]

\[
C_{\rm PCHIP}=1.528656,
\]

so

\[
C>1
\]

under both interpolation methods.

Therefore the loss of refinement contraction in the outermost common-support window is **not** produced by the linear/PCHIP choice.

It is a robust feature of the measured central profiles within VREF-I/A.

---

## 4. Why interpolation sensitivity is concentrated in R2

The frozen common-grid spacing is

\[
\Delta x = 0.063875\ {\rm fm}.
\]

The native lattice spacings are approximately

\[
a_{R1}=0.0639\ {\rm fm},
\]

\[
a_{R2}=0.0426\ {\rm fm},
\]

\[
a_{R3}=0.0320\ {\rm fm}.
\]

Consequently:

- the common grid is almost exactly aligned with every R1 native transverse step;
- it is almost exactly aligned with every second R3 native transverse step;
- for R2, many common-grid points lie approximately halfway between native points.

This is directly visible in the linear/PCHIP differences.

Maximum absolute dimensionless profile difference:

```text
R1: 0.000108
R2: 0.017816
R3: 0.0000758
```

For R2 the largest difference occurs at

\[
u=0.125,
\]

and is about 1.18 times the interpolated published pointwise error scale there.

By contrast, the maximum interpolation difference is only about 0.032 of the published error scale for R1 and 0.0035 for R3.

Therefore the interpolation sensitivity is primarily a **grid-commensurability effect in R2**.

---

## 5. Leave-one-out diagnostic

The deterministic linear leave-one-out diagnostic shows that local interpolation curvature can be larger than the published pointwise error scale, especially on the coarser profiles.

Summary:

| Level | median \(|r|/\epsilon\) | max \(|r|/\epsilon\) | median \(|r|/|E|\) | max \(|r|/|E|\) |
|---|---:|---:|---:|---:|
| R1 | 3.04 | 24.51 | 3.09% | 6.25% |
| R2 | 2.17 | 5.65 | 1.33% | 3.93% |
| R3 | 0.50 | 0.83 | 1.15% | 2.17% |

This does not invalidate the run because the leave-one-out test was preregistered as descriptive only.

It does show that point-interpolation geometry must be treated explicitly in the design of VREF-I/B.

---

## 6. Vacuum-directed profile behavior

For every refinement level and under both interpolation methods,

\[
D_{\rm VREF}(s)
\]

decreases monotonically as the fixed window moves outward.

Under the primary linear interpolation:

```text
R1: 1.820854 -> 0.613678   (-66.30%)
R2: 1.862441 -> 0.653002   (-64.94%)
R3: 1.879987 -> 0.684415   (-63.59%)
```

This is a robust measured movement toward the zero-field reference across the available common domain.

However, the terminal distances remain substantially positive.

Therefore VREF-I/A demonstrates **vacuum-directed decay of the profile**, but it does not demonstrate structural vacuum accessibility.

---

## 7. Outer-region refinement behavior

At the final common-grid point

\[
u=1,\qquad x_t=0.511\ {\rm fm},
\]

the dimensionless central values are approximately:

```text
R1: 0.323366
R2: 0.351492
R3: 0.459651
```

The finest-resolution profile therefore remains systematically above the coarser profiles in the outer common region.

This behavior is also visible in the robust outer-window result

\[
C>1.
\]

VREF-I/A does not determine whether this arises from finite-spacing effects, smearing/renormalization systematics, the published field decomposition, limited transverse support, or another source-specific effect.

It must not be interpreted as structural isolation.

---

## 8. Post-run common-native-point diagnostic

A diagnostic using only the five dimensionless positions that are approximately native-grid aligned across all three resolutions,

\[
u=\{0,\ 0.25,\ 0.5,\ 0.75,\ 1\},
\]

gives whole-profile RMS differences approximately

\[
R_{12}=0.05963,
\]

\[
R_{23}=0.05525,
\]

\[
R_{13}=0.10256,
\]

and

\[
C=\frac{R_{23}}{R_{12}}\approx0.927.
\]

This calculation is **post hoc and diagnostic only**. It cannot alter the frozen VREF-I/A outcome.

Its significance is methodological: removing the strongly off-grid R2 points reduces the interpolation ambiguity and supports an interpolation-minimizing design for VREF-I/B.

---

## 9. What VREF-I/A has established

VREF-I/A has successfully done what a calibration branch was intended to do.

It has shown that:

1. the VREF-I representation is executable and reproducible on real pure-SU(3) lattice data;
2. the gauge-invariant profile maintains a coherent common physical shape across refinement;
3. the vacuum-referenced fixed-window distance decreases monotonically outward at all three resolutions;
4. refinement contraction is robust in the inner/intermediate region;
5. the outer common-support region does not show robust contraction;
6. one transition window is classification-sensitive because the contraction ratio lies almost exactly at unity;
7. interpolation sensitivity is dominated by the R2 grid geometry rather than being distributed uniformly across all refinements.

The correct retained verdict remains:

```text
CALIBRATION-SENSITIVE
```

---

## 10. Mandatory design lessons for VREF-I/B

VREF-I/B should not simply repeat the VREF-I/A geometry on another dataset.

Its preregistration should incorporate the following lessons:

### A. Prefer common native physical coordinates

Where possible, construct the primary comparison from coordinates sampled natively at every refinement level.

Interpolation should be minimized rather than treated as invisible preprocessing.

### B. If interpolation is unavoidable, include it in the primary uncertainty architecture

A result should not hinge on whether a single interpolator places a ratio infinitesimally above or below a categorical threshold.

### C. Require multi-resolution access farther into the vacuum-compatible tail

The source must extend far enough that the profile becomes statistically compatible with the independently defined vacuum reference at more than one refinement level.

### D. Keep fixed structural width

The VREF-I fixed-width principle remains valid.

No shrinking-tail construction should be introduced to manufacture approach to zero.

### E. Preserve absolute amplitude

No peak, norm, integral, or first-point self-normalization should be introduced.

### F. Keep the continuity verdict independent of CORR-I

CORR-I remains comparative only.

---

## 11. Stage implication

VREF-I/A is complete.

It should **not be rerun with retuned parameters**.

The next research branch is:

```text
VREF-I/B — Structural Vacuum Accessibility
```

but only after:

1. identifying a source with adequate multi-resolution vacuum-tail support;
2. freezing its source admission;
3. preregistering an interpolation-minimizing or interpolation-explicit common-refinement architecture;
4. freezing the VREF-I/B falsification and uncertainty rules before inspecting its target outcome.
