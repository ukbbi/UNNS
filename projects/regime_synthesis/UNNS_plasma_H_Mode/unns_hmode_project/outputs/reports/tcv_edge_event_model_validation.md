# TCV Edge-Event Model Validation

## Purpose

This report validates the first event-level UNNS-H Mode model:

```text
m_edge_event = C_edge_capacity - F_route_fragmentation
```

The validator does not run another chamber. It tests whether the already computed
edge-event scores separate the reviewed TCV suspect shots into meaningful
corridors.

## Validation status

```text
state_separation: PASS_STRICT_ORDERING
reviewed_shots: 9
ambiguous_shots: 2
mixed_ILH_shots: 1
```

## Main validation table

|   SHOT | ILH   |   m_edge_event | m_edge_state              | formal_corridor                               | dominant_fragmentation_term   | dominant_capacity_term     | margin_support_level   |
|-------:|:------|---------------:|:--------------------------|:----------------------------------------------|:------------------------------|:---------------------------|:-----------------------|
|  69807 | 0     |     -0.793663  | negative_leakage_margin   | mixed_power_transport_timing_leakage_corridor | S_transport                   | geometry_stability         | strong_negative        |
|  69668 | 0     |     -0.551591  | negative_leakage_margin   | transport_timing_corridor                     | S_transport                   | geometry_stability         | strong_negative        |
|  67992 | 1     |     -0.258305  | negative_leakage_margin   | power_transport_corridor                      | S_power_balance               | geometry_stability         | moderate_negative      |
|  68001 | 1;0   |     -0.227105  | negative_leakage_margin   | power_transport_corridor                      | S_power_balance               | geometry_stability         | moderate_negative      |
|  69913 | 1     |     -0.0738676 | boundary_ambiguous_margin | timing_only_or_timing_dominant_corridor       | S_timing                      | geometry_stability         | ambiguous_boundary     |
|  68206 | 1     |      0.0522413 | boundary_ambiguous_margin | power_balance_corridor                        | S_power_balance               | density_support_percentile | ambiguous_boundary     |
|  66445 | 1     |      0.52759   | positive_boundary_margin  | edge_divertor_response_corridor               | S_timing                      | S_edge_response            | strong_positive        |
|  69892 | 1     |      0.658299  | positive_boundary_margin  | edge_divertor_response_corridor               | S_power_balance               | S_edge_response            | strong_positive        |
|  68719 | 1     |      0.793112  | positive_boundary_margin  | edge_divertor_response_corridor               | S_power_balance               | S_edge_response            | strong_positive        |

## State-level margin summary

| m_edge_state              |   count |       mean |     median |        min |        max |       std |
|:--------------------------|--------:|-----------:|-----------:|-----------:|-----------:|----------:|
| negative_leakage_margin   |       4 | -0.457666  | -0.404948  | -0.793663  | -0.227105  | 0.267469  |
| boundary_ambiguous_margin |       2 | -0.0108132 | -0.0108132 | -0.0738676 |  0.0522413 | 0.0891725 |
| positive_boundary_margin  |       3 |  0.659667  |  0.658299  |  0.52759   |  0.793112  | 0.132766  |

## Branch-family score patterns

| branch_tag                    |   shot_count |   mean_m_edge_event |   min_m_edge_event |   max_m_edge_event |   mean_C_edge_capacity |   mean_F_route_fragmentation |   mean_S_power_balance |   mean_S_transport |   mean_S_edge_response |   mean_S_timing |
|:------------------------------|-------------:|--------------------:|-------------------:|-------------------:|-----------------------:|-----------------------------:|-----------------------:|-------------------:|-----------------------:|----------------:|
| timing_branch                 |            3 |           -0.473041 |          -0.793663 |         -0.0738676 |               0.143749 |                     0.61679  |               0.442135 |           0.675655 |              0.0418478 |        0.751876 |
| transport_branch              |            4 |           -0.457666 |          -0.793663 |         -0.227105  |               0.323267 |                     0.780934 |               0.79827  |           0.979775 |              0.168818  |        0.528725 |
| power_balance_branch          |            4 |           -0.306708 |          -0.793663 |          0.0522413 |               0.430412 |                     0.73712  |               0.954871 |           0.783708 |              0.209715  |        0.428725 |
| edge_divertor_response_branch |            3 |            0.659667 |           0.52759  |          0.793112  |               0.820956 |                     0.161289 |               0.212445 |           0.105618 |              0.970199  |        0.166556 |

## ILH-category summary

| ILH_category   |   count |      mean |    median |       min |       max |        std |
|:---------------|--------:|----------:|----------:|----------:|----------:|-----------:|
| ILH_0          |       2 | -0.672627 | -0.672627 | -0.793663 | -0.551591 |   0.171171 |
| ILH_1          |       6 |  0.283178 |  0.289915 | -0.258305 |  0.793112 |   0.43232  |
| ILH_mixed      |       1 | -0.227105 | -0.227105 | -0.227105 | -0.227105 | nan        |

## Ambiguous shots

|   SHOT |   ILH |   m_edge_event | m_edge_state              | formal_corridor                         | dominant_fragmentation_term   | dominant_capacity_term     | margin_support_level   |
|-------:|------:|---------------:|:--------------------------|:----------------------------------------|:------------------------------|:---------------------------|:-----------------------|
|  69913 |     1 |     -0.0738676 | boundary_ambiguous_margin | timing_only_or_timing_dominant_corridor | S_timing                      | geometry_stability         | ambiguous_boundary     |
|  68206 |     1 |      0.0522413 | boundary_ambiguous_margin | power_balance_corridor                  | S_power_balance               | density_support_percentile | ambiguous_boundary     |

## Mixed-ILH shots

|   SHOT | ILH   |   m_edge_event | m_edge_state            | formal_corridor          | dominant_fragmentation_term   | dominant_capacity_term   | margin_support_level   |
|-------:|:------|---------------:|:------------------------|:-------------------------|:------------------------------|:-------------------------|:-----------------------|
|  68001 | 1;0   |      -0.227105 | negative_leakage_margin | power_transport_corridor | S_power_balance               | geometry_stability       | moderate_negative      |

## Interpretation

The key validation question is whether the formal event margin separates the
shot families into coherent corridors instead of merely restating the raw branch
labels.

A strict ordering pass means:

```text
max(negative leakage margin) < min(boundary ambiguous margin)
and
max(boundary ambiguous margin) < min(positive boundary margin)
```

A coarse ordering pass means the negative and positive corridors separate, but
the boundary-ambiguous zone may overlap with one side.

## Caution

This validation is still internal to the first TCV event-level pilot. It does
not yet prove the physical origin of H-mode, and it does not replace
time-series validation using edge turbulence, radial electric field, E×B shear,
pedestal evolution, confinement time, or ELM timing.

The result should be treated as validation of the first event-level
edge-admissibility model only.
