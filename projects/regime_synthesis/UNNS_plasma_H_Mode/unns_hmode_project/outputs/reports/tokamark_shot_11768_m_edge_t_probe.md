# TokaMark First m_edge(t) Probe — Shot 11768

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

- shot_id: `11768`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11768.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11768.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `3`
  - `summary_power_nbi`: `KeyError('Missing array metadata: summary/power_nbi/.zarray')`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    416
time_min: -0.06720000505447388
time_max: 0.3477999949455265
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
| S_power_balance       |            358 |           416 |          0.860577 |   0          |   0.148294 |   0.343427 |   1        |   0.373049 |
| S_transport           |              0 |           416 |          0        | nan          | nan        | nan        | nan        | nan        |
| S_edge_response       |            358 |           416 |          0.860577 |   0.00948361 |   0.402638 |   0.416507 |   0.755515 |   0.169861 |
| C_edge_capacity       |            358 |           416 |          0.860577 |   0.0705326  |   0.505751 |   0.499322 |   0.702116 |   0.108701 |
| F_route_fragmentation |            416 |           416 |          1        |   0.0606061  |   0.220747 |   0.445335 |   1        |   0.372913 |
| m_edge                |            358 |           416 |          0.860577 |  -0.848659   |   0.372648 |   0.143849 |   0.622713 |   0.400795 |
| missingness_pressure  |            416 |           416 |          1        |   0.333333   |   0.333333 |   0.491987 |   1        |   0.226707 |

## 7. Margin-state counts

```text
positive_boundary_margin: 222
negative_leakage_margin: 96
insufficient_data: 58
boundary_ambiguous_margin: 40
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.09279999494552627
m_edge: 0.6227132671997299
C_edge_capacity: 0.6844493962051987
F_route_fragmentation: 0.061736129005468876
S_edge_response: 0.5728606139608844
S_power_balance: 0.0013811947103878864
S_transport: nan
density_support: 0.8445282606956402
geometry_stability: 0.747548096203386
missingness_pressure: 0.33333333333333337
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.0027999949455261852
m_edge: -0.8486592871581259
C_edge_capacity: 0.07053263203379323
F_route_fragmentation: 0.9191919191919191
S_edge_response: 0.10579894805068984
S_power_balance: 1.0
S_transport: nan
density_support: 0.0
geometry_stability: nan
missingness_pressure: 0.5555555555555556
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.0518 |     0.2728 |      0.221 |           119 |         340 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|  -0.00920001 |     0.0118 |      0.021 |            58 |          79 |
|   0.2758     |     0.3478 |      0.072 |           343 |         415 |

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