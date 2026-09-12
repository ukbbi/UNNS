# TokaMark First m_edge(t) Probe — Shot 11958

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

- shot_id: `11958`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11958.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11958.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `2`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    453
time_min: -0.05800000578165054
time_max: 0.39399999421834986
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
| S_power_balance       |            403 |           453 |          0.889625 |   0         |   0.738135 |   0.53426   |   0.986805 |   0.395231 |
| S_transport           |              0 |           453 |          0        | nan         | nan        | nan         | nan        | nan        |
| S_edge_response       |            403 |           453 |          0.889625 |   0         |   0.331589 |   0.342043  |   0.61255  |   0.149758 |
| C_edge_capacity       |            403 |           453 |          0.889625 |   0.0690884 |   0.387876 |   0.423689  |   0.676669 |   0.126451 |
| F_route_fragmentation |            453 |           453 |          1        |   0.040404  |   0.711034 |   0.546165  |   1        |   0.346918 |
| m_edge                |            403 |           453 |          0.889625 |  -0.647849  |  -0.161786 |  -0.0661689 |   0.36627  |   0.259559 |
| missingness_pressure  |            453 |           453 |          1        |   0.222222  |   0.222222 |   0.368408  |   1        |   0.242505 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 186
negative_leakage_margin: 114
positive_boundary_margin: 103
insufficient_data: 50
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.13499999421834963
m_edge: 0.36626985639165804
C_edge_capacity: 0.41362067792168467
F_route_fragmentation: 0.04735082153002662
S_edge_response: 0.2536934091983062
S_power_balance: 0.008490510265094273
S_transport: nan
density_support: 0.4512953515824106
geometry_stability: 0.6958005417077157
missingness_pressure: 0.2222222222222222
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.3229999942183498
m_edge: -0.647849403749933
C_edge_capacity: 0.0690884168883394
F_route_fragmentation: 0.7169378206382725
S_edge_response: 0.0
S_power_balance: 0.777491904236901
S_transport: nan
density_support: 0.2072652506650182
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.047 |      0.141 |      0.094 |           105 |         199 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.231 |      0.234 |      0.003 |           289 |         292 |
|        0.271 |      0.276 |      0.005 |           329 |         334 |
|        0.312 |      0.393 |      0.081 |           370 |         451 |

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