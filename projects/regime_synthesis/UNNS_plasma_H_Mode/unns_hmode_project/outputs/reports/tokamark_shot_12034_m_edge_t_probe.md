# TokaMark First m_edge(t) Probe — Shot 12034

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

- shot_id: `12034`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12034.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12034.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `2`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    604
time_min: -0.057200007140636444
time_max: 0.5457999928593641
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

| quantity              |   finite_count |   total_count |   finite_fraction |           min |     median |       mean |        max |        std |
|:----------------------|---------------:|--------------:|------------------:|--------------:|-----------:|-----------:|-----------:|-----------:|
| S_power_balance       |            555 |           604 |          0.918874 |   5.90199e-06 |   0.22973  |   0.358559 |   0.788384 |   0.27433  |
| S_transport           |              0 |           604 |          0        | nan           | nan        | nan        | nan        | nan        |
| S_edge_response       |            555 |           604 |          0.918874 |   0.00310255  |   0.480364 |   0.451863 |   0.700287 |   0.167384 |
| C_edge_capacity       |            555 |           604 |          0.918874 |   0.0421031   |   0.577598 |   0.519618 |   0.717937 |   0.142296 |
| F_route_fragmentation |            604 |           604 |          1        |   0.0808172   |   0.247261 |   0.397987 |   1        |   0.272024 |
| m_edge                |            555 |           604 |          0.918874 |  -0.292441    |   0.110632 |   0.174782 |   0.575046 |   0.232877 |
| missingness_pressure  |            604 |           604 |          1        |   0.222222    |   0.222222 |   0.341244 |   1        |   0.226411 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 287
positive_boundary_margin: 227
insufficient_data: 49
negative_leakage_margin: 41
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.28679999285936386
m_edge: 0.5750455213606706
C_edge_capacity: 0.6960862586304077
F_route_fragmentation: 0.12104073726973719
S_edge_response: 0.6006346149958494
S_power_balance: 0.09855596283585163
S_transport: nan
density_support: 0.7016054115623966
geometry_stability: 0.8814703929675355
missingness_pressure: 0.2222222222222222
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.0987999928593637
m_edge: -0.292441322840642
C_edge_capacity: 0.3660215094474743
F_route_fragmentation: 0.6584628322881163
S_edge_response: 0.4475592450110732
S_power_balance: 0.7554051900805373
S_transport: nan
density_support: 0.08629013434401529
geometry_stability: 0.4826774134237355
missingness_pressure: 0.2222222222222222
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.2868 |     0.4488 |      0.162 |           344 |         506 |
|       0.4818 |     0.5448 |      0.063 |           539 |         602 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.0978 |     0.1018 |      0.004 |           155 |         159 |
|       0.1198 |     0.1518 |      0.032 |           177 |         209 |

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