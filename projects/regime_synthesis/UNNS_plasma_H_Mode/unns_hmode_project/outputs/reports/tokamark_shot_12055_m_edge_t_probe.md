# TokaMark First m_edge(t) Probe — Shot 12055

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

- shot_id: `12055`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12055.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12055.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `0`

## 4. Time grid

```text
dt:       0.001
count:    341
time_min: -0.050400011241436005
time_max: 0.2895999887585643
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

| quantity              |   finite_count |   total_count |   finite_fraction |        min |   median |     mean |      max |      std |
|:----------------------|---------------:|--------------:|------------------:|-----------:|---------:|---------:|---------:|---------:|
| S_power_balance       |            300 |           341 |          0.879765 |  0         | 0.119273 | 0.235542 | 0.966975 | 0.266006 |
| S_transport           |            220 |           341 |          0.645161 |  0         | 0.476477 | 0.454475 | 0.90226  | 0.19004  |
| S_edge_response       |            300 |           341 |          0.879765 |  0.0109716 | 0.476221 | 0.460153 | 0.826721 | 0.157568 |
| C_edge_capacity       |            300 |           341 |          0.879765 |  0.0924885 | 0.470923 | 0.503417 | 0.725083 | 0.120803 |
| F_route_fragmentation |            341 |           341 |          1        |  0.0465164 | 0.311093 | 0.398922 | 1        | 0.265552 |
| m_edge                |            300 |           341 |          0.879765 | -0.365577  | 0.206909 | 0.186642 | 0.505867 | 0.215892 |
| missingness_pressure  |            341 |           341 |          1        |  0         | 0        | 0.237537 | 1        | 0.336227 |

## 7. Margin-state counts

```text
positive_boundary_margin: 154
boundary_ambiguous_margin: 118
insufficient_data: 41
negative_leakage_margin: 28
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.15859998875856418
m_edge: 0.5058666422402907
C_edge_capacity: 0.6636092396387451
F_route_fragmentation: 0.15774259739845448
S_edge_response: 0.5247331965708111
S_power_balance: 0.10363068716478928
S_transport: 0.24690841816510953
density_support: 0.9340299636047428
geometry_stability: 0.6709406018086153
missingness_pressure: 0.0
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.012599988758564051
m_edge: -0.3655771817863433
C_edge_capacity: 0.2582492085663572
F_route_fragmentation: 0.6238263903527005
S_edge_response: 0.2501217399464368
S_power_balance: 0.8362532507594
S_transport: 0.5006449006416627
density_support: 0.2745041458061978
geometry_stability: nan
missingness_pressure: 0.2222222222222222
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.0736 |     0.0776 |      0.004 |           124 |         128 |
|       0.0796 |     0.2236 |      0.144 |           130 |         274 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|  -0.00940001 | 0.00459999 |      0.014 |            41 |          55 |
|   0.0106     | 0.0196     |      0.009 |            61 |          70 |

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