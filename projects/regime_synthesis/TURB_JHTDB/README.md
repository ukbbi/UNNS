# TURB_JHTDB

## Purpose

`TURB_JHTDB` is the top-level working and publication folder for the UNNS turbulence research program based on the Johns Hopkins Turbulence Database (JHTDB).

The project investigates whether structural evolution through **scale** and **time** is order-compatible in forced isotropic turbulence. Its central empirical object is the scale–time stitching defect

`D□ = JSD(P_ST, P_TS) / ln 2`

which compares the structural route produced by scale-then-time (`ST`) with the route produced by time-then-scale (`TS`).

The present frozen result is a **Structural Partial Replication** across two operationally independent, spatially and temporally non-overlapping samples of the same `isotropic1024coarse` DNS realization.

---

## Public article

**The Order Hidden in Turbulence**

https://unns.tech/research/the-order-hidden-in-turbulence

This is the public-facing synthesis of the project: the transformation problem, the replicated null hierarchy, the commuting bulk, branching-associated noncommutation, the R3/R7 failures, and the resulting hierarchy of structural invariance.

---

## Primary manuscript

**Reproducible Scale–Time Commutation Structure in Forced Isotropic Turbulence**

The manuscript contains the formal definition of `D□`, the frozen routing and null-hierarchy protocol, the Pilot A / Pilot B comparison, and the complete preregistered R1–R8 result.

Typical publication copy in this folder:

`Reproducible Scale–Time Commutation Structure.pdf`

---

## Interactive resources

Typical publication assets stored beside the project folder include:

- `Jhtdb turbulence dashboard.html` — project-level navigation and evidence dashboard
- `jhtdb_pilot_b_analytics.html` — detailed Pilot-B analytical trace
- `img_jhtd1.png` … `img_jhtd5.png` — article figures illustrating the main synthesis

The dashboard links the manuscript, analytics, project corpus, and archival source-data layer.

---

## Project tree

The canonical lightweight research project is:

`UNNS_TURB_JHTDB_v0_1\`

It contains the frozen analysis, chambers, configuration, ladders, tools, outputs, replication records, provenance, and source-recovery information required to reproduce the analysis.

Key top-level areas include:

```text
UNNS_TURB_JHTDB_v0_1/
├─ analysis/
├─ chambers/
├─ config/
├─ data/
├─ docs/
├─ ladders/
├─ outputs/
├─ PB_SENS/
├─ PB_STAGE/
├─ tests/
├─ tools/
├─ HIGH_RE_BRANCH_MANIFEST.json
├─ HIGH_RE_SCALE_FIX_MANIFEST.json
├─ HIGH_RE_SCALE_STAGE_MANIFEST.json
├─ MANIFEST.json
├─ QUESTIONS.md
├─ README.txt
├─ RUN_INSPECT_H5.bat
├─ SCHEMA.md
├─ SCOPE.md
├─ TREE.txt
├─ WORKFLOW.md
└─ ZENODO_LINK_MANIFEST.json
```

The heavy raw scientific sources are intentionally not required to be duplicated inside lightweight project distributions.

---

## Immutable source-data layer

**Zenodo DOI: 10.5281/zenodo.22650769**

https://doi.org/10.5281/zenodo.22650769

**Role: immutable source-data layer.**

The Zenodo record is:

**UNNS Turbulence — JHTDB Analysis Cutouts and High-Re Export v0.1**

It contains the frozen byte-identified source files used by the project, including:

- Pilot A JHTDB velocity cutout
- Pilot B JHTDB velocity cutout
- High-Re export archive
- SHA-256 checksum records
- attribution and provenance metadata
- source manifest files

For exact reproduction, use the **version DOI above**, verify all hashes, and restore the downloaded source files to the canonical paths documented under:

`UNNS_TURB_JHTDB_v0_1\data\source\zenodo\`

The local `data\raw\jhtdb\` layer is the active working copy; the Zenodo record is the canonical public archival/distribution copy.

Do not modify, normalize, repack, or silently replace the frozen source files when reproducing a published run.

---

## Upstream data provenance

The underlying DNS data originate from the **Johns Hopkins Turbulence Database (JHTDB)**.

Forced Isotropic Turbulence dataset DOI:

`10.7281/T1KK98XB`

The UNNS project does **not** claim authorship of the underlying DNS simulations.

UNNS contributions include:

- frozen extraction selections
- provenance and checksums
- structural-object construction
- scale/time routing
- `D□` measurement
- null hierarchies
- STRUC-I / STRUC-PERC-I evaluation
- STITCH-MECH controls
- preregistered replication logic
- synthesis and interpretation

---

## Frozen scientific status

Pilot B remains frozen as:

**STRUCTURAL PARTIAL REPLICATION**

Preregistered R1–R8 outcome:

```text
R1  PASS
R2  PASS
R3  FAIL
R4  PASS
R5  PASS
R6  PASS
R7  FAIL
R8  PASS
```

The two failures are preserved and are part of the scientific result.

The replicated core includes:

- constrained scale–time routing
- very low real `D□` relative to N0
- survival against N1 geometry controls
- survival against N2 geometry + feature controls
- strong value-space connectivity
- branching-associated noncommutation

Sample-dependent or non-replicated elements include:

- exact STRUC-I regime strength
- the preregistered R7 top-decile physical-intensity selector
- merging localization

---

## Main empirical hierarchy

Across Pilot A and Pilot B, the reproducible ordering is:

`D□(REAL) << D□(N2) < D□(N1) << D□(N0)`

The scientific gain is therefore not a universal numerical value of `D□`, but a reproducible **architecture of separation**.

The project also distinguishes:

`route organization != connectivity != scalar admissibility strength`

and reveals a population consisting of a dominant commuting bulk plus a comparatively sparse noncommuting set preferentially associated with branching.

---

## Reproducibility policy

For published and frozen stages:

1. do not modify frozen chambers or instruments;
2. do not retune failed criteria after seeing the result;
3. do not merge sensitivity runs with primary runs;
4. preserve source hashes and exact provenance;
5. use the Zenodo version DOI for source restoration;
6. keep Pilot A, Pilot B, and High-Re branches scientifically distinct;
7. preserve `FINAL_FROZEN_RESULT` records unchanged;
8. create a new version rather than patching a frozen scientific stage in place.

---

## Publication stack

The project should be read through five complementary layers:

1. **unns.tech article** — public synthesis and significance  
   https://unns.tech/research/the-order-hidden-in-turbulence

2. **Primary manuscript** — formal scientific account

3. **Interactive dashboard / analytics** — navigable evidence and result trace

4. **`UNNS_TURB_JHTDB_v0_1`** — frozen project, code, chambers, outputs, records, and reproducibility structure

5. **Zenodo DOI 10.5281/zenodo.22650769** — immutable source-data layer

Together these layers provide the conceptual, analytical, computational, and archival record of the project.

---

## Current research frontier

The frozen two-pilot result motivates, but does not yet establish:

- higher-Reynolds-number generalization
- alternative structural representations
- field-level surrogate tests
- prediction of branching from rising `D□`
- links to intermittency and dissipation
- reduced-model and LES closure diagnostics
- a broader theory of structural transformation compatibility

These are future tests and must remain separate from the claims already frozen in the current project.

---

## Canonical project identity

**Project:** `UNNS_TURB_JHTDB_v0_1`  
**Parent folder:** `TURB_JHTDB`  
**Program:** UNNS Substrate Research Program — Turbulence Branch  
**Public article:** https://unns.tech/research/the-order-hidden-in-turbulence  
**Source archive:** https://doi.org/10.5281/zenodo.22650769  
**Status:** frozen two-pilot structural partial replication
