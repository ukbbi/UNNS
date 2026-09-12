# TokaMark First m_edge(t) Probe — Shot 11776

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

- shot_id: `11776`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11776.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11776.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `4`
  - `summary_power_nbi`: `KeyError('Missing array metadata: summary/power_nbi/.zarray')`
  - `dalpha_voltage`: `KeyError('Missing array metadata: spectrometer_visible/filter_spectrometer_dalpha_voltage/.zarray')`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    523
time_min: -0.06720000505447388
time_max: 0.4547999949455266
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
| S_power_balance       |            464 |           523 |          0.887189 |   0         |   0.14419  |   0.265143 |   1        |   0.320223 |
| S_transport           |              0 |           523 |          0        | nan         | nan        | nan        | nan        | nan        |
| S_edge_response       |            464 |           523 |          0.887189 |   0         |   0.512797 |   0.493588 |   1        |   0.229431 |
| C_edge_capacity       |            464 |           523 |          0.887189 |   0         |   0.665586 |   0.557564 |   0.859897 |   0.230614 |
| F_route_fragmentation |            523 |           523 |          1        |   0.0808081 |   0.221992 |   0.386545 |   1        |   0.33986  |
| m_edge                |            464 |           523 |          0.887189 |  -0.939394  |   0.486177 |   0.249023 |   0.727017 |   0.496139 |
| missingness_pressure  |            523 |           523 |          1        |   0.444444  |   0.444444 |   0.559805 |   1        |   0.182259 |

## 7. Margin-state counts

```text
positive_boundary_margin: 345
negative_leakage_margin: 82
insufficient_data: 59
boundary_ambiguous_margin: 37
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.31479999494552646
m_edge: 0.7270169659135489
C_edge_capacity: 0.8106372193636006
F_route_fragmentation: 0.08362025345005167
S_edge_response: 0.8545321636664543
S_power_balance: 0.0034370998957421596
S_transport: nan
density_support: 0.7966430814784407
geometry_stability: 0.7368414686430528
missingness_pressure: 0.4444444444444444
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.39979999494552654
m_edge: -0.9393939393939394
C_edge_capacity: 0.0
F_route_fragmentation: 0.9393939393939394
S_edge_response: 0.0
S_power_balance: 1.0
S_transport: nan
density_support: 0.0
geometry_stability: nan
missingness_pressure: 0.6666666666666667
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.0178 |     0.3328 |      0.315 |            85 |         400 |
|       0.3398 |     0.3498 |      0.01  |           407 |         417 |
|       0.3588 |     0.3718 |      0.013 |           426 |         439 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|  -0.00920001 | 0.00579999 |      0.015 |            58 |          73 |
|   0.3888     | 0.4538     |      0.065 |           456 |         521 |

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