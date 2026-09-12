# Diagnostic Confidence Revision Plan — UNNS-H Mode Project

## 1. Purpose

This document defines the missing formal consolidation required before the UNNS-H Mode project continues technically.

It belongs here:

```text
unns_hmode_project/
  docs/
    24_DIAGNOSTIC_CONFIDENCE_REVISION_PLAN.md
```

It follows:

```text
docs/
  23_CURRENT_STATE_AND_DECISION_POINT.md
```

The previous decision document froze the exploratory v0.1 pipeline and identified the central weakness:

```text
v0.1 discriminates, but incomplete diagnostic cases can look artificially positive.
```

This plan defines the next formal correction:

```text
separate raw structural margin from diagnostic confidence
```

The goal is not to invent a new theory.  
The goal is to prevent missing or incomplete diagnostics from being mistaken for structural edge confinement.

---

## 2. Why this revision is necessary

The five-shot TokaMark panel showed two facts at the same time.

### 2.1 v0.1 has real structural signal

Shot `12063` remained top-ranked in the first small panel:

```text
12063:
  class: FULL_PROFILE_EDGE_CANDIDATE
  panel rank: 1
  interpretable positive windows: 8
  missingness median: 0.222...
```

This supports v0.1 as an exploratory structural diagnostic.

### 2.2 v0.1 can over-reward incomplete cases

Some incomplete shots showed inflated positive margins:

```text
11776:
  class: LOW_PRIORITY
  missing NBI power
  missing D-alpha
  missing Thomson Te/ne
  high positive-boundary fraction
  high positive median m_edge

11768:
  class: PARTIAL_DALPHA_CANDIDATE
  missing NBI power
  missing Thomson Te/ne
  inflated positive-boundary fraction
```

This reveals a scoring ambiguity.

The raw margin:

```text
m_edge(t) = C_edge_capacity(t) - F_route_fragmentation(t)
```

can become artificially positive if fragmentation evidence is missing or if capacity proxies remain while critical counter-evidence is absent.

Therefore v0.1 should not be scaled further until diagnostic confidence is included.

---

## 3. Formal problem statement

The current v0.1 margin mixes two distinct quantities:

```text
1. structural edge-admissibility signal
2. diagnostic availability / reliability
```

The corrected framework must distinguish them.

### Existing raw margin

```text
m_edge_raw(t) = C_edge_capacity(t) - F_route_fragmentation(t)
```

This should be preserved for auditability.

### New diagnostic confidence

```text
Q_diag(t) ∈ [0, 1]
```

This measures whether enough diagnostic evidence exists at time `t` to trust the raw margin.

### Confidence-weighted margin

```text
m_edge_conf(t)
```

This is the margin used for comparison and ranking after diagnostic confidence correction.

---

## 4. Design principle

The confidence revision must obey this rule:

```text
Missing diagnostics may reduce confidence.
Missing diagnostics may not create positive evidence.
```

A shot should not gain a stronger positive margin simply because key fragmentation or transport terms are unavailable.

The revision must preserve two layers:

```text
m_edge_raw(t)
  what the original v0.1 structural formula produced

m_edge_conf(t)
  what remains after diagnostic-confidence correction
```

This prevents the correction from hiding the original signal while still protecting interpretation.

---

## 5. Required diagnostic groups

The diagnostic confidence score should be built from five groups.

### 5.1 Power-drive group

Minimum signals:

```text
summary_power_nbi
summary_ip
```

Purpose:

```text
heating / current context
route-stress and power-balance interpretation
```

Missing NBI power is critical because the model cannot distinguish low power pressure from absent power evidence.

### 5.2 Density group

Minimum signals:

```text
interferometer_n_e_line
density_support
```

Purpose:

```text
density support
scaling position
edge-capacity context
```

### 5.3 Edge-response group

Minimum signals:

```text
dalpha_proxy
softx_lower_proxy
softx_upper_proxy
```

Purpose:

```text
D-alpha-like edge response
soft-X edge/activity response
boundary event structure
```

D-alpha and soft-X should not be treated as interchangeable. D-alpha absence is especially serious for H-mode transition interpretation.

### 5.4 Profile / transport group

Minimum signals:

```text
thomson_t_e
thomson_n_e
te_profile_gradient_proxy
ne_profile_gradient_proxy
S_transport
```

Purpose:

```text
edge gradient
transport suppression proxy
profile sharpening
```

If Thomson Te/ne are missing, the model may still run, but the result must be confidence-limited.

### 5.5 Geometry group

Minimum signals:

```text
q95_proxy
elongation_proxy
triangularity_upper_proxy
triangularity_lower_proxy
minor_radius_proxy
geometry_stability
```

Purpose:

```text
route geometry
admissible stabilization context
boundary geometry confidence
```

---

## 6. Proposed confidence terms

Define per-time confidence terms:

```text
Q_power(t)
Q_density(t)
Q_edge(t)
Q_profile(t)
Q_geometry(t)
Q_missing(t)
```

Each term lies in `[0, 1]`.

### 6.1 Power confidence

```text
Q_power(t) =
  1.0 if NBI / heating and current evidence are finite
  0.5 if only partial power/current context exists
  0.0 if critical power-drive evidence is absent
```

### 6.2 Density confidence

```text
Q_density(t) =
  finite confidence of density_proxy and density_support
```

### 6.3 Edge-response confidence

```text
Q_edge(t) =
  weighted confidence from D-alpha and soft-X availability
```

Recommended weights:

```text
D-alpha: 0.50
soft-X lower: 0.25
soft-X upper: 0.25
```

If D-alpha is missing, `Q_edge(t)` should be strongly reduced even if soft-X exists.

### 6.4 Profile / transport confidence

```text
Q_profile(t) =
  confidence from Te profile, ne profile, and S_transport availability
```

Recommended weights:

```text
Te gradient: 0.35
ne gradient: 0.35
S_transport finite: 0.30
```

If Thomson profiles are absent, profile confidence should be close to zero.

### 6.5 Geometry confidence

```text
Q_geometry(t) =
  finite confidence of geometry_stability and core equilibrium proxies
```

Geometry confidence should support the model but should not rescue a shot with missing power, D-alpha, and profiles.

### 6.6 Missingness confidence

The existing v0.1 already has:

```text
missingness_pressure(t)
```

Convert it into a confidence term:

```text
Q_missing(t) = 1 - missingness_pressure(t)
```

This gives a general coverage penalty.

---

## 7. Aggregate diagnostic confidence

A conservative aggregate confidence score should be:

```text
Q_diag(t) =
  0.20 · Q_power(t)
+ 0.15 · Q_density(t)
+ 0.25 · Q_edge(t)
+ 0.25 · Q_profile(t)
+ 0.10 · Q_geometry(t)
+ 0.05 · Q_missing(t)
```

This weighting makes edge and profile diagnostics central, because the H-mode question concerns boundary reorganization, not merely global power or geometry.

The weights may be adjusted later, but the first revision should keep them explicit and auditable.

---

## 8. Critical-missing penalty

In addition to `Q_diag(t)`, define a critical missing penalty:

```text
P_missing_critical(t)
```

It should penalize missing diagnostics that can falsely inflate the margin.

Recommended components:

```text
missing_NBI_power
missing_Dalpha
missing_Thomson_Te
missing_Thomson_ne
missing_softX_pair
missing_transport_term
high_missingness_pressure
```

A simple first version:

```text
P_missing_critical(t) =
  0.20 · I_missing_NBI
+ 0.25 · I_missing_Dalpha
+ 0.15 · I_missing_Te
+ 0.15 · I_missing_ne
+ 0.10 · I_missing_softX_pair
+ 0.10 · I_missing_transport
+ 0.05 · missingness_pressure(t)
```

where each `I_missing_*` is `1` when the required diagnostic is absent or unusable at time `t`, otherwise `0`.

---

## 9. Confidence-weighted margin options

Two candidate forms are allowed.

### Option A — Simple confidence-weighted raw margin

```text
m_edge_conf(t) = m_edge_raw(t) · Q_diag(t)
```

This is easy to understand and preserves sign, but it may not penalize false positives strongly enough.

### Option B — Conservative corrected margin

```text
m_edge_conf(t) =
  C_edge_capacity(t) · Q_capacity(t)
  - F_route_fragmentation(t) · Q_fragmentation(t)
  - P_missing_critical(t)
```

Recommended first implementation:

```text
Q_capacity(t) =
  0.40 · Q_edge(t)
+ 0.25 · Q_density(t)
+ 0.20 · Q_geometry(t)
+ 0.15 · Q_profile(t)

Q_fragmentation(t) =
  0.40 · Q_power(t)
+ 0.40 · Q_profile(t)
+ 0.20 · Q_missing(t)
```

Then:

```text
m_edge_conf(t) =
  C_edge_capacity(t) · Q_capacity(t)
  - F_route_fragmentation(t) · Q_fragmentation(t)
  - P_missing_critical(t)
```

This is more conservative and should be preferred for the first correction.

---

## 10. Confidence-adjusted states

The raw state should remain:

```text
m_edge_state
```

The revised state should be added separately:

```text
m_edge_conf_state
```

Recommended thresholds:

```text
m_edge_conf(t) ≥ +0.20
  confidence_positive_boundary_margin

-0.20 < m_edge_conf(t) < +0.20
  confidence_boundary_ambiguous_margin

m_edge_conf(t) ≤ -0.20
  confidence_negative_leakage_margin

Q_diag(t) < 0.40
  low_confidence_uninterpretable
```

The low-confidence rule should override the positive/negative state, because a high margin with low diagnostic confidence is not interpretable.

---

## 11. Acceptance criteria

The diagnostic-confidence revision succeeds only if all of these hold on the existing five-shot panel.

### 11.1 Preserve shot 12063

Shot `12063` should remain structurally strong after confidence correction.

Expected:

```text
m_edge_conf preserves some positive windows
interpretable positive count remains nonzero
low-confidence flags are limited
panel rank remains high
```

### 11.2 Suppress incomplete inflated cases

Shots `11776` and `11768` should no longer look strongly positive.

Expected:

```text
positive fraction decreases
low-confidence flags increase
m_edge_conf median decreases
inflated long positive intervals are suppressed
```

### 11.3 Confidence-limit shot 11876

Shot `11876` should remain structurally active but confidence-limited because it lacks Thomson profiles.

Expected:

```text
edge activity remains visible
profile confidence is low
transport confidence is low
m_edge_conf is reduced relative to m_edge_raw
```

### 11.4 Preserve weakness of shot 11830

Shot `11830` should remain weaker than `12063` because it lacks soft-X support.

Expected:

```text
edge confidence lower than 12063
positive windows fewer or lower confidence
route fragmentation remains relatively strong
```

### 11.5 Keep auditability

Every output must include both:

```text
m_edge_raw
m_edge_conf
```

The correction must not replace the original raw margin.

---

## 12. Failure conditions

The revision fails if any of the following occurs.

### 12.1 It erases the reference

If shot `12063` loses all meaningful positive structure, the confidence correction is too harsh or the original v0.1 signal was too fragile.

### 12.2 It does not suppress incomplete shots

If `11776` and `11768` remain highly positive after confidence correction, the correction has failed.

### 12.3 It depends only on metadata class

If the correction simply ranks by metadata class and ignores time-dependent evidence, it is not a time-resolved model.

### 12.4 It hides missingness

If the correction removes missingness artifacts without reporting where and why the penalty occurred, it is not auditable.

### 12.5 It produces a new arbitrary score

If the confidence score cannot be explained by diagnostic groups and critical missing penalties, the revision becomes another opaque index.

---

## 13. Required output columns

The revised component should output a CSV with the existing v0.1 columns plus:

```text
Q_power
Q_density
Q_edge
Q_profile
Q_geometry
Q_missing
Q_diag
P_missing_critical
Q_capacity
Q_fragmentation
m_edge_raw
m_edge_conf
m_edge_raw_state
m_edge_conf_state
confidence_flag
missing_critical_flags
```

Optional useful columns:

```text
is_low_confidence
is_confidence_positive
is_confidence_negative
delta_conf_minus_raw
```

---

## 14. Required reports

The revision should produce:

```text
outputs/reports/
  tokamark_shot_<SHOT>_m_edge_confidence_revision.csv
  tokamark_shot_<SHOT>_m_edge_confidence_revision.json
  tokamark_shot_<SHOT>_m_edge_confidence_revision.md
```

For the panel:

```text
outputs/reports/
  tokamark_confidence_panel_comparison.csv
  tokamark_confidence_panel_comparison.json
  tokamark_confidence_panel_comparison.md
```

The project document should be:

```text
docs/
  25_TOKAMARK_M_EDGE_CONFIDENCE_REVISION_RESULTS.md
```

Document `24` is only the plan.

---

## 15. Implementation sequence

The technical implementation should follow this order.

### Step 1 — Do not alter old files

Keep all v0.1 outputs unchanged.

### Step 2 — Build the revision component

Create:

```text
components/
  tokamark_m_edge_confidence_revision.py
```

The component should read existing v0.1 CSV outputs rather than re-downloading arrays.

Input:

```text
outputs/reports/tokamark_shot_<SHOT>_m_edge_t_probe.csv
outputs/reports/tokamark_shot_<SHOT>_signal_probe.json
outputs/reports/tokamark_positive_corridor_metadata_candidates.csv
```

### Step 3 — Run the same five-shot panel

Use only:

```text
12063
11830
11876
11768
11776
```

Do not expand the panel yet.

### Step 4 — Compare raw and confidence-weighted rankings

The report must show:

```text
raw rank
confidence-adjusted rank
raw positive fraction
confidence-positive fraction
raw median
confidence median
Q_diag median
low-confidence fraction
```

### Step 5 — Decide

If the confidence correction works, the project can continue to a larger panel.

If it fails, the current work should be written as an exploratory pilot with limitations.

---

## 16. Proposed component interface

Command:

```powershell
python components\tokamark_m_edge_confidence_revision.py ^
  --shots 12063 11830 11876 11768 11776 ^
  --out-dir outputs\reports
```

Optional:

```powershell
python components\tokamark_m_edge_confidence_revision.py ^
  --shot-id 12063 ^
  --out-dir outputs\reports
```

The component should support both one-shot mode and panel mode.

---

## 17. Correct next decision after the revision

After the confidence revision, the project should ask one question:

> Does diagnostic confidence preserve the structural preference for shot `12063` while suppressing incomplete inflated cases?

If yes:

```text
v0.2 can proceed to a 20–50 shot panel.
```

If no:

```text
the model should stop as an exploratory pilot.
```

No larger scan should happen before this answer exists.

---

## 18. Project status after this plan

```text
v0.1 exploratory margin:             frozen
v0.1 internal trace inspection:      passed
v0.1 cross-shot comparison:          passed weakly
v0.1 five-shot panel:                discriminative but not unique
main weakness:                       incomplete diagnostics can inflate positives
next required correction:            diagnostic confidence
broader scaling:                     blocked until confidence revision
physical validation:                 not yet
```

---

## 19. Final synthesis statement

The diagnostic confidence revision is the necessary bridge between an exploratory structural signal and a serious validation pipeline.

The current v0.1 margin should not be discarded, because it produced coherent structure and ranked shot `12063` strongest in the first panel. But it should not be scaled further, because incomplete shots can appear artificially positive.

The correct next step is to preserve `m_edge_raw(t)`, compute `Q_diag(t)`, penalize critical missing diagnostics, and report a separate confidence-weighted margin `m_edge_conf(t)`.

Only after the same five-shot panel is retested with confidence weighting can the project decide whether to continue toward a broader TokaMark panel or stop as a bounded pilot study.
