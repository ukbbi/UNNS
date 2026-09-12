# TokaMark First m_edge(t) Probe — Shot 11941

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

- shot_id: `11941`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11941.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11941.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `0`

## 4. Time grid

```text
dt:       0.001
count:    521
time_min: -0.059000007808208466
time_max: 0.460999992191792
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

| quantity              |   finite_count |   total_count |   finite_fraction |          min |   median |     mean |      max |      std |
|:----------------------|---------------:|--------------:|------------------:|-------------:|---------:|---------:|---------:|---------:|
| S_power_balance       |            471 |           521 |          0.904031 |  0.000589393 | 0.165751 | 0.233543 | 0.746551 | 0.196276 |
| S_transport           |            375 |           521 |          0.71977  |  0.0802625   | 0.361933 | 0.389267 | 0.923101 | 0.153589 |
| S_edge_response       |            471 |           521 |          0.904031 |  0.00101237  | 0.365819 | 0.380775 | 0.673904 | 0.114457 |
| C_edge_capacity       |            471 |           521 |          0.904031 |  0.0554917   | 0.471138 | 0.480356 | 0.677368 | 0.123775 |
| F_route_fragmentation |            521 |           521 |          1        |  0.0871652   | 0.276482 | 0.349667 | 1        | 0.237261 |
| m_edge                |            471 |           521 |          0.904031 | -0.195755    | 0.180108 | 0.199726 | 0.478934 | 0.175913 |
| missingness_pressure  |            521 |           521 |          1        |  0           | 0        | 0.194924 | 1        | 0.313309 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 262
positive_boundary_margin: 209
insufficient_data: 50
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.3369999921917919
m_edge: 0.47893432720070583
C_edge_capacity: 0.6241631220407539
F_route_fragmentation: 0.14522879484004803
S_edge_response: 0.34073540265265645
S_power_balance: 0.1946124867606663
S_transport: 0.12811816843944038
density_support: 0.9591045162175961
geometry_stability: 0.8560771666401065
missingness_pressure: 0.0
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.40199999219179194
m_edge: -0.19575461908059702
C_edge_capacity: 0.055491723281841966
F_route_fragmentation: 0.251246342362439
S_edge_response: 0.0020247469064871536
S_power_balance: 0.20831343078866005
S_transport: nan
density_support: 0.1624256760325516
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: boundary_ambiguous_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.172 |      0.366 |      0.194 |           231 |         425 |
|        0.375 |      0.379 |      0.004 |           434 |         438 |
|        0.39  |      0.396 |      0.006 |           449 |         455 |

## 10. Candidate negative intervals

_No negative-leakage intervals found under the v0.1 threshold._

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