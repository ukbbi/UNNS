# Color Confinement — Admissibility by Closure

This directory contains the research corpus, provenance records, lattice-QCD-derived diagnostics, chamber inputs and outputs, boundary-pressure analysis, figures, dashboards, and manuscript material for the **UNNS Color Confinement** branch of the UNNS Substrate research program.

The project studies color confinement as a structural distinction between:

- internally valid colored degrees of freedom;
- non-externalizable isolated color routes;
- localized flux-tube structure;
- string-breaking / repair thresholds;
- externally admissible color-neutral closure.

Its central question is:

> **Can color confinement be represented structurally as a route that remains internal until it is repaired into an admissible color-neutral closure?**

The present corpus does **not** claim to derive QCD confinement from UNNS. It is a physically grounded structural benchmark built from published lattice-QCD results, ancillary flux-tube data, reconstructed static-source spectra, and explicitly derived UNNS diagnostics.

## Public research reference

The associated public UNNS article is:

**[The Physics of Forbidden Isolation: Color Confinement in the UNNS Substrate](https://unns.tech/research/the-physics-of-forbidden-isolation-color-confinement-in-the-unns-substrate)**

This article provides the public-facing synthesis of the confinement interpretation developed by the research material in this directory.

---

# Main research artifacts

### `Color Confinement as Admissibility-by-Closure.pdf`

Principal manuscript for this branch.

It develops the interpretation of color confinement as a distinction between **internal structural reality** and **external admissibility by closure**.

### `color_confinement_analytics.html`

Interactive analytical report summarizing the confinement diagnostics and chamber results.

### `Color Confinement.mp4`

Video / animation associated with the structural interpretation.

### `img_1cc.png` … `img_6cc.png`

Figures used in the manuscript and public synthesis.

### `chamber_struc_i_v1_0_4.html`

Frozen STRUC-I instrument used in the stored chamber runs.

### `struc_perc_i_v2_5_0.html`

Frozen STRUC-PERC-I instrument used for realizability / connectivity analysis.

---

# Provenance-controlled research corpus

The main scientific workspace is:

```text
color_confinement_data_seed_v0_1_1_provenance/
```

It contains:

```text
chamber_inputs/
chamber_outputs/
data/
extraction_queue/
provenance/
raw_ancillary/
reports/
scripts/
```

together with manifests, validation utilities, and source registries.

The package is deliberately provenance-heavy. Its source documentation requires each accepted scientific row to retain:

```text
source_id
source_url / DOI / arXiv identifier
source_location
row_provenance
reported / derived / extraction-target status
```

This distinction is essential because the archive mixes:

- reported source values;
- author ancillary pointwise data;
- model-reconstructed values;
- UNNS-derived diagnostics;
- acquisition targets not yet promoted to data.

---

# Primary scientific sources

The preserved provenance map identifies four main QCD sources.

## Bulava et al. 2019 — string breaking

**String breaking by light and strange quarks in QCD**

```text
arXiv:1902.04006
DOI: 10.1016/j.physletb.2019.05.018
```

Used for:

- reported light-channel string-breaking distance;
- reported strange-channel string-breaking distance;
- static-source spectrum reconstruction target.

The two principal threshold markers are:

```text
r_c  ≈ 1.224 fm
r_cs ≈ 1.293 fm
```

---

## Bulava et al. 2024 — static-source potential / mass dependence

**The quark-mass dependence of the potential energy between static colour sources in the QCD vacuum with light and strange quarks**

```text
arXiv:2403.00754
DOI: 10.1016/j.physletb.2024.138754
```

Used for:

- ensemble metadata;
- reported string-tension information;
- static-potential reconstruction context;
- physical-point threshold acquisition targets.

---

## Baker et al. 2024 — full-QCD flux tubes

**Unveiling the flux tube structure in full QCD**

```text
arXiv:2409.20168
DOI: 10.1140/epjc/s10052-024-13725-2
```

Used for:

- pointwise chromoelectric-field ancillary data;
- flux-tube profile analysis;
- separation-dependent peak, width, and area diagnostics.

The archive preserves the original `.agr` ancillary files under:

```text
raw_ancillary/baker2024_arxiv_2409_20168v1/
```

---

## Cardoso et al. 2013 — SU(3) control reference

**Inside the SU(3) quark-antiquark QCD flux tube: screening versus quantum widening**

```text
arXiv:1302.3633
```

Retained as a secondary / control source in the provenance map.

---

# Physical-regime interpretation

The completed program represents the confinement sequence as:

```text
color route extension
    ↓
localized flux-tube route
    ↓
increasing boundary pressure
    ↓
threshold-window channel competition
    ↓
repair into color-neutral composite routes
```

In UNNS terminology:

```text
internal colored coordinate
    ↓
non-externalizable isolated route
    ↓
localized tension-bearing route
    ↓
repair threshold
    ↓
admissible closed route
```

The key structural distinction is therefore:

```text
internal existence
≠
external admissibility
```

A colored constituent may be a valid internal coordinate without constituting an externally realizable isolated state.

---

# Static-source spectrum and repair thresholds

The static-source analysis is stored under:

```text
data/01_core_static_potential/
data/02_core_string_breaking/
```

The reconstructed static-source table contains:

```text
57 rows
r range ≈ 0.70686 … 1.6065 fm
```

Important limitation:

> the static levels used in the current repair-window analysis are **model reconstructions from reported parameters**, not raw measured GEVP point data.

The repair-window analysis focuses on the reported string-breaking thresholds:

```text
r_c  = 1.224 fm
r_cs = 1.293 fm
```

with nearest reconstructed rows near:

```text
1.22094 fm
1.28520 fm
```

The corresponding low-lying gaps are approximately:

```text
at r_c:
V1 - V0 ≈ 0.08970 GeV
V2 - V1 ≈ 0.04594 GeV

at r_cs:
V1 - V0 ≈ 0.08642 GeV
V2 - V1 ≈ 0.04639 GeV
```

The UNNS interpretation is not merely that the potential rises with source separation. The structural object is a **channel-reorganization window** in which an extended color route approaches screened / color-neutral alternatives.

---

# Flux-tube branch

The full-QCD flux-tube material is stored under:

```text
data/03_core_flux_tube_profiles/
raw_ancillary/baker2024_arxiv_2409_20168v1/
```

The extended Baker analysis parses:

```text
1090 pointwise rows
10 source files
20 separation labels
```

The program tracks observables such as:

```text
peak field
FWHM / width
profile area
FULL component
NP component
source separation
```

The intended structural mapping is:

```text
source separation d
    → route-extension coordinate

transverse Ex(x_t) profile
    → localized route geometry

peak / width / area
    → local and integrated route descriptors
```

This branch provides the local flux-tube geometry used alongside the static repair-threshold analysis.

---

# Trusted vs review-only data

The project does not treat every extracted ancillary row as equally reliable.

The Baker extension includes:

```text
QC
trusted-summary generation
review-separately decisions
profile overlays
SNR checks
width flags
```

Important reports include:

```text
04_baker_flux_extension_qc.md
05_baker_review_separately_rows.md
```

The chamber inputs are built from the trusted subsets rather than from the uncontrolled ancillary set.

This separation should be preserved in any rerun.

---

# Chamber analysis — flux ladders

The trusted flux observables are converted into chamber ladders under:

```text
chamber_inputs/
```

The six principal flux ladders are:

```text
flux_FULL_area_trusted_ladder.csv
flux_FULL_peak_trusted_ladder.csv
flux_FULL_width_trusted_ladder.csv
flux_NP_area_trusted_ladder.csv
flux_NP_peak_trusted_ladder.csv
flux_NP_width_trusted_ladder.csv
```

## STRUC-I

All six trusted flux ladders are classified as:

```text
Geometric Persistence / Weak Persistence
```

Interpretation:

> the trusted flux observables remain admissible ordered structures under the tested perturbation protocol.

## STRUC-PERC-I

The connectivity results separate global integral measures from local shape descriptors.

```text
FULL_PERCOLATION:
  flux_FULL_area
  flux_NP_area
  flux_NP_peak

HARD_FRAGMENTATION:
  flux_FULL_peak
  flux_FULL_width
  flux_NP_width
```

The project interprets this as a structural distinction rather than as a failed experiment:

```text
area
    → global route-integral coherence

peak / width
    → stronger local / tail-sensitive structure
```

---

# Static repair-window ladders

The repair-threshold branch produces:

```text
static_gap01_repair_window_ladder.csv
static_gap12_repair_window_ladder.csv
```

## STRUC-I

Both are classified as:

```text
Geometric Persistence / Stable Structure
```

## STRUC-PERC-I

The two channels separate:

```text
static_gap01 → FULL_PERCOLATION
static_gap12 → HARD_FRAGMENTATION
```

This is an important result.

The repair window is not represented as one featureless scalar transition. It contains a structured hierarchy in which one gap channel remains globally connected while another remains admissible but fragmented.

---

# Boundary-pressure proxy

The project then consolidates the static repair-window information into a derived scalar coordinate:

```text
Π_boundary(r)
```

The original symbolic form was:

```text
Π_boundary(r)
=
w_gap · C_gap(r)
+
w_thr · C_threshold(r)
+
w_slope · C_slope(r)
+
w_flux · C_flux(r)
```

For the first executable computation, the flux term was deliberately removed to keep the calculation aligned with the validated static repair-window schema:

```text
Π_boundary_static(r)
=
w_gap · C_gap(r)
+
w_thr · C_threshold(r)
+
w_slope · C_slope(r)
```

Effective normalized weights in the stored computation are approximately:

```text
gap       = 0.411765
threshold = 0.352941
slope     = 0.235294
```

The computation uses:

```text
r_fm
gap01_GeV
gap12_GeV
d_gap01_GeV_d_r_GeV_per_fm
d_gap12_GeV_d_r_GeV_per_fm
```

and produces 17 ordered repair-window values.

---

# Boundary-pressure profile

The stored proxy metrics report:

```text
minimum Π_boundary ≈ 0.277572
maximum Π_boundary ≈ 0.765732
mean Π_boundary    ≈ 0.546270
```

The maximum occurs near:

```text
r ≈ 1.22094 fm
```

which is close to the reported light string-breaking threshold:

```text
r_c ≈ 1.224 fm
```

The pressure-band counts are:

```text
MILD_BOUNDARY_TENSION              7
ACTIVE_REPAIR_WINDOW_PRESSURE      9
HIGH_BOUNDARY_PRESSURE_NEAR_REPAIR 1
```

The archive explicitly labels this object as:

> a **static-only structural diagnostic proxy**, not a QCD potential and not a fitted universal confinement law.

---

# Boundary-pressure chamber result

The proxy itself is tested as:

```text
chamber_inputs/boundary_pressure_proxy_ladder.csv
```

with:

```text
n = 17
```

## STRUC-I

Result:

```text
Regime: Geometric Persistence
State:  Stable Structure

mean Aκ    = 1.000000
min Aκ     = 1.000000
Aκ at κmax = 1.000000

mean ρ     = 0.093711
max ρ      = 0.279687
```

Interpretation:

> the proxy remains admissible across the tested STRUC-I perturbation range.

## STRUC-PERC-I

Result:

```text
Verdict: FULL_PERCOLATION

giantRatio       = 1.000000
isolated         = 0
isolatedFraction = 0.000000
κ_connect        = 10
n                = 17
tailDominance    ≈ 0.362492
```

Interpretation:

> the derived proxy is globally connected in the STRUC-PERC-I vulnerability graph.

This is the strongest chamber result in the current confinement chain.

---

# Main synthesis

The completed first-cycle result can be summarized as:

```text
Raw local descriptors may fragment.
The derived confinement-pressure coordinate does not.
```

More explicitly:

```text
flux peak / width
    → admissible but sometimes fragmented

static gap12
    → admissible but fragmented

static gap01
    → admissible and connected

Π_boundary(r)
    → admissible and fully connected
```

This allows the boundary-pressure proxy to act as a **coordinatizing observable** for the tested confinement regime.

It does not erase the structure of the lower-level descriptors. It provides a higher-level coordinate in which the repair-window structure becomes simultaneously:

```text
admissible
and
connected
```

---

# STRUC-I vs STRUC-PERC-I

The archive repeatedly demonstrates why both instruments are retained.

### STRUC-I

Tests:

- ordered-ladder perturbation response;
- admissibility;
- persistence;
- structural pressure.

### STRUC-PERC-I

Tests:

- gap-space connectivity;
- giant-component structure;
- isolation;
- fragmentation;
- percolative realizability.

The color-confinement corpus contains several cases that are STRUC-I admissible but STRUC-PERC-I fragmented.

Therefore:

```text
admissibility ≠ connectivity
```

This distinction is part of the scientific result, not a discrepancy to be removed.

---

# Report chain

The main research sequence is preserved under:

```text
reports/
```

and includes:

```text
01_first_confinement_diagnostic.md
02_repair_threshold_analysis.md
03_flux_tube_separation_extension.md
04_baker_flux_extension_qc.md
05_baker_review_separately_rows.md
06_chamber_alignment_report.md
07_static_repair_window_chamber_report.md
08_color_confinement_chamber_synthesis.md
09_boundary_pressure_proxy_definition.md
10_boundary_pressure_proxy_chamber_report(1).md
11_color_confinement_final_synthesis.md
12_cross_regime_boundary_pressure_comparison_plan.md
```

The completed Phase I workflow is:

```text
collect
    ↓
QC
    ↓
separate trusted / review-only rows
    ↓
construct chamber ladders
    ↓
run STRUC-I and STRUC-PERC-I
    ↓
define boundary-pressure proxy
    ↓
chamber-test the proxy
    ↓
synthesize the confinement regime
```

---

# Principal scripts

The `scripts/` directory contains the reproducible analysis chain:

```text
reconstruct_bulava_model_E_levels.py
make_first_confinement_diagnostic.py
make_repair_threshold_analysis.py

fetch_baker_ancillary.py
extend_baker_flux_profiles_across_separations.py
qc_baker_flux_extension.py
review_baker_review_separately_rows.py

generate_chamber_inputs.py

compute_boundary_pressure_proxy.py
compute_boundary_pressure_proxy_STATIC_ONLY_EXACT_COLUMNS.py
```

Validation utilities at package root include:

```text
validate_pack.py
validate_provenance.py
```

---

# Chamber outputs

Stored results are separated by instrument:

```text
chamber_outputs/
├── STRUC_I/
│   ├── raw_exports/
│   └── summary_tables/
│
└── STRUC_PERC_I/
    ├── raw_exports/
    └── summary_tables/
```

Key exports include:

```text
struc_i_boundary_pressure_proxy_results.json
struc_i_static_repair_window_results.json

struc_perc_batch_results.json
struc_perc_boundary_pressure_proxy_results.json
struc_perc_static_repair_window_results.json
```

This separation should be retained in later extensions.

---

# Logical directory map

```text
color_confinement/
│
├── Color Confinement as Admissibility-by-Closure.pdf
├── Color Confinement.mp4
├── color_confinement_analytics.html
├── chamber_struc_i_v1_0_4.html
├── struc_perc_i_v2_5_0.html
├── img_1cc.png ... img_6cc.png
│
└── color_confinement_data_seed_v0_1_1_provenance/
    ├── README.md
    ├── manifest.json
    ├── validate_pack.py
    ├── validate_provenance.py
    │
    ├── provenance/
    │   ├── DATA_STATUS_GUIDE.md
    │   ├── SOURCE_PROVENANCE.md
    │   └── source_registry.csv
    │
    ├── data/
    │   ├── 01_core_static_potential/
    │   ├── 02_core_string_breaking/
    │   ├── 03_core_flux_tube_profiles/
    │   ├── 04_control_wilson_loops/
    │   ├── 05_control_free_quark_searches/
    │   ├── 06_control_deconfinement_eos/
    │   └── 07_later_hadronization/
    │
    ├── raw_ancillary/
    │   └── baker2024_arxiv_2409_20168v1/
    │
    ├── chamber_inputs/
    ├── chamber_outputs/
    ├── scripts/
    ├── extraction_queue/
    └── reports/
```

---

# Reproducibility

The intended first-cycle workflow is:

```text
published QCD source material
    ↓
provenance classification
    ↓
static-spectrum / flux-profile extraction
    ↓
QC and trusted-row selection
    ↓
repair-window construction
    ↓
chamber ladders
    ↓
STRUC-I
    +
STRUC-PERC-I
    ↓
boundary-pressure proxy
    ↓
proxy chamber validation
    ↓
final regime synthesis
```

For reproducible work:

1. preserve source IDs and row-provenance labels;
2. do not silently promote reconstruction targets into measured data;
3. keep model-reconstructed static levels distinct from raw lattice GEVP measurements;
4. keep trusted Baker rows separate from review-only rows;
5. preserve the exact repair-window schema when recomputing `Π_boundary`;
6. distinguish STRUC-I admissibility from STRUC-PERC-I connectivity;
7. retain the explicit caveat that `Π_boundary` is a structural proxy, not a physical QCD potential.

---

# Phase II direction

The archive also contains:

```text
12_cross_regime_boundary_pressure_comparison_plan.md
```

This document proposes the next research layer:

> **Cross-Regime Boundary-Pressure Comparison**

The first planned comparison is with H-mode plasma confinement.

The shared structural hypothesis is:

```text
local descriptors may fragment
while
a properly constructed global boundary-pressure coordinate stabilizes
```

The proposed cross-regime comparison is intentionally kept separate from the completed color-confinement seed package.

---

# What the current corpus supports

The stored material supports the following conclusions:

- published QCD string-breaking thresholds define a concrete repair-window target;
- Baker ancillary data provide pointwise full-QCD flux-tube geometry;
- trusted flux observables remain STRUC-I admissible;
- some local flux descriptors remain STRUC-PERC-I fragmented;
- both static repair-window gaps remain STRUC-I stable;
- the lower gap is connected while the upper gap remains fragmented;
- a static-only boundary-pressure proxy can be constructed from the repair-window data;
- that proxy is STRUC-I stable and STRUC-PERC-I fully connected.

This is a complete **structural benchmark cycle**.

---

# What the current corpus does not support

The archive explicitly does **not** claim:

- that UNNS derives QCD confinement;
- that `Π_boundary(r)` is a physical QCD potential;
- that the current proxy weights are universal;
- that the static-only proxy is a final confinement law;
- that HARD_FRAGMENTATION implies physical instability;
- that reconstructed static levels are equivalent to raw measured GEVP point data;
- that one completed confinement benchmark proves a universal law across all confinement systems.

These limits are part of the research record and should be retained.

---

# Final structural interpretation

The completed first-cycle synthesis is:

```text
internal color
    ↓
localized tension
    ↓
repair threshold
    ↓
color-neutral closure
    ↓
Π_boundary(r)
    ↓
stable connected structural coordinate
```

The project therefore treats color confinement as a physically grounded example of **admissibility by closure**:

> isolated color remains an internal coordinate, while externally admissible continuation occurs through color-neutral composite closure.

For the public synthesis of this research branch, see:

**[The Physics of Forbidden Isolation: Color Confinement in the UNNS Substrate](https://unns.tech/research/the-physics-of-forbidden-isolation-color-confinement-in-the-unns-substrate)**

