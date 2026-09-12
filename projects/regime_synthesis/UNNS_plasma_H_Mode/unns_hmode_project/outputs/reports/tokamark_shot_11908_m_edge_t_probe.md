# TokaMark First m_edge(t) Probe — Shot 11908

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

- shot_id: `11908`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11908.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11908.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `2`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    548
time_min: -0.06080000847578049
time_max: 0.48619999152422
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

| quantity              |   finite_count |   total_count |   finite_fraction |           min |       median |        mean |        max |        std |
|:----------------------|---------------:|--------------:|------------------:|--------------:|-------------:|------------:|-----------:|-----------:|
| S_power_balance       |            497 |           548 |          0.906934 |   0.000288174 |   0.63458    |   0.489476  |   0.86587  |   0.281708 |
| S_transport           |              0 |           548 |          0        | nan           | nan          | nan         | nan        | nan        |
| S_edge_response       |            497 |           548 |          0.906934 |   0.000420498 |   0.411258   |   0.368248  |   0.628823 |   0.154261 |
| C_edge_capacity       |            497 |           548 |          0.906934 |   0.0359954   |   0.405027   |   0.465728  |   0.803969 |   0.190283 |
| F_route_fragmentation |            548 |           548 |          1        |   0.0502646   |   0.575056   |   0.503573  |   1        |   0.264896 |
| m_edge                |            497 |           548 |          0.906934 |  -0.607       |  -0.00489147 |   0.0130961 |   0.543745 |   0.315311 |
| missingness_pressure  |            548 |           548 |          1        |   0.222222    |   0.222222   |   0.353204  |   1        |   0.229134 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 233
negative_leakage_margin: 133
positive_boundary_margin: 131
insufficient_data: 51
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.32719999152421986
m_edge: 0.5437452449997587
C_edge_capacity: 0.7983138215773176
F_route_fragmentation: 0.2545685765775588
S_edge_response: 0.6198867212147751
S_power_balance: 0.2617566553231892
S_transport: nan
density_support: 0.9947910287660389
geometry_stability: 0.958690815113681
missingness_pressure: 0.2222222222222222
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.02419999152421959
m_edge: -0.6069995714911735
C_edge_capacity: 0.13607480837262595
F_route_fragmentation: 0.7430743798637994
S_edge_response: 0.07148988962031468
S_power_balance: 0.8094365877347671
S_transport: nan
density_support: 0.26524464587724844
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.2692 |     0.3842 |      0.115 |           330 |         445 |
|       0.3872 |     0.3922 |      0.005 |           448 |         453 |
|       0.3982 |     0.4012 |      0.003 |           459 |         462 |
|       0.4822 |     0.4862 |      0.004 |           543 |         547 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.0132 |     0.1432 |       0.13 |            74 |         204 |

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