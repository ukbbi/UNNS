# TokaMark First m_edge(t) Probe — Shot 11946

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

- shot_id: `11946`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11946.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11946.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `0`

## 4. Time grid

```text
dt:       0.001
count:    546
time_min: -0.05880001187324524
time_max: 0.48619998812675524
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
| S_power_balance       |            497 |           546 |          0.910256 |  0.00142774 | 0.507852  | 0.48415   | 0.968641 | 0.318543 |
| S_transport           |            380 |           546 |          0.695971 |  0.0705972  | 0.354791  | 0.423622  | 0.77898  | 0.166321 |
| S_edge_response       |            496 |           546 |          0.908425 |  0          | 0.33134   | 0.374183  | 0.62588  | 0.137105 |
| C_edge_capacity       |            496 |           546 |          0.908425 |  0.0478754  | 0.464965  | 0.465203  | 0.778128 | 0.153095 |
| F_route_fragmentation |            546 |           546 |          1        |  0.054506   | 0.395825  | 0.455547  | 1        | 0.245024 |
| m_edge                |            496 |           546 |          0.908425 | -0.186518   | 0.0453373 | 0.0628523 | 0.477608 | 0.119917 |
| missingness_pressure  |            546 |           546 |          1        |  0          | 0         | 0.188645  | 1        | 0.312941 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 433
positive_boundary_margin: 63
insufficient_data: 50
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.48519998812675524
m_edge: 0.4776080487909965
C_edge_capacity: 0.5798078179906414
F_route_fragmentation: 0.10219976919964488
S_edge_response: 0.5798078179906414
S_power_balance: 0.0014540388983313958
S_transport: nan
density_support: nan
geometry_stability: nan
missingness_pressure: 0.5555555555555556
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.4161999881267552
m_edge: -0.18651818546761537
C_edge_capacity: 0.0478753736997814
F_route_fragmentation: 0.23439355916739676
S_edge_response: 0.0
S_power_balance: 0.18771558466138621
S_transport: nan
density_support: 0.1436261210993442
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: boundary_ambiguous_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.3522 |     0.4102 |      0.058 |           411 |         469 |
|       0.4822 |     0.4852 |      0.003 |           541 |         544 |

## 10. Candidate negative intervals

_No negative-leakage intervals found under the v0.1 threshold._

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