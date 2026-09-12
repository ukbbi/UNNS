# 06 Chamber Alignment Report — Color Confinement Flux Ladders

**UNNS Substrate / Color Confinement Workstream**  
**Report file:** `reports/06_chamber_alignment_report.md`  
**Inputs:** trusted Baker flux-tube chamber ladders generated from QC-accepted FULL / NP rows only  
**Chambers used:** STRUC-I v1.0.4 and STRUC-PERC-I v2.5.0

---

## 1. Purpose

This report aligns the first color-confinement chamber outputs with the prior diagnostic chain:

```
01 First Confinement Diagnostic
02 Repair-Threshold Analysis
03 Flux-Tube Separation Extension
04 Baker Flux Extension QC
05 Review-Separately Rows
Regime Synthesis Note
```

The chamber stage does **not** test QCD directly. It tests whether confinement-derived observables, after QC and conversion into ordered ladders, occupy recognizable UNNS structural regimes.

The specific question is:

> Do trusted flux-tube route observables behave as admissible ordered ladders under STRUC-I, and how connected are their gap structures under STRUC-PERC-I?

---

## 2. Source files used

```
chamber_outputs/STRUC_I/raw_exports/chamber_struc_i_v1_0_4_results.json
chamber_outputs/STRUC_I/summary_tables/chamber_struc_i_v1_0_4_profiles.csv
chamber_outputs/STRUC_PERC_I/raw_exports/struc_perc_batch_results.json
chamber_outputs/STRUC_PERC_I/summary_tables/struc_perc_batch_results.csv
```

The STRUC-I run used:

```
kappa range: 0.01 → 1.0
kappa steps: 40
Monte Carlo runs: 2000
perturbation: δᵢ ~ Uniform[-ε, ε]
scale: ε = κ · median(gaps)
inequality: inv(P_ε; L) ≤ ν(V_ε(L))
```

The STRUC-PERC-I batch run used the six trusted flux ladders exported from `chamber_inputs/`.

---

## 3. Chamber-input ladders tested

Only QC-accepted trusted FULL / NP flux-profile summaries were used:

```
flux_FULL_area_trusted_ladder.csv
flux_FULL_peak_trusted_ladder.csv
flux_FULL_width_trusted_ladder.csv
flux_NP_area_trusted_ladder.csv
flux_NP_peak_trusted_ladder.csv
flux_NP_width_trusted_ladder.csv
```

The `PAPER_DEFINED`, large-distance, wide/outlier, and single-point summary rows were **not** included in this chamber alignment. They remain separate controls or later-normalization candidates.

---

## 4. Alignment table

| Ladder | STRUC-I n | STRUC-I class | mean Aκ | min Aκ | mean ρ | max ρ | STRUC-PERC-I verdict | giant ratio | isolated | tail dominance | κ_connect |
|---|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| `flux_FULL_area_trusted_ladder` | 15 | Geometric Persistence / Weak Persistence | 0.999962 | 0.9990 | 0.416638 | 0.5205 | FULL_PERCOLATION | 1.000000 | 0 | 0.688785 | 40.024 |
| `flux_FULL_peak_trusted_ladder` | 15 | Geometric Persistence / Weak Persistence | 0.958263 | 0.8605 | 0.597430 | 0.9405 | HARD_FRAGMENTATION | 0.857143 | 2 | 0.505134 | — |
| `flux_FULL_width_trusted_ladder` | 15 | Geometric Persistence / Weak Persistence | 0.999987 | 0.9995 | 0.413903 | 0.5022 | HARD_FRAGMENTATION | 0.857143 | 2 | 0.799072 | — |
| `flux_NP_area_trusted_ladder` | 15 | Geometric Persistence / Weak Persistence | 0.999738 | 0.9975 | 0.465831 | 0.5682 | FULL_PERCOLATION | 1.000000 | 0 | 0.623352 | 10.000 |
| `flux_NP_peak_trusted_ladder` | 15 | Geometric Persistence / Weak Persistence | 0.995575 | 0.9805 | 0.491032 | 0.6173 | FULL_PERCOLATION | 1.000000 | 0 | 0.459730 | 4.015 |
| `flux_NP_width_trusted_ladder` | 15 | Geometric Persistence / Weak Persistence | 1.000000 | 1.0000 | 0.438545 | 0.5152 | HARD_FRAGMENTATION | 0.923077 | 1 | 0.753140 | — |

---

## 5. STRUC-I reading: all trusted flux ladders are admissible

STRUC-I classified all six trusted flux ladders as:

```
Geometric Persistence / Weak Persistence
```

This is the first chamber-level admissibility result for the color-confinement dataset. The ladders remain within the STRUC-I perturbation budget across the tested κ-range.

The strongest STRUC-I readings are:

```
flux_NP_width_trusted_ladder   mean Aκ = 1.000000
flux_FULL_width_trusted_ladder mean Aκ = 0.999987
flux_FULL_area_trusted_ladder  mean Aκ = 0.999962
flux_NP_area_trusted_ladder    mean Aκ = 0.999738
flux_NP_peak_trusted_ladder    mean Aκ = 0.995575
flux_FULL_peak_trusted_ladder  mean Aκ = 0.958263
```

The notable pressure case is `flux_FULL_peak_trusted_ladder`: it remains admissible, but with the lowest mean Aκ and the highest max ρ among the six tested ladders.

UNNS reading:

```
trusted flux observables
→ admissible ordered route descriptors
→ not structurally unstable under STRUC-I perturbation
```

---

## 6. STRUC-PERC-I reading: admissible does not mean equally connected

STRUC-PERC-I separates the same six ladders into two groups.

### 6.1 Fully percolating / globally connected group

```
flux_FULL_area_trusted_ladder.csv
flux_NP_area_trusted_ladder.csv
flux_NP_peak_trusted_ladder.csv
```

These reach:

```
giant ratio = 1.0
isolated = 0
verdict = FULL_PERCOLATION
```

Interpretation:

```
area-like routed-field summaries
→ globally connected gap geometry
```

`flux_NP_peak_trusted_ladder.csv` also percolates, suggesting the nonperturbative peak sequence is more globally connected than the FULL peak sequence under this current small trusted dataset.

### 6.2 Hard-fragmented / tail-sensitive group

```
flux_FULL_peak_trusted_ladder.csv
flux_FULL_width_trusted_ladder.csv
flux_NP_width_trusted_ladder.csv
```

These show:

```
flux_FULL_peak:  giant ratio ≈ 0.857143, isolated = 2
flux_FULL_width: giant ratio ≈ 0.857143, isolated = 2
flux_NP_width:   giant ratio ≈ 0.923077, isolated = 1
```

Interpretation:

```
local intensity and transverse-spread descriptors
→ admissible under STRUC-I
→ fragmented in STRUC-PERC-I gap geometry
→ tail-sensitive boundary structure
```

This is not a physical claim that the flux tube fails. It says that the **ordered gap geometry** of local peak/width descriptors is less globally connected than the area or NP-peak ladders.

---

## 7. Main chamber-alignment finding

The confinement-derived flux ladders are **STRUC-I admissible**, but STRUC-PERC-I distinguishes between globally connected and fragmented observable classes.

The core finding is:

> Trusted flux-tube observables form admissible ordered ladders under STRUC-I. However, STRUC-PERC-I separates them into globally connected route-integral ladders and fragmented local-shape ladders. This suggests that color-confinement route geometry is structurally admissible, while local route descriptors such as FULL peak and width carry stronger tail-sensitive boundary structure.

In compact UNNS form:

```
route-area / routed-field integral
→ coherent global route measure
→ percolating gap geometry

route-peak / route-width
→ local shape descriptor
→ admissible but tail-fragmented gap geometry
```

---

## 8. Relation to prior diagnostics

The earlier diagnostics established:

```
separation
→ route tension
→ no free color externalization
→ threshold repair
→ admissible color-neutral composite channel
```

The chamber stage adds:

```
extracted route observables
→ ordered ladders
→ STRUC-I admissibility
→ STRUC-PERC-I connectivity class
```

So color confinement now contributes not only a physical analogy, but a chamber-testable UNNS object:

```
localized route geometry
+ repair-threshold interpretation
+ admissible ladder behavior
+ differentiated gap-connectivity classes
```

---

## 9. What is supported

Supported by the current chamber alignment:

```
1. Trusted Baker-derived flux observables can be converted into valid chamber ladders.
2. All six trusted flux ladders are STRUC-I Geometric Persistence / Weak Persistence.
3. Area ladders are globally connected under STRUC-PERC-I.
4. Peak and width ladders are more tail-sensitive, with several HARD_FRAGMENTATION verdicts.
5. The NP peak ladder percolates, while the FULL peak ladder fragments, suggesting component-level differences worth investigating.
```

The practical interpretation is:

```
global routed-field measures are structurally smoother;
local route-shape measures expose boundary/tail sensitivity.
```

---

## 10. What is not yet supported

Not yet supported:

```
1. A derivation of QCD confinement from UNNS.
2. A universal chamber law for confinement.
3. A final physical meaning of HARD_FRAGMENTATION for small n flux ladders.
4. A direct threshold-local chamber result near r_c and r_cs.
5. A chamber result using raw measured static V0(r), V1(r), V2(r) lattice tables.
```

The STRUC-PERC-I outputs are especially small-n:

```
n ≈ 13–14 gap vertices
```

Therefore the hard-fragmented verdicts should be treated as **tail-sensitive structural signals**, not as final physical failure claims.

---

## 11. New questions opened

The chamber alignment opens sharper questions:

```
1. Why do area ladders percolate while width ladders fragment?
2. Why does NP peak percolate while FULL peak fragments?
3. Are fragmented peak/width ladders caused by small sample size, real route-shape transition, or remaining normalization structure?
4. Do longer flux-profile separation series preserve the same distinction?
5. Do static repair-window gap ladders show Structural Boundary behavior under STRUC-I or STRUC-PERC-I?
```

---

## 12. Next work item

The next work item is to run the **static repair-window chamber inputs** separately:

```
static_gap01_repair_window_ladder.csv
static_gap12_repair_window_ladder.csv
```

These should not be mixed with the flux ladders. They address a different question:

```
flux ladders
→ route-localization geometry

static gap ladders
→ repair-threshold channel competition
```

Expected output location:

```
chamber_outputs/STRUC_I/raw_exports/struc_i_static_repair_window_results.json
chamber_outputs/STRUC_I/summary_tables/struc_i_static_repair_window_profiles.csv
chamber_outputs/STRUC_PERC_I/raw_exports/struc_perc_static_repair_window_results.json
chamber_outputs/STRUC_PERC_I/summary_tables/struc_perc_static_repair_window_summary.csv
```

After those are run, create:

```
reports/07_static_repair_window_chamber_report.md
```

---

## 13. One-line conclusion

The first chamber pass confirms that trusted confinement-derived flux observables are **admissible ordered structures** under STRUC-I, while STRUC-PERC-I reveals a meaningful distinction between **globally connected route-integral measures** and **tail-fragmented local-shape measures**.
