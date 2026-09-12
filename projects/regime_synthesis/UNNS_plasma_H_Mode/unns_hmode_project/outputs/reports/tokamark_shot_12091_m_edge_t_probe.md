# TokaMark First m_edge(t) Probe — Shot 12091

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

- shot_id: `12091`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12091.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12091.zarr/.zmetadata`

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
count:    426
time_min: -0.0690000057220459
time_max: 0.3559999942779545
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

| quantity              |   finite_count |   total_count |   finite_fraction |        min |     median |       mean |        max |         std |
|:----------------------|---------------:|--------------:|------------------:|-----------:|-----------:|-----------:|-----------:|------------:|
| S_power_balance       |              0 |           426 |          0        | nan        | nan        | nan        | nan        | nan         |
| S_transport           |              0 |           426 |          0        | nan        | nan        | nan        | nan        | nan         |
| S_edge_response       |            365 |           426 |          0.856808 |   0        |   0.366745 |   0.371271 |   1        |   0.246722  |
| C_edge_capacity       |            365 |           426 |          0.856808 |   0        |   0.366745 |   0.371271 |   1        |   0.246722  |
| F_route_fragmentation |            426 |           426 |          1        |   0.777778 |   0.777778 |   0.809598 |   1        |   0.0778376 |
| m_edge                |            365 |           426 |          0.856808 |  -0.777778 |  -0.411033 |  -0.406507 |   0.222222 |   0.246722  |
| missingness_pressure  |            426 |           426 |          1        |   0.777778 |   0.777778 |   0.809598 |   1        |   0.0778376 |

## 7. Margin-state counts

```text
negative_leakage_margin: 285
boundary_ambiguous_margin: 79
insufficient_data: 61
positive_boundary_margin: 1
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.1499999942779543
m_edge: 0.2222222222222222
C_edge_capacity: 1.0
F_route_fragmentation: 0.7777777777777778
S_edge_response: 1.0
S_power_balance: nan
S_transport: nan
density_support: nan
geometry_stability: nan
missingness_pressure: 0.7777777777777778
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.2839999942779544
m_edge: -0.7777777777777778
C_edge_capacity: 0.0
F_route_fragmentation: 0.7777777777777778
S_edge_response: 0.0
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
|  -0.00900001 |      0.079 |      0.088 |            60 |         148 |
|   0.081      |      0.119 |      0.038 |           150 |         188 |
|   0.193      |      0.196 |      0.003 |           262 |         265 |
|   0.217      |      0.22  |      0.003 |           286 |         289 |
|   0.222      |      0.236 |      0.014 |           291 |         305 |
|   0.238      |      0.247 |      0.009 |           307 |         316 |
|   0.249      |      0.268 |      0.019 |           318 |         337 |
|   0.27       |      0.355 |      0.085 |           339 |         424 |

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