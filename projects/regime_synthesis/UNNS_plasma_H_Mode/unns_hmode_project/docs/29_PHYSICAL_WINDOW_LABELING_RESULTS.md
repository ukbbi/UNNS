# Physical-Window Labeling Results — UNNS-H Mode Project

## 1. Purpose

This document reports the first physical-window alignment test for the UNNS-H Mode project.

It belongs here:

```text
unns_hmode_project/
  docs/
    29_PHYSICAL_WINDOW_LABELING_RESULTS.md
```

It follows:

```text
docs/
  28_PHYSICAL_WINDOW_LABELING_REQUIREMENTS.md
```

The purpose of this stage was to test whether independently edited physical-window labels align with the v0.2 diagnostic-confidence UNNS-H Mode trace:

```text
m_edge_conf(t)
```

This is the first stage where the project moves beyond structural-methodology testing into a provisional physical-window alignment test.

---

## 2. Input files

The analyzer used the edited label file:

```text
outputs/reports/
  tokamark_physical_window_label_template_EDITED.csv
```

and compared it against per-shot confidence traces:

```text
outputs/reports/
  tokamark_shot_<SHOT>_m_edge_confidence_revision.csv
```

The generated analysis outputs were:

```text
outputs/reports/
  tokamark_physical_window_label_analysis.csv
  tokamark_physical_window_label_analysis_by_label.csv
  tokamark_physical_window_label_analysis_transition_pairs.csv
  tokamark_physical_window_label_analysis.json
  tokamark_physical_window_label_analysis.md
```

---

## 3. Decision

The physical-window analysis returned:

```text
decision: physical_window_analysis_passes_first_gate
eligible windows: 17
excluded windows: 72
label counts: {'L_MODE': 6, 'LH_TRANSITION': 6, 'H_MODE_STABLE': 5}
```

Reasons:

```text
- Both L_MODE and H_MODE_STABLE labels are present.
- LH_TRANSITION labels are present for transition-local comparison.
- H_MODE_STABLE windows have higher median m_edge_conf than L_MODE windows.
- H_MODE_STABLE windows have equal or higher confidence-positive fraction than L_MODE windows.
- Most within-shot H_MODE_STABLE windows have higher m_edge_conf than L_MODE windows.
- UNLABELABLE control windows are excluded from validation.
```

Warnings:

```text
- None.
```

This passes the first physical-window gate.

The result is not final H-mode validation. It is a first-gate alignment result showing that the confidence-corrected UNNS margin behaves in the expected direction across independently edited physical windows.

---

## 4. Eligible and excluded windows

The edited label file contained:

```text
eligible validation windows: 17
excluded windows: 72
```

Eligible windows were:

```text
L_MODE:        6
LH_TRANSITION: 6
H_MODE_STABLE: 5
```

Excluded windows included ambiguous review windows and unlabelable controls. The controls were intentionally excluded from validation because critical independent diagnostics were missing.

---

## 5. By-label summary

| label_type    |   window_count |   shot_count |   total_duration |   m_edge_conf_median_median |   m_edge_raw_median_median |   conf_positive_fraction_median |   conf_negative_fraction_median |   Q_diag_median_median |   P_missing_critical_median_median |   C_edge_capacity_median_median |   F_route_fragmentation_median_median |
|:--------------|---------------:|-------------:|-----------------:|----------------------------:|---------------------------:|--------------------------------:|--------------------------------:|-----------------------:|-----------------------------------:|--------------------------------:|--------------------------------------:|
| H_MODE_STABLE |              5 |            5 |            0.336 |                   0.0525031 |                  0.0525031 |                         0.26087 |                        0        |               1        |                          0         |                        0.467415 |                              0.445735 |
| LH_TRANSITION |              6 |            6 |            0.115 |                  -0.288993  |                 -0.0875676 |                         0       |                        0.590909 |               0.888889 |                          0.0111111 |                        0.340801 |                              0.391533 |
| L_MODE        |              6 |            6 |            0.39  |                  -1.12      |                 -0.0879704 |                         0       |                        0.108392 |               0.06     |                          1         |                        0.432684 |                              1        |

The central directional result is:

```text
L_MODE        median m_edge_conf: -1.12
LH_TRANSITION median m_edge_conf: -0.288993
H_MODE_STABLE median m_edge_conf: 0.0525031
```

Thus the first-gate ordering is:

```text
L_MODE < LH_TRANSITION < H_MODE_STABLE
```

The confidence-positive fractions also follow the expected direction:

```text
L_MODE        median confidence-positive fraction: 0
LH_TRANSITION median confidence-positive fraction: 0
H_MODE_STABLE median confidence-positive fraction: 0.26087
```

---

## 6. Interpretation of each physical label

### 6.1 L_MODE

L-mode windows were the pre-transition baseline intervals.

Observed summary:

```text
window count: 6
shot count: 6
median m_edge_conf: -1.12
median confidence-positive fraction: 0
median confidence-negative fraction: 0.108392
median Q_diag: 0.06
median P_missing_critical: 1
```

The L-mode result is strongly negative in `m_edge_conf`. This supports the intended interpretation that the pre-transition edge is not yet structurally boundary-admissible in the v0.2 sense.

However, L-mode windows also have very low diagnostic confidence and high critical-missing penalty. This means the negative L-mode result is useful, but it must be treated cautiously.

### 6.2 LH_TRANSITION

L-H transition windows were assigned from early D-alpha sharp-change intervals in full-diagnostic shots.

Observed summary:

```text
window count: 6
shot count: 6
median m_edge_conf: -0.288993
median confidence-positive fraction: 0
median confidence-negative fraction: 0.590909
median Q_diag: 0.888889
median P_missing_critical: 0.0111111
```

The transition windows sit between L-mode and H-mode-stable windows. This is directionally consistent with a boundary reorganization phase rather than a fully established confinement state.

### 6.3 H_MODE_STABLE

H-mode-stable windows were low-confidence post-transition candidates, included only for first-pass comparison.

Observed summary:

```text
window count: 5
shot count: 5
median m_edge_conf: 0.0525031
median confidence-positive fraction: 0.26087
median confidence-negative fraction: 0
median Q_diag: 1
median P_missing_critical: 0
```

This is the strongest alignment result. H-mode-stable windows have higher `m_edge_conf`, higher confidence-positive fraction, full diagnostic confidence, and zero critical-missing penalty.

---

## 7. Within-shot L/H comparison

|   shot_id | has_L_MODE   | has_LH_TRANSITION   | has_H_MODE_STABLE   |   L_MODE_m_edge_conf_median |   LH_TRANSITION_m_edge_conf_median |   H_MODE_STABLE_m_edge_conf_median |   delta_H_minus_L_m_edge_conf_median |   L_MODE_conf_positive_fraction |   H_MODE_STABLE_conf_positive_fraction |   delta_H_minus_L_conf_positive_fraction |
|----------:|:-------------|:--------------------|:--------------------|----------------------------:|-----------------------------------:|-----------------------------------:|-------------------------------------:|--------------------------------:|---------------------------------------:|-----------------------------------------:|
|     11941 | True         | True                | False               |                       -1.12 |                         -0.313112  |                        nan         |                            nan       |                               0 |                             nan        |                               nan        |
|     12007 | True         | True                | True                |                       -1.12 |                         -0.174448  |                         -0.038158  |                              1.08184 |                               0 |                               0        |                                 0        |
|     12017 | True         | True                | True                |                       -1.12 |                         -0.0301809 |                         -0.0580491 |                              1.06195 |                               0 |                               0        |                                 0        |
|     12046 | True         | True                | True                |                       -1.12 |                         -0.498215  |                          0.205992  |                              1.32599 |                               0 |                               0.514493 |                                 0.514493 |
|     12055 | True         | True                | True                |                       -1.12 |                         -0.264874  |                          0.195762  |                              1.31576 |                               0 |                               0.481481 |                                 0.481481 |
|     12063 | True         | True                | True                |                       -1.12 |                         -0.313209  |                          0.0525031 |                              1.1725  |                               0 |                               0.26087  |                                 0.26087  |

The within-shot comparison is important because it reduces the risk that the result is only a between-shot artifact.

For each shot with both L-mode and H-mode-stable windows, the analyzer computed:

```text
delta_H_minus_L_m_edge_conf_median
```

The observed deltas are positive in the available paired cases. This means that, within the same shot, the post-transition H-mode-stable candidate has higher `m_edge_conf` than the pre-transition L-mode baseline.

That is the first physically meaningful alignment result in the project.

---

## 8. Eligible window-level analysis

|   shot_id | window_id                      | label_type    | label_confidence   | validation_eligible   |     t_start |       t_end |   window_duration |   n_samples |   m_edge_conf_median |   m_edge_raw_median |   conf_positive_fraction |   conf_negative_fraction |   Q_diag_median |   P_missing_critical_median | analysis_status   |
|----------:|:-------------------------------|:--------------|:-------------------|:----------------------|------------:|------------:|------------------:|------------:|---------------------:|--------------------:|-------------------------:|-------------------------:|----------------:|----------------------------:|:------------------|
|     11941 | 11941_MANUAL_L_MODE_001        | L_MODE        | moderate           | True                  | -0.059      | -0.00300001 |             0.056 |          55 |           -1.12      |           0.181325  |                 0        |                 0.109091 |        0.06     |                   1         | ok                |
|     11941 | 11941_CANDIDATE_001            | LH_TRANSITION | moderate           | True                  | -0.00300001 |  0.00899999 |             0.012 |          13 |           -0.313112  |           0.119541  |                 0        |                 1        |        0.627778 |                   0.422222  | ok                |
|     12007 | 12007_MANUAL_L_MODE_001        | L_MODE        | moderate           | True                  | -0.0692     | -0.00220001 |             0.067 |          66 |           -1.12      |          -0.0878773 |                 0        |                 0.106061 |        0.06     |                   1         | ok                |
|     12007 | 12007_CANDIDATE_001            | LH_TRANSITION | moderate           | True                  | -0.00220001 |  0.0208     |             0.023 |          24 |           -0.174448  |          -0.0875264 |                 0        |                 0.458333 |        0.888889 |                   0.0111111 | ok                |
|     12007 | 12007_MANUAL_H_MODE_STABLE_001 | H_MODE_STABLE | low                | True                  |  0.0358     |  0.0738     |             0.038 |          38 |           -0.038158  |          -0.038158  |                 0        |                 0.105263 |        1        |                   0         | ok                |
|     12017 | 12017_MANUAL_L_MODE_001        | L_MODE        | moderate           | True                  | -0.0692     |  0.00979999 |             0.079 |          78 |           -1.12      |          -0.0803871 |                 0        |                 0.205128 |        0.06     |                   1         | ok                |
|     12017 | 12017_CANDIDATE_001            | LH_TRANSITION | moderate           | True                  |  0.00979999 |  0.0218     |             0.012 |          12 |           -0.0301809 |           0.0031961 |                 0        |                 0        |        0.888889 |                   0.0111111 | ok                |
|     12017 | 12017_MANUAL_H_MODE_STABLE_001 | H_MODE_STABLE | low                | True                  |  0.0368     |  0.0738     |             0.037 |          37 |           -0.0580491 |          -0.0580491 |                 0        |                 0.027027 |        1        |                   0         | ok                |
|     12046 | 12046_MANUAL_L_MODE_001        | L_MODE        | moderate           | True                  | -0.068      | -0.00200001 |             0.066 |          65 |           -1.12      |          -0.265573  |                 0        |                 0.107692 |        0.06     |                   1         | ok                |
|     12046 | 12046_CANDIDATE_001            | LH_TRANSITION | moderate           | True                  | -0.00200001 |  0.02       |             0.022 |          22 |           -0.498215  |          -0.214882  |                 0        |                 0.636364 |        0.627778 |                   0.422222  | ok                |
|     12046 | 12046_MANUAL_H_MODE_STABLE_001 | H_MODE_STABLE | low                | True                  |  0.035      |  0.173      |             0.138 |         138 |            0.205992  |           0.205992  |                 0.514493 |                 0        |        1        |                   0         | ok                |
|     12055 | 12055_MANUAL_L_MODE_001        | L_MODE        | moderate           | True                  | -0.0504     |  0.00559999 |             0.056 |          56 |           -1.12      |          -0.282424  |                 0        |                 0.285714 |        0.06     |                   1         | ok                |
|     12055 | 12055_CANDIDATE_002            | LH_TRANSITION | moderate           | True                  |  0.00559999 |  0.0296     |             0.024 |          24 |           -0.264874  |          -0.204304  |                 0        |                 0.75     |        0.888889 |                   0.0111111 | ok                |
|     12055 | 12055_MANUAL_H_MODE_STABLE_001 | H_MODE_STABLE | low                | True                  |  0.0446     |  0.0986     |             0.054 |          54 |            0.195762  |           0.195762  |                 0.481481 |                 0        |        1        |                   0         | ok                |
|     12063 | 12063_MANUAL_L_MODE_001        | L_MODE        | moderate           | True                  | -0.068      | -0.00200001 |             0.066 |          65 |           -1.12      |          -0.0880636 |                 0        |                 0.107692 |        0.06     |                   1         | ok                |
|     12063 | 12063_CANDIDATE_001            | LH_TRANSITION | moderate           | True                  | -0.00200001 |  0.02       |             0.022 |          22 |           -0.313209  |          -0.0876087 |                 0        |                 0.545455 |        0.888889 |                   0.0111111 | ok                |
|     12063 | 12063_MANUAL_H_MODE_STABLE_001 | H_MODE_STABLE | low                | True                  |  0.035      |  0.104      |             0.069 |          69 |            0.0525031 |           0.0525031 |                 0.26087  |                 0        |        1        |                   0         | ok                |

These are the windows that actually contributed validation evidence. Ambiguous and unlabelable windows were retained in the files but excluded from the validation decision.

---

## 9. Excluded-window audit

| label_type   |   window_count |   shot_count |   median_m_edge_conf |   median_Q_diag |   median_P_missing_critical |
|:-------------|---------------:|-------------:|---------------------:|----------------:|----------------------------:|
| AMBIGUOUS    |             54 |            6 |            0.0405482 |        1        |                    0        |
| UNLABELABLE  |             18 |            2 |           -0.526867  |        0.482222 |                    0.627778 |

The exclusion behavior matters because the earlier v0.1 method was vulnerable to over-reading incomplete cases.

The controls remain excluded:

```text
11768:
  UNLABELABLE
  missing NBI power and Thomson Te/ne profile gradients

11776:
  UNLABELABLE
  missing D-alpha, NBI power, and Thomson Te/ne profile gradients
```

This confirms that the physical-window analysis did not smuggle weak controls back into the validation set.

---

## 10. What this establishes

This first physical-window gate establishes five things.

### 10.1 Independent labels can be compared to the UNNS trace

The project now has a working path from physical labels to structural comparison:

```text
manual physical labels
→ window-level extraction
→ m_edge_conf comparison
→ by-label and within-shot summaries
```

### 10.2 H-mode-stable windows are structurally stronger than L-mode windows

The direction is correct:

```text
H_MODE_STABLE > L_MODE
```

by median `m_edge_conf`.

### 10.3 Transition windows are intermediate

L-H transition windows sit between L-mode and H-mode-stable windows in the first-pass summary.

### 10.4 Controls remain excluded

Unlabelable control windows do not contribute validation evidence.

### 10.5 The result is no longer only metadata-class behavior

The test is now performed on labeled time windows rather than only on shot-level candidate classes.

---

## 11. What this does not establish

This result does not yet prove the physical origin of H-mode.

It does not prove that all H-mode windows are detected.

It does not prove that all confidence-positive windows are true H-mode intervals.

It does not compare against standard plasma predictors.

It does not validate against published expert L-H transition labels.

It does not show cross-machine generality.

It does not remove the need for manual review of the labels.

It remains a first-gate physical-window alignment result.

---

## 12. Main caveat

The main caveat is the quality of the physical labels.

The labels were conservative but still provisional. In particular:

```text
H_MODE_STABLE windows are low-confidence post-transition candidates.
L_MODE windows show very low Q_diag and high P_missing_critical.
Several later physical marker windows remain AMBIGUOUS and excluded.
The TokaMark signals may be normalized or preprocessed rather than raw physical units.
```

Therefore the result should be described as:

```text
first-gate physical-window alignment
```

not as final H-mode validation.

---

## 13. Decision

The correct decision after this result is:

```text
physical-window first gate: passed
model status: v0.2 physically aligned on provisional labels
validation status: provisional, not final
next step: independent label hardening and/or expert-label comparison
```

The project should not jump directly to a public H-mode claim.

The next legitimate options are:

```text
1. Harden labels by manual review of the ambiguous windows.
2. Add published or expert L-H transition labels if available.
3. Compare v0.2 against standard predictors.
4. Expand physical-window labeling to more full-profile-edge shots.
```

---

## 14. Recommended next step

The best next step is label hardening:

```text
docs/
  30_PHYSICAL_WINDOW_LABEL_HARDENING_PLAN.md
```

That plan should define how to turn provisional labels into stronger physical labels by requiring:

```text
D-alpha morphology confirmation
profile-gradient confirmation
soft-X consistency
power/density context
manual rejection of ambiguous windows
comparison against any published L-H timing if available
```

Only after label hardening should the project attempt a stronger validation statement.

---

## 15. Project status update

```text
TCV event-level model:                         complete
TCV full-corpus extension:                     complete
TokaMark metadata access:                      complete
TokaMark one-shot array probe:                 complete
TokaMark raw m_edge(t) v0.1:                   complete
TokaMark confidence revision v0.2:             passed initial panel
Moderate 30-shot confidence panel:             passed
Physical-window label template:                complete
Edited physical-window label draft:            complete
Physical-window alignment analysis:            passed first gate
Current model status:                          v0.2 provisionally physically aligned
Final H-mode validation:                       not yet
Next required gate:                            label hardening / expert-label comparison
```

---

## 16. Final synthesis statement

The UNNS-H Mode project has now passed its first physical-window alignment gate.

The v0.2 confidence-corrected structural margin is not merely ranking diagnostically complete shots. When compared against provisional independently edited physical windows, it orders the windows in the expected direction: L-mode is most negative, transition is intermediate, and H-mode-stable candidates are structurally stronger and partially confidence-positive. Within-shot comparisons also show higher `m_edge_conf` in H-mode-stable candidate windows than in L-mode baselines.

This is the first result in the project that begins to connect the UNNS boundary-admissibility interpretation to physical plasma-regime windows.

The claim must remain bounded: this is not final proof of the H-mode mechanism. It is a successful first-gate physical-window alignment test, and the next step is to harden the labels.
