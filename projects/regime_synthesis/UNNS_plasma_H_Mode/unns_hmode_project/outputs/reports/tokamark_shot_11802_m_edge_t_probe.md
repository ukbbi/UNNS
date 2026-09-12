# TokaMark First m_edge(t) Probe — Shot 11802

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

- shot_id: `11802`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11802.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11802.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `2`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    496
time_min: -0.06760000437498093
time_max: 0.4273999956250195
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

| quantity              |   finite_count |   total_count |   finite_fraction |          min |     median |       mean |        max |        std |
|:----------------------|---------------:|--------------:|------------------:|-------------:|-----------:|-----------:|-----------:|-----------:|
| S_power_balance       |            438 |           496 |          0.883065 |   0.00543148 |   0.34034  |   0.376212 |   1        |   0.205108 |
| S_transport           |              0 |           496 |          0        | nan          | nan        | nan        | nan        | nan        |
| S_edge_response       |            438 |           496 |          0.883065 |   0          |   0.509192 |   0.497154 |   0.87409  |   0.171504 |
| C_edge_capacity       |            438 |           496 |          0.883065 |   0.121374   |   0.572476 |   0.536166 |   0.737411 |   0.127089 |
| F_route_fragmentation |            496 |           496 |          1        |   0.044848   |   0.364965 |   0.434369 |   1        |   0.262603 |
| m_edge                |            438 |           496 |          0.883065 |  -0.551002   |   0.227214 |   0.176698 |   0.606079 |   0.244112 |
| missingness_pressure  |            496 |           496 |          1        |   0.222222   |   0.222222 |   0.367832 |   1        |   0.248361 |

## 7. Margin-state counts

```text
positive_boundary_margin: 237
boundary_ambiguous_margin: 166
insufficient_data: 58
negative_leakage_margin: 35
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.0713999956250192
m_edge: 0.6060794925373134
C_edge_capacity: 0.6671941082818156
F_route_fragmentation: 0.06111461574450214
S_edge_response: 0.8600998378398083
S_power_balance: 0.025312925416119913
S_transport: nan
density_support: 0.5179869125211196
geometry_stability: 0.4305898449265263
missingness_pressure: 0.2222222222222222
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.36239999562501946
m_edge: -0.5510019845313796
C_edge_capacity: 0.3009388622464183
F_route_fragmentation: 0.8519408467777979
S_edge_response: 0.39718927855018615
S_power_balance: 0.9424956028518765
S_transport: nan
density_support: 0.10843802963888256
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.0274 |     0.0324 |      0.005 |            95 |         100 |
|       0.0484 |     0.0534 |      0.005 |           116 |         121 |
|       0.0624 |     0.0784 |      0.016 |           130 |         146 |
|       0.0874 |     0.0934 |      0.006 |           155 |         161 |
|       0.1074 |     0.1124 |      0.005 |           175 |         180 |
|       0.1234 |     0.1374 |      0.014 |           191 |         205 |
|       0.1434 |     0.1584 |      0.015 |           211 |         226 |
|       0.1614 |     0.1784 |      0.017 |           229 |         246 |
|       0.1824 |     0.1914 |      0.009 |           250 |         259 |
|       0.1934 |     0.1964 |      0.003 |           261 |         264 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.3604 |     0.3634 |      0.003 |           428 |         431 |
|       0.3744 |     0.3774 |      0.003 |           442 |         445 |
|       0.3814 |     0.3844 |      0.003 |           449 |         452 |

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