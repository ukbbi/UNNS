# UNNS Cross-Regime Boundary-Pressure Comparison Plan

**Report:** 12_cross_regime_boundary_pressure_comparison_plan.md  
**Program:** UNNS Substrate / Phase II — Cross-Regime Boundary-Pressure Comparison  
**Regime A:** Color confinement / QCD-inspired confinement benchmark  
**Regime B:** H-mode plasma confinement / L-H transition edge-admissibility  
**Law-level bridge:** Charge Boundary-Route Preservation Law  
**Status:** Phase II planning document  
**Purpose:** define the first cross-regime comparison protocol for UNNS boundary pressure, route preservation, and admissibility-by-closure  

---

## 1. Executive purpose

Phase I established color confinement as a completed UNNS regime-template case:

```
physical diagnostic
→ curated ladder
→ chamber classification
→ derived boundary-pressure proxy
→ STRUC-I stable
→ STRUC-PERC-I fully connected
```

The key completed object was:

```
Π_boundary(r)
```

constructed from static repair-window gap compression, threshold proximity, and local sharpening.

The Phase I result was:

```
Π_boundary(r)

STRUC-I:
  Geometric Persistence / Stable Structure

STRUC-PERC-I:
  FULL_PERCOLATION
```

Phase II asks whether this result is isolated to color confinement or whether a related boundary-pressure architecture appears across physically different confinement systems.

The first comparison target is H-mode plasma confinement, because the uploaded H-mode corpus already defines the analogous UNNS object:

```
m_edge,event = C_edge − F_route
```

and its time-resolved extension:

```
m_edge,conf(t)
```

The central Phase II question is therefore:

```
Is boundary pressure a reusable UNNS structural coordinate across physically
different confinement systems?
```

---

## 2. Why H-mode is the correct second regime

H-mode is not just another dataset. It is structurally aligned with color confinement.

Color confinement has:

```
colored constituent
→ non-externalizable isolated color route
→ localized flux-tube route tension
→ repair threshold / string breaking
→ admissible color-neutral composite closure
```

H-mode plasma has:

```
L-mode leakage
→ route-fragmentation pressure
→ L-H transition / admissibility crossing
→ edge-route preservation
→ H-mode confinement state
```

Both regimes contain:

```
route extension
boundary pressure
threshold crossing
local descriptor instability
global route-preserving coordinate
admissible post-threshold state
```

H-mode is therefore the natural Regime B for the first cross-regime boundary-pressure comparison.

---

## 3. Source basis

### 3.1 Regime A — Color confinement

The color-confinement track has completed the following reports:

```
01 First Confinement Diagnostic
02 Repair-Threshold Analysis
03 Flux-Tube Separation Extension
04 Baker Flux Extension QC
05 Baker Review-Separately Rows
06 Chamber Alignment Report
07 Static Repair-Window Chamber Report
08 Color Confinement Chamber Synthesis
09 Boundary-Pressure Proxy Definition
10 Boundary-Pressure Proxy Chamber Report
11 Color Confinement Final Synthesis
```

The completed Regime A object is:

```
Π_boundary(r)
```

with chamber result:

```
STRUC-I:
  Geometric Persistence / Stable Structure

STRUC-PERC-I:
  FULL_PERCOLATION
```

### 3.2 Regime B — H-mode plasma

Primary source:

```
Boundary-Route Preservation in H-Mode Plasma.pdf
```

This source defines the event-level edge-admissibility margin:

```
m_edge,event = C_edge − F_route
```

where:

```
F_route
  route-fragmentation pressure

C_edge
  edge-preserving capacity
```

The source also defines a time-resolved and diagnostic-confidence-corrected version:

```
m_edge,conf(t)
```

The H-mode manuscript reports:

```
TCV nine-shot pilot:
  three strictly non-overlapping corridors

TCV 92-event full-corpus extension:
  persistent three-corridor structure
  AUC = 0.690
  permutation p = 0.0022

TokaMark / MAST physical-window recovery:
  l_mode < lh_transition < h_mode_stable
  positive H-minus-L deltas in all five recovered H-mode-stable cases
```

### 3.3 Law-level bridge

Primary source:

```
Charge Boundary-Route Preservation Law.pdf
```

Core statement:

```
charge balance is the visible projection;
boundary-route preservation is the structural invariant.
```

For Phase II this becomes the cross-regime principle:

```
observable threshold access is the visible projection;
boundary-route preservation is the structural invariant.
```

---

## 4. Cross-regime comparison table

| Coordinate | Color confinement | H-mode plasma | Charge-boundary law |
|---|---|---|---|
| Visible projection | color-neutral hadrons / absence of free color | ILH label / H-mode access / threshold crossing | scalar charge conservation |
| Hidden route coordinate | color route / flux-tube route | edge route / confinement route | charge route / closure tuple |
| Route-extension coordinate | static-source separation `r` | event index / time window `t` | transition tuple |
| Pressure term | gap compression, threshold proximity, slope sharpening | `F_route` fragmentation pressure | forbidden / constrained boundary pressure |
| Capacity / closure term | color-neutral composite closure | `C_edge` edge-preserving capacity | route/closure coherence |
| Boundary event | string breaking / repair threshold | L-H transition | admissibility or transition boundary |
| Local descriptors | flux peak, width, area; static gaps | power, transport, timing, edge-response channels | charge value, route code, closure code |
| Derived global coordinate | `Π_boundary(r)` | `m_edge,event`, `m_edge,conf(t)` | boundary-route admissibility |
| Chamber outcome target | stable + fully connected proxy | test margin ladders for stability/connectivity | route admissibility vs graph connectivity |
| UNNS interpretation | admissibility-by-closure | boundary-route preservation | value projection vs route invariant |

---

## 5. Shared structural hypothesis

The Phase II hypothesis is:

```
Different confinement systems may have fragmented local descriptors, but their
properly constructed boundary-pressure or edge-admissibility coordinate should
stabilize into an admissible and connected UNNS ladder.
```

In compact form:

```
local descriptors may fragment
global boundary-pressure coordinate should stabilize
```

For color confinement this has already been observed:

```
flux peak / width
→ admissible but sometimes fragmented

static gap12
→ admissible but fragmented

Π_boundary(r)
→ stable and fully connected
```

For H-mode plasma this must now be tested chamber-wise using:

```
m_edge,event
m_edge,conf(t)
C_edge
F_route
state-corridor encodings
```

---

## 6. Comparison variables

The cross-regime comparison requires variables in four families.

### 6.1 Pressure variables

Color confinement:

```
C_gap(r)
C_threshold(r)
C_slope(r)
Π_boundary(r)
```

H-mode plasma:

```
F_route
S_power_balance
S_transport
S_timing
```

Charge-boundary law:

```
boundary_pressure_index
forbiddenness / constraint status
route-incoherence flag
free-fractional externalization pressure
```

### 6.2 Capacity / closure variables

Color confinement:

```
color-neutral closure
screened channel
composite route
```

H-mode plasma:

```
C_edge
S_edge_response
density support
geometry support
species support
```

Charge-boundary law:

```
route_transition_code
closure_transition_code
route/closure coherence
```

### 6.3 Margin variables

Color confinement:

```
Π_boundary(r)
```

H-mode plasma:

```
m_edge,event = C_edge − F_route
m_edge,conf(t)
```

Charge-boundary law:

```
admissibility status
route-transition stability
```

### 6.4 Chamber variables

For each regime, record:

```
STRUC-I regime
STRUC-I state
mean Aκ
min Aκ
Aκ at κmax
mean ρ
max ρ

STRUC-PERC-I verdict
giantRatio
isolated
isolatedFraction
κ_connect
tailDominance
```

---

## 7. Required Phase II data products

Create a new folder:

```
phase_II_cross_regime_boundary_pressure/
```

Recommended structure:

```
phase_II_cross_regime_boundary_pressure/
├── README.md
├── regime_registry.csv
├── comparison_tables/
│   ├── cross_regime_variable_map.csv
│   ├── cross_regime_chamber_summary.csv
│   ├── cross_regime_pressure_capacity_summary.csv
│   └── cross_regime_transition_map.csv
│
├── chamber_inputs/
│   ├── color/
│   │   └── boundary_pressure_proxy_ladder.csv
│   ├── hmode/
│   │   ├── hmode_m_edge_event_ladder.csv
│   │   ├── hmode_C_edge_ladder.csv
│   │   ├── hmode_F_route_ladder.csv
│   │   └── hmode_m_edge_conf_window_ladder.csv
│   └── charge_boundary/
│       ├── route_transition_code_ladder.csv
│       ├── closure_transition_code_ladder.csv
│       └── boundary_pressure_index_ladder.csv
│
├── chamber_outputs/
│   ├── STRUC_I/
│   └── STRUC_PERC_I/
│
├── scripts/
│   ├── build_cross_regime_registry.py
│   ├── extract_hmode_margin_ladders.py
│   ├── build_cross_regime_chamber_summary.py
│   └── make_cross_regime_figures.py
│
└── reports/
    ├── 13_hmode_margin_ladder_extraction.md
    ├── 14_cross_regime_chamber_alignment.md
    └── 15_cross_regime_boundary_pressure_synthesis.md
```

Do not mix this with the color-confinement seed package. This is a higher-level comparison layer.

---

## 8. Regime registry schema

Create:

```
phase_II_cross_regime_boundary_pressure/regime_registry.csv
```

Recommended columns:

```
regime_id,regime_name,domain,route_coordinate,pressure_coordinate,capacity_coordinate,margin_coordinate,transition_marker,primary_source,status
```

Rows:

```
color_confinement,Color confinement,QCD-inspired confinement,r,Pi_boundary components,color-neutral closure,Pi_boundary,string breaking / repair threshold,11_color_confinement_final_synthesis.md,COMPLETE
hmode_plasma,H-mode plasma,magnetic confinement,time/event window,F_route,C_edge,m_edge_event / m_edge_conf,L-H transition,Boundary-Route Preservation in H-Mode Plasma.pdf,READY_FOR_EXTRACTION
charge_boundary,Charge boundary routing,charge-bearing transitions,transition tuple,boundary pressure / forbiddenness,route-closure coherence,route admissibility,allowed-forbidden boundary,Charge Boundary-Route Preservation Law.pdf,LAW_LEVEL_BRIDGE
```

---

## 9. First executable task

The first executable Phase II task is not another manuscript.

It is:

```
extract H-mode margin ladders
```

Create:

```
scripts/extract_hmode_margin_ladders.py
```

It should read the H-mode analysis outputs or canonical event/window tables and produce:

```
chamber_inputs/hmode/hmode_m_edge_event_ladder.csv
chamber_inputs/hmode/hmode_C_edge_ladder.csv
chamber_inputs/hmode/hmode_F_route_ladder.csv
chamber_inputs/hmode/hmode_m_edge_conf_window_ladder.csv
```

Each ladder must be a one-column CSV:

```
value
...
```

Do not run the whole H-mode dashboard through the chambers. Extract declared numeric ladders only.

---

## 10. First chamber tests for Phase II

Run STRUC-I and STRUC-PERC-I on:

```
hmode_m_edge_event_ladder.csv
hmode_C_edge_ladder.csv
hmode_F_route_ladder.csv
hmode_m_edge_conf_window_ladder.csv
```

Expected interpretation targets:

```
m_edge_event / m_edge_conf
  should show strongest global stability if the margin is a true boundary coordinate

F_route
  may show fragmentation or boundary-sensitive behavior

C_edge
  may show stabilization if edge-response capacity is organized

state/window ladders
  should not be overinterpreted if categorical encodings are used
```

---

## 11. Comparison test

The first comparison test is:

```
Does H-mode reproduce the color-confinement pattern?
```

Color-confinement pattern:

```
local descriptors:
  mixed connectivity / some fragmentation

derived proxy:
  STRUC-I stable
  STRUC-PERC-I fully connected
```

H-mode expected test:

```
local components:
  power / transport / timing / edge-response may differ in chamber behavior

derived margin:
  m_edge_event or m_edge_conf should be more coherent than the fragmented inputs
```

If this holds, then the Phase II cross-regime claim becomes:

```
Boundary-pressure coordinates stabilize across distinct confinement regimes.
```

If it fails, the outcome is still useful:

```
Color confinement and H-mode require different boundary-pressure geometries.
```

---

## 12. Formal comparison metric

Define a cross-regime stability score:

```
S_cross(regime)
=
0.5 · A_STRUC-I_margin
+
0.5 · G_STRUC-PERC-I_margin
```

where:

```
A_STRUC-I_margin
  normalized STRUC-I mean Aκ of the regime's derived margin / proxy

G_STRUC-PERC-I_margin
  giantRatio of the regime's derived margin / proxy
```

For color confinement:

```
A_STRUC-I_margin = 1.000000
G_STRUC-PERC-I_margin = 1.000000

S_cross(color) = 1.000000
```

For H-mode:

```
S_cross(hmode)
```

must be computed after H-mode margin ladders are chamber-tested.

---

## 13. Interpretation bands

For `S_cross`:

```
0.90–1.00
  strong cross-regime boundary-coordinate stability

0.75–0.90
  moderate boundary-coordinate stability

0.50–0.75
  weak or partial boundary-coordinate stability

< 0.50
  no current evidence of reusable boundary-coordinate stability
```

These are methodological bands, not physical constants.

---

## 14. Expected findings to test

### Finding target A — derived margin stabilization

```
The derived margin/proxy should be more chamber-stable than at least some of its local components.
```

Color confinement:

```
Π_boundary(r) stabilizes relative to flux peak/width and gap12 fragmentation.
```

H-mode test:

```
m_edge_event or m_edge_conf should stabilize relative to power/transport/timing components.
```

### Finding target B — threshold ordering

Color confinement:

```
repair-window pressure organizes around r_c and r_cs.
```

H-mode:

```
m_edge_conf orders l_mode < lh_transition < h_mode_stable.
```

### Finding target C — route preservation

Color confinement:

```
external admissibility requires color-neutral closure.
```

H-mode:

```
sustained confinement requires edge-route preservation.
```

Charge law:

```
charge balance alone is insufficient; route preservation is structural invariant.
```

---

## 15. Non-claims

Phase II must not claim:

```
UNNS derives QCD confinement.
UNNS derives H-mode physics.
Π_boundary and m_edge are the same physical quantity.
The H-mode margin outperforms standard plasma predictors.
Boundary pressure is already universal.
```

The allowed claim is:

```
Color confinement and H-mode plasma confinement can be compared using a
shared UNNS boundary-route template, and their derived margin/proxy ladders
can be tested for stability and connectivity under the same chamber protocol.
```

---

## 16. Deliverables

Minimum Phase II deliverables:

```
12_cross_regime_boundary_pressure_comparison_plan.md
regime_registry.csv
cross_regime_variable_map.csv
extract_hmode_margin_ladders.py
hmode chamber input ladders
hmode STRUC-I outputs
hmode STRUC-PERC-I outputs
14_cross_regime_chamber_alignment.md
15_cross_regime_boundary_pressure_synthesis.md
```

Optional visual artifacts:

```
cross_regime_boundary_pressure_map.png
cross_regime_chamber_alignment_table.png
boundary_route_template_diagram.svg
```

Optional Joomla artifacts:

```
phase_II_cross_regime_boundary_pressure_dashboard.html
UNNS Boundary Pressure Across Confinement Regimes article
```

---

## 17. Immediate next action

The immediate next action is:

```
create the Phase II folder and registry
```

Then write:

```
phase_II_cross_regime_boundary_pressure/README.md
phase_II_cross_regime_boundary_pressure/regime_registry.csv
phase_II_cross_regime_boundary_pressure/comparison_tables/cross_regime_variable_map.csv
```

After that, extract H-mode margin ladders.

---

## 18. Summary statement

Phase II begins with a clean comparison:

```
Color confinement:
  Π_boundary(r)
  stable and fully connected

H-mode plasma:
  m_edge,event / m_edge,conf(t)
  ready for chamber extraction and comparison
```

The governing question is:

```
Do boundary-pressure coordinates stabilize across distinct confinement regimes?
```

If yes, the UNNS program gains its first cross-regime boundary-pressure invariant.

If no, the comparison still identifies where confinement regimes diverge structurally.
