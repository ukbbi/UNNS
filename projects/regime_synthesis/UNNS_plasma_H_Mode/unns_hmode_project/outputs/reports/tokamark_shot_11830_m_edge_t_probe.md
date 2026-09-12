# TokaMark First m_edge(t) Probe — Shot 11830

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

- shot_id: `11830`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11830.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11830.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `2`
  - `soft_x_lower`: `KeyError('Missing array metadata: soft_x_rays/horizontal_cam_lower/.zarray')`
  - `soft_x_upper`: `KeyError('Missing array metadata: soft_x_rays/horizontal_cam_upper/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    376
time_min: -0.06720000505447388
time_max: 0.30779999494552646
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

| quantity              |   finite_count |   total_count |   finite_fraction |       min |     median |      mean |      max |      std |
|:----------------------|---------------:|--------------:|------------------:|----------:|-----------:|----------:|---------:|---------:|
| S_power_balance       |            318 |           376 |          0.845745 |  0        |  0.710196  | 0.579243  | 1        | 0.370855 |
| S_transport           |            220 |           376 |          0.585106 |  0.108393 |  0.481211  | 0.499589  | 0.80834  | 0.195234 |
| S_edge_response       |            318 |           376 |          0.845745 |  0        |  0.499333  | 0.581373  | 1        | 0.266043 |
| C_edge_capacity       |            318 |           376 |          0.845745 |  0.123503 |  0.612696  | 0.562577  | 0.750578 | 0.13275  |
| F_route_fragmentation |            376 |           376 |          1        |  0.137264 |  0.694692  | 0.625778  | 1        | 0.29669  |
| m_edge                |            318 |           376 |          0.845745 | -0.745802 | -0.0366668 | 0.0050537 | 0.387901 | 0.234438 |
| missingness_pressure  |            376 |           376 |          1        |  0.222222 |  0.222222  | 0.469858  | 1        | 0.291185 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 147
negative_leakage_margin: 86
positive_boundary_margin: 85
insufficient_data: 58
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.06879999494552624
m_edge: 0.3879011835469034
C_edge_capacity: 0.5400460434068379
F_route_fragmentation: 0.15214485985993453
S_edge_response: 0.44456915293760046
S_power_balance: 3.095364758602014e-06
S_transport: 0.28871387716349095
density_support: 0.5602371377889792
geometry_stability: 0.7108087299631715
missingness_pressure: 0.2222222222222222
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.2377999949455264
m_edge: -0.7458024540979937
C_edge_capacity: 0.12350314555463215
F_route_fragmentation: 0.8693055996526259
S_edge_response: 0.1120976693809741
S_power_balance: 0.9143364736495058
S_transport: nan
density_support: 0.14631409790194827
geometry_stability: nan
missingness_pressure: 0.6666666666666667
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |    end_time |   duration |   start_index |   end_index |
|-------------:|------------:|-----------:|--------------:|------------:|
|  -0.00920001 | -0.00320001 |      0.006 |            58 |          64 |
|   0.0268     |  0.0958     |      0.069 |            94 |         163 |
|   0.3038     |  0.3078     |      0.004 |           371 |         375 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.2148 |     0.2948 |       0.08 |           282 |         362 |

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