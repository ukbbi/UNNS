# H-Mode-Stable Evidence Recovery Plan — UNNS-H Mode Project

## 1. Purpose

This document defines the next gate after the conservative physical-window label hardening pass.

It belongs here:

```text
unns_hmode_project/
  docs/
    32_H_MODE_STABLE_EVIDENCE_RECOVERY_PLAN.md
```

It follows:

```text
docs/
  31_PHYSICAL_WINDOW_LABEL_HARDENING_RESULTS.md
```

The hardening stage produced an honest but weaker result:

```text
decision: physical_window_analysis_inconclusive_or_weak
eligible windows: 12
excluded windows: 77

eligible:
  L_MODE:        6
  LH_TRANSITION: 6
  H_MODE_STABLE: 0
```

The reason was not computational failure. It was evidentiary discipline: all provisional `H_MODE_STABLE` windows were excluded because they had not yet been independently supported by stronger physical evidence.

This document defines how to recover, reject, or keep excluded those `H_MODE_STABLE` windows.

---

## 2. Central question

The question for this gate is:

> Can any excluded `H_MODE_STABLE` window be independently supported by physical diagnostics strongly enough to re-enter validation?

The question is not:

```text
Does m_edge_conf become positive there?
```

That is already known for some windows and cannot be used to assign the physical label.

The correct question is:

```text
Does independent physical evidence support a stable H-mode-like window?
```

Only after that decision may the window be compared against `m_edge_conf(t)`.

---

## 3. Why this gate exists

The first physical-window analysis showed the promising ordering:

```text
L_MODE < LH_TRANSITION < H_MODE_STABLE
```

But this result depended on provisional `H_MODE_STABLE` labels.

The conservative hardening pass then excluded all five `H_MODE_STABLE` windows because the evidence was not strong enough under the hardening rule.

Therefore the current bottleneck is precise:

```text
H_MODE_STABLE evidence
```

The project does not need a new UNNS formula now.

It needs stronger independent physical support for stable H-mode candidate intervals.

---

## 4. Candidate windows to review

The five excluded candidate windows are:

```text
12007_MANUAL_H_MODE_STABLE_001
12017_MANUAL_H_MODE_STABLE_001
12046_MANUAL_H_MODE_STABLE_001
12055_MANUAL_H_MODE_STABLE_001
12063_MANUAL_H_MODE_STABLE_001
```

These windows were excluded from the conservative hardened validation set.

They must now be treated as evidence-recovery targets, not accepted labels.

---

## 5. Required input files

The review should use:

```text
outputs/reports/
  tokamark_physical_window_labels_HARDENED_v0_1.csv
  tokamark_physical_window_labels_HARDENING_REVIEW.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_1.csv
  tokamark_physical_window_label_candidate_markers.csv
  tokamark_physical_window_label_preview_shot_<SHOT>.csv
  tokamark_shot_<SHOT>_m_edge_confidence_revision.csv
```

For each candidate shot, the preview and confidence-revision files should be available:

```text
12007
12017
12046
12055
12063
```

---

## 6. Strict non-circularity rule

The reviewer must inspect physical diagnostics first.

Do not use these columns to accept an H-mode-stable label:

```text
m_edge_raw
m_edge_conf
m_edge_conf_state
confidence_structural_score
conf_positive_fraction
UNNS rank
```

These can be inspected only after the physical review decision is recorded.

Allowed physical evidence sources:

```text
D-alpha morphology
profile-gradient proxy
soft-X / edge-activity proxy
power and density context
geometry context as support only
external L-H/H-mode timing if available
manual plasma-regime notes if available
```

---

## 7. Evidence families

Each `H_MODE_STABLE` candidate must be reviewed across five evidence families.

### 7.1 D-alpha morphology

Look for:

```text
post-transition behavior different from pre-transition baseline
suppression or sustained altered edge-emission pattern
absence of immediate burst/crash structure inside the candidate window
```

Reject or downgrade if:

```text
D-alpha is absent
D-alpha is dominated by burst-like behavior
D-alpha does not differ from pre-transition baseline
```

### 7.2 Profile-gradient behavior

Look for:

```text
edge-gradient strengthening after transition
pedestal-like proxy behavior
sustained post-transition profile-gradient regime
```

Reject or downgrade if:

```text
profile proxy is absent
profile-gradient behavior is flat, missing, or contradictory
candidate window has no profile support
```

### 7.3 Soft-X / edge activity

Look for:

```text
soft-X response consistent with post-transition edge organization
absence of large disruptive events inside stable interval
coherence with D-alpha and profile timing
```

Reject or downgrade if:

```text
soft-X is absent
soft-X shows disruption rather than stability
soft-X contradicts D-alpha or profile interpretation
```

### 7.4 Power and density context

Look for:

```text
physically plausible post-transition context
heating/power not obviously incompatible with the candidate interval
density not dominated by pathological missingness or impossible values
```

Reject or downgrade if:

```text
power/density context is missing or contradictory
candidate is only a numerically convenient interval
```

### 7.5 External timing / expert reference

Strongest evidence comes from:

```text
published L-H timing
expert annotation
shot logs
standard H-mode labels
known transition timing from an independent source
```

Without such external support, the maximum level should usually be:

```text
2_SUPPORTED
```

not:

```text
3_EXTERNALLY_ANCHORED
```

---

## 8. Evidence scoring

Each candidate window should receive a physical evidence score independent of UNNS.

Suggested scoring:

```text
D-alpha evidence:        0, 1, or 2
profile evidence:        0, 1, or 2
soft-X evidence:         0, 1, or 2
power/density context:   0, 1, or 2
external reference:      0, 1, or 2
```

Interpretation:

```text
0 = absent, contradictory, or unusable
1 = weak / plausible
2 = clear support
```

Total score:

```text
H_evidence_score = dalpha + profile + softx + power_density + external_reference
```

Maximum:

```text
10
```

Minimum acceptance suggestion:

```text
H_evidence_score >= 5
```

Stronger acceptance suggestion:

```text
H_evidence_score >= 6
and at least two evidence families score 2
```

Externally anchored acceptance:

```text
external_reference = 2
and at least one independent diagnostic family also supports the label
```

---

## 9. Review decisions

Allowed decisions:

```text
ACCEPT_H_MODE_STABLE
DOWNGRADE_TO_AMBIGUOUS
REJECT
NEEDS_EXTERNAL_REFERENCE
KEEP_EXCLUDED
```

Meaning:

### 9.1 ACCEPT_H_MODE_STABLE

Use only when independent physical evidence supports the stable H-mode interpretation.

Requirements:

```text
not selected from m_edge_conf
finite interval
physical evidence recorded
diagnostic support sufficient
```

### 9.2 DOWNGRADE_TO_AMBIGUOUS

Use when evidence is suggestive but not strong enough.

### 9.3 REJECT

Use when the candidate window is physically inconsistent with H-mode-stable behavior.

### 9.4 NEEDS_EXTERNAL_REFERENCE

Use when internal diagnostics are suggestive but insufficient.

### 9.5 KEEP_EXCLUDED

Use when the window cannot be evaluated reliably.

---

## 10. Required output file

Create:

```text
outputs/reports/
  tokamark_hmode_stable_evidence_review.csv
```

Required columns:

```text
shot_id
window_id
t_start
t_end
dalpha_evidence_score
profile_evidence_score
softx_evidence_score
power_density_context_score
external_reference_score
H_evidence_score
dalpha_notes
profile_notes
softx_notes
power_density_notes
external_reference_notes
physical_review_decision
accepted_as_hmode_stable
hardening_level
excluded_from_validation
exclusion_reason
reviewer_notes
```

Allowed `hardening_level` values:

```text
0_PROVISIONAL
1_PLAUSIBLE
2_SUPPORTED
3_EXTERNALLY_ANCHORED
```

---

## 11. Required markdown review file

Create:

```text
outputs/reports/
  tokamark_hmode_stable_evidence_review.md
```

For each candidate, the review sheet should show:

```text
shot_id
window_id
time interval
D-alpha evidence summary
profile-gradient evidence summary
soft-X evidence summary
power/density context
external reference status
decision
```

It should also include the UNNS audit values separately, under a clearly marked section:

```text
UNNS audit only — not used for physical label assignment
```

---

## 12. Required next component

Create:

```text
components/
  tokamark_hmode_stable_evidence_reviewer.py
```

Its job:

```text
read hardened label file
select excluded H_MODE_STABLE rows
load preview and confidence-revision files
summarize physical evidence windows
write a focused review CSV
write a focused markdown review sheet
```

It should not auto-accept H-mode-stable labels.

It should produce a review artifact that can be manually edited.

---

## 13. Updated hardened label file after recovery

After review, create:

```text
outputs/reports/
  tokamark_physical_window_labels_HARDENED_v0_2.csv
```

This should start from:

```text
tokamark_physical_window_labels_HARDENED_v0_1.csv
```

and change only the five candidate H-mode-stable rows according to the evidence review.

If a candidate is accepted:

```text
label_type = H_MODE_STABLE
hardened_label_type = H_MODE_STABLE
excluded_from_validation = False
review_decision = ACCEPT
hardening_level = 1_PLAUSIBLE or 2_SUPPORTED or 3_EXTERNALLY_ANCHORED
```

If not accepted:

```text
excluded_from_validation = True
review_decision = KEEP_EXCLUDED / REJECT / NEEDS_EXTERNAL_REFERENCE
```

Do not alter L-mode or L-H transition labels in this recovery step.

---

## 14. Reanalysis after evidence recovery

Run:

```powershell
python components\tokamark_physical_window_label_analyzer.py ^
  --labels outputs\reports\tokamark_physical_window_labels_HARDENED_v0_2.csv ^
  --out-dir outputs\reports ^
  --prefix tokamark_physical_window_label_analysis_HARDENED_v0_2
```

Expected outputs:

```text
outputs/reports/
  tokamark_physical_window_label_analysis_HARDENED_v0_2.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_2_by_label.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_2_transition_pairs.csv
  tokamark_physical_window_label_analysis_HARDENED_v0_2.json
  tokamark_physical_window_label_analysis_HARDENED_v0_2.md
```

---

## 15. Success criteria

The evidence recovery gate succeeds if:

```text
at least 3 H_MODE_STABLE windows are accepted
accepted windows are supported by independent physical evidence
accepted windows are not selected using m_edge_conf
within-shot H-minus-L m_edge_conf deltas become finite again
most accepted H_MODE_STABLE windows have higher m_edge_conf than L_MODE
controls remain excluded
```

Minimum success:

```text
3 accepted H_MODE_STABLE windows at hardening level 1 or higher
```

Stronger success:

```text
3 accepted H_MODE_STABLE windows at hardening level 2 or higher
```

Best success:

```text
3 accepted H_MODE_STABLE windows with external timing support
```

---

## 16. Failure criteria

The evidence recovery gate fails if:

```text
fewer than 3 H_MODE_STABLE windows can be accepted
accepted windows depend on m_edge_conf rather than physical diagnostics
D-alpha/profile/soft-X evidence contradicts the H-mode-stable interpretation
controls become validation-eligible
within-shot H-minus-L comparison remains impossible
```

If failure occurs, the project should stop short of claiming physical H-mode validation.

The correct conclusion would be:

```text
UNNS-H Mode remains a promising structural methodology,
but current public TokaMark evidence is insufficient to harden stable H-mode labels.
```

---

## 17. Relation to the original H-mode question

The project began with the physical question:

```text
What is the structural origin of H-mode?
```

The present bottleneck shows exactly what remains missing:

```text
independently defensible H-mode-stable windows
```

Without those windows, the project cannot validate a structural explanation of H-mode.

With those windows, the project can test whether the UNNS margin aligns with real H-mode-stable behavior.

---

## 18. Expected outcomes

There are three possible outcomes.

### 18.1 Positive recovery

Several H-mode-stable windows are accepted.

Then proceed to:

```text
docs/
  33_H_MODE_STABLE_EVIDENCE_RECOVERY_RESULTS.md
```

and rerun hardened analysis v0.2.

### 18.2 Partial recovery

One or two windows are accepted, but not enough.

Then report the project as promising but underpowered.

### 18.3 No recovery

No windows survive.

Then stop the physical H-mode claim and preserve the project as a methodological pilot.

---

## 19. Report after evidence recovery

After the reviewer and updated hardened analysis are complete, produce:

```text
docs/
  33_H_MODE_STABLE_EVIDENCE_RECOVERY_RESULTS.md
```

It should answer:

```text
Did any excluded H_MODE_STABLE windows survive independent physical evidence review?
```

It should include:

```text
per-window decisions
evidence scores
accepted/rejected counts
updated hardened v0.2 label counts
updated H-vs-L analysis
decision
```

---

## 20. Final decision statement

The next gate is H-mode-stable evidence recovery.

The hardening stage did not invalidate the project, but it blocked the strongest physical claim. The project now needs to recover or reject the five excluded `H_MODE_STABLE` windows using independent physical evidence.

Only after at least several stable H-mode windows survive this review can the project responsibly return to the claim that the UNNS-H Mode margin aligns with real H-mode regime structure.
