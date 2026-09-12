# TokaMark First m_edge(t) Probe — Shot 11996

## 1. Purpose

This report records the first normalized time-resolved UNNS-H Mode edge-admissibility probe for a public MAST/TokaMark shot.

It computes first versions of:

```text
S_power_balance(t)
S_transport(t)
S_edge_response(t)
C_edge_capacity(t)
F_route_fragmentation(t)
m_edge(t)
```

This is a first structural probe, not a final physical validation.

## 2. Source

- shot_id: `11996`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11996.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11996.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `0`

## 4. Time grid

```text
dt:       0.001
count:    541
time_min: -0.05620000511407852
time_max: 0.48379999488592196
```

## 5. Formula version

`tokamark_m_edge_t_probe_v0.1_normalized`

```text
S_power_balance = 0.70*nbi_pressure + 0.30*density_deviation_pressure
S_transport = 0.40*Te_gradient + 0.40*ne_gradient + 0.10*Te_edge_core_deviation + 0.10*ne_edge_core_deviation
S_edge_response = 0.40*Dalpha_suppression + 0.30*softX_activity + 0.30*profile_sharpening
C_edge_capacity = 0.50*S_edge_response + 0.25*density_support + 0.25*geometry_stability
F_route_fragmentation = 0.45*S_power_balance + 0.45*S_transport + 0.10*missingness_pressure
m_edge = C_edge_capacity - F_route_fragmentation
```

## 6. Summary statistics

| quantity              |   finite_count |   total_count |   finite_fraction |         min |    median |      mean |      max |      std |
|:----------------------|---------------:|--------------:|------------------:|------------:|----------:|----------:|---------:|---------:|
| S_power_balance       |            494 |           541 |          0.913124 |  4.5983e-05 | 0.300039  | 0.474146  | 0.94538  | 0.275524 |
| S_transport           |            210 |           541 |          0.38817  |  0          | 0.428682  | 0.425184  | 0.874648 | 0.185206 |
| S_edge_response       |            494 |           541 |          0.913124 |  0.00271597 | 0.369451  | 0.381143  | 0.597236 | 0.112162 |
| C_edge_capacity       |            494 |           541 |          0.913124 |  0.0822136  | 0.482985  | 0.482977  | 0.700421 | 0.153842 |
| F_route_fragmentation |            541 |           541 |          1        |  0.0812422  | 0.389347  | 0.449584  | 1        | 0.248547 |
| m_edge                |            494 |           541 |          0.913124 | -0.289985   | 0.0328101 | 0.0857603 | 0.493317 | 0.226293 |
| missingness_pressure  |            541 |           541 |          1        |  0          | 0.222222  | 0.255083  | 1        | 0.283689 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 338
positive_boundary_margin: 130
insufficient_data: 47
negative_leakage_margin: 26
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.3917999948859219
m_edge: 0.4933167469008951
C_edge_capacity: 0.6247076570937071
F_route_fragmentation: 0.13139091019281204
S_edge_response: 0.4126423673756207
S_power_balance: 0.11120617418627644
S_transport: nan
density_support: 0.7806128046848322
geometry_stability: 0.8929330889387547
missingness_pressure: 0.2222222222222222
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.04879999488592157
m_edge: -0.28998450475584747
C_edge_capacity: 0.25960234948489314
F_route_fragmentation: 0.5495868542407406
S_edge_response: 0.3900742186776885
S_power_balance: 0.7426315309393487
S_transport: 0.47867258959563025
density_support: 0.23186693343818293
geometry_stability: 0.026394027146012643
missingness_pressure: 0.0
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.2848 |     0.4108 |      0.126 |           341 |         467 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.0468 |     0.0548 |      0.008 |           103 |         111 |
|       0.0908 |     0.1008 |      0.01  |           147 |         157 |

## 11. Interpretation

This output is the first computable `m_edge(t)` trace for the public TokaMark candidate shot.

It should be interpreted as a normalized structural diagnostic, because TokaMark signals may be preprocessed and not in raw physical engineering units.

A positive interval means that, under this v0.1 normalized formula, edge-capacity proxies exceed route-fragmentation proxies. It does not by itself prove H-mode, L-H transition timing, or positive-corridor status.

A negative interval means that route-fragmentation proxies exceed edge-capacity proxies under the same exploratory formula.

## 12. Limitations

```text
1. Uses robust within-shot normalization, not absolute physical thresholds.
2. Uses a crude Thomson edge approximation: last 20 percent of profile indices.
3. Does not yet use explicit radial or flux-coordinate mapping.
4. Does not identify L-H transition time.
5. Does not compare against negative or ambiguous MAST shots.
6. Does not validate the positive corridor physically.
```

## 13. Next step

The next step is to inspect the generated CSV and decide whether the v0.1 margin intervals align with recognizable edge-response structure.

Then create a validation note:

```text
docs/
  19_TOKAMARK_M_EDGE_T_PROBE_REPORT.md
```

Only after that should the formula be revised or extended.