# TokaMark First m_edge(t) Probe — Shot 12007

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

- shot_id: `12007`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12007.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12007.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `0`

## 4. Time grid

```text
dt:       0.001
count:    446
time_min: -0.06920000910758972
time_max: 0.3757999908924107
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
| S_power_balance       |            386 |           446 |          0.865471 |  0         | 0.468475 | 0.42535  | 1        | 0.247585 |
| S_transport           |            296 |           446 |          0.663677 |  0.0330082 | 0.475568 | 0.445273 | 0.909662 | 0.225735 |
| S_edge_response       |            386 |           446 |          0.865471 |  0         | 0.509694 | 0.482739 | 0.748938 | 0.156259 |
| C_edge_capacity       |            386 |           446 |          0.865471 |  0.0973251 | 0.524947 | 0.539696 | 0.780114 | 0.154002 |
| F_route_fragmentation |            446 |           446 |          1        |  0.0392025 | 0.430883 | 0.493673 | 1        | 0.25203  |
| m_edge                |            386 |           446 |          0.865471 | -0.666409  | 0.146025 | 0.124727 | 0.622765 | 0.258093 |
| missingness_pressure  |            446 |           446 |          1        |  0         | 0        | 0.239163 | 1        | 0.347149 |

## 7. Margin-state counts

```text
positive_boundary_margin: 171
boundary_ambiguous_margin: 169
insufficient_data: 60
negative_leakage_margin: 46
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.19979999089241052
m_edge: 0.622765466821574
C_edge_capacity: 0.6619679402819303
F_route_fragmentation: 0.039202473460356276
S_edge_response: 0.4500996748917954
S_power_balance: 0.0
S_transport: 0.08711660768968062
density_support: 0.8463523242505605
geometry_stability: 0.90132008709357
missingness_pressure: 0.0
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.3047999908924106
m_edge: -0.6664089217702088
C_edge_capacity: 0.12375998727807018
F_route_fragmentation: 0.790168909048279
S_edge_response: 0.002385772073864676
S_power_balance: 0.8669965678491312
S_transport: nan
density_support: 0.3665084176864812
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.1048 |     0.1088 |      0.004 |           174 |         178 |
|       0.1118 |     0.1318 |      0.02  |           181 |         201 |
|       0.1338 |     0.1368 |      0.003 |           203 |         206 |
|       0.1408 |     0.1598 |      0.019 |           210 |         229 |
|       0.1648 |     0.2238 |      0.059 |           234 |         293 |
|       0.2348 |     0.2378 |      0.003 |           304 |         307 |
|       0.2478 |     0.2568 |      0.009 |           317 |         326 |
|       0.2608 |     0.2708 |      0.01  |           330 |         340 |
|       0.2728 |     0.2758 |      0.003 |           342 |         345 |
|       0.2818 |     0.2868 |      0.005 |           351 |         356 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.3028 |     0.3058 |      0.003 |           372 |         375 |
|       0.3528 |     0.3578 |      0.005 |           422 |         427 |

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