# TokaMark First m_edge(t) Probe — Shot 11772

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

- shot_id: `11772`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11772.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11772.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `3`
  - `summary_power_nbi`: `KeyError('Missing array metadata: summary/power_nbi/.zarray')`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    479
time_min: -0.0674000084400177
time_max: 0.4105999915599827
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

| quantity              |   finite_count |   total_count |   finite_fraction |          min |     median |       mean |        max |         std |
|:----------------------|---------------:|--------------:|------------------:|-------------:|-----------:|-----------:|-----------:|------------:|
| S_power_balance       |            420 |           479 |          0.876827 |   0          |   0.142133 |   0.290029 |   1        |   0.348758  |
| S_transport           |              0 |           479 |          0        | nan          | nan        | nan        | nan        | nan         |
| S_edge_response       |            420 |           479 |          0.876827 |   0.00594257 |   0.387264 |   0.405146 |   0.753489 |   0.185208  |
| C_edge_capacity       |            420 |           479 |          0.876827 |   0.124409   |   0.545503 |   0.520601 |   0.697226 |   0.0983076 |
| F_route_fragmentation |            479 |           479 |          1        |   0.0606061  |   0.208927 |   0.394504 |   1        |   0.361631  |
| m_edge                |            420 |           479 |          0.876827 |  -0.687421   |   0.366728 |   0.211155 |   0.612999 |   0.37325   |
| missingness_pressure  |            479 |           479 |          1        |   0.333333   |   0.333333 |   0.47112  |   1        |   0.219385  |

## 7. Margin-state counts

```text
positive_boundary_margin: 315
negative_leakage_margin: 90
insufficient_data: 59
boundary_ambiguous_margin: 15
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.30459999155998263
m_edge: 0.6129985416746535
C_edge_capacity: 0.6736046022807142
F_route_fragmentation: 0.060606060606060615
S_edge_response: 0.5462495817087848
S_power_balance: 0.0
S_transport: nan
density_support: 0.805595009719465
geometry_stability: 0.7963242359858222
missingness_pressure: 0.33333333333333337
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.002599991559982362
m_edge: -0.6874205746253836
C_edge_capacity: 0.1528550320586895
F_route_fragmentation: 0.8402756066840731
S_edge_response: 0.19139468493141834
S_power_balance: 0.903546729157077
S_transport: nan
density_support: 0.07577572631323183
geometry_stability: nan
missingness_pressure: 0.5555555555555556
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.0196 |     0.3336 |      0.314 |            87 |         401 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|  -0.00940001 | 0.00659999 |      0.016 |            58 |          74 |
|   0.3376     | 0.4096     |      0.072 |           405 |         477 |

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