# TokaMark First m_edge(t) Probe — Shot 12046

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

- shot_id: `12046`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12046.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12046.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `0`

## 4. Time grid

```text
dt:       0.001
count:    451
time_min: -0.06800001114606857
time_max: 0.3819999888539318
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
| S_power_balance       |            392 |           451 |          0.86918  |  0         | 0.464174 | 0.482961 | 1        | 0.205114 |
| S_transport           |            301 |           451 |          0.667406 |  0.0829893 | 0.440123 | 0.438059 | 0.836285 | 0.165123 |
| S_edge_response       |            392 |           451 |          0.86918  |  0         | 0.524539 | 0.489634 | 0.782915 | 0.184986 |
| C_edge_capacity       |            392 |           451 |          0.86918  |  0.100555  | 0.529227 | 0.551613 | 0.844496 | 0.169374 |
| F_route_fragmentation |            451 |           451 |          1        |  0.0608268 | 0.448011 | 0.518045 | 1        | 0.236178 |
| m_edge                |            392 |           451 |          0.86918  | -0.556986  | 0.175811 | 0.106107 | 0.589814 | 0.254467 |
| missingness_pressure  |            451 |           451 |          1        |  0         | 0        | 0.225425 | 1        | 0.347787 |

## 7. Margin-state counts

```text
positive_boundary_margin: 181
boundary_ambiguous_margin: 143
negative_leakage_margin: 68
insufficient_data: 59
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.19899998885393166
m_edge: 0.5898142764000227
C_edge_capacity: 0.7486848807764462
F_route_fragmentation: 0.15887060437642353
S_edge_response: 0.6329902080875117
S_power_balance: 0.006567694985760012
S_transport: 0.34647809251740336
density_support: 0.8243919210226494
geometry_stability: 0.9043671859081123
missingness_pressure: 0.0
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.00299998885393149
m_edge: -0.5569858641843879
C_edge_capacity: 0.32116834515679904
F_route_fragmentation: 0.8781542093411869
S_edge_response: 0.46241613254986247
S_power_balance: 0.9745341570960186
S_transport: nan
density_support: 0.03867277037067222
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.095 |      0.098 |      0.003 |           163 |         166 |
|        0.105 |      0.119 |      0.014 |           173 |         187 |
|        0.127 |      0.137 |      0.01  |           195 |         205 |
|        0.144 |      0.165 |      0.021 |           212 |         233 |
|        0.167 |      0.183 |      0.016 |           235 |         251 |
|        0.188 |      0.258 |      0.07  |           256 |         326 |
|        0.26  |      0.274 |      0.014 |           328 |         342 |
|        0.282 |      0.285 |      0.003 |           350 |         353 |
|        0.287 |      0.29  |      0.003 |           355 |         358 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|  -0.00600001 | 0.00899999 |      0.015 |            62 |          77 |
|   0.328      | 0.331      |      0.003 |           396 |         399 |
|   0.334      | 0.343      |      0.009 |           402 |         411 |
|   0.347      | 0.356      |      0.009 |           415 |         424 |
|   0.366      | 0.372      |      0.006 |           434 |         440 |

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