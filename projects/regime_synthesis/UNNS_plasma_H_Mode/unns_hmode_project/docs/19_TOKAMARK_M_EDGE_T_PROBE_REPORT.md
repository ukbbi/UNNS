# TokaMark m_edge(t) Probe Report — Shot 12063

## 1. Purpose

This document reports the first normalized time-resolved UNNS-H Mode edge-admissibility probe computed from a public MAST/TokaMark discharge.

It belongs here:

```text
unns_hmode_project/
  docs/
    19_TOKAMARK_M_EDGE_T_PROBE_REPORT.md
```

It follows:

```text
docs/
  18_TOKAMARK_ONE_SHOT_ARRAY_PROBE_REPORT.md
```

The previous step established that shot `12063` is array-readable and contains the required diagnostic families. This step converts those extracted diagnostics into a first normalized structural margin:

```text
m_edge(t) = C_edge_capacity(t) - F_route_fragmentation(t)
```

This report is a first result note. It does not claim final physical validation of H-mode or positive-corridor status.

---

## 2. Source and run status

Source:

```text
shot_id: 12063
base URL: https://s3.echo.stfc.ac.uk/mast/tokamark/v1
shot store: https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12063.zarr
metadata: https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12063.zarr/.zmetadata
```

Run status:

```text
component: tokamark_m_edge_t_probe.py
loaded labels: 16
failed arrays/time arrays: 0
metadata keys: 211
```

Loaded diagnostic families included:

```text
dalpha_voltage
equilibrium_beta_normal
equilibrium_beta_pol
equilibrium_elongation
equilibrium_minor_radius
equilibrium_q95
equilibrium_triangularity_lower
equilibrium_triangularity_upper
equilibrium_whmd
interferometer_n_e_line
soft_x_lower
soft_x_upper
summary_ip
summary_power_nbi
thomson_n_e
thomson_t_e
```

This confirms that the computation used the same complete diagnostic family established in the one-shot array probe: power/current, density, D-alpha-like edge response, soft-X activity, Thomson Te/ne profiles, and equilibrium geometry.

---

## 3. Time grid

The probe aligned diagnostics onto a common time grid:

```text
dt:       0.001
count:    426
time_min: -0.06800001114606857
time_max: 0.3569999888539318
```

The grid covers approximately:

```text
-0.068 s → 0.357 s
```

with 1 ms spacing.

---

## 4. Formula version

Formula version:

```text
tokamark_m_edge_t_probe_v0.1_normalized
```

The normalized v0.1 construction was:

```text
S_power_balance(t)
  = 0.70 · nbi_pressure
  + 0.30 · density_deviation_pressure

S_transport(t)
  = 0.40 · Te_gradient
  + 0.40 · ne_gradient
  + 0.10 · Te_edge_core_deviation
  + 0.10 · ne_edge_core_deviation

S_edge_response(t)
  = 0.40 · Dalpha_suppression
  + 0.30 · softX_activity
  + 0.30 · profile_sharpening

C_edge_capacity(t)
  = 0.50 · S_edge_response
  + 0.25 · density_support
  + 0.25 · geometry_stability

F_route_fragmentation(t)
  = 0.45 · S_power_balance
  + 0.45 · S_transport
  + 0.10 · missingness_pressure

m_edge(t)
  = C_edge_capacity - F_route_fragmentation
```

All terms are within-shot normalized structural proxies. Absolute physical-unit thresholds were deliberately avoided because TokaMark arrays may be preprocessed or normalized.

---

## 5. Summary statistics

| quantity              |   finite_count |   total_count |   finite_fraction |        min |   median |     mean |      max |      std |
|:----------------------|---------------:|--------------:|------------------:|-----------:|---------:|---------:|---------:|---------:|
| S_power_balance       |            367 |           426 |          0.861502 |  0         | 0.569205 | 0.514674 | 1        | 0.287845 |
| S_transport           |            281 |           426 |          0.659624 |  0         | 0.484131 | 0.436759 | 0.737484 | 0.176334 |
| S_edge_response       |            367 |           426 |          0.861502 |  0         | 0.572315 | 0.478887 | 0.77312  | 0.188107 |
| C_edge_capacity       |            367 |           426 |          0.861502 |  0.0567782 | 0.559422 | 0.525146 | 0.758847 | 0.142406 |
| F_route_fragmentation |            426 |           426 |          1        |  0.0651664 | 0.516301 | 0.543434 | 1        | 0.253914 |
| m_edge                |            367 |           426 |          0.861502 | -0.770609  | 0.087961 | 0.055111 | 0.475695 | 0.245434 |
| missingness_pressure  |            426 |           426 |          1        |  0         | 0.222222 | 0.314293 | 1        | 0.3142   |

The important result is:

```text
m_edge finite fraction: 0.861502
m_edge median:          0.087961
m_edge mean:            0.055111
m_edge min:             -0.770609
m_edge max:             0.475695
```

This shows a boundary-near shot overall, with both positive and negative excursions.

---

## 6. Margin-state distribution

State counts:

```text
boundary_ambiguous_margin: 209
positive_boundary_margin: 110
insufficient_data: 59
negative_leakage_margin: 48
```

As percentages of the 426-point time grid:

```text
boundary_ambiguous_margin: 49.06%
positive_boundary_margin:  25.82%
negative_leakage_margin:   11.27%
insufficient_data:         13.85%
```

The dominant state is boundary-ambiguous, not uniformly positive.

This is important: shot `12063` is not a simple always-positive case under v0.1. It is a boundary-near case with multiple positive-boundary excursions.

---

## 7. Peak positive margin

The strongest positive point is:

```text
time_s: 0.2089999888539316
m_edge: 0.4756954508722634
C_edge_capacity: 0.710963099667329
F_route_fragmentation: 0.2352676487950655
S_edge_response: 0.7509394425293954
S_power_balance: 0.0209250515441744
S_transport: 0.4525092297288106
density_support: 0.6310104139431961
geometry_stability: nan
missingness_pressure: 0.2222222222222222
m_edge_state: positive_boundary_margin
```

Interpretation:

At the peak positive point, the edge-capacity proxy exceeds route-fragmentation pressure. The value is driven by high `S_edge_response` together with low `S_power_balance`, while `S_transport` remains moderate.

This is the most important interval for direct inspection against D-alpha, soft-X, Thomson gradient, power, and density behavior.

---

## 8. Peak negative margin

The strongest negative point is:

```text
time_s: 0.0039999888539314
m_edge: -0.7706091622560678
C_edge_capacity: 0.0567781535380827
F_route_fragmentation: 0.8273873157941506
S_edge_response: 0.0470608029337013
S_power_balance: 0.9124857316496408
S_transport: nan
density_support: 0.0762128547468455
geometry_stability: nan
missingness_pressure: 0.4444444444444444
m_edge_state: negative_leakage_margin
```

Interpretation:

At the peak negative point, route-fragmentation pressure strongly exceeds edge-capacity. The v0.1 diagnostic marks this as a leakage-like or route-stressed state.

---

## 9. Candidate positive intervals

The v0.1 probe detected these positive-boundary intervals:

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.097 |      0.1   |      0.003 |           165 |         168 |
|        0.115 |      0.119 |      0.004 |           183 |         187 |
|        0.148 |      0.151 |      0.003 |           216 |         219 |
|        0.154 |      0.158 |      0.004 |           222 |         226 |
|        0.168 |      0.173 |      0.005 |           236 |         241 |
|        0.226 |      0.229 |      0.003 |           294 |         297 |
|        0.251 |      0.256 |      0.005 |           319 |         324 |

These intervals are short, ranging from 3 ms to 5 ms in the reported list.

The intervals are candidate structural windows, not yet physical transition labels. They should be inspected against the raw diagnostic traces before any physical interpretation is made.

The strongest single positive point occurs near:

```text
time ≈ 0.209 s
m_edge ≈ 0.4756954508722634
```

Although the interval table lists positive windows above the duration threshold, the peak point should also be inspected in the CSV because it may lie in a broader boundary-near region with a local maximum.

---

## 10. Candidate negative intervals

The v0.1 probe detected these negative-leakage intervals:

|   start_time |   end_time |   duration |   start_index |   end_index |
|-------------:|-----------:|-----------:|--------------:|------------:|
|        0.313 |      0.317 |      0.004 |           381 |         385 |
|        0.322 |      0.326 |      0.004 |           390 |         394 |

These later negative intervals occur around:

```text
0.313–0.317 s
0.322–0.326 s
```

They should be inspected as possible post-event route-stress or signal-coverage/normalization effects before any physical claim is made.

---

## 11. What this establishes

This report establishes six things.

### 11.1 A computable public m_edge(t) trace now exists

The project now has a time-resolved UNNS-H Mode margin from a public MAST/TokaMark discharge.

### 11.2 The shot is boundary-near with excursions

The margin is not uniformly positive or uniformly negative. It is mostly boundary-ambiguous, with positive-boundary and negative-leakage intervals.

### 11.3 Positive-boundary intervals are present under v0.1

The model identifies several short positive windows where `C_edge_capacity(t) > F_route_fragmentation(t)` by the positive threshold.

### 11.4 The strongest positive point is interpretable

The peak positive point has high `S_edge_response`, low `S_power_balance`, and moderate `S_transport`, which is consistent with the structural form of a candidate edge-capacity-dominant interval.

### 11.5 The result remains physically unvalidated

The model has not yet identified an L-H transition time or compared the margin against independent confinement labels.

### 11.6 The next step is inspection, not immediate formula revision

The v0.1 output should be inspected against raw traces before modifying weights or definitions.

---

## 12. What this does not establish

This report does not prove that shot `12063` is an H-mode discharge.

It does not establish that the detected positive intervals are L-H transition intervals.

It does not prove a positive-corridor physical classification.

It does not yet compare this shot with a negative MAST shot or a boundary-ambiguous MAST shot.

It does not use explicit radial or flux-coordinate mapping for Thomson profiles.

It does not establish cross-machine generality.

The result should be described as:

> a first normalized structural `m_edge(t)` probe on a public MAST/TokaMark candidate shot.

not as:

> confirmed physical validation of H-mode origin.

---

## 13. Immediate interpretation

The most honest interpretation is:

> Shot `12063` is technically suitable for time-resolved UNNS-H Mode analysis and produces a nontrivial normalized margin trace. The v0.1 `m_edge(t)` trace is mostly boundary-ambiguous, but it contains short positive-boundary windows and later negative-leakage windows. This is a promising structural signal, but it requires trace-level inspection and independent physical anchoring before it can be treated as positive-corridor validation.

This is actually a good result. If the whole shot had been uniformly positive, the result would look suspiciously overfit. The mixture of states suggests the formula is responding to changing diagnostic structure rather than simply labeling the whole discharge as favorable.

---

## 14. Recommended next technical inspection

Before creating another model, inspect the CSV around these windows:

```text
positive candidate windows:
  0.097–0.100 s
  0.115–0.119 s
  0.148–0.151 s
  0.154–0.158 s
  0.168–0.173 s
  0.226–0.229 s
  0.251–0.256 s

peak positive:
  ≈ 0.209 s

negative candidate windows:
  0.313–0.317 s
  0.322–0.326 s
```

For each window, compare:

```text
m_edge
C_edge_capacity
F_route_fragmentation
S_edge_response
S_power_balance
S_transport
dalpha_proxy
softx_lower_proxy
softx_upper_proxy
te_profile_gradient_proxy
ne_profile_gradient_proxy
density_proxy
nbi_proxy
missingness_pressure
```

The purpose is to determine whether positive intervals correspond to recognizable edge-response structure or are artifacts of missingness, interpolation, or normalization.

---

## 15. Recommended next document

The next document should be:

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```

Its purpose should be to inspect the positive and negative intervals directly in the CSV output and decide whether the v0.1 formula has interpretable diagnostic behavior.

Only after that should the formula be adjusted.

---

## 16. Project status update

```text
TCV event-level model:                       complete
TCV full-corpus extension:                   complete
TCV time-resolved positive trace:            missing
TokaMark metadata access:                    complete
TokaMark candidate scan:                     complete
TokaMark shot 12063 array extraction:        complete
TokaMark shot 12063 first m_edge(t):         complete
physical positive-corridor validation:       not yet
trace-level diagnostic inspection:           next
cross-shot MAST comparison:                  later
```

---

## 17. Final synthesis statement

The first public MAST/TokaMark `m_edge(t)` probe succeeded.

Shot `12063` now has a computable normalized time-resolved UNNS-H Mode margin. The trace is primarily boundary-ambiguous but contains multiple short positive-boundary intervals and later negative-leakage intervals. The strongest positive point occurs near 0.209 s, where edge-capacity exceeds route-fragmentation under the v0.1 formula.

This is a meaningful transition from source acquisition to time-resolved structural modeling.

The result is promising, but still bounded: it is not yet physical validation of H-mode or the positive corridor. The next step is trace-level inspection of the detected intervals against raw diagnostic proxies.
