# TokaMark First m_edge(t) Probe — Shot 12063

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

- shot_id: `12063`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12063.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12063.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `0`

## 4. Time grid

```text
dt:       0.001
count:    426
time_min: -0.06800001114606857
time_max: 0.3569999888539318
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
| S_power_balance       |            367 |           426 |          0.861502 |  0         | 0.569205 | 0.514674 | 1        | 0.287845 |
| S_transport           |            281 |           426 |          0.659624 |  0         | 0.484131 | 0.436759 | 0.737484 | 0.176334 |
| S_edge_response       |            367 |           426 |          0.861502 |  0         | 0.572315 | 0.478887 | 0.77312  | 0.188107 |
| C_edge_capacity       |            367 |           426 |          0.861502 |  0.0567782 | 0.559422 | 0.525146 | 0.758847 | 0.142406 |
| F_route_fragmentation |            426 |           426 |          1        |  0.0651664 | 0.516301 | 0.543434 | 1        | 0.253914 |
| m_edge                |            367 |           426 |          0.861502 | -0.770609  | 0.087961 | 0.055111 | 0.475695 | 0.245434 |
| missingness_pressure  |            426 |           426 |          1        |  0         | 0.222222 | 0.314293 | 1        | 0.3142   |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 209
positive_boundary_margin: 110
insufficient_data: 59
negative_leakage_margin: 48
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.20899998885393167
m_edge: 0.47569545087226345
C_edge_capacity: 0.710963099667329
F_route_fragmentation: 0.2352676487950655
S_edge_response: 0.7509394425293954
S_power_balance: 0.020925051544174445
S_transport: 0.45250922972881064
density_support: 0.6310104139431961
geometry_stability: nan
missingness_pressure: 0.2222222222222222
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.003999988853931491
m_edge: -0.7706091622560678
C_edge_capacity: 0.05677815353808274
F_route_fragmentation: 0.8273873157941506
S_edge_response: 0.04706080293370135
S_power_balance: 0.9124857316496409
S_transport: nan
density_support: 0.07621285474684551
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.097 |      0.1   |      0.003 |           165 |         168 |
|        0.115 |      0.119 |      0.004 |           183 |         187 |
|        0.148 |      0.151 |      0.003 |           216 |         219 |
|        0.154 |      0.158 |      0.004 |           222 |         226 |
|        0.168 |      0.173 |      0.005 |           236 |         241 |
|        0.226 |      0.229 |      0.003 |           294 |         297 |
|        0.251 |      0.256 |      0.005 |           319 |         324 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.313 |      0.317 |      0.004 |           381 |         385 |
|        0.322 |      0.326 |      0.004 |           390 |         394 |

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