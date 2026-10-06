# PREREG_YM3B.md

## UNNS Yang–Mills Gap / Vacuum Boundary Non-Crossability
### YM-3B Supplementary Preregistration — Class B Measured-Data Refinement

**Project:** `UNNS_YM_GAP`  
**Stage:** YM-3B — measured correlator/effective-mass refinement  
**Supplementary preregistration:** `YM3B-PREREG v0.1.0`  
**Frozen chamber:** CORR-I v0.1.2  
**Primary evidence class:** B — published effective-mass trajectories  
**Status:** FROZEN BEFORE DIGITIZATION / CORR-I EXECUTION  
**Date:** 2026-09-30

---

## 1. Purpose

YM-3A established:

> **The massive-side CORR-I signature is persistent across the AT20 mass-anchored Class C refinement sequence.**

That result is model-refinement evidence only.

YM-3B now asks the measured-data question:

> **Does the massive-side CORR-I separation persist across an ordered sequence of published Yang–Mills effective-mass trajectories?**

No YM-3B CORR-I result may be inspected until the source, digitization, reconstruction,
common-refinement, uncertainty, adversary, and outcome rules below are frozen.

---

## 2. Admitted primary source

The primary YM-3B source is:

**Keita Sakai and Shoichi Sasaki,  
“Glueball spectroscopy in lattice QCD using gradient flow,”  
Physical Review D 107, 034510 (2023),  
arXiv:2211.15176, DOI: 10.1103/PhysRevD.107.034510.**

The admitted sequence is pure SU(3) Yang–Mills with the standard Wilson plaquette action.

Published refinement levels:

| beta | lattice | a [fm] | r0/a | physical extent La [fm] |
|---:|---:|---:|---:|---:|
| 6.20 | 24^3 x 24 | 0.0677(3) | 7.38(3) | 1.62 |
| 6.40 | 32^3 x 32 | 0.0513(3) | 9.74(5) | 1.64 |
| 6.71 | 48^3 x 48 | 0.0345(2) | 14.49(10) | 1.66 |
| 6.93 | 64^3 x 64 | 0.0256(2) | 19.48(12) | 1.64 |

The physical volume is approximately fixed across the sequence. This reduces, but does not
eliminate, finite-volume confounding.

The admitted channel is only:

`A1++ ground state` = continuum `0++` scalar glueball = mass-gap channel.

Published effective-mass figures:

- Figure 9 — beta 6.20
- Figure 10 — beta 6.40
- Figure 11 — beta 6.71
- Figure 12 — beta 6.93

The figures are the source for the Class B trajectories.

Published fit anchors from Table VII:

| beta | aM(0++) | fit range |
|---:|---:|---:|
| 6.20 | 0.5198(67) | [2, 8] |
| 6.40 | 0.4025(62) | [3, 8] |
| 6.71 | 0.2664(45) | [3, 10] |
| 6.93 | 0.1970(36) | [3, 12] |

These mass values are verification anchors. They are not substitutes for the digitized trajectories.

---

## 3. Why this source is admitted as Class B

The paper publishes effective-mass trajectories derived from a variational analysis of a 6 x 6
correlation matrix. The matrix is constructed from the fish-shaped gauge-invariant operator
at six different spatial-gradient-flow iterations.

For the variational eigenvalue lambda_n(t,t0), with t0/a = 0, the published effective mass is

M_eff(t) = log[ lambda(t,t0) / lambda(t+1,t0) ].

Therefore the published effective-mass trajectory can be reconstructed into a normalized
eigen-correlator proxy without assuming an exact single exponential.

This is Class B evidence:

- more informative than a fitted mass alone;
- less complete than the raw correlation matrix and covariance;
- suitable for a published-figure reconstruction with explicit provenance.

It must never be described as raw correlator data.

---

## 4. Frozen refinement axes

### R1 — primary lattice-spacing refinement

Ordered by decreasing lattice spacing:

6.20 -> 6.40 -> 6.71 -> 6.93

or equivalently

a/r0:
1/7.38 -> 1/9.74 -> 1/14.49 -> 1/19.48 -> 0.

This supplies four ordered Class B refinement levels.

### R3 — independent ladder-resolution refinement

The second refinement axis is nested sampling on the common physical-time grid.

Three nested ladders are frozen:

- R3-L5: first 5 common-grid points
- R3-L6: first 6 common-grid points
- R3-L7: all 7 common-grid points

The R3 test asks whether the sign and ordering of the measured-vs-gapless separation is stable
as ladder resolution/length is increased without changing the source trajectory.

R3 is a sensitivity/refinement axis. The primary YM-3B verdict is based on R3-L7 and must
remain qualitatively compatible with L5 and L6.

---

## 5. Frozen digitization protocol

Only the top-left `A1++` panel of Figures 9–12 is digitized.

For each beta:

1. render the publication PDF at high resolution;
2. crop the top-left panel;
3. calibrate x and y axes using labeled tick marks;
4. extract only the **ground-state** marker centers;
5. extract vertical error-bar endpoints where graphically resolvable;
6. retain native integer `t/a` locations;
7. record every extracted pixel coordinate and axis calibration in JSON;
8. do not infer missing points;
9. do not smooth the native effective-mass data before reconstruction;
10. do not use the first-excited-state trajectory in the primary run.

If a point cannot be unambiguously separated from another marker/error bar, it is recorded as
`NA` and excluded rather than guessed.

Digitization resolution uncertainty is the larger of:

- half a rendered pixel mapped into the y coordinate;
- the uncertainty implied by ambiguity in the marker center.

Published graphical error bars, when extractable, are stored separately from digitization uncertainty.

---

## 6. Native Class B reconstruction

For each beta, let the digitized ground-state effective mass be `m_eff(t)`.

Set:

lambda(0) = 1

and reconstruct recursively:

lambda(t+1) = lambda(t) * exp[-m_eff(t)].

This follows the effective-mass definition used for the variational eigenvalues in the admitted
figures.

The reconstruction is normalized. Absolute operator normalization is not used.

The native reconstructed object is labelled:

`Class B / published-effective-mass reconstruction`.

---

## 7. Physical-time normalization

Define the dimensionless physical-time coordinate

u = t * a/r0 = t / (r0/a).

The literature `r0/a` values quoted by Sakai-Sasaki are frozen:

- beta 6.20: 7.38
- beta 6.40: 9.74
- beta 6.71: 14.49
- beta 6.93: 19.48

No refit of the scale is allowed after seeing CORR-I results.

---

## 8. Frozen common-refinement window

The published Table-VII fit windows imply the following plateau-supported physical-time ranges:

- beta 6.20: [2/7.38, 8/7.38]
- beta 6.40: [3/9.74, 8/9.74]
- beta 6.71: [3/14.49, 10/14.49]
- beta 6.93: [3/19.48, 12/19.48]

Their common overlap contains approximately:

u in [0.308, 0.616].

The primary common grid is frozen before digitization as:

u = 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61.

Thus:

- common spacing: Delta u = 0.05;
- common points: 7;
- all points lie inside the published fitted-plateau support for all four beta values.

---

## 9. Frozen interpolation rule

Interpolation is performed only after reconstructing the native normalized `lambda(t)`.

Primary interpolation:

- piecewise linear interpolation of `log(lambda)` as a function of `u`.

No extrapolation outside native support is permitted.

Sensitivity interpolation:

- monotone PCHIP interpolation of `log(lambda)` where the native reconstruction is monotone.

Both methods are preregistered now. The linear method is primary. PCHIP is a sensitivity check.

If the two methods reverse the sign of the measured-vs-gapless separation at any beta,
the YM-3B result is labelled `INTERPOLATION-SENSITIVE`.

---

## 10. Common-grid normalization

After interpolation to the common grid, normalize the first common-grid point:

C_B(u0) = 1.

All later common-grid values are divided by the same first-point value.

This removes arbitrary eigenvector/operator normalization while preserving the measured decay shape.

---

## 11. CORR-I chamber freeze

Use CORR-I v0.1.2 mathematically unchanged.

No threshold, plateau rule, positivity test, Hankel/Hausdorff rule, adversarial scan coordinate,
or `R_contract` definition may be altered for YM-3B.

The chamber hash must match the frozen YM-3A hash before execution:

`f972c9d460cebc19ef165e66c03f971411062eba093876406ed2efe614e2deb2`

---

## 12. Measured-data baseline handling

Because Class B trajectories are digitized published measurements, exact positive-spectral moment
conditions may be more sensitive to graphical/statistical noise than the underlying raw correlator.

Therefore each beta records, without concealment:

- positivity;
- monotonicity;
- log-convexity;
- effective-mass behavior;
- plateau behavior;
- Hankel/Hausdorff tests;
- baseline classification.

A `SPECTRAL-POSITIVITY TENSION` verdict does not automatically discard the envelope, provided:

- all reconstructed C values are positive;
- the reconstruction is finite;
- no input is missing on the seven-point common grid.

This is the same provenance discipline used for the AT20 Figure-7 Class B proxy.

---

## 13. Frozen gapless adversarial family

For each beta, construct the same Gamma family:

p = 0.5, 1, 2, 4, 8.

On the common physical-time coordinate u:

C_p(u) = (1 + theta_p * (u-u0))^(-p).

The local target scale is the published fitted ground-state mass expressed in r0 units:

m_ref(beta) = [aM(beta)] * [r0/a(beta)].

For common spacing Delta u = 0.05, choose theta_p so that the first-interval effective mass equals
the beta-matched target:

theta_p = [exp(m_ref * Delta u / p) - 1] / Delta u.

Thus every adversary is:

- positive spectral;
- exactly gapless;
- beta-matched to the measured physical mass scale;
- evaluated on the identical common grid.

No p value may be added after seeing the results.

---

## 14. Frozen primary metric

For each beta record:

R_B(beta) = R_contract of the reconstructed Class B trajectory.

For the hardest matched gapless control:

R_8(beta) = R_contract of p=8.

Define the boundary-separation coordinate

S_B(beta) = log10[ R_8(beta) / R_B(beta) ].

Interpretation:

- S_B > 0: measured massive-side response remains more contracted than the hardest matched gapless control;
- S_B = 0: boundary contact;
- S_B < 0: measured response has crossed the hardest matched gapless response.

Track S_B against a/r0.

This is the explicit YM-3B boundary-tracking output.

---

## 15. Digitization / no-covariance sensitivity ensemble

The publication does not supply the full covariance of the plotted effective masses.

A descriptive sensitivity ensemble is therefore preregistered:

- seed: 20260930;
- draws: 2000;
- use published graphical pointwise errors when extractable;
- otherwise use digitization uncertainty only;
- draw positive effective masses from independent normal perturbations around the digitized central values;
- reconstruct and interpolate each draw identically;
- record the distribution of R_B and S_B.

This ensemble is explicitly **not** a covariance-correct confidence interval.

It is a pointwise-no-covariance robustness diagnostic.

---

## 16. Run order

The scientific run order is frozen:

1. digitize all four beta panels;
2. save raw pixel/calibration records;
3. reconstruct all four native Class B sequences;
4. verify fitted-plateau consistency against Table VII;
5. construct all four seven-point common-grid inputs;
6. construct all 20 matched Gamma controls;
7. verify CORR-I hash;
8. run all four measured inputs and all matched controls;
9. only after the batch is complete inspect R_B, S_B, ordering, and R3 sensitivity;
10. run the 2000-draw uncertainty sensitivity ensemble last.

No beta may be interpreted early.

---

## 17. Frozen admission checks before CORR-I execution

A beta is admitted only if:

- at least the full seven-point common grid lies inside native published support after interpolation;
- all common-grid C values are positive and finite;
- the reconstructed plateau scale is compatible with the published Table-VII mass within
  digitization/graphical uncertainty;
- provenance files are complete.

If fewer than three beta levels survive admission, YM-3B is not executed as a refinement test.

---

## 18. Frozen outcome language

### DATA-REFINEMENT PERSISTENT

Allowed only if:

1. at least three ordered beta levels are admitted;
2. S_B(beta) > 0 at every admitted level;
3. no R3-L5/L6/L7 sequence reverses the sign of S_B;
4. linear and PCHIP interpolation do not reverse the sign;
5. no systematic approach to S_B = 0 is seen toward finer lattice spacing within the validated range;
6. the finest admitted level remains separated from p=8.

Allowed statement:

> **The massive-side CORR-I separation persists across the admitted Class B measured effective-mass refinement sequence.**

### DATA-REFINEMENT ERODING

Used if S_B remains positive at coarse levels but systematically approaches boundary contact,
or if the finest levels become compatible with S_B = 0 under the preregistered sensitivity checks.

### DATA-REFINEMENT CROSSED

Used if S_B < 0 at any admitted level under the primary analysis and the crossing is not attributable
to a failed baseline/provenance check.

### INTERPOLATION-SENSITIVE

Used if the sign of S_B depends on the preregistered interpolation rule.

### DATA-INDETERMINATE

Used if fewer than three levels survive admission, digitization uncertainty dominates the sign,
or source quality prevents a stable boundary statement.

---

## 19. Claim boundary

Even `DATA-REFINEMENT PERSISTENT` would not prove the Yang–Mills mass gap.

It would establish measured-data refinement persistence of the frozen CORR-I discriminator across
an independent four-level Class B sequence.

The Hamiltonian bridge remains YM-4.

---

## 20. Freeze statement

As of 2026-09-30, the source, channel, four beta levels, R1 and R3 axes, digitization procedure,
effective-mass reconstruction, physical-time normalization, common window, seven-point grid,
interpolation rules, Gamma adversaries, boundary coordinate, uncertainty sensitivity, run order,
admission checks, and outcome language above are frozen before any YM-3B CORR-I result is inspected.
