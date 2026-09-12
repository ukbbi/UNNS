# TokaMark Small-Panel m_edge(t) Comparison

## 1. Purpose

This document records the first small multi-shot panel comparison of the normalized UNNS-H Mode `m_edge(t)` probe on public MAST/TokaMark data.

It belongs here:

```text
unns_hmode_project/
  docs/
    22_TOKAMARK_SMALL_PANEL_M_EDGE_COMPARISON.md
```

It follows:

```text
docs/
  21_TOKAMARK_CROSS_SHOT_M_EDGE_COMPARISON.md
```

The previous document compared reference shot `12063` against one weaker TokaMark candidate, shot `11830`, and found the reference structurally stronger. This document extends the comparison to a five-shot panel:

```text
12063  FULL_PROFILE_EDGE_CANDIDATE        reference
11830  PROFILE_DALPHA_CANDIDATE          profile/no-softX comparison
11876  CORE_DALPHA_GEOMETRY_CANDIDATE    core+softX/no-Thomson comparison
11768  PARTIAL_DALPHA_CANDIDATE          partial comparison
11776  LOW_PRIORITY                      weak / stress-test comparison
```

The central question is:

> Does shot `12063` remain structurally stronger across several weaker public TokaMark candidates?

The answer is yes, but not uniquely enough to claim physical validation.

---

## 2. Panel decision

The panel runner returned:

```text
decision: reference_structurally_strong_but_not_unique
reference shot: 12063
panel size: 5
reference panel rank: 1
```

Decision reasons:

```text
- reference_has_top_panel_structural_score
- reference_has_highest_or_tied_interpretable_positive_count
- reference_result_not_explained_by_lower_missingness
```

The correct interpretation is:

> Shot `12063` remains the top-ranked shot in the five-shot panel, but the result is not unique enough to treat `12063` as physically validated. The panel strengthens the structural case while also exposing a v0.1 weakness around incomplete diagnostics.

---

## 3. Pipeline parity

Each shot was processed through the same pipeline:

```text
1. one-shot array probe
2. normalized m_edge(t) probe
3. trace-level inspection
4. panel aggregation and structural ranking
```

The runner used:

```text
components/
  tokamark_small_panel_runner.py
```

The panel output files were:

```text
outputs/reports/
  tokamark_small_panel_m_edge_comparison.csv
  tokamark_small_panel_m_edge_comparison.json
  tokamark_small_panel_m_edge_comparison.md
  tokamark_small_panel_runner.log
```

---

## 4. Panel ranking

```text
rank 1: shot 12063 | score 20.8439 | interpretable+ 8 | class FULL_PROFILE_EDGE_CANDIDATE
rank 2: shot 11876 | score 13.1648 | interpretable+ 5 | class CORE_DALPHA_GEOMETRY_CANDIDATE
rank 3: shot 11776 | score 9.91819 | interpretable+ 4 | class LOW_PRIORITY
rank 4: shot 11768 | score 4.33617 | interpretable+ 2 | class PARTIAL_DALPHA_CANDIDATE
rank 5: shot 11830 | score 1.78583 | interpretable+ 2 | class PROFILE_DALPHA_CANDIDATE
```

Shot `12063` ranked first:

```text
shot: 12063
rank: 1
panel structural score: 20.8439
interpretable positive windows: 8
candidate class: FULL_PROFILE_EDGE_CANDIDATE
```

The closest comparison was `11876`:

```text
shot: 11876
rank: 2
panel structural score: 13.1648
interpretable positive windows: 5
interpretable negative windows: 7
candidate class: CORE_DALPHA_GEOMETRY_CANDIDATE
```

---

## 5. Core panel summary

|   panel_rank | panel_role   |   shot_id | candidate_class                |   candidate_score |   panel_structural_score |   positive_boundary_margin_fraction |   negative_leakage_margin_fraction |   boundary_ambiguous_margin_fraction |   insufficient_data_fraction |   m_edge_median |   m_edge_mean |   m_edge_min |   m_edge_max |   interpretable_positive_count |   interpretable_negative_count |   fragile_positive_count |   fragile_negative_count |   missingness_pressure_median |
|-------------:|:-------------|----------:|:-------------------------------|------------------:|-------------------------:|------------------------------------:|-----------------------------------:|-------------------------------------:|-----------------------------:|----------------:|--------------:|-------------:|-------------:|-------------------------------:|-------------------------------:|-------------------------:|-------------------------:|------------------------------:|
|            1 | reference    |     12063 | FULL_PROFILE_EDGE_CANDIDATE    |            97.143 |                 20.8439  |                            0.258216 |                           0.112676 |                            0.49061   |                     0.138498 |       0.087961  |     0.055111  |    -0.770609 |     0.475695 |                              8 |                              3 |                        0 |                        0 |                      0.222222 |
|            2 | comparison   |     11876 | CORE_DALPHA_GEOMETRY_CANDIDATE |            72.143 |                 13.1648  |                            0.216015 |                           0.165736 |                            0.504655  |                     0.113594 |       0.0156955 |     0.0236812 |    -0.590862 |     0.568895 |                              5 |                              7 |                        0 |                        0 |                      0.222222 |
|            3 | comparison   |     11776 | LOW_PRIORITY                   |            58.929 |                  9.91819 |                            0.659656 |                           0.156788 |                            0.0707457 |                     0.112811 |       0.486177  |     0.249023  |    -0.939394 |     0.727017 |                              4 |                              0 |                        0 |                        3 |                      0.444444 |
|            4 | comparison   |     11768 | PARTIAL_DALPHA_CANDIDATE       |            65.179 |                  4.33617 |                            0.533654 |                           0.230769 |                            0.0961538 |                     0.139423 |       0.372648  |     0.143849  |    -0.848659 |     0.622713 |                              2 |                              0 |                        0 |                        3 |                      0.333333 |
|            5 | comparison   |     11830 | PROFILE_DALPHA_CANDIDATE       |            81.429 |                  1.78583 |                            0.226064 |                           0.228723 |                            0.390957  |                     0.154255 |      -0.0366668 |     0.0050537 |    -0.745802 |     0.387901 |                              2 |                              0 |                        2 |                        2 |                      0.222222 |

---

## 6. Diagnostic metadata roles

|   shot_id | candidate_class                |   core_required_present |   profile_preferred_present |   edge_activity_present |   supporting_present | missing_core_required                                                     | missing_profile_preferred                     | missing_edge_activity                                             |   loaded_signal_arrays |   failed_signal_arrays |
|----------:|:-------------------------------|------------------------:|----------------------------:|------------------------:|---------------------:|:--------------------------------------------------------------------------|:----------------------------------------------|:------------------------------------------------------------------|-----------------------:|-----------------------:|
|     11768 | PARTIAL_DALPHA_CANDIDATE       |                       7 |                           0 |                       2 |                    9 | summary-power_nbi                                                         | thomson_scattering-t_e;thomson_scattering-n_e | nan                                                               |                     13 |                      3 |
|     11776 | LOW_PRIORITY                   |                       6 |                           0 |                       2 |                    9 | summary-power_nbi;spectrometer_visible-filter_spectrometer_dalpha_voltage | thomson_scattering-t_e;thomson_scattering-n_e | nan                                                               |                     12 |                      4 |
|     11830 | PROFILE_DALPHA_CANDIDATE       |                       8 |                           2 |                       0 |                    9 | nan                                                                       | nan                                           | soft_x_rays-horizontal_cam_lower;soft_x_rays-horizontal_cam_upper |                     14 |                      2 |
|     11876 | CORE_DALPHA_GEOMETRY_CANDIDATE |                       8 |                           0 |                       2 |                   10 | nan                                                                       | thomson_scattering-t_e;thomson_scattering-n_e | nan                                                               |                     14 |                      2 |
|     12063 | FULL_PROFILE_EDGE_CANDIDATE    |                       8 |                           2 |                       2 |                   10 | nan                                                                       | nan                                           | nan                                                               |                     16 |                      0 |

This table is crucial because the panel mixes diagnostically complete and incomplete shots. The interpretation must distinguish genuine structural behavior from missing-diagnostic artifacts.

---

## 7. Main finding: shot 12063 remains strongest

Shot `12063` remains strongest by the panel scoring rule:

```text
panel rank: 1
panel structural score: 20.8439
positive boundary fraction: 0.258216
negative leakage fraction: 0.112676
m_edge median: 0.087961
m_edge max: 0.475695
interpretable positive windows: 8
interpretable negative windows: 3
missingness median: 0.222222
```

It has the strongest combination of complete diagnostic family, positive median `m_edge`, high interpretable-positive count, nonzero interpretable-negative internal contrast, low/moderate missingness, and top panel structural score.

---

## 8. Closest control: shot 11876

Shot `11876` is the closest meaningful structural comparison:

```text
candidate class: CORE_DALPHA_GEOMETRY_CANDIDATE
panel rank: 2
panel structural score: 13.1648
positive boundary fraction: 0.216015
negative leakage fraction: 0.165736
m_edge median: 0.0156955
m_edge max: 0.568895
interpretable positive windows: 5
interpretable negative windows: 7
missingness median: 0.222222
```

Shot `11876` has core and soft-X support but lacks Thomson profiles:

```text
missing_profile_preferred:
  thomson_scattering-t_e;thomson_scattering-n_e
```

It remains structurally active and produces five interpretable positive windows, but it also produces seven interpretable negative windows and has no transport coverage:

```text
S_transport finite fraction: 0
```

Therefore, `11876` is a useful comparison showing that the v0.1 margin responds to edge activity even when profile/transport information is missing.

---

## 9. Warning case: shot 11776

Shot `11776` exposes the main v0.1 weakness.

It is a `LOW_PRIORITY` shot, yet it shows:

```text
positive boundary fraction: 0.659656
m_edge median: 0.486177
m_edge max: 0.727017
interpretable positive windows: 4
missingness median: 0.444444
```

But diagnostically it is incomplete:

```text
missing_core_required:
  summary-power_nbi;spectrometer_visible-filter_spectrometer_dalpha_voltage

missing_profile_preferred:
  thomson_scattering-t_e;thomson_scattering-n_e

failed signal arrays:
  4
```

This means v0.1 can over-reward incomplete shots when missing diagnostics reduce fragmentation terms or leave capacity terms artificially dominant. The runner still ranks `11776` below `12063`, but its high positive fraction is a warning sign, not positive evidence.

---

## 10. Shot 11768: partial candidate

Shot `11768` also has inflated positive fraction but incomplete diagnostics:

```text
candidate class: PARTIAL_DALPHA_CANDIDATE
positive boundary fraction: 0.533654
negative leakage fraction: 0.230769
m_edge median: 0.372648
interpretable positive windows: 2
fragile negative windows: 3
missingness median: 0.333333
```

It is missing NBI power and Thomson profiles:

```text
missing_core_required:
  summary-power_nbi

missing_profile_preferred:
  thomson_scattering-t_e;thomson_scattering-n_e
```

This reinforces the same caution: high positive fraction alone is not enough. It must be weighted by diagnostic completeness and trace interpretability.

---

## 11. Shot 11830: profile/no-softX control

Shot `11830`, already used in the two-shot comparison, remains weakest by panel structural score:

```text
candidate class: PROFILE_DALPHA_CANDIDATE
panel rank: 5
panel structural score: 1.78583
positive boundary fraction: 0.226064
negative leakage fraction: 0.228723
m_edge median: -0.0366668
interpretable positive windows: 2
fragile positive windows: 2
fragile negative windows: 2
```

It has core and Thomson profiles but lacks soft-X edge activity:

```text
missing_edge_activity:
  soft_x_rays-horizontal_cam_lower;soft_x_rays-horizontal_cam_upper
```

This remains a useful control because it shows that profile availability alone is not enough to reproduce the stronger `12063` pattern.

---

## 12. What the panel establishes

This panel establishes six things.

### 12.1 Shot 12063 remains top-ranked

The reference shot has the highest panel structural score.

### 12.2 Shot 12063 has the strongest interpretable-positive count

It has eight interpretable positive windows, more than any comparison shot in this panel.

### 12.3 The result is not explained by lower missingness

`12063` and `11876` have the same median missingness, while `12063` still ranks higher. The decision explicitly records that the reference result is not explained by lower missingness.

### 12.4 Incomplete shots can inflate positive fractions

Shots `11776` and `11768` show high positive fractions despite missing critical diagnostics. This exposes a limitation of v0.1.

### 12.5 Interpretability is more reliable than positive fraction alone

The ranking depends not only on positive-boundary fraction but also on interpretable-window counts, fragile classifications, missingness, and structural score.

### 12.6 v0.1 should be refined, not discarded

The formula distinguishes `12063`, but it needs a diagnostic confidence modifier before broader use.

---

## 13. What this does not establish

This panel still does not prove that `12063` is physically H-mode.

It does not identify the L-H transition time.

It does not prove that the positive windows are actual L-H transition intervals.

It does not validate the positive corridor physically.

It does not establish cross-machine generality.

It does not prove that v0.1 is final.

The bounded claim is:

> Shot `12063` remains the strongest case in the first five-shot TokaMark panel under the v0.1 normalized `m_edge(t)` pipeline, but the panel reveals that v0.1 can over-reward incomplete diagnostic cases.

---

## 14. Decision

The correct decision after this panel is:

```text
Do not claim physical validation.
Do not discard v0.1.
Do revise v0.1 before broad panel scaling.
```

Specifically, the next formula revision should add:

```text
diagnostic completeness confidence
transport coverage confidence
soft-X / D-alpha edge-response confidence
missing-critical-signal penalties
separate structural margin from confidence-weighted margin
```

The distinction should be:

```text
m_edge_raw(t)
  raw structural margin

Q_diag(t)
  diagnostic confidence / coverage quality

m_edge_conf(t)
  confidence-weighted margin
```

This would prevent LOW_PRIORITY shots like `11776` from looking artificially strong simply because missing diagnostics reduce fragmentation pressure.

---

## 15. Recommended next technical component

The next component should be:

```text
components/
  tokamark_m_edge_confidence_revision.py
```

Its job should be to compute:

```text
Q_diag(t)
m_edge_conf(t) = m_edge_raw(t) · Q_diag(t)
```

or a more conservative form:

```text
m_edge_conf(t) = C_edge_capacity(t) · Q_capacity(t)
                 - F_route_fragmentation(t) · Q_fragmentation(t)
                 - P_missing_critical(t)
```

At minimum, it should penalize:

```text
missing NBI power
missing D-alpha
missing Thomson Te/ne
missing soft-X
missing transport term
high missingness_pressure
```

It should preserve the raw `m_edge(t)` column while adding confidence-adjusted columns.

---

## 16. Recommended next document

After the confidence revision is run, produce:

```text
docs/
  23_TOKAMARK_M_EDGE_CONFIDENCE_REVISION.md
```

That document should answer:

> Does the diagnostic-confidence revision preserve shot `12063` while suppressing inflated incomplete cases such as `11776` and `11768`?

---

## 17. Pipeline stage status

|   shot_id | stage                | status           |   return_code |
|----------:|:---------------------|:-----------------|--------------:|
|     12063 | one_shot_array_probe | skipped_existing |             0 |
|     12063 | m_edge_t_probe       | skipped_existing |             0 |
|     12063 | trace_inspection     | skipped_existing |             0 |
|     11830 | one_shot_array_probe | skipped_existing |             0 |
|     11830 | m_edge_t_probe       | skipped_existing |             0 |
|     11830 | trace_inspection     | skipped_existing |             0 |
|     11876 | one_shot_array_probe | ok               |             0 |
|     11876 | m_edge_t_probe       | ok               |             0 |
|     11876 | trace_inspection     | ok               |             0 |
|     11768 | one_shot_array_probe | ok               |             0 |
|     11768 | m_edge_t_probe       | ok               |             0 |
|     11768 | trace_inspection     | ok               |             0 |
|     11776 | one_shot_array_probe | ok               |             0 |
|     11776 | m_edge_t_probe       | ok               |             0 |
|     11776 | trace_inspection     | ok               |             0 |

---

## 18. Project status update

```text
TCV event-level model:                      complete
TCV full-corpus extension:                  complete
TCV time-resolved positive trace:           missing in TCV
TokaMark metadata access:                   complete
TokaMark candidate scan:                    complete
TokaMark shot 12063 array extraction:       complete
TokaMark shot 12063 first m_edge(t):        complete
TokaMark shot 12063 trace inspection:       complete
TokaMark cross-shot comparison:             complete
TokaMark five-shot panel comparison:        complete
v0.1 discrimination:                        supported
v0.1 uniqueness:                            not established
v0.1 confidence handling:                   needs revision
physical positive-corridor validation:      not yet
```

---

## 19. Final synthesis statement

The five-shot TokaMark panel strengthens the structural case for shot `12063`, but it also clarifies the next methodological problem.

Shot `12063` remains the top-ranked panel member and has the strongest interpretable-positive count. It is not simply advantaged by lower missingness. This supports the v0.1 margin as a discriminative structural probe.

However, the panel also shows that incomplete shots such as `11776` and `11768` can produce inflated positive-boundary fractions and high positive medians despite missing critical diagnostics. Therefore, v0.1 should not be scaled further without a diagnostic-confidence correction.

The correct next step is not physical validation and not a larger blind scan. The correct next step is to revise the margin with explicit diagnostic confidence: preserve the raw `m_edge(t)`, compute `Q_diag(t)`, and compare confidence-weighted margins across the same panel.
