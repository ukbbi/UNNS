# YM3B_SOURCE_AUDIT.md

## UNNS Yang–Mills Gap — YM-3B Public-Source Audit

**Date:** 2026-09-30  
**Purpose:** identify publicly available non-Class-C information suitable for measured-data refinement, replication, and extension of YM-3.

---

## 1. Current evidence architecture

The project now uses a layered evidence structure:

- **AT20** remains the completed **YM-3A Class C refinement backbone**.
- **Sakai & Sasaki (2023)** is the **primary YM-3B Class B refinement source**.
- **Liang et al. (2014)** is an **independent two-level Class B replication source**.
- **Chen et al. (2006)** is a **strong independent five-level candidate** for an additional refinement branch.
- Other historical glueball studies remain reserve comparison sources.

The project will **not pursue an AT20 Class A data request**. No unpublished-data request is part of the active plan.

---

## 2. AT20 — RETAIN AS YM-3A / CLASS C BACKBONE ONLY

### Athenodorou & Teper (2020)

**A. Athenodorou and M. Teper,**  
“The glueball spectrum of SU(3) gauge theory in 3+1 dimensions,”  
JHEP 11 (2020) 172, arXiv:2007.06422.

Role:

- eight-level refinement backbone already used in YM-3A;
- provides the published glueball mass sequence used for the completed Class C refinement test;
- provides the beta = 6.50 `0++` effective-mass figure used earlier as a published-figure reconstruction;
- remains the physical reference sequence for the completed YM-3A result.

Decision:

- retain AT20 as the **completed Class C / model-refinement backbone**;
- do not relabel mass-only coarser levels as Class B;
- do not request raw correlation matrices from the authors;
- do not treat unpublished material as part of the active YM-3 path.

Verdict:

**FOUNDATIONAL YM-3A SOURCE; NOT AN ACTIVE YM-3B DATA-ACQUISITION ROUTE.**

---

## 3. Sakai & Sasaki (2023) — PRIMARY YM-3B SOURCE / ADMITTED

Citation:

**Keita Sakai and Shoichi Sasaki,**  
“Glueball spectroscopy in lattice QCD using gradient flow,”  
Phys. Rev. D 107, 034510 (2023), arXiv:2211.15176.  
DOI: 10.1103/PhysRevD.107.034510

Why admitted:

- pure SU(3) Yang–Mills;
- standard Wilson plaquette action;
- approximately fixed physical volume, `La ≈ 1.6 fm`;
- four ordered lattice spacings / couplings:
  - beta = 6.20
  - beta = 6.40
  - beta = 6.71
  - beta = 6.93
- published `A1++` / `0++` ground-state effective-mass trajectories;
- gauge-invariant spacelike Wilson-loop glueball operators;
- variational analysis using a `6 x 6` correlation matrix;
- Figures 9–12 provide the four-beta effective-mass sequence;
- published masses, fit ranges, and lattice scales provide external checks for reconstruction.

Evidence class:

**Class B — published effective-mass trajectories.**

Operational role:

`SS23_B4 = beta 6.20, 6.40, 6.71, 6.93`

This is the primary executable YM-3B measured-data refinement sequence.

Verdict:

**ADMITTED — PRIMARY YM-3B CLASS B REFINEMENT SOURCE.**

---

## 4. Liang et al. (2014) — INDEPENDENT TWO-LEVEL CLASS B REPLICATION

Citation:

**Jian Liang et al.,**  
“Wave functions of SU(3) pure gauge glueballs on the lattice,”  
arXiv:1411.1083.

Relevant source properties:

- pure SU(3) gauge theory;
- two anisotropic lattices with beta = 2.4 and beta = 2.8;
- spatial lattice spacings approximately:
  - `a_s = 0.222 fm`
  - `a_s = 0.138 fm`
- both ensembles use approximately fixed physical volume near 1.7 fm;
- 5000 gauge configurations are used for each lattice;
- the scalar channel is `A1++`, corresponding to `0++`;
- the study uses a `24 x 24` variational correlation matrix to construct optimized operators;
- Figure 1 publishes effective-mass plateaus for the ground and first excited scalar and tensor states on both lattices.

Evidence class:

**Class B — published effective-mass trajectories / plateaus.**

Strength:

This is a genuinely independent two-spacing test with a different operator and analysis pipeline.

Limitation:

Only two ordered lattice spacings are available, so Liang14 cannot satisfy the frozen minimum for the primary YM-3B refinement verdict by itself.

Operational role:

- independent Class B replication;
- representation robustness check;
- external confirmation of whether the CORR-I massive-side separation survives a different anisotropic-lattice construction.

Verdict:

**ADMITTED AS SECONDARY TWO-LEVEL CLASS B REPLICATION.**

---

## 5. Chen et al. (2006) — STRONG FIVE-LEVEL INDEPENDENT CANDIDATE

Citation:

**Y. Chen et al.,**  
“Glueball Spectrum and Matrix Elements on Anisotropic Lattices,”  
Phys. Rev. D 73, 014516 (2006), arXiv:hep-lat/0510074.

Why this source is now important:

- pure SU(3) lattice gauge study;
- five independent coupling values:
  - beta = 2.4
  - beta = 2.6
  - beta = 2.7
  - beta = 3.0
  - beta = 3.2
- corresponding spatial lattice spacings span approximately `0.222 fm` to `0.101 fm`;
- the paper states that the Monte Carlo calculation produces a `24 x 24` correlation matrix for each channel;
- a generalized eigenvalue / variational procedure is used to optimize the glueball state;
- the scalar `A1++` channel is included and its fitted masses are reported across all five lattice spacings;
- the study explicitly performs continuum extrapolation across the five lattice spacings.

Important distinction:

The paper **describes** the `24 x 24` correlation matrices and the variational pipeline, but the uploaded publication does not itself provide those full matrices as machine-readable public data.

Therefore:

- the existence of the matrices strengthens the methodological relevance of the source;
- the publicly usable evidence must still be classified according to what is actually exposed in the paper;
- no unpublished matrix access is assumed.

Current classification:

**Strong multi-level candidate.**

Possible use:

1. inspect the publication for recoverable `A1++` effective-mass trajectories at multiple beta values;
2. if a sufficiently complete published trajectory sequence exists, admit it as an additional Class B refinement branch;
3. otherwise use the five-level mass sequence as an independent Class C comparison only, without conflating it with Class B evidence.

Verdict:

**HIGH-PRIORITY FIVE-LEVEL INDEPENDENT CANDIDATE; CLASS B ADMISSION REQUIRES SUFFICIENT PUBLISHED TRAJECTORY DATA.**

---

## 6. Morningstar & Peardon — RESERVE COMPARISON SOURCE

The anisotropic pure-SU(3) studies of Morningstar and Peardon contain multiple lattice spacings and high-quality glueball spectroscopy and form part of the methodological lineage used by later anisotropic-lattice studies.

However, for the present audit, no complete multi-level published `0++` effective-mass trajectory sequence has yet been established from the material currently in the project.

Verdict:

**RESERVE COMPARISON / EXTERNAL REPLICATION CANDIDATE.**

---

## 7. Loan / Luo / related historical studies — SECONDARY ONLY

Historical anisotropic and Hamiltonian-limit studies remain potentially useful as representation checks and independent context.

At present they do not provide a cleaner primary refinement sequence than:

- SS23 for four-level Class B refinement;
- Liang14 for two-level Class B replication;
- Chen06 as the strongest five-level extension candidate.

Verdict:

**SECONDARY / RESERVE SOURCES.**

---

## 8. Active YM-3 data plan

### Primary measured-data refinement

`SS23_B4`

- Sakai & Sasaki 2023
- beta = 6.20, 6.40, 6.71, 6.93
- four-level Class B sequence
- execute under `PREREG_YM3B.md`

### Independent replication

`LIANG14_B2`

- Liang et al. 2014
- beta = 2.4, 2.8
- two-level Class B replication
- analyze only after the primary SS23 sequence is completed or under a separately frozen replication protocol

### Independent multi-level extension candidate

`CHEN06_CAND5`

- Chen et al. 2006
- beta = 2.4, 2.6, 2.7, 3.0, 3.2
- five-level source
- inspect for sufficient published `A1++` trajectory information before assigning final evidence class

### Completed model-refinement backbone

`AT20_C8`

- Athenodorou & Teper 2020
- eight-level Class C refinement backbone
- already completed in YM-3A
- no raw-data request planned

---

## 9. Admission decision

The active YM-3B architecture is:

**AT20 Class C backbone -> SS23 primary Class B -> Liang14 replication -> Chen06 extension candidate**

This deliberately separates:

- **model-refinement persistence** already established in YM-3A;
- **published measured-data refinement** to be tested in YM-3B;
- **independent replication** across different anisotropic-lattice/operator pipelines;
- **future multi-level extension** without assuming access to unpublished data.

The immediate next scientific action remains unchanged:

> **Digitize and reconstruct the four SS23 `A1++ / 0++` effective-mass trajectories under the frozen `PREREG_YM3B.md` protocol before running CORR-I.**
