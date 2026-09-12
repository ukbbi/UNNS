# TokaMark Cross-Shot m_edge(t) Comparison

## Purpose

Compare the reference public TokaMark shot against a weaker / comparison candidate after both have been run through the same `m_edge(t)` and trace-inspection pipeline.

This is the next step after `docs/20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md`.

## Compared shots

| shot_id | candidate_class | candidate_score | positive_boundary_margin_fraction | negative_leakage_margin_fraction | boundary_ambiguous_margin_fraction | insufficient_data_fraction | m_edge_median | m_edge_mean | m_edge_min | m_edge_max | C_edge_capacity_median | F_route_fragmentation_median | S_edge_response_median | S_power_balance_median | S_transport_median | missingness_pressure_median | interpretable_positive_count | interpretable_negative_count | interpretable_positive_total_duration | interpretable_negative_total_duration |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 12063 | FULL_PROFILE_EDGE_CANDIDATE | 97.143 | 0.258216 | 0.112676 | 0.49061 | 0.138498 | 0.087961 | 0.055111 | -0.770609 | 0.475695 | 0.559422 | 0.516301 | 0.572315 | 0.569205 | 0.484131 | 0.222222 | 8 | 3 | 0.035 | 0.016 |
| 11830 | PROFILE_DALPHA_CANDIDATE | 81.429 | 0.226064 | 0.228723 | 0.390957 | 0.154255 | -0.0366668 | 0.0050537 | -0.745802 | 0.387901 | 0.612696 | 0.694692 | 0.499333 | 0.710196 | 0.481211 | 0.222222 | 2 | 0 | 0.077 | 0 |

## Decision

```text
decision: reference_structurally_stronger
- reference_has_more_interpretable_positive_windows
- reference_has_higher_positive_fraction
- reference_has_higher_peak_m_edge
delta positive fraction: -0.03215213265408051
delta interpretable positive count: -6
delta missingness median: 0.0
```

## Interpretation

If the reference shot has more coherent positive windows and a stronger positive-margin distribution, shot 12063 becomes structurally more meaningful. If the comparison shot reproduces the same pattern, v0.1 may be overbroad and should be revised before further claims.

## Bounded claim

This comparison is still not physical H-mode validation. It tests whether the structural margin distinguishes two public TokaMark shots under the same pipeline.