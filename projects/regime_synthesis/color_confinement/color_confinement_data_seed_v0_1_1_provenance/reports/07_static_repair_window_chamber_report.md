# 07 Static Repair-Window Chamber Report — Color Confinement
**UNNS Substrate / Color Confinement Workstream**  
**Report file:** `reports/07_static_repair_window_chamber_report.md`  
**Inputs:** static repair-window gap ladders generated from the reconstructed Bulava threshold-window diagnostic  
**Chambers used:** STRUC-I v1.0.4 and STRUC-PERC-I v2.5.0
---
## 1. Purpose
This report records the second chamber pass for the color-confinement workstream. The first chamber pass tested Baker flux-tube route-localization ladders. This pass tests the two static repair-window gap ladders:
```
static_gap01_repair_window_ladder.csv
static_gap12_repair_window_ladder.csv
```
These ladders address a different question from the flux-profile ladders:
```
flux ladders        -> route-localization geometry
static gap ladders  -> repair-threshold channel competition
```
The chamber stage does not test QCD directly. It tests whether the extracted static-gap structures behave as admissible ordered ladders and what connectivity class their gap geometry occupies.
---
## 2. Source files used
Store the source outputs as:
```
chamber_outputs/STRUC_I/raw_exports/struc_i_static_repair_window_results.json
chamber_outputs/STRUC_I/summary_tables/struc_i_static_repair_window_profiles.csv
chamber_outputs/STRUC_PERC_I/raw_exports/struc_perc_static_repair_window_results.json
chamber_outputs/STRUC_PERC_I/summary_tables/struc_perc_static_repair_window_summary.csv
```
STRUC-I run settings:
```
kappa range: 0.01 -> 1
kappa steps: 40
Monte Carlo runs: 2000
perturbation: δᵢ ~ Uniform[-ε, ε]
scale: ε = κ · median(gaps)
inequality: inv(P_ε; L) ≤ ν(V_ε(L))
```
---
## 3. Alignment table
| Ladder | STRUC-I n | STRUC-I class | mean Aκ | min Aκ | mean ρ | max ρ | STRUC-PERC-I verdict | giant ratio | isolated | tail dominance | κ_connect |
|---|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| `static_gap01_repair_window_ladder` | 17 | Geometric Persistence / Stable Structure | 0.998487 | 0.9740 | 0.179775 | 0.562000 | FULL_PERCOLATION | 1.000000 | 0 | 0.570349 | 10 |
| `static_gap12_repair_window_ladder` | 17 | Geometric Persistence / Stable Structure | 1.000000 | 1.0000 | 0.089607 | 0.421167 | HARD_FRAGMENTATION | 0.941176 | 1 | 0.000000 | — |

---
## 4. STRUC-I reading: both repair-window gap ladders are stable
STRUC-I classifies both repair-window gap ladders as:
```
Geometric Persistence / Stable Structure
```
- `static_gap01_repair_window_ladder`: mean Aκ = **0.998487**, min Aκ = **0.9740**, mean ρ = **0.179775**.
- `static_gap12_repair_window_ladder`: mean Aκ = **1.000000**, min Aκ = **1.0000**, mean ρ = **0.089607**.

This is stronger than the flux-profile pass, where the trusted flux ladders were Geometric Persistence / Weak Persistence. Here, the threshold-window gap ladders remain well within the STRUC-I admissibility budget.

UNNS reading:
```
repair-window channel gaps
-> admissible ordered threshold descriptors
-> stable under STRUC-I perturbation
```
---
## 5. STRUC-PERC-I reading: gap01 percolates, gap12 fragments narrowly
STRUC-PERC-I separates the two static gap ladders:

### 5.1 gap01: fully connected
`static_gap01_repair_window_ladder.csv` reaches FULL_PERCOLATION with giant ratio = 1.0, isolated = 0, and κ_connect = 10.

UNNS reading:
```
V1 - V0 repair-window gap sequence
-> globally connected low-channel competition geometry
```

### 5.2 gap12: stable but connectivity-fragmented
`static_gap12_repair_window_ladder.csv` is HARD_FRAGMENTATION in STRUC-PERC-I, with giant ratio ≈ 0.941176 and one isolated gap vertex. Tail dominance is 0 in this run, so the fragmentation is not an outlier-tail effect under the exported PRP diagnostic.

UNNS reading:
```
V2 - V1 repair-window gap sequence
-> admissible under STRUC-I
-> nearly connected but PRP-fragmented gap geometry
-> possible marker of secondary-channel stiffness or transition asymmetry
```
---
## 6. Main chamber-alignment finding
The repair-window gap ladders are both STRUC-I stable, but STRUC-PERC-I distinguishes the lower and upper channel-gap geometries. The lower gap sequence, V1 - V0, is globally connected. The upper gap sequence, V2 - V1, remains fully admissible under STRUC-I but fails full PRP connectivity by a narrow margin.

The compact result is:
```
static_gap01_repair_window_ladder
-> Stable Structure + FULL_PERCOLATION
-> coherent repair-window channel competition

static_gap12_repair_window_ladder
-> Stable Structure + HARD_FRAGMENTATION
-> admissible but connectivity-asymmetric upper-channel geometry
```
This strengthens the repair-threshold interpretation: the threshold window is not disordered. It is structurally stable under perturbation, while still carrying channel-specific connectivity asymmetry.
---
## 7. Relation to the confinement synthesis
The earlier repair-threshold diagnostic treated the reported string-breaking thresholds as markers of route repair rather than free-color externalization. This chamber pass adds a structural stress test to that interpretation:
```
reported repair-window gap behavior
-> converted into ordered ladders
-> STRUC-I Stable Structure
-> STRUC-PERC-I channel-specific connectivity class
```
So the repair-window object is now more concrete:
```
stretched color route
-> threshold-window approach
-> stable channel-competition ladder
-> asymmetric connectivity between lower and upper gap channels
-> repaired admissible color-neutral composite route
```
---
## 8. What is supported
Supported by this chamber pass:
```
1. Both static repair-window ladders are STRUC-I Stable Structure.
2. The V1 - V0 gap ladder is fully connected under STRUC-PERC-I.
3. The V2 - V1 gap ladder is admissible but PRP-fragmented with one isolated vertex.
4. The repair-window region behaves like an ordered, chamber-testable UNNS structure rather than a noisy transition.
```
---
## 9. What is not yet supported
Not yet supported:
```
1. A derivation of QCD confinement from UNNS.
2. A final physical interpretation of the gap12 HARD_FRAGMENTATION verdict.
3. A measured-point chamber test using raw V0(r), V1(r), V2(r) GEVP lattice values.
4. A covariance-aware static repair-window analysis.
5. A fitted UNNS boundary-pressure law.
```
The static levels used in the earlier diagnostic remain model-reconstructed from reported parameters, not raw measured pointwise lattice data. The chamber result should therefore be read as a structural diagnostic of the reconstructed repair-window model.
---
## 10. Next work item
Update the synthesis with a chamber-level distinction:
```
flux route geometry:
  admissible, with area/NP peak more connected than local width/FULL peak

static repair-window gaps:
  stable under STRUC-I, with gap01 connected and gap12 narrowly PRP-fragmented
```
Then build a combined report:
```
reports/08_color_confinement_chamber_synthesis.md
```
This should combine the flux-ladder chamber report and the static repair-window chamber report.
---
## 11. One-line conclusion
The static repair-window chamber pass shows that reconstructed string-breaking gap ladders are STRUC-I stable, while STRUC-PERC-I reveals a channel-specific distinction: the lower repair-window gap is globally connected, and the upper gap is admissible but narrowly fragmented in PRP connectivity.
