# UNNS Yang–Mills Structural–Spectral Research

This folder is the umbrella archive for two sequential UNNS investigations of the relation between the Yang–Mills vacuum, structural admissibility, and spectral discreteness in pure SU(3) gauge theory.

The research arc is:

```text
UNNS_YM_GAP
    ↓
original vacuum non-crossability hypothesis tested
    ↓
refinement-stable universal structural boundary NOT ESTABLISHED
    ↓
UNNS_VACUUM_CONTINUITY
    ↓
structural vacuum accessibility tested across independent representations
    ↓
no universal positive structural exclusion floor detected
    ↓
independent positive continuum scalar spectral scales retained
    ↓
STRUCTURAL-SPECTRAL-COEXISTENCE-SUPPORTED
```

The final synthesis is presented in:

**[Structural Accessibility and Spectral Discreteness in Pure SU(3) Yang–Mills](./Structural%20Accessibility%20and%20Spectral%20Discreteness.pdf)**  
*A UNNS Reassessment of Vacuum Non-Crossability and the Mass Gap*

A project-wide interactive evidence summary is also available as:

**[UNNS Vacuum Continuity Analytics](./UNNS_VACUUM_CONTINUITY_ANALYTICS.html)**

---

## 1. Research progression

### Project I — `UNNS_YM_GAP`

**Folder:** [`UNNS_YM_GAP/`](./UNNS_YM_GAP/)  
**Full project:** UNNS Yang–Mills Gap / Vacuum Boundary Non-Crossability  
**Status:** **CLOSED**  
**Final central hypothesis:** **NOT ESTABLISHED**

The first project tested whether the Yang–Mills mass gap corresponds to a refinement-stable non-crossable structural boundary separating the vacuum from admissible non-vacuum structure.

The investigation progressed from vacuum-anchored spectral ladders to a correlator-native chamber, CORR-I, and then through model and measured-data refinement.

Important frozen outcomes include:

- the short spectral-ladder representation did not establish vacuum-specific non-crossability;
- CORR-I separated massive controls from legitimate gapless adversaries at fixed resolution;
- Class C exact mass-anchored controls gave `MODEL-REFINEMENT PERSISTENT`;
- the decisive Class B measured-data reconstruction gave `DATA-INDETERMINATE`;
- the central Class B trajectory crossed the proposed boundary at `beta = 6.71`, but the preregistered uncertainty interval straddled zero;
- no structural-to-Hamiltonian bridge theorem was reached.

The correct terminal reading is therefore not that non-crossability was disproved, but that a universal refinement-stable structural vacuum boundary was **not established**.

See:

- [`UNNS_YM_GAP/FINAL_STATUS.md`](./UNNS_YM_GAP/FINAL_STATUS.md)
- [`UNNS_YM_GAP/docs/FINAL_SYNTHESIS.md`](./UNNS_YM_GAP/docs/FINAL_SYNTHESIS.md)

---

### Project II — `UNNS_VACUUM_CONTINUITY`

**Folder:** [`UNNS_VACUUM_CONTINUITY/`](./UNNS_VACUUM_CONTINUITY/)  
**Status:** **CLOSED / PRIMARY PROGRAM COMPLETE**

> **Archive note:** `UNNS_VACUUM_CONTINUITY/README.md` is retained as the project's early Stage-1 initialization snapshot and therefore still describes later stages as not yet open. The authoritative closed-project records are [`stage3/PROJECT_STATUS.md`](./UNNS_VACUUM_CONTINUITY/stage3/PROJECT_STATUS.md), [`stage3/PROJECT_CLOSURE.md`](./UNNS_VACUUM_CONTINUITY/stage3/PROJECT_CLOSURE.md), and [`stage3/STAGE3_SYNTHESIS.md`](./UNNS_VACUUM_CONTINUITY/stage3/STAGE3_SYNTHESIS.md).

The second project began from the correction forced by the first:

> **A mass gap separates eigenvalues, not necessarily structural neighborhoods.**

Instead of asking whether the vacuum is protected by a universal structural wall, the project tested whether vacuum-like structure is accessible from within the admissible structural domain.

Stage 2 examined multiple independent representations and controls, including:

- Baker et al. pure-SU(3) chromoelectric-field profiles;
- Cea et al. connected flux-tube profiles under common refinement;
- canonical `STRUC-I` and `STRUC-PERC-I` structural readouts;
- Battelli–Bonati unsmoothed connected-correlator data;
- Yanagihara et al. vacuum-subtracted continuum energy–momentum-tensor profiles;
- geometry sensitivity across multiple source separations.

The frozen Stage-2 synthesis is:

**`NO-UNIVERSAL-STRUCTURAL-EXCLUSION-DETECTED`**

with the structural interpretation:

**`STRUCTURAL-VACUUM-ACCESSIBILITY-SUPPORTED`**

This is an empirical statement over the tested representations. It does **not** prove a representation-independent sequence with structural distance tending to zero.

Stage 3 then retained two independent positive continuum scalar spectral scales in their native coordinates:

- `M_0++ / sqrt(sigma) = 3.405(21)` — Athenodorou–Teper;
- `r0 M_0++ = 4.16(11)(4)` — Chen et al.

No numerical conversion between the two anchors is used.

The deterministic BRIDGE-III synthesis therefore returned:

**`COEXISTENCE-SUPPORTED`**

and the project-level result:

**`STRUCTURAL-SPECTRAL-COEXISTENCE-SUPPORTED`**

---

## 2. Principal gain

The central result of the combined program is the separation of two notions that the original hypothesis implicitly tied together:

```text
structural proximity to the vacuum
        ≠
spectral proximity to the vacuum
```

Within the frozen pure-SU(3) evidence architecture, structural vacuum accessibility is supported while independent positive continuum scalar spectral scales are retained.

The final manuscript formalizes the corresponding elementary structural–spectral separation result:

- a positive spectral gap alone does not imply a structural exclusion neighborhood;
- continuity of the excitation-energy functional at the vacuum is a sufficient bridge from a gap to structural exclusion;
- a local Hölder upper bound of energy by structural distance gives a quantitative exclusion radius;
- if a genuine physical excitation sequence approaches the vacuum structurally while a positive gap persists, the relevant structural-to-spectral continuity must fail somewhere.

The hard open problem is therefore no longer “find the wall,” but to construct and study the structure-to-spectrum map

```text
Pi : S_UNNS -> Y_spec
```

and determine the relevant topology.

---

## 3. Claim boundary

The combined research **does establish/support**, at its stated empirical and mathematical levels:

- no universal positive structural exclusion floor was detected in the tested representations;
- structural vacuum accessibility is supported empirically;
- two independent continuum scalar spectral scales remain strictly positive;
- structural accessibility and spectral discreteness coexist within the frozen evidence architecture;
- a spectral gap alone does not logically require structural isolation.

The research **does not claim**:

- `V` lies in the representation-independent closure of the physical Yang–Mills excitation space as a theorem;
- the strong limit statement `H_acc^lim` has been established;
- the Yang–Mills mass gap has been proved;
- the Clay Millennium problem has been solved;
- UNNS derives the physical mass gap from structure;
- the two spectral normalizations should be converted or averaged.

---

## 4. Frozen verdict map

| Stage / branch | Frozen outcome |
|---|---|
| `UNNS_YM_GAP` final hypothesis | `NOT ESTABLISHED` |
| YM-3A / Class C refinement | `MODEL-REFINEMENT PERSISTENT` |
| YM-3B / Class B measured data | `DATA-INDETERMINATE` |
| Baker VREF-I/A | `CALIBRATION-SENSITIVE` |
| CEA VREF-I/B | `REFINEMENT-INDETERMINATE` |
| CEA structural bridge | `ARCHITECTURE-PRESERVED` |
| Battelli unsmoothed control | `UNSMOOTHED-ARCHITECTURE-CONSISTENT` |
| EMT primary branch | `EMT-UNCERTAINTY-LIMITED` |
| EMT geometry synthesis | `GEOMETRY-ROBUST-NO-FLOOR` |
| Stage 2 synthesis | `NO-UNIVERSAL-STRUCTURAL-EXCLUSION-DETECTED` |
| Stage 2 interpretation | `STRUCTURAL-VACUUM-ACCESSIBILITY-SUPPORTED` |
| SPEC-I/A | `SPECTRAL-SCALE-POSITIVE` |
| SPEC-I/B | `SPECTRAL-SCALE-POSITIVE` |
| BRIDGE-III | `COEXISTENCE-SUPPORTED` |
| Final project synthesis | `STRUCTURAL-SPECTRAL-COEXISTENCE-SUPPORTED` |

Frozen verdict strings are historical research outputs and should not be rewritten retrospectively.

---

## 5. Repository structure

```text
UNNS_YM_STRUCTURAL_SPECTRAL/
│
├── README.md
├── Structural Accessibility and Spectral Discreteness.pdf
├── UNNS_VACUUM_CONTINUITY_ANALYTICS.html
│
├── UNNS_YM_GAP/
│   ├── chambers/
│   ├── data/
│   ├── docs/
│   ├── inputs/
│   ├── ladders/
│   ├── nulls/
│   ├── output/
│   ├── scripts/
│   ├── FINAL_STATUS.md
│   └── README.md
│
└── UNNS_VACUUM_CONTINUITY/
    ├── analytics/
    ├── chambers/
    ├── data/
    │   ├── raw/
    │   ├── derived/
    │   └── sources/
    │       └── baker_2022/
    │           ├── arXiv-2207.08797v1.tar.gz
    │           └── s10052-022-10848-2.pdf
    ├── docs/
    ├── manuscript/
    │   ├── structural_accessibility_spectral_discreteness_manuscript_v1.pdf
    │   ├── structural_accessibility_spectral_discreteness_manuscript_v1.tex
    │   ├── structural_accessibility_spectral_discreteness_manuscript_v2.pdf
    │   ├── structural_accessibility_spectral_discreteness_manuscript_v2.tex
    │   ├── structural_accessibility_spectral_discreteness_manuscript_v3.pdf
    │   └── structural_accessibility_spectral_discreteness_manuscript_v3.tex
    ├── output/
    ├── scripts/
    ├── stage0/
    ├── stage1/
    ├── stage2/
    ├── stage3/
    └── README.md
```

The root PDF is the frozen final manuscript for convenient access. The versioned manuscript sources and prior builds remain under `UNNS_VACUUM_CONTINUITY/manuscript/` for provenance.

---

## 6. Reproducibility and provenance

The projects preserve their preregistration records, source-admission records, chamber builds, scripts, output tables, manifests, checksums, and frozen verdicts.

The Baker VREF-I/A provenance is closed. The original arXiv source package and published article are stored under:

[`UNNS_VACUUM_CONTINUITY/data/sources/baker_2022/`](./UNNS_VACUUM_CONTINUITY/data/sources/baker_2022/)

The three profile inputs used by VREF-I/A were verified byte-for-byte against the publisher-identified ancillary data underlying the published plots, and their SHA-256 digests match the frozen VREF-I/A configuration.

The final manuscript records the provenance and claim boundaries in Appendix C.

---

## 7. Final manuscript and analytics

### Final manuscript

**[Structural Accessibility and Spectral Discreteness in Pure SU(3) Yang–Mills](./Structural%20Accessibility%20and%20Spectral%20Discreteness.pdf)**

The final manuscript synthesizes both projects into one research argument:

```text
non-crossability hypothesis
        ↓
measured-data challenge
        ↓
structural accessibility
        ↓
independent spectral positivity
        ↓
structural–spectral coexistence
        ↓
open structure-to-spectrum problem
```

### Analytics

**[Open the project analytics](./UNNS_VACUUM_CONTINUITY_ANALYTICS.html)**

The analytics page provides the quantitative evidence chain, frozen verdict map, Stage-2 branch summaries, Stage-3 spectral anchors, BRIDGE-III synthesis, and provenance audit.

---

## 8. Project status

**Umbrella project status:** **FINAL / FROZEN**

The two component projects are closed at their recorded endpoints. No frozen result should be silently retuned, relabeled, or replaced.

Future work should start as a new, explicitly versioned research program centered on the open structure-to-spectrum problem rather than by reopening the completed experiments.

---

## Citation / use

When referring to this repository, distinguish clearly between:

1. the frozen empirical verdicts of the two projects;
2. the elementary structural–spectral theorem in the final manuscript;
3. the open Yang–Mills specialization problem.

This separation is central to the scientific interpretation of the archive.
