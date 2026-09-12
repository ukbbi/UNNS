# Extreme Physical Transitions

This directory contains the working research corpus, pipelines, structural ladders, STRUC-PERC outputs, figures, and synthesis material for the **Extreme Physical Transitions** branch of the UNNS Substrate research program.

The branch investigates a common structural question across very different high-energy or rapidly changing systems:

> **How does structural coherence behave when a physical system is driven toward, through, or beyond an extreme transition?**

The emphasis is not on equating the underlying physics of the domains. The purpose is to test whether different systems exhibit comparable **admissibility, connectivity, fragmentation, heavy-tail, and margin-collapse behavior** after their native observables are transformed into structural ladders.

## Public research reference

The associated public UNNS article is:

**[The Edge of Collapse: How Coherence Survives Extreme Physical Forcing](https://unns.tech/research/the-edge-of-collapse-how-coherence-survives-extreme-physical-forcing)**

This article provides the public-facing research context for the cross-domain extreme-transition program represented by this directory.

---

## Research structure

The archive is organized around several complementary branches.

### `margin-collapse/`

Cross-domain margin-collapse program built around rapid physical transitions.

The frozen program notes define the common workflow as:

```text
raw signal
    ↓
structural observable
    ↓
ladder construction
    ↓
STRUC-PERC
    ↓
regime / connectivity / fragmentation analysis
```

The branch uses transformed observables rather than relying only on raw signals.

#### `supernova/`

Type Ia supernova structural-transition analysis.

The package preserves:

- processed light-curve data;
- raw-magnitude ladders;
- Δmag ladders;
- curvature ladders;
- ladder-generation scripts;
- curvature and Δmag diagnostics;
- time-resolved margin-analysis material;
- STRUC-PERC outputs.

A central result preserved in the run records is that the raw magnitude ladder is classified as **HARD_FRAGMENTATION**, while both the Δmag and curvature ladders reach **FULL_PERCOLATION**.

The corresponding STRUC-PERC runs record:

- Δmag: `kappa_connect ≈ 140.85`
- curvature: `kappa_connect ≈ 185.12`

This branch therefore demonstrates that transition structure may become visible only after an appropriate observable-layer transformation.

#### `non-sensitive seismic waveform/`

Seismic-waveform comparison branch.

The structural observable is based on amplitude differences:

```text
ΔA(t) = A(t+1) - A(t)
```

The folder contains:

- SAC waveform inputs;
- SAC → CSV conversion utilities;
- ΔA ladder generation;
- STRUC-PERC result files;
- full pipeline documentation.

The purpose is cross-domain comparison with the supernova transition case, not a claim that the two systems share the same underlying physics.

#### `nevada_earthquake/`

Local earthquake / rupture branch.

Contains:

- SAC waveform traces;
- converted CSV files;
- ΔA ladders;
- conversion scripts;
- STRUC-PERC outputs;
- pipeline documentation.

The preserved batch results include multiple realizability regimes across stations, including FULL, GIANT_COMPONENT, TAIL, and HARD fragmentation outcomes.

#### `explosion/nk_explosion_sac_dataset/`

North Korea nuclear-explosion waveform corpus for the 2006, 2009, and 2013 events.

Contains:

- raw SAC data;
- SAC → CSV tooling;
- ΔA structural ladders;
- STRUC-PERC batch outputs;
- pipeline and usage notes.

The working interpretation preserved in the package is **forced coherent collapse**: strong global coherence can coexist with tail fragmentation.

The package also preserves source links to the IRIS special-event material used in the workflow.

---

### `κ evolution over time/`

Time-local structural analysis of the ZTF light curve `ZTF20acobvxk`.

The pipeline contains:

- detections and non-detections;
- light-curve preprocessing;
- mass / energy / `pt` ladder generation;
- fracture analysis;
- sliding-window / time-resolved structural analysis;
- STRUC-PERC outputs.

The branch is designed to move beyond a single global verdict and examine how structural quantities evolve locally in time.

The working pipeline tracks quantities such as:

```text
giant_ratio(t)
kappa_connect(t)
fragmentation(t)
```

with the goal of locating time-local transition or fracture regions that can be hidden in a global analysis.

---

### `cern/`

CMS collision-data structural analysis.

The pipeline begins from `2e2mu_2012.csv` and constructs an ordered UNNS collision trajectory, followed by several structural representations:

- trajectory ladder;
- gap ladder;
- peak ladder.

The preserved batch output classifies all four tested collision representations as **FULL_PERCOLATION**.

The folder contains:

- source collision table;
- trajectory-construction code;
- ladder-generation code;
- plotting utilities;
- generated ladders;
- STRUC-PERC batch results.

The pipeline documentation identifies the source as CMS Open Data record 5200.

---

## Top-level synthesis material

The archive also contains research-level synthesis artifacts, including:

- `Beyond Fragmentation.pdf`
- `Forced Coherent Collapse.mp4`
- `unns_explosive_dynamics_analysis.html`
- `image1p.png` … `image5p.png`

These materials should be read as interpretation and synthesis built on the domain-specific pipelines and results stored in the subdirectories.

---

## Structural observables

Different domains require different observable transformations before comparison.

Examples preserved in this archive include:

| Domain | Structural observable |
|---|---|
| Supernova | raw magnitude, Δmag, curvature |
| Seismic waveform | Δamplitude |
| Nuclear explosion waveform | Δamplitude |
| ZTF transient | magnitude, transformed energy, local difference / `pt` |
| CMS collisions | ordered trajectory, gaps, peaks |

The common object of comparison is therefore **structural response**, not raw physical units.

---

## STRUC-PERC interpretation

The result packages use STRUC-PERC classifications such as:

- `FULL_PERCOLATION`
- `GIANT_COMPONENT_PERCOLATION`
- `TAIL_FRAGMENTATION`
- `HARD_FRAGMENTATION`

Related diagnostics include:

- giant ratio;
- connectivity threshold / `kappa_connect`;
- fragmentation index;
- isolated fraction;
- tail dominance;
- component structure.

These quantities are used to compare how structural coherence persists, weakens, fragments, or collapses under extreme forcing.

---

## Reproducibility

Where possible, each domain folder preserves the complete chain from source data to structural result:

```text
source data
    ↓
conversion / preprocessing
    ↓
structural observable
    ↓
ladder generation
    ↓
STRUC-PERC
    ↓
CSV / JSON / summary outputs
```

For reproducible work:

1. use the source data preserved or referenced in the relevant domain folder;
2. follow the local pipeline document before substituting alternative preprocessing;
3. preserve event or time ordering where the pipeline requires it;
4. distinguish raw observables from transformed structural observables;
5. retain the generated STRUC-PERC outputs together with the exact input ladder used for the run.

---

## Data and provenance

This directory contains a mixture of:

- original UNNS scripts and transformations;
- derived structural ladders;
- public scientific datasets;
- archived source waveforms;
- diagnostic figures;
- STRUC-PERC output files.

Upstream datasets remain attributable to their original providers. Source links and acquisition notes are preserved inside the relevant branches where available.

Important source families represented in the archive include:

- ZTF light-curve data;
- IRIS seismic waveform data;
- North Korea nuclear-test seismic event data distributed through IRIS;
- CMS Open Data.

Consult the source-specific files and pipeline notes before redistributing upstream data independently of this research archive.

---

## Scope

This directory is not a general collection of extreme-event datasets.

It is a **research record of the UNNS structural-transition program**, organized around the question of whether coherence, admissibility, and realizability exhibit recurrent structural behavior under extreme physical forcing.

The public interpretive reference for this branch is:

**[The Edge of Collapse: How Coherence Survives Extreme Physical Forcing](https://unns.tech/research/the-edge-of-collapse-how-coherence-survives-extreme-physical-forcing)**

