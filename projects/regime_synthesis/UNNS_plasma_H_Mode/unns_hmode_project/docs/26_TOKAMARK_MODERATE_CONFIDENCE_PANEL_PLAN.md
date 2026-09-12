# TokaMark Moderate Confidence Panel Plan — UNNS-H Mode Project

## 1. Purpose

This document defines the next controlled validation step for the UNNS-H Mode project after the diagnostic-confidence revision passed the initial five-shot panel.

It belongs here:

```text
unns_hmode_project/
  docs/
    26_TOKAMARK_MODERATE_CONFIDENCE_PANEL_PLAN.md
```

It follows:

```text
docs/
  25_TOKAMARK_M_EDGE_CONFIDENCE_REVISION_RESULTS.md
```

The purpose of this document is to prevent another uncontrolled expansion. The next step is not a blind full-corpus scan, not a public claim, and not another formula revision. The next step is a moderate, balanced panel designed to test whether the v0.2 diagnostic-confidence method remains sane beyond the hand-checked five-shot set.

---

## 2. Current status

The project has reached this state:

```text
v0.1 raw m_edge(t):
  useful exploratory signal
  unsafe for scaling because incomplete shots can appear artificially positive

v0.2 confidence correction:
  preserves m_edge_raw(t)
  adds diagnostic confidence Q_diag(t)
  adds critical-missing penalty P_missing_critical(t)
  computes confidence-weighted m_edge_conf(t)
  passed the initial five-shot panel

Initial five-shot result:
  12063 remains confidence-ranked first
  11776 and 11768 are suppressed
  11876 is confidence-limited by missing Thomson profiles
  11830 remains weaker due to missing soft-X edge support
```

The next question is:

> Does v0.2 remain structurally sane on a larger, balanced, non-hand-picked panel?

---

## 3. What this step is not

This step is not physical H-mode validation.

It is not proof of the L-H transition mechanism.

It is not a full TokaMark scan.

It is not a public-facing result.

It is not a manuscript-ready claim.

It is a controlled intermediate test of the confidence-corrected UNNS-H Mode margin.

---

## 4. Central test question

The moderate panel must answer:

> When diagnostic confidence is applied, do confidence-positive structures concentrate in diagnostically complete or physically plausible candidates, while incomplete / low-priority candidates are suppressed?

This is the next necessary gate before any broader scaling.

---

## 5. Panel size

Use a moderate panel of:

```text
20–50 TokaMark shots
```

Recommended first run:

```text
30 shots
```

This is large enough to test whether the initial five-shot behavior generalizes, but small enough to inspect failures manually.

Do not exceed 50 shots in this stage.

---

## 6. Panel composition

The panel should be balanced by candidate class.

Recommended 30-shot composition:

```text
6 FULL_PROFILE_EDGE_CANDIDATE
6 PROFILE_DALPHA_CANDIDATE
6 CORE_DALPHA_GEOMETRY_CANDIDATE
6 PARTIAL_DALPHA_CANDIDATE
6 LOW_PRIORITY / weak controls
```

If a class has fewer available or array-readable cases, the selector should record the shortage and fill only from the nearest weaker class.

The selector must not simply pick the top 30 by score.

---

## 7. Candidate classes and intended roles

### 7.1 FULL_PROFILE_EDGE_CANDIDATE

Role:

```text
positive / high-confidence candidate class
```

Expected behavior:

```text
higher Q_diag
lower P_missing_critical
possible nonzero confidence-positive windows
enrichment near the top of confidence-adjusted ranking
```

This class should not all become positive. But it should be enriched among the strongest cases if v0.2 is meaningful.

### 7.2 PROFILE_DALPHA_CANDIDATE

Role:

```text
profile-supported but soft-X-limited comparison class
```

Expected behavior:

```text
moderate or high Q_diag
soft-X penalty visible
confidence-positive fraction lower than full profile-edge class
```

This class tests whether profile availability alone is insufficient.

### 7.3 CORE_DALPHA_GEOMETRY_CANDIDATE

Role:

```text
edge/geometry-supported but profile-limited comparison class
```

Expected behavior:

```text
edge activity visible
profile confidence reduced
transport confidence limited
confidence-positive windows rare or reduced
```

This class tests whether edge activity without Thomson profiles is confidence-limited.

### 7.4 PARTIAL_DALPHA_CANDIDATE

Role:

```text
partial / incomplete stress-test class
```

Expected behavior:

```text
raw m_edge may appear positive
m_edge_conf should suppress inflated positive intervals
Q_diag lower than complete classes
P_missing_critical higher than complete classes
```

### 7.5 LOW_PRIORITY / weak controls

Role:

```text
negative / missingness stress-test class
```

Expected behavior:

```text
mostly low confidence or confidence-negative
near-zero confidence-positive fraction
high P_missing_critical
low ranking
```

If this class frequently becomes confidence-positive, v0.2 fails.

---

## 8. Required selector component

The next component should be:

```text
components/
  tokamark_confidence_panel_selector.py
```

Its job is to select a balanced panel from:

```text
outputs/reports/
  tokamark_positive_corridor_metadata_candidates.csv
```

It should output:

```text
outputs/reports/
  tokamark_moderate_confidence_panel_selection.csv
  tokamark_moderate_confidence_panel_selection.json
  tokamark_moderate_confidence_panel_selection.md
```

The selector should support:

```powershell
python components\tokamark_confidence_panel_selector.py ^
  --metadata outputs\reports\tokamark_positive_corridor_metadata_candidates.csv ^
  --per-class 6 ^
  --out-dir outputs\reports
```

Optional:

```powershell
python components\tokamark_confidence_panel_selector.py ^
  --metadata outputs\reports\tokamark_positive_corridor_metadata_candidates.csv ^
  --panel-size 30 ^
  --out-dir outputs\reports
```

---

## 9. Selection rules

The selector should use explicit rules.

### 9.1 Preserve class balance

Select approximately equal numbers from each class.

Do not select only highest-score shots.

### 9.2 Prefer array-readability

Prefer candidates whose metadata was successfully fetched and whose key arrays are likely present.

### 9.3 Avoid duplicate overconcentration

Avoid selecting only adjacent shots from the same local run unless needed.

If possible, distribute by:

```text
shot_id range
campaign
split membership
candidate class
```

### 9.4 Include reference shot 12063

Always include:

```text
12063
```

It should be marked as:

```text
reference_anchor
```

It should not be the only success condition.

### 9.5 Include known stress cases

Include the five already analyzed shots as calibration anchors:

```text
12063
11830
11876
11768
11776
```

These allow comparison between the initial panel and the moderate panel.

### 9.6 Record why each shot was selected

The selection output must include:

```text
shot_id
candidate_class
candidate_score
selection_role
selection_reason
core_required_present
profile_preferred_present
edge_activity_present
supporting_present
missing_core_required
missing_profile_preferred
missing_edge_activity
```

---

## 10. Required runner behavior

After selection, the workflow should run the existing pipeline.

For each selected shot:

```text
1. tokamark_one_shot_array_probe.py
2. tokamark_m_edge_t_probe.py
3. tokamark_m_edge_trace_inspector.py
4. tokamark_m_edge_confidence_revision.py
```

The moderate-panel runner may be either:

```text
A. a new orchestration script
```

or:

```text
B. the existing scripts run in sequence using the selected shot list
```

Do not create a new margin formula.

Do not revise v0.2 during the panel.

The v0.2 method must be frozen for this test.

---

## 11. Recommended runner component

If automation is needed, create:

```text
components/
  tokamark_moderate_confidence_panel_runner.py
```

It should read:

```text
outputs/reports/
  tokamark_moderate_confidence_panel_selection.csv
```

and produce:

```text
outputs/reports/
  tokamark_moderate_confidence_panel_results.csv
  tokamark_moderate_confidence_panel_results.json
  tokamark_moderate_confidence_panel_results.md
```

The runner should skip already existing per-shot files unless `--force` is used.

Suggested command:

```powershell
python components\tokamark_moderate_confidence_panel_runner.py ^
  --selection outputs\reports\tokamark_moderate_confidence_panel_selection.csv ^
  --out-dir outputs\reports
```

---

## 12. Required panel-level metrics

The moderate panel report must include these metrics.

### 12.1 Ranking metrics

```text
confidence_panel_rank
confidence_structural_score
candidate_class
candidate_score
```

### 12.2 Raw versus confidence metrics

```text
raw_positive_fraction
conf_positive_fraction
raw_negative_fraction
conf_negative_fraction
raw m_edge median
confidence m_edge median
delta_conf_minus_raw median
```

### 12.3 Diagnostic confidence metrics

```text
Q_diag_median
Q_diag_mean
Q_diag_min
conf_low_confidence_fraction
P_missing_critical_median
```

### 12.4 Class-level summaries

For each candidate class:

```text
count
median Q_diag
median P_missing_critical
median conf_positive_fraction
median confidence_structural_score
fraction with conf_positive_fraction > 0
fraction with low-confidence fraction > 0.25
```

### 12.5 Failure distribution

Report how many shots fail due to:

```text
array download / read failure
missing m_edge input
no finite m_edge
no finite Q_diag
all low-confidence
unexpected exception
```

---

## 13. Acceptance criteria

v0.2 is strengthened if the moderate panel shows:

```text
1. FULL_PROFILE_EDGE_CANDIDATE shots are enriched near the top ranks.
2. LOW_PRIORITY shots are suppressed or low-confidence flagged.
3. PARTIAL_DALPHA_CANDIDATE shots rarely become confidence-positive.
4. Confidence-positive windows mostly occur where Q_diag is moderate/high.
5. P_missing_critical is low for top-ranked cases.
6. The known anchor 12063 remains strong but is not the only plausible strong case.
7. Raw-positive inflation is reduced in incomplete classes.
```

The key condition is not that `12063` must always be number one. The key condition is that the confidence-adjusted ranking must make diagnostic and structural sense.

---

## 14. Failure criteria

v0.2 is weakened if the moderate panel shows:

```text
1. LOW_PRIORITY shots frequently become confidence-positive.
2. PARTIAL_DALPHA_CANDIDATE shots dominate top ranks.
3. FULL_PROFILE_EDGE_CANDIDATE shots are not enriched among top ranks.
4. Confidence-positive windows occur mostly at low Q_diag.
5. Rankings are dominated by missingness artifacts.
6. P_missing_critical is high among top-ranked cases.
7. Results depend mostly on metadata class rather than time-resolved evidence.
8. Many shots fail due to array access or preprocessing limitations.
```

If these occur, the project should stop as a bounded pilot rather than scale further.

---

## 15. Manual review requirement

The moderate panel must include a manual review of the top and bottom cases.

Review at minimum:

```text
top 5 confidence-ranked shots
bottom 5 confidence-ranked shots
all confidence-positive shots
all LOW_PRIORITY shots with nonzero confidence-positive fraction
all shots where raw positive fraction > 0.5 but confidence-positive fraction = 0
```

This prevents the panel from becoming another black-box ranking.

---

## 16. Output document after running the panel

After the moderate panel is run, produce:

```text
docs/
  27_TOKAMARK_MODERATE_CONFIDENCE_PANEL_RESULTS.md
```

That document should answer:

> Does the diagnostic-confidence revision remain stable and meaningful on a balanced 20–50 shot panel?

It should not claim physical H-mode validation.

---

## 17. Relation to the original UNNS-H Mode program

This step brings the project back toward the original research program.

The original goal was not to generate many scripts. It was to test whether UNNS features separate meaningful plasma regimes better than raw parameters alone.

The moderate confidence panel is a necessary bridge:

```text
from:
  one-shot structural behavior

to:
  class-balanced empirical behavior

before:
  physically labeled L/H/ELM validation
```

Only after the moderate panel passes should the project consider true physical-window validation.

---

## 18. What comes after a passed moderate panel

If the moderate panel passes, the next valid step would be:

```text
docs/
  28_PHYSICAL_WINDOW_LABELING_REQUIREMENTS.md
```

That would define what is needed to move from structural candidates to physically labeled windows:

```text
L-mode interval
L-H transition interval
stable H-mode interval
pre-ELM interval
post-ELM interval
H-L back transition
```

At that point the project would return directly to the original H-mode question.

---

## 19. What comes after a failed moderate panel

If the moderate panel fails, the correct response is not another correction loop.

The correct response is:

```text
freeze the current work as an exploratory pilot
document the failure modes
do not scale
do not claim validation
```

The pilot would still be valuable because it would have shown:

```text
how to construct m_edge(t)
how diagnostic incompleteness affects structural margins
where the UNNS interpretation becomes fragile
what plasma data is actually needed
```

---

## 20. Implementation boundary

The selector and runner may be created after this plan.

No new formal variables should be added during the moderate panel.

Frozen method for this stage:

```text
m_edge_raw(t)
Q_diag(t)
P_missing_critical(t)
m_edge_conf(t)
m_edge_conf_state
confidence_structural_score
```

Any new quantity must wait until after `27_TOKAMARK_MODERATE_CONFIDENCE_PANEL_RESULTS.md`.

---

## 21. Final decision statement

The next step is a moderate balanced confidence panel, not broad scaling.

The v0.2 diagnostic-confidence correction passed the first five-shot test. That makes it worthy of a larger controlled panel, but not worthy of physical validation claims.

The moderate panel must test whether confidence-positive behavior is enriched in diagnostically complete cases and suppressed in incomplete cases. If it passes, the project can move toward physical-window labeling. If it fails, the project should stop as a bounded pilot study.

This plan is the gate between exploratory method-building and serious empirical validation.
