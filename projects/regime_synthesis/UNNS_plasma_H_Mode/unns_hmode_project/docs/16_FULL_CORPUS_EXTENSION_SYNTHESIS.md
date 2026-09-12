# UNNS-H Mode Project — Full-Corpus Extension Synthesis

## 1. Purpose

This document synthesizes the result of extending the event-level UNNS-H Mode edge-admissibility model from the manually reviewed 9-shot suspect set to the full 92-row TCV canonical event corpus.

It belongs here:

```
unns_hmode_project/
  docs/
    16_FULL_CORPUS_EXTENSION_SYNTHESIS.md
```

It follows:

```
docs/
  13_EDGE_EVENT_MODEL_VALIDATION.md
  14_EDGE_EVENT_MODEL_VALIDATION_SYNTHESIS.md
  15_FULL_CORPUS_EDGE_EVENT_EXTENSION_REPORT.md
```

The goal of this synthesis is to state clearly what the full-corpus extension gained, what it weakened, what it preserved, and what must happen next.

---

## 2. Previous status before full-corpus extension

Before this step, the project had a strong internal 9-shot validation result.

The manually reviewed suspect-shot set separated cleanly into:

```
negative_leakage_margin
boundary_ambiguous_margin
positive_boundary_margin
```

with strict ordering:

```
negative < ambiguous < positive
```

That 9-shot result was important, but it was deliberately concentrated on suspect and branch-rich events. It was therefore not enough to claim corpus-level behavior.

The next required question was:

> Does the event-level UNNS-H Mode margin still behave meaningfully when applied to the full 92-row TCV canonical corpus?

This document answers that question.

---

## 3. Full-corpus extension setup

The full-corpus extension was run on:

```
data/processed/tcv_lh_events_canonical.csv
```

with optional time-resolved probe input:

```
data/raw/tcv_zenodo_14996664/LH_DATA.h5
```

The script used was:

```
components/full_corpus_edge_event_extension.py
```

Outputs were written to:

```text
outputs/reports/
  tcv_full_corpus_edge_event_scores.csv
  tcv_full_corpus_state_summary.csv
  tcv_full_corpus_corridor_summary.csv
  tcv_full_corpus_standard_vs_unns_comparison.csv
  tcv_full_corpus_residual_analysis.csv
  tcv_full_corpus_single_variable_auc.csv
  tcv_time_resolved_corridor_inventory.csv
  tcv_full_corpus_edge_event_summary.json
```

The full corpus contains:

```
event rows:   92
unique shots: 66
ILH = 1:      84
ILH = 0:      8
```

---

## 4. Important methodological change

The 9-shot validation model used fragment-family information obtained from the fragment-isolate mapping and suspect-shot review stages.

The full 92-event corpus cannot rely on those manual fragment tags for every row. Therefore the full-corpus extension uses a tag-free numeric generalization of the event-level margin.

The generalized model is:

```
m_edge_event = C_edge_capacity - F_route_fragmentation
```

where:

```
F_route_fragmentation =
  0.35 · S_power_balance
+ 0.35 · S_transport
+ 0.30 · S_timing
```

and:

```
C_edge_capacity =
  0.45 · S_edge_response
+ 0.25 · density_support
+ 0.15 · geometry_stability
+ 0.15 · species_position
```

This is a crucial point.

The full-corpus scores are not a direct repeat of the tag-assisted 9-shot validation. They are a first numerical generalization of the model.

Therefore:

```
9-shot model:       tag-assisted event validation
92-event extension: tag-free numeric generalization
```

The 92-event result should be treated as the first v0.2 generalization test.

---

## 5. Full-corpus state distribution

The full corpus separates into:

```
boundary_ambiguous_margin: 68
positive_boundary_margin:  13
negative_leakage_margin:   11
```

This is the first major result.

The full corpus is not dominated by strong leakage or strong edge-response cases. It is dominated by boundary-ambiguous events.

That means the 9-shot set was correctly understood as a selected suspect set rather than a representative sample of the full corpus.

---

## 6. State-level numerical separation

The full-corpus state summaries are:

```
negative_leakage_margin:
  count  = 11
  mean m = -0.356
  CI95   = [-0.450, -0.270]

boundary_ambiguous_margin:
  count  = 68
  mean m = -0.038
  CI95   = [-0.061, -0.015]

positive_boundary_margin:
  count  = 13
  mean m = +0.341
  CI95   = [+0.297, +0.395]
```

The three state means remain separated.

This supports the existence of a full-corpus corridor structure.

However, unlike the manually reviewed 9-shot set, the full corpus is not organized into extreme non-overlapping branch-rich groups. Most events sit near the boundary.

This is not a failure. It is expected when moving from a suspect subset to a full event table.

The correct interpretation is:

> The three-corridor structure survives the full-corpus extension, but the full corpus is mostly boundary-near rather than strongly separated.

---

## 7. Formal corridor distribution

The full-corpus formal corridors are:

```text
weak_or_unclassified_corridor:                 30
mixed_power_transport_timing_leakage_corridor: 21
timing_only_or_timing_dominant_corridor:       12
power_balance_corridor:                        10
edge_divertor_response_corridor:               10
power_transport_corridor:                      6
transport_timing_corridor:                     2
transport_corridor:                            1
```

The largest class is `weak_or_unclassified_corridor`, followed by the mixed leakage corridor.

This is important because it shows the full corpus contains many ordinary or weakly resolved cases. It does not consist mainly of the branch-rich cases used in the 9-shot analysis.

The edge-divertor response corridor exists in the full corpus, but it is not the dominant class.

---

## 8. Association with ILH

The full-corpus margin has a measurable association with ILH:

```
AUC of m_edge_event for ILH = 1: 0.690
mean difference, ILH=1 minus ILH=0: 0.242
permutation p-value: 0.0022
```

This means the margin is not random with respect to ILH.

The UNNS event-level margin carries signal.

However, this does not mean it is the best binary classifier of ILH. That question requires comparison against standard plasma variables.

---

## 9. Comparison against standard plasma variables

The full-corpus comparison shows:

```
standard_core:
  LOO AUC for ILH=1 = 1.000

standard_core + m_edge_event:
  LOO AUC for ILH=1 = 1.000

standard_edge_inclusive:
  LOO AUC for ILH=1 = 1.000

standard_edge_inclusive + m_edge_event:
  LOO AUC for ILH=1 = 0.999

UNNS_components:
  LOO AUC for ILH=1 = 0.696

UNNS_margin_only:
  LOO AUC for ILH=1 = 0.655
```

This is a sobering and useful result.

The event table already contains standard plasma variables that classify ILH extremely well. Adding `m_edge_event` does not improve the binary ILH classifier.

Therefore, the full-corpus extension does not establish residual binary predictive superiority over standard variables.

The correct conclusion is:

> The current value of `m_edge_event` is structural interpretation and corridor decomposition, not superior binary ILH prediction.

This preserves the scientific value of the UNNS approach while preventing overclaiming.

---

## 10. Residual UNNS contribution

The residual analysis asks:

> After standard plasma variables explain the margin, is the leftover UNNS residual still useful for ILH separation?

The answer is currently no.

The residual analysis shows that standard variables explain a substantial part of `m_edge_event`, and the residual does not add ILH discrimination.

This means:

```
m_edge_event is partly reducible to standard variables in the current event table.
```

This is expected, because the UNNS margin is constructed from physical variables rather than from an independent diagnostic source.

The result does not invalidate the model. It simply bounds the claim.

The UNNS margin is not an independent magic variable. It is a structural recombination of plasma observables into a boundary-admissibility interpretation.

---

## 11. Time-resolved diagnostic probe

The time-resolved inspection of `LH_DATA.h5` found trace coverage for six shots:

```
66464
66465
66468
66527
66530
72681
```

Their corridor coverage is:

```
boundary_ambiguous_margin: 5
negative_leakage_margin:   1
positive_boundary_margin:  0
```

Therefore, the requested time-resolved validation cannot yet be completed for one discharge per corridor.

The available traces do not include a positive-boundary case.

The current file supports a first probe of boundary-ambiguous and negative cases, but not full corridor validation.

---

## 12. Time-resolved first probe result

The boundary-ambiguous ILH=1 traces show post/pre edge-temperature-gradient ratios above 1:

```
66464: ratio ≈ 2.15
66465: ratio ≈ 2.56
66468: ratio ≈ 1.94
66527: ratio ≈ 1.66
72681: ratio ≈ 1.50
```

This suggests that even boundary-ambiguous cases may show edge-profile sharpening after the event time.

However, this is only a first profile-level probe.

It is not yet full time-dependent validation of:

```
m_edge(t)
```

because the current probe does not include direct edge turbulence, radial electric field, E×B shear, confinement-time response, ELM timing, or a positive-boundary trace.

---

## 13. What the full-corpus extension establishes

The full-corpus extension establishes five things.

### 13.1 The margin is computable beyond the suspect set

`m_edge_event` can be computed across all 92 canonical TCV event rows without manual branch tags.

This is a major operational gain.

### 13.2 The three-corridor structure survives

The corpus separates into negative, ambiguous, and positive margin states.

However, the dominant state is boundary-ambiguous.

This means the full event table sits mostly near the boundary rather than in strongly separated extremes.

### 13.3 The margin has real ILH association

The AUC of approximately 0.69 and the permutation p-value of approximately 0.0022 show that `m_edge_event` is not random with respect to ILH.

### 13.4 The margin is not a superior binary classifier

Standard plasma variables classify ILH extremely well in the event table.

The UNNS margin does not currently improve that classification.

### 13.5 Time-series validation is not yet complete

Available time traces cover boundary-ambiguous and negative cases, but not positive-boundary cases.

A positive-boundary discharge must be obtained before one-discharge-per-corridor time validation can be claimed.

---

## 14. What the full-corpus extension does not establish

This extension does not prove the physical origin of H-mode.

It does not establish the full time-dependent edge margin:

```
m_edge(t)
```

It does not prove cross-machine generality.

It does not show residual predictive superiority over standard variables.

It does not yet validate the model on one time-resolved discharge per corridor.

It does not replace plasma-physics mechanisms such as radial electric field formation, E×B shear, turbulence suppression, pedestal formation, or edge/divertor dynamics.

The correct framing is:

> The UNNS model currently provides a structural organization of the event table, not a replacement for plasma physics.

---

## 15. How the interpretation changes after this result

Before the full-corpus extension, the strongest interpretation was:

> The 9 reviewed suspect shots separate cleanly into leakage-like, ambiguous, and edge-response corridors.

After the full-corpus extension, the interpretation becomes more precise:

> The full 92-event TCV corpus supports a tag-free event-level margin with measurable ILH association and three-corridor structure, but most events are boundary-near, and standard plasma variables already classify ILH strongly.

This is a more mature and more credible result.

It prevents the project from overclaiming while preserving the central structural insight.

---

## 16. Updated project status

```text
project structure                         complete
TCV ingestion                              complete
STRUC-I baseline                           complete
STRUC-PERC-I fragmentation test            complete
fragment-isolate mapping                   complete
suspect-shot review                        complete
manual physical review                     complete
event-level edge-admissibility model       complete
9-shot model validation                    complete
validation synthesis                       complete
full 92-event extension                    complete
standard-variable comparison               complete
residual analysis                          complete
time-resolved inventory/probe              partial
positive-boundary time trace               missing
full m_edge(t) validation                  not yet
cross-machine validation                   not yet
technical note / manuscript                not yet
```

---

## 17. Recommended next steps

### Step 1 — Freeze the v0.2 full-corpus scoring definition

The tag-free full-corpus formula should be frozen as:

```
m_edge_event v0.2
```

This allows reproducibility and prevents accidental retuning after seeing results.

### Step 2 — Produce a full-corpus dashboard update

The previous 9-shot dashboard should not be replaced. Instead, create a second dashboard:

```
site/
  unns_hmode_full_corpus_extension_dashboard.html
```

Its purpose should be different:

```
9-shot dashboard:
  shows strong branch-rich corridor validation

92-event dashboard:
  shows full-corpus generalization, boundary dominance, and bounded claims
```

### Step 3 — Search for positive-boundary time traces

The current `LH_DATA.h5` inventory lacks positive-boundary coverage.

Priority positive-boundary candidates include the strongest positive cases from the full-corpus score table and/or the earlier reviewed positive corridor:

```
66445
69892
68719
```

A time-resolved trace for at least one positive-boundary discharge is required.

### Step 4 — Build a minimal m_edge(t) prototype

Once one discharge per corridor is available, build:

```
components/time_resolved_edge_margin_probe.py
```

Target output:

```
outputs/reports/tcv_time_resolved_edge_margin_probe.csv
docs/17_TIME_RESOLVED_EDGE_MARGIN_PROBE.md
```

### Step 5 — Prepare a technical note only after the time-resolved gap is addressed

The project is close to a technical note, but the missing positive-boundary time trace is now the main evidence gap.

---

## 18. Final synthesis statement

The full 92-event TCV extension succeeded.

It confirmed that the UNNS event-level edge-admissibility margin can be computed across the complete canonical event corpus and that it has a statistically measurable association with ILH.

It also showed that the full corpus is mostly boundary-ambiguous and that standard plasma variables already classify ILH extremely well.

Therefore, the UNNS contribution at this stage is not superior binary prediction. It is structural organization:

> `m_edge_event` reorganizes the TCV event table into leakage-like, boundary-ambiguous, and edge-response corridors, revealing how power-balance, transport, timing, and edge-response terms oppose each other in an event-level boundary-admissibility model.

The next decisive task is not another event-level classifier. It is time-resolved validation of `m_edge(t)`, especially for a positive-boundary discharge.
