# Cosmological Boundary Routing

This directory contains the principal research artifacts for the **Cosmological Boundary Routing** branch of the UNNS Substrate research program.

The project compares three matched cosmological route types:

```text
A — classical Friedmann contraction toward a terminal small-scale boundary
B — effective loop-quantum-cosmology contraction → finite bounce → expansion
C — Planck-anchored ΛCDM expansion away from the early small-scale regime
```

The central question is not whether these models are physically identical. It is whether their trajectories occupy **different structural route classes** when analyzed through a common UNNS admissibility framework.

The completed experiment distinguishes:

- **terminal boundary approach**;
- **finite turning-surface routing**;
- **boundary recession / expansion**.

Its main result is that the effective LQC trajectory remains connected and globally admissible through an exact finite turning point, while the surrounding near-bounce shell shows localized deformation sensitivity.

## Public research reference

The associated public UNNS article is:

**[When the Universe Reaches Zero but Does Not End](https://unns.tech/research/when-the-universe-reaches-zero-but-does-not-end)**

This article provides the public-facing synthesis of the cosmological boundary-routing experiment preserved in this directory.

---

# Main research artifacts

### `Admissible Boundary Routing.pdf`

Technical manuscript for the cosmological boundary-routing program.

It develops the structural comparison between:

- classical singular approach;
- finite bounce routing;
- observationally anchored expansion.

---

### `cosmological_boundary_routing_dashboard.html`

Interactive dashboard summarizing the experiment and its principal structural results.

---

### `cosmological_boundary_routing_analytics.html`

Analytical companion to the dashboard, providing a more detailed view of the route comparison and structural diagnostics.

---

### `cosmo_bound_rout.mp4`

Video / animation associated with the cosmological boundary-routing interpretation.

---

### `image_1.png` … `image_4.png`

Figures used in the manuscript and public synthesis.

---

# Scientific workspace

The main reproducibility corpus is stored under:

```text
cosmological_boundary_routing/
```

Its principal structure is:

```text
cosmological_boundary_routing/
├── A_classical_friedmann/
├── B_lqc_bounce/
├── C_planck_lcdm/
├── ABC_bridge/
├── tools/
├── COSMOLOGICAL_BOUNDARY_ROUTING_SYNTHESIS.txt
└── README.txt
```

---

# Dataset A — Classical Friedmann boundary approach

### `A_classical_friedmann/`

Dataset A is the matched classical baseline.

It represents a **contracting Friedmann trajectory** moving toward the small-scale-factor singular boundary.

The trajectory is model-generated and uses the same Planck 2018 parameter anchor as Dataset C.

Its numerical route is:

```text
a = 1
    ↓
a = 10^-8
```

with:

```text
H(a) = -H0 E(a)
```

to select the contracting branch.

The numerical cutoff at `a = 10^-8` is an approach to the classical singular regime; the trajectory does not evaluate `a = 0`.

## Dataset A role

Dataset A is used as the controlled non-bouncing comparison branch.

Its expected direction is:

```text
scale factor ↓
density ↑
curvature ↑
provisional boundary margin ↓
```

The final route classification is:

```text
terminal_boundary_approach
```

---

# Dataset B — Effective LQC bounce

### `B_lqc_bounce/`

Dataset B is the corrected finite-bounce trajectory.

It contains the full direction-preserving path:

```text
contraction
    ↓
exact bounce
    ↓
expansion
```

The accepted trajectory version is `v2.2`.

A bounce-safe response coordinate is used:

```text
q_B = asinh(H_signed / H0)
```

This coordinate:

- remains finite at `H = 0`;
- preserves contraction / expansion sign;
- passes continuously through the exact bounce;
- avoids replacing the bounce by an arbitrary epsilon.

---

## Direct structural result for Dataset B

The finite LQC expansion branch remains admissible across the complete tested κ range.

The accepted direct result records:

```text
Regime = Geometric Persistence
State  = Weak Persistence
mean A_kappa = 1.000000
minimum A_kappa = 1.000000
mean structural pressure rho = 0.306052
maximum structural pressure rho = 0.636336
```

Compared with Datasets A and C, Dataset B has:

- higher structural pressure;
- weaker small-κ connectivity;
- a broader gap hierarchy;
- preserved global admissibility.

Its recorded connectivity scale is:

```text
κ_connect = 0.100000
```

whereas A and C are approximately:

```text
κ_connect ≈ 0.013335
```

---

# Dataset B alpha-deformation result

The accepted alpha analysis uses:

```text
0.50 ≤ alpha ≤ 1.50
21 alpha points
84,000 grid rows
```

with five structural regions:

1. contraction outer;
2. contraction near bounce;
3. bounce crossing;
4. expansion near bounce;
5. expansion outer.

The accepted normalization uses:

- Q90 regional scales;
- dedicated bounce-crossing scales;
- bounded normalized responses;
- response cap = 5.

The accepted preliminary 5D vector is:

```text
mean_GR                     = 0.259626302909
var_GR                      = 0.041445769350
anisotropic_persistence     = 0.001170567290
admissibility_persistence   = 0.988309523810
collapse_onset_radius       = 0.05
```

The grid contains:

```text
83,018 valid rows
982 unstable rows
84,000 total rows
```

All unstable rows occur in the two symmetric near-bounce shells:

```text
contraction_near_bounce = 491
expansion_near_bounce   = 491
```

while:

```text
bounce_crossing   = 0 unstable rows
contraction_outer = 0 unstable rows
expansion_outer   = 0 unstable rows
```

This is a central result of the program:

> **The exact turning surface remains admissible; the localized sensitivity occurs around the bounce, not at the bounce itself.**

The first local instability appears at:

```text
|alpha - 1| = 0.05
```

This is explicitly a **first-local-instability coordinate**, not a claim of global trajectory collapse under a 5% deformation.

---

# Dataset C — Planck-anchored ΛCDM expansion

### `C_planck_lcdm/`

Dataset C provides the observationally anchored expansion reference.

Its source anchor is the official **Planck 2018 cosmological-parameter products** from the Planck Legacy Archive.

The selected baseline is:

```text
base_plikHM_TTTEEE_lowl_lowE
```

corresponding to the flat six-parameter ΛCDM model constrained by:

- high-ℓ TT;
- high-ℓ TE;
- high-ℓ EE;
- low-ℓ temperature;
- lowE polarization.

Dataset C is not raw sky-map data. It is a deterministic model trajectory generated from the selected Planck parameter record.

---

## Dataset C direct result

The direct scalar coordinate is:

```text
q_C(a) = ln(E(a))
```

The accepted full-ladder STRUC-PERC-I result is:

```text
Verdict = FULL_PERCOLATION
Giant ratio = 1.000000
κ_connect = 0.0133352143
Isolated vertices = 0
Tail dominance = 0
```

The STRUC-I full-ladder result is:

```text
Regime = Geometric Persistence
State = Stable Structure
mean A_kappa = 1.000000
minimum A_kappa = 1.000000
mean structural pressure rho = 0.041627
maximum structural pressure rho = 0.290517
```

The accepted full run contains:

```text
n = 4001
subsampled = false
```

and confirms that the earlier 2000-point stratified surrogate did not alter the regime classification.

The final route class is:

```text
boundary_recession_expansion
```

---

# Why an orientation-sensitive bridge was required

A and C initially appeared almost identical in the direct scalar and magnitude-only alpha analyses.

That apparent degeneracy was expected because those representations discarded **route direction**.

The final bridge therefore restores signed quantities:

- signed `Δ ln(a)`;
- signed H flow;
- signed density flow;
- signed curvature flow;
- signed provisional-margin flow;
- branch identity;
- route phase;
- turning-surface identity.

This separates:

```text
contraction toward a boundary
```

from:

```text
expansion away from a boundary
```

even when their magnitude geometry is matched.

---

# A–B–C orientation-sensitive bridge

### `ABC_bridge/`

The accepted bridge is:

```text
Bridge v1.1
```

It constructs a shared dimensionless route coordinate from cumulative:

```text
|Δ ln(a)|
```

The common route topology is:

```text
Dataset A:
-1 → 0

Dataset B:
-1 → 0 → +1

Dataset C:
0 → +1
```

Interpretation:

```text
A = terminal approach
B = finite turning-surface routing
C = boundary recession
```

---

# Dataset A route signature

Accepted mean normalized signed flows:

```text
Δ ln(a) flow  = -0.500000
H flow        = -0.100772
density flow  = +0.462724
curvature     = +0.480638
margin flow   = -0.092779
```

This is the signature of:

```text
contraction
density growth
curvature growth
margin decrease
terminal boundary approach
```

---

# Dataset C route signature

Accepted mean normalized signed flows:

```text
Δ ln(a) flow  = +0.500000
H flow        = -0.100772
density flow  = -0.462724
curvature     = -0.480638
margin flow   = +0.092779
```

This reverses the A signature and identifies:

```text
expansion
density decrease
curvature decrease
margin increase
boundary recession
```

The bridge therefore resolves the A/C magnitude degeneracy.

A and C are **opposite orientations of matched magnitude geometry**, not the same trajectory.

---

# Dataset B branch-resolved routing

The full-path signed means of Dataset B nearly cancel because the contraction and expansion branches are approximately symmetric.

That cancellation is not interpreted as absence of structure.

The accepted analysis is therefore branch resolved.

## Pre-bounce branch

```text
route: -1 → 0
Δ ln(a) flow   ≈ -0.304527
density flow   ≈ +0.298770
margin flow    ≈ -0.100246
```

Interpretation:

```text
approach toward the finite turning surface
```

## Exact turning surface

The bridge preserves the two exact turning-crossing intervals separately.

At the turning surface:

```text
route coordinate ≈ 0
Δ ln(a) flow ≈ 0
density flow = 0
margin flow = 0
```

The route remains continuous through the finite bounce.

## Post-bounce branch

```text
route: 0 → +1
Δ ln(a) flow   ≈ +0.304527
density flow   ≈ -0.298770
margin flow    ≈ +0.100246
```

Interpretation:

```text
recession from the finite turning surface
```

Thus the branch pattern is:

```text
approach
    ↓
finite turning surface
    ↓
recession
```

---

# Principal finding

The completed experiment distinguishes three different cosmological route topologies.

### Dataset A

```text
terminal boundary approach
```

### Dataset B

```text
finite admissible turning-surface routing
```

### Dataset C

```text
boundary recession / expansion
```

All three remain connected in the tested structural representation.

Dataset B, however, carries substantially higher structural pressure and weaker low-κ connectivity than A and C.

The decisive distinction is therefore not simply:

```text
connected vs disconnected
```

but:

```text
how an admissible trajectory is routed through structural space
```

---

# Cosmological Boundary Routing interpretation

Within the selected models and fixed methodology, the experiment supports the following structural picture:

```text
Classical contraction:
admissible route
    ↓
terminal boundary approach

Effective LQC:
admissible contraction
    ↓
finite turning locus
    ↓
route reversal
    ↓
admissible expansion

Planck-anchored ΛCDM:
early boundary regime
    ↓
admissible recession / expansion
```

The central UNNS interpretation is:

> a singularity-avoiding correction can be represented not merely as the removal of a divergent endpoint, but as a **change in admissible route topology**.

In the effective LQC experiment, the bounce is not represented as structural disappearance. It is represented as **admissible continuation through a finite turning locus**.

---

# Key reproducibility artifacts

## Dataset A

```text
A_classical_friedmann/generated_trajectory/validated/
classical_friedmann_approach_validated.csv

A_classical_friedmann/canonical/ladder/

A_classical_friedmann/canonical/struc_perc/

A_classical_friedmann/canonical/alpha/
```

## Dataset B

```text
B_lqc_bounce/generated_trajectory/validated/
lqc_bounce_trajectory_validated_v2_2.csv

B_lqc_bounce/canonical/ladder/
lqc_bounce_response_path_preliminary.csv

B_lqc_bounce/canonical/struc_perc/

B_lqc_bounce/canonical/alpha/

B_lqc_bounce/canonical/alpha/
DATASET_B_ALPHA_V2_2_RESULT.txt
```

## Dataset C

```text
C_planck_lcdm/generated_trajectory/validated/
planck_lcdm_trajectory_validated.csv

C_planck_lcdm/canonical/struc_perc/

C_planck_lcdm/canonical/alpha/
```

## A–B–C Bridge

```text
ABC_bridge/tools/
build_orientation_sensitive_abc_bridge_v1_1.py

ABC_bridge/tools/
build_abc_route_profiles_v1_1.py

ABC_bridge/outputs/
ABC_orientation_sensitive_bridge_v1_1.csv

ABC_bridge/outputs/
ABC_orientation_sensitive_bridge_summary_v1_1.csv

ABC_bridge/outputs/
ABC_orientation_sensitive_phase_summary_v1_1.csv

ABC_bridge/outputs/
ABC_orientation_sensitive_route_profile_v1_1.csv

ABC_bridge/outputs/
ABC_BRIDGE_V1_1_RESULT.txt
```

---

# Structural instruments

The archive includes frozen browser-based UNNS instruments:

```text
tools/chamber_struc_i_v1_0_4.html
tools/struc_perc_i_v2_5_0.html
```

These are the instrument versions associated with the stored direct structural evaluations.

---

# Reproducibility sequence

The complete workflow is:

```text
Planck parameter anchor
    ↓
A / B / C trajectory generation
    ↓
trajectory validation
    ↓
canonical ladder construction
    ↓
STRUC-PERC-I
    ↓
STRUC-I
    ↓
alpha deformation
    ↓
normalization review
    ↓
structural vectors
    ↓
orientation-sensitive A–B–C bridge
    ↓
branch-resolved route profiles
    ↓
consolidated synthesis
```

For matched reruns, the project records the following methodological fixed points:

- Dataset B effective equation;
- adopted `rho_c` convention;
- hybrid Dataset B trajectory grid;
- exact-bounce identification;
- Q90 regional alpha normalization;
- response cap = 5;
- first-local-instability criterion;
- cumulative `|Δ ln(a)|` shared route coordinate;
- dataset-specific Q90 signed-flow normalization;
- branch-resolved Dataset B interpretation.

These choices should remain fixed if the stored results are to be reproduced directly.

---

# Data provenance

### Dataset C / Planck anchor

Source:

**ESA Planck Legacy Archive — Planck 2018 / PR3 cosmological parameter products**

The preserved source packages include the baseline:

```text
COM_CosmoParams-base-plikHM-TTTEEE-lowl-lowE_R3.00.zip
```

and the official parameter-table package:

```text
COM_CosmoParams_parameter-tables_R3.01.zip
```

Dataset C is generated from those official parameter products.

Dataset A uses the same compact Planck parameter record to create a matched classical contraction baseline.

Dataset B is a model-generated effective LQC trajectory and is not a Planck observation.

---

# Interpretive limits

The project documentation explicitly states that the experiment does **not** establish:

- that loop quantum cosmology is the correct theory of the early universe;
- that a cosmological bounce occurred in nature;
- direct observational confirmation of singularity removal;
- a universal metric distance on the admissibility manifold;
- a final canonical UNNS boundary margin;
- a normalization independent of the fixed Q90 / response-cap methodology;
- a model-independent proof that every non-singular cosmology follows the same routing mechanism.

The shared route coordinate is **path intrinsic**.

It is not claimed to be a physical metric distance on the admissibility manifold.

The `boundary_margin_candidate` used in the experiment remains provisional and diagnostic.

---

# Program status

The consolidated synthesis records the following stages as complete:

```text
Dataset A trajectory              COMPLETE
Dataset A direct structure        COMPLETE
Dataset A alpha                   COMPLETE

Dataset B trajectory              COMPLETE
Dataset B validation              COMPLETE
Dataset B direct structure        COMPLETE
Dataset B alpha                   COMPLETE

Dataset C trajectory              COMPLETE
Dataset C direct structure        COMPLETE
Dataset C alpha                   COMPLETE

A–B–C Bridge v1.1                COMPLETE
Route profile                     COMPLETE
Phase summary                     COMPLETE
Consolidated synthesis            COMPLETE
```

---

# Scope

This directory is not a general cosmology-data archive and does not present the LQC branch as an observationally established history of the Universe.

It is a **controlled structural experiment** comparing three cosmological route classes under a common UNNS analysis.

The final structural distinction is:

```text
A: -1 → 0
   terminal approach

B: -1 → 0 → +1
   finite route reversal

C: 0 → +1
   boundary recession
```

For the public synthesis of this research branch, see:

**[When the Universe Reaches Zero but Does Not End](https://unns.tech/research/when-the-universe-reaches-zero-but-does-not-end)**

