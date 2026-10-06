# SOURCE_ADMISSION.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Record:** VREF-I/A source admission  
**Status:** **FROZEN — ADMITTED FOR CALIBRATION / REFINEMENT VALIDATION ONLY**  
**Source ID:** `BAKER_2022_SU3`  
**Freeze date:** 2026-09-30

---

## 1. Admission decision

The Baker et al. 2022 pure-gauge SU(3) dataset is admitted as the first Stage-2 physical source for:

> **VREF-I/A — refinement / continuum-scaling calibration**

It is **not admitted as the primary structural-vacuum-continuity source**.

The source is used to test whether the VREF-I representation, common-grid mapping, interpolation rule, uncertainty propagation, and refinement comparison behave coherently across three lattice resolutions describing the same physical source separation.

No result from VREF-I/A may be promoted into a Stage-2 structural-vacuum-continuity verdict.

---

## 2. Canonical source

M. Baker, V. Chelnokov, L. Cosmai, F. Cuteri, A. Papa,  
**“Unveiling confinement in pure gauge SU(3): flux tubes, fields, and magnetic currents,”**  
*European Physical Journal C* **82**, 937 (2022).  
DOI: `10.1140/epjc/s10052-022-10848-2`  
arXiv: `2207.08797`

Local canonical source package:

```text
data/raw/baker_2022/
```

The paper states that the numerical tables for all plots are provided in the `anc` subfolder of the arXiv source archive.

---

## 3. Physical provenance

The source is pure SU(3) gauge theory.

The color-field distributions are obtained from the connected Wilson-loop–plaquette correlator. The paper states that this connected correlator supplies a lattice definition of a gauge-invariant field-strength tensor.

The admitted profile is the longitudinal non-perturbative field

\[
E_x^{NP}(x_t)
\]

at

\[
x_l=d/4\approx0.128\ \mathrm{fm}.
\]

The non-perturbative field is defined by the source as

\[
\mathbf E^{NP}=\mathbf E-\mathbf E^C,
\]

where \(\mathbf E^C\) is the curl-free Coulomb-like component.

Therefore the admitted observable is a **published derived gauge-invariant field component**, not the primitive unsubtracted full field.

This distinction is retained explicitly in all later VREF-I records.

---

## 4. Refinement branch

All three source ensembles use the same physical quark–antiquark separation

\[
d=0.511\ \mathrm{fm}.
\]

The admitted refinement levels are:

| Level | \(\beta\) | \(a\) [fm] | \(d/a\) | physical \(d\) [fm] |
|---|---:|---:|---:|---:|
| R1 | 6.240 | 0.0639 | 8 | 0.511 |
| R2 | 6.544 | 0.0426 | 12 | 0.511 |
| R3 | 6.769 | 0.0320 | 16 | 0.511 |

The ordering

\[
R1\rightarrow R2\rightarrow R3
\]

means decreasing lattice spacing / increasing spatial resolution.

---

## 5. Exact admitted numerical files

Only the following three `anc` tables define the primary VREF-I/A profile branch:

```text
anc/EX_NP_xl0.128_beta6.240.dat
anc/EX_NP_xl0.128_beta6.544.dat
anc/EX_NP_xl0.128_beta6.769.dat
```

Their SHA-256 checksums in the uploaded arXiv source archive are:

```text
6.240  7188b65ff3ad25c60d7996fd96d69bab8f246eb6a960d4c442fb102b5b56d47e
6.544  d72f075c6cc3d0dab00da9175101a53658f807cbdc9fc74563dac604747ebb59
6.769  c572706572cc06aeb5b163306e3beeeecd37a0f27ff8c76687ad7d6dff194a39
```

Uploaded arXiv archive SHA-256:

```text
258414998761aa954417784c09c94aff95220943044a11fa0bebdbe7d4b2a081
```

---

## 6. Column format

Each admitted file has exactly three numerical columns:

```text
# XT [fm]    EX_NP [GeV^2]    EX_NP_ERROR [GeV^2]
```

Therefore:

1. `XT` — transverse spatial coordinate \(x_t\), in fm;
2. `EX_NP` — published \(E_x^{NP}\), in GeV\(^2\);
3. `EX_NP_ERROR` — one symmetric pointwise published error scale, in GeV\(^2\).

The table itself does **not** split the third column into statistical and systematic pieces.

For VREF-I/A it is therefore retained exactly as:

> **published pointwise symmetric error**

and is not silently re-labelled as a complete uncertainty budget.

The primary propagation rule below does not require interpreting the column as Gaussian or as an exact 68% confidence interval.

---

## 7. Native support

The three tables contain:

| \(\beta\) | rows | non-negative \(x_t\) rows | native support [fm] |
|---|---:|---:|---:|
| 6.240 | 33 | 17 | \([-1.022434,+1.022434]\) |
| 6.544 | 25 | 13 | \([-0.511477,+0.511477]\) |
| 6.769 | 33 | 17 | \([-0.511238,+0.511238]\) |

The negative and positive branches are exact numerical mirrors in the supplied tables: corresponding \(E_x^{NP}\) central values and error values are duplicated.

Accordingly, the primary VREF-I/A branch uses only

\[
x_t\ge0
\]

to avoid counting the same transverse profile information twice.

The negative branch is retained only as an ingestion/symmetry integrity check.

---

## 8. Common physical support

The primary three-level common support is frozen as

\[
0\le x_t\le 0.511\ \mathrm{fm}.
\]

This lies inside all three native supports.

No VREF-I/A value may be extrapolated beyond measured support.

The longer R1 tail extending to \(1.022434\) fm is preserved in the raw data but is excluded from the primary three-level comparison because R2 and R3 do not measure that region.

---

## 9. Vacuum reference

The Stage-1 VREF-I convention is retained:

\[
V_r^*=0
\]

in vacuum-referenced coordinates.

For this source, \(E_x^{NP}=0\) is the field-free reference of the published non-perturbative component.

However, the common three-resolution support does **not** extend to an independently demonstrated vacuum-compatible asymptotic region.

Therefore:

```text
VREF-I/A may test refinement stability.
VREF-I/A may not issue CONTINUITY-SUPPORTED or ISOLATION-SUPPORTED.
```

The source is not permitted to establish or reject Structural Vacuum Continuity.

---

## 10. Source-admission verdict

\[
\boxed{\texttt{BAKER\_2022\_SU3 = ADMITTED FOR VREF-I/A}}
\]

with role:

```text
REFINEMENT / CONTINUUM-SCALING CALIBRATION
```

and restriction:

```text
NO PRIMARY VACUUM-CONTINUITY VERDICT
```

This admission is frozen before implementation of the VREF-I/A chamber.
