# YANAGIHARA_EMT_FREEZE.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Branch:** EMT-I — Independent Vacuum-Subtracted Representation  
**Source ID:** `YANAGIHARA_2019_EMT`  
**Status:** **FROZEN BEFORE VECTOR EXTRACTION / OUTCOME INSPECTION**  
**Date:** 2026-10-05

---

## 1. Purpose

EMT-I is the independent-representation test required by the Stage-2 architecture.

The preceding connected-field evidence is:

```text
CEA_2017 VREF-I/B:
REFINEMENT-INDETERMINATE

CEA_2017 STRUC:
ARCHITECTURE-PRESERVED

BATTELLI_2019:
UNSMOOTHED-ARCHITECTURE-CONSISTENT
```

EMT-I changes the physical observable itself.

It asks:

> Does a continuum-extrapolated, gauge-invariant, explicitly vacuum-subtracted Yang-Mills energy-momentum-tensor representation also approach the zero-vacuum structural locus in the transverse direction?

It is not a new test of the physical Yang-Mills Hamiltonian mass gap.

---

## 2. Source

R. Yanagihara, T. Iritani, M. Kitazawa, M. Asakawa, T. Hatsuda,  
**“Distribution of Stress Tensor around Static Quark–Anti-Quark from Yang-Mills Gradient Flow,”** Phys. Lett. B 789 (2019) 210–214, arXiv:1803.05656v5.

Only the final v5 representation is admissible.

The final revision is required because Fig. 3 was corrected before publication.

Canonical local source folder:

```text
data/raw/yanagihara_2019/
```

The already acquired final paper/source assets remain the provenance basis.

---

## 3. Why this representation is independent

The representation is the renormalized Yang-Mills energy-momentum tensor obtained through gradient flow and a continuum / zero-flow double limit.

It is not defined by:

- CORR-I;
- the Gamma adversary;
- the CEA connected-field amplitude;
- the Battelli connected-field ladder;
- the VREF-I/B zero-floor fit.

The source constructs the renormalized EMT from flowed gauge fields and explicitly subtracts the vacuum expectation contribution.

Therefore its vacuum expectation is operationally normalized to:

\[
\boxed{\langle T_{\mu\nu}^{R}\rangle_0=0}.
\]

This supplies an independent physical zero-vacuum coordinate.

---

## 4. Continuum status

The published transverse EMT profiles are continuum / zero-flow results.

The source obtains:

\[
\langle T_{\mu\nu}^{R}(x)\rangle_{Q\bar Q}
=
\lim_{t\to0}\lim_{a\to0}
\langle T_{\mu\nu}(t,x)\rangle_{Q\bar Q}^{\rm lat}.
\]

Therefore EMT-I is **not** a third finite-lattice refinement chamber.

Its role is representation independence after the source's own continuum extrapolation.

The absence of recoverable per-lattice transverse profile tables remains a hard restriction:

```text
EMT-I cannot independently reconstruct the finite-a tail refinement sequence.
```

That requirement is already covered separately by the Stage-2 VREF/refinement branches.

---

## 5. Primary geometry

Freeze the primary physical separation as:

\[
\boxed{R=0.69\ {\rm fm}}.
\]

Reasons fixed before extraction:

1. it is the central physical separation among the source's principal reported values;
2. it is neither the shortest nor longest source geometry;
3. it has multiple lattice realizations in the source continuum program;
4. it was already selected during source admission before the EMT outcome was inspected for this project.

The other published separations, where vector-recoverable, are secondary representation-sensitivity checks only.

They may not replace the primary branch after the result is known.

---

## 6. Physical EMT coordinates

Define the physical coordinate vector on the transverse mid-plane:

\[
Y(r)=
\left(
\varepsilon(r),
\sigma_{zz}(r),
\sigma_{rr}(r),
\sigma_{\theta\theta}(r)
\right),
\]

with

\[
\varepsilon=-T_{44},
\qquad
\sigma_{ij}=-T_{ij}.
\]

No sign is discarded in the stored component table.

The vacuum coordinate is:

\[
Y_{\rm vac}=(0,0,0,0).
\]

---

## 7. Primary scalar representation

The primary EMT-I structural distance at each transverse coordinate is the Euclidean component norm

\[
\boxed{
D_{\rm EMT}(r)
=
R^4
\sqrt{
\frac{
\varepsilon(r)^2+
\sigma_{zz}(r)^2+
\sigma_{rr}(r)^2+
\sigma_{\theta\theta}(r)^2
}{4}
}
}.
\]

This definition:

- preserves absolute component amplitude;
- does not peak-normalize;
- does not divide by the central value;
- does not privilege one stress component;
- is zero if and only if all four admitted EMT components are zero.

The factor \(R^4\) makes the distance dimensionless in natural units once the physical unit conversion is applied.

For monotonicity and zero-floor classification, any overall positive unit-conversion factor cancels qualitatively. The executable extraction record must nevertheless state the exact unit convention used.

---

## 8. Component-level cross-check

The primary component cross-check is the energy density:

\[
\boxed{
D_{\varepsilon}(r)=R^4|\varepsilon(r)|
}.
\]

Secondary checks retain the three stress components individually.

A positive EMT-I result requires that no individual component demonstrates a robust nonzero outer floor that is hidden by the vector norm.

---

## 9. Deterministic vector extraction

Primary extraction asset:

```text
mid_separates.pdf
```

from the final Yanagihara source package.

The already established source inspection showed that this is a genuine vector figure, not a raster screenshot.

The extraction must recover:

```text
r
component central value
published error bar
physical separation R
component identity
```

directly from vector geometry.

Prohibited:

- OCR;
- raster WebPlotDigitizer extraction;
- tracing a fit curve instead of point markers;
- using the visual axis by hand when exact vector coordinates are available;
- replacing v5 with an earlier revision.

The extractor must produce:

```text
data/derived/yanagihara_2019/YAN19_EMT_POINTS.csv
data/derived/yanagihara_2019/YAN19_EMT_EXTRACT.json
```

No scientific EMT-I verdict may be calculated during extraction.

---

## 10. Common-coordinate rule

The four EMT components must be evaluated only on transverse coordinates represented by all four components in the primary \(R=0.69\) panel.

If the vector asset uses identical native coordinates for all components, those coordinates are used directly.

If one component is sampled at a different coordinate set, freeze the primary common grid as the sparsest component-native coordinate set restricted to mutual support, and map the remaining components by piecewise linear interpolation.

Mandatory interpolation sensitivity:

```text
PCHIP
```

No extrapolation is allowed.

If linear/PCHIP changes the qualitative EMT-I verdict:

```text
EMT-INTERPOLATION-SENSITIVE
```

---

## 11. Vacuum-directed path test

For the extracted common coordinates:

\[
r_0<r_1<\cdots<r_n,
\]

compute:

\[
D_{\rm EMT}(r_i).
\]

The primary path criterion is vacuum-directed if the fixed representation shows no statistically material outward reversal.

A reversal is material only when the lower uncertainty envelope of the later point lies above the upper uncertainty envelope of the preceding point.

All eligible outward points are audited.

No favorable subset may be selected after extraction.

---

## 12. Outer-tail floor comparison

The outer-tail cut is fixed geometrically as:

\[
\boxed{r\ge R/2=0.345\ {\rm fm}}.
\]

This is chosen from the source geometry, not from the extracted EMT amplitudes.

Two preregistered model families are used for the primary scalar distance:

### Exponential family

\[
M_{E0}: D(r)=Ae^{-r/\lambda}
\]

versus

\[
M_{E\delta}: D(r)=\delta+Ae^{-r/\lambda},
\qquad \delta\ge0.
\]

### Bessel family

\[
M_{K0}: D(r)=A K_0(r/\lambda)
\]

versus

\[
M_{K\delta}: D(r)=\delta+A K_0(r/\lambda),
\qquad \delta\ge0.
\]

Use diagonal-error weighted fitting because the published cross-component covariance matrix is unavailable.

Rank models by AICc.

Freeze:

\[
\Delta_{\rm floor}
=
{\rm AICc}(M_\delta)-{\rm AICc}(M_0).
\]

Decisive threshold:

\[
\boxed{|\Delta_{\rm floor}|\ge6}.
\]

Positive \(\Delta_{\rm floor}\) favors zero floor.

Negative \(\Delta_{\rm floor}\) favors positive floor.

If the extracted tail has too few points for a valid AICc comparison in either family, do not invent a lower threshold; return:

```text
EMT-DATA-LIMITED
```

---

## 13. Tail-cut sensitivity

The only preregistered tail sensitivity is:

```text
drop the first eligible outer-tail coordinate
```

and repeat the same two model families.

No further tail cut is permitted.

A robust representation result requires the floor classification not to reverse under this sensitivity.

---

## 14. Component-consistency rule

After the primary vector-norm result is frozen, inspect each component individually.

Allowed component labels:

```text
VACUUM-DIRECTED
NONZERO-FLOOR
UNCERTAINTY-LIMITED
NONMONOTONE
```

The project-level EMT result is blocked from `EMT-CONTINUITY-CONSISTENT` if any component shows a decisive `NONZERO-FLOOR`.

A sign change of a stress component is not by itself a failure. The question is its structural distance from zero in the tail.

---

## 15. Frozen EMT-I outcomes

Allowed branch statuses:

```text
EMT-CONTINUITY-CONSISTENT
EMT-POSITIVE-FLOOR
EMT-REPRESENTATION-SPLIT
EMT-INTERPOLATION-SENSITIVE
EMT-DATA-LIMITED
EMT-UNCERTAINTY-LIMITED
EMT-EXTRACTION-INVALID
```

### EMT-CONTINUITY-CONSISTENT

Requires:

1. valid deterministic vector extraction;
2. vacuum-directed \(D_{\rm EMT}(r)\);
3. no interpolation-sensitive qualitative reversal;
4. both tail-model families favor zero floor decisively, or the finite measured tail reaches a statistically vacuum-compatible regime strongly enough that both positive-floor fits collapse to zero under the frozen uncertainty model;
5. no individual EMT component supports a robust positive floor;
6. the conclusion survives the one frozen tail-cut sensitivity.

### EMT-POSITIVE-FLOOR

Requires:

1. valid extraction;
2. both tail-model families decisively favor \(\delta>0\);
3. the positive floor survives tail-cut sensitivity;
4. component-level analysis is compatible with a nonzero outer structural floor.

### EMT-REPRESENTATION-SPLIT

The vector-norm result and one or more independent EMT components imply materially incompatible vacuum topology.

### EMT-DATA-LIMITED / EMT-UNCERTAINTY-LIMITED

Used when the published continuum figure cannot support the preregistered asymptotic comparison or its errors do not distinguish the alternatives.

---

## 16. Relation to the Stage-2 hypothesis

EMT-I is the first branch in this project whose physical observable is not a connected chromoelectric-field profile.

Therefore it is the critical independent-representation check required by the frozen Stage-1 standard:

\[
D_{\rm struct}(X_n,V)\to0
\]

should survive representation change.

The branch may strengthen or weaken the structural-continuity case, but it cannot by itself establish a mathematical Yang-Mills mass gap.

---

## 17. No-retuning rule

After vector extraction begins, do not:

- change \(R=0.69\) fm as the primary geometry;
- change the four-component EMT vector;
- peak-normalize any component;
- remove a component because its sign is inconvenient;
- shift the vacuum away from zero;
- alter the \(r\ge R/2\) tail cut;
- add a third asymptotic family;
- change the \(|\Delta{\rm AICc}|=6\) threshold;
- reinterpret the source's continuum extrapolation as a new finite-\(a\) refinement test.

---

## 18. Next permitted action

The next permitted operation is:

```text
deterministic vector extraction of mid_separates.pdf
```

from the final Yanagihara v5 source assets.

Only after:

```text
EMT EXTRACTION = VALID
```

may an EMT-I scientific fit or verdict be produced.
