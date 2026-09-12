# Boundary-Mediated Structural Continuity

This directory contains the principal research artifacts for the **Boundary-Mediated Structural Continuity** branch of the UNNS Substrate research program.

The program investigates the internal organization of admissible structure after the admissibility boundary itself has already been defined. Its central question is:

> **If a system remains admissible, how are its admissible regions actually connected into a traversable structural world?**

The working answer developed here is that admissible structure is not uniformly distributed. It organizes into **basins, continuity corridors, stitching regions, fragmentation barriers, and recoverable paths**. Boundary geometry therefore does more than separate admissible from non-admissible states: it also helps organize how admissible structures remain connected.

## Public research reference

The associated public UNNS article is:

**[How Admissible Structures Form Connected Worlds](https://unns.tech/research/how-admissible-structures-form-connected-worlds)**

This article provides the public-facing synthesis of the admissible-cluster and structural-continuity program represented by this directory.

---

## Foundational manuscript

### `Admissible Cluster Geometry.pdf`

**Admissible Cluster Geometry: Recoverable Connectivity in Realizability Space**

This manuscript develops the internal-topology layer of the admissibility manifold `M_adm`.

It builds on earlier UNNS work on:

- the Universal Structural Law;
- the Percolative Realizability Principle;
- Connectivity Margin;
- the Margin-Confinement Law;
- Dual Observability.

The manuscript asks what happens **inside** the admissible region once non-crossability of the external boundary has been established.

Its operational picture is that admissible systems organize into:

- dense admissible basins;
- sparse continuity corridors;
- stitching-defect basins;
- hard-fragmented regions;
- recoverable trajectories between structurally related representations.

The manuscript introduces **Admissible Cluster Geometry (ACG)** as the topology layer describing those internal relations.

---

## Main empirical branches

### 1. Metallic-glass / spectral-chemistry corpus

The large chemistry branch is built from SciGlass spectral-chemistry data.

Primary source material:

```text
spectralparam_full.TXT
```

The acquisition notes identify the upstream database as:

```text
https://github.com/epam/SciGlass
```

The working export was produced from SciGlass database material and preserves glass/material identifiers, component identity, concentration, refractive/spectral coordinates, density-related fields, and model/source labels.

The chemistry pipeline is documented in:

- `UNNS Spectral Corpus Acquisition.md`
- `UNNS Metallic Glass Structural Ladder.md`

The central transformation is:

```text
SciGlass source data
    ↓
material / oxide grouping
    ↓
ordered compositional trajectory
    ↓
structural ladder
    ↓
normalization
    ↓
STRUC-PERC-I
    ↓
regime / connectivity analysis
```

---

### `metallic_ladders/`

This directory contains the raw metallic-glass / chemistry ladder corpus and its STRUC-PERC-I results.

The preserved batch output contains **500 analyzed ladders**:

- `132` — `FULL_PERCOLATION`
- `368` — `HARD_FRAGMENTATION`

A particularly important feature of the raw chemistry corpus is the localization of many failures. Among the 368 HARD cases, **296 contain exactly one isolated node**.

This is the empirical basis for the interpretation of many apparent failures as **localized stitching defects** rather than global structural collapse.

---

## Spectral Trajectory Extraction Engine

### `UNNS Spectral Trajectory Extraction Engine/`

This subdirectory contains the normalized spectral-trajectory pipeline and its grid-stability validation infrastructure.

Principal components include:

```text
spectralparam_full.TXT
spectral_ladder_generator.py
trajectory_normalizer.py
grid_sweep_runner.py
ladders/
normalized_ladders/
grid_runs/
struc_perc_output/
```

### `spectral_ladder_generator.py`

Builds ordered material trajectories from the SciGlass export.

The generator:

- parses the source export;
- groups observations by material / component;
- orders structural coordinates;
- emits UNNS-compatible ladders.

### `trajectory_normalizer.py`

Constructs the normalized representation used for cross-material regime analysis.

The normalization stage is designed to reduce representational artifacts such as:

- duplicated coordinates;
- discontinuous jumps;
- outlier spikes;
- sparse-trajectory instability;
- scale incompatibility.

### `normalized_ladders/`

Contains the normalized material corpus used for the multi-grid STRUC-PERC-I study.

The archive contains **188 normalized TXT ladders**.

---

## κ-grid stability program

The directory:

```text
UNNS Spectral Trajectory Extraction Engine/grid_runs/
```

contains seven grid configurations designed to test whether the observed structural regimes are artifacts of κ-grid resolution or range.

The preserved configurations are:

| Grid | κ range | Points | Purpose |
|---|---:|---:|---|
| `GRID_A` | `[0.01, 1.0]` | 17 | baseline |
| `GRID_B` | `[0.01, 1.0]` | 33 | refined |
| `GRID_C` | `[0.01, 1.0]` | 65 | high resolution |
| `GRID_D` | `[0.01, 1.0]` | 129 | ultra-refined |
| `GRID_E` | `[0.005, 1.0]` | 65 | lower-κ perturbation |
| `GRID_F` | `[0.01, 1.25]` | 65 | upper-range extension |
| `GRID_G` | `[0.001, 2.0]` | 65 | extreme perturbation |

The intended validation target is stability of:

- `κ_connect`;
- regime classification;
- giant-component behavior;
- percolation persistence;
- structural continuity.

---

## Regime-map analysis

### `regime_map_analysis_v3.html`

Interactive analysis of the normalized spectral corpus.

The report summarizes:

```text
188 materials
× 7 κ-grid configurations
= 1316 evaluations
```

and reports:

- **0 regime flips**
- **0 κ-class drift**
- **100% giant-ratio stability per material across the seven grids**

The normalized corpus is summarized as:

- `175` — FULL_CONTINUITY
- `12` — FRAGMENTED
- `1` — ANOMALOUS
- `0` — MARGINAL_CONTINUITY

The 12 fragmented systems form a discrete class with:

```text
giant ratio = 0.700
n = 10
```

while the dominant 175-material basin is fully connected.

The analysis also identifies discrete `κ_connect` classes rather than a continuously drifting threshold spectrum. This is used as evidence that the observed regime structure is not merely a scan-resolution artifact.

---

## Protein MSM branch

### `protein/`

This branch extends the continuity framework into protein folding using a **Folding@home Markov State Model (MSM)** obtained through the OSF COVID-19 simulation corpus.

Primary source files:

```text
tprobs.npy
populations.npy
```

The MSM is interpreted as a weighted transition graph over metastable states.

The objective is not biological classification. It is to test whether folding dynamics exhibit:

- admissibility corridors;
- metastable basins;
- localized bottlenecks;
- stitching strength;
- constrained manifold traversal.

### `protein_msm_ladder_generator.py`

Constructs five structural ladders:

```text
msm_out_strength.txt
msm_in_strength.txt
msm_population.txt
msm_stitching_strength.txt
msm_bottleneck_risk.txt
```

Their interpretations are:

| Ladder | Structural role |
|---|---|
| `msm_out_strength` | outgoing continuity strength |
| `msm_in_strength` | incoming accessibility |
| `msm_population` | metastable basin occupancy |
| `msm_stitching_strength` | local continuity / gluing proxy |
| `msm_bottleneck_risk` | localized traversal-risk proxy |

The preserved STRUC-PERC-I results show:

- 4 ladders — `FULL_PERCOLATION`
- `msm_out_strength.txt` — `GIANT_COMPONENT_PERCOLATION`

For the partially fragmented output:

```text
n = 4999
giantRatio = 0.998400
isolated = 3
```

Thus the protein MSM branch exhibits near-global continuity with only highly localized loss of connectivity.

---

## Boundary-mediated continuity

The common empirical pattern across the chemistry and protein branches is:

> **global coherence can survive even when local continuity fails.**

This motivates a distinction between:

- global structural collapse;
- localized stitching failure;
- sparse-corridor connectivity;
- recoverable continuity under an alternative structural representation.

In this program, boundaries are therefore not treated only as exclusion surfaces. They can also act as **organizational interfaces** through which structurally compatible basins remain connected.

---

## Admissible basins and stitching

The working basin interpretation includes four operational classes:

1. **Type I — dense admissible basin**  
   Fully percolating, globally connected structure.

2. **Type II — marginal / sparse-corridor basin**  
   Connectivity survives through a reduced continuity backbone.

3. **Type III — stitching-defect basin**  
   Global structure remains coherent while one or a few localized nodes fail to stitch.

4. **Type IV — hard-fragmented basin**  
   Full connectivity cannot be recovered within the tested representation and structural budget.

The chemistry corpus is particularly important for distinguishing Type III localized defects from genuinely global fragmentation.

---

## Recoverable connectivity

The foundational manuscript treats **recoverability** as a geometric property rather than a mere numerical repair.

The broader ACG framework integrates several mechanisms by which connectivity may be recovered or revealed:

- ε-corridor bridging;
- representation / chart transitions;
- Δ-lifting;
- deep-embedding transformations;
- constrained basin traversal.

Some of the supporting evidence for these mechanisms comes from earlier UNNS corpora discussed in the manuscript but not duplicated in this directory.

---

## Media and figures

### `acg.mp4`

Video / animation associated with the Admissible Cluster Geometry interpretation.

### `image1ac.png` … `image4ac.png`

Figures supporting the manuscript and public synthesis.

---

## STRUC-PERC-I instrument

### `struc_perc_i_v2_5_0.html`

Frozen browser-based STRUC-PERC-I instrument used by this branch for percolative realizability analysis.

The chemistry grid-sweep documentation explicitly uses this instrument for the multi-grid validation program.

---

## Logical directory map

The archive contains a repeated packaging directory, but the scientific structure can be read as:

```text
boundary-mediated_structural_continuity/
│
├── Admissible Cluster Geometry.pdf
├── regime_map_analysis_v3.html
├── struc_perc_i_v2_5_0.html
├── acg.mp4
├── image1ac.png
├── image2ac.png
├── image3ac.png
├── image4ac.png
│
├── spectralparam_full.TXT
├── UNNS Spectral Corpus Acquisition.md
├── UNNS Metallic Glass Structural Ladder.md
│
├── metallic_ladders/
│   └── STRUC-PERC-I/
│
├── UNNS Spectral Trajectory Extraction Engine/
│   ├── spectral_ladder_generator.py
│   ├── trajectory_normalizer.py
│   ├── grid_sweep_runner.py
│   ├── ladders/
│   ├── normalized_ladders/
│   ├── struc_perc_output/
│   └── grid_runs/
│       ├── GRID_A/
│       ├── GRID_B/
│       ├── GRID_C/
│       ├── GRID_D/
│       ├── GRID_E/
│       ├── GRID_F/
│       ├── GRID_G/
│       └── STRUC-PERC-I_output/
│
└── protein/
    ├── tprobs.npy
    ├── populations.npy
    ├── protein_msm_ladder_generator.py
    ├── UNNS Protein MSM Admissibility Pipeline.md
    └── protein_ladders/
        └── STRUC_PERC_I_output/
```

---

## Reproducibility

### Spectral / chemistry branch

Use the preserved flow:

```text
spectralparam_full.TXT
    ↓
spectral_ladder_generator.py
    ↓
ladders/
    ↓
trajectory_normalizer.py
    ↓
normalized_ladders/
    ↓
grid_sweep_runner.py
    ↓
GRID_A ... GRID_G
    ↓
STRUC-PERC-I
    ↓
regime_map_analysis_v3.html
```

Do not collapse raw and normalized chemistry results into a single corpus. They answer different structural questions:

- raw ladders expose local rupture and stitching sensitivity;
- normalized ladders test the stability of global regime structure.

### Protein branch

Use:

```text
tprobs.npy + populations.npy
    ↓
protein_msm_ladder_generator.py
    ↓
protein_ladders/
    ↓
STRUC-PERC-I
    ↓
continuity / bottleneck analysis
```

---

## Data and provenance

The principal upstream data families represented directly in this archive are:

- **SciGlass** spectral / glass-property data  
  https://github.com/epam/SciGlass

- **Folding@home MSM data** distributed through the OSF COVID-19 simulation corpus  
  https://osf.io/fs2yv/files/osfstorage

The archive contains both upstream-derived data and original UNNS transformations, scripts, normalized ladders, analyses, figures, and interpretive material.

Upstream data remain attributable to their original providers. Consult the corresponding source terms before redistributing upstream material independently of this research package.

---

## Scope

This directory is not a general materials or protein-science database.

It is a **research record of the UNNS admissible-cluster program**, designed to test how structurally admissible systems organize internally and how connectivity can persist through sparse corridors, localized rupture, and boundary-mediated stitching.

The central conceptual progression is:

```text
admissibility boundary
    ↓
admissible basins
    ↓
continuity corridors
    ↓
stitching interfaces
    ↓
recoverable connectivity
    ↓
connected structural worlds
```

For the public synthesis of this program, see:

**[How Admissible Structures Form Connected Worlds](https://unns.tech/research/how-admissible-structures-form-connected-worlds)**

