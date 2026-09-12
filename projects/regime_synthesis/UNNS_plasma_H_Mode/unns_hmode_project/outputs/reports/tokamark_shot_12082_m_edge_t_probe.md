# TokaMark First m_edge(t) Probe — Shot 12082

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

- shot_id: `12082`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12082.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12082.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `14`
  - `summary_power_nbi`: `KeyError('Missing array metadata: summary/power_nbi/.zarray')`
  - `summary_ip`: `KeyError('Missing array metadata: summary/ip/.zarray')`
  - `interferometer_n_e_line`: `KeyError('Missing array metadata: interferometer/n_e_line/.zarray')`
  - `dalpha_voltage`: `KeyError('Missing array metadata: spectrometer_visible/filter_spectrometer_dalpha_voltage/.zarray')`
  - `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
  - `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`
  - `equilibrium_q95`: `KeyError('Missing array metadata: equilibrium/q95/.zarray')`
  - `equilibrium_elongation`: `KeyError('Missing array metadata: equilibrium/elongation/.zarray')`
  - `equilibrium_triangularity_upper`: `KeyError('Missing array metadata: equilibrium/triangularity_upper/.zarray')`
  - `equilibrium_triangularity_lower`: `KeyError('Missing array metadata: equilibrium/triangularity_lower/.zarray')`
  - `equilibrium_minor_radius`: `KeyError('Missing array metadata: equilibrium/minor_radius/.zarray')`
  - `equilibrium_beta_normal`: `KeyError('Missing array metadata: equilibrium/beta_normal/.zarray')`
  - `equilibrium_beta_pol`: `KeyError('Missing array metadata: equilibrium/beta_pol/.zarray')`
  - `equilibrium_whmd`: `KeyError('Missing array metadata: equilibrium/whmd/.zarray')`

## 4. Time grid

```text
dt:       0.001
count:    254
time_min: -0.06920000910758972
time_max: 0.1837999908924105
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

| quantity              |   finite_count |   total_count |   finite_fraction |          min |     median |       mean |        max |         std |
|:----------------------|---------------:|--------------:|------------------:|-------------:|-----------:|-----------:|-----------:|------------:|
| S_power_balance       |              0 |           254 |          0        | nan          | nan        | nan        | nan        | nan         |
| S_transport           |              0 |           254 |          0        | nan          | nan        | nan        | nan        | nan         |
| S_edge_response       |            193 |           254 |          0.759843 |   0.00285714 |   0.401213 |   0.376425 |   0.88381  |   0.243682  |
| C_edge_capacity       |            193 |           254 |          0.759843 |   0.00285714 |   0.401213 |   0.376425 |   0.88381  |   0.243682  |
| F_route_fragmentation |            254 |           254 |          1        |   0.777778   |   0.777778 |   0.831146 |   1        |   0.0949287 |
| m_edge                |            193 |           254 |          0.759843 |  -0.774921   |  -0.376565 |  -0.401353 |   0.106032 |   0.243682  |
| missingness_pressure  |            254 |           254 |          1        |   0.777778   |   0.777778 |   0.831146 |   1        |   0.0949287 |

## 7. Margin-state counts

```text
negative_leakage_margin: 140
insufficient_data: 61
boundary_ambiguous_margin: 53
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.09279999089241042
m_edge: 0.10603174643556368
C_edge_capacity: 0.8838095242133415
F_route_fragmentation: 0.7777777777777778
S_edge_response: 0.8838095242133415
S_power_balance: nan
S_transport: nan
density_support: nan
geometry_stability: nan
missingness_pressure: 0.7777777777777778
m_edge_state: boundary_ambiguous_margin
```

### Peak negative m_edge

```text
time_s: 0.12179999089241045
m_edge: -0.7749206348516939
C_edge_capacity: 0.002857142926083825
F_route_fragmentation: 0.7777777777777778
S_edge_response: 0.002857142926083825
S_power_balance: nan
S_transport: nan
density_support: nan
geometry_stability: nan
missingness_pressure: 0.7777777777777778
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

_No positive-boundary intervals found under the v0.1 threshold._

## 10. Candidate negative intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|  -0.00920001 |     0.0178 |      0.027 |            60 |          87 |
|   0.0218     |     0.0278 |      0.006 |            91 |          97 |
|   0.0298     |     0.0338 |      0.004 |            99 |         103 |
|   0.0858     |     0.0898 |      0.004 |           155 |         159 |
|   0.1108     |     0.1828 |      0.072 |           180 |         252 |

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