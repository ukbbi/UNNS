# UNNS-H Mode / TCV Two-Chamber Results Report

**Project:** UNNS Plasma Boundary Confinement Program  
**Dataset:** TCV L-H transition database, Zenodo 14996664  
**Prepared from:** `lhdatabase.h5`, `tcv_lh_events_canonical.csv`, STRUC-I v1.0.4 output, STRUC-PERC-I v2.5.0 output  
**Report date:** 2026-06-23

---

## 1. Purpose of this report

This report consolidates the first complete two-chamber pass over the TCV L-H transition dataset. Its purpose is to state what has already been gained before moving to the next technical step: mapping fragmented variables back to the actual shots and rows.

The present stage answers four limited questions:

1. Was the TCV L-H dataset ingested into a usable UNNS-compatible structure?
2. Do the scalar plasma ladders remain admissible under STRUC-I perturbation?
3. Do the same ladders percolate or fragment under STRUC-PERC-I?
4. Which variables now deserve row-level / shot-level isolation analysis?

This report does **not** claim to explain H-mode yet. It establishes the first structural facts needed for that later claim.

---

## 2. Dataset basis

The inspected `lhdatabase.h5` file contains:

| Quantity | Value |
|---|---:|
| Rows | 92 |
| Columns | 79 |
| Unique TCV shots | 66 |
| Shot range | 66444–73917 |
| Years | 2020, 2021, 2022 |
| ILH = 1 entries | 84 |
| ILH = 0 entries | 8 |
| COND = 1 entries | 92 |

The core outcome is that the dataset is small, coherent, and suitable for a first controlled pilot: it contains enough events for a structural scan, while still being tractable for manual follow-up and row-level inspection.

---

## 3. Chamber protocols used

### 3.1 STRUC-I v1.0.4

STRUC-I was run on two prepared long-format scalar ladder files:

- `tcv_lh_core_all_events__struc_i_long.csv`
- `tcv_lh_core_LH_only__struc_i_long.csv`

Run parameters:

| Parameter | Value |
|---|---:|
| Inequality | `inv(Pε ; L) ≤ ν(Vε(L))` |
| Perturbation | `δᵢ ~ Uniform[-ε, ε]` |
| Scale | `ε = κ · median(gaps)` |
| κ range | 0.01–1 |
| κ steps | 40 |
| Monte Carlo runs | 2000 |
| Total ladders evaluated | 48 |

The STRUC-I question was:

> Do the scalar plasma variables preserve admissible ordering under perturbation?

### 3.2 STRUC-PERC-I v2.5.0

STRUC-PERC-I was run in batch mode on the per-variable scalar ladder files for:

- all events;
- L-H-only events.

The STRUC-PERC-I question was:

> Does each variable's gap structure form a connected percolating graph, or does it fragment into isolated branches?

---

## 4. STRUC-I result: global admissibility is preserved

STRUC-I found no structural collapse. Both the all-events and L-H-only ladder sets remain overwhelmingly in Geometric Persistence / Stable Structure.

### 4.1 STRUC-I state counts

| group      | state            |   count |
|:-----------|:-----------------|--------:|
| all_events | Stable Structure |      21 |
| all_events | Weak Persistence |       3 |
| lh_only    | Stable Structure |      21 |
| lh_only    | Weak Persistence |       3 |

Interpretation:

- The data are not structurally random junk.
- The conversion from plasma event table to scalar ladders did not destroy order.
- The scalar variables around the TCV L-H transition are admissible under the STRUC-I perturbation protocol.
- Weakness appears only in a small number of variables, not across the whole corpus.

### 4.2 Highest structural-pressure variables: all events

| name                          | state            |   mean_Ak |   min_Ak |   mean_rho |   max_rho |   rho_at_kappa_max |
|:------------------------------|:-----------------|----------:|---------:|-----------:|----------:|-------------------:|
| event_time                    | Weak Persistence |  0.997725 |   0.9925 |   0.431163 |  0.6103   |           0.402688 |
| helium_fraction_candidate     | Weak Persistence |  1        |   1      |   0.314515 |  0.581933 |           0.581933 |
| P_Ryter                       | Stable Structure |  1        |   1      |   0.277338 |  0.516703 |           0.516703 |
| I_p_MA                        | Stable Structure |  1        |   1      |   0.297693 |  0.496796 |           0.467455 |
| divertor_signal_150_candidate | Stable Structure |  1        |   1      |   0.258526 |  0.490809 |           0.490809 |
| kappa                         | Stable Structure |  1        |   1      |   0.194937 |  0.49     |           0.49     |
| n_Ryter                       | Stable Structure |  1        |   1      |   0.294553 |  0.4755   |           0.446608 |
| dWmhd_dt_candidate_MW         | Stable Structure |  1        |   1      |   0.263284 |  0.475031 |           0.475031 |
| divertor_signal_candidate     | Stable Structure |  1        |   1      |   0.217849 |  0.470443 |           0.470443 |
| volume_m3                     | Weak Persistence |  1        |   1      |   0.303261 |  0.459389 |           0.459389 |

### 4.3 Highest structural-pressure variables: L-H only

| name                          | state            |   mean_Ak |   min_Ak |   mean_rho |   max_rho |   rho_at_kappa_max |
|:------------------------------|:-----------------|----------:|---------:|-----------:|----------:|-------------------:|
| event_time                    | Weak Persistence |  0.994738 |   0.9855 |   0.451285 |  0.63525  |           0.368635 |
| helium_fraction_candidate     | Weak Persistence |  1        |   1      |   0.317418 |  0.602981 |           0.602981 |
| P_Ryter                       | Stable Structure |  1        |   1      |   0.274326 |  0.5019   |           0.5019   |
| n_Ryter                       | Weak Persistence |  1        |   1      |   0.301235 |  0.4855   |           0.435357 |
| divertor_signal_150_candidate | Stable Structure |  1        |   1      |   0.224822 |  0.483242 |           0.483242 |
| I_p_MA                        | Stable Structure |  1        |   1      |   0.29595  |  0.471444 |           0.452562 |
| divertor_signal_candidate     | Stable Structure |  1        |   1      |   0.224936 |  0.468703 |           0.468703 |
| kappa                         | Stable Structure |  1        |   1      |   0.179147 |  0.468417 |           0.468417 |
| B_t_T                         | Stable Structure |  0.99995  |   0.999  |   0.282756 |  0.434783 |           0.426773 |
| P_LH_candidate_MW             | Stable Structure |  1        |   1      |   0.143586 |  0.43131  |           0.425687 |

The repeated weak points are important: `event_time` and `helium_fraction_candidate` are near or above the informal boundary-warning zone in maximum ρ. In the L-H-only subset, `n_Ryter` also moves into Weak Persistence.

### 4.4 Most relaxed variables by mean ρ: all events

| name                      | state            |   mean_Ak |   mean_rho |   max_rho |
|:--------------------------|:-----------------|----------:|-----------:|----------:|
| P_LH_candidate_MW         | Stable Structure |         1 |   0.138548 |  0.444909 |
| Wmhd_J                    | Stable Structure |         1 |   0.145224 |  0.366066 |
| n_e_1e20_m3               | Stable Structure |         1 |   0.154466 |  0.438271 |
| Z_eff                     | Stable Structure |         1 |   0.17276  |  0.383333 |
| chi_eff_candidate         | Stable Structure |         1 |   0.183612 |  0.390958 |
| kappa                     | Stable Structure |         1 |   0.194937 |  0.49     |
| delta                     | Stable Structure |         1 |   0.20195  |  0.390612 |
| divertor_signal_candidate | Stable Structure |         1 |   0.217849 |  0.470443 |

### 4.5 Most relaxed variables by mean ρ: L-H only

| name                     | state            |   mean_Ak |   mean_rho |   max_rho |
|:-------------------------|:-----------------|----------:|-----------:|----------:|
| n_e_1e20_m3              | Stable Structure |         1 |   0.139976 |  0.406955 |
| P_LH_candidate_MW        | Stable Structure |         1 |   0.143586 |  0.43131  |
| Wmhd_J                   | Stable Structure |         1 |   0.14673  |  0.344264 |
| Z_eff                    | Stable Structure |         1 |   0.170781 |  0.382338 |
| kappa                    | Stable Structure |         1 |   0.179147 |  0.468417 |
| chi_eff_candidate        | Stable Structure |         1 |   0.183865 |  0.3773   |
| delta                    | Stable Structure |         1 |   0.210892 |  0.403114 |
| P_total_aux_candidate_MW | Stable Structure |         1 |   0.224358 |  0.427848 |

The candidate L-H power variable, `P_LH_candidate_MW`, is notably relaxed in STRUC-I. This will matter later: the threshold-power candidate itself is structurally coherent, while total power variables fragment under STRUC-PERC-I.

---

## 5. STRUC-PERC-I result: most variables percolate, but not all

### 5.1 Verdict counts

All events:

| verdict            |   count |
|:-------------------|--------:|
| FULL_PERCOLATION   |      20 |
| HARD_FRAGMENTATION |       4 |

L-H only:

| verdict            |   count |
|:-------------------|--------:|
| FULL_PERCOLATION   |      19 |
| HARD_FRAGMENTATION |       5 |

This is the first major two-chamber result:

> The TCV L-H dataset is globally admissible under STRUC-I, but several variables contain disconnected structural branches under STRUC-PERC-I.

This means the dataset is not collapsing globally. Instead, it is separating locally in physically meaningful channels.

---

## 6. Hard-fragmenting variables

### 6.1 All-events hard fragmentation

| var                       |   giantRatio |   isolated |   isolatedFraction |   tailDominance |
|:--------------------------|-------------:|-----------:|-------------------:|----------------:|
| divertor_signal_candidate |     0.913043 |          2 |           0.021739 |        0.585082 |
| chi_eff_candidate         |     0.955056 |          2 |           0.022472 |        0.573016 |
| P_total_aux_candidate_MW  |     0.977528 |          2 |           0.022472 |        0.290259 |
| P_total_candidate_MW      |     0.978261 |          2 |           0.021739 |        0.423619 |

### 6.2 L-H-only hard fragmentation

| var                      |   giantRatio |   isolated |   isolatedFraction |   tailDominance |
|:-------------------------|-------------:|-----------:|-------------------:|----------------:|
| P_loss_candidate_MW      |     0.95122  |          2 |           0.02439  |        0.275048 |
| event_time               |     0.962025 |          3 |           0.037975 |        0.644251 |
| chi_eff_candidate        |     0.987805 |          1 |           0.012195 |        0.31258  |
| P_total_aux_candidate_MW |     0.987805 |          1 |           0.012195 |        0.323516 |
| P_total_candidate_MW     |     0.988095 |          1 |           0.011905 |        0.371203 |

The hard-fragmenting variables are not mainly magnetic geometry variables. They cluster around:

- transport / diffusivity proxy: `chi_eff_candidate`;
- total power balance: `P_total_candidate_MW`, `P_total_aux_candidate_MW`;
- loss power: `P_loss_candidate_MW` in L-H-only;
- transition timing: `event_time` in L-H-only;
- divertor / edge response: `divertor_signal_candidate` in all-events.

This is exactly where a serious H-mode origin analysis should look. H-mode should not be expected to appear as a simple property of machine size or raw field geometry; it should appear in the interaction between boundary transport, power balance, edge response, and transition timing.

---

## 7. Stable percolating variables

A large set of variables remain FULL_PERCOLATION in both all-events and L-H-only runs. The most connected low-κ variables include:

| var                           |   kappa_connect_all |   kappa_connect_lh |   tailDominance_all |   tailDominance_lh |
|:------------------------------|--------------------:|-------------------:|--------------------:|-------------------:|
| hydrogen_fraction_candidate   |             4.5858  |            4.28817 |            0.346909 |           0.347006 |
| dWmhd_dt_candidate_MW         |             7.87533 |            5.90393 |            0.583914 |           0.410604 |
| divertor_signal_150_candidate |           108.004   |          108.004   |            0.586553 |           0.652012 |
| n_e_1e20_m3                   |            92.8913  |          158.753   |            0.65356  |           0.663068 |
| Wmhd_J                        |           131.711   |          160.189   |            0.560391 |           0.605804 |
| Z_eff                         |           161.975   |          164.743   |            0.702507 |           0.628033 |
| P_LH_candidate_MW             |           155.368   |          214.463   |            0.70444  |           0.673469 |
| helium_fraction_candidate     |          2729.18    |           49.7799  |            0.874972 |           0.874972 |
| q95                           |          1878.61    |         1953.87    |            0.972717 |           0.966277 |
| volume_m3                     |          2114       |         2234.24    |            0.942404 |           0.948882 |

Interpretation:

- `hydrogen_fraction_candidate` and `dWmhd_dt_candidate_MW` connect at low κ in both subsets.
- `P_LH_candidate_MW`, `Wmhd_J`, `Z_eff`, and `n_e_1e20_m3` remain connected and usable as stable coordinates.
- The L-H candidate threshold power is not the fragmented object; total/auxiliary power and loss-power branches are.

The high-tail but still percolating variables include:

| var            |   tailDominance_all |   tailDominance_lh |   kappa_connect_all |   kappa_connect_lh |
|:---------------|--------------------:|-------------------:|--------------------:|-------------------:|
| R_geo_m        |            0.995134 |           0.995206 |            21613.6  |           21627.7  |
| B_t_T          |            0.990819 |           0.991736 |            15961.3  |           15961.3  |
| P_Ryter        |            0.988691 |           0.989553 |             9283.27 |           10340.5  |
| minor_radius_m |            0.974144 |           0.977121 |             6129.49 |            6103.48 |
| I_p_MA         |            0.964899 |           0.978559 |             2594.45 |            3484.84 |
| delta          |            0.970848 |           0.970848 |             3590.35 |            3537.11 |
| q95            |            0.972717 |           0.966277 |             1878.61 |            1953.87 |
| n_Ryter        |            0.966034 |           0.967137 |             2135.79 |            2515.35 |
| kappa          |            0.95553  |           0.969244 |             3153.94 |            3764.35 |
| volume_m3      |            0.942404 |           0.948882 |             2114    |            2234.24 |

These variables are connected, but their high tail dominance means they may contain stretched or scale-separated branch geometry. They are not immediate failures, but they may matter when we later compare transition families.

---

## 8. Verdict changes between all-events and L-H-only

| var                       | verdict_all        |   giantRatio_all |   isolated_all |   isolatedFraction_all | kappa_connect_all   |   tailDominance_all | verdict_lh         |   giantRatio_lh |   isolated_lh |   isolatedFraction_lh | kappa_connect_lh   |   tailDominance_lh |
|:--------------------------|:-------------------|-----------------:|---------------:|-----------------------:|:--------------------|--------------------:|:-------------------|----------------:|--------------:|----------------------:|:-------------------|-------------------:|
| divertor_signal_candidate | HARD_FRAGMENTATION |         0.913043 |              2 |               0.021739 |                     |            0.585082 | FULL_PERCOLATION   |        1        |             0 |              0        | 133.680897         |           0.634932 |
| event_time                | FULL_PERCOLATION   |         1        |              0 |               0        | 135.666667          |            0.6133   | HARD_FRAGMENTATION |        0.962025 |             3 |              0.037975 |                    |           0.644251 |
| P_loss_candidate_MW       | FULL_PERCOLATION   |         1        |              0 |               0        | 40.945583           |            0.308138 | HARD_FRAGMENTATION |        0.95122  |             2 |              0.02439  |                    |           0.275048 |

These changes are one of the most meaningful results of the entire pass.

### 8.1 `divertor_signal_candidate`

`divertor_signal_candidate` is HARD_FRAGMENTATION in all-events but FULL_PERCOLATION in L-H-only.

Interpretation:

> Non-L-H or non-transition entries likely disturb the divertor signal structure. When we restrict to actual L-H events, the divertor signal becomes structurally connected.

This supports the idea that edge/divertor response is not noise; it may be a transition-specific coordinate.

### 8.2 `event_time`

`event_time` is FULL_PERCOLATION in all-events but HARD_FRAGMENTATION in L-H-only.

Interpretation:

> Actual L-H transition times may separate into distinct timing families or access corridors.

This is one of the strongest indicators that H-mode access may not be a single smooth path. It may have multiple boundary-admissible routes.

### 8.3 `P_loss_candidate_MW`

`P_loss_candidate_MW` is FULL_PERCOLATION in all-events but HARD_FRAGMENTATION in L-H-only.

Interpretation:

> Power-loss balance at actual L-H events may be branch-structured, even when the broader event table makes the variable appear connected.

This is central for the H-mode origin question because it points toward power balance rather than total heating alone.

---

## 9. Persistent fragmentation across both subsets

| var                      | verdict_all        |   giantRatio_all |   isolated_all |   isolatedFraction_all | kappa_connect_all   |   tailDominance_all | verdict_lh         |   giantRatio_lh |   isolated_lh |   isolatedFraction_lh | kappa_connect_lh   |   tailDominance_lh |
|:-------------------------|:-------------------|-----------------:|---------------:|-----------------------:|:--------------------|--------------------:|:-------------------|----------------:|--------------:|----------------------:|:-------------------|-------------------:|
| chi_eff_candidate        | HARD_FRAGMENTATION |         0.955056 |              2 |               0.022472 |                     |            0.573016 | HARD_FRAGMENTATION |        0.987805 |             1 |              0.012195 |                    |           0.31258  |
| P_total_aux_candidate_MW | HARD_FRAGMENTATION |         0.977528 |              2 |               0.022472 |                     |            0.290259 | HARD_FRAGMENTATION |        0.987805 |             1 |              0.012195 |                    |           0.323516 |
| P_total_candidate_MW     | HARD_FRAGMENTATION |         0.978261 |              2 |               0.021739 |                     |            0.423619 | HARD_FRAGMENTATION |        0.988095 |             1 |              0.011905 |                    |           0.371203 |

These are now the highest-priority variables for row-level mapping.

### 9.1 `P_total_candidate_MW` and `P_total_aux_candidate_MW`

Both total-power variables are HARD_FRAGMENTATION in both all-events and L-H-only runs.

This is the key interpretation:

> Total heating power is not a single connected structural path to H-mode.

This does **not** mean power is irrelevant. It means power alone is not the complete structural coordinate. A plasma may receive enough power, but whether it enters H-mode depends on how that power is organized relative to density, transport, stored energy, and boundary response.

### 9.2 `chi_eff_candidate`

`chi_eff_candidate` is HARD_FRAGMENTATION in both subsets.

This is also critical:

> The transport/diffusivity-like coordinate is branch-structured.

That is exactly what the UNNS H-mode hypothesis expects: the origin should live in transition of transport-route geometry, not merely in a scalar power value.

---

## 10. Core result gained so far

The first two-chamber result can be stated as follows:

> The TCV L-H dataset is structurally admissible under STRUC-I, but STRUC-PERC-I reveals localized fragmentation in variables tied to power balance, transport, timing, and edge/divertor response.

This is the first credible UNNS-H Mode signal.

It supports the following refined working hypothesis:

> H-mode access is not just a total-heating threshold. It is a boundary-admissibility transition in which power, loss balance, transport reduction, species/density position, and edge response must enter a connected route-preserving configuration.

---

## 11. What we have gained

### 11.1 A clean data spine

We now have a structured chain:

```
raw TCV .h5 files
→ canonical event CSV
→ chamber-ready scalar ladders
→ STRUC-I admissibility profiles
→ STRUC-PERC-I percolation profiles
```

This is essential because it makes the research reproducible.

### 11.2 A baseline admissibility result

The scalar ladders do not fail globally. They are suitable for further UNNS analysis.

### 11.3 A non-trivial fragmentation signal

Fragmentation is selective. It appears in variables that are physically plausible H-mode origin coordinates.

### 11.4 A distinction between threshold power and power balance

`P_LH_candidate_MW` stays connected, while total/auxiliary power fragments.

This suggests that a threshold value can be coherent as a measurement, while the underlying power-route organization remains branched.

### 11.5 A first route-family hypothesis

L-H-only `event_time` fragmentation suggests that transition access may occur through multiple timing families.

---

## 12. What we should not claim yet

We should not claim that:

- UNNS has solved H-mode;
- the physical origin of H-mode is proven;
- total power is unimportant;
- STRUC-PERC fragmentation automatically equals physical instability;
- the hard-fragmenting variables are causally responsible.

The correct claim is narrower:

> The first two-chamber pass identifies physically plausible structural branches that must now be mapped back to shots, rows, species, powers, densities, and timing.

---

## 13. Immediate next step justified by this report

The next step is justified and well-defined:

```
components/tcv_fragment_isolate_mapper.py
```

It should map the fragmented variables back to row identities:

```
SHOT
TIME
ILH
species indicators
P_LH_candidate_MW
P_total_candidate_MW
P_total_aux_candidate_MW
P_loss_candidate_MW
chi_eff_candidate
event_time
divertor_signal_candidate
n_e_1e20_m3
n_Ryter
P_Ryter
I_p_MA
B_t_T
q95
kappa
```

The target variables for first isolation are:

```text
chi_eff_candidate
P_total_candidate_MW
P_total_aux_candidate_MW
P_loss_candidate_MW
event_time
divertor_signal_candidate
```

The goal is to identify which actual shots/rows form the isolated branches.

---

## 14. Research significance

This result is significant because it transforms the H-mode question from a vague conceptual analogy into a structured research program.

The original questions were:

1. Can ionized gases be confined long enough and hot enough for fusion power?
2. What is the physical origin of H-mode?

The present result does not answer them, but it gives UNNS a concrete path:

- Confinement must be studied as structural persistence, not only as scalar power input.
- H-mode origin should be sought in boundary-route reorganization.
- The first dataset already shows branch structure in the right physical neighborhood: power balance, transport, timing, and edge response.

The emerging UNNS formulation is:

> Fusion-relevant confinement may require a plasma to enter a connected boundary-admissible route configuration. H-mode is the observed transition into that configuration; ELMs and back-transition may be failures or overloads of it.

---

## 15. Provisional conclusion

The two-chamber pass is successful.

It establishes that:

1. The TCV L-H dataset is usable.
2. Its scalar ladders are globally admissible.
3. Percolation is mostly present, but not universal.
4. Fragmentation appears in physically meaningful variables.
5. The next necessary step is not another chamber run, but row-level branch identification.

The strongest single sentence is:

> The TCV L-H transition corpus is admissible but internally branched; the branches concentrate in transport, power-balance, timing, and edge-response variables, which are precisely the variables expected to carry the physical origin of H-mode.
