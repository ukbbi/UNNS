# UNNS Plasma H-Mode — Boundary-Route Preservation

This directory contains the research corpus, analysis pipeline, chamber inputs, time-resolved diagnostics, validation records, dashboards, figures, and manuscript material for the **UNNS Plasma H-Mode / Boundary Confinement Program**.

The project studies the L-mode → H-mode transition in magnetically confined plasma from a structural perspective.

Its working question is:

> **Does the plasma edge reorganize from turbulent route fragmentation into a boundary-preserving confinement structure during H-mode access?**

The program does **not** replace transport theory, magnetohydrodynamics, gyrokinetics, pedestal physics, neutral physics, or reactor engineering. Its purpose is narrower: to test whether confinement-state change can be represented as a measurable change in **edge admissibility, route fragmentation, and boundary capacity**.

## Public research reference

The associated public UNNS article is:

**[The Hidden Route Behind H-Mode Plasma Confinement](https://unns.tech/research/the-hidden-route-behind-h-mode-plasma-confinement)**

This article provides the public-facing synthesis of the plasma boundary-routing program represented by this directory.

---

# Main research artifacts

### `Boundary-Route Preservation in H-Mode Plasma.pdf`

Primary research manuscript for the H-mode boundary-routing interpretation.

### `unns_hmode_event_level_analysis.html`

Interactive event-level analysis of the TCV L-H transition corpus.

### `unns_hmode_project_dashboard.html`

Project dashboard consolidating the major event-level, time-resolved, diagnostic-confidence, and physical-window results.

### `h_mode_vid.mp4`

Video / animation associated with the H-mode structural interpretation.

### `image_1.png` … `image_4.png`

Figures used in the manuscript and public synthesis.

---

# Scientific workspace

The main reproducibility corpus is stored under:

```text
unns_hmode_project/
```

Its principal structure is:

```text
unns_hmode_project/
├── adapters/
├── chamber_inputs/
├── components/
├── data/
├── docs/
├── manuscript/
├── outputs/
├── pipelines/
├── schemas/
├── site/
├── tests/
├── TokaMark_data_splits.csv
├── TokaMark_temporal_data_splits.csv
├── project_manifest.json
└── unns_hmode_fragment_mapping_pack.zip
```

The internal project rule is explicit:

> new devices and datasets enter through `adapters/`; shared quantities belong in `components/`; orchestration stays in `pipelines/`.

---

# Core structural hypothesis

The working hypothesis is:

```text
L-mode
    ↓
high route fragmentation / edge leakage
    ↓
L→H transition
    ↓
edge reorganization
    ↓
route-preserving confinement layer
    ↓
H-mode
```

The central event-level margin is written schematically as:

```text
m_edge = C_edge_capacity - F_route_fragmentation
```

where `C_edge_capacity` represents evidence for a coherent edge / confinement response, while `F_route_fragmentation` represents structural pressure associated with transport, timing, and power-balance fragmentation.

---

# TCV L-H transition corpus

The first empirical branch uses the public TCV L-H transition dataset archived at:

```text
https://zenodo.org/records/14996664
```

The inspected TCV event table contains:

```text
92 event rows
79 columns
66 unique TCV shots
84 ILH = 1 events
8 ILH = 0 events
```

with shots spanning 2020–2022.

The archived raw workspace includes:

```text
data/raw/tcv_zenodo_14996664/
├── lhdatabase.h5
├── LH_DATA.h5
├── LH_analysis.ipynb
├── README_1.md
└── requirements.txt
```

The processed canonical forms include:

```text
data/processed/
├── tcv_lh_events_canonical.csv
└── tcv_lh_events_raw_flat.csv
```

---

# Two-chamber structural analysis

The TCV corpus was processed through:

```text
STRUC-I v1.0.4
STRUC-PERC-I v2.5.0
```

Frozen browser-based chamber instruments are preserved under:

```text
chamber_inputs/
├── chamber_struc_i_v1_0_4.html
└── struc_perc_i_v2_5_0.html
```

## STRUC-I result

The first complete TCV pass found no corpus-wide structural collapse.

Across both the all-events and L-H-only scalar ladders:

```text
Stable Structure: 21
Weak Persistence: 3
```

This established that the canonicalization process preserved ordered structure and that the TCV variables remained largely admissible under the STRUC-I perturbation protocol.

The corresponding report is:

```text
docs/06_RESULTS_TCV_TWO_CHAMBER_REPORT.md
```

## STRUC-PERC-I role

STRUC-PERC-I tests a different property:

> whether a variable's structural gap geometry remains connected or fragments into isolated branches.

The project therefore keeps the distinction:

```text
admissibility ≠ connectivity
```

---

# Fragment / isolate mapping

Following the chamber scan, the project mapped fragmented scalar variables back to actual event rows and shots.

Relevant components include:

```text
components/tcv_fragment_isolate_mapper.py
components/tcv_suspect_shot_reviewer.py
```

with reports:

```text
docs/07_FRAGMENT_ISOLATE_MAPPING_ANALYSIS_NOTE.md
docs/07_FRAGMENT_ISOLATE_MAPPING_REPORT.md
docs/08_FRAGMENT_MAPPING_RESULT_ANALYSIS.md
docs/09_SUSPECT_SHOT_REVIEW.md
docs/10_MANUAL_PHYSICAL_REVIEW_NINE_SHOTS.md
```

This stage identified recurring branch families associated with:

```text
power balance
transport
timing
edge / divertor response
```

These branches became the basis of the event-level edge-admissibility model.

---

# Event-level edge-admissibility model

The formal event score is:

```text
m_edge_event = C_edge_capacity - F_route_fragmentation
```

with fragmentation terms drawn from:

```text
S_power_balance
S_transport
S_timing
```

and capacity terms drawn from quantities including:

```text
S_edge_response
density support
geometry stability
species position
```

The model is implemented in:

```text
components/edge_admissibility_event_model.py
```

with validation in:

```text
components/edge_event_model_validator.py
```

---

# Nine-shot validation

The manually reviewed nine-shot set separated into three margin corridors:

```text
negative_leakage_margin
boundary_ambiguous_margin
positive_boundary_margin
```

The validator returned:

```text
state_separation: PASS_STRICT_ORDERING
reviewed_shots: 9
ambiguous_shots: 2
mixed_ILH_shots: 1
```

Measured margin ranges were:

```text
negative leakage:
-0.793663 … -0.227105

boundary ambiguous:
-0.073868 … +0.052241

positive boundary:
+0.527590 … +0.793112
```

The branch-family means were:

```text
timing branch          ≈ -0.473041
transport branch       ≈ -0.457666
power-balance branch   ≈ -0.306708
edge/divertor response ≈ +0.659667
```

Within this reviewed set, the edge/divertor-response branch occupied a distinct positive structural corridor.

The corresponding synthesis is:

```text
docs/14_EDGE_EVENT_MODEL_VALIDATION_SYNTHESIS.md
```

---

# Full 92-event TCV extension

The event-level model was extended to the complete 92-row canonical TCV corpus.

The generalized tag-free margin produced:

```text
negative_leakage_margin: 11
boundary_ambiguous_margin: 68
positive_boundary_margin: 13
```

State means remained ordered:

```text
negative mean  ≈ -0.356
ambiguous mean ≈ -0.038
positive mean  ≈ +0.341
```

The full corpus is therefore dominated by **boundary-near events**, rather than by the branch-rich extremes selected for manual review.

## Association with L-H transition labels

The full-corpus margin showed a measurable relationship with `ILH`:

```text
AUC of m_edge_event for ILH = 1: 0.690
mean ILH difference:               0.242
permutation p-value:               0.0022
```

However, standard plasma variables already classified the binary `ILH` label extremely well.

The preserved comparison reported:

```text
standard_core LOO AUC                 = 1.000
standard_core + m_edge_event          = 1.000
standard_edge_inclusive LOO AUC       = 1.000
standard_edge_inclusive + m_edge      = 0.999

UNNS_components LOO AUC               = 0.696
UNNS_margin_only LOO AUC              = 0.655
```

Therefore this archive does **not** claim superior binary L-H prediction.

The current role of `m_edge_event` is:

```text
structural interpretation
corridor decomposition
boundary-route analysis
```

The corresponding synthesis is:

```text
docs/16_FULL_CORPUS_EXTENSION_SYNTHESIS.md
```

---

# Time-resolved TokaMark / MAST extension

The TCV corpus was useful at event level but did not provide the desired time-resolved positive-corridor case.

The project therefore expanded to public MAST/TokaMark data.

The TokaMark source reconnaissance queried public metadata through:

```text
https://s3.echo.stfc.ac.uk/mast/tokamark/v1/<shot_id>.zarr/.zmetadata
```

The first 200-shot metadata scan completed with:

```text
200 successful metadata fetches
0 failed metadata fetches
```

and identified:

```text
45 FULL_PROFILE_EDGE_CANDIDATE shots
```

with combinations of:

- power;
- line density;
- D-alpha-like response;
- equilibrium geometry;
- Thomson temperature / density profiles;
- soft-X-ray activity proxies.

The highest-ranked first reference candidate was:

```text
shot 12063
```

---

# Time-resolved edge margin

The TokaMark branch constructs:

```text
m_edge(t)
```

rather than a single event-level scalar.

The first time-resolved analysis showed that shot `12063` was not uniformly favorable. Its trajectory contained:

```text
positive boundary excursions
boundary-ambiguous intervals
negative leakage intervals
```

The exploratory v0.1 five-shot panel ranked:

```text
12063  rank 1
11876  rank 2
11776  rank 3
11768  rank 4
11830  rank 5
```

but also exposed a methodological weakness:

> incomplete diagnostic cases could appear artificially positive because missing fragmentation evidence reduced the penalty side of the margin.

---

# Diagnostic-confidence revision

To address that failure mode, the project introduced:

```text
m_edge_raw(t)
Q_diag(t)
P_missing_critical(t)
m_edge_conf(t)
```

The confidence revision was designed to preserve the original structural margin while explicitly accounting for diagnostic coverage.

The revised five-shot panel returned:

```text
decision:
confidence_revision_passes_initial_panel

reference shot:
12063

reference confidence rank:
1

reference confidence-positive fraction:
0.169014

max comparison confidence-positive fraction:
0

reference Q_diag median:
0.888889

incomplete cases suppressed:
True
```

This step is documented in:

```text
docs/24_DIAGNOSTIC_CONFIDENCE_REVISION_PLAN.md
docs/25_TOKAMARK_M_EDGE_CONFIDENCE_REVISION_RESULTS.md
```

---

# Physical-window analysis

The next stage compared the confidence-corrected margin against independently edited physical windows.

The first provisional analysis used:

```text
L_MODE
LH_TRANSITION
H_MODE_STABLE
```

and returned:

```text
physical_window_analysis_passes_first_gate
```

with:

```text
17 eligible windows
72 excluded windows
```

The median ordering was:

```text
L_MODE        = -1.12
LH_TRANSITION = -0.288993
H_MODE_STABLE = +0.0525031
```

giving:

```text
L_MODE < LH_TRANSITION < H_MODE_STABLE
```

This was promising, but the project did not accept it as final validation.

---

# Conservative label hardening

The first hardening pass deliberately excluded all `H_MODE_STABLE` windows unless stronger independent physical evidence was available.

Under this conservative rule:

```text
eligible:
L_MODE        = 6
LH_TRANSITION = 6
H_MODE_STABLE = 0
```

The hardened analyzer correctly returned:

```text
physical_window_analysis_inconclusive_or_weak
```

because a direct H-vs-L comparison was no longer possible.

This negative result is preserved in:

```text
docs/31_PHYSICAL_WINDOW_LABEL_HARDENING_RESULTS.md
```

and is an important part of the non-circular validation record.

---

# H-mode-stable evidence recovery — v0.2

The project then performed a stricter recovery gate using physical diagnostic evidence rather than the UNNS margin itself.

Recovered `H_MODE_STABLE` windows were supported by combinations of:

```text
D-alpha morphology
profile-gradient evidence
soft-X context
power-density context
```

The non-circularity rule remained:

> UNNS audit columns were not used to decide which windows should be accepted as H-mode-stable.

The v0.2 gate restored:

```text
L_MODE        = 6
LH_TRANSITION = 6
H_MODE_STABLE = 5
```

and again returned:

```text
physical_window_analysis_passes_first_gate
```

The recovered ordering was:

```text
L_MODE        median m_edge_conf = -1.12
LH_TRANSITION median m_edge_conf = -0.288993
H_MODE_STABLE median m_edge_conf = +0.0525031
```

For every shot containing both accepted L-mode and recovered H-mode-stable windows, the within-shot H-minus-L margin difference was positive:

```text
12007  +1.08184
12017  +1.06195
12046  +1.32599
12055  +1.31576
12063  +1.17250
```

This result is documented in:

```text
docs/33_H_MODE_STABLE_EVIDENCE_RECOVERY_RESULTS.md
```

---

# Current validation status

The strongest defensible status preserved in the archive is:

> **v0.2 passes the first physical-window recovery gate.**

The project does **not** claim:

```text
UNNS has validated H-mode.
```

The recovered H-mode-stable windows are:

```text
2_SUPPORTED
```

rather than:

```text
3_EXTERNALLY_ANCHORED
```

because no independent external L-H / H-mode timing reference was supplied for those windows.

The next required gate is:

```text
external anchoring
or
falsification stress testing
```

Recommended external-anchor shots are:

```text
12007
12017
12046
12055
12063
```

---

# Principal components

The `components/` directory contains the reusable computational pieces, including:

```text
edge_margin.py
pedestal_load.py
turbulence_fragmentation.py
transition_detector.py
elm_risk.py

edge_admissibility_event_model.py
edge_event_model_validator.py
full_corpus_edge_event_extension.py

tcv_fragment_isolate_mapper.py
tcv_suspect_shot_reviewer.py

tokamark_metadata_candidate_scanner.py
tokamark_one_shot_array_probe.py
tokamark_m_edge_t_probe.py
tokamark_m_edge_trace_inspector.py
tokamark_cross_shot_m_edge_comparator.py
tokamark_small_panel_runner.py

tokamark_m_edge_confidence_revision.py
tokamark_moderate_confidence_panel_runner.py
tokamark_physical_window_label_analyzer.py
tokamark_physical_label_hardening_template.py
tokamark_hmode_stable_evidence_reviewer.py
```

The associated README files inside `components/` document the purpose and use of individual tools.

---

# Reproducibility flow

## TCV event-level path

```text
TCV Zenodo source
    ↓
adapter / inspection
    ↓
canonical event table
    ↓
STRUC-I + STRUC-PERC-I
    ↓
fragment / isolate mapping
    ↓
suspect-shot review
    ↓
event-level edge-admissibility model
    ↓
9-shot validation
    ↓
92-event full-corpus extension
```

## TokaMark time-resolved path

```text
public TokaMark metadata
    ↓
candidate scan
    ↓
diagnostic array retrieval
    ↓
m_edge_raw(t)
    ↓
diagnostic-confidence correction
    ↓
m_edge_conf(t)
    ↓
physical-window labeling
    ↓
conservative hardening
    ↓
H-mode-stable evidence recovery
    ↓
external anchoring / falsification gate
```

---

# Methodological lessons preserved by the archive

1. TCV event-level analysis repeatedly identifies power-balance, transport, timing, and edge/divertor-response branches.

2. In the reviewed nine-shot set, edge/divertor-response cases occupy a distinct positive margin corridor.

3. The full 92-event TCV corpus is mostly boundary-near rather than dominated by extreme cases.

4. Standard plasma variables remain stronger for binary `ILH` classification; the UNNS margin is not presented as a superior classifier.

5. Diagnostic missingness can artificially inflate a structural margin.

6. Diagnostic-confidence correction is therefore necessary.

7. Circular validation is explicitly avoided: unsupported H-mode labels were removed before being selectively restored from independent physical evidence.

8. The current v0.2 result is provisional but nontrivial: the recovered physical-window set reproduces the ordering

```text
L_MODE < LH_TRANSITION < H_MODE_STABLE
```

and all five within-shot H-minus-L comparisons are positive.

---

# Scientific limits

This repository does **not** establish:

- a complete physical theory of H-mode;
- that UNNS replaces established plasma-confinement physics;
- superior binary L-H classification;
- a final universal `m_edge` formula;
- cross-machine generality;
- externally anchored H-mode timing for the recovered v0.2 panel;
- fusion-gain prediction;
- reactor-control prescriptions.

The strongest current claim is narrower:

> a confidence-corrected structural edge margin shows a reproducible directional relationship with a small internally supported set of L-mode, transition, and H-mode-stable windows, while broader external validation remains open.

---

# Data provenance

The main data sources represented in this directory include:

### TCV L-H transition database

Public Zenodo record:

```text
https://zenodo.org/records/14996664
```

Used for the first event-level structural analysis and chamber experiments.

### MAST / TokaMark public data

Used for the later time-resolved diagnostic program through publicly accessible metadata and array resources.

The archive contains a mixture of:

- third-party scientific source data;
- UNNS-derived canonical tables;
- structural ladders;
- scripts;
- chamber inputs;
- diagnostic-confidence analyses;
- physical-window labels;
- result tables;
- figures;
- dashboards;
- manuscript material.

Upstream scientific data remain attributable to their original providers.

---

# Scope

This directory is not a general plasma-data repository.

It is a **research record of the UNNS H-mode boundary-routing program**, documenting the progression:

```text
TCV chamber analysis
    ↓
event-level route decomposition
    ↓
full-corpus generalization
    ↓
time-resolved TokaMark analysis
    ↓
diagnostic-confidence correction
    ↓
physical-window testing
    ↓
conservative hardening
    ↓
supported H-mode-stable recovery
    ↓
open external-validation gate
```

For the public synthesis of this research branch, see:

**[The Hidden Route Behind H-Mode Plasma Confinement](https://unns.tech/research/the-hidden-route-behind-h-mode-plasma-confinement)**

