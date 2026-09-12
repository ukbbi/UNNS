# Physical-Window Label Hardening Plan — UNNS-H Mode Project

## 1. Purpose

This document defines the next gate after the first physical-window alignment test passed.

It belongs here:

```
unns_hmode_project/
  docs/
    30_PHYSICAL_WINDOW_LABEL_HARDENING_PLAN.md
```

It follows:

```
docs/
  29_PHYSICAL_WINDOW_LABELING_RESULTS.md
```

The previous stage showed a promising first-gate alignment:

```
L_MODE < LH_TRANSITION < H_MODE_STABLE
```

under the v0.2 confidence-corrected UNNS-H Mode margin:

```
m_edge_conf(t)
```

However, the labels used in that first comparison were still provisional. The purpose of this document is to define how to harden those labels before making any stronger physical claim.

---

## 2. Current status

The project has reached this state:

```
v0.1 raw m_edge(t):                         complete
v0.2 diagnostic-confidence correction:      complete
five-shot confidence panel:                 passed
30-shot moderate confidence panel:          passed
physical-window label template:             complete
edited physical-window label draft:         complete
physical-window analysis first gate:        passed
current status:                             provisionally physically aligned
final H-mode validation:                    not yet
```

The first-gate physical-window result was:

```
eligible windows: 17
excluded windows: 72

L_MODE:        6
LH_TRANSITION: 6
H_MODE_STABLE: 5
```

The result was directionally correct, but not yet hardened enough for final validation.

---

## 3. Why label hardening is needed

The first-gate result is promising, but several weaknesses remain:

```text
H_MODE_STABLE windows were low-confidence post-transition candidates.
L_MODE windows had very low Q_diag and high P_missing_critical.
Some later physical marker windows remained AMBIGUOUS.
TokaMark signals may be normalized or preprocessed.
The labels were generated from a conservative rule, not expert plasma annotation.
No external L-H transition timing was used.
```

Therefore, the next goal is not to change the UNNS formula.

The next goal is to improve the physical labels.

---

## 4. Central question

The label-hardening gate asks:

> Do the provisional physical labels survive stricter physical review using D-alpha morphology, profile-gradient behavior, soft-X response, power/density context, and rejection of ambiguous intervals?

The purpose is to separate:

```
structurally convenient labels
```

from:

```
physically defensible labels
```

---

## 5. Label-hardening principle

The UNNS score must not decide the label.

The physical label must be decided first.

Correct logic:

```
D-alpha / profile / soft-X / power / density review
→ hardened physical label
→ compare hardened labels with m_edge_conf(t)
```

Incorrect logic:

```
m_edge_conf(t)
→ choose H_MODE_STABLE window
→ claim physical agreement
```

This rule must remain strict.

---

## 6. Hardening levels

Each window should be assigned a hardening level.

### 6.1 Level 0 — provisional

Definition:

```
label assigned by first-pass template or simple marker logic
```

Use:

```
for review only
not sufficient for strong validation
```

### 6.2 Level 1 — physically plausible

Definition:

```
label is supported by at least one independent physical diagnostic
```

Examples:

```
D-alpha sharp change supports LH_TRANSITION
quiet post-transition D-alpha behavior supports H_MODE_STABLE candidate
pre-transition baseline supports L_MODE
```

Use:

```
acceptable for exploratory physical-window comparison
```

### 6.3 Level 2 — physically supported

Definition:

```
label is supported by at least two independent physical diagnostic families
```

Examples:

```
D-alpha change + profile-gradient change
D-alpha suppression + soft-X consistency
profile-gradient steepening + density/power context
```

Use:

```
acceptable for stronger internal validation
```

### 6.4 Level 3 — externally anchored

Definition:

```
label is supported by independent published timing, expert annotation, shot log, or standard plasma analysis
```

Use:

```
required before strong H-mode validation claims
```

---

## 7. Required hardening fields

Create a hardened label file:

```
outputs/reports/
  tokamark_physical_window_labels_HARDENED_v0_1.csv
```

Required columns:

```
shot_id
window_id
original_label_type
hardened_label_type
t_start
t_end
hardening_level
label_confidence
dalpha_evidence
profile_evidence
softx_evidence
power_density_context
geometry_context
external_reference
review_decision
reviewer_notes
excluded_from_validation
exclusion_reason
```

Allowed `hardened_label_type` values:

```
L_MODE
LH_TRANSITION
H_MODE_STABLE
PRE_ELM
POST_ELM
HL_BACK_TRANSITION
AMBIGUOUS
UNLABELABLE
REJECTED
```

Allowed `hardening_level` values:

```
0_PROVISIONAL
1_PLAUSIBLE
2_SUPPORTED
3_EXTERNALLY_ANCHORED
```

Allowed `review_decision` values:

```
ACCEPT
DOWNGRADE
REJECT
KEEP_AMBIGUOUS
KEEP_UNLABELABLE
NEEDS_EXTERNAL_REFERENCE
```

---

## 8. Evidence requirements by label

### 8.1 L_MODE

Minimum evidence:

```
pre-transition interval
no clear post-transition barrier behavior
D-alpha not yet in suppressed / altered post-transition state
```

Stronger evidence:

```
weaker edge-gradient proxy than later interval
higher turbulence / edge activity if available
physically plausible pre-transition power and density context
```

Hardening rule:

```
L_MODE should not be accepted solely because it is early in time.
```

### 8.2 LH_TRANSITION

Minimum evidence:

```
localized D-alpha change or edge-emission change
finite transition interval
occurs after a baseline interval
```

Stronger evidence:

```
profile-gradient change near the same interval
soft-X or edge activity response
power/density context does not contradict transition
```

Hardening rule:

```
LH_TRANSITION requires a localized event, not a broad arbitrary window.
```

### 8.3 H_MODE_STABLE

Minimum evidence:

```
post-transition interval
D-alpha behavior differs from pre-transition baseline
no immediate disruptive marker
```

Stronger evidence:

```
sustained edge-gradient / pedestal-like proxy
soft-X consistency
reduced fragmentation relative to transition window
not simply a high-Q_diag region selected by UNNS
```

Hardening rule:

```
H_MODE_STABLE cannot be accepted solely because m_edge_conf is positive.
```

### 8.4 PRE_ELM

Minimum evidence:

```
edge activity buildup before burst-like event
```

Stronger evidence:

```
D-alpha or soft-X burst follows
profile or edge response indicates buildup
```

Hardening rule:

```
Do not assign PRE_ELM without a subsequent event.
```

### 8.5 POST_ELM

Minimum evidence:

```
burst-like event followed by relaxation/recovery
```

Stronger evidence:

```
D-alpha burst and decay
soft-X response
edge-gradient relaxation
```

Hardening rule:

```
Do not assign POST_ELM unless the burst/recovery structure is visible.
```

### 8.6 HL_BACK_TRANSITION

Minimum evidence:

```
loss of post-transition edge-barrier behavior
return toward L-mode-like D-alpha / edge response
```

Stronger evidence:

```
profile-gradient weakening
soft-X or density/power context consistent with back transition
```

Hardening rule:

```
Do not assign H-L transition from a late negative m_edge_conf interval alone.
```

---

## 9. Required review set

Begin with the same physical-window first-gate shots:

```
12046
11941
12055
12007
12017
12063
11768
11776
```

Review all eligible windows:

```
L_MODE
LH_TRANSITION
H_MODE_STABLE
```

Review selected excluded windows:

```
AMBIGUOUS windows with high confidence-positive fraction
AMBIGUOUS windows near transition or later marker events
UNLABELABLE controls 11768 and 11776 for audit only
```

---

## 10. Manual review protocol

For each shot:

```
1. Open tokamark_physical_window_label_preview_shot_<SHOT>.csv.
2. Inspect D-alpha proxy vs time.
3. Inspect profile-gradient proxy vs time.
4. Inspect soft-X combined proxy vs time.
5. Inspect power and density context.
6. Only then inspect m_edge_conf(t) for comparison.
7. Assign or revise hardened label.
8. Record evidence and hardening level.
9. Keep uncertain intervals AMBIGUOUS or UNLABELABLE.
```

The review must preserve rejected and ambiguous rows. Do not delete them.

---

## 11. Required rejection rules

Reject or downgrade a label if:

```
D-alpha evidence is absent or contradictory
profile evidence is absent for H_MODE_STABLE
soft-X response contradicts the proposed label
time window overlaps an obvious burst or disruption
window is too short to support a stable-state claim
label was chosen mainly because m_edge_conf was positive
Q_diag is low and no independent physical evidence exists
```

---

## 12. Required acceptance rules

Accept or harden a label if:

```
the label is supported by physical diagnostics independent of UNNS
the time interval is finite and physically plausible
the evidence is recorded explicitly
the label can survive without looking at m_edge_conf
```

For stronger acceptance:

```
at least two physical diagnostic families agree
```

For strongest acceptance:

```
external timing or expert annotation confirms the window
```

---

## 13. Comparison after hardening

After hardened labels are created, rerun the label analyzer using the hardened file.

Suggested command:

```powershell
python components\tokamark_physical_window_label_analyzer.py ^
  --labels outputs\reports\tokamark_physical_window_labels_HARDENED_v0_1.csv ^
  --out-dir outputs\reports ^
  --prefix tokamark_physical_window_label_analysis_HARDENED_v0_1
```

Expected outputs:

```
outputs/reports/
  tokamark_physical_window_label_analysis_HARDENED_v0_1.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_1_by_label.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_1_transition_pairs.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_1.json
  tokamark_physical_window_label_analysis_HARDENED_v0_1.md
```

---

## 14. Acceptance criteria for the hardening gate

The hardening gate strengthens the project if:

```
1. Most first-gate L_MODE labels remain accepted or plausible.
2. Most LH_TRANSITION labels remain accepted or plausible.
3. At least three H_MODE_STABLE labels survive review.
4. H_MODE_STABLE still has higher m_edge_conf than L_MODE.
5. Within-shot H-minus-L deltas remain positive in most paired shots.
6. Controls remain excluded.
7. Results do not depend on low-Q_diag windows.
8. AMBIGUOUS windows do not dominate the positive evidence.
```

---

## 15. Failure criteria

The hardening gate weakens the project if:

```
1. H_MODE_STABLE labels are mostly rejected.
2. L_MODE labels are not physically defensible.
3. Transition labels cannot be localized.
4. H-minus-L improvement disappears after hardening.
5. Positive alignment depends mainly on ambiguous windows.
6. Controls regain validation status.
7. Labels cannot be justified without m_edge_conf.
```

If these occur, the project should stop or return to label construction rather than make a physical claim.

---

## 16. Required next component

The next component should be:

```
components/
  tokamark_physical_label_hardening_template.py
```

Its job:

```
read tokamark_physical_window_label_template_EDITED.csv
read tokamark_physical_window_label_analysis.csv
create a hardening review CSV
create a markdown hardening review sheet
copy over all current labels
add evidence columns and review-decision fields
```

Suggested outputs:

```
outputs/reports/
  tokamark_physical_window_labels_HARDENING_REVIEW.csv
  tokamark_physical_window_labels_HARDENING_REVIEW.md
```

The reviewer then edits:

```
tokamark_physical_window_labels_HARDENING_REVIEW.csv
```

into:

```
tokamark_physical_window_labels_HARDENED_v0_1.csv
```

---

## 17. Report after hardening

After the hardened labels are analyzed, produce:

```
docs/
  31_PHYSICAL_WINDOW_LABEL_HARDENING_RESULTS.md
```

That report should answer:

> Does the first-gate physical-window alignment survive stricter physical-label review?

It should include:

```
label survival counts
downgraded labels
rejected labels
by-label m_edge_conf summary after hardening
within-shot H-minus-L deltas after hardening
controls audit
decision
```

---

## 18. Relation to the original H-mode question

The project is now close to the original physical question, but not all the way there.

Current evidence supports:

```
UNNS v0.2 margin aligns with provisional physical windows
```

Hardening is needed before claiming:

```
UNNS v0.2 margin aligns with physically defensible L/H regime windows
```

Only after hardening can the project proceed to:

```
standard predictor comparison
external expert-label comparison
broader validation
```

---

## 19. Stop condition

Stop or downgrade the project if:

```
labels cannot be hardened without using m_edge_conf
H_MODE_STABLE windows fail physical review
transition windows cannot be localized
controls become validation-positive
```

The correct scientific response to a failed hardening gate is not another formula. It is to mark the current result as an exploratory pilot.

---

## 20. Final decision statement

The next gate is label hardening.

The first physical-window analysis passed, but its labels remain provisional. The project must now strengthen the physical labels before claiming that the UNNS-H Mode margin corresponds to real L/H regime structure.

The immediate next file is:

```
components/
  tokamark_physical_label_hardening_template.py
```

The next report after that is:

```
docs/
  31_PHYSICAL_WINDOW_LABEL_HARDENING_RESULTS.md
```
