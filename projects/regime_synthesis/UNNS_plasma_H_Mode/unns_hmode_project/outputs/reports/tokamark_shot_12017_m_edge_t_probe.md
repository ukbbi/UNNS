# TokaMark First m_edge(t) Probe — Shot 12017

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

- shot_id: `12017`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12017.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12017.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `0`

## 4. Time grid

```text
dt:       0.001
count:    546
time_min: -0.06920000910758972
time_max: 0.47579999089241076
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

| quantity              |   finite_count |   total_count |   finite_fraction |         min |    median |      mean |      max |      std |
|:----------------------|---------------:|--------------:|------------------:|------------:|----------:|----------:|---------:|---------:|
| S_power_balance       |            486 |           546 |          0.89011  |  0          | 0.48051   | 0.463853  | 1        | 0.245234 |
| S_transport           |            396 |           546 |          0.725275 |  0          | 0.430113  | 0.441371  | 0.925813 | 0.1858   |
| S_edge_response       |            486 |           546 |          0.89011  |  0.00429717 | 0.523112  | 0.456022  | 0.760646 | 0.178424 |
| C_edge_capacity       |            486 |           546 |          0.89011  |  0.0933021  | 0.513844  | 0.508572  | 0.744847 | 0.128396 |
| F_route_fragmentation |            546 |           546 |          1        |  0.095662   | 0.453408  | 0.488335  | 1        | 0.229163 |
| m_edge                |            486 |           546 |          0.89011  | -0.498633   | 0.0956259 | 0.0834048 | 0.531594 | 0.216655 |
| missingness_pressure  |            546 |           546 |          1        |  0          | 0         | 0.193325  | 1        | 0.327623 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 271
positive_boundary_margin: 161
insufficient_data: 60
negative_leakage_margin: 54
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.1927999908924105
m_edge: 0.5315944162032659
C_edge_capacity: 0.6923809380260894
F_route_fragmentation: 0.16078652182282346
S_edge_response: 0.6514724323576586
S_power_balance: 0.003574043189490617
S_transport: 0.35372933863900596
density_support: 0.5046056122318159
geometry_stability: 0.9619732751572243
missingness_pressure: 0.0
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.46979999089241076
m_edge: -0.49863346485737403
C_edge_capacity: 0.38420956050588506
F_route_fragmentation: 0.8828430253632591
S_edge_response: 0.5763143407588276
S_power_balance: 0.9802649322341068
S_transport: nan
density_support: 0.0
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.1378 |     0.1418 |      0.004 |           207 |         211 |
|       0.1738 |     0.1788 |      0.005 |           243 |         248 |
|       0.1838 |     0.1978 |      0.014 |           253 |         267 |
|       0.2028 |     0.2078 |      0.005 |           272 |         277 |
|       0.2098 |     0.2148 |      0.005 |           279 |         284 |
|       0.2258 |     0.2328 |      0.007 |           295 |         302 |
|       0.2408 |     0.2458 |      0.005 |           310 |         315 |
|       0.2478 |     0.2528 |      0.005 |           317 |         322 |
|       0.2648 |     0.2678 |      0.003 |           334 |         337 |
|       0.2698 |     0.2728 |      0.003 |           339 |         342 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.3928 |     0.3958 |      0.003 |           462 |         465 |
|       0.4428 |     0.4458 |      0.003 |           512 |         515 |
|       0.4478 |     0.4528 |      0.005 |           517 |         522 |

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