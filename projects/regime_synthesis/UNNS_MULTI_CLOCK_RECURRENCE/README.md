# UNNS Multi-Clock Recurrence

This directory contains the complete research record for the **UNNS Multi-Clock Recurrence** program: source corpora, neutral ingests, representation bake-offs, drive-torus and fractional-cover methods, external validation, specificity controls, grammar development and freeze, prospective testing, and the final one-shot re-evaluation of the historical C003 time-quasi-crystal case.

The project was created after the earlier **TIME-CRYSTAL-I v1.1.0** integer-depth grammar encountered a physically important boundary case: a robust quasi-periodically driven time-crystalline system that was not admitted as supported integer-depth recurrence.

The central question of this program is therefore:

> **Can a frozen two-clock structural grammar recognize organized quasi-periodic temporal order without being tuned to the target system after the fact?**

The answer preserved by this archive is deliberately mixed rather than simplified:

- several development and validation datasets exhibit strong source-defined two-clock organization;
- a compact multi-clock grammar could be selected and frozen without using C003;
- the first prospective external transfer **failed** on its predeclared positive candidate;
- the historical C003 candidate was then evaluated exactly once under the unchanged frozen grammar;
- C003 remained outside the second grammar as well.

This is why the public synthesis is framed around a time crystal that **broke two grammars**.

## Public research reference

The associated public UNNS article is:

**[The Time Crystal That Broke Two Grammars](https://unns.tech/research/the-time-crystal-that-broke-two-grammars)**

This article provides the public-facing synthesis of the integer-depth failure, multi-clock grammar development, prospective limitation, and final C003 boundary result preserved in this directory.

---

# Main research artifacts

### `Beyond_Integer_Depth.pdf`

Primary manuscript for the multi-clock recurrence program.

It develops the transition from ordinary integer-depth temporal recurrence to a source-defined two-clock structural grammar.

### `Multi clock recurrence dashboard · HTML.html`

Interactive project dashboard.

### `MULTI_CLOCK_RECURRENCE_ANALYTICS.html`

Detailed analytical companion report.

### `img_mc1.png` … `img_mc5.png`

Figures supporting the manuscript and public synthesis.

---

# Scientific workspace

The main reproducibility corpus is stored under:

```text
UNNS_MULTI_CLOCK_RECURRENCE/
```

Its principal structure is:

```text
UNNS_MULTI_CLOCK_RECURRENCE/
├── 00_PROTOCOL/
├── 01_SOURCES/
├── 02_RAW/
├── 03_INGEST/
├── 04_CORPUS/
├── 05_METHODS/
├── 06_VALIDATION/
├── 07_HOLDOUT/
├── 08_OUTPUTS/
└── 09_DOCS/
```

The archive is methodologically staged. Development, validation, prospective testing, and final historical boundary evaluation are intentionally separated.

---

# Research firewall

The project preserves an explicit research firewall.

Its central discipline is:

```text
develop
    ↓
validate
    ↓
stress-test
    ↓
select compact grammar
    ↓
freeze
    ↓
prospective unseen test
    ↓
only then open C003
```

C003 was deliberately excluded from method development and grammar freezing.

The frozen grammar record confirms:

```text
C003_loaded_at_freeze = false
```

and the prospective firewall prohibits:

- threshold changes after candidate ingest;
- null-model changes after candidate ingest;
- robustness changes after candidate ingest;
- representation changes after candidate ingest;
- opening C003 before the prospective reveal.

---

# Source corpus

The archive preserves several independent or adjacent-domain source families.

## Huang 2025

Stored under:

```text
01_SOURCES/HUANG_2025/
02_RAW/HUANG_2025/
03_INGEST/HUANG/
```

The neutral ingest includes:

```text
HUANG_LC.csv
HUANG_QP.csv
HUANG_CHAOS.csv
```

These trajectories provide limit-cycle, quasi-periodic, and chaotic reference behavior for early representation testing.

---

## Luo 2026

Stored under:

```text
01_SOURCES/LUO_2026/
02_RAW/LUO_2026/
03_INGEST/LUO/
```

The Luo corpus contains multiple source-native time-domain observables, including:

```text
M
F
entanglement entropy
```

across low-frequency, DTQC, and high-frequency regimes and multiple system sizes.

Important records include:

```text
LUO_EE_LOW_N12
LUO_EE_LOW_N32
LUO_EE_DTQC_N12
LUO_EE_DTQC_N32
LUO_EE_HIGH_N12
LUO_EE_HIGH_N32
```

This corpus became the main development platform for the source-defined two-clock analysis.

---

## Zhu 2026

Stored under:

```text
01_SOURCES/Zhu 2026/
06_VALIDATION/ZHU_2026/
```

Zhu was originally protected as a holdout.

Its locked validation outcome was:

```text
PARTIAL_TRANSFER_WITH_COVER_DEPTH_FAILURE
```

The source-defined two-clock organization transferred, but the first automatic depth-selection rule did not.

That failure was preserved and directly motivated the parent-vs-fractional decomposition used in the next method.

---

## Malz–Smith 2021

Stored under:

```text
02_RAW/MALZ_SMITH_2021/
06_VALIDATION/MALZ_SMITH_2021/
```

This corpus provides an independent **two-clock non-DTQC specificity challenge**.

The preserved result is:

```text
PASS_STRONG_SPECIFICITY_CHALLENGE
```

The experiment shows strong source-torus organization, but little or negative incremental fractional-cover organization.

This establishes that:

```text
two incommensurate clocks
```

do not automatically produce the fractional signature developed for the DTQC-positive corpus.

---

# 1. Neutral ingestion

The first completed corpus stage contains:

```text
13 canonical time-domain records
```

with audit status:

```text
PASS_NEUTRAL_INGEST
```

The neutral ingestion stage standardizes source trajectories without introducing classification thresholds or target-specific response frequencies.

The preserved corpus-state documentation also distinguishes:

```text
ZHU_2026      → validation consumed
MOON_2025     → access restricted
HIST_C003     → do not calibrate
```

---

# 2. Representation bake-off — `BAKEOFF_v001`

The first representation bake-off compares several possible multi-clock descriptions.

The main findings are negative and diagnostic.

## Frequency lattice

A two-dimensional spectral lattice detects genuine multi-frequency organization.

For example, Luo development records show strong lattice gain in the DTQC regime.

However, the high-frequency decoupled control remains strongly lattice-organized.

Therefore:

```text
multi-frequency organization
≠
coupled DTQC organization
```

## Observable-derived torus

This representation fails specificity.

For the N=32 entanglement triplet:

```text
low-frequency control   torus R² ≈ 0.9254
DTQC                     torus R² ≈ 0.7171
high-frequency control   torus R² ≈ 0.9235
```

The proper DTQC regime does not maximize the score.

## Vector recurrence

This also fails as a standalone discriminator.

The high-frequency decoupled control can exceed the DTQC regime, while Huang quasi-periodic and chaotic traces can both show nearly saturated recurrence-pair scores.

The result of the bake-off is therefore:

> do not build a multi-clock classifier from raw spectral organization or recurrence alone.

---

# 3. Source-defined drive torus — `DRIVE_TORUS_v002`

The next method anchors the chart to the **externally specified drive clocks** rather than to frequencies inferred from the measured response.

This reverses the earlier specificity failure.

For Luo N=32:

| Regime | Full source-torus R² | Axis-only R² | Mixed interaction gain | Mean entanglement |
|---|---:|---:|---:|---:|
| Low-frequency aperiodic | 0.1213 | 0.0697 | 0.0515 | 0.5853 |
| Intermediate DTQC | **0.9409** | 0.7167 | **0.2242** | 0.2425 |
| High-frequency decoupled | 0.6976 | 0.5972 | 0.1004 | 0.0719 |

The key result is that the DTQC regime has the strongest joint-drive organization.

However:

```text
d = 2
```

is selected for all three regimes.

Therefore two-cover recurrence is still **not** equivalent to DTQC admissibility.

The archive keeps coupling / entanglement as a separate physical axis.

The development vector at this stage is:

```text
M = (T_source, J_mixed, S_coupling)
```

rather than one scalar score.

---

# 4. Zhu validation and the depth-selection failure

The Zhu validation transferred the source-defined two-clock organization but broke the initial automatic cover-depth rule.

Both Zhu records selected:

```text
best_cover_depth = 1
```

instead of the predeclared:

```text
d = 2
```

The project did not hide or retune this failure.

Post-validation diagnosis showed that:

```text
d = 1
```

was representing the strong **integer source / mixing lattice**, while:

```text
d = 2
```

represented the first **fractional cover sector**.

For Zhu, strong parent-drive or difference-frequency content could therefore beat the fractional sector in total explained variance even when genuine fractional organization was present.

This led to a conceptual correction:

```text
integer parent lattice
    ↓
additional fractional-cover organization
    ↓
independent coupling / collective sector
```

rather than making integer and fractional sectors compete for one maximum-R² label.

---

# 5. Fractional-cover method — `FC_v003`

The corrected v003 method explicitly separates:

1. parent source/mixing structure;
2. incremental fractional-cover structure;
3. collective / coupling evidence.

For Luo N=32:

| Regime | Parent R² | Fractional axis gain | Fractional mixed gain | Fractional total gain | Mean S |
|---|---:|---:|---:|---:|---:|
| LOW | 0.002072 | 0.076870 | 0.051774 | 0.128645 | 0.585326 |
| DTQC | 0.012515 | 0.717709 | 0.224366 | 0.942075 | 0.242481 |
| HIGH | 0.035786 | 0.598050 | 0.100526 | 0.698576 | 0.071881 |

The DTQC regime has the strongest:

```text
fractional total gain
fractional mixed gain
```

but the high-frequency decoupled control still retains substantial fractional structure.

Therefore:

> fractional temporal organization alone is not sufficient for physical DTQC admissibility.

The coupling / collective sector remains independent.

---

# 6. Cross-representation study

The project next compares several representation families directly.

Its main conclusion is that they do **not** collapse to one universal coordinate.

The useful layered structure is:

```text
integer/source recurrence
    ↓
fractional joint-phase recurrence
    ↓
fractional mixed-clock organization
    ↓
independent collective/coupling evidence
```

The strongest temporal discriminator emerging from the development corpus is:

```text
FC_frac_mixed_gain
```

while joint-phase recurrence provides an important chart / domain coordinate.

Vector-depth recurrence and raw frequency-lattice alignment remain useful descriptive views but are too permissive to define admission on their own.

---

# 7. Specificity challenge — Malz–Smith

The Malz–Smith experiment is an independent two-clock system that is highly organized on the integer parent torus.

Yet its fractional-cover contribution remains weak or negative.

Median fractional-total gain in the topological regime is near zero or negative across X, Y, and Z components.

The preserved conclusion is:

> the v003 fractional-cover signature is not a generic consequence of having two incommensurate clocks.

This is an important negative-domain specificity result.

It does **not** by itself prove that v003 is a complete DTQC classifier.

---

# 8. Grammar development

The grammar-development stage combines:

- null models;
- robustness tests;
- control discrimination;
- representation redundancy analysis;
- source-domain checks.

The development evidence supports four separate sectors:

```text
P_src
    parent/source organization

J_frac
    fractional joint-phase chart coordinate

M_frac
    fractional mixed-clock temporal coordinate

C_coll
    independent source-native collective/coupling evidence
```

The archive rejects a one-number universal DTQC score.

---

# 9. Compact grammar selection

The selected compact architecture is:

```text
D_2clk → [ P_src ; J_frac | M_frac ]
```

with a separate physical extension:

```text
+ C_coll
```

where:

```text
D_2clk
```

is the two-clock chart domain.

### `P_src`

Source-torus anchor:

```text
metric: JPR_parent_gain
null: PHASE_LABEL_PERMUTE
gate: p_upper <= 0.10
```

### `J_frac`

Fractional joint-phase chart coordinate:

```text
JPR_cover_advantage
```

It is reported but **not** used as a hard admission gate.

### `M_frac`

Primary temporal decision coordinate:

```text
metric: FC_frac_mixed_gain
raw gate: M_frac >= 0.12
hard null: FOURIER_PHASE
null gate: p_upper <= 0.10
```

The raw `M_frac` threshold must also remain satisfied under the frozen robustness suite.

### `C_coll`

Independent domain-specific physical evidence interface.

No fabricated universal cross-platform coupling scalar is introduced.

---

# 10. Frozen grammar — `MC_GRAMMAR_v001`

The compact grammar was frozen before prospective testing.

The machine-readable frozen record is:

```text
08_OUTPUTS/GRAMMAR_FREEZE_v001/FROZEN_GRAMMAR.json
```

Frozen status:

```text
grammar: MC_GRAMMAR_v001
status: FROZEN
freeze stage: pre-prospective
```

The empirical ratio domain of v001 is explicitly limited to the:

```text
golden-ratio branch
```

A different irrational ratio is therefore not automatically a negative result; it is outside the empirically qualified ratio domain of this version.

---

# Frozen robustness suite

The frozen temporal grammar must survive:

```text
temporal-origin shift
clock exchange
coordinatewise affine state transform
×5 downsampling
first 75% of the trajectory
2% RMS additive noise
```

If `M_frac >= 0.12` fails under any of these, the frozen state becomes:

```text
MIXED_ORGANIZATION_UNSTABLE
```

---

# Frozen temporal-state vocabulary

The state precedence is:

```text
OUTSIDE_CHART_DOMAIN
OUTSIDE_EMPIRICALLY_QUALIFIED_RATIO_DOMAIN
SOURCE_UNANCHORED
MIXED_ORGANIZATION_WEAK
MIXED_ORGANIZATION_SPECTRAL_NULL
MIXED_ORGANIZATION_UNSTABLE
TEMPORAL_CORE_SUPPORTED
```

This vocabulary is fixed for `MC_GRAMMAR_v001`.

Changing it requires a new grammar version.

---

# 11. Prospective P001 campaign

The first prospective unseen candidate/control test is stored under:

```text
06_VALIDATION/PROSPECTIVE_P01/
08_OUTPUTS/PROSPECTIVE_P01/
```

The trajectories were generated from the Marripour–Abouie 2026 Hamiltonian family under a pre-generation lock.

The blinded pair used two frequency-scale conditions, with A/B assignment sealed before analysis.

## Revealed result

The high-frequency candidate hypothesis was:

```text
P001_B
```

Frozen state:

```text
MIXED_ORGANIZATION_WEAK
```

Key values:

```text
P_src p = 0.010
J_frac = -0.166375
M_frac = -0.330050
Fourier-phase p = 1.000
minimum robust M_frac = -1.024544
```

The predeclared expectation was:

```text
TEMPORAL_CORE_SUPPORTED
```

and it was **not met**.

The low-frequency breakdown control was also not admitted, as expected.

Formal prospective verdict:

```text
PROSPECTIVE_FAILURE_CANDIDATE_REJECTED
```

This failure is preserved.

The grammar was not altered afterward.

---

# 12. C003 — the time crystal that broke two grammars

C003 is the historical boundary case that motivated the entire multi-clock branch.

Its source is:

```text
rawdata.xls
sheet: Fig. 1
```

containing signed polarization dynamics from a **quasi-periodically driven interacting NV-spin ensemble**.

The documented clock ratio is:

```text
tau2 / tau1 = 1.618
```

The fixed mapping is:

```text
candidate:
robust long-interaction representative dynamics
Fig.1d

control:
short-interaction breakdown regime
Fig.1b
```

No interpolation, filtering, sign alignment, favorable sub-window selection, or response-frequency injection is used in the final multi-clock evaluation.

---

## First grammar — TIME-CRYSTAL-I v1.1.0

Under the frozen integer-depth grammar:

### C003 candidate

```text
q0 = 6
C = 0.198765
F = 0.093433
p = 0.960199

NO_TEMPORAL_ORDER
```

### Matched control

```text
q0 = 6
C = 0.094640
F = 0.030874
p = 0.995025

NO_TEMPORAL_ORDER
```

The earlier interpretation was not that the physical experiment lacked temporal order.

It was that the robust quasi-periodic state lay outside the supported **integer-depth recurrence grammar**.

That result motivated the multi-clock research branch.

---

## Second grammar — `MC_GRAMMAR_v001`

C003 was evaluated only after:

```text
development
validation
grammar selection
freeze
prospective P001 reveal
```

had all been completed.

### C003 candidate — Fig.1d

```text
P_src phase-label p = 1.000
J_frac = 0.910688
M_frac = 0.596092
Fourier-phase p = 0.020
minimum robust M_frac = 0.595093
state = SOURCE_UNANCHORED
```

The candidate has:

- strong fractional-cover organization;
- strong mixed-clock gain;
- a significant Fourier-phase null result;
- robust `M_frac`.

But it fails the frozen **source-anchor** clause:

```text
P_src p <= 0.10
```

because:

```text
P_src p = 1.000
```

### Matched breakdown control — Fig.1b

```text
P_src p = 0.010
J_frac = -0.593846
M_frac = -0.003958
Fourier-phase p = 0.780
minimum robust M_frac = -0.558942
state = MIXED_ORGANIZATION_WEAK
```

Formal outcome:

```text
C003_REMAINS_OUTSIDE_FROZEN_MULTI_CLOCK_GRAMMAR
```

The grammar was not changed for C003.

---

# Why the C003 result matters

C003 is not simply a false negative in an otherwise universally permissive method.

The archive already contains a failed prospective transfer:

```text
P001 candidate → rejected
```

before C003 was opened.

Therefore the final C003 result sits inside a documented method that had already shown it could reject physically motivated external candidates.

The important scientific point is:

> the robust C003 quasi-periodic time-crystalline state carries strong fractional and mixed-clock organization, yet still violates the exact source-anchor logic selected and frozen from the development corpus.

This makes C003 a genuine **grammar-boundary object**.

It broke:

1. the integer-depth temporal grammar;
2. the frozen multi-clock recurrence grammar.

That boundary result is retained rather than repaired away.

---

# Reproducing C003

The final one-shot evaluation is stored under:

```text
06_VALIDATION/C003_FINAL_v001/
08_OUTPUTS/C003_FINAL_v001/
```

The normal reproduction uses the canonical ingest CSVs already stored in the project:

```text
TC_P01_C003.csv
TC_P01_C003_CTRL.csv
```

and does not require the historical `rawdata.xls`.

Run:

```text
python run_C003_final.py
```

then:

```text
python verify_C003_final.py
```

A successful verification reproduces the historical quantitative lock.

The reproduction guide is:

```text
06_VALIDATION/C003_FINAL_v001/REPRODUCE_C003_FINAL.md
```

---

# Important methodological result

The completed program does **not** support one universal scalar definition of multi-clock temporal order.

Instead it reveals a layered structure:

```text
chart-domain validity
    ↓
source-torus anchoring
    ↓
fractional joint-phase organization
    ↓
mixed fractional organization
    ↓
robustness
    ↓
independent collective / coupling context
```

Different physical systems can fail at different layers.

That is why the archive preserves named failure states rather than reducing every outcome to one binary number.

---

# Logical directory map

```text
UNNS_MULTI_CLOCK_RECURRENCE/
│
├── Beyond_Integer_Depth.pdf
├── Multi clock recurrence dashboard · HTML.html
├── MULTI_CLOCK_RECURRENCE_ANALYTICS.html
├── img_mc1.png ... img_mc5.png
│
└── UNNS_MULTI_CLOCK_RECURRENCE/
    ├── 00_PROTOCOL/
    │   └── RESEARCH_FIREWALL.md
    │
    ├── 01_SOURCES/
    │   ├── HUANG_2025/
    │   ├── LUO_2026/
    │   ├── MOON_2025/
    │   └── Zhu 2026/
    │
    ├── 02_RAW/
    │   ├── HUANG_2025/
    │   ├── LUO_2026/
    │   ├── MALZ_SMITH_2021/
    │   ├── MOON_2025/
    │   └── Zhu 2026/
    │
    ├── 03_INGEST/
    │   ├── HUANG/
    │   └── LUO/
    │
    ├── 04_CORPUS/
    │   ├── CORPUS_v001.csv
    │   ├── CORPUS_v001.json
    │   ├── CORPUS_STATUS_v002.json
    │   └── CROSS_CHART/
    │
    ├── 05_METHODS/
    │   ├── bakeoff_v001.py
    │   ├── drive_torus_coupling_v002.py
    │   ├── fc_v003.py
    │   ├── rep_study_v002.py
    │   ├── grammar_dev_v001.py
    │   ├── grammar_select_v001.py
    │   ├── mc_grammar_v001.py
    │   ├── METHOD_SPEC.md
    │   ├── PROSPECTIVE_PROTOCOL_v001.md
    │   └── method / grammar specifications
    │
    ├── 06_VALIDATION/
    │   ├── ZHU_2026/
    │   ├── MALZ_SMITH_2021/
    │   ├── PROSPECTIVE_P01/
    │   └── C003_FINAL_v001/
    │
    ├── 07_HOLDOUT/
    │
    ├── 08_OUTPUTS/
    │   ├── BAKEOFF_v001/
    │   ├── DRIVE_TORUS_v002/
    │   ├── FC_v003/
    │   ├── REP_STUDY_v002/
    │   ├── GRAMMAR_DEV_v001/
    │   ├── GRAMMAR_SELECT_v001/
    │   ├── GRAMMAR_FREEZE_v001/
    │   ├── PROSPECTIVE_P01/
    │   └── C003_FINAL_v001/
    │
    └── 09_DOCS/
        ├── RECOVERY_STATUS.md
        └── SHA256SUMS.txt
```

---

# Reproducibility sequence

The intended research sequence is:

```text
source acquisition
    ↓
neutral ingest
    ↓
representation bake-off
    ↓
source-defined drive torus
    ↓
external Zhu validation
    ↓
depth-failure diagnosis
    ↓
fractional-cover v003
    ↓
Malz–Smith specificity challenge
    ↓
cross-representation study
    ↓
nulls + robustness + controls
    ↓
compact grammar selection
    ↓
grammar freeze
    ↓
prospective P001 campaign
    ↓
reveal prospective failure
    ↓
one-shot C003 evaluation
```

For a faithful reproduction:

1. preserve source / development / validation / holdout roles;
2. do not use C003 to recalibrate `MC_GRAMMAR_v001`;
3. retain the golden-ratio qualification boundary of v001;
4. keep `P_src`, `J_frac`, `M_frac`, and `C_coll` conceptually distinct;
5. retain the Fourier-phase and phase-label null models;
6. preserve the frozen robustness suite;
7. do not reinterpret the failed P001 candidate as a successful prospective test;
8. do not alter the C003 state after observing its result.

---

# What this archive establishes

The preserved record supports the following conclusions:

- naive recurrence, inferred-torus, and raw frequency-lattice coordinates are insufficient by themselves;
- source-defined drive phases produce a more meaningful multi-clock chart;
- integer parent organization and fractional-cover organization are structurally distinct;
- fractional mixed-clock gain is a strong temporal discriminator in the development corpus;
- a separate collective / coupling sector remains necessary for physical interpretation;
- independent two-clock non-DTQC systems need not reproduce the fractional-cover signature;
- a compact grammar can be selected and frozen without using C003;
- the first prospective candidate under that grammar was rejected;
- C003 remains outside the frozen multi-clock grammar despite strong fractional organization;
- therefore C003 is a real boundary case for both the earlier integer-depth grammar and the later multi-clock grammar.

---

# What this archive does not establish

The project does **not** establish:

- a universal detector of all quasi-periodic time-crystalline order;
- that every DTQC must satisfy `MC_GRAMMAR_v001`;
- that `M_frac` alone defines a DTQC;
- that `J_frac` alone defines a DTQC;
- that the golden-ratio branch generalizes automatically to all irrational ratios;
- that a failed source-anchor clause means the physical system lacks organized temporal order;
- that the failed P001 transfer invalidates all multi-clock structure;
- that C003 should be forced into the frozen grammar by threshold changes.

The strongest defensible conclusion is narrower:

> **MC_GRAMMAR_v001 captures one empirically developed class of source-anchored fractional multi-clock organization, and C003 lies outside that class despite exhibiting strong robust fractional structure.**

That boundary is scientifically informative.

---

# Future direction

The C003 result motivates a future grammar that is structurally different rather than a post-hoc repair of v001.

Possible questions include:

```text
Can source anchoring be reformulated without losing specificity?

Can robust fractional organization define a separate admissibility branch?

Can joint-phase structure be represented on a more general toroidal or irrational-cover geometry?

Can a future grammar distinguish source-unanchored yet physically robust quasi-periodic order from generic quasiperiodicity?
```

Any such work requires:

```text
new grammar version
new development corpus
new freeze
new unseen prospective candidates
```

C003 must remain associated with the frozen v001 result.

---

# Public reference

For the public synthesis of this research branch, see:

**[The Time Crystal That Broke Two Grammars](https://unns.tech/research/the-time-crystal-that-broke-two-grammars)**

