# TokaMark Moderate Confidence Panel Results

## 1. Purpose

This document reports the moderate controlled TokaMark panel run for the v0.2 diagnostic-confidence UNNS-H Mode pipeline.

It belongs here:

```text
unns_hmode_project/
  docs/
    27_TOKAMARK_MODERATE_CONFIDENCE_PANEL_RESULTS.md
```

It follows:

```text
docs/
  26_TOKAMARK_MODERATE_CONFIDENCE_PANEL_PLAN.md
```

The question for this step was:

> Does the v0.2 diagnostic-confidence correction remain stable and meaningful on a controlled 30-shot TokaMark panel?

The answer is yes, with an important methodological caveat: this is still not physical H-mode validation. It is a stability and class-behavior test of the confidence-corrected structural margin.

---

## 2. Inputs

The moderate panel was selected from:

```text
outputs/reports/
  tokamark_moderate_confidence_panel_selection.csv
```

The panel contained 30 shots:

```text
12046
11941
12055
12007
12017
11823
12069
12063
11946
12076
11996
11802
11830
11780
12034
11772
11876
11768
11851
11908
11958
11795
12079
12081
12082
12087
12091
11789
12027
11776
```

The run used the existing v0.2 pipeline:

```text
components/
  tokamark_one_shot_array_probe.py
  tokamark_m_edge_t_probe.py
  tokamark_m_edge_trace_inspector.py
  tokamark_m_edge_confidence_revision.py
  tokamark_moderate_confidence_panel_runner.py
```

Generated outputs:

```text
outputs/reports/
  tokamark_moderate_confidence_panel_results.csv
  tokamark_moderate_confidence_panel_results.json
  tokamark_moderate_confidence_panel_results.md
  tokamark_moderate_confidence_panel_runner.log
```

---

## 3. Decision

The moderate panel returned:

```text
decision: moderate_confidence_panel_passes_initial_stability_test
selected total: 30
processed ok: 30
confidence-positive case count: 10
```

Reasons:

```text
- FULL_PROFILE_EDGE_CANDIDATE shots are enriched among top-ranked cases.
- LOW_PRIORITY shots are absent from top-ranked cases.
- LOW_PRIORITY shots have zero confidence-positive fraction.
- PARTIAL_DALPHA_CANDIDATE shots are mostly suppressed.
- Confidence-positive cases have moderate/high median Q_diag.
- Critical-missing penalties are higher in LOW_PRIORITY cases than in FULL_PROFILE_EDGE_CANDIDATE cases.
```

Warnings:

```text
- None.
```

This is the strongest methodological result so far: all selected shots processed successfully, full-profile-edge candidates dominate the top-ranked cases, and incomplete / weak classes are suppressed.

---

## 4. Stage completion

| stage                     |   total |   ok |   failed |   missing_after_skip |
|:--------------------------|--------:|-----:|---------:|---------------------:|
| confidence_revision_panel |       1 |    1 |        0 |                    0 |
| m_edge_t_probe            |      30 |   30 |        0 |                    0 |
| one_shot_array_probe      |      30 |   30 |        0 |                    0 |
| trace_inspection          |      30 |   30 |        0 |                    0 |

All four stages completed for the panel: array probing, raw `m_edge(t)` probing, trace inspection, and confidence revision.

---

## 5. Confidence-adjusted ranking

|   confidence_panel_rank |   selection_order |   shot_id | candidate_class                |   confidence_structural_score |   raw_positive_fraction |   conf_positive_fraction |   raw_negative_fraction |   conf_negative_fraction |   conf_low_confidence_fraction |   m_edge_raw_median |   m_edge_conf_median |   Q_diag_median |   P_missing_critical_median | selection_role                                |
|------------------------:|------------------:|----------:|:-------------------------------|------------------------------:|------------------------:|-------------------------:|------------------------:|-------------------------:|-------------------------------:|--------------------:|---------------------:|----------------:|----------------------------:|:----------------------------------------------|
|                       1 |                14 |     12046 | FULL_PROFILE_EDGE_CANDIDATE    |                      8.33592  |              0.40133    |                0.40133   |               0.150776  |                 0.203991 |                      0.13082   |          0.175811   |            0.0995503 |        1        |                   0         | class_balanced_FULL_PROFILE_EDGE_CANDIDATE    |
|                       2 |                 9 |     11941 | FULL_PROFILE_EDGE_CANDIDATE    |                      8.11244  |              0.401152   |                0.37428   |               0         |                 0.184261 |                      0.0959693 |          0.180108   |            0.0785146 |        1        |                   0         | class_balanced_FULL_PROFILE_EDGE_CANDIDATE    |
|                       3 |                15 |     12055 | FULL_PROFILE_EDGE_CANDIDATE    |                      7.90659  |              0.451613   |                0.442815  |               0.0821114 |                 0.290323 |                      0.120235  |          0.206909   |            0.119147  |        1        |                   0         | shortage_filler                               |
|                       4 |                12 |     12007 | FULL_PROFILE_EDGE_CANDIDATE    |                      7.28316  |              0.383408   |                0.378924  |               0.103139  |                 0.221973 |                      0.134529  |          0.146025   |            0.0268082 |        1        |                   0         | class_balanced_FULL_PROFILE_EDGE_CANDIDATE    |
|                       5 |                13 |     12017 | FULL_PROFILE_EDGE_CANDIDATE    |                      6.22806  |              0.294872   |                0.294872  |               0.0989011 |                 0.190476 |                      0.10989   |          0.0956259  |            0.0446953 |        1        |                   0         | shortage_filler                               |
|                       6 |                 8 |     11823 | FULL_PROFILE_EDGE_CANDIDATE    |                      5.96579  |              0.298319   |                0.292017  |               0.121849  |                 0.214286 |                      0.121849  |          0.140869   |            0.116046  |        1        |                   0         | shortage_filler                               |
|                       7 |                 6 |     12069 | FULL_PROFILE_EDGE_CANDIDATE    |                      5.40928  |              0.449405   |                0.28869   |               0.130952  |                 0.247024 |                      0.0565476 |          0.189151   |            0.0750786 |        0.888889 |                   0.0111111 | class_balanced_FULL_PROFILE_EDGE_CANDIDATE    |
|                       8 |                 1 |     12063 | FULL_PROFILE_EDGE_CANDIDATE    |                      2.11139  |              0.258216   |                0.169014  |               0.112676  |                 0.215962 |                      0.138498  |          0.087961   |           -0.0217341 |        0.888889 |                   0.0111111 | reference_anchor                              |
|                       9 |                10 |     11946 | FULL_PROFILE_EDGE_CANDIDATE    |                      1.67207  |              0.115385   |                0.0897436 |               0         |                 0.203297 |                      0.0915751 |          0.0453373  |           -0.0275021 |        1        |                   0         | shortage_filler                               |
|                      10 |                 7 |     12076 | FULL_PROFILE_EDGE_CANDIDATE    |                     -0.426056 |              0.19407    |                0.102426  |               0.134771  |                 0.283019 |                      0.161725  |          0.0795471  |           -0.10362   |        0.888889 |                   0.0111111 | class_balanced_FULL_PROFILE_EDGE_CANDIDATE    |
|                      11 |                11 |     11996 | FULL_PROFILE_EDGE_CANDIDATE    |                     -4.38658  |              0.240296   |                0         |               0.0480591 |                 0.343808 |                      0.0868762 |          0.0328101  |           -0.116975  |        0.738889 |                   0.411111  | shortage_filler                               |
|                      12 |                17 |     11802 | CORE_DALPHA_GEOMETRY_CANDIDATE |                     -4.51466  |              0.477823   |                0         |               0.0705645 |                 0.332661 |                      0.116935  |          0.227214   |           -0.156324  |        0.738889 |                   0.411111  | class_balanced_CORE_DALPHA_GEOMETRY_CANDIDATE |
|                      13 |                 2 |     11830 | PROFILE_DALPHA_CANDIDATE       |                     -6.4816   |              0.226064   |                0         |               0.228723  |                 0.510638 |                      0.154255  |         -0.0366668  |           -0.322615  |        0.863889 |                   0.111111  | profile_no_softx_anchor                       |
|                      14 |                22 |     11780 | PARTIAL_DALPHA_CANDIDATE       |                     -6.6878   |              0.496994   |                0         |               0.202405  |                 0.40481  |                      0.116232  |          0.308622   |           -0.237795  |        0.593333 |                   0.616667  | class_balanced_PARTIAL_DALPHA_CANDIDATE       |
|                      15 |                16 |     12034 | CORE_DALPHA_GEOMETRY_CANDIDATE |                     -6.86402  |              0.375828   |                0         |               0.0678808 |                 0.511589 |                      0.0811258 |          0.110632   |           -0.243411  |        0.738889 |                   0.411111  | class_balanced_CORE_DALPHA_GEOMETRY_CANDIDATE |
|                      16 |                21 |     11772 | PARTIAL_DALPHA_CANDIDATE       |                     -7.35521  |              0.65762    |                0         |               0.187891  |                 0.444676 |                      0.123173  |          0.366728   |           -0.212731  |        0.593333 |                   0.616667  | class_balanced_PARTIAL_DALPHA_CANDIDATE       |
|                      17 |                 3 |     11876 | CORE_DALPHA_GEOMETRY_CANDIDATE |                     -7.80769  |              0.216015   |                0         |               0.165736  |                 0.55121  |                      0.113594  |          0.0156955  |           -0.27706   |        0.738889 |                   0.411111  | core_dalpha_geometry_anchor                   |
|                      18 |                 4 |     11768 | PARTIAL_DALPHA_CANDIDATE       |                     -8.0591   |              0.533654   |                0         |               0.230769  |                 0.480769 |                      0.139423  |          0.372648   |           -0.255289  |        0.593333 |                   0.616667  | partial_dalpha_anchor                         |
|                      19 |                18 |     11851 | CORE_DALPHA_GEOMETRY_CANDIDATE |                     -8.39218  |              0.156627   |                0         |               0.284337  |                 0.578313 |                      0.142169  |         -0.0470812  |           -0.374273  |        0.738889 |                   0.411111  | class_balanced_CORE_DALPHA_GEOMETRY_CANDIDATE |
|                      20 |                19 |     11908 | CORE_DALPHA_GEOMETRY_CANDIDATE |                     -9.6035   |              0.239051   |                0         |               0.242701  |                 0.687956 |                      0.0930657 |         -0.00489147 |           -0.332723  |        0.738889 |                   0.411111  | class_balanced_CORE_DALPHA_GEOMETRY_CANDIDATE |
|                      21 |                20 |     11958 | CORE_DALPHA_GEOMETRY_CANDIDATE |                    -10.0735   |              0.227373   |                0         |               0.251656  |                 0.690949 |                      0.110375  |         -0.161786   |           -0.34341   |        0.738889 |                   0.411111  | class_balanced_CORE_DALPHA_GEOMETRY_CANDIDATE |
|                      22 |                24 |     11795 | PARTIAL_DALPHA_CANDIDATE       |                    -11.1403   |              0.284274   |                0         |               0.108871  |                 0.729839 |                      0.116935  |          0.091558   |           -0.353615  |        0.583333 |                   0.416667  | class_balanced_PARTIAL_DALPHA_CANDIDATE       |
|                      23 |                26 |     12079 | LOW_PRIORITY                   |                    -11.3694   |              0.0341207  |                0         |               0.682415  |                 0        |                      1         |         -0.659619   |           -0.902052  |        0.136111 |                   0.888889  | class_balanced_LOW_PRIORITY                   |
|                      23 |                27 |     12081 | LOW_PRIORITY                   |                    -11.3694   |              0.0205128  |                0         |               0.64359   |                 0        |                      1         |         -0.544359   |           -0.883667  |        0.136111 |                   0.888889  | class_balanced_LOW_PRIORITY                   |
|                      23 |                28 |     12082 | LOW_PRIORITY                   |                    -11.3694   |              0          |                0         |               0.551181  |                 0        |                      1         |         -0.376565   |           -0.885771  |        0.136111 |                   0.888889  | class_balanced_LOW_PRIORITY                   |
|                      23 |                29 |     12087 | LOW_PRIORITY                   |                    -11.3694   |              0          |                0         |               0.585302  |                 0        |                      1         |         -0.372758   |           -0.879284  |        0.136111 |                   0.888889  | class_balanced_LOW_PRIORITY                   |
|                      23 |                30 |     12091 | LOW_PRIORITY                   |                    -11.3694   |              0.00234742 |                0         |               0.669014  |                 0        |                      1         |         -0.411033   |           -0.865613  |        0.136111 |                   0.888889  | class_balanced_LOW_PRIORITY                   |
|                      28 |                23 |     11789 | PARTIAL_DALPHA_CANDIDATE       |                    -11.7973   |              0.294466   |                0         |               0.104743  |                 0.770751 |                      0.116601  |          0.128838   |           -0.376818  |        0.583333 |                   0.416667  | class_balanced_PARTIAL_DALPHA_CANDIDATE       |
|                      29 |                25 |     12027 | PARTIAL_DALPHA_CANDIDATE       |                    -13.565    |              0.276458   |                0         |               0.524838  |                 0.896328 |                      0.103672  |         -0.284308   |           -0.543243  |        0.583333 |                   0.416667  | class_balanced_PARTIAL_DALPHA_CANDIDATE       |
|                      30 |                 5 |     11776 | LOW_PRIORITY                   |                    -13.6066   |              0.659656   |                0         |               0.156788  |                 0.650096 |                      0.349904  |          0.486177   |           -0.48441   |        0.462778 |                   0.872222  | low_priority_anchor                           |

The top-ranked cases are all `FULL_PROFILE_EDGE_CANDIDATE` shots. The reference shot `12063` remains interpretable and confidence-positive, but it is no longer rank 1. It ranks:

```text
shot: 12063
confidence rank: 8
confidence structural score: 2.11139
raw positive fraction: 0.258216
confidence-positive fraction: 0.169014
Q_diag median: 0.888889
P_missing_critical median: 0.0111111
```

This is not a failure. It shows that `12063` was not a single cherry-picked anomaly. The method found a broader full-diagnostic class behavior.

---

## 6. Class-level summary

| candidate_class                |   count |   confidence_structural_score_median |   conf_positive_fraction_median |   conf_negative_fraction_median |   conf_low_confidence_fraction_median |   Q_diag_median_median |   P_missing_critical_median_median |   fraction_with_conf_positive_gt_0 |   fraction_with_low_conf_gt_0_25 |
|:-------------------------------|--------:|-------------------------------------:|--------------------------------:|--------------------------------:|--------------------------------------:|-----------------------:|-----------------------------------:|-----------------------------------:|---------------------------------:|
| CORE_DALPHA_GEOMETRY_CANDIDATE |       6 |                             -8.09994 |                        0        |                        0.564762 |                              0.111985 |               0.738889 |                           0.411111 |                           0        |                                0 |
| FULL_PROFILE_EDGE_CANDIDATE    |      11 |                              5.96579 |                        0.292017 |                        0.215962 |                              0.120235 |               1        |                           0        |                           0.909091 |                                0 |
| LOW_PRIORITY                   |       6 |                            -11.3694  |                        0        |                        0        |                              1        |               0.136111 |                           0.888889 |                           0        |                                1 |
| PARTIAL_DALPHA_CANDIDATE       |       6 |                             -9.59968 |                        0        |                        0.605304 |                              0.116768 |               0.588333 |                           0.516667 |                           0        |                                0 |
| PROFILE_DALPHA_CANDIDATE       |       1 |                             -6.4816  |                        0        |                        0.510638 |                              0.154255 |               0.863889 |                           0.111111 |                           0        |                                0 |

The class-level pattern is the key result.

### FULL_PROFILE_EDGE_CANDIDATE

```text
count: 11
median confidence-positive fraction: 0.292017
fraction with confidence-positive > 0: 0.909091
median Q_diag: 1
median critical-missing penalty: 0
```

This class is enriched among the top-ranked cases and is the only class with broad confidence-positive behavior.

### LOW_PRIORITY

```text
count: 6
median confidence-positive fraction: 0
fraction with confidence-positive > 0: 0
median low-confidence fraction: 1
median Q_diag: 0.136111
median critical-missing penalty: 0.888889
```

This class is fully suppressed or confidence-limited, which is exactly what v0.2 was designed to do.

### PARTIAL_DALPHA_CANDIDATE

```text
count: 6
median raw-positive fraction: 0.39573
median confidence-positive fraction: 0
median Q_diag: 0.588333
median critical-missing penalty: 0.516667
```

The partial class shows the most important correction behavior: raw positive fractions can be high, but confidence-positive fractions collapse to zero when diagnostic incompleteness is accounted for.

---

## 7. Main finding

The v0.2 confidence correction passed the moderate controlled panel.

The most important result is not that a particular shot won. The important result is that the class behavior became methodologically sane:

```text
FULL_PROFILE_EDGE_CANDIDATE:
  enriched in top-ranked cases
  high Q_diag
  low P_missing_critical
  nonzero confidence-positive behavior

LOW_PRIORITY:
  absent from top-ranked cases
  zero confidence-positive behavior
  high low-confidence fraction
  high P_missing_critical

PARTIAL_DALPHA_CANDIDATE:
  raw-positive inflation suppressed
  confidence-positive fraction reduced to zero
```

This means the diagnostic-confidence correction is not merely cosmetic. It changes the interpretation in the intended direction.

---

## 8. Manual review queues

### 8.1 Top 5 confidence-ranked shots

|   confidence_panel_rank |   selection_order |   shot_id | candidate_class             |   confidence_structural_score |   raw_positive_fraction |   conf_positive_fraction |   raw_negative_fraction |   conf_negative_fraction |   conf_low_confidence_fraction |   m_edge_raw_median |   m_edge_conf_median |   Q_diag_median |   P_missing_critical_median | selection_role                             |
|------------------------:|------------------:|----------:|:----------------------------|------------------------------:|------------------------:|-------------------------:|------------------------:|-------------------------:|-------------------------------:|--------------------:|---------------------:|----------------:|----------------------------:|:-------------------------------------------|
|                       1 |                14 |     12046 | FULL_PROFILE_EDGE_CANDIDATE |                       8.33592 |                0.40133  |                 0.40133  |               0.150776  |                 0.203991 |                      0.13082   |           0.175811  |            0.0995503 |               1 |                           0 | class_balanced_FULL_PROFILE_EDGE_CANDIDATE |
|                       2 |                 9 |     11941 | FULL_PROFILE_EDGE_CANDIDATE |                       8.11244 |                0.401152 |                 0.37428  |               0         |                 0.184261 |                      0.0959693 |           0.180108  |            0.0785146 |               1 |                           0 | class_balanced_FULL_PROFILE_EDGE_CANDIDATE |
|                       3 |                15 |     12055 | FULL_PROFILE_EDGE_CANDIDATE |                       7.90659 |                0.451613 |                 0.442815 |               0.0821114 |                 0.290323 |                      0.120235  |           0.206909  |            0.119147  |               1 |                           0 | shortage_filler                            |
|                       4 |                12 |     12007 | FULL_PROFILE_EDGE_CANDIDATE |                       7.28316 |                0.383408 |                 0.378924 |               0.103139  |                 0.221973 |                      0.134529  |           0.146025  |            0.0268082 |               1 |                           0 | class_balanced_FULL_PROFILE_EDGE_CANDIDATE |
|                       5 |                13 |     12017 | FULL_PROFILE_EDGE_CANDIDATE |                       6.22806 |                0.294872 |                 0.294872 |               0.0989011 |                 0.190476 |                      0.10989   |           0.0956259 |            0.0446953 |               1 |                           0 | shortage_filler                            |

### 8.2 Bottom 5 confidence-ranked shots

|   confidence_panel_rank |   selection_order |   shot_id | candidate_class          |   confidence_structural_score |   raw_positive_fraction |   conf_positive_fraction |   raw_negative_fraction |   conf_negative_fraction |   conf_low_confidence_fraction |   m_edge_raw_median |   m_edge_conf_median |   Q_diag_median |   P_missing_critical_median | selection_role                          |
|------------------------:|------------------:|----------:|:-------------------------|------------------------------:|------------------------:|-------------------------:|------------------------:|-------------------------:|-------------------------------:|--------------------:|---------------------:|----------------:|----------------------------:|:----------------------------------------|
|                      23 |                29 |     12087 | LOW_PRIORITY             |                      -11.3694 |              0          |                        0 |                0.585302 |                 0        |                       1        |           -0.372758 |            -0.879284 |        0.136111 |                    0.888889 | class_balanced_LOW_PRIORITY             |
|                      23 |                30 |     12091 | LOW_PRIORITY             |                      -11.3694 |              0.00234742 |                        0 |                0.669014 |                 0        |                       1        |           -0.411033 |            -0.865613 |        0.136111 |                    0.888889 | class_balanced_LOW_PRIORITY             |
|                      28 |                23 |     11789 | PARTIAL_DALPHA_CANDIDATE |                      -11.7973 |              0.294466   |                        0 |                0.104743 |                 0.770751 |                       0.116601 |            0.128838 |            -0.376818 |        0.583333 |                    0.416667 | class_balanced_PARTIAL_DALPHA_CANDIDATE |
|                      29 |                25 |     12027 | PARTIAL_DALPHA_CANDIDATE |                      -13.565  |              0.276458   |                        0 |                0.524838 |                 0.896328 |                       0.103672 |           -0.284308 |            -0.543243 |        0.583333 |                    0.416667 | class_balanced_PARTIAL_DALPHA_CANDIDATE |
|                      30 |                 5 |     11776 | LOW_PRIORITY             |                      -13.6066 |              0.659656   |                        0 |                0.156788 |                 0.650096 |                       0.349904 |            0.486177 |            -0.48441  |        0.462778 |                    0.872222 | low_priority_anchor                     |

### 8.3 Confidence-positive shots

|   confidence_panel_rank |   selection_order |   shot_id | candidate_class             |   confidence_structural_score |   raw_positive_fraction |   conf_positive_fraction |   raw_negative_fraction |   conf_negative_fraction |   conf_low_confidence_fraction |   m_edge_raw_median |   m_edge_conf_median |   Q_diag_median |   P_missing_critical_median | selection_role                             |
|------------------------:|------------------:|----------:|:----------------------------|------------------------------:|------------------------:|-------------------------:|------------------------:|-------------------------:|-------------------------------:|--------------------:|---------------------:|----------------:|----------------------------:|:-------------------------------------------|
|                       1 |                14 |     12046 | FULL_PROFILE_EDGE_CANDIDATE |                      8.33592  |                0.40133  |                0.40133   |               0.150776  |                 0.203991 |                      0.13082   |           0.175811  |            0.0995503 |        1        |                   0         | class_balanced_FULL_PROFILE_EDGE_CANDIDATE |
|                       2 |                 9 |     11941 | FULL_PROFILE_EDGE_CANDIDATE |                      8.11244  |                0.401152 |                0.37428   |               0         |                 0.184261 |                      0.0959693 |           0.180108  |            0.0785146 |        1        |                   0         | class_balanced_FULL_PROFILE_EDGE_CANDIDATE |
|                       3 |                15 |     12055 | FULL_PROFILE_EDGE_CANDIDATE |                      7.90659  |                0.451613 |                0.442815  |               0.0821114 |                 0.290323 |                      0.120235  |           0.206909  |            0.119147  |        1        |                   0         | shortage_filler                            |
|                       4 |                12 |     12007 | FULL_PROFILE_EDGE_CANDIDATE |                      7.28316  |                0.383408 |                0.378924  |               0.103139  |                 0.221973 |                      0.134529  |           0.146025  |            0.0268082 |        1        |                   0         | class_balanced_FULL_PROFILE_EDGE_CANDIDATE |
|                       5 |                13 |     12017 | FULL_PROFILE_EDGE_CANDIDATE |                      6.22806  |                0.294872 |                0.294872  |               0.0989011 |                 0.190476 |                      0.10989   |           0.0956259 |            0.0446953 |        1        |                   0         | shortage_filler                            |
|                       6 |                 8 |     11823 | FULL_PROFILE_EDGE_CANDIDATE |                      5.96579  |                0.298319 |                0.292017  |               0.121849  |                 0.214286 |                      0.121849  |           0.140869  |            0.116046  |        1        |                   0         | shortage_filler                            |
|                       7 |                 6 |     12069 | FULL_PROFILE_EDGE_CANDIDATE |                      5.40928  |                0.449405 |                0.28869   |               0.130952  |                 0.247024 |                      0.0565476 |           0.189151  |            0.0750786 |        0.888889 |                   0.0111111 | class_balanced_FULL_PROFILE_EDGE_CANDIDATE |
|                       8 |                 1 |     12063 | FULL_PROFILE_EDGE_CANDIDATE |                      2.11139  |                0.258216 |                0.169014  |               0.112676  |                 0.215962 |                      0.138498  |           0.087961  |           -0.0217341 |        0.888889 |                   0.0111111 | reference_anchor                           |
|                       9 |                10 |     11946 | FULL_PROFILE_EDGE_CANDIDATE |                      1.67207  |                0.115385 |                0.0897436 |               0         |                 0.203297 |                      0.0915751 |           0.0453373 |           -0.0275021 |        1        |                   0         | shortage_filler                            |
|                      10 |                 7 |     12076 | FULL_PROFILE_EDGE_CANDIDATE |                     -0.426056 |                0.19407  |                0.102426  |               0.134771  |                 0.283019 |                      0.161725  |           0.0795471 |           -0.10362   |        0.888889 |                   0.0111111 | class_balanced_FULL_PROFILE_EDGE_CANDIDATE |

### 8.4 Raw-positive inflated but confidence-suppressed shots

|   confidence_panel_rank |   selection_order |   shot_id | candidate_class          |   confidence_structural_score |   raw_positive_fraction |   conf_positive_fraction |   raw_negative_fraction |   conf_negative_fraction |   conf_low_confidence_fraction |   m_edge_raw_median |   m_edge_conf_median |   Q_diag_median |   P_missing_critical_median | selection_role                          |
|------------------------:|------------------:|----------:|:-------------------------|------------------------------:|------------------------:|-------------------------:|------------------------:|-------------------------:|-------------------------------:|--------------------:|---------------------:|----------------:|----------------------------:|:----------------------------------------|
|                      16 |                21 |     11772 | PARTIAL_DALPHA_CANDIDATE |                      -7.35521 |                0.65762  |                        0 |                0.187891 |                 0.444676 |                       0.123173 |            0.366728 |            -0.212731 |        0.593333 |                    0.616667 | class_balanced_PARTIAL_DALPHA_CANDIDATE |
|                      18 |                 4 |     11768 | PARTIAL_DALPHA_CANDIDATE |                      -8.0591  |                0.533654 |                        0 |                0.230769 |                 0.480769 |                       0.139423 |            0.372648 |            -0.255289 |        0.593333 |                    0.616667 | partial_dalpha_anchor                   |
|                      30 |                 5 |     11776 | LOW_PRIORITY             |                     -13.6066  |                0.659656 |                        0 |                0.156788 |                 0.650096 |                       0.349904 |            0.486177 |            -0.48441  |        0.462778 |                    0.872222 | low_priority_anchor                     |

These review queues should be inspected before moving to physical-window labeling.

---

## 9. What this establishes

This panel establishes six things.

### 9.1 v0.2 scales beyond the five-shot panel

The diagnostic-confidence correction did not only work on the original hand-checked five-shot set.

### 9.2 Full-diagnostic cases are enriched

All top-ranked cases are full-profile-edge candidates, and the top 10 contains no low-priority shots.

### 9.3 Weak controls are suppressed

Low-priority shots have zero confidence-positive fraction and high critical-missing penalties.

### 9.4 Partial cases are corrected

Partial D-alpha candidates can show substantial raw-positive behavior, but confidence correction suppresses them.

### 9.5 Confidence-positive behavior is tied to diagnostic confidence

Confidence-positive cases have moderate/high median `Q_diag`.

### 9.6 The reference shot is no longer artificially privileged

Shot `12063` remains interpretable, but other full-diagnostic cases rank above it. This is a healthy result because it suggests the method is identifying a broader diagnostic class structure rather than only recovering the original reference.

---

## 10. What this does not establish

This result still does not prove physical H-mode.

It does not identify L-mode, L-H transition, stable H-mode, pre-ELM, post-ELM, or H-L back-transition windows.

It does not prove that confidence-positive windows correspond to true H-mode confinement.

It does not compare against standard plasma predictors.

It does not validate confinement improvement.

It does not justify full 11,188-shot scaling yet.

It does not justify a public-facing claim that UNNS explains H-mode.

The bounded claim is:

> The v0.2 diagnostic-confidence UNNS-H Mode margin passed a 30-shot controlled TokaMark stability test: full-profile-edge candidates were enriched among top-ranked confidence-positive cases, while partial and low-priority cases were suppressed.

---

## 11. Decision

The correct decision after this panel is:

```text
v0.2 method status: methodologically strengthened
moderate panel status: passed initial stability test
physical validation: not yet
next step: define physical-window labeling requirements
```

The next step should not be another formula revision and not a blind full scan.

The next step is:

```text
docs/
  28_PHYSICAL_WINDOW_LABELING_REQUIREMENTS.md
```

That document should define what evidence is needed to label:

```text
L-mode interval
L-H transition interval
stable H-mode interval
pre-ELM interval
post-ELM interval
H-L back-transition interval
```

Only after that can this project return to the original physical H-mode question.

---

## 12. Failure modes still to watch

Even though the moderate panel passed, several risks remain.

```text
TokaMark signals may be normalized/preprocessed rather than raw physical units.
FULL_PROFILE_EDGE_CANDIDATE enrichment may partly reflect diagnostic completeness rather than true physics.
Q_diag currently encodes diagnostic availability, not physical correctness.
No physical L/H labels have been applied yet.
The confidence structural score is still a methodological score, not a plasma-performance metric.
```

These risks are why the next phase must be physical-window labeling, not immediate publication or full-corpus scaling.

---

## 13. Project status update

```text
TCV event-level model:                         complete
TCV full-corpus extension:                     complete
TokaMark metadata access:                      complete
TokaMark one-shot array probe:                 complete
TokaMark raw m_edge(t) v0.1:                   complete
TokaMark trace inspection:                     complete
TokaMark five-shot confidence revision:        passed
Moderate 30-shot confidence panel:             passed initial stability test
Current model status:                          v0.2 methodologically strengthened
Physical H-mode validation:                    not yet
Next required step:                            physical-window labeling requirements
```

---

## 14. Final synthesis statement

The moderate TokaMark confidence panel is the strongest methodological result produced in the UNNS-H Mode project so far.

The v0.2 diagnostic-confidence correction preserved meaningful confidence-positive behavior in diagnostically complete full-profile-edge candidates while suppressing partial and low-priority cases. It also showed that the original reference shot `12063` is not unique: other full-profile-edge shots rank above it, which strengthens the case that the method is detecting a broader diagnostic class structure rather than overfitting one chosen shot.

This remains a methodological validation, not a physical validation. The project can now move from structural confidence testing to the next necessary gate: defining physical-window labels and requirements.
