# Full 92-Event TCV Edge-Event Extension Report

## Purpose

This report extends the event-level UNNS-H Mode margin from the manually reviewed 9-shot set to the full 92-row TCV canonical event corpus. It also performs a first residual comparison against standard plasma variables and inventories the available time-resolved diagnostic traces in `LH_DATA.h5`.

## Important methodological change

The 9-shot model used fragment-family tags from the chamber mapping stage. The full-corpus extension cannot rely on those tags for all rows. Therefore this extension uses a tag-free numeric generalization of the model:

```text
m_edge_event = C_edge_capacity - F_route_fragmentation
F_route_fragmentation = 0.35*S_power_balance + 0.35*S_transport + 0.30*S_timing
C_edge_capacity = 0.45*S_edge_response + 0.25*density_support + 0.15*geometry_stability + 0.15*species_position
```

This means the full-corpus scores are not identical to the earlier 9-shot tag-assisted scores. They are a first generalization test.

## Full-corpus state counts

| m_edge_state              |   count |   mean_m |   median_m |   min_m |   max_m |   std_m |   ILH1_rate |   mean_m_ci95_lo |   mean_m_ci95_hi |
|:--------------------------|--------:|---------:|-----------:|--------:|--------:|--------:|------------:|-----------------:|-----------------:|
| boundary_ambiguous_margin |      68 |   -0.038 |     -0.055 |  -0.199 |   0.182 |   0.098 |       0.956 |           -0.061 |           -0.015 |
| negative_leakage_margin   |      11 |   -0.356 |     -0.285 |  -0.664 |  -0.207 |   0.163 |       0.636 |           -0.450 |           -0.270 |
| positive_boundary_margin  |      13 |    0.341 |      0.312 |   0.223 |   0.585 |   0.095 |       0.923 |            0.297 |            0.395 |

## Formal corridor counts

| formal_corridor                               |   count |   mean_m |   min_m |   max_m |   ILH1_rate |
|:----------------------------------------------|--------:|---------:|--------:|--------:|------------:|
| power_transport_corridor                      |       6 |   -0.209 |  -0.664 |   0.223 |       0.500 |
| transport_timing_corridor                     |       2 |   -0.173 |  -0.326 |  -0.019 |       1.000 |
| power_balance_corridor                        |      10 |   -0.148 |  -0.413 |  -0.043 |       0.900 |
| mixed_power_transport_timing_leakage_corridor |      21 |   -0.112 |  -0.426 |  -0.016 |       0.857 |
| timing_only_or_timing_dominant_corridor       |      12 |   -0.019 |  -0.236 |   0.291 |       1.000 |
| transport_corridor                            |       1 |   -0.006 |  -0.006 |  -0.006 |       1.000 |
| weak_or_unclassified_corridor                 |      30 |    0.043 |  -0.281 |   0.445 |       1.000 |
| edge_divertor_response_corridor               |      10 |    0.228 |   0.064 |   0.585 |       0.900 |

## ILH separation

- AUC of `m_edge_event` for ILH=1: `0.690`
- Mean difference ILH=1 minus ILH=0: `0.242`
- Permutation p-value, two-sided: `0.0022`

Interpretation: because the full corpus is highly imbalanced (84 ILH=1 rows, 8 ILH=0 rows), AUC and permutation tests are more informative than raw accuracy.

## Standard plasma variables vs UNNS structural margin

| model                                    |   loo_auc_for_ILH1 |   loo_r2_linear_to_ILH |   pred_min |   pred_max | features                                                                                                                                                                                                                                                                                                                     |
|:-----------------------------------------|-------------------:|-----------------------:|-----------:|-----------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| standard_core                            |              1.000 |                  0.724 |     -0.005 |      1.243 | P_LH_candidate_MW;P_total_candidate_MW;P_total_aux_candidate_MW;P_loss_candidate_MW;dWmhd_dt_candidate_MW;Wmhd_J;n_e_1e20_m3;I_p_MA;B_t_T;q95;kappa;delta;hydrogen_fraction_candidate;helium_fraction_candidate;Z_eff;n_Ryter;P_Ryter                                                                                        |
| standard_core_plus_UNNS_margin           |              1.000 |                  0.716 |     -0.053 |      1.237 | P_LH_candidate_MW;P_total_candidate_MW;P_total_aux_candidate_MW;P_loss_candidate_MW;dWmhd_dt_candidate_MW;Wmhd_J;n_e_1e20_m3;I_p_MA;B_t_T;q95;kappa;delta;hydrogen_fraction_candidate;helium_fraction_candidate;Z_eff;n_Ryter;P_Ryter;m_edge_event                                                                           |
| standard_edge_inclusive                  |              1.000 |                  0.707 |      0.002 |      1.239 | P_LH_candidate_MW;P_total_candidate_MW;P_total_aux_candidate_MW;P_loss_candidate_MW;dWmhd_dt_candidate_MW;Wmhd_J;n_e_1e20_m3;I_p_MA;B_t_T;q95;kappa;delta;hydrogen_fraction_candidate;helium_fraction_candidate;Z_eff;n_Ryter;P_Ryter;chi_eff_candidate;divertor_signal_candidate;divertor_signal_150_candidate              |
| standard_edge_inclusive_plus_UNNS_margin |              0.999 |                  0.698 |     -0.059 |      1.236 | P_LH_candidate_MW;P_total_candidate_MW;P_total_aux_candidate_MW;P_loss_candidate_MW;dWmhd_dt_candidate_MW;Wmhd_J;n_e_1e20_m3;I_p_MA;B_t_T;q95;kappa;delta;hydrogen_fraction_candidate;helium_fraction_candidate;Z_eff;n_Ryter;P_Ryter;chi_eff_candidate;divertor_signal_candidate;divertor_signal_150_candidate;m_edge_event |
| UNNS_components                          |              0.696 |                 -0.009 |      0.656 |      1.174 | S_power_balance;S_transport;S_edge_response;S_timing;C_edge_capacity;F_route_fragmentation                                                                                                                                                                                                                                   |
| UNNS_margin_only                         |              0.655 |                  0.036 |      0.714 |      1.198 | m_edge_event                                                                                                                                                                                                                                                                                                                 |

## Residual analysis

| model                                   |   loo_r2_explaining_m_edge |   residual_std |   residual_auc_for_ILH1 |   residual_mean_ILH1_minus_ILH0 |
|:----------------------------------------|---------------------------:|---------------:|------------------------:|--------------------------------:|
| standard_core_explains_m_edge           |                      0.520 |          0.144 |                   0.458 |                          -0.039 |
| standard_edge_inclusive_explains_m_edge |                      0.536 |          0.141 |                   0.440 |                          -0.044 |

Interpretation: `standard_core_explains_m_edge` estimates how much of the UNNS margin is reducible to core plasma variables only. `standard_edge_inclusive_explains_m_edge` includes chi_eff and divertor/edge response signals, so higher explanatory power is expected because those variables are direct inputs to the margin.

## Top single-variable associations with ILH

| variable                 |   auc_for_ILH1 |   abs_auc_distance_from_0_5 |
|:-------------------------|---------------:|----------------------------:|
| dWmhd_dt_candidate_MW    |          0.999 |                       0.499 |
| kappa                    |          0.908 |                       0.408 |
| chi_eff_candidate        |          0.122 |                       0.378 |
| S_power_balance          |          0.144 |                       0.356 |
| Z_eff                    |          0.164 |                       0.336 |
| P_loss_candidate_MW      |          0.172 |                       0.328 |
| P_total_candidate_MW     |          0.210 |                       0.290 |
| F_route_fragmentation    |          0.220 |                       0.280 |
| S_transport              |          0.228 |                       0.272 |
| I_p_MA                   |          0.744 |                       0.244 |
| P_total_aux_candidate_MW |          0.268 |                       0.232 |
| Wmhd_J                   |          0.728 |                       0.228 |

## Time-resolved diagnostic inventory

|   shot_id |   event_time |   src_ILH | m_edge_state              | formal_corridor                               |   m_edge_event |   time_points |   profile_points |   post_pre_edge_te_gradient_ratio |   post_pre_edge_te_ratio |
|----------:|-------------:|----------:|:--------------------------|:----------------------------------------------|---------------:|--------------:|-----------------:|----------------------------------:|-------------------------:|
|     66464 |        0.913 |     1.000 | boundary_ambiguous_margin | weak_or_unclassified_corridor                 |         -0.121 |           148 |              109 |                             2.153 |                    2.306 |
|     66465 |        0.906 |     1.000 | boundary_ambiguous_margin | weak_or_unclassified_corridor                 |         -0.074 |           148 |              109 |                             2.563 |                    1.845 |
|     66468 |        0.893 |     1.000 | boundary_ambiguous_margin | weak_or_unclassified_corridor                 |         -0.057 |           148 |              109 |                             1.940 |                    2.039 |
|     66527 |        0.894 |     1.000 | boundary_ambiguous_margin | weak_or_unclassified_corridor                 |         -0.108 |           148 |              109 |                             1.662 |                    1.847 |
|     66530 |        1.990 |     0.000 | negative_leakage_margin   | mixed_power_transport_timing_leakage_corridor |         -0.426 |           148 |              109 |                           nan     |                  nan     |
|     72681 |        1.135 |     1.000 | boundary_ambiguous_margin | power_balance_corridor                        |         -0.112 |           178 |              109 |                             1.495 |                    2.242 |

Available time-resolved traces by full-corpus corridor: `{'boundary_ambiguous_margin': 5, 'negative_leakage_margin': 1}`

This does not yet satisfy the requirement of one discharge per corridor unless all three states are present in the time-resolved inventory. It is a diagnostic inventory plus first probe only.

## Conclusions

1. The full 92-event extension is now computable without manual fragment tags.
2. The three-corridor structure should be interpreted cautiously because the full-corpus model is a numeric generalization, not the same tag-assisted 9-shot validator.
3. The residual analysis should be treated as a first check, not a final statistical proof, because the margin is constructed from physical variables rather than independently measured.
4. The `LH_DATA.h5` time-resolved traces are available only for a limited set of shots; these do not automatically provide one case per corridor. Additional time-resolved data must be acquired if a corridor is missing.

