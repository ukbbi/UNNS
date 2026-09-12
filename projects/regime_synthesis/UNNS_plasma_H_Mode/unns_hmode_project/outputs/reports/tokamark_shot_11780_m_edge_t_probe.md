# TokaMark First m_edge(t) Probe — Shot 11780

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

- shot_id: `11780`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11780.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11780.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `3`
  - `summary_power_nbi`: `KeyError('Missing array metadata: summary/power_nbi/.zarray')`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    499
time_min: -0.06720000505447388
time_max: 0.43079999494552657
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

| quantity              |   finite_count |   total_count |   finite_fraction |         min |     median |       mean |        max |        std |
|:----------------------|---------------:|--------------:|------------------:|------------:|-----------:|-----------:|-----------:|-----------:|
| S_power_balance       |            441 |           499 |          0.883768 |   0         |   0.317533 |   0.417719 |   1        |   0.310606 |
| S_transport           |              0 |           499 |          0        | nan         | nan        | nan        | nan        | nan        |
| S_edge_response       |            441 |           499 |          0.883768 |   0         |   0.575167 |   0.521148 |   0.735828 |   0.151547 |
| C_edge_capacity       |            441 |           499 |          0.883768 |   0.111951  |   0.587957 |   0.54966  |   0.733404 |   0.13261  |
| F_route_fragmentation |            499 |           499 |          1        |   0.0606061 |   0.341681 |   0.482041 |   1        |   0.315129 |
| m_edge                |            441 |           499 |          0.883768 |  -0.639664  |   0.308622 |   0.13574  |   0.654207 |   0.376199 |
| missingness_pressure  |            499 |           499 |          1        |   0.333333  |   0.333333 |   0.466934 |   1        |   0.215126 |

## 7. Margin-state counts

```text
positive_boundary_margin: 248
negative_leakage_margin: 101
boundary_ambiguous_margin: 92
insufficient_data: 58
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.1467999949455263
m_edge: 0.6542070150619366
C_edge_capacity: 0.7155472662096973
F_route_fragmentation: 0.06134025114776072
S_edge_response: 0.6797350519886816
S_power_balance: 0.0008973439954112382
S_transport: nan
density_support: 0.6818957068437437
geometry_stability: 0.8208232540176825
missingness_pressure: 0.33333333333333337
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.003799994945526186
m_edge: -0.6396636829560278
C_edge_capacity: 0.1999585039893792
F_route_fragmentation: 0.839622186945407
S_edge_response: 0.27111650881407984
S_power_balance: 0.9027481050320407
S_transport: nan
density_support: 0.05764249433997797
geometry_stability: nan
missingness_pressure: 0.5555555555555556
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.0728 |     0.3198 |      0.247 |           140 |         387 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|  -0.00920001 | 0.00879999 |      0.018 |            58 |          76 |
|   0.3468     | 0.3518     |      0.005 |           414 |         419 |
|   0.3578     | 0.4308     |      0.073 |           425 |         498 |

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