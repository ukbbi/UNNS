# TokaMark First m_edge(t) Probe — Shot 12076

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

- shot_id: `12076`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12076.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12076.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `0`

## 4. Time grid

```text
dt:       0.001
count:    371
time_min: -0.0690000057220459
time_max: 0.30099999427795443
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

| quantity              |   finite_count |   total_count |   finite_fraction |        min |    median |      mean |      max |      std |
|:----------------------|---------------:|--------------:|------------------:|-----------:|----------:|----------:|---------:|---------:|
| S_power_balance       |            311 |           371 |          0.838275 |  0         | 0.489578  | 0.479127  | 1        | 0.288155 |
| S_transport           |            216 |           371 |          0.58221  |  0         | 0.464197  | 0.457324  | 0.793222 | 0.178093 |
| S_edge_response       |            311 |           371 |          0.838275 |  0.0061665 | 0.502698  | 0.437215  | 0.754447 | 0.171901 |
| C_edge_capacity       |            311 |           371 |          0.838275 |  0.0553804 | 0.442436  | 0.485897  | 0.826188 | 0.159256 |
| F_route_fragmentation |            371 |           371 |          1        |  0.0598608 | 0.494003  | 0.548926  | 1        | 0.266023 |
| m_edge                |            311 |           371 |          0.838275 | -0.776094  | 0.0795471 | 0.0239952 | 0.517955 | 0.248034 |
| missingness_pressure  |            371 |           371 |          1        |  0         | 0.222222  | 0.371369  | 1        | 0.309335 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 189
positive_boundary_margin: 72
insufficient_data: 60
negative_leakage_margin: 50
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.19699999427795434
m_edge: 0.5179550307500518
C_edge_capacity: 0.7204234464788609
F_route_fragmentation: 0.20246841572880914
S_edge_response: 0.6292703574199214
S_power_balance: 0.10802623243685952
S_transport: 0.29252086424444473
density_support: 0.9027296245967401
geometry_stability: nan
missingness_pressure: 0.2222222222222222
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.23099999427795437
m_edge: -0.7760944827751256
C_edge_capacity: 0.05716781284661807
F_route_fragmentation: 0.8332622956217437
S_edge_response: 0.006166495376462871
S_power_balance: 0.9196662625500324
S_transport: nan
density_support: 0.1591704477869285
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.193 |      0.205 |      0.012 |           262 |         274 |
|        0.207 |      0.214 |      0.007 |           276 |         283 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.23  |      0.233 |      0.003 |           299 |         302 |
|        0.243 |      0.249 |      0.006 |           312 |         318 |

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