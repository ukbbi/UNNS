# Physical-Window Label Hardening Results — UNNS-H Mode Project

## 1. Purpose

This document reports the conservative hardening pass for the physical-window labels in the UNNS-H Mode project.

It belongs here:

```text
unns_hmode_project/
  docs/
    31_PHYSICAL_WINDOW_LABEL_HARDENING_RESULTS.md
```

It follows:

```text
docs/
  30_PHYSICAL_WINDOW_LABEL_HARDENING_PLAN.md
docs/
  31A_REPRODUCIBILITY_PROTOCOL_HARDENED_LABELS.md
```

The purpose of this stage was to test whether the first physical-window alignment result survives a stricter, reproducible, conservative hardening pass.

The answer is:

```text
No, not yet.
```

The earlier first-gate alignment remains useful as a provisional result, but after conservative hardening the `H_MODE_STABLE` windows are excluded from validation pending stronger physical evidence. Therefore the key H-vs-L comparison cannot yet be claimed as hardened.

---

## 2. Inputs

The hardened analyzer used:

```text
outputs/reports/
  tokamark_physical_window_labels_HARDENED_v0_1.csv
```

and compared it against:

```text
outputs/reports/
  tokamark_shot_<SHOT>_m_edge_confidence_revision.csv
```

The analyzer generated:

```text
outputs/reports/
  tokamark_physical_window_label_analysis_HARDENED_v0_1.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_1_by_label.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_1_transition_pairs.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_1.json
  tokamark_physical_window_label_analysis_HARDENED_v0_1.md
```

The hardened label file was reproducible from:

```text
outputs/reports/
  tokamark_physical_window_labels_HARDENING_REVIEW.csv
```

using:

```text
components/
  reproduce_hardened_v0_1_from_review.py
```

---

## 3. Conservative hardening rule

The hardening rule was:

```text
Conservative v0.1 hardening: accept L_MODE/LH_TRANSITION rows initially marked ACCEPT; exclude all H_MODE_STABLE rows pending external or stronger physical evidence; keep AMBIGUOUS and UNLABELABLE excluded.
```

Operationally:

```text
Accepted:
  L_MODE rows initially marked ACCEPT
  LH_TRANSITION rows initially marked ACCEPT

Excluded:
  all H_MODE_STABLE rows
  all AMBIGUOUS rows
  all UNLABELABLE rows
```

The reason for excluding `H_MODE_STABLE` was strict non-circularity: post-transition quiet intervals were not accepted as stable H-mode unless independently confirmed by stronger physical evidence such as D-alpha morphology, profile-gradient support, soft-X consistency, or external timing.

UNNS audit columns were not used to accept physical labels.

---

## 4. Hardened artifact counts

The conservative hardened file contains:

```text
rows: 89
shots: 8
eligible rows: 12
```

Label counts in the hardened artifact:

```text
{
  "AMBIGUOUS": 54,
  "UNLABELABLE": 18,
  "L_MODE": 6,
  "LH_TRANSITION": 6,
  "H_MODE_STABLE": 5
}
```

Eligible label counts:

```text
{
  "L_MODE": 6,
  "LH_TRANSITION": 6
}
```

The hardening pass therefore reduced the validation set to:

```text
L_MODE:        6
LH_TRANSITION: 6
H_MODE_STABLE: 0
```

---

## 5. Analyzer decision

The hardened analyzer returned:

```text
decision: physical_window_analysis_inconclusive_or_weak
eligible windows: 12
excluded windows: 77
label counts: {'L_MODE': 6, 'LH_TRANSITION': 6}
```

Reasons:

```text
- LH_TRANSITION labels are present for transition-local comparison.
- UNLABELABLE control windows are excluded from validation.
```

Warnings:

```text
- L_MODE and H_MODE_STABLE are not both present; direct comparison is limited.
- No finite within-shot H-vs-L m_edge_conf deltas.
```

This is the expected result of conservative hardening.

The analyzer is inconclusive or weak because the hardened validation set no longer contains both `L_MODE` and `H_MODE_STABLE`. Without accepted `H_MODE_STABLE` windows, the core comparison cannot be performed.

---

## 6. By-label summary after hardening

| label_type    |   window_count |   shot_count |   total_duration |   m_edge_conf_median_median |   m_edge_raw_median_median |   conf_positive_fraction_median |   conf_negative_fraction_median |   Q_diag_median_median |   P_missing_critical_median_median |   C_edge_capacity_median_median |   F_route_fragmentation_median_median |
|:--------------|---------------:|-------------:|-----------------:|----------------------------:|---------------------------:|--------------------------------:|--------------------------------:|-----------------------:|-----------------------------------:|--------------------------------:|--------------------------------------:|
| LH_TRANSITION |              6 |            6 |            0.115 |                   -0.288993 |                 -0.0875676 |                               0 |                        0.590909 |               0.888889 |                          0.0111111 |                        0.340801 |                              0.391533 |
| L_MODE        |              6 |            6 |            0.39  |                   -1.12     |                 -0.0879704 |                               0 |                        0.108392 |               0.06     |                          1         |                        0.432684 |                              1        |

The hardened by-label result contains only:

```text
L_MODE
LH_TRANSITION
```

The earlier first-gate ordering:

```text
L_MODE < LH_TRANSITION < H_MODE_STABLE
```

cannot be tested here because `H_MODE_STABLE` was excluded.

Observed hardened medians:

```text
L_MODE median m_edge_conf:        -1.12
LH_TRANSITION median m_edge_conf: -0.288993
H_MODE_STABLE median m_edge_conf: NA
```

Only the L-mode to transition comparison remains available.

---

## 7. Within-shot comparison after hardening

|   shot_id | has_L_MODE   | has_LH_TRANSITION   | has_H_MODE_STABLE   |   L_MODE_m_edge_conf_median |   LH_TRANSITION_m_edge_conf_median |   H_MODE_STABLE_m_edge_conf_median |   delta_H_minus_L_m_edge_conf_median |   L_MODE_conf_positive_fraction |   H_MODE_STABLE_conf_positive_fraction |   delta_H_minus_L_conf_positive_fraction |
|----------:|:-------------|:--------------------|:--------------------|----------------------------:|-----------------------------------:|-----------------------------------:|-------------------------------------:|--------------------------------:|---------------------------------------:|-----------------------------------------:|
|     11941 | True         | True                | False               |                       -1.12 |                         -0.313112  |                                nan |                                  nan |                               0 |                                    nan |                                      nan |
|     12007 | True         | True                | False               |                       -1.12 |                         -0.174448  |                                nan |                                  nan |                               0 |                                    nan |                                      nan |
|     12017 | True         | True                | False               |                       -1.12 |                         -0.0301809 |                                nan |                                  nan |                               0 |                                    nan |                                      nan |
|     12046 | True         | True                | False               |                       -1.12 |                         -0.498215  |                                nan |                                  nan |                               0 |                                    nan |                                      nan |
|     12055 | True         | True                | False               |                       -1.12 |                         -0.264874  |                                nan |                                  nan |                               0 |                                    nan |                                      nan |
|     12063 | True         | True                | False               |                       -1.12 |                         -0.313209  |                                nan |                                  nan |                               0 |                                    nan |                                      nan |

Each reviewed full-profile shot still has `L_MODE` and `LH_TRANSITION` windows.

However, each has:

```text
has_H_MODE_STABLE = False
```

Therefore the within-shot quantity:

```text
delta_H_minus_L_m_edge_conf_median
```

is not finite.

This is not a numerical failure. It is the correct consequence of excluding all `H_MODE_STABLE` windows from hardened validation.

---

## 8. Eligible hardened windows

|   shot_id | window_id               | label_type    | label_confidence   | validation_eligible   |     t_start |       t_end |   window_duration |   n_samples |   m_edge_conf_median |   m_edge_raw_median |   conf_positive_fraction |   conf_negative_fraction |   Q_diag_median |   P_missing_critical_median | analysis_status   |
|----------:|:------------------------|:--------------|:-------------------|:----------------------|------------:|------------:|------------------:|------------:|---------------------:|--------------------:|-------------------------:|-------------------------:|----------------:|----------------------------:|:------------------|
|     11941 | 11941_MANUAL_L_MODE_001 | L_MODE        | moderate           | True                  | -0.059      | -0.00300001 |             0.056 |          55 |           -1.12      |           0.181325  |                        0 |                 0.109091 |        0.06     |                   1         | ok                |
|     11941 | 11941_CANDIDATE_001     | LH_TRANSITION | moderate           | True                  | -0.00300001 |  0.00899999 |             0.012 |          13 |           -0.313112  |           0.119541  |                        0 |                 1        |        0.627778 |                   0.422222  | ok                |
|     12007 | 12007_MANUAL_L_MODE_001 | L_MODE        | moderate           | True                  | -0.0692     | -0.00220001 |             0.067 |          66 |           -1.12      |          -0.0878773 |                        0 |                 0.106061 |        0.06     |                   1         | ok                |
|     12007 | 12007_CANDIDATE_001     | LH_TRANSITION | moderate           | True                  | -0.00220001 |  0.0208     |             0.023 |          24 |           -0.174448  |          -0.0875264 |                        0 |                 0.458333 |        0.888889 |                   0.0111111 | ok                |
|     12017 | 12017_MANUAL_L_MODE_001 | L_MODE        | moderate           | True                  | -0.0692     |  0.00979999 |             0.079 |          78 |           -1.12      |          -0.0803871 |                        0 |                 0.205128 |        0.06     |                   1         | ok                |
|     12017 | 12017_CANDIDATE_001     | LH_TRANSITION | moderate           | True                  |  0.00979999 |  0.0218     |             0.012 |          12 |           -0.0301809 |           0.0031961 |                        0 |                 0        |        0.888889 |                   0.0111111 | ok                |
|     12046 | 12046_MANUAL_L_MODE_001 | L_MODE        | moderate           | True                  | -0.068      | -0.00200001 |             0.066 |          65 |           -1.12      |          -0.265573  |                        0 |                 0.107692 |        0.06     |                   1         | ok                |
|     12046 | 12046_CANDIDATE_001     | LH_TRANSITION | moderate           | True                  | -0.00200001 |  0.02       |             0.022 |          22 |           -0.498215  |          -0.214882  |                        0 |                 0.636364 |        0.627778 |                   0.422222  | ok                |
|     12055 | 12055_MANUAL_L_MODE_001 | L_MODE        | moderate           | True                  | -0.0504     |  0.00559999 |             0.056 |          56 |           -1.12      |          -0.282424  |                        0 |                 0.285714 |        0.06     |                   1         | ok                |
|     12055 | 12055_CANDIDATE_002     | LH_TRANSITION | moderate           | True                  |  0.00559999 |  0.0296     |             0.024 |          24 |           -0.264874  |          -0.204304  |                        0 |                 0.75     |        0.888889 |                   0.0111111 | ok                |
|     12063 | 12063_MANUAL_L_MODE_001 | L_MODE        | moderate           | True                  | -0.068      | -0.00200001 |             0.066 |          65 |           -1.12      |          -0.0880636 |                        0 |                 0.107692 |        0.06     |                   1         | ok                |
|     12063 | 12063_CANDIDATE_001     | LH_TRANSITION | moderate           | True                  | -0.00200001 |  0.02       |             0.022 |          22 |           -0.313209  |          -0.0876087 |                        0 |                 0.545455 |        0.888889 |                   0.0111111 | ok                |

These 12 windows are the only validation-eligible rows after conservative hardening.

They include:

```text
L_MODE:        6
LH_TRANSITION: 6
```

They do not include `H_MODE_STABLE`.

---

## 9. Excluded-window audit

| label_type    |   window_count |   shot_count |   median_m_edge_conf_median |   median_Q_diag_median |   median_P_missing_critical_median |
|:--------------|---------------:|-------------:|----------------------------:|-----------------------:|-----------------------------------:|
| AMBIGUOUS     |             54 |            6 |                   0.0405482 |               1        |                           0        |
| H_MODE_STABLE |              5 |            5 |                   0.0525031 |               1        |                           0        |
| UNLABELABLE   |             18 |            2 |                  -0.526867  |               0.482222 |                           0.627778 |

The excluded set contains the rows that should not contribute to validation under the conservative rule:

```text
H_MODE_STABLE:
  excluded pending external or stronger physical evidence

AMBIGUOUS:
  excluded pending manual interpretation

UNLABELABLE:
  excluded because critical independent diagnostics are missing
```

This is scientifically important. The hardening pass prevents the project from using attractive positive `m_edge_conf` intervals unless they also survive independent physical review.

---

## 10. What changed from the first physical-window gate

The first physical-window analysis found:

```text
L_MODE < LH_TRANSITION < H_MODE_STABLE
```

and passed the first gate.

The conservative hardening pass changed the validation set:

```text
Before hardening:
  L_MODE:        6 eligible
  LH_TRANSITION: 6 eligible
  H_MODE_STABLE: 5 eligible

After hardening:
  L_MODE:        6 eligible
  LH_TRANSITION: 6 eligible
  H_MODE_STABLE: 0 eligible
```

Therefore the strong H-vs-L alignment is not yet hardened.

The result is not disproven. It is withheld.

---

## 11. What this establishes

This hardening stage establishes four important things.

### 11.1 The pipeline is reproducible

The hardened label artifact can be reproduced deterministically from the hardening review file.

### 11.2 The method is non-circular

The conservative rule refuses to accept H-mode-stable labels merely because they look good under `m_edge_conf(t)`.

### 11.3 The controls remain excluded

Unlabelable controls remain outside validation.

### 11.4 The physical claim is not yet hardened

The strongest physical claim — that stable H-mode windows have higher `m_edge_conf` than L-mode windows — is not available after hardening because stable H-mode labels were excluded.

---

## 12. What this does not establish

This result does not establish final H-mode validation.

It does not establish that the H-mode-stable windows are false.

It does not establish that the UNNS margin is wrong.

It does not establish that the first-gate result was meaningless.

It does establish that the first-gate result was not yet strong enough to survive a conservative hardening pass.

---

## 13. Correct interpretation

The correct interpretation is:

```text
The project passed provisional physical-window alignment.
The conservative hardening artifact is reproducible.
The hardened validation set does not yet contain H_MODE_STABLE windows.
Therefore the H-vs-L result is not hardened.
The project needs stronger independent physical evidence before making a physical H-mode claim.
```

This is a useful narrowing result, not wasted work.

It tells us exactly where the evidentiary gap is:

```text
H_MODE_STABLE labeling
```

---

## 14. Decision

The hardening gate decision is:

```text
hardening artifact reproducibility: passed
conservative hardened physical validation: inconclusive_or_weak
H_MODE_STABLE survival: failed / not accepted
physical H-mode claim: not supported yet
next step: obtain stronger independent evidence for H_MODE_STABLE labels
```

The project should not proceed to broad validation or public H-mode claims yet.

---

## 15. Required next step

The next step should focus narrowly on the excluded H-mode-stable windows.

Create:

```text
docs/
  32_H_MODE_STABLE_EVIDENCE_RECOVERY_PLAN.md
```

That plan should ask:

> Can any of the excluded `H_MODE_STABLE` windows be independently supported by D-alpha morphology, profile-gradient behavior, soft-X response, power/density context, or external L-H/H-mode timing?

The next component should be:

```text
components/
  tokamark_hmode_stable_evidence_reviewer.py
```

Its purpose should be to generate focused review sheets for the five excluded H-mode-stable windows:

```text
12007_MANUAL_H_MODE_STABLE_001
12017_MANUAL_H_MODE_STABLE_001
12046_MANUAL_H_MODE_STABLE_001
12055_MANUAL_H_MODE_STABLE_001
12063_MANUAL_H_MODE_STABLE_001
```

The reviewer should inspect physical diagnostics only, then decide whether each window becomes:

```text
H_MODE_STABLE accepted
AMBIGUOUS
REJECTED
NEEDS_EXTERNAL_REFERENCE
```

---

## 16. Stop condition

Stop short of a physical H-mode claim unless at least several `H_MODE_STABLE` windows can be hardened independently.

Minimum survival condition:

```text
At least 3 H_MODE_STABLE windows accepted at hardening level 1 or 2.
```

Stronger condition:

```text
At least 3 H_MODE_STABLE windows accepted at hardening level 2,
with support from at least two physical diagnostic families.
```

Best condition:

```text
External or expert L/H timing supports the accepted windows.
```

---

## 17. Project status update

```text
TCV event-level model:                              complete
TCV full-corpus extension:                          complete
TokaMark metadata access:                           complete
TokaMark one-shot array probe:                      complete
TokaMark raw m_edge(t) v0.1:                        complete
TokaMark confidence revision v0.2:                  complete
Moderate 30-shot confidence panel:                  passed
Physical-window label template:                     complete
Edited physical-window label draft:                 complete
Physical-window first-gate alignment:               passed
Reproducibility protocol for hardened labels:       complete
Conservative hardened label artifact:               reproduced
Hardened analysis:                                  inconclusive_or_weak
Current bottleneck:                                 H_MODE_STABLE evidence
Final H-mode validation:                            not yet
```

---

## 18. Final synthesis statement

The hardening stage did exactly what it was supposed to do: it prevented a premature H-mode claim.

The earlier first-gate physical-window analysis was promising, but it relied on provisional `H_MODE_STABLE` windows. Under the conservative hardening rule, those windows were excluded because they lacked sufficiently independent physical confirmation. The hardened analysis therefore becomes inconclusive or weak, not because the code failed, but because the evidentiary standard became stricter.

The UNNS-H Mode project now has a clear next target: recover or reject the H-mode-stable windows using independent physical evidence. Until that happens, the strongest honest claim is methodological and provisional, not a validated physical explanation of H-mode.
