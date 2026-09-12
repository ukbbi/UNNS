# TokaMark Cross-Shot m_edge(t) Comparison

## 1. Purpose

This document records the first cross-shot comparison of the normalized UNNS-H Mode `m_edge(t)` probe on public MAST/TokaMark data.

It belongs here:

```text
unns_hmode_project/
  docs/
    21_TOKAMARK_CROSS_SHOT_M_EDGE_COMPARISON.md
```

It follows:

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```

The previous step showed that reference shot `12063` has an internally interpretable `m_edge(t)` trace. This document asks the next necessary question:

> Does shot `12063` remain structurally stronger when compared against a weaker TokaMark candidate under the same pipeline?

The answer is yes under the v0.1 normalized probe.

---

## 2. Compared shots

The comparison used:

```text
reference shot:  12063
comparison shot: 11830
```

The reference shot was selected because it was the strongest metadata candidate:

```text
shot 12063
class: FULL_PROFILE_EDGE_CANDIDATE
core signals: 8/8
Thomson profile signals: 2/2
soft-X edge/activity signals: 2/2
```

The comparison shot was selected as a weaker but still usable control:

```text
shot 11830
class: PROFILE_DALPHA_CANDIDATE
core signals: 8/8
Thomson profile signals: 2/2
soft-X edge/activity signals: 0/2
```

This makes shot `11830` a useful first comparison because it preserves core and Thomson coverage but lacks soft-X edge-activity support. It is therefore weaker than `12063`, but not so incomplete that the comparison is dominated only by missingness.

---

## 3. Pipeline parity

Both shots were processed through the same pipeline:

```text
1. one-shot array probe
2. normalized m_edge(t) probe
3. trace-level inspection
4. cross-shot comparison
```

The comparator used:

```text
components/
  tokamark_cross_shot_m_edge_comparator.py
```

The source outputs were:

```text
outputs/reports/
  tokamark_shot_12063_m_edge_t_probe.csv
  tokamark_shot_12063_m_edge_trace_inspection_summary.json
  tokamark_shot_11830_m_edge_t_probe.csv
  tokamark_shot_11830_m_edge_trace_inspection_summary.json
```

The comparison output was:

```text
outputs/reports/
  tokamark_cross_shot_m_edge_comparison.csv
  tokamark_cross_shot_m_edge_comparison.json
  tokamark_cross_shot_m_edge_comparison.md
```

---

## 4. Core comparison table

|   shot_id | candidate_class             |   candidate_score |   positive_boundary_margin_fraction |   negative_leakage_margin_fraction |   boundary_ambiguous_margin_fraction |   insufficient_data_fraction |   m_edge_median |   m_edge_mean |   m_edge_min |   m_edge_max |   C_edge_capacity_median |   F_route_fragmentation_median |   S_edge_response_median |   S_power_balance_median |   S_transport_median |   missingness_pressure_median |   interpretable_positive_count |   interpretable_negative_count |   interpretable_positive_total_duration |   interpretable_negative_total_duration |
|----------:|:----------------------------|------------------:|------------------------------------:|-----------------------------------:|-------------------------------------:|-----------------------------:|----------------:|--------------:|-------------:|-------------:|-------------------------:|-------------------------------:|-------------------------:|-------------------------:|---------------------:|------------------------------:|-------------------------------:|-------------------------------:|----------------------------------------:|----------------------------------------:|
|     12063 | FULL_PROFILE_EDGE_CANDIDATE |            97.143 |                            0.258216 |                           0.112676 |                             0.49061  |                     0.138498 |       0.087961  |     0.055111  |    -0.770609 |     0.475695 |                 0.559422 |                       0.516301 |                 0.572315 |                 0.569205 |             0.484131 |                      0.222222 |                              8 |                              3 |                                   0.035 |                                   0.016 |
|     11830 | PROFILE_DALPHA_CANDIDATE    |            81.429 |                            0.226064 |                           0.228723 |                             0.390957 |                     0.154255 |      -0.0366668 |     0.0050537 |    -0.745802 |     0.387901 |                 0.612696 |                       0.694692 |                 0.499333 |                 0.710196 |             0.481211 |                      0.222222 |                              2 |                              0 |                                   0.077 |                                   0     |

---

## 5. Comparator decision

The comparator returned:

```text
decision: reference_structurally_stronger
```

The decision was supported by:

```text
- reference_has_more_interpretable_positive_windows
- reference_has_higher_positive_fraction
- reference_has_higher_peak_m_edge
```

The measured deltas were:

```text
delta positive fraction
  comparison - reference = -0.032152133

delta interpretable positive count
  comparison - reference = -6

delta missingness median
  comparison - reference = 0
```

The missingness median did not increase in the comparison shot, so the result is not explained simply by a missing-data penalty.

---

## 6. Main numerical contrast

### 6.1 Positive-boundary fraction

```text
shot 12063: 0.258216
shot 11830: 0.226064
```

Shot `12063` has the higher positive-boundary fraction.

### 6.2 Negative-leakage fraction

```text
shot 12063: 0.112676
shot 11830: 0.228723
```

Shot `11830` has approximately twice the negative-leakage fraction of `12063`.

### 6.3 Median m_edge

```text
shot 12063: 0.087961
shot 11830: -0.0366668
```

The reference shot has a positive median `m_edge`, while the comparison shot has a negative median `m_edge`.

### 6.4 Peak m_edge

```text
shot 12063: 0.475695
shot 11830: 0.387901
```

The reference shot has the higher peak `m_edge`.

### 6.5 Interpretable positive windows

```text
shot 12063: 8
shot 11830: 2
```

Shot `12063` has four times as many interpretable positive windows as shot `11830`.

---

## 7. Structural interpretation

The comparison supports the claim that shot `12063` is structurally stronger under the v0.1 normalized `m_edge(t)` probe.

The contrast is not merely that `12063` has more data. The important difference is structural:

```text
12063:
  more positive-boundary fraction
  fewer negative-leakage points
  positive median m_edge
  higher peak m_edge
  8 interpretable positive windows
  3 interpretable negative windows

11830:
  lower positive-boundary fraction
  higher negative-leakage fraction
  negative median m_edge
  lower peak m_edge
  only 2 interpretable positive windows
  0 interpretable negative windows
  2 fragile positive windows
  2 fragile negative windows
```

The comparison shot also has a higher route-fragmentation median:

```text
shot 12063 F_route_fragmentation median: 0.516301
shot 11830 F_route_fragmentation median: 0.694692
```

and higher power-balance pressure:

```text
shot 12063 S_power_balance median: 0.569205
shot 11830 S_power_balance median: 0.710196
```

This is consistent with the UNNS-H Mode interpretation that the stronger edge corridor is not simply a high-power state. A structurally favorable corridor is one where edge capacity can exceed route fragmentation.

---

## 8. Why this matters

Before this comparison, shot `12063` had passed only internal tests:

```text
metadata availability
array-level extraction
first m_edge(t) computation
trace-level interpretability
```

After this comparison, shot `12063` has passed a first cross-shot specificity test.

The v0.1 margin does not label the weaker candidate in the same way. Shot `11830` still produces some positive windows, but its global and inspected behavior are weaker:

```text
lower positive fraction
higher negative fraction
negative median m_edge
fewer interpretable positive windows
more fragile classifications
```

Therefore, v0.1 is not obviously overbroad at this first comparison stage.

---

## 9. What this establishes

This comparison establishes five things.

### 9.1 Cross-shot discrimination exists

The v0.1 `m_edge(t)` pipeline distinguishes shot `12063` from shot `11830`.

### 9.2 Shot 12063 is structurally stronger

The reference shot has a stronger positive-margin profile, more interpretable positive windows, and a higher peak margin.

### 9.3 Shot 11830 is a useful weaker control

The comparison shot is not empty or unusable. It contains core and Thomson coverage, but lacks soft-X support, making it a meaningful first weaker candidate.

### 9.4 The result is not simply missingness

Both shots have the same median missingness pressure:

```text
shot 12063 missingness median: 0.222222
shot 11830 missingness median: 0.222222
```

The comparison result therefore reflects different structural behavior, not just different missingness.

### 9.5 v0.1 can proceed to a broader comparison

The formula should not be revised immediately. It should be tested on additional shots.

---

## 10. What this does not establish

This comparison still does not prove that shot `12063` is physically H-mode.

It does not identify the L-H transition time.

It does not prove that the detected positive windows are actual L-H transition intervals.

It does not validate the positive corridor physically.

It does not establish cross-machine generality.

It does not prove that the v0.1 formula is final.

The correct bounded claim is:

> The v0.1 normalized `m_edge(t)` pipeline distinguishes shot `12063` from a weaker comparison candidate and supports `12063` as structurally stronger under this first cross-shot test.

not:

> H-mode has been validated.

---

## 11. Decision

The decision after this comparison is:

```text
Do not revise v0.1 yet.
Do not claim physical validation yet.
Proceed to a small multi-shot comparison.
```

The reason is:

```text
v0.1 passed internal trace inspection
v0.1 passed first cross-shot specificity check
the next falsification step is a small comparison panel
```

A single comparison is useful but not sufficient. The next step should test whether the same pattern holds across several candidates.

---

## 12. Recommended next technical step

The next technical step should be a small TokaMark comparison panel:

```text
reference:
  12063

weaker / comparison candidates:
  11830
  one additional PROFILE_DALPHA_CANDIDATE
  one CORE_DALPHA_GEOMETRY_CANDIDATE
  one LOW_PRIORITY or PARTIAL_DALPHA candidate if array-readable
```

The goal is to determine whether `12063` remains structurally stronger across several controls.

The next component should be:

```text
components/
  tokamark_small_panel_runner.py
```

Its job should be to automate:

```text
one-shot array probe
m_edge(t) probe
trace inspection
cross-shot summary table
```

for a small list of shot IDs.

---

## 13. Recommended next document

After the small panel is run, produce:

```text
docs/
  22_TOKAMARK_SMALL_PANEL_M_EDGE_COMPARISON.md
```

That document should answer:

> Does shot `12063` remain structurally stronger against multiple weaker TokaMark candidates?

---

## 14. Project status update

```text
TCV event-level model:                         complete
TCV full-corpus extension:                     complete
TCV time-resolved positive trace:              missing in TCV
TokaMark metadata access:                      complete
TokaMark candidate scan:                       complete
TokaMark shot 12063 array extraction:          complete
TokaMark shot 12063 first m_edge(t):           complete
TokaMark shot 12063 trace inspection:          complete
TokaMark cross-shot comparison 12063 vs 11830: complete
first cross-shot specificity test:             passed
physical positive-corridor validation:         not yet
small multi-shot comparison:                   next
```

---

## 15. Final synthesis statement

The first TokaMark cross-shot `m_edge(t)` comparison supports shot `12063` as structurally stronger than shot `11830`.

Under the same v0.1 normalized pipeline, shot `12063` has a higher positive-boundary fraction, fewer negative-leakage points, a positive median margin, a higher peak margin, and more interpretable positive windows. Shot `11830`, while still diagnostically usable, shows a weaker margin profile, higher route-fragmentation pressure, higher power-balance pressure, and fewer interpretable positive windows.

This result does not validate H-mode physically. It does, however, show that the v0.1 `m_edge(t)` probe is not simply assigning the same positive structure to every usable TokaMark shot. The next decisive step is a small multi-shot panel comparison.
