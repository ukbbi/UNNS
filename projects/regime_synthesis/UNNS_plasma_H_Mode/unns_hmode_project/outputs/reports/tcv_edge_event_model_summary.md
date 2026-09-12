# TCV Event-Level Edge-Admissibility Model v0.1

## Purpose

This report converts the four observed TCV branch families into a first formal UNNS-H Mode event-level model. It does not run another chamber and does not claim a full time-dependent edge margin. It defines and evaluates `m_edge_event`, an event-table precursor to `m_edge(t)`.

## Model definition

The observed branch vector is:

```text
β_event = (B_power_balance, B_transport, B_edge_divertor_response, B_timing)
```

The event-level margin is:

```text
m_edge_event = C_edge_capacity - F_route_fragmentation
```

where route fragmentation is driven by power-balance, transport, and timing branch evidence, while edge capacity is driven by edge/divertor response, density support, geometry stability, and species position.

## Margin states

- `negative_leakage_margin`: 4 shots
- `positive_boundary_margin`: 3 shots
- `boundary_ambiguous_margin`: 2 shots

## Formal corridor counts

- `edge_divertor_response_corridor`: 3 shots
- `power_transport_corridor`: 2 shots
- `mixed_power_transport_timing_leakage_corridor`: 1 shots
- `transport_timing_corridor`: 1 shots
- `timing_only_or_timing_dominant_corridor`: 1 shots
- `power_balance_corridor`: 1 shots

## Scored shot table

|   SHOT | ILH   |   fragment_count | fragment_tags                                       |   S_power_balance |   S_transport |   S_edge_response |   S_timing |   F_route_fragmentation |   C_edge_capacity |   m_edge_event | m_edge_state              | formal_corridor                               |
|-------:|:------|-----------------:|:----------------------------------------------------|------------------:|--------------:|------------------:|-----------:|------------------------:|------------------:|---------------:|:--------------------------|:----------------------------------------------|
|  69807 | 0     |                5 | power_balance_branch;transport_branch;timing_branch |             0.945 |         0.990 |             0.063 |      0.856 |                   0.934 |             0.140 |         -0.794 | negative_leakage_margin   | mixed_power_transport_timing_leakage_corridor |
|  69668 | 0     |                4 | transport_branch;timing_branch                      |             0.299 |         0.997 |             0.044 |      0.700 |                   0.663 |             0.112 |         -0.552 | negative_leakage_margin   | transport_timing_corridor                     |
|  67992 | 1     |                3 | power_balance_branch;transport_branch               |             0.961 |         0.960 |             0.282 |      0.271 |                   0.753 |             0.495 |         -0.258 | negative_leakage_margin   | power_transport_corridor                      |
|  68001 | 1;0   |                4 | power_balance_branch;transport_branch               |             0.989 |         0.973 |             0.287 |      0.288 |                   0.773 |             0.546 |         -0.227 | negative_leakage_margin   | power_transport_corridor                      |
|  69913 | 1     |                4 | timing_branch                                       |             0.083 |         0.040 |             0.019 |      0.700 |                   0.253 |             0.179 |         -0.074 | boundary_ambiguous_margin | timing_only_or_timing_dominant_corridor       |
|  68206 | 1     |                3 | power_balance_branch                                |             0.925 |         0.212 |             0.207 |      0.300 |                   0.488 |             0.540 |          0.052 | boundary_ambiguous_margin | power_balance_corridor                        |
|  66445 | 1     |                4 | edge_divertor_response_branch                       |             0.240 |         0.135 |             0.970 |      0.290 |                   0.218 |             0.746 |          0.528 | positive_boundary_margin  | edge_divertor_response_corridor               |
|  69892 | 1     |                4 | edge_divertor_response_branch                       |             0.295 |         0.182 |             0.945 |      0.209 |                   0.230 |             0.888 |          0.658 | positive_boundary_margin  | edge_divertor_response_corridor               |
|  68719 | 1     |                4 | edge_divertor_response_branch                       |             0.103 |         0.000 |             0.996 |      0.000 |                   0.036 |             0.829 |          0.793 | positive_boundary_margin  | edge_divertor_response_corridor               |

## Interpretation

The most negative margins represent route-fragmentation-dominated events: power-balance, transport, and/or timing pressure exceed event-level boundary response capacity. The positive or less negative margins represent candidate edge-response corridors where divertor/edge response and density support partly offset route fragmentation.

In this first v0.1 model, `69807` is the strongest mixed leakage case because it combines power-balance, transport, and timing branch evidence with weak edge/divertor response. The edge-divertor trio is separated because it has strong boundary-response evidence rather than mixed route-fragmentation evidence.

## What this model is not

This is not a proof of H-mode origin, not a reactor confinement model, and not a replacement for plasma physics. It is a formal UNNS event-level bridge from observed branch families to a computable edge-admissibility precursor.

## Next use

Use this model to test whether branch families occupy separable regions in feature space. Once richer time-series data are available, replace `m_edge_event` with `m_edge(t)` and test whether the margin rises before L-H transition and weakens before ELM or H-L relaxation.