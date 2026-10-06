# PREREG_VREF_I.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Branch:** **VREF-I/A — Refinement Validation**  
**Source:** `BAKER_2022_SU3`  
**Status:** **FROZEN — CALIBRATION PROTOCOL**  
**Freeze date:** 2026-09-30

---

## 1. Scope

VREF-I/A is the first implementation test of the frozen Stage-1 representation:

> **VREF-I — Vacuum-Referenced Profile Representation**

Its purpose is to determine whether a fixed physical gauge-invariant profile can be represented and compared coherently across three ordered lattice refinements.

VREF-I/A is **not** the confirmatory Structural Vacuum Continuity experiment.

The numerical source values were necessarily inspected to identify file structure, coordinate support, duplication, units, and uncertainty format. For that reason this branch is explicitly classified as **calibration**, not as a blind confirmatory test.

The later VREF-I/B continuity source must receive a separate preregistration before its target structural outcome is inspected.

---

## 2. Primary observable

The only primary VREF-I/A channel is

\[
O(x_t)=E_x^{NP}(x_l=d/4,x_t)
\]

from the three admitted Baker et al. tables.

No other field, current, divergence, force-density, string-tension, or fitted quantity may be introduced into the primary VREF-I/A result.

---

## 3. Physical scale

The frozen reference length is the physical source separation

\[
\boxed{\ell_{\rm ref}=d=0.511\ {\rm fm}}.
\]

Using

\[
\hbar c = 0.1973269804\ {\rm GeV\,fm},
\]

this is

\[
\ell_{\rm ref}=2.5896103967\ {\rm GeV}^{-1}.
\]

Because \(E_x^{NP}\) has mass dimension 2, the frozen dimensionless profile is

\[
\boxed{
z^{(r)}(u)=\ell_{\rm ref}^2 E_x^{NP,(r)}(x_t)
}
\]

with

\[
u=\frac{x_t}{d}.
\]

Numerically,

\[
\ell_{\rm ref}^2=6.7060820069\ {\rm GeV}^{-2}.
\]

No profile-dependent normalization is allowed.

---

## 4. Branch selection

The source tables contain exact duplicated positive and negative transverse branches.

The primary branch is frozen as

\[
\boxed{x_t\ge0}.
\]

The negative branch is used only to verify symmetry and ingestion integrity.

No averaging of \(+x_t\) and \(-x_t\) is required because the supplied central values and errors are exact duplicates.

---

## 5. Common support

The frozen three-level common support is

\[
\boxed{0\le x_t\le0.511\ {\rm fm}}
\]

or equivalently

\[
\boxed{0\le u\le1}.
\]

No extrapolation is permitted.

The R1-only extension beyond \(0.511\) fm is excluded from all three-level primary metrics.

---

## 6. Frozen common grid

The VREF-I/A common grid is fixed independently of profile amplitude as nine equally spaced points in the dimensionless coordinate:

\[
\boxed{
u_j=\frac{j}{8},\qquad j=0,1,\ldots,8
}
\]

corresponding to

| \(j\) | \(u_j\) | \(x_t=u_jd\) [fm] |
|---:|---:|---:|
| 0 | 0.000 | 0.000000 |
| 1 | 0.125 | 0.063875 |
| 2 | 0.250 | 0.127750 |
| 3 | 0.375 | 0.191625 |
| 4 | 0.500 | 0.255500 |
| 5 | 0.625 | 0.319375 |
| 6 | 0.750 | 0.383250 |
| 7 | 0.875 | 0.447125 |
| 8 | 1.000 | 0.511000 |

This grid is fixed for VREF-I/A and may not be moved after the chamber is run.

---

## 7. Frozen interpolation

### Primary interpolation

For each refinement level, central values are mapped to the common grid by **piecewise linear interpolation** between the two nearest native points.

No cubic spline is permitted in the primary branch.

No extrapolation is permitted.

### Error-column interpolation

If the bracketing native errors are \(\epsilon_i,\epsilon_{i+1}\) and

\[
t=\frac{x-x_i}{x_{i+1}-x_i},
\]

the primary interpolated published error scale is

\[
\boxed{
\epsilon(x)=(1-t)\epsilon_i+t\epsilon_{i+1}.
}
\]

This linear-envelope rule is used because the public tables do not provide a point-to-point covariance matrix and do not fully decompose the error column.

### Sensitivity interpolation

PCHIP may be run once as a preregistered sensitivity check on the central profile.

It may not replace the primary linear result.

A cubic spline with unconstrained overshoot is excluded.

---

## 8. Frozen fixed-width VREF-I windows

The fixed dimensionless window width is

\[
\boxed{W=0.5}.
\]

Each window contains

\[
\boxed{m=5}
\]

ordered points with offsets

\[
\boxed{
\xi=\{0,\ 0.125,\ 0.250,\ 0.375,\ 0.500\}.
}
\]

Five overlapping windows are evaluated at

\[
\boxed{
s\in\{0,\ 0.125,\ 0.250,\ 0.375,\ 0.500\}.
}
\]

Thus the structural path spans the common domain from the flux-tube core toward its outer measured region without changing window width or point count.

---

## 9. Primary VREF-I vacuum distance

For each refinement level \(r\) and window start \(s\),

\[
\boxed{
D_{\rm VREF}^{(r)}(s)
=
\left[
\frac{1}{5}
\sum_{j=1}^{5}
z^{(r)}(s+\xi_j)^2
\right]^{1/2}.
}
\]

The operational vacuum proxy remains

\[
V_r^*=(0,0,0,0,0).
\]

VREF-I/A reports \(D_{\rm VREF}\) but may not interpret its terminal value as evidence for or against structural vacuum continuity.

---

## 10. Secondary VREF-I metric

The preregistered metric sensitivity is

\[
\boxed{
D_\infty^{(r)}(s)
=
\max_j |z^{(r)}(s+\xi_j)|.
}
\]

It is reported beside the RMS distance.

No other metric may be promoted into the primary VREF-I/A result after viewing the output.

---

## 11. Refinement-comparison metric

To quantify the representation-level difference between two refinements \(r_a,r_b\) on the same fixed window, define

\[
\boxed{
R_{ab}(s)
=
\left[
\frac{1}{5}
\sum_{j=1}^{5}
\left(
z^{(r_a)}(s+\xi_j)-z^{(r_b)}(s+\xi_j)
\right)^2
\right]^{1/2}.
}
\]

The primary reported pairs are:

\[
R_{12}(s),\qquad
R_{23}(s),\qquad
R_{13}(s).
\]

The descriptive contraction ratio

\[
\boxed{
C(s)=\frac{R_{23}(s)}{R_{12}(s)}
}
\]

is reported when \(R_{12}(s)>0\).

Interpretation is purely calibration-level:

- \(C(s)<1\): medium-to-fine discrepancy is smaller than coarse-to-medium discrepancy;
- \(C(s)=1\): equal RMS discrepancy;
- \(C(s)>1\): medium-to-fine discrepancy is larger.

No Stage-2 continuity claim is attached to \(C(s)\).

---

## 12. Uncertainty propagation

The published pointwise error column is propagated but is not used to redefine the metric.

For each common-grid point, define the dimensionless error scale

\[
\epsilon_z(u)=\ell_{\rm ref}^2\epsilon_E(u).
\]

### Primary deterministic envelope

For each VREF-I window, form lower and upper pointwise profiles

\[
z_j^- = z_j-\epsilon_{z,j},
\qquad
z_j^+ = z_j+\epsilon_{z,j}.
\]

The chamber reports the induced minimum/maximum RMS distances obtained from these pointwise envelopes.

Because the public archive supplies no covariance matrix, these bounds are treated as **sensitivity envelopes**, not confidence intervals.

### Optional probabilistic sensitivity

No Gaussian Monte Carlo is part of the primary VREF-I/A result.

A Gaussian/no-covariance simulation may be added later only as an explicitly labelled sensitivity calculation; it may not alter the frozen primary verdict.

---

## 13. Ingestion and integrity checks

Before any VREF-I/A metric is accepted, the implementation must verify:

1. exactly three numerical columns are present;
2. all coordinates, central values, and errors are finite;
3. \(x_t\) is strictly ordered on each selected non-negative branch;
4. all error entries are non-negative;
5. the negative and positive branches match exactly where both are supplied;
6. the frozen common grid lies inside each native support;
7. no common-grid value is extrapolated;
8. units are retained exactly as supplied before the frozen dimensionless conversion.

Failure of any mandatory check produces:

```text
IMPLEMENTATION-INVALID
```

rather than a physical conclusion.

---

## 14. Interpolation self-check

A deterministic leave-one-out interpolation diagnostic is run independently at each refinement:

- on the non-negative native branch;
- omit each eligible interior native point one at a time;
- reconstruct it from its immediate neighbors using the frozen linear interpolation;
- record the absolute residual in GeV\(^2\);
- record the residual relative to the published pointwise error scale.

This diagnostic does not change the interpolation rule.

It exists only to expose whether the common-grid interpolation itself is a material source of distortion.

---

## 15. VREF-I/A outcome classes

VREF-I/A can return only one of the following calibration outcomes:

### `CALIBRATION-VALID`

All mandatory ingestion/common-grid checks pass; the VREF-I profile and fixed-window metrics are finite and reproducible at all three refinement levels; linear/PCHIP sensitivity does not create a support violation or qualitative representation failure.

### `CALIBRATION-SENSITIVE`

The chamber is reproducible, but interpolation choice or native-grid sparsity materially changes the cross-refinement comparison.

### `CALIBRATION-INVALID`

A mandatory source, support, unit, symmetry, or interpolation requirement fails.

These are **representation-calibration verdicts only**.

The labels

```text
CONTINUITY-SUPPORTED
ISOLATION-SUPPORTED
```

are prohibited for VREF-I/A.

---

## 16. Required outputs

The VREF-I/A chamber must produce:

```text
output/tables/VREF_A_GRID.csv
output/tables/VREF_A_PROFILE.csv
output/tables/VREF_A_WINDOWS.csv
output/tables/VREF_A_REFINEMENT.csv
output/reports/VREF_A_REPORT.md
output/figures/VREF_A_PROFILE.png
output/figures/VREF_A_DISTANCE.png
```

The implementation must also save a machine-readable run record containing:

- source hashes;
- frozen constants;
- interpolation rule;
- grid;
- window definition;
- software version;
- run timestamp;
- outcome class.

---

## 17. Explicit exclusions

VREF-I/A must not:

- use the R1-only tail beyond the three-level common support in a primary metric;
- normalize profiles by their own peak, norm, integral, or first point;
- alter \(\ell_{\rm ref}\), \(W\), \(m\), offsets, grid, or interpolation after seeing the chamber result;
- infer a physical Yang–Mills mass gap;
- infer structural vacuum continuity;
- compare against CORR-I in the primary calibration result;
- modify STRUC-I.

---

## 18. Freeze statement

The VREF-I/A calibration protocol is frozen with:

\[
\ell_{\rm ref}=d=0.511\ {\rm fm},
\]

\[
u_j=j/8,\quad j=0,\ldots,8,
\]

\[
W=0.5,\quad m=5,
\]

\[
\xi=\{0,0.125,0.25,0.375,0.5\},
\]

and piecewise linear interpolation as the primary common-grid map.

The next permitted step is implementation and execution of **VREF-I/A only**.

A separate source and separate preregistration are required before **VREF-I/B — Structural Vacuum Accessibility** may be run.
