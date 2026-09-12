# TokaMark First m_edge(t) Probe — Shot 11851

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

- shot_id: `11851`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11851.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11851.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `2`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    415
time_min: -0.06800001114606857
time_max: 0.3459999888539318
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
| S_power_balance       |            356 |           415 |          0.857831 |   0          |   0.606758  |   0.576362  |   0.995827 |   0.21911  |
| S_transport           |              0 |           415 |          0        | nan          | nan         | nan         | nan        | nan        |
| S_edge_response       |            356 |           415 |          0.857831 |   0.00213484 |   0.469177  |   0.41418   |   0.731585 |   0.172243 |
| C_edge_capacity       |            356 |           415 |          0.857831 |   0.0436167  |   0.424849  |   0.477501  |   0.738837 |   0.147237 |
| F_route_fragmentation |            415 |           415 |          1        |   0.040404   |   0.578743  |   0.593038  |   1        |   0.238888 |
| m_edge                |            356 |           415 |          0.857831 |  -0.758351   |  -0.0470812 |  -0.0480915 |   0.643923 |   0.258249 |
| missingness_pressure  |            415 |           415 |          1        |   0.222222   |   0.222222  |   0.397055  |   1        |   0.264038 |

## 7. Margin-state counts

```text
boundary_ambiguous_margin: 173
negative_leakage_margin: 118
positive_boundary_margin: 65
insufficient_data: 59
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.20499998885393167
m_edge: 0.6439225409868778
C_edge_capacity: 0.699923000708458
F_route_fragmentation: 0.056000459721580235
S_edge_response: 0.670364748068945
S_power_balance: 0.01906229027699313
S_transport: nan
density_support: 0.6526724159152664
geometry_stability: 0.806290090780676
missingness_pressure: 0.2222222222222222
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.00299998885393149
m_edge: -0.758351325041007
C_edge_capacity: 0.043616664469101375
F_route_fragmentation: 0.8019679895101084
S_edge_response: 0.04047384620869571
S_power_balance: 0.8814176661913671
S_transport: nan
density_support: 0.04990230098991271
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.188 |      0.194 |      0.006 |           256 |         262 |
|        0.203 |      0.212 |      0.009 |           271 |         280 |
|        0.214 |      0.218 |      0.004 |           282 |         286 |
|        0.256 |      0.259 |      0.003 |           324 |         327 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|   0.00499999 | 0.00799999 |      0.003 |            73 |          76 |
|   0.013      | 0.02       |      0.007 |            81 |          88 |
|   0.041      | 0.044      |      0.003 |           109 |         112 |
|   0.08       | 0.083      |      0.003 |           148 |         151 |
|   0.097      | 0.103      |      0.006 |           165 |         171 |
|   0.271      | 0.276      |      0.005 |           339 |         344 |
|   0.28       | 0.289      |      0.009 |           348 |         357 |
|   0.291      | 0.3        |      0.009 |           359 |         368 |
|   0.302      | 0.32       |      0.018 |           370 |         388 |
|   0.326      | 0.33       |      0.004 |           394 |         398 |

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