# Physical-Window Labeling Requirements — UNNS-H Mode Project

## 1. Purpose

This document defines the next gate for the UNNS-H Mode project after the v0.2 diagnostic-confidence method passed the moderate 30-shot TokaMark stability panel.

It belongs here:

```text
unns_hmode_project/
  docs/
    28_PHYSICAL_WINDOW_LABELING_REQUIREMENTS.md
```

It follows:

```text
docs/
  27_TOKAMARK_MODERATE_CONFIDENCE_PANEL_RESULTS.md
```

The previous stage established methodological stability:

```text
v0.2 diagnostic-confidence margin passed the 30-shot controlled panel
FULL_PROFILE_EDGE_CANDIDATE shots were enriched near the top
LOW_PRIORITY and PARTIAL_DALPHA cases were suppressed
confidence-positive behavior was tied to diagnostic confidence
```

This document defines what must happen before the project can move from:

```text
structural confidence testing
```

to:

```text
physical H-mode validation
```

The next gate is physical-window labeling.

---

## 2. Why this gate is necessary

The project currently has a confidence-corrected structural margin:

```text
m_edge_conf(t)
```

It can identify time intervals where the UNNS-H Mode structural model says the plasma edge is more boundary-admissible.

But this is not yet the same as saying:

```text
this interval is L-mode
this interval is the L-H transition
this interval is stable H-mode
this interval is pre-ELM
this interval is post-ELM
```

The method has passed a structural consistency test. It has not yet passed a physical labeling test.

Therefore, the next step must define physical windows independently of the UNNS score.

---

## 3. Core principle

Physical labels must not be assigned by `m_edge_conf(t)` itself.

The labels must be derived from independent physical diagnostics and known plasma-regime signatures.

The UNNS margin is then tested against those labels.

Correct logic:

```text
physical diagnostics → physical labels
m_edge_conf(t)       → structural prediction / structural trace
comparison           → validation or failure
```

Incorrect logic:

```text
m_edge_conf(t) → labels → validation of m_edge_conf(t)
```

That would be circular.

---

## 4. Required physical windows

The project needs six possible time-window types.

### 4.1 L-mode interval

Definition:

```text
low-confinement baseline before L-H transition
```

Expected physical traits:

```text
higher edge turbulence / fluctuation activity
no sustained pedestal-like edge structure
D-alpha not suppressed in the H-mode sense
edge profile gradients weaker than post-transition state
m_edge_conf(t) may be low, negative, or ambiguous
```

### 4.2 L-H transition interval

Definition:

```text
short transition window where the plasma edge reorganizes from L-mode to H-mode
```

Expected physical traits:

```text
rapid change in D-alpha / edge emission behavior
change in edge gradient / pedestal proxy
drop or sharp change in turbulence proxy if available
change in edge response before or near confinement improvement
transition should be localized in time
```

### 4.3 Stable H-mode interval

Definition:

```text
post-transition confinement state with sustained edge barrier behavior
```

Expected physical traits:

```text
sustained D-alpha suppression or altered edge emission pattern
stronger edge gradients / pedestal proxy
lower turbulence proxy if available
relatively coherent edge response
m_edge_conf(t) should be more often positive or less negative than L-mode
```

### 4.4 Pre-ELM interval

Definition:

```text
interval shortly before an edge-localized-mode-like crash or burst
```

Expected physical traits:

```text
edge pressure / gradient buildup
possible increase in instability indicators
soft-X or D-alpha behavior indicating imminent edge event
m_edge_conf(t) may show overload, fragmentation, or declining confidence-positive behavior
```

### 4.5 Post-ELM interval

Definition:

```text
recovery interval after an ELM-like burst or edge crash
```

Expected physical traits:

```text
sudden D-alpha / edge emission burst followed by recovery
edge gradient relaxation
temporary route disruption
m_edge_conf(t) may become negative or ambiguous before recovery
```

### 4.6 H-L back-transition interval

Definition:

```text
transition from H-mode-like state back to L-mode-like state
```

Expected physical traits:

```text
loss of sustained edge barrier behavior
return of higher edge transport / turbulence proxy
D-alpha / edge emission returns toward L-mode-like behavior
m_edge_conf(t) should decline or lose confidence-positive persistence
```

---

## 5. Minimum independent diagnostic requirements

A shot should not enter physical-window validation unless it has enough independent diagnostics.

### 5.1 Required baseline diagnostics

Minimum:

```text
time vector / synchronized common time base
D-alpha or credible edge-emission proxy
density or line-integrated density proxy
heating / power input proxy
edge profile proxy or Thomson profile data
at least one edge-activity / soft-X / fluctuation-like proxy
```

### 5.2 Strong validation diagnostics

Preferred:

```text
D-alpha
Thomson Te profile
Thomson ne profile
soft-X lower / upper channels
NBI or auxiliary heating proxy
line density
q95 / equilibrium geometry
stored energy or beta proxy
magnetic fluctuation / Mirnov-like signal if available
```

### 5.3 Exclusion condition

A shot should not be physically labeled if:

```text
D-alpha is missing
all profile information is missing
time alignment is uncertain
too much of the candidate interval is low-confidence
the signal is too sparse to localize a transition
only metadata class is available
```

---

## 6. Labeling must be independent of UNNS

The following columns must not be used to create physical labels:

```text
m_edge_raw
m_edge_conf
m_edge_conf_state
confidence_structural_score
UNNS rank
selection_role
```

They may only be used after labeling, for comparison.

Allowed label sources:

```text
D-alpha morphology
profile-gradient morphology
soft-X / edge activity morphology
density / power context
known shot notes if available
published event labels if available
operator/manual physical review
```

---

## 7. First-pass manual labeling protocol

The first physical-window labeling should be manual and conservative.

Use a small subset first:

```text
top 5 confidence-ranked FULL_PROFILE_EDGE_CANDIDATE shots
reference shot 12063
one or two suppressed partial cases
one low-priority negative control
```

Recommended first set:

```text
12046
11941
12055
12007
12017
12063
11768
11776
```

This includes:

```text
strong full-profile-edge cases
the original reference anchor
a partial raw-positive but confidence-suppressed case
a low-priority suppressed stress-test
```

---

## 8. Required labeling artifact

Create a human-readable physical-window label file:

```text
outputs/reports/
  tokamark_physical_window_labels_v0_1.csv
```

Required columns:

```text
shot_id
window_id
label_type
t_start
t_end
label_confidence
primary_evidence
secondary_evidence
excluded_from_validation
exclusion_reason
notes
```

Allowed `label_type` values:

```text
L_MODE
LH_TRANSITION
H_MODE_STABLE
PRE_ELM
POST_ELM
HL_BACK_TRANSITION
AMBIGUOUS
UNLABELABLE
```

Allowed `label_confidence` values:

```text
high
moderate
low
unlabelable
```

---

## 9. Window-label rules

### 9.1 Time windows must be finite

Every labeled physical window must have:

```text
t_start < t_end
```

Point events may be recorded as narrow windows, but not as single isolated timestamps unless unavoidable.

### 9.2 Label confidence must be explicit

No physical label should be used without a confidence level.

### 9.3 Ambiguity is allowed

If the evidence is mixed, use:

```text
AMBIGUOUS
```

rather than forcing an H-mode or transition label.

### 9.4 Unlabelable shots must be retained

Do not delete failed or unlabelable shots. Mark them:

```text
UNLABELABLE
excluded_from_validation = true
```

This prevents survivorship bias.

---

## 10. Candidate physical evidence patterns

### 10.1 D-alpha pattern

For L-H transition candidates, inspect whether D-alpha shows:

```text
sharp drop
sustained suppression
burst-like ELM features
recovery cycles
```

For post-ELM candidates, inspect whether D-alpha shows:

```text
burst then decay
```

### 10.2 Profile-gradient pattern

For H-mode candidates, inspect whether Thomson profile proxies show:

```text
edge steepening
stronger edge gradient
pedestal-like structure
sustained post-transition gradient
```

### 10.3 Soft-X / edge activity pattern

Inspect whether soft-X channels show:

```text
edge activity change near transition
burst-like activity
correlated response with D-alpha or profiles
```

### 10.4 Power and density context

Inspect whether transition-like changes occur in a physically plausible context:

```text
heating sufficient or changing
density not obviously pathological
time region not dominated by missing data
```

### 10.5 Geometry context

Use geometry only as support, not as the main label source:

```text
q95
elongation
triangularity
minor radius
```

---

## 11. UNNS comparison after labels

After physical windows are labeled, compare them against `m_edge_conf(t)`.

Required comparisons:

```text
median m_edge_conf by label_type
confidence-positive fraction by label_type
confidence-negative fraction by label_type
Q_diag by label_type
P_missing_critical by label_type
transition-aligned m_edge_conf behavior
```

Expected if the method is meaningful:

```text
H_MODE_STABLE windows have higher m_edge_conf than L_MODE windows
LH_TRANSITION windows show change or rise in m_edge_conf near transition
PRE_ELM windows may show overload / decline / fragmentation signatures
POST_ELM windows show disruption and recovery
UNLABELABLE windows do not dominate positive evidence
```

---

## 12. Acceptance criteria for physical-window validation

The next validation stage succeeds only if:

```text
1. Physical labels are assigned independently of UNNS scores.
2. At least several FULL_PROFILE_EDGE_CANDIDATE shots receive usable labels.
3. H_MODE_STABLE or post-transition windows show higher m_edge_conf than L_MODE windows.
4. LH_TRANSITION windows show meaningful local change in m_edge_conf.
5. Confidence-positive intervals are enriched in physically plausible H-mode/post-transition windows.
6. Suppressed partial or low-priority shots remain weak or unlabelable.
7. Results are not explained only by Q_diag or metadata class.
```

---

## 13. Failure criteria

The physical-window stage fails if:

```text
1. Physical labels cannot be assigned from available diagnostics.
2. m_edge_conf does not differ between L-mode and H-mode-like windows.
3. Confidence-positive intervals appear mostly outside plausible H-mode windows.
4. Low-priority or partial shots regain positive status after physical labeling.
5. The result depends on circular label creation from m_edge_conf.
6. The method cannot distinguish transition, stable, and recovery windows.
```

If this stage fails, the project should stop as a methodological pilot.

---

## 14. Required next component

The next component should be:

```text
components/
  tokamark_physical_window_label_template.py
```

Its job is not to auto-label physics.

Its job is to generate a review template for selected shots:

```text
load per-shot time series
extract diagnostic preview windows
write a CSV labeling template
write a markdown review sheet per shot
```

Suggested outputs:

```text
outputs/reports/
  tokamark_physical_window_label_template.csv
  tokamark_physical_window_label_review.md
```

A later manual or semi-automatic pass can fill labels.

---

## 15. Suggested initial shot set

Use this initial set:

```text
12046
11941
12055
12007
12017
12063
11768
11776
```

Why:

```text
12046–12017:
  top-ranked full-profile-edge shots from the moderate panel

12063:
  original reference anchor

11768:
  partial raw-positive but confidence-suppressed control

11776:
  low-priority raw-positive but confidence-suppressed control
```

Do not label all 30 shots at first.

---

## 16. Required visual/manual review products

For each selected shot, the review sheet should include:

```text
D-alpha proxy vs time
m_edge_conf vs time
m_edge_raw vs time
Q_diag vs time
P_missing_critical vs time
profile-gradient proxy vs time
soft-X proxy vs time
power / density proxy vs time
```

The review sheet should mark candidate intervals where:

```text
D-alpha changes sharply
profile-gradient proxy changes
soft-X activity changes
m_edge_conf becomes positive
m_edge_conf becomes negative
Q_diag drops below threshold
```

Again, these markers are aids, not final labels.

---

## 17. Physical validation report after labeling

After labels are filled, produce:

```text
docs/
  29_PHYSICAL_WINDOW_LABELING_RESULTS.md
```

That report should answer:

> Do independently labeled physical windows align with the v0.2 UNNS-H Mode margin?

It should include:

```text
label counts
excluded windows
per-label m_edge_conf statistics
transition-aligned plots or summaries
failure cases
decision
```

---

## 18. Relation to the original H-mode question

This gate returns the project to the original physical question:

```text
What is the structural origin of the L-H transition?
```

So far, the project has shown:

```text
a structural margin can be built
diagnostic confidence can prevent missing-data artifacts
full diagnostic candidates are enriched in positive structural behavior
```

But the original physical question requires:

```text
Does the structural margin align with actual L/H/transition/ELM windows?
```

That is what the physical-window gate must test.

---

## 19. Stop condition

If physical windows cannot be labeled independently, stop.

If the labels do not align with `m_edge_conf(t)`, stop or revise the physical interpretation.

If the labels do align, then and only then proceed toward:

```text
broader validation
comparison with standard predictors
possible manuscript/article framing
```

---

## 20. Final decision statement

The UNNS-H Mode project has passed structural-methodology testing but has not yet passed physical validation.

The next gate is independent physical-window labeling.

The work should now shift from:

```text
Which shots score highly?
```

to:

```text
Do physically identified L/H/ELM windows correspond to the structural boundary-admissibility margin?
```

Only this can move the project from an internally coherent UNNS diagnostic toward a physically meaningful H-mode claim.
