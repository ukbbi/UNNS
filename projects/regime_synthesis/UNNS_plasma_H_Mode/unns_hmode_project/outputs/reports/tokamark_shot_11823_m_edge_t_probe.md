# TokaMark First m_edge(t) Probe — Shot 11823

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

- shot_id: `11823`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11823.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11823.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `0`

## 4. Time grid

```text
dt:       0.001
count:    476
time_min: -0.06700000911951065
time_max: 0.40799999088048977
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

| quantity              |   finite_count |   total_count |   finite_fraction |        min |   median |      mean |      max |      std |
|:----------------------|---------------:|--------------:|------------------:|-----------:|---------:|----------:|---------:|---------:|
| S_power_balance       |            418 |           476 |          0.878151 |  0         | 0.457085 | 0.46665   | 1        | 0.193259 |
| S_transport           |            315 |           476 |          0.661765 |  0.0933606 | 0.5      | 0.449118  | 0.774303 | 0.19153  |
| S_edge_response       |            418 |           476 |          0.878151 |  0         | 0.502938 | 0.494859  | 0.713281 | 0.121241 |
| C_edge_capacity       |            418 |           476 |          0.878151 |  0.0646229 | 0.543679 | 0.529075  | 0.770548 | 0.129641 |
| F_route_fragmentation |            476 |           476 |          1        |  0.110106  | 0.453586 | 0.504664  | 1        | 0.222598 |
| m_edge                |            418 |           476 |          0.878151 | -0.763488  | 0.140869 | 0.0931416 | 0.489    | 0.197495 |
| missingness_pressure  |            476 |           476 |          1        |  0         | 0        | 0.225023  | 1        | 0.338342 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 218
positive_boundary_margin: 142
insufficient_data: 58
negative_leakage_margin: 58
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.2169999908804896
m_edge: 0.4890000228831718
C_edge_capacity: 0.6623744891070569
F_route_fragmentation: 0.17337446622388508
S_edge_response: 0.4455403711960629
S_power_balance: 0.06331131859506363
S_transport: 0.32196527301356986
density_support: 0.8251335548379382
geometry_stability: 0.9332836591981636
missingness_pressure: 0.0
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.3419999908804897
m_edge: -0.7634878254149712
C_edge_capacity: 0.06462293282920537
F_route_fragmentation: 0.8281107582441766
S_edge_response: 0.010376878033408992
S_power_balance: 0.9133699390885615
S_transport: nan
density_support: 0.17311504242079812
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.152 |      0.159 |      0.007 |           219 |         226 |
|        0.161 |      0.165 |      0.004 |           228 |         232 |
|        0.167 |      0.176 |      0.009 |           234 |         243 |
|        0.178 |      0.182 |      0.004 |           245 |         249 |
|        0.188 |      0.195 |      0.007 |           255 |         262 |
|        0.197 |      0.201 |      0.004 |           264 |         268 |
|        0.215 |      0.218 |      0.003 |           282 |         285 |
|        0.222 |      0.225 |      0.003 |           289 |         292 |
|        0.228 |      0.237 |      0.009 |           295 |         304 |
|        0.239 |      0.243 |      0.004 |           306 |         310 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.34  |      0.349 |      0.009 |           407 |         416 |
|        0.353 |      0.356 |      0.003 |           420 |         423 |
|        0.358 |      0.362 |      0.004 |           425 |         429 |
|        0.365 |      0.374 |      0.009 |           432 |         441 |
|        0.383 |      0.387 |      0.004 |           450 |         454 |
|        0.389 |      0.394 |      0.005 |           456 |         461 |
|        0.4   |      0.403 |      0.003 |           467 |         470 |

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