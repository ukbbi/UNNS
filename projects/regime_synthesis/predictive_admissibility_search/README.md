# Predictive Admissibility Search

This directory contains the preserved research corpus, canonicalization pipelines, Canonical Ladder Engine (CLE) development artifacts, rigidity-manifold experiments, adversarial controls, and cross-domain analyses for the **Predictive Admissibility Search (PAS)** branch of the UNNS Substrate research program.

The program asks a forward-looking structural question:

> **Can the location and trajectory of a physical system in admissibility space be reconstructed well enough to distinguish stable, plastic, pathological, and adversarial structural regimes?**

Rather than comparing raw scientific variables directly, the workflow transforms heterogeneous physical data into canonical structural representations, evaluates their realizability geometry, and then compares those representations in a common admissibility space.

## Public research reference

The associated public UNNS article is:

**[How Physical Systems Find Their Place in Admissibility Space](https://unns.tech/research/how-physical-systems-find-their-place-in-admissibility-space)**

This article provides the public-facing synthesis of the admissibility-space program represented by this directory.

---

## Main research artifact

### `Canonical Structures in Admissibility Space.pdf`

Foundational manuscript for this branch.

The manuscript develops the idea that physically meaningful ladder representations occupy structured regions of admissibility space rather than behaving as arbitrary encodings.

The surrounding corpus preserves the computational path by which that idea was tested:

```text
raw physical data
    ↓
domain adapter
    ↓
canonical ladder
    ↓
STRUC-PERC / CLE structural analysis
    ↓
rigidity / persistence descriptors
    ↓
admissibility-space embedding
    ↓
cross-domain and adversarial comparison
```

---

# CLE v2.0.0 corpus

The main experimental body is contained in:

```text
CLE_v2.0.0_corpus/
```

Its `experimental artifacts/` directory is deliberately preserved as the **discovery layer** of CLE v2.

The archive documentation explicitly states that this material is not obsolete. It records the experimental evolution through:

- failed reconstructions;
- rigidity collapse;
- schema mismatches;
- reconstruction recovery;
- anisotropic studies;
- cross-domain comparison;
- adversarial falsification.

The scripts in this layer should therefore be treated as historical / reference implementations rather than as a single polished production API.

---

# Predictive Admissibility Search pipeline

The preserved PAS pipeline is documented in:

```text
Predictive Admissibility Search Pipeline (PASP).txt
```

Its end-to-end architecture is:

```text
raw scientific data
    ↓
domain adapters
    ↓
canonical realizability ladders
    ↓
STRUC-PERC-I structural analysis
    ↓
5D admissibility vectors
    ↓
pairwise similarity matrices
    ↓
structural-manifold analysis
```

A central design rule is that **STRUC-PERC-I operates on canonical realizability trajectories, not directly on raw scientific file formats**.

The pipeline separates:

1. raw domain ingestion;
2. canonicalization;
3. structural analysis;
4. vector construction;
5. similarity-space analysis.

---

# Canonical Ladder Engine

### `cle.zip`

Frozen CLE implementation associated with this research phase.

The preserved `CLE_v1_0_2_GUIDE.txt` describes CLE as a domain-agnostic structural engine that converts ordered scalar data into a canonical structural description based on the geometry of the gap field.

The architectural stack is:

```text
RAW DOMAIN VALUES
    ↓
Domain Adapter Layer
    ↓
CLEPipeline
    ↓
Canonical Structural Tensor
    ↓
CLEvaluator / canonicality ranking
    ↓
FamilyResult
```

Only the adapters are intended to contain domain knowledge.

The core engine operates on structural geometry.

---

## Structural coordinates

The CLE guide and v2 research artifacts use quantities including:

- giant ratio (`GR`);
- `κ_conn`;
- `κ*`;
- fragmentation entropy;
- rigidity persistence;
- tail dominance;
- admissibility persistence;
- recovery elasticity;
- anisotropic persistence;
- collapse-onset radius;
- full-region volume;
- bifurcation sharpness.

The engine distinguishes structural classes such as:

```text
FULL
GIANT
TAIL
HARD
```

and uses connectivity margin relative to the FULL threshold as one of the principal coordinates of admissibility.

---

# Canonicality and reconstruction fidelity

One of the strongest findings preserved in this archive came from the helium program.

The initial helium reconstruction produced an apparent near-total rigidity collapse. Subsequent analysis concluded that this was **not an engine bug** and not an intrinsic physical result.

The cause was insufficient reconstruction fidelity.

The refined helium pipeline restored:

- coherent giant-ratio distributions;
- nonzero persistence;
- stable manifold structure;
- meaningful anisotropic behavior.

The preserved status document therefore records the structural result:

> **rigidity geometry depends on reconstruction fidelity.**

This is a crucial point for the entire PAS program: the representation used to reconstruct an admissibility manifold is itself structurally active.

The original pathological helium outputs are retained alongside the refined results because they document the failure mode and its recovery.

---

# Domain programs

## Helium

Primary material includes:

```text
helium_rigidity_generator.py
helium_refined_rigidity_generator.py
helium_interaction_rigidity_experiment.py
generate_helium_delta.py
extract_helium_rigidity_metrics.py
extract_helium_refined_metrics.py
run_helium_v2_validation.py
UNNS_CLE_HELIUM_RIGIDITY_PROTOCOL.txt
HELIUM_RIGIDITY_RECONSTRUCTION_DISTINCTION.txt
```

The helium branch is used to study:

- topology vs. rigidity;
- interaction-induced deformation;
- reconstruction pathology;
- persistence recovery;
- anisotropic structural response.

The preserved validation records distinguish the original coarse reconstruction from the refined physically meaningful reconstruction.

---

## Neutrino

The neutrino branch is stored under:

```text
CLE_PILOT_I/neutrino/
CLE_PILOT_I/raw/neutrino/
```

It includes detector-derived ladders from:

- TMVA outputs;
- deep-learning representations;
- signal/background observables;
- significance structures;
- detector geometry / fiber coordinates.

Scripts include:

```text
neutrino_rigidity_generator.py
extract_neutrino_rigidity_metrics.py
neutrino_family_comparator.py
neutrini_rigidity_phase_mapper.py
```

The project uses these data to reconstruct **semantic / detector rigidity manifolds** and study which observational structures persist under deformation without fragmentation.

---

## Cosmology

The cosmology branch uses Planck spectral families:

```text
planck_TT
planck_TE
planck_EE
```

with principal scripts:

```text
cosmology_rigidity_generator.py
cosmology_family_comparator.py
```

The preserved family report records 100% admissibility for the three analyzed families and very high TT/TE/EE structural alignment.

The report interprets the dominant difference as **rigidity depth rather than topology**.

---

## Protein

The pilot corpus also includes a protein Markov-state-model branch.

Its preserved pipeline derives structural ladders such as:

```text
msm_population
msm_out_strength
msm_in_strength
msm_stitching_strength
msm_bottleneck_risk
```

The protein branch is part of the broader attempt to test whether the admissibility-space formalism can be applied to structurally unrelated domains through domain-specific adapters and a common structural engine.

---

# Cross-domain rigidity comparison

The principal prototype is:

```text
cross_domain_rigidity_comparator.py
```

The preserved cross-domain report compares refined helium, neutrino, and cosmology.

It classifies the domain-level rigidity signatures as:

| Domain | Preserved signature |
|---|---|
| Helium | `COHERENT_RIGID_MANIFOLD` |
| Neutrino | `PLASTIC_TRANSITION_MANIFOLD` |
| Cosmology | `DEEP_PERSISTENCE_MANIFOLD` |

The report records:

```text
helium ↔ cosmology  ≈ 0.9935
helium ↔ neutrino   ≈ 0.9012
neutrino ↔ cosmology ≈ 0.8818
```

These values belong to the preserved domain-summary comparison and should not be read as evidence that the underlying physical systems are the same.

The report explicitly states:

> similarity indicates shared rigidity geometry, not shared source physics.

---

# 5D admissibility representation

The PAS pipeline compresses structural outputs into a common five-dimensional representation:

```text
v(L) = (
    P_depth,
    sigma2_GR,
    frag_rate,
    adm_persist,
    aniso_persist
)
```

The preserved pipeline interprets these coordinates as:

| Coordinate | Meaning |
|---|---|
| `P_depth` | connectivity-persistence depth |
| `sigma2_GR` | giant-component structural-variance proxy |
| `frag_rate` | fragmentation tendency |
| `adm_persist` | admissibility persistence |
| `aniso_persist` | anisotropic persistence proxy |

Scripts:

```text
construct_real_5d_vectors.py
construct_adversarial_5d_vectors.py
compute_similarity_matrices.py
```

Outputs include:

```text
real_STRUC_5D_vectors.csv
adversarial_STRUC_5D_proxy_vectors.csv
similarity_outputs/
```

---

# Adversarial program

The corpus contains a substantial adversarial baseline designed to test whether apparent cross-domain similarity is structurally meaningful or merely a generic property of ordered sequences.

The canonical adversarial corpus contains **650 ladders**:

```text
uniform     100
randomwalk  100
pareto      100
shuffle     350
```

Relevant generators include:

```text
generate_uniform_ladder.py
generate_randomwalk_ladder.py
generate_pareto_ladder.py
generate_shuffle_ladder.py
canonicalize_adversarial_ladders.py
```

The strongest control is the shuffled-real family, which preserves much of the marginal gap information while disrupting structural order.

---

## Adversarial similarity baseline

The pipeline in:

```text
adversarial_similarity_baseline/
```

was created specifically to test whether the `R_sim` similarity measure is genuinely discriminative.

The preserved test specification treats high similarity between adversarial and real ladders as evidence against strong universality claims.

Importantly, this archive also preserves a **negative falsification result**.

The included `falsification_report.txt` records:

```text
Median(adversarial ↔ real) = -0.091963
Median(real ↔ real)        = -0.179017
Max(adversarial ↔ real)    =  0.950886
Min(real ↔ real)           = -0.841433
```

and concludes:

```text
RESULT: H1 weakened / falsified.
```

The stated reasons are:

- no structural separation boundary was detected;
- real-real similarity was unexpectedly weak.

This failed test is part of the scientific record and should not be removed. It demonstrates that the project did not simply retain favorable comparisons: the similarity layer was explicitly subjected to adversarial falsification and, in the preserved configuration, did not support the stronger hypothesis.

---

# Rigidity outputs

### `CLE_OUTPUT/`

Contains domain-level rigidity products, including:

```text
cross_domain/
helium_refined/
neutrino/
```

The cross-domain summary preserves metrics including:

- mean GR;
- GR variance;
- full-region volume;
- collapse-onset radius;
- fragmentation rate;
- admissibility persistence;
- bifurcation sharpness;
- recovery elasticity;
- anisotropic persistence;
- rigidity signature.

---

### `anisotropic_outputs/`

Contains anisotropic deformation studies and generated rigidity grids, including helium Zeeman and Δ-Zeeman families.

These outputs probe whether structural persistence depends on deformation direction rather than only deformation magnitude.

---

# Pilot corpus

### `CLE_PILOT_I/`

This is the main cross-domain pilot workspace.

Its contents include:

- raw domain inputs;
- canonicalized ladders;
- adversarial controls;
- helium data;
- neutrino data;
- cosmology data;
- protein data;
- comparison products.

The adapters preserved in the pilot include:

```text
helium_adapter.py
neutrino_adapter.py
cosmology_adapter.py
protein_adapter.py
```

This directory records the transition from isolated domain experiments toward a common canonical structural interface.

---

# Architecture status

The preserved research-status document records a deliberate distinction between **scientific progress** and **software architecture maturity**.

During rapid experimentation, `cross_domain_rigidity_comparator.py` accumulated many responsibilities:

- parsing;
- normalization;
- validation;
- orchestration;
- analysis;
- export.

The archive identifies this as architectural drift, not theoretical failure.

The target architecture separates these responsibilities into:

```text
adapters/
normalization.py
rigidity_models.py
rigidity_engine.py
pipeline.py
```

The long-term goal is to move experimentally validated logic into reusable substrate infrastructure.

---

# Logical directory map

The most important material can be read as:

```text
predictive_admissibility_search/
│
├── Canonical Structures in Admissibility Space.pdf
├── image1pas.png
├── image2pas.png
├── image3pas.png
├── image4pas.png
│
└── CLE_v2.0.0_corpus/
    └── experimental artifacts/
        ├── Predictive Admissibility Search Pipeline (PASP).txt
        ├── CLE_V2_0_0_RESEARCH_PIPELINE_STATUS.txt
        ├── Purpose of This Folder.md
        ├── CLE_v1_0_2_GUIDE.txt
        ├── cle.zip
        │
        ├── CLE_PILOT_I/
        │   ├── raw/
        │   ├── canonical/
        │   ├── adversarial/
        │   ├── helium/
        │   ├── neutrino/
        │   ├── cosmology/
        │   ├── protein/
        │   └── adapters/
        │
        ├── CLE_OUTPUT/
        │   ├── cross_domain/
        │   ├── helium_refined/
        │   └── neutrino/
        │
        ├── anisotropic_outputs/
        ├── similarity_outputs/
        ├── adversarial_similarity_baseline/
        │
        ├── construct_real_5d_vectors.py
        ├── construct_adversarial_5d_vectors.py
        ├── compute_similarity_matrices.py
        │
        └── domain-specific generators,
            comparators, extractors, and validation scripts
```

---

# Reproducibility

The intended PAS workflow is:

```text
1. acquire / identify domain data
2. run the domain adapter
3. canonicalize the ladder representation
4. evaluate structural geometry with CLE / STRUC-PERC
5. extract rigidity and persistence metrics
6. construct the standardized admissibility vector
7. compare within and across domains
8. run adversarial / shuffled controls
9. retain both successful and failed falsification outcomes
```

For reproducibility:

- do not run the structural engine directly on arbitrary raw scientific formats;
- preserve canonicalization settings;
- distinguish coarse and refined helium reconstructions;
- preserve intermediate outputs;
- keep adversarial controls separate from real-domain corpora;
- treat negative falsification results as part of the research record.

---

# Interpretation

This folder should not be read as evidence that unrelated physical domains share the same microscopic physics.

The common object of study is **structural admissibility geometry** after domain-specific data have been transformed into a canonical representation.

The core progression of the program is:

```text
physical system
    ↓
canonical representation
    ↓
admissibility geometry
    ↓
rigidity manifold
    ↓
cross-domain position
    ↓
predictive / falsifiable structural comparison
```

The program therefore aims to make “position in admissibility space” an operational, testable quantity rather than a metaphor.

---

## Public reference

For the public synthesis of this research branch, see:

**[How Physical Systems Find Their Place in Admissibility Space](https://unns.tech/research/how-physical-systems-find-their-place-in-admissibility-space)**

