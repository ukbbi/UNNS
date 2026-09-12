# UNNS Color Confinement — Boundary-Pressure Proxy Definition

**Report:** 09_boundary_pressure_proxy_definition.md  
**Program:** UNNS Substrate / Color Confinement Regime Synthesis  
**Status:** Definition note, not a fitted law  
**Version:** v0.1.0  
**Prepared after:** 06_chamber_alignment_report.md, 07_static_repair_window_chamber_report.md, 08_color_confinement_chamber_synthesis.md  

---

## 1. Purpose

The previous color-confinement reports established three separate evidence tracks:

```
01 First Confinement Diagnostic
02 Repair-Threshold Analysis
03 Flux-Tube Separation Extension
06 Chamber Alignment
07 Static Repair-Window Chamber Report
08 Color Confinement Chamber Synthesis
```

These tracks show that color confinement can be treated, within the UNNS Substrate framework, as a benchmark for:

```
admissibility-by-closure
repair-threshold behavior
localized route geometry
chamber-stable ordered ladders
```

What is still missing is a single derived variable that measures:

```
how much boundary pressure is accumulating near the repair threshold
```

This note defines that variable symbolically.

The proposed object is:

```
Π_boundary(r)
```

where `r` is the static color-source separation.

This proxy is not yet a universal confinement law.  
It is a controlled UNNS diagnostic variable built from already curated static-spectrum and flux-tube observables.

---

## 2. What the proxy adds

The boundary-pressure proxy adds a bridge between the physical diagnostics and the chamber outputs.

Before this proxy, the project has separate quantities:

```
static energy levels:          V0(r), V1(r), V2(r)
channel gaps:                  Δ01(r), Δ12(r)
repair markers:                r_c, r_cs
flux-tube observables:          peak, width, area
STRUC-I result:                admissibility class
STRUC-PERC-I result:            connectivity / fragmentation class
```

The proxy combines them into one UNNS diagnostic:

```
localized route geometry
+
repair-window channel competition
+
threshold proximity
+
gap compression
=
boundary-pressure proxy
```

The intended interpretation is:

```
low Π_boundary(r)
  route extension is away from repair pressure

rising Π_boundary(r)
  route tension and channel competition are increasing

high Π_boundary(r)
  the system is near an admissible repair transition into color-neutral composite routes
```

---

## 3. What it is based on

The proxy is based only on already curated material in the current color-confinement package.

### 3.1 Static repair-window data

Primary static inputs:

```
reports/repair_threshold_window_static_gaps.csv
```

Derived chamber ladders:

```
chamber_inputs/static_gap01_repair_window_ladder.csv
chamber_inputs/static_gap12_repair_window_ladder.csv
```

Definitions:

```
Δ01(r) = V1(r) − V0(r)
Δ12(r) = V2(r) − V1(r)
```

Interpretation:

```
Δ01(r)
  lower channel separation / first excitation gap

Δ12(r)
  upper channel separation / next channel gap
```

These quantities describe how the low-lying static-source spectrum reorganizes in the threshold window.

### 3.2 Repair markers

The repair-window analysis uses the two reported threshold markers:

```
r_c   = light static-light repair threshold
r_cs  = strange static-strange repair threshold
```

In the current diagnostic chain, these are not treated as free-color escape points. They are treated as repair-window markers:

```
stretched color route
→ threshold-window approach
→ competing screened channel
→ repaired admissible color-neutral route
```

### 3.3 Flux-tube trusted trend data

Primary trusted flux summary:

```
reports/baker_flux_profile_trusted_summary.csv
```

Derived chamber ladders:

```
chamber_inputs/flux_FULL_peak_trusted_ladder.csv
chamber_inputs/flux_NP_peak_trusted_ladder.csv
chamber_inputs/flux_FULL_width_trusted_ladder.csv
chamber_inputs/flux_NP_width_trusted_ladder.csv
chamber_inputs/flux_FULL_area_trusted_ladder.csv
chamber_inputs/flux_NP_area_trusted_ladder.csv
```

Interpretation:

```
peak
  local central route intensity

width
  transverse route spread

area
  route-integral / total localized field proxy
```

Only QC-accepted FULL/NP rows are admissible for the main proxy construction.

### 3.4 Chamber outputs

The proxy is motivated by the chamber pattern already observed:

```
STRUC-I:
  tested flux and static repair-window ladders are admissible / stable

STRUC-PERC-I:
  global route-integral measures tend to be connected
  local peak / width / upper-channel descriptors can fragment
```

Therefore, the proxy should not collapse all observables into one undifferentiated number. It must preserve the difference between:

```
global route coherence
local shape sensitivity
upper-channel fragmentation
repair-window proximity
```

---

## 4. Working definition

The boundary-pressure proxy is defined as a weighted normalized sum:

```
Π_boundary(r)
=
w_gap · C_gap(r)
+
w_thr · C_threshold(r)
+
w_slope · C_slope(r)
+
w_flux · C_flux(r)
```

with:

```
w_gap + w_thr + w_slope + w_flux = 1
```

Initial neutral weights:

```
w_gap   = 0.35
w_thr   = 0.30
w_slope = 0.20
w_flux  = 0.15
```

These weights are provisional. They are not fitted.

They only express the current methodological priority:

```
static channel gaps         strongest input
threshold proximity         essential repair coordinate
local slope / curvature     repair-window sharpening signal
flux geometry               optional supporting geometry
```

---

## 5. Component definitions

### 5.1 Gap-compression component

Let:

```
Δ01(r) = V1(r) − V0(r)
Δ12(r) = V2(r) − V1(r)
```

Define normalized compression scores:

```
G01(r) = 1 − norm[Δ01(r)]
G12(r) = 1 − norm[Δ12(r)]
```

where `norm[x]` maps the available repair-window values of `x` into `[0, 1]`.

Then:

```
C_gap(r) = 0.5 · G01(r) + 0.5 · G12(r)
```

Interpretation:

```
small channel gaps
→ stronger compression
→ higher boundary pressure
```

If one gap channel is unavailable, use the available channel alone and mark the row as partial.

---

### 5.2 Threshold-proximity component

Let the two threshold markers be:

```
r_c
r_cs
```

Define the nearest threshold distance:

```
d_thr(r) = min(|r − r_c|, |r − r_cs|)
```

Choose a repair-window width `W_thr`.

Default:

```
W_thr = max(|r_cs − r_c|, median spacing of available r values)
```

Then:

```
C_threshold(r) = clip(1 − d_thr(r) / W_thr, 0, 1)
```

Interpretation:

```
r far from threshold
→ C_threshold close to 0

r near r_c or r_cs
→ C_threshold close to 1
```

This component turns the repair markers into a local boundary coordinate.

---

### 5.3 Slope / sharpening component

Define local gap-slope magnitudes:

```
S01(r) = |dΔ01 / dr|
S12(r) = |dΔ12 / dr|
```

In tabular implementation, use finite differences:

```
S01_i = |Δ01_{i+1} − Δ01_{i-1}| / |r_{i+1} − r_{i-1}|
S12_i = |Δ12_{i+1} − Δ12_{i-1}| / |r_{i+1} − r_{i-1}|
```

Then normalize both into `[0, 1]`:

```
N01(r) = norm[S01(r)]
N12(r) = norm[S12(r)]
```

and define:

```
C_slope(r) = 0.5 · N01(r) + 0.5 · N12(r)
```

Interpretation:

```
rapid gap reorganization near threshold
→ stronger local boundary-pressure signal
```

If the finite-difference stencil is unavailable at endpoints, use one-sided differences and mark the row as endpoint-derived.

---

### 5.4 Flux-localization component

The flux component is optional in v0.1 because the trusted Baker flux-tube range and the static repair-window range are not identical.

If a flux row can be matched or interpolated to a static separation `r`, define:

```
F_peak(r)  = normalized peak field strength
F_width(r) = normalized transverse width
F_area(r)  = normalized profile area
```

A conservative flux-localization score is:

```
C_flux(r)
=
0.40 · F_area(r)
+
0.30 · F_peak(r)
+
0.30 · F_width(r)
```

Interpretation:

```
area
  global routed field strength

peak
  local central intensity

width
  transverse route spread
```

If no matched flux profile is available:

```
C_flux(r) = null
```

and the total proxy is renormalized over the available components.

---

## 6. Renormalized proxy for missing components

Because not all rows have flux support, define the computable proxy as:

```
Π_boundary_available(r)
=
sum over available components [w_i · C_i(r)]
/
sum over available weights [w_i]
```

This prevents missing flux data from artificially lowering the pressure score.

Example:

```
If C_flux is unavailable:

Π_boundary_available(r)
=
(w_gap · C_gap + w_thr · C_threshold + w_slope · C_slope)
/
(w_gap + w_thr + w_slope)
```

---

## 7. Interpretation bands

Initial qualitative bands:

```
0.00 ≤ Π < 0.25
  relaxed route extension

0.25 ≤ Π < 0.50
  mild boundary tension

0.50 ≤ Π < 0.75
  active repair-window pressure

0.75 ≤ Π ≤ 1.00
  high boundary pressure / near-repair condition
```

These bands are descriptive only.

They are not calibrated physical thresholds.

---

## 8. Expected output table

The future computed proxy table should be stored as:

```
data/08_boundary_pressure_proxy/boundary_pressure_proxy_table.csv
```

or, if treated as a derived analysis product rather than source data:

```
reports/boundary_pressure_proxy_table.csv
```

Recommended columns:

```csv
r_fm,delta01_GeV,delta12_GeV,C_gap,C_threshold,C_slope,C_flux,Pi_boundary_available,pressure_band,data_status,notes
```

Column meanings:

```
r_fm
  static source separation

delta01_GeV
  V1 − V0 gap

delta12_GeV
  V2 − V1 gap

C_gap
  normalized gap-compression component

C_threshold
  proximity to r_c or r_cs

C_slope
  finite-difference local reorganization score

C_flux
  optional flux-localization score

Pi_boundary_available
  renormalized boundary-pressure proxy

pressure_band
  qualitative interpretation band

data_status
  e.g. STATIC_ONLY, STATIC_PLUS_FLUX_INTERPOLATED, ENDPOINT_DERIVED

notes
  provenance and caveats
```

---

## 9. Chamber-input consequence

Once the proxy table is computed, generate the ladder:

```
chamber_inputs/boundary_pressure_proxy_ladder.csv
```

This ladder should contain only:

```csv
value
0.1234
0.1851
...
```

where `value` is the ordered set of `Π_boundary_available(r)` values.

Then run:

```
STRUC-I
  admissibility and pressure profile

STRUC-PERC-I
  gap-connectivity / fragmentation profile
```

Expected next output paths:

```
chamber_outputs/STRUC_I/raw_exports/struc_i_boundary_pressure_proxy_results.json
chamber_outputs/STRUC_I/summary_tables/struc_i_boundary_pressure_proxy_profiles.csv

chamber_outputs/STRUC_PERC_I/raw_exports/struc_perc_boundary_pressure_proxy_results.json
chamber_outputs/STRUC_PERC_I/summary_tables/struc_perc_boundary_pressure_proxy_summary.csv
```

---

## 10. Methodological boundary

This definition does not claim that UNNS derives QCD confinement.

It defines a structural diagnostic object.

The proxy is allowed to support statements such as:

```
The repair-window region has high boundary-pressure score under the chosen normalization.

The boundary-pressure proxy is STRUC-I admissible or non-admissible under perturbation.

The proxy ladder is STRUC-PERC-I connected, tail-fragmented, or hard-fragmented.

The proxy aligns or fails to align with previously observed flux and static gap chamber behavior.
```

It is not allowed to support statements such as:

```
UNNS proves confinement.

Π_boundary is a physical QCD potential.

Π_boundary replaces lattice QCD observables.

The numerical weights are universal.
```

---

## 11. Current status

At v0.1, the proxy is formally defined but not yet computed.

The next executable work item is:

```
scripts/compute_boundary_pressure_proxy.py
```

That script should read:

```
reports/repair_threshold_window_static_gaps.csv
reports/baker_flux_profile_trusted_summary.csv
```

and produce:

```
reports/boundary_pressure_proxy_table.csv
chamber_inputs/boundary_pressure_proxy_ladder.csv
```

The proxy ladder can then be tested in the chambers.

---

## 12. Summary statement

The boundary-pressure proxy is the first explicit scalar UNNS object extracted from the color-confinement regime synthesis.

It converts the previously separate diagnostics:

```
static gap compression
threshold proximity
finite-difference repair-window sharpening
optional flux-tube localization
```

into:

```
Π_boundary(r)
```

This creates a testable bridge from the physical confinement data to the UNNS chamber machinery.

The value of the proxy is not that it proves confinement.

Its value is that it gives the project a disciplined next object:

```
a computable, provenance-bound, chamber-testable boundary-pressure ladder
```
