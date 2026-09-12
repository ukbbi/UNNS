# TokaMark First m_edge(t) Probe — Shot 11795

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

- shot_id: `11795`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11795.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11795.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `3`
  - `interferometer_n_e_line`: `KeyError('Missing array metadata: interferometer/n_e_line/.zarray')`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    496
time_min: -0.06680000573396683
time_max: 0.4281999942660336
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
| S_power_balance       |            438 |           496 |          0.883065 |   0         |   0.578178 |   0.52889  |   1        |   0.250696 |
| S_transport           |              0 |           496 |          0        | nan         | nan        | nan        | nan        | nan        |
| S_edge_response       |            438 |           496 |          0.883065 |   0         |   0.622482 |   0.588881 |   0.78836  |   0.152186 |
| C_edge_capacity       |            438 |           496 |          0.883065 |   0         |   0.647895 |   0.605488 |   0.798318 |   0.142492 |
| F_route_fragmentation |            496 |           496 |          1        |   0.0606061 |   0.574065 |   0.562601 |   1        |   0.252022 |
| m_edge                |            438 |           496 |          0.883065 |  -0.679857  |   0.091558 |   0.100807 |   0.737712 |   0.270928 |
| missingness_pressure  |            496 |           496 |          1        |   0.333333  |   0.333333 |   0.466398 |   1        |   0.215665 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 243
positive_boundary_margin: 141
insufficient_data: 58
negative_leakage_margin: 54
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.16219999426603338
m_edge: 0.7377119586329368
C_edge_capacity: 0.7983180192389975
F_route_fragmentation: 0.060606060606060615
S_edge_response: 0.7360030341491264
S_power_balance: 0.0
S_transport: nan
density_support: nan
geometry_stability: 0.9229479894187398
missingness_pressure: 0.33333333333333337
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.35719999426603355
m_edge: -0.6798569711856994
C_edge_capacity: 0.0
F_route_fragmentation: 0.6798569711856994
S_edge_response: 0.0
S_power_balance: 0.7074795079923981
S_transport: nan
density_support: nan
geometry_stability: nan
missingness_pressure: 0.5555555555555556
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.0242 |     0.0292 |      0.005 |            91 |          96 |
|       0.0392 |     0.0492 |      0.01  |           106 |         116 |
|       0.0632 |     0.0702 |      0.007 |           130 |         137 |
|       0.0802 |     0.0882 |      0.008 |           147 |         155 |
|       0.1162 |     0.1212 |      0.005 |           183 |         188 |
|       0.1392 |     0.1492 |      0.01  |           206 |         216 |
|       0.1602 |     0.1702 |      0.01  |           227 |         237 |
|       0.1812 |     0.1882 |      0.007 |           248 |         255 |
|       0.2022 |     0.2082 |      0.006 |           269 |         275 |
|       0.2202 |     0.2292 |      0.009 |           287 |         296 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.3252 |     0.3282 |      0.003 |           392 |         395 |
|       0.3362 |     0.3662 |      0.03  |           403 |         433 |
|       0.4052 |     0.4082 |      0.003 |           472 |         475 |

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