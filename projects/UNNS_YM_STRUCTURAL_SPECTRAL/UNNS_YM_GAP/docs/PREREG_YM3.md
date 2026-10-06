# PREREG_YM3.md

## UNNS Yang–Mills Gap / Vacuum Boundary Non-Crossability
### YM-3 Common Refinement — Frozen Preregistration

**Project:** `UNNS_YM_GAP`  
**Preregistration version:** `YM3-PREREG v0.1.0`  
**Freeze date:** 2026-09-30  
**Stage entering:** YM-3 — Common Refinement  
**Frozen chamber:** CORR-I v0.1.2  
**Prior stage record:** `docs/SYNTHESIS_YM2.md`  
**Input provenance table:** `docs/YM3_INPUT_MATRIX.csv`

---

## 1. Question frozen before the YM-3 run

The YM-3 question is:

\[
\boxed{
\text{Does the massive-side CORR-I signature persist across the eight AT20 lattice refinements?}
}
\]

The project hypothesis remains unchanged:

> **Gapless Yang–Mills continuation is structurally non-generable under refinement, whereas the massive branch is refinement-stable.**

YM-3 does not ask whether every AT20 lattice spacing has a nonzero fitted mass. That fact is already present in the source corpus. It asks whether the **same correlator-side structural separation identified in YM-2** survives an ordered refinement sequence without changing the frozen chamber or selecting a favorable normalization after viewing the results.

---

## 2. Scope split: YM-3A and YM-3B

The current AT20 package does not contain raw correlator matrices across all eight β values. The evidence classes must therefore remain explicit.

### YM-3A — mass-anchored model refinement

Run the full eight-β sequence using **Class C** exact single-exponential controls anchored only to the published fitted \(0^{++}\) masses.

Purpose:

- test whether CORR-I behaves coherently across the published refinement backbone;
- test whether the YM-2 massive-side signature persists in a common physical-time representation;
- expose any lattice-window or normalization dependence before claiming a physical refinement result;
- establish a reproducible model-level bridge from YM-2 to a later data-level refinement test.

A positive YM-3A result is **not** a refinement test of eight measured Yang–Mills correlators. It is a refinement test of the **AT20 mass-anchored model family**.

### YM-3B — measured correlator/effective-mass refinement

A physical refinement claim requires Class A and/or Class B evidence at multiple ordered refinement levels. In the present package:

- **Class A:** none available across the eight-level AT20 sequence;
- **Class B:** β = 6.50 Figure-7 \(0^{++}\) effective-mass reconstruction only;
- **Class C:** available at all eight β values.

YM-3B therefore remains **not yet executable from the present AT20 package alone**. It will require additional raw/published correlator-level information or published effective-mass trajectories at further β values. No Class C-only result may be relabeled as YM-3B.

---

## 3. Frozen refinement backbone

The eight ordered refinement levels are:

| β | \(a\sqrt{\sigma}\) | \(aM_{0^{++}}\) | \(M_{0^{++}}/\sqrt{\sigma}\) | Current evidence |
|---:|---:|---:|---:|---|
| 5.6924 | 0.39990 | 0.9870 | 2.468117029 | C |
| 5.8000 | 0.31666 | 0.9080 | 2.867428788 | C |
| 5.8941 | 0.26118 | 0.7991 | 3.059575771 | C |
| 5.9900 | 0.21982 | 0.7045 | 3.204894914 | C |
| 6.0625 | 0.19472 | 0.6365 | 3.268796220 | C |
| 6.2350 | 0.15003 | 0.4969 | 3.312004266 | C |
| 6.3380 | 0.12928 | 0.4276 | 3.307549505 | C |
| 6.5000 | 0.10383 | 0.3474 | 3.345853799 | B + C |

At β = 5.8941, the extracted source corpus preserves the small Table 1 / Table 8 rounding difference rather than silently reconciling it. The YM-3A central sequence uses the already frozen refinement-backbone value \(aM=0.7991\).

---

## 4. Evidence classes frozen for YM-3

### Class A — raw or published correlator-level data

Best evidence. None is presently available across the eight-level AT20 backbone in the local package.

### Class B — published effective-mass trajectories

May support reconstructed correlator proxies when provenance is explicit. The current physical-side Class B anchor is the β = 6.50 Figure-7 \(0^{++}\) ground-state reconstruction frozen in YM-2.

### Class C — exact mass-anchored model controls

For each β,

\[
C^{(C)}_\beta(t)=e^{-M_\beta t}
\]

in the chosen dimensionless time coordinate. These are controlled representations, not independent measurements.

The evidence class is carried into every filename, manifest, batch summary, and synthesis table. No class may be silently upgraded.

---

## 5. Frozen chamber and settings

CORR-I v0.1.2 remains mathematically unchanged.

Frozen chamber artifact:

`chambers/corr_i/corr_i_v012.html`

SHA-256:

`f972c9d460cebc19ef165e66c03f971411062eba093876406ed2efe614e2deb2`

Frozen visible settings for YM-3A:

| Setting | Frozen value |
|---|---:|
| PSD tolerance | `1e-10` |
| Plateau relative range | `0.05` |
| Minimum plateau points | `4` |
| α cap | `0.5` |
| μ/mref minimum | `0.001` |
| μ/mref maximum | `1` |
| μ points | `25` |
| RMS-z limit | `1` |
| max-|z| limit | `3` |
| RMS-relative limit | `0.05` |
| max-relative limit | `0.15` |

Class C inputs have no independent pointwise error model; therefore their envelope remains the CORR-I **relative-limits descriptive** envelope. This limitation is part of the preregistration, not a post-run qualification.

The α = 0 identity null must pass exactly for every YM-3 input.

---

## 6. Primary refinement-normalized representation

The primary YM-3A representation uses a common dimensionless physical-time coordinate

\[
u=t\sqrt{\sigma}.
\]

The grid is frozen by the finest AT20 refinement so that the β = 6.50 YM-2 control is preserved exactly in sampled shape:

\[
\Delta u = 0.10383,
\qquad
u_j=j\,\Delta u,
\qquad
j=0,1,\ldots,10.
\]

Thus the common observation window is

\[
0\le u\le1.0383.
\]

For each β define

\[
q_\beta=\frac{aM_\beta}{a\sqrt{\sigma}_\beta}
       =\frac{M_\beta}{\sqrt{\sigma}}.
\]

The Class C input is then

\[
\boxed{
C^{(C)}_\beta(u_j)=e^{-q_\beta u_j}.
}
\]

This construction holds the **physical-time window and sampling grid fixed** while allowing only the published dimensionless mass trajectory \(M/\sqrt{\sigma}\) to vary with refinement.

For the seven coarser β values the values on this fine common grid are analytic evaluations of the Class C model; they are **not interpolated measured correlator samples**. This is why the sequence remains Class C.

No alternate common grid may replace this primary grid after results are viewed.

---

## 7. Native-lattice diagnostic representation

A secondary, preregistered window-sensitivity diagnostic uses

\[
n=0,1,\ldots,10,
\qquad
C^{(C,native)}_\beta(n)=e^{-aM_\beta n}.
\]

This representation deliberately keeps the same number of lattice steps rather than the same physical-time window. It therefore mixes refinement with changing physical coverage and is **not** the primary YM-3A result.

Its purpose is diagnostic:

- quantify how much the CORR-I response changes when the observation window changes with lattice spacing;
- detect whether a claimed refinement effect is actually a finite-window effect.

If the primary common-physical-grid result and the native-grid diagnostic lead to qualitatively different separation conclusions, the result is labelled **WINDOW-SENSITIVE** and may not be promoted to a refinement-stable boundary claim.

---

## 8. β = 6.50 checksum rule

The common-grid β = 6.50 Class C input is a unit-representation of the already frozen YM-2 massive plateau control. Its sampled correlator values must therefore reproduce the YM-2 control values after the deterministic change of time coordinate.

Before the eight-level batch is accepted:

1. the generated β = 6.50 samples must match the frozen control to numerical precision after coordinate conversion;
2. baseline classification must remain `POSITIVE-SPECTRAL CONSISTENT`;
3. the stable plateau must remain present;
4. the α = 0 identity null must pass;
5. `R_contract` must reproduce the frozen YM-2 massive-control value within numerical serialization tolerance.

A failed checksum stops the batch before scientific interpretation.

The existing β = 6.50 Figure-7 Class B result is **not rerun merely for repetition**. A transformed copy may be run only if required as a new common-coordinate checksum, and if so it remains explicitly labelled `Class B / published-figure reconstruction`.

---

## 9. Frozen gapless references

### 9.1 Primary fixed reference family

The YM-2 positive-spectral Gamma family remains the primary gapless reference:

\[
C_p(t)=(1+\theta_p t)^{-p},
\qquad
p\in\{0.5,1,2,4,8\}.
\]

For the common \(u\) coordinate, the already frozen β = 6.50 family is transformed by units only, so that its sampled values and CORR-I results remain identical to YM-2.

The frozen reference contraction ratios are:

| Gapless reference | \(R_{contract}\) |
|---|---:|
| p = 0.5 | 0.500947 |
| p = 1 | 0.326916 |
| p = 2 | 0.178612 |
| p = 4 | 0.084534 |
| p = 8 | 0.037668 |

The `p=8` member is the **hardest frozen gapless comparator** because it was the closest tested gapless control to the massive response in YM-2.

These fixed references are not retuned after looking at the eight massive-side results.

### 9.2 Preregistered matched-control sensitivity panel

A second panel is allowed because it is frozen here **before** the YM-3A results are generated.

For each β and each \(p\in\{0.5,1,2,4,8\}\), construct a gapless Gamma correlator on the same primary grid whose first-interval effective mass equals \(q_\beta\):

\[
C_{p,\beta}(u)=(1+\theta_{p,\beta}u)^{-p},
\]

with

\[
\boxed{
\theta_{p,\beta}
=
\frac{\exp(q_\beta\Delta u/p)-1}{\Delta u}.
}
\]

Every matched control remains genuinely gapless because its spectral support reaches \(E=0\).

This panel tests whether separation survives when the initial effective-mass scale is matched independently at every β. It is a **sensitivity test**, not a replacement for the fixed primary references.

---

## 10. Frozen outputs and metrics

For every massive-side and preregistered matched gapless input record:

- baseline classification;
- positive-point count;
- monotonicity violations;
- log-convexity violations;
- plateau found / not found;
- \(m_{ref}\);
- Hankel/Hausdorff consistency;
- α = 0 identity-null status;
- full \(\alpha_{max}(\mu)\) envelope;
- \(\alpha_{max}\) at \(\mu/m_{ref}=1\);
- \(\alpha_{max}\) at \(\mu/m_{ref}=10^{-3}\);
- \(R_{contract}\).

The primary scalar separation coordinate is frozen as

\[
R_{contract}
=
\frac{\alpha_{max}(10^{-3})}{\alpha_{max}(1)}.
\]

No replacement scalar may be selected after viewing the results merely because it increases massive/gapless separation.

---

## 11. Frozen decision quantities

For each β define the fixed-reference hard margin

\[
S^{fixed}_\beta
=
\log\frac{R_{p=8}^{fixed}}{R_{massive,\beta}}.
\]

A positive value means the massive-side control contracts more strongly than the hardest frozen gapless reference.

For the matched sensitivity family define

\[
S^{match}_\beta
=
\log\frac{R_{p=8,\beta}^{match}}{R_{massive,\beta}}.
\]

No arbitrary numerical margin is introduced. The preregistered boundary is the sign of the separation relative to the hardest gapless comparator.

---

## 12. YM-3A outcome rules

### MODEL-REFINEMENT PERSISTENT

All of the following must hold on the primary common-physical grid:

1. all eight massive Class C inputs are valid CORR-I baselines;
2. the α = 0 identity null passes for all eight;
3. the massive plateau remains present for all eight;
4. \(S^{fixed}_\beta>0\) at every β;
5. \(S^{match}_\beta>0\) at every β;
6. in every matched family, the ordering remains
   \[
   R_{0.5}>R_1>R_2>R_4>R_8>R_{massive};
   \]
7. there is no refinement level at which the massive branch crosses into or beyond the hardest matched gapless response.

Allowed conclusion:

> **The massive-side CORR-I signature is persistent across the AT20 mass-anchored Class C refinement sequence.**

This remains a model-level result.

### PARTIAL MODEL PERSISTENCE

Use this outcome if the massive branch remains separated from the fixed references but the matched-control ordering or one of the eight matched hard margins fails, without a chamber/input validity failure.

Interpretation: separation exists, but some of it depends on the changing physical scale or finite window.

### WINDOW-SENSITIVE

Use this outcome if the primary common-physical-grid conclusion and the native-lattice diagnostic give qualitatively incompatible separation behavior.

### MODEL-REFINEMENT ERODING

Use this outcome if either hard margin systematically approaches zero and crosses zero at a finer level, or if the massive response becomes indistinguishable from / less contracted than the hardest matched gapless control.

### INVALID / INCONCLUSIVE

Use this outcome if the β = 6.50 checksum fails, input generation is inconsistent with the frozen equations, the identity null fails, or chamber validity is compromised.

No failed level may be discarded solely because it weakens the desired result.

---

## 13. What YM-3A cannot establish

Even a clean `MODEL-REFINEMENT PERSISTENT` result does **not** establish:

- eight-level refinement stability of measured Yang–Mills correlators;
- a Class A/B refinement-stable vacuum boundary;
- a continuum theorem;
- a Hamiltonian spectral lower bound;
- the Yang–Mills mass gap.

It establishes only that the **frozen CORR-I massive-side signature persists in the AT20 mass-anchored model sequence under the preregistered refinement representation**.

The physical claim remains reserved for YM-3B and later YM-4 bridge work.

---

## 14. YM-3B admission rule

YM-3B may begin only when the project has enough non-Class-C information for a genuine measured-data refinement comparison.

The original `REFINEMENT_PLAN.md` minimum standard remains controlling: at least three ordered levels on a primary axis when available, a second independent refinement axis, matched physical/adversarial processing, a frozen chamber, and explicit boundary tracking.

If additional Class A/B data are acquired, their interpolation/resampling and uncertainty protocol must be frozen in a supplementary preregistration **before** those new refinement results are inspected. The present YM-3A analytic common-grid rule must not be silently applied to noisy measured correlators as if they were exact functions.

---

## 15. Run order frozen before execution

1. preserve CORR-I v0.1.2 unchanged;
2. build `YM3_INPUT_MATRIX.csv` into machine-readable metadata;
3. generate the eight Class C primary common-grid inputs from the frozen AT20 values;
4. verify the β = 6.50 checksum against the frozen YM-2 massive control;
5. generate the eight native-grid diagnostic inputs;
6. transform/reuse the frozen fixed Gamma references without retuning;
7. generate the preregistered β-matched Gamma sensitivity families;
8. run the primary eight massive inputs in one CORR-I batch where possible;
9. run the matched gapless family batch(es) under the identical visible chamber settings;
10. calculate the frozen hard margins and family ordering;
11. compare primary and native-grid outcomes for window sensitivity;
12. write the result record without changing the frozen decision rules;
13. only then decide whether the evidence justifies proceeding to a data-acquisition step for YM-3B.

No scientific interpretation is to be made from partial batch output before the complete preregistered primary sequence has been generated and verified.

---

## 16. Planned project locations

New YM-3 material should use short Windows-safe names:

```text
UNNS_YM_GAP/
│
├── docs/
│   ├── PREREG_YM3.md
│   └── YM3_INPUT_MATRIX.csv
│
├── data/derived/corr_i/ym3/
│   ├── common/
│   ├── native/
│   └── matched_gapless/
│
├── scripts/ym3/
│
└── output/ym3/
```

These directories are created when the builders are implemented. The preregistration itself does not generate or inspect YM-3 scientific outputs.

---

## 17. Freeze statement

As of 2026-09-30, the equations, evidence classes, primary common grid, secondary native-grid diagnostic, fixed and matched gapless controls, CORR-I settings, recorded metrics, run order, and outcome rules above are frozen **before the YM-3A batch is constructed or interpreted**.

Any later change requires a new version of this preregistration with an explicit reason and must not overwrite this record.
