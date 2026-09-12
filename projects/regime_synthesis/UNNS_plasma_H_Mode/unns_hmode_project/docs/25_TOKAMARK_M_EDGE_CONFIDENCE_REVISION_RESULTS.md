# TokaMark m_edge Diagnostic-Confidence Revision Results

## 1. Purpose

This document reports the first results of the diagnostic-confidence correction to the UNNS-H Mode `m_edge(t)` pipeline.

It belongs here:

```text
unns_hmode_project/
  docs/
    25_TOKAMARK_M_EDGE_CONFIDENCE_REVISION_RESULTS.md
```

It follows:

```text
docs/
  24_DIAGNOSTIC_CONFIDENCE_REVISION_PLAN.md
```

The purpose of this step was precise:

> Preserve the raw v0.1 `m_edge(t)` margin, add diagnostic confidence, and test whether incomplete shots that looked artificially positive are suppressed without erasing the stronger structure of shot `12063`.

This report does not claim physical H-mode validation.

---

## 2. Input panel

The same five-shot panel was retested:

```text
12063  FULL_PROFILE_EDGE_CANDIDATE        reference
11830  PROFILE_DALPHA_CANDIDATE          profile/no-softX comparison
11876  CORE_DALPHA_GEOMETRY_CANDIDATE    core+softX/no-Thomson comparison
11768  PARTIAL_DALPHA_CANDIDATE          partial comparison
11776  LOW_PRIORITY                      weak / stress-test comparison
```

The component used was:

```text
components/
  tokamark_m_edge_confidence_revision.py
```

The output files were:

```text
outputs/reports/
  tokamark_confidence_panel_comparison.csv
  tokamark_confidence_panel_comparison.json
  tokamark_confidence_panel_comparison.md
```

Per-shot outputs were also produced:

```text
outputs/reports/
  tokamark_shot_<SHOT>_m_edge_confidence_revision.csv
  tokamark_shot_<SHOT>_m_edge_confidence_revision.json
  tokamark_shot_<SHOT>_m_edge_confidence_revision.md
```

---

## 3. Decision

The confidence revision returned:

```text
decision: confidence_revision_passes_initial_panel
reference shot: 12063
reference confidence rank: 1
reference confidence-positive fraction: 0.169014
max comparison confidence-positive fraction: 0
reference Q_diag median: 0.888889
incomplete cases suppressed: True
```

Decision reasons:

```text
- reference_has_top_confidence_adjusted_rank
- reference_has_highest_or_tied_confidence_positive_fraction
- reference_has_highest_confidence_structural_score
- reference_remains_interpretable_after_confidence_correction
- incomplete_inflated_cases_are_confidence_limited_or_suppressed
```

This is the first correction result that satisfies the methodological requirement set in document `24`.

---

## 4. Confidence-adjusted ranking

|   confidence_panel_rank |   shot_id | candidate_class                |   confidence_structural_score |   raw_positive_fraction |   conf_positive_fraction |   raw_negative_fraction |   conf_negative_fraction |   conf_low_confidence_fraction |   m_edge_raw_median |   m_edge_conf_median |   Q_diag_median |   P_missing_critical_median | missing_core_required                                                     | missing_profile_preferred                     | missing_edge_activity                                             |
|------------------------:|----------:|:-------------------------------|------------------------------:|------------------------:|-------------------------:|------------------------:|-------------------------:|-------------------------------:|--------------------:|---------------------:|----------------:|----------------------------:|:--------------------------------------------------------------------------|:----------------------------------------------|:------------------------------------------------------------------|
|                       1 |     12063 | FULL_PROFILE_EDGE_CANDIDATE    |                       2.11139 |                0.258216 |                 0.169014 |                0.112676 |                 0.215962 |                       0.138498 |           0.087961  |           -0.0217341 |        0.888889 |                   0.0111111 | nan                                                                       | nan                                           | nan                                                               |
|                       2 |     11830 | PROFILE_DALPHA_CANDIDATE       |                      -6.4816  |                0.226064 |                 0        |                0.228723 |                 0.510638 |                       0.154255 |          -0.0366668 |           -0.322615  |        0.863889 |                   0.111111  | nan                                                                       | nan                                           | soft_x_rays-horizontal_cam_lower;soft_x_rays-horizontal_cam_upper |
|                       3 |     11876 | CORE_DALPHA_GEOMETRY_CANDIDATE |                      -7.80769 |                0.216015 |                 0        |                0.165736 |                 0.55121  |                       0.113594 |           0.0156955 |           -0.27706   |        0.738889 |                   0.411111  | nan                                                                       | thomson_scattering-t_e;thomson_scattering-n_e | nan                                                               |
|                       4 |     11768 | PARTIAL_DALPHA_CANDIDATE       |                      -8.0591  |                0.533654 |                 0        |                0.230769 |                 0.480769 |                       0.139423 |           0.372648  |           -0.255289  |        0.593333 |                   0.616667  | summary-power_nbi                                                         | thomson_scattering-t_e;thomson_scattering-n_e | nan                                                               |
|                       5 |     11776 | LOW_PRIORITY                   |                     -13.6066  |                0.659656 |                 0        |                0.156788 |                 0.650096 |                       0.349904 |           0.486177  |           -0.48441   |        0.462778 |                   0.872222  | summary-power_nbi;spectrometer_visible-filter_spectrometer_dalpha_voltage | thomson_scattering-t_e;thomson_scattering-n_e | nan                                                               |

The confidence-adjusted ranking is now methodologically cleaner than the raw v0.1 panel:

```text
rank 1: 12063  FULL_PROFILE_EDGE_CANDIDATE
rank 2: 11830  PROFILE_DALPHA_CANDIDATE
rank 3: 11876  CORE_DALPHA_GEOMETRY_CANDIDATE
rank 4: 11768  PARTIAL_DALPHA_CANDIDATE
rank 5: 11776  LOW_PRIORITY
```

The most important result is that `12063` is the only shot in this panel with nonzero confidence-positive fraction.

---

## 5. Diagnostic coverage table

|   shot_id | candidate_class                |   loaded_signal_arrays |   failed_signal_arrays |   core_required_present |   profile_preferred_present |   edge_activity_present |   supporting_present |   Q_diag_median |   P_missing_critical_median | missing_core_required                                                     | missing_profile_preferred                     | missing_edge_activity                                             |
|----------:|:-------------------------------|-----------------------:|-----------------------:|------------------------:|----------------------------:|------------------------:|---------------------:|----------------:|----------------------------:|:--------------------------------------------------------------------------|:----------------------------------------------|:------------------------------------------------------------------|
|     11768 | PARTIAL_DALPHA_CANDIDATE       |                     13 |                      3 |                       7 |                           0 |                       2 |                    9 |        0.593333 |                   0.616667  | summary-power_nbi                                                         | thomson_scattering-t_e;thomson_scattering-n_e | nan                                                               |
|     11776 | LOW_PRIORITY                   |                     12 |                      4 |                       6 |                           0 |                       2 |                    9 |        0.462778 |                   0.872222  | summary-power_nbi;spectrometer_visible-filter_spectrometer_dalpha_voltage | thomson_scattering-t_e;thomson_scattering-n_e | nan                                                               |
|     11830 | PROFILE_DALPHA_CANDIDATE       |                     14 |                      2 |                       8 |                           2 |                       0 |                    9 |        0.863889 |                   0.111111  | nan                                                                       | nan                                           | soft_x_rays-horizontal_cam_lower;soft_x_rays-horizontal_cam_upper |
|     11876 | CORE_DALPHA_GEOMETRY_CANDIDATE |                     14 |                      2 |                       8 |                           0 |                       2 |                   10 |        0.738889 |                   0.411111  | nan                                                                       | thomson_scattering-t_e;thomson_scattering-n_e | nan                                                               |
|     12063 | FULL_PROFILE_EDGE_CANDIDATE    |                     16 |                      0 |                       8 |                           2 |                       2 |                   10 |        0.888889 |                   0.0111111 | nan                                                                       | nan                                           | nan                                                               |

This table explains why the confidence revision changed the interpretation. The weaker and incomplete candidates are not merely lower-ranked by class; they are penalized because specific missing diagnostic families reduce interpretability.

---

## 6. Result for reference shot 12063

Shot `12063` remains the strongest case after confidence correction.

```text
candidate class: FULL_PROFILE_EDGE_CANDIDATE
confidence rank: 1
confidence structural score: 2.11139
raw positive fraction: 0.258216
confidence-positive fraction: 0.169014
raw negative fraction: 0.112676
confidence-negative fraction: 0.215962
raw m_edge median: 0.087961
confidence m_edge median: -0.0217341
Q_diag median: 0.888889
P_missing_critical median: 0.0111111
```

The correction reduced `12063`:

```text
raw positive fraction:
  0.258216

confidence-positive fraction:
  0.169014
```

This is good. The correction did not blindly preserve the reference. It made the result more conservative while still preserving a nonzero confidence-positive structure.

The median confidence score remains high:

```text
Q_diag median: 0.888889
```

and the critical missing penalty remains very low:

```text
P_missing_critical median: 0.0111111
```

This is the main reason `12063` remains interpretable.

---

## 7. Suppression of shot 11776

Shot `11776` was the most important stress test because raw v0.1 made it look strongly positive despite its weak diagnostic class.

Before confidence correction:

```text
raw positive fraction: 0.659656
raw m_edge median: 0.486177
```

After confidence correction:

```text
confidence-positive fraction: 0
confidence-negative fraction: 0.650096
confidence low-confidence fraction: 0.349904
confidence m_edge median: -0.48441
Q_diag median: 0.462778
P_missing_critical median: 0.872222
```

Missing diagnostics:

```text
missing_core_required:
  summary-power_nbi;spectrometer_visible-filter_spectrometer_dalpha_voltage

missing_profile_preferred:
  thomson_scattering-t_e;thomson_scattering-n_e
```

This is exactly the desired behavior. The low-priority shot no longer masquerades as strongly positive. Its confidence-positive fraction falls to zero and its critical-missing penalty becomes high.

---

## 8. Suppression of shot 11768

Shot `11768` was another incomplete case that looked too positive under raw v0.1.

Before correction:

```text
raw positive fraction: 0.533654
raw m_edge median: 0.372648
```

After correction:

```text
confidence-positive fraction: 0
confidence-negative fraction: 0.480769
confidence m_edge median: -0.255289
Q_diag median: 0.593333
P_missing_critical median: 0.616667
```

Missing diagnostics:

```text
missing_core_required:
  summary-power_nbi

missing_profile_preferred:
  thomson_scattering-t_e;thomson_scattering-n_e
```

Again, this is the desired correction. The raw positive fraction was inflated by incomplete evidence; the confidence-adjusted margin suppresses it.

---

## 9. Confidence-limiting shot 11876

Shot `11876` remains structurally active but is now confidence-limited.

```text
candidate class: CORE_DALPHA_GEOMETRY_CANDIDATE
raw positive fraction: 0.216015
confidence-positive fraction: 0
confidence-negative fraction: 0.55121
raw m_edge median: 0.0156955
confidence m_edge median: -0.27706
Q_diag median: 0.738889
P_missing_critical median: 0.411111
```

Missing diagnostics:

```text
missing_profile_preferred:
  thomson_scattering-t_e;thomson_scattering-n_e
```

This is also consistent with the plan. Shot `11876` has edge and soft-X support, but lacks Thomson profiles. The confidence revision therefore does not discard it as unusable, but it prevents it from competing with the fully diagnostic reference.

---

## 10. Weakness of shot 11830 preserved

Shot `11830` remains weaker than `12063`.

```text
candidate class: PROFILE_DALPHA_CANDIDATE
raw positive fraction: 0.226064
confidence-positive fraction: 0
confidence-negative fraction: 0.510638
raw m_edge median: -0.0366668
confidence m_edge median: -0.322615
Q_diag median: 0.863889
P_missing_critical median: 0.111111
```

Missing diagnostics:

```text
missing_edge_activity:
  soft_x_rays-horizontal_cam_lower;soft_x_rays-horizontal_cam_upper
```

This confirms that profile availability alone is insufficient. Without soft-X edge support, the confidence-weighted margin becomes non-positive.

---

## 11. What the revision establishes

The confidence revision establishes five things.

### 11.1 The raw v0.1 margin was useful but unsafe

Raw v0.1 produced a real structural signal, but incomplete shots could look artificially positive.

### 11.2 The confidence layer solves the immediate panel flaw

The incomplete inflated cases were suppressed:

```text
11776 confidence-positive fraction: 0
11768 confidence-positive fraction: 0
```

### 11.3 The reference was not preserved automatically

Shot `12063` was also reduced:

```text
12063 raw positive fraction: 0.258216
12063 confidence-positive fraction: 0.169014
```

That makes the correction more credible.

### 11.4 Shot 12063 remains interpretable

Shot `12063` remains the only confidence-positive shot in the panel, with high median diagnostic confidence and very low critical-missing penalty.

### 11.5 The project can now cautiously continue

The immediate methodological bottleneck has been addressed on the initial panel.

---

## 12. What this does not establish

This result still does not prove H-mode origin.

It does not identify the true L-H transition time.

It does not prove that confidence-positive windows are physically H-mode windows.

It does not validate confinement improvement.

It does not compare against standard plasma-physics predictors.

It does not establish cross-machine generality.

It does not justify scaling to all available shots yet.

The bounded claim is:

> The diagnostic-confidence revision passes the initial five-shot TokaMark panel: it preserves shot `12063` as the strongest confidence-adjusted case while suppressing incomplete inflated cases.

---

## 13. Decision

The correct decision after this result is:

```text
v0.1 raw margin: freeze as audit layer
confidence revision: retain as v0.2 candidate
initial five-shot confidence test: passed
physical validation: not yet
broader scaling: allowed only cautiously
```

The next step should not be a blind scan of thousands of shots.

The next step should be a **moderate validation panel**:

```text
20–50 TokaMark shots
balanced by diagnostic class
including full-profile-edge, profile-only, edge-only, partial, and low-priority candidates
```

The purpose is to see whether v0.2 remains sane outside the hand-selected five-shot panel.

---

## 14. Recommended next technical step

Create a moderate panel selector/runner, not a full scan.

Suggested component:

```text
components/
  tokamark_confidence_panel_selector.py
```

It should select a balanced panel from the metadata candidates:

```text
5–10 FULL_PROFILE_EDGE_CANDIDATE
5–10 PROFILE_DALPHA_CANDIDATE
5–10 CORE_DALPHA_GEOMETRY_CANDIDATE
5–10 PARTIAL_DALPHA_CANDIDATE
5–10 LOW_PRIORITY / weak controls
```

Then run the existing confidence revision on that panel.

The next project document should be:

```text
docs/
  26_TOKAMARK_MODERATE_CONFIDENCE_PANEL_PLAN.md
```

not a public article and not a physical validation claim.

---

## 15. Failure conditions for the next panel

The v0.2 confidence revision should be considered weakened if:

```text
low-priority cases frequently reappear as confidence-positive
full-profile-edge candidates are not enriched among top-ranked cases
confidence-positive windows occur mostly in low-Q_diag periods
rankings are dominated by missingness artifacts
the result cannot distinguish edge-complete cases from incomplete cases
```

It should be considered strengthened if:

```text
confidence-positive cases are enriched among diagnostically complete candidates
partial / low-priority cases are usually suppressed or confidence-limited
raw margin and confidence-adjusted margin remain auditable
the reference behavior of 12063 is not isolated but not universal
```

---

## 16. Project status update

```text
TCV event-level model:                       complete
TCV full-corpus extension:                   complete
TokaMark metadata access:                    complete
TokaMark one-shot array probe:               complete
TokaMark raw m_edge(t) v0.1:                 complete
TokaMark trace inspection:                   complete
TokaMark cross-shot comparison:              complete
TokaMark five-shot raw panel:                complete
Diagnostic-confidence plan:                  complete
Diagnostic-confidence revision implementation: complete
Initial confidence-adjusted five-shot panel: passed
Current model status:                        v0.2 candidate
Physical H-mode validation:                  not yet
Next allowed step:                           moderate balanced panel
```

---

## 17. Final synthesis statement

The diagnostic-confidence revision is the first point in the UNNS-H Mode project where the methodology becomes materially stronger rather than merely more elaborate.

The raw v0.1 margin produced a plausible signal but was unsafe because incomplete diagnostics could inflate positive boundary margins. The v0.2 confidence correction fixes this flaw on the initial five-shot panel. It preserves `12063` as the strongest confidence-adjusted case, reduces its positive fraction conservatively, suppresses incomplete inflated cases, and produces a more credible ranking.

The result is still not physical validation. It is, however, a valid methodological advance. The project can now proceed only to a moderate, balanced confidence panel. It should not jump to public claims or full-corpus scaling.
