# Non-Crossability and the Margin-Confinement Program

This directory contains the research artifacts, detector-corpus pipelines, visualizations, analyses, and synthesis material for the **non-crossability / margin-confinement** branch of the UNNS Substrate research program.

The central question is:

> **Can an admissible structure cross the boundary of admissibility under identity-preserving evolution, or does structural survival force the trajectory to remain confined to the admissible side?**

The material in this folder develops that question through the **Margin-Confinement Law**, representation-sensitive realizability analysis, Δ-lifting, Representation-Induced Structural Collapse (RISC), and Forced Coherent Collapse (FCC).

## Public research reference

The associated public UNNS article is:

**[The Hidden Rule Behind Structural Survival](https://unns.tech/research/the-hidden-rule-behind-structural-survival)**

This article provides the public-facing interpretation of the structural-survival principle developed and tested by the material in this directory.

---

## Core claim

The working framework represented here treats the admissible region as a structurally confining domain.

The central formulation preserved in the mission-control dashboard is:

> once a system is represented inside the admissible region, identity-preserving dynamics cannot cross the boundary `m(L_t) = 0`.

In this formulation, collapse is approached asymptotically rather than by a genuine trans-boundary crossing.

The near-boundary regime is described as **Forced Coherent Collapse (FCC)**: strong local compression or tail dominance may develop while global relational coherence remains preserved.

---

## Main research artifacts

### `The Margin-Confinement Law.pdf`

Foundational manuscript for the non-crossability program.

The manuscript is represented in the dashboard as the central theorem-level document of this branch, connecting:

- admissibility geometry;
- non-crossability;
- margin confinement;
- RISC;
- FCC;
- Δ-lifting;
- representation-covariant admissibility.

---

### `margin_confinement_dashboard.html`

Interactive mission-control dashboard for the complete program.

The dashboard summarizes the major corpus-level results and links the theoretical and empirical components of the project.

The preserved dashboard reports:

- **0 genuine crossings detected**;
- **15,401 evaluations across 16 domains**;
- **9/9 Δ-lifting recovery** in the highlighted recovery set;
- **34 FCC-like states in Δ-space**, compared with 5 in raw space;
- a boundary monitor for minimum margin, giant ratio, tail dominance, FCC state count, and crossing count.

It also connects the Margin-Confinement Law to:

- the Percolative Realizability Principle;
- the Universal Structural Law;
- representation geometry;
- empirical boundary dynamics;
- the neutrino detector corpus.

---

### `neutrino_corpus_analysis.html`

Interactive analysis of the neutrino detector observational corpus using **STRUC-PERC-I v2.5.0**.

The analysis is explicitly **representation-sensitive** and is careful to distinguish detector-observable geometry from neutrino ontology.

The corpus summary preserved in the analysis reports:

- **67 ladders**;
- **5 observational representation groups**;
- 50 FULL;
- 8 GIANT;
- 6 TAIL;
- 3 HARD;
- 6 RISC matched pairs;
- 5 FCC-like raw states;
- 0 USL violations;
- 61 Δ-FULL outcomes;
- 9/9 Δ-recovery;
- 34 Δ-FCC-like states.

The corpus is described as observational reconstruction geometry for pp solar-neutrino vs. ¹⁴C pile-up discrimination in a liquid-scintillator detector.

---

### `data_analysis_corpus.zip`

Cross-domain analysis archive.

The package contains interactive analyses spanning several previously developed UNNS branches, including:

- atomic phase landscapes;
- cross-constant analysis;
- helium multi-chart analysis;
- phase mapping;
- Si-28 local-geometry validation;
- biological corpus analysis;
- condensed-matter corpus analysis;
- STRUC-I corpus analysis;
- STRUC-PERC corpus analysis;
- Voyager 1 multiscale analysis;
- Voyager realizability analysis;
- explosive-dynamics analysis.

This archive functions as the wider empirical comparison layer around the non-crossability program.

---

## Neutrino detector pipeline

The `neutrinos_roots/` directory contains the complete detector-corpus extraction and realizability pipeline.

### ROOT sources

The preserved ROOT files include:

- `deepL_performance.root`
- `TMVA_performance.root`
- `EnerySpectrum.root`
- `evt.root`
- `Fib_CDPMT.root`

The pipeline documentation also refers to a `variable.root` source in the original workflow.

These files provide classifier outputs, energy observables, angular observables, hit-time variables, detector-geometry coordinates, and learned representations.

---

### Stage 1 — ROOT structure inspection

Scripts:

- `inspect_root_structure.py`
- `inspect_branch_structure.py`

Purpose:

- identify usable ROOT branches;
- locate classifier outputs;
- locate energy, angular, hit-time, and embedding observables;
- establish the extraction map before ladder construction.

---

### Stage 2 — ladder extraction

Script:

- `extract_neutrino_ladders.py`

Purpose:

- extract arrays;
- remove invalid values;
- normalize;
- sort;
- export scalar TXT ladders.

The resulting raw ladders are stored under:

```text
neutrinos_roots/raw/
```

Representative families include:

```text
L_TMVA_*.txt
L_deepL_*.txt
L_bkg*.txt
L_sig*.txt
L_Fib_*.txt
```

These files form the baseline observational realizability corpus.

---

### Stage 3 — STRUC-PERC-I raw analysis

Results:

```text
neutrinos_roots/struc_perc_raw_results/
```

The raw analysis evaluates:

- verdict class;
- giant ratio;
- tail dominance;
- `κ_connect`;
- isolated-node count;
- isolated fraction;
- margin-related behavior.

The preserved batch file contains FULL, GIANT, TAIL, and HARD outcomes across the detector-observable representations.

---

### Stage 4 — Δ-lifting

Script:

```text
neutrinos_roots/raw/delta_txt_ladder.py
```

Definition:

```text
ΔL = |x(i+1) - x(i)|
```

The pipeline describes Δ-lifting operationally as **local continuity extraction**.

Generated Δ-ladders are stored under:

```text
neutrinos_roots/raw/delta_outputs/
```

---

### Stage 5 — STRUC-PERC-I Δ analysis

Results:

```text
neutrinos_roots/raw/delta_outputs/struc_perc_delta_results/
```

The Δ-space analysis reruns the same structural diagnostics on the lifted ladders.

The preserved corpus shows many fragmented raw representations recovering FULL percolation after Δ-lifting, while a smaller number remain TAIL or HARD.

The pipeline identifies recovery cases such as:

```text
HARD → FULL
HARD → GIANT
TAIL → FULL
TAIL → GIANT
```

as evidence of latent admissibility recovery.

---

## Representation-Induced Structural Collapse (RISC)

The neutrino corpus is used as a testbed for **Representation-Induced Structural Collapse (RISC)**.

The same underlying detector process is represented through different observational charts, including TMVA and deep-learning spaces.

The corpus analysis identifies matched cases in which:

```text
TMVA representation → TAIL / HARD
deep-learning representation → FULL
```

The analysis interprets these transitions as representation-dependent changes in observability rather than changes in the underlying physical process.

A highlighted example in the corpus is a HARD → FULL transition for the matched `h_SigSB_significance_2` observable.

The program therefore distinguishes:

- **observational collapse** from
- **ontological collapse**.

---

## Forced Coherent Collapse (FCC)

FCC is the near-boundary regime in which strong compression coexists with retained global coherence.

Operationally, the dashboard and corpus analysis associate FCC-like behavior with:

- very high tail dominance;
- giant ratio remaining at or near 1;
- zero or very few isolated nodes;
- admissibility retained close to the structural boundary.

This is used as evidence that strong forcing does not necessarily imply trans-boundary structural destruction.

---

## Non-crossability

The project uses the term **non-crossability** for the hypothesis / law that admissible trajectories do not pass through the admissibility boundary under the class of identity-preserving transformations considered by the framework.

The project therefore separates three distinct possibilities:

1. **interior admissibility** — the structure remains well inside the admissible region;
2. **boundary approach / FCC** — the structure becomes strongly compressed while preserving relational coherence;
3. **representation-induced fragmentation** — the observed chart may become TAIL or HARD even when another locality-preserving representation recovers admissibility.

The empirical program searches for genuine boundary crossings and compares them against these alternative mechanisms.

---

## Media and figures

### `forbidden_crossing.gif`
### `forbidden_crossing.mp4`

Visualization of the forbidden-crossing / boundary-confinement concept.

### `hidden_continuity.gif`
### `hidden_continuity.mp4`

Visualization of latent or recovered continuity under structural transformation.

### `image1fc.png` … `image6fc.png`

Figures associated with the non-crossability and margin-confinement synthesis.

---

## Directory map

```text
non-crossability/
├── The Margin-Confinement Law.pdf
├── margin_confinement_dashboard.html
├── neutrino_corpus_analysis.html
├── data_analysis_corpus.zip
│
├── forbidden_crossing.gif
├── forbidden_crossing.mp4
├── hidden_continuity.gif
├── hidden_continuity.mp4
│
├── image1fc.png
├── image2fc.png
├── image3fc.png
├── image4fc.png
├── image5fc.png
├── image6fc.png
│
└── neutrinos_roots/
    ├── *.root
    ├── extract_neutrino_ladders.py
    ├── inspect_root_structure.py
    ├── inspect_branch_structure.py
    ├── NEUTRINO_RISC_ MARGIN-CONFINEMENT_PIPELINE.txt
    ├── struc_perc_raw_results/
    └── raw/
        ├── *.txt
        ├── delta_txt_ladder.py
        └── delta_outputs/
            ├── *_delta.txt
            ├── NEUTRINO RISC Δ-LIFTING + STRUC-PERC-I PIPELINE.md
            └── struc_perc_delta_results/
```

---

## Reproducibility

For the neutrino detector corpus, the intended workflow is:

```text
ROOT source
    ↓
branch inspection
    ↓
observable extraction
    ↓
normalization and sorting
    ↓
raw ladder
    ↓
STRUC-PERC-I raw analysis
    ↓
Δ-lifting
    ↓
STRUC-PERC-I Δ analysis
    ↓
raw ↔ Δ comparison
    ↓
RISC / recovery / FCC interpretation
```

The pipeline documentation should be treated as the canonical operational guide when rerunning the detector analysis.

Do not collapse raw and Δ-space results into a single dataset: they represent different structural charts and are compared explicitly.

---

## Scope and interpretation

This directory does **not** claim that detector reconstruction variables are direct statements about neutrino ontology.

The neutrino analysis explicitly states that its structural verdicts describe the admissibility geometry of **observational representations**.

Similarly, the cross-domain corpus is used to test structural invariance and confinement behavior across representations and domains; it does not imply that the underlying physical mechanisms are identical.

The central structural question is narrower:

> **Does relational coherence remain confined to the admissible side of the boundary, even when representation, fragmentation, or extreme forcing drives the observed structure toward collapse?**

---

## Public reference

For the public research interpretation of this program, see:

**[The Hidden Rule Behind Structural Survival](https://unns.tech/research/the-hidden-rule-behind-structural-survival)**

