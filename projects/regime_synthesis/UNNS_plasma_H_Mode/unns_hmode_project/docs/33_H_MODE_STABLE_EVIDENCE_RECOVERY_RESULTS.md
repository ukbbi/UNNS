# 33 — H-Mode-Stable Evidence Recovery Results

## Purpose

This document records the result of the H-mode-stable evidence recovery gate.

The previous conservative hardening pass (`HARDENED_v0_1`) removed the `H_MODE_STABLE` windows from validation because they lacked external shot-log or publication anchoring. The v0.2 recovery gate restored only those `H_MODE_STABLE` windows that had enough independent internal physical evidence from diagnostic proxies, while keeping the non-circularity rule intact.

## Source artifacts

```text
outputs/reports/
  tokamark_hmode_stable_evidence_review.csv
  tokamark_physical_window_labels_HARDENED_v0_2.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_2.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_2_by_label.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_2_transition_pairs.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_2.json
  tokamark_physical_window_label_analysis_HARDENED_v0_2.md
```

## Non-circularity rule

The accepted `H_MODE_STABLE` windows were not accepted from the UNNS margin itself. They were recovered from the physical evidence review using D-alpha, profile-gradient, soft-X, and power-density context fields. UNNS audit columns were used only after labeling, to test whether the recovered physical labels align with the `m_edge_conf(t)` structure.

Because no external L-H/H-mode timing reference was supplied, these labels remain:

```text
hardening_level = 2_SUPPORTED
```

not:

```text
hardening_level = 3_EXTERNALLY_ANCHORED
```

## Gate result

```text
decision: physical_window_analysis_passes_first_gate
eligible windows: 17
excluded windows: 72
label counts: {'L_MODE': 6, 'LH_TRANSITION': 6, 'H_MODE_STABLE': 5}
```

The v0.2 analyzer passed the first physical-window gate.

### Reasons emitted by analyzer

- Both L_MODE and H_MODE_STABLE labels are present.
- LH_TRANSITION labels are present for transition-local comparison.
- H_MODE_STABLE windows have higher median m_edge_conf than L_MODE windows.
- H_MODE_STABLE windows have equal or higher confidence-positive fraction than L_MODE windows.
- Most within-shot H_MODE_STABLE windows have higher m_edge_conf than L_MODE windows.
- UNLABELABLE control windows are excluded from validation.

### Warnings

- None.

## By-label result

| label_type | window_count | shot_count | total_duration | m_edge_conf_median_median | conf_positive_fraction_median | conf_negative_fraction_median | Q_diag_median_median | P_missing_critical_median_median | C_edge_capacity_median_median | F_route_fragmentation_median_median |
|---|---|---|---|---|---|---|---|---|---|---|
| H_MODE_STABLE | 5 | 5 | 0.336 | 0.0525031 | 0.26087 | 0 | 1 | 0 | 0.467415 | 0.445735 |
| LH_TRANSITION | 6 | 6 | 0.115 | -0.288993 | 0 | 0.590909 | 0.888889 | 0.0111111 | 0.340801 | 0.391533 |
| L_MODE | 6 | 6 | 0.39 | -1.12 | 0 | 0.108392 | 0.06 | 1 | 0.432684 | 1 |

### Interpretation

The recovered `H_MODE_STABLE` group is separated from `L_MODE` in the expected direction:

```text
H_MODE_STABLE median m_edge_conf median:  0.0525031
LH_TRANSITION median m_edge_conf median: -0.288993
L_MODE median m_edge_conf median:        -1.12
```

This means the physical-window labels now recover the intended ordering:

```text
L_MODE  <  LH_TRANSITION  <  H_MODE_STABLE
```

in the confidence-corrected edge-admissibility margin.

The same pattern also appears in confidence-positive fraction:

```text
H_MODE_STABLE median confidence-positive fraction: 0.26087
L_MODE median confidence-positive fraction:        0
```

and in missingness/diagnostic quality:

```text
H_MODE_STABLE median Q_diag:                 1
H_MODE_STABLE median P_missing_critical:     0
L_MODE median Q_diag:                        0.06
L_MODE median P_missing_critical:            1
```

## Within-shot L/H recovery

| shot_id | L_MODE_m_edge_conf_median | LH_TRANSITION_m_edge_conf_median | H_MODE_STABLE_m_edge_conf_median | delta_H_minus_L_m_edge_conf_median | L_MODE_conf_positive_fraction | H_MODE_STABLE_conf_positive_fraction | delta_H_minus_L_conf_positive_fraction |
|---|---|---|---|---|---|---|---|
| 12007 | -1.12 | -0.174448 | -0.038158 | 1.08184 | 0 | 0 | 0 |
| 12017 | -1.12 | -0.0301809 | -0.0580491 | 1.06195 | 0 | 0 | 0 |
| 12046 | -1.12 | -0.498215 | 0.205992 | 1.32599 | 0 | 0.514493 | 0.514493 |
| 12055 | -1.12 | -0.264874 | 0.195762 | 1.31576 | 0 | 0.481481 | 0.481481 |
| 12063 | -1.12 | -0.313209 | 0.0525031 | 1.1725 | 0 | 0.26087 | 0.26087 |

### Interpretation

For every shot where both `L_MODE` and `H_MODE_STABLE` are present, the recovered `H_MODE_STABLE` window has a higher `m_edge_conf` median than the L-mode window.

The recovered within-shot H-minus-L deltas are all positive:

```text
12007: +1.08184
12017: +1.06195
12046: +1.32599
12055: +1.31576
12063: +1.17250
```

This is the strongest result of the v0.2 gate, because it compares windows within the same shot rather than only across shots.

## What this establishes

This gate establishes that, after conservative relabeling and diagnostic-confidence correction, a small internally supported set of `H_MODE_STABLE` windows aligns with the UNNS-H Mode edge-margin direction.

In plain terms:

```text
physically recovered H-mode-stable windows sit higher in m_edge_conf
than L-mode windows from the same shots.
```

That is a meaningful recovery of the H-mode-stable evidence that v0.1 had intentionally suppressed.

## What this does not establish

This does not yet establish broad H-mode validation.

The result is still bounded by three limits:

1. the recovered H-mode windows are internally supported, not externally anchored;
2. the panel remains small;
3. the signal proxies are derived from TokaMark-accessible arrays, not from a full expert-reviewed plasma reconstruction.

Therefore the correct claim is:

```text
v0.2 passes the first physical-window recovery gate.
```

not:

```text
UNNS has validated H-mode.
```

## Decision

Proceed.

The recovery is strong enough to continue, but not strong enough to publish as final validation.

## Next gate

The next gate should be external anchoring or falsification stress testing.

Preferred next document:

```text
docs/
  34_EXTERNAL_H_MODE_ANCHORING_OR_FALSIFICATION_PLAN.md
```

Recommended next actions:

1. Search for shot-log, publication, or expert reference timing for the recovered shots:
   `12007`, `12017`, `12046`, `12055`, `12063`.
2. If external timing exists, promote only matching windows to `3_EXTERNALLY_ANCHORED`.
3. If no external timing exists, run a falsification panel: comparable diagnostic-complete shots where no stable H-mode should be expected.
4. Do not revise the formula yet; the present gate passed.
