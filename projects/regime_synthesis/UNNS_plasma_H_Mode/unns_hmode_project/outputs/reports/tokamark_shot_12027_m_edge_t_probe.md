# TokaMark First m_edge(t) Probe — Shot 12027

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

- shot_id: `12027`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12027.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12027.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `3`
  - `interferometer_n_e_line`: `KeyError('Missing array metadata: interferometer/n_e_line/.zarray')`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    463
time_min: -0.057200007140636444
time_max: 0.40479999285936397
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
| S_power_balance       |            415 |           463 |          0.896328 |   0           |   0.864252 |   0.573623 |   1        |   0.452937 |
| S_transport           |              0 |           463 |          0        | nan           | nan        | nan        | nan        | nan        |
| S_edge_response       |            415 |           463 |          0.896328 |   0.000261723 |   0.341998 |   0.348244 |   0.605156 |   0.145625 |
| C_edge_capacity       |            415 |           463 |          0.896328 |   0.000261723 |   0.467894 |   0.43623  |   0.615123 |   0.13587  |
| F_route_fragmentation |            463 |           463 |          1        |   0.0606061   |   0.837592 |   0.589575 |   1        |   0.369644 |
| m_edge                |            415 |           463 |          0.896328 |  -0.891011    |  -0.284308 |  -0.105874 |   0.503668 |   0.356415 |
| missingness_pressure  |            463 |           463 |          1        |   0.333333    |   0.333333 |   0.462443 |   1        |   0.206735 |

## 7. Margin-state counts

```text
negative_leakage_margin: 243
positive_boundary_margin: 128
insufficient_data: 48
boundary_ambiguous_margin: 44
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: -0.009200007140636401
m_edge: 0.5036683987407522
C_edge_capacity: 0.6051561850253322
F_route_fragmentation: 0.10148778628457994
S_edge_response: 0.6051561850253322
S_power_balance: 0.0005838375576964698
S_transport: nan
density_support: nan
geometry_stability: nan
missingness_pressure: 0.5555555555555556
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.3327999928593639
m_edge: -0.8910106456944579
C_edge_capacity: 0.002093784078279721
F_route_fragmentation: 0.8931044297727376
S_edge_response: 0.002093784078279721
S_power_balance: 0.9681152907098892
S_transport: nan
density_support: nan
geometry_stability: nan
missingness_pressure: 0.5555555555555556
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|  -0.00920001 | 0.00279999 |      0.012 |            48 |          60 |
|   0.0298     | 0.0348     |      0.005 |            87 |          92 |
|   0.0368     | 0.0428     |      0.006 |            94 |         100 |
|   0.0448     | 0.0908     |      0.046 |           102 |         148 |
|   0.3528     | 0.4048     |      0.052 |           410 |         462 |

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.0978 |     0.1078 |      0.01  |           155 |         165 |
|       0.1168 |     0.3478 |      0.231 |           174 |         405 |

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