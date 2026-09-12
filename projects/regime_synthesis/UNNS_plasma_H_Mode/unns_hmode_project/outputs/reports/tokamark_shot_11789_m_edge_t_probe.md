# TokaMark First m_edge(t) Probe — Shot 11789

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

- shot_id: `11789`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11789.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11789.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `3`
  - `interferometer_n_e_line`: `KeyError('Missing array metadata: interferometer/n_e_line/.zarray')`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    506
time_min: -0.06720000505447388
time_max: 0.43779999494552657
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

| quantity              |   finite_count |   total_count |   finite_fraction |         min |     median |        mean |        max |        std |
|:----------------------|---------------:|--------------:|------------------:|------------:|-----------:|------------:|-----------:|-----------:|
| S_power_balance       |            447 |           506 |          0.883399 |   0         |   0.550898 |   0.54084   |   1        |   0.265526 |
| S_transport           |              0 |           506 |          0        | nan         | nan        | nan         | nan        | nan        |
| S_edge_response       |            447 |           506 |          0.883399 |   0         |   0.645612 |   0.601092  |   0.781894 |   0.171142 |
| C_edge_capacity       |            447 |           506 |          0.883399 |   0         |   0.662738 |   0.611863  |   0.814526 |   0.162225 |
| F_route_fragmentation |            506 |           506 |          1        |   0.0606061 |   0.511341 |   0.57119   |   1        |   0.25741  |
| m_edge                |            447 |           506 |          0.883399 |  -0.919192  |   0.128838 |   0.0972727 |   0.694985 |   0.275515 |
| missingness_pressure  |            506 |           506 |          1        |   0.333333  |   0.333333 |   0.466842  |   1        |   0.215389 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 245
positive_boundary_margin: 149
insufficient_data: 59
negative_leakage_margin: 53
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.15479999494552632
m_edge: 0.6949852520795213
C_edge_capacity: 0.7900249011657096
F_route_fragmentation: 0.0950396490861882
S_edge_response: 0.7631492158851112
S_power_balance: 0.04208549703126705
S_transport: nan
density_support: nan
geometry_stability: 0.8437762717269063
missingness_pressure: 0.33333333333333337
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.3657999949455265
m_edge: -0.9191919191919191
C_edge_capacity: 0.0
F_route_fragmentation: 0.9191919191919191
S_edge_response: 0.0
S_power_balance: 1.0
S_transport: nan
density_support: nan
geometry_stability: nan
missingness_pressure: 0.5555555555555556
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.1348 |     0.1398 |      0.005 |           202 |         207 |
|       0.1478 |     0.1528 |      0.005 |           215 |         220 |
|       0.1578 |     0.1648 |      0.007 |           225 |         232 |
|       0.1668 |     0.1718 |      0.005 |           234 |         239 |
|       0.1758 |     0.1808 |      0.005 |           243 |         248 |
|       0.1878 |     0.1958 |      0.008 |           255 |         263 |
|       0.1978 |     0.2028 |      0.005 |           265 |         270 |
|       0.2168 |     0.2208 |      0.004 |           284 |         288 |
|       0.2518 |     0.2548 |      0.003 |           319 |         322 |
|       0.3078 |     0.3118 |      0.004 |           375 |         379 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.3498 |     0.3608 |      0.011 |           417 |         428 |

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