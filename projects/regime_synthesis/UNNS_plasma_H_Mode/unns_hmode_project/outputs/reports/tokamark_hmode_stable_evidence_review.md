# TokaMark H-Mode-Stable Evidence Review

## Purpose

Focused review of excluded `H_MODE_STABLE` candidate windows from the conservative hardened-label pass.

This review supports:

```text
docs/
  33_H_MODE_STABLE_EVIDENCE_RECOVERY_RESULTS.md
```

## Non-circularity rule

Do not accept an H-mode-stable label from `m_edge_conf(t)`. UNNS audit columns are shown only after the physical evidence fields.

## Summary

- **candidate_count**: `5`
- **shot_count**: `5`
- **decision_counts**: `{'NEEDS_EXTERNAL_REFERENCE': 5}`
- **hardening_level_counts**: `{'1_PLAUSIBLE': 5}`
- **accepted_count_initial**: `0`
- **score_summary**: `{'min': 7.0, 'median': 8.0, 'max': 8.0}`

## Candidate review table

|   shot_id | window_id                      |   t_start |   t_end |   dalpha_evidence_score |   profile_evidence_score |   softx_evidence_score |   power_density_context_score |   external_reference_score |   H_evidence_score | physical_review_decision   | accepted_as_hmode_stable   | hardening_level   | excluded_from_validation   |   UNNS_AUDIT_m_edge_conf_median |   UNNS_AUDIT_conf_positive_fraction |   UNNS_AUDIT_Q_diag_median |
|----------:|:-------------------------------|----------:|--------:|------------------------:|-------------------------:|-----------------------:|------------------------------:|---------------------------:|-------------------:|:---------------------------|:---------------------------|:------------------|:---------------------------|--------------------------------:|------------------------------------:|---------------------------:|
|     12007 | 12007_MANUAL_H_MODE_STABLE_001 |    0.0358 |  0.0738 |                       2 |                        2 |                      2 |                             2 |                          0 |                  8 | NEEDS_EXTERNAL_REFERENCE   | False                      | 1_PLAUSIBLE       | True                       |                      -0.038158  |                            0        |                          1 |
|     12017 | 12017_MANUAL_H_MODE_STABLE_001 |    0.0368 |  0.0738 |                       2 |                        2 |                      2 |                             2 |                          0 |                  8 | NEEDS_EXTERNAL_REFERENCE   | False                      | 1_PLAUSIBLE       | True                       |                      -0.0580491 |                            0        |                          1 |
|     12046 | 12046_MANUAL_H_MODE_STABLE_001 |    0.035  |  0.173  |                       1 |                        2 |                      2 |                             2 |                          0 |                  7 | NEEDS_EXTERNAL_REFERENCE   | False                      | 1_PLAUSIBLE       | True                       |                       0.205992  |                            0.514493 |                          1 |
|     12055 | 12055_MANUAL_H_MODE_STABLE_001 |    0.0446 |  0.0986 |                       2 |                        2 |                      2 |                             2 |                          0 |                  8 | NEEDS_EXTERNAL_REFERENCE   | False                      | 1_PLAUSIBLE       | True                       |                       0.195762  |                            0.481481 |                          1 |
|     12063 | 12063_MANUAL_H_MODE_STABLE_001 |    0.035  |  0.104  |                       2 |                        2 |                      2 |                             2 |                          0 |                  8 | NEEDS_EXTERNAL_REFERENCE   | False                      | 1_PLAUSIBLE       | True                       |                       0.0525031 |                            0.26087  |                          1 |

## Per-window physical notes

### 12007_MANUAL_H_MODE_STABLE_001

- Shot: `12007`
- Interval: `0.0357999909` to `0.0737999909`
- D-alpha: column=dalpha_proxy; pre_median=0.3247070311849275; window_median=0.43457031251058453; post_median=0.4956054687672185; pre_to_window_delta=0.10986328132565704; window_std=0.03318663384903698. Reviewer must decide whether morphology supports post-transition stable H-mode behavior.
- Profile: column=profile_gradient_proxy; pre_median=1.3637850972906538e+17; window_median=3.439960335257875e+17; post_median=3.543657948382902e+17; pre_to_window_delta=2.0761752379672214e+17. Reviewer must confirm edge-gradient/pedestal-like support.
- Soft-X: column=softx_combined_proxy; pre_median=0.0001049041746747; window_median=0.0005817413323896; post_median=0.0058746337886405; pre_to_window_delta=0.0004768371577149; window_std=0.0001986136848286288. Reviewer must confirm edge-activity consistency and absence of disruptive behavior.
- Power/density: nbi_column=nbi_proxy; nbi_window_median=-0.366126537322998; density_column=density_proxy; density_window_median=7.560383129880782e+19. Reviewer must decide whether power/density context is physically plausible.
- External reference: No external L-H/H-mode timing supplied. Fill if published timing, shot log, or expert annotation is available.

UNNS audit only — not used for physical label assignment:

```text
m_edge_conf median: -0.03815799232530345
confidence-positive fraction: 0.0
confidence-negative fraction: 0.10526315789473684
Q_diag median: 1.0
P_missing_critical median: 0.0
```

### 12017_MANUAL_H_MODE_STABLE_001

- Shot: `12017`
- Interval: `0.0367999909` to `0.0737999909`
- D-alpha: column=dalpha_proxy; pre_median=0.2661132812232405; window_median=0.3405761718820066; post_median=0.4687500000171439; pre_to_window_delta=0.0744628906587661; window_std=0.05053331181972597. Reviewer must decide whether morphology supports post-transition stable H-mode behavior.
- Profile: column=profile_gradient_proxy; pre_median=8.170479752484616e+16; window_median=3.219332543185731e+17; post_median=3.034785959140936e+17; pre_to_window_delta=2.4022845679372698e+17. Reviewer must confirm edge-gradient/pedestal-like support.
- Soft-X: column=softx_combined_proxy; pre_median=0.0002551078801517; window_median=0.00059843063297745; post_median=0.0038814544679269; pre_to_window_delta=0.00034332275282575; window_std=0.00013688663585826523. Reviewer must confirm edge-activity consistency and absence of disruptive behavior.
- Power/density: nbi_column=nbi_proxy; nbi_window_median=0.4393558800220489; density_column=density_proxy; density_window_median=7.316921788579552e+19. Reviewer must decide whether power/density context is physically plausible.
- External reference: No external L-H/H-mode timing supplied. Fill if published timing, shot log, or expert annotation is available.

UNNS audit only — not used for physical label assignment:

```text
m_edge_conf median: -0.0580491296275909
confidence-positive fraction: 0.0
confidence-negative fraction: 0.02702702702702703
Q_diag median: 1.0
P_missing_critical median: 0.0
```

### 12046_MANUAL_H_MODE_STABLE_001

- Shot: `12046`
- Interval: `0.0349999889` to `0.172999989`
- D-alpha: column=dalpha_proxy; pre_median=0.1928710937147431; window_median=0.214843750001938; post_median=0.2490234375290701; pre_to_window_delta=0.021972656287194914; window_std=0.08479919902086212. Reviewer must decide whether morphology supports post-transition stable H-mode behavior.
- Profile: column=profile_gradient_proxy; pre_median=8.371031769153917e+16; window_median=2.6401111171268166e+17; post_median=1.6575868126704496e+17; pre_to_window_delta=1.803007940211425e+17. Reviewer must confirm edge-gradient/pedestal-like support.
- Soft-X: column=softx_combined_proxy; pre_median=9.536743156985002e-05; window_median=0.0065040588391974494; post_median=0.0197601318376275; pre_to_window_delta=0.006408691407627599; window_std=0.004329499263785462. Reviewer must confirm edge-activity consistency and absence of disruptive behavior.
- Power/density: nbi_column=nbi_proxy; nbi_window_median=-0.4393183887004852; density_column=density_proxy; density_window_median=7.524857469382689e+19. Reviewer must decide whether power/density context is physically plausible.
- External reference: No external L-H/H-mode timing supplied. Fill if published timing, shot log, or expert annotation is available.

UNNS audit only — not used for physical label assignment:

```text
m_edge_conf median: 0.2059915757127067
confidence-positive fraction: 0.5144927536231884
confidence-negative fraction: 0.0
Q_diag median: 1.0
P_missing_critical median: 0.0
```

### 12055_MANUAL_H_MODE_STABLE_001

- Shot: `12055`
- Interval: `0.0445999888` to `0.0985999888`
- D-alpha: column=dalpha_proxy; pre_median=0.4467773437508131; window_median=0.48339843750190925; post_median=0.4174804687465576; pre_to_window_delta=0.03662109375109612; window_std=0.022599825647082128. Reviewer must decide whether morphology supports post-transition stable H-mode behavior.
- Profile: column=profile_gradient_proxy; pre_median=2.1644317308409357e+17; window_median=4.1732987709187546e+17; post_median=3.523179885667975e+17; pre_to_window_delta=2.008867040077819e+17. Reviewer must confirm edge-gradient/pedestal-like support.
- Soft-X: column=softx_combined_proxy; pre_median=-8.583068848369763e-05; window_median=0.00010728836057160001; post_median=0.0005340576172243; pre_to_window_delta=0.00019311904905529764; window_std=0.00024044883872415134. Reviewer must confirm edge-activity consistency and absence of disruptive behavior.
- Power/density: nbi_column=nbi_proxy; nbi_window_median=410.3318176269531; density_column=density_proxy; density_window_median=6.846116627026333e+19. Reviewer must decide whether power/density context is physically plausible.
- External reference: No external L-H/H-mode timing supplied. Fill if published timing, shot log, or expert annotation is available.

UNNS audit only — not used for physical label assignment:

```text
m_edge_conf median: 0.19576176397209072
confidence-positive fraction: 0.48148148148148145
confidence-negative fraction: 0.0
Q_diag median: 1.0
P_missing_critical median: 0.0
```

### 12063_MANUAL_H_MODE_STABLE_001

- Shot: `12063`
- Interval: `0.0349999889` to `0.103999989`
- D-alpha: column=dalpha_proxy; pre_median=0.1977539062466085; window_median=0.2612304687547332; post_median=0.075683593721377; pre_to_window_delta=0.06347656250812472; window_std=0.02795443739262532. Reviewer must decide whether morphology supports post-transition stable H-mode behavior.
- Profile: column=profile_gradient_proxy; pre_median=8.23097803856558e+16; window_median=2.3836912763803248e+17; post_median=2.5032458366803866e+17; pre_to_window_delta=1.5605934725237667e+17. Reviewer must confirm edge-gradient/pedestal-like support.
- Soft-X: column=softx_combined_proxy; pre_median=0.0001049041747393; window_median=0.0006961822499458; post_median=0.0051021575932425; pre_to_window_delta=0.0005912780752065; window_std=0.0018634469702105368. Reviewer must confirm edge-activity consistency and absence of disruptive behavior.
- Power/density: nbi_column=nbi_proxy; nbi_window_median=0.6151038408279419; density_column=density_proxy; density_window_median=7.205856600620689e+19. Reviewer must decide whether power/density context is physically plausible.
- External reference: No external L-H/H-mode timing supplied. Fill if published timing, shot log, or expert annotation is available.

UNNS audit only — not used for physical label assignment:

```text
m_edge_conf median: 0.0525030970732071
confidence-positive fraction: 0.2608695652173913
confidence-negative fraction: 0.0
Q_diag median: 1.0
P_missing_critical median: 0.0
```

## Manual next step

Edit:

```text
outputs/reports/tokamark_hmode_stable_evidence_review.csv
```

Then create:

```text
outputs/reports/tokamark_physical_window_labels_HARDENED_v0_2.csv
```
