# Galaxy Structure and Validation

This directory contains the consolidated research corpus, structural atlas, reproducibility tests, representation-sensitivity analysis, transfer-validation results, figures, dashboard material, and manuscript artifacts for the **UNNS Galaxy Structure and Validation** program.

The project studies whether galaxy rotation-curve data admit reproducible **galaxy-specific multiscale structural fingerprints** when baryonic acceleration profiles are analyzed through STRUC-I and STRUC-PERC-I.

Its central question is:

> **Does each galaxy carry a stable structural identity in multiscale admissibility space, and how does that identity change when the observational representation changes?**

The completed v0.3 program separates two issues that must not be conflated:

1. **structural identity** — whether a galaxy has a reproducible multiscale fingerprint;
2. **transfer** — whether that fingerprint improves prediction under a particular external gravity-model architecture.

The first is strongly supported by the preserved atlas. The second produced a negative / weak result for the tested static whole-galaxy transfer design.

## Public research reference

The associated public UNNS article is:

**[The Structural Identity of Galaxies](https://unns.tech/research/the-structural-identity-of-galaxies)**

This article provides the public-facing synthesis of the galaxy structural-fingerprint program represented by this directory.

---

# Main research artifacts

### `Galaxy_Structural_Fingerprints.pdf`

Primary manuscript for the galaxy structural-fingerprint program.

### `galaxy_structural_fingerprints_dashboard.html`

Interactive dashboard presenting the principal atlas, regime, reproducibility, and validation results.

### `UNNS_Galaxy_Structural_Fingerprint_Analytics.html`

Analytical companion report for the galaxy fingerprint corpus.

### `gal_fngprnt.mp4`

Video / animation associated with the structural-fingerprint interpretation.

### Figures

```text
figure1_structural_fingerprint_pipeline.png
figure2_stable_vs_weak_persistence.png
figure3_five_admissibility_clusters.png
figure4_persistence_fragmentation_connectivity.png
figure5_manuscript_findings_showcase.png
```

These figures summarize the main pipeline and structural findings.

---

# Canonical research package

The core workspace is:

```text
UNNS_GALAXY_STRUCTURE_AND_VALIDATION_v0_3/
```

The project map separates the research into:

```text
01_STRUCTURAL_ATLAS/
02_TRANSFER_VALIDATION/
03_MANUSCRIPT_PREPARATION/
90_LEGACY_FRAMING/
```

The archive preserves historical framing and development material, but the active scientific interpretation is defined by the v0.3 documentation.

---

# Structural Atlas

The main atlas is located under:

```text
01_STRUCTURAL_ATLAS/
└── UNNS_GALAXY_STRUCTURAL_FINGERPRINTS_v0_1/
```

The active canonical project is the nested:

```text
UNNS_GALAXY_STRUCTURAL_FINGERPRINTS_v0_1/
```

The surrounding `Archive/` and `Evolution/` material is preserved for history and reproducibility but is not the canonical interpretation layer.

---

# Source data

The structural atlas is built from the **SPARC** galaxy database:

> Spitzer Photometry and Accurate Rotation Curves

Frozen source files include:

```text
SPARC_Lelli2016c.mrt
MassModels_Lelli2016c.mrt
Rotmod_LTG.zip
```

The prepared baryonic profile uses:

- signed gas contribution;
- disk mass-to-light ratio = `0.5`;
- bulge mass-to-light ratio = `0.7`;
- observed radial positions only;
- no interpolation;
- no extrapolation.

The individual Rotmod files were cross-checked against the combined mass-model table.

---

# Foundation corpus

The preserved foundation synthesis reports:

```text
3389 prepared valid radial rows
175 paired chamber ladders
121 consolidated galaxy fingerprints
4840 complete STRUC-I κ-profile rows
```

The program includes:

- STRUC-I multiscale response curves;
- STRUC-PERC-I fragmentation and connectivity descriptors;
- direct chamber exports;
- neutral curve descriptors;
- PCA-based structural atlas coordinates;
- Gate B reproducibility outputs;
- Gate C representation-sensitivity outputs;
- a consolidated Excel atlas archive.

---

# Structural fingerprint

The preferred conceptual object is:

> **galaxy-specific multiscale structural fingerprint**

For each galaxy, the fingerprint is built from the complete multiscale chamber response rather than from one scalar verdict.

The principal response channels include:

```text
ρ(κ)
ν(Vκ)(κ)
Aκ(κ)
```

together with connectivity / fragmentation information from STRUC-PERC-I.

The fingerprint therefore encodes multiple independent aspects of structure:

```text
persistence
fragmentation
connectivity
representation geometry
```

---

# Gate B — reproducibility

Gate B tested whether the complete fingerprint is stable under unchanged chamber execution.

Across five unchanged-ladder STRUC-I runs:

```text
top-1 source retrieval                 = 1.000000
top-5 source retrieval                 = 1.000000
median own / nearest-wrong distance    = 0.117893
median ICC across ρ PC1–PC3            = 0.999849
median top-5 neighbour Jaccard          = 1.000000
```

This is one of the strongest results in the archive.

The conclusion is:

> complete STRUC-I curves form stable galaxy-specific structural identities under unchanged representation.

The atlas is therefore not an artifact of native chamber randomness.

---

# Gate C — representation sensitivity

Gate C deliberately changes the measured ladder representation.

Four branches were tested:

1. leave-one-radius-out;
2. deterministic thinning to `n = 10`;
3. fixed-count radial coverage;
4. mass-to-light-ratio sensitivity.

The preserved source-recovery results are:

| Branch | Top-1 | Top-5 | Median own/wrong | Geometry-matched Top-1 |
|---|---:|---:|---:|---:|
| Leave one radius out | 0.551 | 0.730 | 0.916 | 0.726 |
| Deterministic n=10 thinning | 0.165 | 0.314 | 1.835 | 0.347 |
| Fixed-count coverage | 0.050 | 0.198 | 2.138 | 0.256 |
| M/L sensitivity | 0.517 | 0.619 | 0.916 | 0.649 |

None of the perturbation branches preserves the unchanged-ladder source-identification performance.

The project does **not** interpret this as disappearance of the fingerprint.

Instead, Gate C establishes a second research object:

> **the sampling, coverage, and preparation response law of the galaxy fingerprint.**

The measured fingerprint is therefore representation-sensitive, and that sensitivity is itself mapped and quantifiable.

---

# Low-dimensional atlas structure

The multiscale response space is strongly organized.

Variance retained in the first three principal components:

```text
ρ(κ)          90.8%
ν(Vκ)(κ)      88.5%
Aκ(κ)         55.9%
combined      61.0%
```

This shows that:

- `ρ` and `ν` form compact dominant response families;
- `Aκ` is more heterogeneous;
- the combined fingerprint still retains substantial low-dimensional structure.

The atlas is therefore not an arbitrary cloud of chamber outputs.

---

# Stable Structure vs Weak Persistence

The chamber regime is a major atlas coordinate.

Median `ρ-PC1`:

```text
Stable Structure     -2.109
Weak Persistence     11.218
```

Median combined structural-PC1:

```text
Stable Structure     -0.794
Weak Persistence      3.076
```

The project therefore treats **Weak Persistence** as a pronounced multiscale response regime rather than a minor label fluctuation.

The corpus contains:

```text
Stable Structure     110 / 121
Weak Persistence      11 / 121
```

---

# Physical alignment

The atlas is not organized only by chamber labels.

Selected Spearman alignments include:

```text
structural-PC2 vs effective surface brightness   +0.463
structural-PC2 vs 3.6 μm luminosity              +0.456
structural-PC2 vs flat rotation velocity         +0.404
structural-PC2 vs H I mass                       +0.391
```

The result is that a major structural coordinate tracks broad galaxy scale, brightness, rotation, and gas content.

---

# Structural neighbours

The nearest structural neighbours are more similar in conventional galaxy properties than random galaxy pairs.

Median differences:

| Property | Structural neighbour | All galaxy pairs |
|---|---:|---:|
| Hubble type | 2 | 3 |
| flat velocity | 62.7 km/s | 80.1 km/s |
| 3.6 μm luminosity | 37.3 × 10⁹ L☉ | 65.6 × 10⁹ L☉ |
| effective surface brightness | 275.1 L☉/pc² | 396.1 L☉/pc² |
| H I mass | 2.41 × 10⁹ M☉ | 3.80 × 10⁹ M☉ |

The archive therefore supports the conclusion that structural proximity is physically meaningful rather than arbitrary.

---

# Observation geometry is also encoded

The atlas records not only galaxy physics but also how the galaxy was sampled.

Examples:

```text
final ρ vs median ladder gap                   -0.541
structural-PC3 vs valid radial-point count     -0.493
vulnerability fraction vs median ladder gap    +0.455
```

This result is central to the current interpretation.

The fingerprint is expressed through a **measurement geometry** consisting of:

- point count;
- radial coverage;
- gap structure;
- baryonic preparation.

The project therefore treats normalization of this representation layer as the next research stage.

---

# Persistence, fragmentation, and connectivity are distinct

The paired chamber analysis gives:

```text
Stable Structure               110 / 121
Weak Persistence                11 / 121

HARD_FRAGMENTATION             103 / 121
FULL_PERCOLATION                17 / 121

Stable + HARD_FRAGMENTATION      94 / 121
```

All full-percolation cases reached connectivity only through the adaptive extension.

The key conclusion is:

> **stable persistence can coexist with fragmentation and without native-range global connectivity.**

Therefore:

```text
persistence ≠ fragmentation ≠ connectivity
```

These are distinct structural coordinates.

---

# Transfer validation

The second major branch is:

```text
02_TRANSFER_VALIDATION/
└── UNNS_GRAVITY_BRIDGE_v0_1/
```

This branch asks whether the fingerprint improves a static whole-galaxy gravity prediction architecture.

The preserved compact-model comparison is:

```text
ordinary profile baseline M2 RMSE     0.188389
combined chamber M-IP RMSE            0.194554
relative change                       -3.272%
verdict                               NON_GENERALIZING_SIGNAL
```

The full-curve comparison reports:

```text
aggregate improvement                 0.435%
positive folds                        1 / 5
bootstrap interval                    crossed zero
verdict                               WEAK_FOLD_DEPENDENT_FULL_CURVE_SIGNAL
```

This is a **negative / weak transfer result** and is preserved as such.

It means:

> the tested static whole-galaxy architecture is not the scale at which the structural fingerprint provides a consistent held-out gain.

It does **not** erase the independently established identity structure.

Correct galaxy-to-curve assignment still outperforms shuffled assignment, and complete response curves retain galaxy-specific information.

---

# Transfer-sensitive channels

The full-curve audit separates the three main response channels:

```text
ρ(κ)    +1.142% aggregate; 4 / 5 positive folds
Aκ      +0.457% aggregate; 3 / 5 positive folds
ν       -1.516% aggregate; 1 / 5 positive folds
```

The current conclusion is:

- `ρ` is the strongest candidate for a new local or regime-conditioned transfer experiment;
- `Aκ` carries weaker transfer structure;
- `ν` is counterproductive for the present prediction target.

The next transfer question is therefore not another static global model of the same form.

It is a **local, transition-based, or regime-conditioned** test, especially through `ρ`.

---

# Manuscript preparation

The package map also includes:

```text
03_MANUSCRIPT_PREPARATION/
```

with evidence, claims, figure, and completion registers.

The v0.3 package states that the core manuscript is ready around the direction:

> **Multiscale Structural Fingerprints of Galaxy Rotation Curves: Reproducibility, Atlas Organization, Representation Sensitivity, and Transfer Structure**

---

# Legacy framing

Historical pre-result material is retained under:

```text
90_LEGACY_FRAMING/
```

These documents are explicitly non-canonical.

They should not override:

- `CURRENT_INTERPRETATION.md`;
- `FINDINGS_REGISTER.md`;
- `RESEARCH_SCOPE.md`;
- `PROJECT_STATUS.json`;
- the canonical v0.3 README.

---

# Current project status

The preserved `PROJECT_STATUS.json` records:

```text
primary galaxies: 121
STRUC-I profile rows: 4840
fingerprints: ESTABLISHED_GALAXY_SPECIFIC_RESPONSES
Gate B: PASS
Gate C: REPRESENTATION_SENSITIVITY_MAPPED_4_BRANCHES
```

Transfer status:

```text
compact verdict:
NON_GENERALIZING_SIGNAL

full-curve verdict:
WEAK_FOLD_DEPENDENT_FULL_CURVE_SIGNAL

static global architecture:
COMPLETED_NEGATIVE_TRANSFER_RESULT

leading transfer-sensitive channel:
RHO
```

The manuscript status is:

```text
CORE_READY
```

---

# Next research priorities

The preserved roadmap identifies the next major directions as:

```text
sampling response surfaces
coverage transformation maps
observational uncertainty envelopes
regime-controlled atlas views
geometry-matched nulls
sampling-normalized coordinates
local ρ transfer
```

The research hierarchy is:

```text
fingerprint exists
    ↓
fingerprint is reproducible
    ↓
fingerprint changes under representation
    ↓
representation sensitivity is modeled
    ↓
normalized structural coordinates
    ↓
sharper physical and transfer interpretation
```

---

# Logical directory map

```text
galaxy-structure_and_validation/
│
├── Galaxy_Structural_Fingerprints.pdf
├── galaxy_structural_fingerprints_dashboard.html
├── UNNS_Galaxy_Structural_Fingerprint_Analytics.html
├── gal_fngprnt.mp4
│
├── figure1_structural_fingerprint_pipeline.png
├── figure2_stable_vs_weak_persistence.png
├── figure3_five_admissibility_clusters.png
├── figure4_persistence_fragmentation_connectivity.png
├── figure5_manuscript_findings_showcase.png
│
└── UNNS_GALAXY_STRUCTURE_AND_VALIDATION_v0_3/
    ├── README.md
    ├── RESEARCH_SCOPE.md
    ├── FINDINGS_REGISTER.md
    ├── PROJECT_MAP.md
    ├── PROJECT_STATUS.json
    ├── PACKAGE_MANIFEST_SHA256.txt
    │
    ├── 01_STRUCTURAL_ATLAS/
    │   └── UNNS_GALAXY_STRUCTURAL_FINGERPRINTS_v0_1/
    │       └── UNNS_GALAXY_STRUCTURAL_FINGERPRINTS_v0_1/
    │           ├── data/
    │           ├── inputs/
    │           ├── instruments/
    │           ├── outputs/
    │           ├── runs/
    │           ├── analysis/
    │           │   ├── curve_atlas/
    │           │   └── gal_fingerprint_i/
    │           ├── scripts/
    │           ├── tests/
    │           ├── CURRENT_INTERPRETATION.md
    │           ├── DATA_PROVENANCE.md
    │           └── FOUNDATION_SYNTHESIS.md
    │
    ├── 02_TRANSFER_VALIDATION/
    │   └── UNNS_GRAVITY_BRIDGE_v0_1/
    │
    ├── 03_MANUSCRIPT_PREPARATION/
    │
    └── 90_LEGACY_FRAMING/
```

---

# Reproducibility

The intended research flow is:

```text
SPARC source files
    ↓
prepared baryonic profiles
    ↓
paired galaxy ladders
    ↓
STRUC-I + STRUC-PERC-I
    ↓
complete multiscale response curves
    ↓
galaxy fingerprints
    ↓
curve descriptors + PCA atlas
    ↓
Gate B reproducibility
    ↓
Gate C representation sensitivity
    ↓
physical-alignment analysis
    ↓
gravity-transfer validation
```

For reproducible work:

1. preserve the frozen SPARC source files;
2. use the stated gas / disk / bulge preparation rules;
3. do not interpolate or extrapolate radial points unless explicitly running a new experiment;
4. preserve the distinction between direct chamber exports and derived atlas descriptors;
5. keep Gate B unchanged-ladder reproducibility separate from Gate C representation perturbations;
6. do not reinterpret the negative transfer result as failure of the fingerprint itself;
7. preserve historical material as non-canonical where the package marks it as such.

---

# Data provenance and integrity

The package preserves:

```text
PACKAGE_MANIFEST_SHA256.txt
PACKAGE_MANIFEST_SHA256.digest
```

for archive-level integrity tracking.

The structural atlas also contains its own manifests, source cross-checks, preparation summaries, and frozen SPARC source files.

The project should therefore be treated as a provenance-controlled research package rather than as a loose collection of galaxy plots.

---

# Scientific scope

This directory does **not** establish:

- a new universal law of galactic dynamics;
- a replacement for conventional rotation-curve modeling;
- representation-independent galaxy fingerprints;
- a successful global gravity predictor;
- that fragmentation implies instability;
- that full percolation is required for structural persistence.

What the current corpus does establish is narrower and stronger:

- complete multiscale response curves define reproducible galaxy-specific identities;
- those identities occupy an organized structural atlas;
- the atlas carries both physical-galaxy information and observation-geometry information;
- representation changes transform the fingerprint in measurable ways;
- persistence, fragmentation, and connectivity are distinct;
- the tested static global transfer architecture does not generalize;
- `ρ` is the leading candidate for the next local or regime-conditioned transfer experiment.

---

# Public reference

For the public synthesis of this research branch, see:

**[The Structural Identity of Galaxies](https://unns.tech/research/the-structural-identity-of-galaxies)**

