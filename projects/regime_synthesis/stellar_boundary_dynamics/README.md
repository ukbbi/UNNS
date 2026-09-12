# Stellar Boundary Dynamics

This directory contains the principal research corpus, structural-ladder pipelines, bridge analyses, figures, and manuscript material for the **Stellar Boundary Dynamics (SBD)** branch of the UNNS Substrate research program.

The project asks whether a catastrophic stellar transition is best understood as simple structural destruction, or instead as **routing between distinct but still admissible structural regimes**.

Its central research question is:

> **Can a massive-star boundary event preserve structural admissibility while redistributing the system into multiple post-boundary observable regimes?**

The preserved workflow tests this question across three linked layers:

```text
A — pre-supernova radial stellar structure
B — post-collapse light-curve response
C — post-collapse spectral evolution
```

Each layer is converted into structural ladders, processed through STRUC-PERC-I and deformation / normalization stages, and then compared through A–B, B–C, and A–B–C bridge geometry.

## Public research reference

The associated public UNNS article is:

**[How Catastrophe Routes Structure Instead of Destroying It](https://unns.tech/research/how-catastrophe-routes-structure-instead-of-destroying-it)**

This article provides the public-facing synthesis of the boundary-routing interpretation developed by the research material in this directory.

---

# Foundational manuscript

### `Stellar Boundary Dynamics.pdf`

Main manuscript for this branch.

The manuscript frames catastrophic stellar collapse as a **boundary-routing problem** rather than as a simple disappearance of prior structure.

The empirical program tests whether:

```text
pre-boundary support/composition structure
    ↓
catastrophic boundary
    ↓
post-boundary brightness response
    ↓
post-boundary spectral redistribution
```

can remain internally admissible while occupying different structural regions.

The final synthesis preserved in the corpus recommends the framing:

> **Stellar Boundary Dynamics: Catastrophic Transition as Routing Between Admissible Structural Regimes**

---

# Three-layer architecture

The core research workspace is stored under the nested `stellar_boundary_dynamics/` dataset tree.

Its principal scientific branches are:

```text
A_mesa_precollapse_tracks/
B_supernova_light_curves/
C_spectral_time_series/

AB_bridge/
BC_bridge/
ABC_bridge/

tools/
```

The repeated nested folder names in the archive are packaging artifacts. The scientific structure is the A/B/C + bridge organization described below.

---

# Phase A — Pre-supernova radial structure

### `A_mesa_precollapse_tracks/`

Phase A represents the **pre-boundary side** of the stellar system.

The preserved project documentation records that local MESA execution was unavailable for the final empirical branch, so the study used public **precomputed pre-supernova radial profiles** from:

> *Different to the core: the pre-supernova structures of massive single and binary-stripped stars*  
> Zenodo record **5556959**

Selected real pre-supernova profiles:

```text
profile_single_M12.09_128net.data
profile_single_M19.98_128net.data
```

These are represented in the project as:

```text
A1_12M
A2_20M
```

They are terminal / pre-supernova **radial snapshots**, not full time-resolved stellar-evolution tracks.

## Phase A pipeline

```text
pre-supernova profile .data
    ↓
radial profile ladder
    ↓
STRUC-PERC-I canonical input
    ↓
numeric ladder
    ↓
STRUC-PERC-I
    ↓
α-deformation
    ↓
5D structural vector
    ↓
normalization review
    ↓
A_5D_VECTOR_SUMMARY_v2.csv
```

Key scripts include:

```text
a_presupernova_profile_to_ladder.py
a_profile_ladder_to_struc_perc_i.py
a_alpha_apply.py
a_alpha_normalization_review.py
```

## Phase A result

Both pre-supernova profile ladders reached:

```text
FULL_PERCOLATION
```

Preserved results:

```text
A1_12M:
κ_connect = 2
tailDominance = 0

A2_20M:
κ_connect = 1
tailDominance = 0
```

The result establishes that the selected pre-boundary radial structures are internally connected under STRUC-PERC-I.

A normalization review was required because the composition channel dominated the raw deformation-vector scale. Bridge analysis therefore uses the reviewed:

```text
A_5D_VECTOR_SUMMARY_v2.csv
```

rather than the first-pass vectors.

---

# Phase B — Supernova light curves

### `B_supernova_light_curves/`

Phase B represents the **post-collapse brightness-response layer**.

The preserved pipeline uses supernova light-curve data derived from the Open Supernova Catalog / AstroCats material.

The object set is:

```text
SN1987A
SN1993J
SN1999em
SN2011dh
SN2012aw
SN2013ej
```

The source-neutral ladder schema maps photometric records into canonical structural stages such as:

```text
pre_discovery_or_baseline
rise
peak
early_decline
plateau_or_shoulder
break
tail_decay
late_relaxation
```

## Phase B pipeline

```text
raw supernova photometry / JSON
    ↓
light-curve ladder
    ↓
STRUC-PERC-I canonical input
    ↓
numeric ladder
    ↓
STRUC-PERC-I
    ↓
α-deformation
    ↓
5D structural vector
    ↓
normalization review
    ↓
B_5D_VECTOR_SUMMARY_v2.csv
```

Key scripts include:

```text
osc_to_b_ladder.py
b_ladder_to_struc_perc_i.py
b_struc_input_to_numeric_ladders.py
b_alpha_apply.py
b_alpha_normalization_review.py
```

## Phase B result

All six Phase B light-curve ladders reached:

```text
FULL_PERCOLATION
```

The light-curve layer therefore forms a connected post-collapse brightness-response regime.

A persistent special case is:

```text
SN2012aw
```

which remains the primary high-tail / high-κ object in this layer.

Bridge work uses the normalization-reviewed:

```text
B_5D_VECTOR_SUMMARY_v2.csv
```

---

# Phase C — Spectral time series

### `C_spectral_time_series/`

Phase C represents **post-collapse spectral line evolution**.

Source:

```text
WISeREP public spectra
```

Pilot objects:

```text
C1_SN1993J
C2_SN2012aw
```

These were selected deliberately:

- `SN1993J` was the strongest contact-like Phase B object relative to the pre-supernova domain;
- `SN2012aw` was the strongest high-tail / high-κ outlier.

Target spectral features include:

```text
H_alpha
H_beta
He_I_5876
O_I_7774
Ca_II_NIR
Si_II_6355
Fe_II_5169
Ni_Co_decay_proxy
```

These are structural **line-window proxies**, not direct abundance measurements.

## Phase C pipeline

```text
raw WISeREP spectra
    ↓
spectral line-window ladder
    ↓
STRUC-PERC-I canonical input
    ↓
numeric ladder
    ↓
STRUC-PERC-I
    ↓
α-deformation
    ↓
5D structural vector
    ↓
normalization review
    ↓
C_5D_VECTOR_SUMMARY_v2.csv
```

Key scripts include:

```text
c_spectra_to_line_ladder.py
c_line_ladder_to_struc_perc_i.py
c_alpha_apply.py
c_alpha_normalization_review.py
```

## Phase C result

Both pilot spectral ladders reached:

```text
FULL_PERCOLATION
```

Preserved results:

| Object | Verdict | κ_connect | n | tail dominance |
|---|---|---:|---:|---:|
| `C1_SN1993J` | FULL_PERCOLATION | 201.404839 | 685 | 0.570046 |
| `C2_SN2012aw` | FULL_PERCOLATION | 3992.353937 | 198 | 0.959429 |

This reproduces the earlier contact/outlier distinction:

- `SN1993J` remains connected and comparatively moderate;
- `SN2012aw` remains connected but becomes extremely tail-dominated and requires a much larger connectivity scale.

---

# A–B bridge

### `AB_bridge/`

The A–B bridge compares:

```text
pre-supernova radial structure
        ↕
post-collapse light-curve response
```

using normalization-reviewed v2 structural vectors.

The bridge compares quantities including:

```text
mean_GR
var_GR
anisotropic_persistence_bounded
admissibility_persistence
collapse_onset_radius
kappa_connect_reference
tail_dominance_reference
```

The first A–B result record reports weak separation between the two domains.

A key object-level relation is:

```text
A2_20M ↔ B_SN1993J
```

which is the closest pre-boundary / post-boundary contact in the bridge.

`SN2012aw` remains the most strongly separated special case.

The bridge therefore supports a **related-but-shifted transition** rather than either complete identity or complete structural rupture.

---

# B–C bridge

### `BC_bridge/`

The B–C bridge compares two different post-boundary observables:

```text
light-curve response
        ↕
spectral line evolution
```

The result shows that the two post-collapse representations are **not redundant descriptions of one structural coordinate**.

The B–C geometry is strongly separated in the final tri-domain synthesis.

This means that the catastrophic boundary does not merely produce one post-collapse state measured in two interchangeable ways. Instead, brightness relaxation and spectral redistribution occupy distinct admissible regimes.

---

# A–B–C tri-domain bridge

### `ABC_bridge/`

This is the main synthesis layer of the project.

The bridge compares all three domains simultaneously:

```text
A = pre-supernova radial support / composition
B = post-collapse luminosity response
C = post-collapse spectral redistribution
```

The preserved final interpretation reports:

| Domain pair | Centroid distance | Classification |
|---|---:|---|
| A–B | 0.401021 | weak separation |
| B–C | 1.286808 | strong separation |
| A–C | 1.364620 | strong separation |

Global classification:

```text
A_to_B_contact_with_C_branching
```

This is the central result of the Stellar Boundary Dynamics program.

The best structural description is therefore **not**:

```text
A → B → C
```

as one simple linear trajectory.

It is better represented as:

```text
A
│
└──→ B   contact / inheritance
      \
       └──→ C   branching into a distinct post-collapse regime
```

---

# Object-chain results

## SN1993J — contact chain

The preserved tri-domain alignment is:

```text
A2_20M
   ↓
B_SN1993J
   ↓
C1_SN1993J
```

Final bridge values:

```text
dAB = 0.150098
dBC = 0.654183
dAC = 0.660980
branching_index = 0.504084
```

Interpretation:

> **compact transition chain with C still near B**

`SN1993J` is therefore the strongest example in the current corpus of a coherent boundary route spanning all three layers.

---

## SN2012aw — anomaly chain

The preserved alignment is:

```text
A2_20M
   ↓
B_SN2012aw
   ↓
C2_SN2012aw
```

Final bridge values:

```text
dAB = 0.437997
dBC = 1.907783
dAC = 2.008599
branching_index = 1.469786
```

Interpretation:

> **C branches away from the A–B contact path**

`SN2012aw` is therefore not merely a photometric outlier. Its anomalous structural position persists into the spectral layer and becomes more strongly separated.

---

# Main structural result

All processed A, B, and C ladders remain internally connected.

Yet the cross-domain bridge geometry shows substantial separation between the structural regimes.

This establishes an important distinction:

```text
internal percolation
≠
cross-domain structural equivalence
```

In the preserved corpus:

- A can remain admissible;
- B can remain admissible;
- C can remain admissible;
- while A, B, and C still occupy different structural regions.

The catastrophic event therefore does not need to destroy admissibility in order to produce a major structural transition.

It can instead **route admissible structure into non-equivalent observable regimes**.

---

# Boundary-routing interpretation

The project supports the following structural picture:

```text
pre-supernova radial structure
        ↓
catastrophic stellar boundary
        ↓
light-curve response contact / inheritance
        ↓
spectral branching
```

More generally:

1. catastrophic transition can occur without loss of structural admissibility;
2. the first post-boundary observable may remain close to the pre-boundary regime;
3. other observables may branch into strongly separated structural regimes;
4. persistent object-specific anomalies can survive across several observational layers;
5. connectedness inside each regime and distance between regimes are separate structural quantities.

This is the basis for the interpretation of stellar collapse as an **admissible cluster-routing event** rather than a simple rupture.

---

# STRUC-PERC-I instrument

The archive includes the frozen browser-based instrument:

```text
tools/struc_perc_i_v2_5_0.html
```

The A/B/C pipelines generate canonical and numeric ladder forms before STRUC-PERC-I evaluation.

The instrument is used here to establish the internal realizability of each structural representation before bridge geometry is evaluated across domains.

---

# Bridge tools

The shared `tools/` directory contains the comparison infrastructure for the bridge stages, including:

```text
ab_bridge_compare.py
bc_bridge_compare.py
abc_bridge_compare.py
```

and corresponding README documentation.

These scripts operate on the normalization-reviewed structural-vector summaries rather than directly on raw astrophysical data.

---

# Key result files

Important result records include:

```text
AB_bridge/summaries/AB_BRIDGE_RESULT_RECORD.txt
BC_bridge/summaries/BC_BRIDGE_RESULT_RECORD.txt
ABC_bridge/summaries/ABC_BRIDGE_RESULT_RECORD.txt
ABC_bridge/summaries/ABC_BRIDGE_INTERPRETATION.txt
```

Important comparison tables include:

```text
ABC_DOMAIN_CENTROID_COMPARISON.csv
ABC_OBJECT_CHAIN_ALIGNMENT.csv
ABC_PAIRWISE_DOMAIN_DISTANCE.csv
ABC_TRANSITION_CHAIN_TEST.csv
ABC_BRIDGE_SUMMARY.csv
```

These files preserve the numerical basis for the final boundary-routing interpretation.

---

# Figures

Top-level figures:

```text
image1sbd.png
image2sbd.png
image3sbd.png
image4sbd.png
```

These accompany the manuscript and public-facing synthesis.

---

# Logical directory map

Ignoring repeated packaging levels, the research structure can be read as:

```text
stellar_boundary_dynamics/
│
├── Stellar Boundary Dynamics.pdf
├── image1sbd.png
├── image2sbd.png
├── image3sbd.png
├── image4sbd.png
│
├── A_mesa_precollapse_tracks/
│   ├── precomputed / source material
│   ├── ladders/
│   ├── struc_perc_i/
│   ├── alpha_application/
│   ├── normalization_review/
│   └── tools/
│
├── B_supernova_light_curves/
│   ├── sources/
│   ├── raw/
│   ├── ladders/
│   ├── struc_perc_i/
│   ├── alpha_application/
│   ├── normalization_review/
│   └── tools/
│
├── C_spectral_time_series/
│   ├── raw spectra / metadata
│   ├── ladders/
│   ├── struc_perc_i/
│   ├── alpha_application/
│   ├── normalization_review/
│   └── tools/
│
├── AB_bridge/
│   ├── inputs/
│   ├── comparisons/
│   └── summaries/
│
├── BC_bridge/
│   ├── inputs/
│   ├── comparisons/
│   └── summaries/
│
├── ABC_bridge/
│   ├── inputs/
│   ├── comparisons/
│   └── summaries/
│
└── tools/
    ├── ab_bridge_compare.py
    ├── bc_bridge_compare.py
    ├── abc_bridge_compare.py
    └── struc_perc_i_v2_5_0.html
```

---

# Reproducibility

The intended research flow is:

```text
Phase A source
    ↓
A ladder
    ↓
STRUC-PERC-I
    ↓
α-grid / reviewed structural vector

Phase B source
    ↓
B ladder
    ↓
STRUC-PERC-I
    ↓
α-grid / reviewed structural vector

Phase C source
    ↓
C ladder
    ↓
STRUC-PERC-I
    ↓
α-grid / reviewed structural vector

A_v2 + B_v2
    ↓
AB bridge

B_v2 + C_v2
    ↓
BC bridge

A_v2 + B_v2 + C_v2
    ↓
ABC bridge
    ↓
boundary-routing synthesis
```

For reproducible work:

1. preserve the distinction between raw astrophysical data and structural ladder representations;
2. use the normalization-reviewed `*_5D_VECTOR_SUMMARY_v2.csv` files for bridge analysis;
3. do not substitute the raw first-pass vector summaries where the project explicitly records scale-review conditions;
4. preserve object identity across B and C when evaluating transition chains;
5. distinguish internal STRUC-PERC-I connectivity from cross-domain bridge distance.

---

# Scientific limits

The project documentation explicitly limits the claims that can be made from this corpus.

The current study does **not** constitute:

- direct prediction of a specific supernova from a specific progenitor profile;
- full hydrodynamic explosion modeling;
- radiative-transfer modeling;
- nucleosynthesis-yield recovery;
- direct abundance reconstruction from line-window proxies;
- a population-complete survey of massive-star collapse.

The present corpus contains:

- two Phase A pre-supernova radial profiles;
- six Phase B light curves;
- two Phase C spectral pilot objects.

The result is therefore a **structural boundary-routing test**, not a complete astrophysical explosion model.

---

# Data provenance

The principal upstream data families represented in this archive are:

- pre-supernova profile data from Zenodo record `5556959`;
- Open Supernova Catalog / AstroCats-derived light-curve data;
- public WISeREP spectra.

The archive contains a mixture of upstream scientific material, UNNS-derived ladders, conversion scripts, STRUC-PERC-I results, deformation grids, reviewed structural vectors, bridge comparisons, figures, and manuscript material.

Upstream material remains attributable to its original providers.

---

# Scope

This directory is not a general supernova-data repository.

It is a **research record of the UNNS Stellar Boundary Dynamics program**, built to test whether catastrophic physical transition can preserve admissibility while routing structure between non-equivalent regimes.

Its central structural progression is:

```text
admissible pre-boundary structure
    ↓
catastrophic boundary
    ↓
admissible post-boundary contact
    ↓
observable branching
    ↓
multiple connected structural regimes
```

For the public synthesis of this research branch, see:

**[How Catastrophe Routes Structure Instead of Destroying It](https://unns.tech/research/how-catastrophe-routes-structure-instead-of-destroying-it)**

