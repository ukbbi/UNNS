# PREREG_VREF_B.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Branch:** VREF-I/B — Structural Vacuum Accessibility  
**Primary source:** `CEA_2017_SU3`  
**Status:** **FROZEN — BEFORE PRIMARY EXTRACTION/FIT**  
**Freeze date:** 2026-10-05

---

## 1. Scientific question

VREF-I/B tests whether the vacuum-referenced Yang–Mills profile is consistent with an asymptotic approach to the vacuum locus,

\[
D_{\rm struct}\rightarrow0,
\]

or instead with a positive refinement-stable structural floor,

\[
D_{\rm struct}\rightarrow\delta,\qquad \delta>0.
\]

This is not a test of whether the physical Yang–Mills mass gap vanishes.

The physical interpretation remains:

> **The mass gap separates eigenvalues, not necessarily structural neighborhoods.**

---

## 2. Primary hypothesis

### H1 — Structural Vacuum Accessibility

The vacuum-referenced profile admits an asymptotic zero-floor continuation compatible with both physical refinements, while the fixed-width VREF-I distance decreases outward without a refinement contradiction.

Operationally:

\[
E_l(x_t)\rightarrow0
\]

as \(x_t\) increases, with no detected positive asymptotic floor that survives the frozen model and refinement checks.

### H0 — Structural Isolation / Positive Floor

The profile is better described by

\[
E_l(x_t)\rightarrow\delta,\qquad \delta>0,
\]

with the positive floor stable across both refinements and both preregistered asymptotic model families.

---

## 3. Source geometry

The physical source separation is frozen as

\[
d=0.76\ {\rm fm}.
\]

Two measured physical refinements are used:

```text
R1: beta = 6.050, d = 8a
R2: beta = 6.195, d = 10a
```

No third refinement is invented.

---

## 4. Absolute amplitude is preserved

The following operations are prohibited:

- peak normalization;
- normalization by the first point;
- normalization by the profile norm;
- normalization by the integrated field;
- rescaling either refinement to match the other;
- subtracting a fitted constant before the floor test.

The vacuum reference remains the physical zero field defined by the connected-correlator subtraction.

---

## 5. Common-grid VREF representation

To preserve the frozen Stage-1 VREF-I definition while minimizing interpolation, the primary common grid is defined algorithmically from the **coarser R1 native transverse coordinates**.

Let the extracted R1 native coordinates be

\[
x^{(1)}_0<x^{(1)}_1<\cdots.
\]

Let

\[
x_{\max}^{\rm common}
=
\min(x_{\max}^{(1)},x_{\max}^{(2)}).
\]

Then the frozen common grid is:

\[
\boxed{
G=
\{x^{(1)}_j:\;x^{(1)}_j\le x_{\max}^{\rm common}\}.
}
\]

Consequences:

- R1 is never interpolated;
- only the more finely sampled R2 profile is interpolated;
- no point is extrapolated.

### Primary interpolation

R2 is mapped to \(G\) by piecewise linear interpolation.

### Mandatory sensitivity interpolation

R2 is independently mapped to \(G\) by PCHIP.

The primary VREF-I/B verdict must not change between these two interpolation rules. If it does, the result is `INTERPOLATION-SENSITIVE`.

---

## 6. Fixed-width VREF windows

Let

\[
\Delta_G
\]

be the median spacing of the R1-derived common grid.

The VREF-I/B window is frozen as:

\[
m=5,
\qquad
W=4\Delta_G.
\]

For every allowed start point \(s_k\in G\) for which five consecutive common-grid points exist, define

\[
L_r(s_k)=
[z_r(x_k),z_r(x_{k+1}),\ldots,z_r(x_{k+4})].
\]

The dimensionless field coordinate is

\[
z_r(x)=d^2E_l^{(r)}(x).
\]

The vacuum proxy is the five-vector

\[
V^*=(0,0,0,0,0).
\]

The primary structural distance is

\[
\boxed{
D_r(s_k)=
\left[
\frac{1}{5}
\sum_{j=0}^{4}
z_r(x_{k+j})^2
\right]^{1/2}.
}
\]

The window width and point count never shrink in the tail.

---

## 7. VREF path requirement

For a continuity-supporting result, the fixed-width distance must show a vacuum-directed path at both refinements.

The primary descriptive requirement is:

\[
D_r(s_{k+1})\le D_r(s_k)
\]

through the tail windows, allowing equality within propagated pointwise uncertainty.

A local reversal larger than the frozen uncertainty envelope is recorded as `PATH-NONMONOTONE`.

`PATH-NONMONOTONE` does not by itself prove isolation; it blocks a positive continuity verdict.

---

## 8. Native-tail floor test — no interpolation

The asymptotic floor test is performed directly on the two **native** extracted point sets.

No common-grid interpolation enters this test.

### Primary tail cut

Only native points satisfying

\[
\boxed{x_t\ge d/2 = 0.38\ {\rm fm}}
\]

and

\[
x_t\le x_{\max}^{\rm common}
\]

enter the primary asymptotic fit.

The cut \(d/2\) is fixed by the physical source geometry, not by field amplitude.

### Tail-cut sensitivity

A second fit drops the first eligible tail point from each refinement.

The scientific verdict must agree between the primary and sensitivity tail cuts.

---

## 9. Competing asymptotic families

Two independently preregistered model families are used.

### Family E — exponential tail

Zero-floor model:

\[
M_{E0}:
\qquad
E_r(x)=A_r e^{-x/\lambda}.
\]

Positive-floor model:

\[
M_{E\delta}:
\qquad
E_r(x)=\delta+A_r e^{-x/\lambda},
\qquad
\delta\ge0.
\]

### Family K — Bessel tail

Zero-floor model:

\[
M_{K0}:
\qquad
E_r(x)=A_r K_0(x/\lambda).
\]

Positive-floor model:

\[
M_{K\delta}:
\qquad
E_r(x)=\delta+A_r K_0(x/\lambda),
\qquad
\delta\ge0.
\]

For both families:

- \(A_1>0\) and \(A_2>0\) are refinement-specific amplitudes;
- \(\lambda>0\) is common to both refinements;
- \(\delta\) is common to both refinements in the positive-floor model.

Allowing refinement-specific amplitudes avoids forcing exact normalization identity while preserving the physical vacuum floor and common decay scale.

---

## 10. Error model

The EPS error bars are treated as the source's published pointwise statistical errors.

A deterministic vector-quantization uncertainty is added in quadrature:

\[
\sigma_{\rm fit}^2
=
\sigma_{\rm published}^2
+
\sigma_{\rm EPS}^2.
\]

The frozen conservative EPS ordinate uncertainty is

\[
\boxed{
\sigma_{\rm EPS}
=
10^{-4}\times\frac{0.5}{0.7}
=
7.142857\times10^{-5}\ {\rm GeV}^2.
}
\]

No covariance matrix is available.

Therefore all information-criterion comparisons are explicitly described as **diagonal-error operational model comparisons**, not exact correlated-data likelihood statements.

---

## 11. Model ranking

For each model, minimize

\[
\chi^2
=
\sum_i
\frac{(E_i-E_{\rm model}(x_i))^2}
{\sigma_{{\rm fit},i}^2}.
\]

Define

\[
{\rm AICc}
=
\chi^2+2k+
\frac{2k(k+1)}{n-k-1},
\]

where \(k\) is the number of fitted parameters and \(n\) the total number of native tail points across both refinements.

For each family define

\[
\Delta_{\rm floor}
=
{\rm AICc}(M_{\delta})
-
{\rm AICc}(M_0).
\]

Thus:

- \(\Delta_{\rm floor}>0\) favors zero floor;
- \(\Delta_{\rm floor}<0\) favors a positive floor.

The frozen decisive threshold is

\[
\boxed{|\Delta_{\rm floor}|\ge6}.
\]

No threshold is retuned after extraction.

---

## 12. Refinement consistency

The two refinements must independently describe the same physical tail.

On the common grid, define

\[
Q_j
=
\frac{
E_1(x_j)-E_2(x_j)
}{
\sqrt{
\sigma_1(x_j)^2+\sigma_2(x_j)^2+\sigma_{\rm EPS}^2
}
}.
\]

The primary refinement summary is

\[
\chi^2_{\rm ref}
=
\sum_{j\in G_{\rm tail}}Q_j^2,
\]

where \(G_{\rm tail}\) contains common-grid points at \(x\ge d/2\).

Because cross-point covariance is unavailable, this is a diagnostic rather than a formal hypothesis-test probability.

A large, structured refinement mismatch blocks a continuity or isolation verdict and yields `REFINEMENT-INDETERMINATE`.

---

## 13. Primary outcome logic

### `CONTINUITY-SUPPORTED`

All of the following must hold:

1. mandatory vector extraction and source-integrity checks pass;
2. the VREF fixed-width distance is vacuum-directed through the tail for both refinements;
3. linear and PCHIP mappings give the same qualitative VREF path verdict;
4. both asymptotic families favor the zero-floor model with

\[
\Delta_{\rm floor}\ge6;
\]

5. the zero-floor preference survives the tail-cut sensitivity;
6. there is no structured refinement contradiction.

This verdict means:

> within the preregistered CEA_2017 VREF representation, no positive structural exclusion floor is detected and the measured tail supports approach toward the vacuum locus.

It does **not** mean the Yang–Mills mass gap vanishes.

### `ISOLATION-SUPPORTED`

All of the following must hold:

1. extraction checks pass;
2. both asymptotic families favor the positive-floor model with

\[
\Delta_{\rm floor}\le-6;
\]

3. the fitted common floor satisfies

\[
\delta>0;
\]

4. the positive-floor preference survives the tail-cut sensitivity;
5. there is no refinement contradiction.

### `MODEL-SPLIT`

The exponential and Bessel families imply opposite floor classifications.

### `INTERPOLATION-SENSITIVE`

The common-grid VREF path classification changes between linear and PCHIP interpolation.

### `REFINEMENT-INDETERMINATE`

The two physical refinements show a material structural disagreement that prevents a shared asymptotic interpretation.

### `UNCERTAINTY-LIMITED`

Neither zero-floor nor positive-floor model reaches the decisive AICc threshold in both families.

### `EXTRACTION-INVALID`

The deterministic vector-extraction integrity checks fail.

---

## 14. Coarse-only extended tail

R1 may contain measured points beyond the common two-resolution support.

Those points are preserved and reported as:

```text
COARSE_EXTENDED_TAIL
```

They are excluded from the primary floor verdict.

They may be shown only as a non-verdict sensitivity/visual extension.

---

## 15. External validation hierarchy

After the primary CEA_2017 outcome is frozen, comparison may proceed with:

```text
BAKER_2022
role: three-level tabulated refinement calibration

BATTELLI_2019
role: unsmoothed connected-correlator control

YANAGIHARA_2019
role: independent vacuum-subtracted EMT continuum-tail representation
```

None of these sources may be used to retune the CEA_2017 primary protocol.

---

## 16. Prohibited moves

After extraction begins, do not:

- change the tail cut because of the field values;
- alter the common grid;
- change \(m=5\) or \(W=4\Delta_G\);
- replace linear interpolation because of the result;
- introduce amplitude self-normalization;
- drop inconvenient tail points except under the frozen tail-cut sensitivity;
- choose a third asymptotic family to rescue a preferred conclusion;
- redefine the vacuum away from zero;
- infer the physical Yang–Mills mass gap from the structural verdict.

---

## 17. Freeze statement

The VREF-I/B primary experiment is frozen around:

```text
SOURCE: CEA_2017_SU3
OBSERVABLE: E_l(x_t)
VACUUM: E_l = 0
GEOMETRY: d = 0.76 fm
REFINEMENTS: beta 6.050 / beta 6.195
COMMON GRID: R1 native grid truncated to common support
VREF WINDOW: m=5, W=4*Delta_G
PRIMARY TAIL: x_t >= d/2
ASYMPTOTIC FAMILIES: exponential + K0
MODEL TEST: zero floor vs common positive floor
DECISIVE |Delta AICc|: 6
```

The next permitted action is deterministic vector extraction under `VREF_B_EXTRACT.md`.
