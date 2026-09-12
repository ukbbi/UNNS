# TokaMark First m_edge(t) Probe — Shot 11876

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

- shot_id: `11876`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11876.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11876.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `2`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    537
time_min: -0.06940000504255295
time_max: 0.46659999495744753
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

| quantity              |   finite_count |   total_count |   finite_fraction |          min |      median |        mean |        max |        std |
|:----------------------|---------------:|--------------:|------------------:|-------------:|------------:|------------:|-----------:|-----------:|
| S_power_balance       |            476 |           537 |          0.886406 |   0.0139789  |   0.503467  |   0.505439  |   1        |   0.212992 |
| S_transport           |              0 |           537 |          0        | nan          | nan         | nan         | nan        | nan        |
| S_edge_response       |            476 |           537 |          0.886406 |   0.00444717 |   0.488219  |   0.425641  |   0.707172 |   0.168249 |
| C_edge_capacity       |            476 |           537 |          0.886406 |   0.14018    |   0.508545  |   0.487387  |   0.690709 |   0.112791 |
| F_route_fragmentation |            537 |           537 |          1        |   0.0518413  |   0.490288  |   0.524626  |   1        |   0.240194 |
| m_edge                |            476 |           537 |          0.886406 |  -0.590862   |   0.0156955 |   0.0236812 |   0.568895 |   0.233492 |
| missingness_pressure  |            537 |           537 |          1        |   0.222222   |   0.222222  |   0.358163  |   1        |   0.246603 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 271
positive_boundary_margin: 116
negative_leakage_margin: 89
insufficient_data: 61
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.24259999495744733
m_edge: 0.5688954772308871
C_edge_capacity: 0.6657979897613409
F_route_fragmentation: 0.09690251253045383
S_edge_response: 0.5540186014372664
S_power_balance: 0.0690536881545053
S_transport: nan
density_support: 0.651689751958158
geometry_stability: 0.9034650042126728
missingness_pressure: 0.2222222222222222
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.003599994957447117
m_edge: -0.5908616292621237
C_edge_capacity: 0.19480413970983626
F_route_fragmentation: 0.7856657689719599
S_edge_response: 0.2693945207132828
S_power_balance: 0.8614927299780745
S_transport: nan
density_support: 0.04562337770294325
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.1246 |     0.1276 |      0.003 |           194 |         197 |
|       0.1666 |     0.1706 |      0.004 |           236 |         240 |
|       0.1786 |     0.1816 |      0.003 |           248 |         251 |
|       0.1886 |     0.1916 |      0.003 |           258 |         261 |
|       0.1996 |     0.2026 |      0.003 |           269 |         272 |
|       0.2056 |     0.2136 |      0.008 |           275 |         283 |
|       0.2406 |     0.2436 |      0.003 |           310 |         313 |

## 10. Candidate negative intervals

|   start_time |    end_time |   duration |   start_index |   end_index |
|-------------:|------------:|-----------:|--------------:|------------:|
|  -0.00540001 | -0.00140001 |      0.004 |            64 |          68 |
|   0.00259999 |  0.00659999 |      0.004 |            72 |          76 |
|   0.3866     |  0.3896     |      0.003 |           456 |         459 |
|   0.4086     |  0.4126     |      0.004 |           478 |         482 |
|   0.4256     |  0.4296     |      0.004 |           495 |         499 |
|   0.4496     |  0.4596     |      0.01  |           519 |         529 |

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