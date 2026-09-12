# TokaMark First m_edge(t) Probe — Shot 12069

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

- shot_id: `12069`
- source: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12069.zarr`
- metadata: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12069.zarr/.zmetadata`

## 3. Load status

- failed arrays/time arrays: `0`

## 4. Time grid

```text
dt:       0.001
count:    336
time_min: -0.028400011360645294
time_max: 0.306599988639355
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

| quantity              |   finite_count |   total_count |   finite_fraction |        min |   median |     mean |      max |      std |
|:----------------------|---------------:|--------------:|------------------:|-----------:|---------:|---------:|---------:|---------:|
| S_power_balance       |            317 |           336 |          0.943452 |  0         | 0.484644 | 0.424641 | 1        | 0.269437 |
| S_transport           |            235 |           336 |          0.699405 |  0.0206745 | 0.244491 | 0.269113 | 0.572178 | 0.11139  |
| S_edge_response       |            317 |           336 |          0.943452 |  0.07846   | 0.533247 | 0.503625 | 0.778418 | 0.132275 |
| C_edge_capacity       |            317 |           336 |          0.943452 |  0.235827  | 0.535601 | 0.528935 | 0.792047 | 0.12448  |
| F_route_fragmentation |            336 |           336 |          1        |  0.0542591 | 0.370497 | 0.402654 | 1        | 0.224249 |
| m_edge                |            317 |           336 |          0.943452 | -0.471379  | 0.189151 | 0.162084 | 0.595647 | 0.24571  |
| missingness_pressure  |            336 |           336 |          1        |  0         | 0.222222 | 0.303902 | 1        | 0.207996 |

## 7. Margin-state counts

```text
positive_boundary_margin: 151
boundary_ambiguous_margin: 122
negative_leakage_margin: 44
insufficient_data: 19
```

## 8. Peak margin points

### Peak positive m_edge

```text
time_s: 0.21659998863935492
m_edge: 0.5956467858177973
C_edge_capacity: 0.7382011202335875
F_route_fragmentation: 0.14255433441579024
S_edge_response: 0.6738683547905987
S_power_balance: 0.07158820590061746
S_transport: 0.19581648786286698
density_support: 0.866866651119565
geometry_stability: nan
missingness_pressure: 0.2222222222222222
m_edge_state: positive_boundary_margin
```

### Peak negative m_edge

```text
time_s: 0.26359998863935497
m_edge: -0.4713792435933392
C_edge_capacity: 0.37048411071443416
F_route_fragmentation: 0.8418633543077734
S_edge_response: 0.47950004822995174
S_power_balance: 0.9301786676107353
S_transport: nan
density_support: 0.15245223568339908
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

## 9. Candidate positive intervals

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|       0.0756 |     0.0816 |      0.006 |           104 |         110 |
|       0.0966 |     0.1056 |      0.009 |           125 |         134 |
|       0.1156 |     0.1196 |      0.004 |           144 |         148 |
|       0.1396 |     0.1506 |      0.011 |           168 |         179 |
|       0.1526 |     0.1626 |      0.01  |           181 |         191 |
|       0.1646 |     0.2116 |      0.047 |           193 |         240 |
|       0.2136 |     0.2306 |      0.017 |           242 |         259 |
|       0.2356 |     0.2416 |      0.006 |           264 |         270 |
|       0.2456 |     0.2496 |      0.004 |           274 |         278 |

## 10. Candidate negative intervals

|   start_time |    end_time |   duration |   start_index |   end_index |
|-------------:|------------:|-----------:|--------------:|------------:|
|  -0.00540001 | -0.00240001 |      0.003 |            23 |          26 |
|   0.2576     |  0.2606     |      0.003 |           286 |         289 |
|   0.2836     |  0.2866     |      0.003 |           312 |         315 |

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