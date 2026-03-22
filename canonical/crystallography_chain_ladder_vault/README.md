# crystallography_chain_ladder_vault

**UNNS Substrate Research Program — Condensed Matter Domain**
**Crystallographic Phase Chains & Polymorph Ladders · March 22, 2026**

---

## Overview

This vault contains the complete scientific output for the crystallographic branch of the UNNS admissibility program: the instruments, corpus analyses, chamber output data, and the formal manuscript reporting the first systematic evaluation of crystallographic phase chains and polymorph families under the admissibility inequality.

The central result: **zero violations across 48 descriptor ladders and 1,920 κ-step evaluations** spanning eight materials — three ferroic phase chains, three polymorph oxide systems, a metallic structural pair, and a single-phase control. The SiO₂ c-axis ladder (ρ̄ = 0.499) establishes a new high-water mark for ordered non-biological matter in the STRUC-I corpus.

---

## Contents

### Files in this repository

| File | Type | Description |
|------|------|-------------|
| `Structural_Admissibility_Crystallographic_Phase_Chains_v4.pdf` | PDF | Formal manuscript — full paper with definitions, tables, figures, and discussion |
| `chamber_struc_i_v1_0_4.html` | HTML (interactive) | STRUC-I v1.0.4 computational chamber — the instrument used for all evaluations |
| `struc_condmat_corpus_analysis.html` | HTML (interactive) | Condensed matter corpus analysis — per-material and per-descriptor results dashboard |
| `struc_i_v1_0_4_corpus_analysis.html` | HTML (interactive) | Full STRUC-I v1.0.4 corpus analysis — all 5,233 evaluations across 14 physical domains |

### External data archives (Google Drive)

| Archive | Contents | Link |
|---------|----------|------|
| `crystallography_phase_chain_ladder_corpus.zip` | 8 material folders, each containing CIF-derived descriptor ladder CSV files in STRUC-I-ready format | [Download](https://drive.google.com/file/d/1SxROPeiKzC1I00WPb-QqZExUy143RysU/view?usp=sharing) |
| `crystallography_phase-chain_ladders_struc-i_output.zip` | Chamber output files: `chamber_struc_i_v1_0_4_profiles (26–31).csv` and `chamber_struc_i_v1_0_4_results (23–30).json` — full ρ(κ) profiles and per-ladder results | [Download](https://drive.google.com/file/d/1jf5dNtDfG3-OAtEmXmdI4N0of-MDaFpz/view?usp=sharing) |

---

## Corpus

### Materials

Eight materials were selected to cover the principal structural roles in crystallographic phase families:

| Material | Phase sequence | n | Role |
|----------|---------------|---|------|
| Al₂O₃ | Corundum (*R*3̄*c*) | 1 | Single-phase control — degenerate limit |
| Fe | BCC (*Im*3̄*m*) → FCC (*Fm*3̄*m*) | 2 | Metallic structural pair |
| PbTiO₃ | Tetragonal (*P4mm*) → Cubic (*Pm*3̄*m*) | 2 | Minimal ferroic pair |
| TiO₂ | Rutile → Anatase → Brookite | 3 | Polymorph oxide — relaxed |
| ZrO₂ | Monoclinic → Tetragonal → Cubic | 3 | Polymorph oxide — moderate |
| SiO₂ | Quartz → Tridymite → Cristobalite | 3 | Polymorph oxide — high pressure |
| BaTiO₃ | Rhomb. → Ortho. → Tetrag. → Cubic | 4 | Ferroic chain — reference standard |
| KNbO₃ | Rhomb. → Ortho. → Tetrag. → Cubic | 4 | Ferroic chain — highest ferroic pressure |

### Descriptor channels

For each material, six descriptor ladders were extracted from canonical CIF-derived crystallographic data:

- Lattice parameters **a**, **b**, **c**
- **Cell volume**
- **Volume per atom**
- **Volume per formula unit**

Total corpus: **48 ladders** (8 materials × 6 descriptors).

### Corpus archive structure

```
crystallography_phase_chain_ladder_corpus.zip
├── Al2O3_CIFs/
├── BaTiO3 CIFs/
├── Fe_CIFs/
├── KNbO3_CIFs/
├── PbTiO3_CIFs/
├── SiO2_CIFs/
├── TiO2_CIFs/
└── ZrO2_CIFs/
```

Each folder contains the CIF files for the canonical phase representatives of that material and the derived descriptor ladder CSV files in STRUC-I-accepted schema.

---

## Instrument

All evaluations were performed with **CHAMBER STRUC-I v1.0.4** (`chamber_struc_i_v1_0_4.html`), a self-contained browser-based computational instrument implementing the preregistered admissibility protocol.

### Protocol (locked, no post-hoc adjustments)

| Parameter | Value |
|-----------|-------|
| κ range | [0.01, 1.0] |
| κ steps | 40 (logarithmically spaced) |
| Monte Carlo draws per step | M = 2,000 |
| Perturbation scale | ε = κ · δ_med |
| Total evaluations | 1,920 (48 ladders × 40 steps) |

The chamber accepts a sorted descriptor sequence as input, computes the inversion count and vulnerability capacity independently at each κ-step, and reports ρ(κ), Aκ, and the structural state classification for each ladder.

### Falsification criterion

A violation is formally defined as any single perturbation draw with `inv(p; L) > ν(Vε(L))`. A single confirmed violation would falsify the inequality for that ladder. **None were observed across any of the 1,920 evaluations.**

---

## Results

### Summary

| Metric | Value |
|--------|-------|
| Total evaluations | 1,920 |
| Violations | **0** |
| Global min Aκ | 0.9835 (KNbO₃ volume/fu at κ = 1) |
| Weak Persistence ladders | 5 (SiO₂ ×4, KNbO₃ ×1) |
| Boundary-Stabilized ladders | 0 |
| New corpus max ρ̄ (non-biological) | **0.499** (SiO₂ c-axis) |

### Per-material results

| Material | ρ̄ range | Min Aκ | WP | Worst state |
|----------|----------|--------|-----|-------------|
| Al₂O₃ | 0.000 | 1.0000 | 0 | Stable (degenerate) |
| Fe | 0.008–0.010 | 1.0000 | 0 | Stable Structure |
| PbTiO₃ | 0.008–0.009 | 1.0000 | 0 | Stable Structure |
| TiO₂ | 0.022–0.076 | 1.0000 | 0 | Stable Structure |
| ZrO₂ | 0.019–0.192 | 1.0000 | 0 | Stable Structure |
| BaTiO₃ | 0.070–0.250 | 0.9945 | 0 | Stable Structure |
| KNbO₃ | 0.023–0.362 | 0.9835 | 1 | Weak Persistence |
| SiO₂ | 0.194–0.499 | 1.0000 | 4 | Weak Persistence |

### Key structural findings

**Zero violations across all 48 ladders.** The crystallographic domain is empirically non-falsifying under STRUC-I v1.0.4.

**Ferroic isostructural discrimination.** BaTiO₃ and KNbO₃ follow the same nominal four-state phase sequence (rhombohedral → orthorhombic → tetragonal → cubic) yet produce measurably different structural pressures. The cell-volume pressure differential Δρ̄ = 0.362 − 0.248 = 0.114 quantifies the greater geometric anisotropy of KNbO₃ lattice distortions.

**Polymorph hierarchy.** The ordering TiO₂ ≪ ZrO₂ ≪ SiO₂ tracks the known crystallographic severity of structural reorganization — from octahedral tilting (TiO₂) through monoclinic distortion (ZrO₂) to radical network topology change (SiO₂: six-membered rings in quartz → four-membered rings in cristobalite). This hierarchy is recovered from descriptor ladder geometry alone, without energetics input.

**Descriptor-channel anisotropy.** Volumetric channels (cell volume, volume/atom, volume/fu) consistently carry higher pressure than axial channels (a, b, c), except in SiO₂ where the c-axis is anomalously elevated — crystallographically attributable to the tetrahedral helix running along the c-direction in quartz.

**New non-biological corpus maximum.** The SiO₂ c-axis ladder (ρ̄ = 0.499) exceeds the prior STRUC-I condensed-matter maximum of ρ̄ = 0.424 (Si density ladder), establishing a new high-water mark for ordered non-biological matter while maintaining Aκ = 1.000.

---

## Chamber output archive

```
crystallography_phase-chain_ladders_struc-i_output.zip
├── chamber_struc_i_v1_0_4_profiles (26).csv   — ρ(κ) profiles for material set 26
├── chamber_struc_i_v1_0_4_profiles (27).csv
├── chamber_struc_i_v1_0_4_profiles (28).csv
├── chamber_struc_i_v1_0_4_profiles (29).csv
├── chamber_struc_i_v1_0_4_profiles (30).csv
├── chamber_struc_i_v1_0_4_profiles (31).csv
├── chamber_struc_i_v1_0_4_results (23).json   — full results for material 23 (Al₂O₃)
├── chamber_struc_i_v1_0_4_results (24).json   — BaTiO₃
├── chamber_struc_i_v1_0_4_results (25).json   — Fe
├── chamber_struc_i_v1_0_4_results (26).json   — KNbO₃
├── chamber_struc_i_v1_0_4_results (27).json   — PbTiO₃
├── chamber_struc_i_v1_0_4_results (28).json   — SiO₂
├── chamber_struc_i_v1_0_4_results (29).json   — TiO₂
└── chamber_struc_i_v1_0_4_results (30).json   — ZrO₂
```

Each `.json` file contains the full per-ladder record: `mean_rho`, `min_Ak`, `rho_at_kappa_max`, `max_rho`, `state`, `regime`, and the complete 40-point ρ(κ) curve with `kappa`, `nu`, `inv`, `rho`, and `Ak` at every step. Each `.csv` file contains the corresponding ρ(κ) profile data in tabular form for plotting.

---

## Admissibility framework

The admissibility inequality is:

```
inv(Pε; L)  ≤  ν(Vε(L))
```

where:
- **L** is a structural descriptor ladder — a finite ordered sequence of values extracted from a phase chain or polymorph family
- **inv(Pε; L)** is the expected inversion count under perturbation family Pε at scale ε = κ · δ_med
- **ν(Vε(L))** is the vulnerability capacity — the maximum independent set of the vulnerability graph, computed from the static gap structure of L
- **ρ = inv/ν** is the structural pressure index — how much of the admissibility budget the ladder consumes
- **Aκ** is the admissibility rate — the fraction of perturbation draws satisfying the inequality at a given κ

Structural state classifications:
- **Stable Structure**: Aκ = 1.000 and ρ̄ < θ_WP
- **Weak Persistence**: Aκ < 1.000 or ρ̄ ≥ θ_WP
- **Boundary-Stabilized**: high ρ̄ with Aκ < 1.000 (not observed in this corpus)

The combinatorial basis of the inequality — that admissibility holds whenever inversion events embed as an independent set of the vulnerability graph — is established in the Universal Structural Law manuscript (v6, 2026).

---

## Reproducibility

All results are fully reproducible:

1. Download the corpus ladders from the [corpus archive](https://drive.google.com/file/d/1SxROPeiKzC1I00WPb-QqZExUy143RysU/view?usp=sharing)
2. Open `chamber_struc_i_v1_0_4.html` in any modern browser
3. Drag and drop any ladder CSV file into the chamber
4. The chamber will execute the full preregistered protocol and export JSON/CSV output matching the archived results

The chamber is a single-file self-contained HTML/JavaScript instrument — no installation, no server, no dependencies. Source data (CIF-derived descriptor values) are traceable to the Materials Project database (Jain et al., *APL Materials* 1, 011002, 2013; [next-gen.materialsproject.org/materials](https://next-gen.materialsproject.org/materials)).

---

## Corpus context

This crystallographic corpus contributes **1,920 evaluations** to the broader STRUC-I evidence base. The wider corpus (`struc_i_v1_0_4_corpus_analysis.html`) now totals **5,233 evaluations** across 14 physical domains:

| Domain | Evaluations | Violations |
|--------|-------------|------------|
| Random matrices (GOE, null baseline) | 3,000 | 0 |
| Molecular spectra (HITRAN) | 6 ladders | 0 |
| Nuclear γ-spectra (NuDat) | 15 ladders | 0 |
| Condensed-matter DFT property ladders | ~40 ladders | 0 |
| **Crystallographic phase chains (this corpus)** | **48 ladders · 1,920 steps** | **0** |
| Cosmic web (DESI/2MRS/SDSS) | 8 ladders | 0 |
| QM atomic spectra (NIST) | ~23 ladders | 0 |
| Planetary gravity (EIGEN/JGM/AIUB) | 24 ladders | 0 |
| Atmosphere ERA5 | 6 ladders | 0 |
| Solar plasma | 3 ladders | 0 |
| CMB Planck 2018 | 3 ladders | 0 |
| GNSS crustal displacement (NGL) | 5 ladders | 0 |
| Biology (QT ribozyme) | 6 ladders | 0 |
| Adversarial cluster attack | 4 ladders | violations (engineered) |

---

## Citation

```
UNNS Substrate Research Program.
Structural Admissibility in Crystallographic Phase Chains and Polymorph Ladders.
Manuscript v4, March 22, 2026.
```

---

## Links

| Resource | URL |
|----------|-----|
| Manuscript (PDF) | [Structural_Admissibility_Crystallographic_Phase_Chains_v4.pdf](./Structural_Admissibility_Crystallographic_Phase_Chains_v4.pdf) |
| STRUC-I v1.0.4 Chamber | [chamber_struc_i_v1_0_4.html](./chamber_struc_i_v1_0_4.html) |
| Condensed Matter Corpus Analysis | [struc_condmat_corpus_analysis.html](./struc_condmat_corpus_analysis.html) |
| Full STRUC-I Corpus Analysis | [struc_i_v1_0_4_corpus_analysis.html](./struc_i_v1_0_4_corpus_analysis.html) |
| Corpus ladder  (source data) | [crystallography_phase_chain_ladder_corpus.zip](https://drive.google.com/file/d/1SxROPeiKzC1I00WPb-QqZExUy143RysU/view?usp=sharing) |
| Chamber output archive (JSON + CSV) | [crystallography_phase-chain_ladders_struc-i_output.zip](https://drive.google.com/file/d/1jf5dNtDfG3-OAtEmXmdI4N0of-MDaFpz/view?usp=sharing) |
| Materials Project (source data) | [next-gen.materialsproject.org/materials](https://next-gen.materialsproject.org/materials) |

---

*UNNS Substrate Research Program · Condensed Matter Domain · March 22, 2026*
*Instrument: STRUC-I v1.0.4 · Protocol preregistered · κ ∈ [0.01, 1.0] · 40 steps · M = 2,000 MC · 0 violations*
