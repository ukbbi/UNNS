# TokaMark m_edge(t) Trace Inspection — Shot 12063

## 1. Purpose

This document records the project-level synthesis of the trace-level inspection of the first public MAST/TokaMark `m_edge(t)` probe.

It belongs here:

```text
unns_hmode_project/
  docs/
    20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```

It follows:

```text
docs/
  19_TOKAMARK_M_EDGE_T_PROBE_REPORT.md
```

The previous document established that shot `12063` has a computable normalized `m_edge(t)` trace. This document answers the next question:

> Are the detected positive and negative `m_edge(t)` intervals internally interpretable when checked against the diagnostic proxies?

The answer is yes, within the limits of the v0.1 normalized probe.

---

## 2. Core synthesis

The trace inspection confirms that the first public MAST/TokaMark `m_edge(t)` probe is internally interpretable.

The inspector found:

```text
interpretable_positive_candidate: 8
interpretable_negative_candidate: 3
```

This means the positive and negative windows were not simply accepted because the margin crossed a threshold. They were checked against the internal component structure of the margin:

```text
C_edge_capacity(t)
F_route_fragmentation(t)
S_edge_response(t)
S_power_balance(t)
S_transport(t)
missingness_pressure(t)
raw diagnostic proxies
```

The positive windows generally satisfy:

```text
C_edge_capacity > F_route_fragmentation
low or reduced S_power_balance
often elevated S_edge_response
m_edge higher than before
missingness not dominant
```

The negative windows generally satisfy:

```text
F_route_fragmentation > C_edge_capacity
high S_power_balance
m_edge lower than before
```

Therefore, the v0.1 `m_edge(t)` trace should be carried into cross-shot comparison rather than revised immediately.

---

## 3. Input and settings

The inspection used:

```text
outputs/reports/tokamark_shot_12063_m_edge_t_probe.csv
```

The inspector component was:

```text
components/
  tokamark_m_edge_trace_inspector.py
```

Inspection settings:

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
peak half-width: 0.004 s
```

The trace covered:

```text
rows:     426
time_min: -0.0680000111460685
time_max: 0.3569999888539318
```

---

## 4. Global state distribution

The original `m_edge(t)` state distribution was:

```text
boundary_ambiguous_margin: 209
positive_boundary_margin:  110
negative_leakage_margin:   48
insufficient_data:         59
```

As percentages of the full grid:

```text
boundary_ambiguous_margin: 49.06%
positive_boundary_margin:  25.82%
negative_leakage_margin:   11.27%
insufficient_data:         13.85%
```

This is important because shot `12063` is not uniformly positive. It is structurally mixed:

```text
mostly boundary-ambiguous
with several positive-boundary excursions
and later negative-leakage intervals
```

That mixed behavior is preferable to a trivial always-positive result, because it suggests the margin is responding to changing diagnostic structure rather than simply labeling the whole discharge as favorable.

---

## 5. Main m_edge(t) statistics

The global margin statistics were:

```text
m_edge finite fraction: 0.861502
m_edge median:          0.087961
m_edge mean:            0.055111
m_edge min:             -0.770609
m_edge max:             0.475695
m_edge std:             0.245434
```

The structural component statistics were:

```text
C_edge_capacity median:       0.559422
F_route_fragmentation median: 0.516301
S_edge_response median:       0.572315
S_power_balance median:       0.569205
S_transport median:           0.484131
missingness_pressure median:  0.222222
```

This confirms the earlier interpretation: the shot is boundary-near overall, not cleanly separated into one regime.

---

## 6. Inspected windows

The inspector identified 11 windows:

```text
window_count: 11
```

Detailed inspection table:

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                            |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:----------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| peak_negative  | peak_negative_window     | -1.11461e-08 | 0.00799999 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before                             |               -0.353819 |                         0.212636 |                               0.546474 |                         0.17363  |                        0.817648  |                     0.363595 |                              0.444444 |
| positive_001   | positive_boundary_margin |  0.097       | 0.1        |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before                    |                0.250337 |                         0.63988  |                               0.383785 |                         0.372179 |                        0.276923  |                     0.580207 |                              0        |
| positive_002   | positive_boundary_margin |  0.115       | 0.119      |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before |                0.327917 |                         0.649378 |                               0.324168 |                         0.657676 |                        0.104338  |                     0.612101 |                              0        |
| positive_003   | positive_boundary_margin |  0.148       | 0.151      |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                            |                0.305896 |                         0.693833 |                               0.383724 |                         0.628243 |                        0.319432  |                     0.488398 |                              0.222222 |
| positive_004   | positive_boundary_margin |  0.154       | 0.158      |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                            |                0.293961 |                         0.69252  |                               0.399742 |                         0.61817  |                        0.32686   |                     0.512073 |                              0.222222 |
| positive_005   | positive_boundary_margin |  0.168       | 0.173      |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                            |                0.3587   |                         0.643511 |                               0.282544 |                         0.58263  |                        0.0294515 |                     0.54488  |                              0.222222 |
| peak_positive  | peak_positive_window     |  0.205       | 0.213      |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high                                                                                 |                0.185417 |                         0.706302 |                               0.520884 |                         0.750939 |                        0.669381  |                     0.461112 |                              0.222222 |
| positive_006   | positive_boundary_margin |  0.226       | 0.229      |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                            |                0.324377 |                         0.553458 |                               0.226864 |                         0.562636 |                        0.19931   |                     0.254105 |                              0.222222 |
| positive_007   | positive_boundary_margin |  0.251       | 0.256      |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                               |                0.317629 |                         0.564742 |                               0.232088 |                         0.534338 |                        0.157848  |                     0.345388 |                              0.222222 |
| negative_001   | negative_leakage_margin  |  0.313       | 0.317      |      0.004 |             5 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                                               |               -0.468495 |                         0.388034 |                               0.854965 |                         0.575412 |                        0.946192  |                   nan        |                              0.444444 |
| negative_002   | negative_leakage_margin  |  0.322       | 0.326      |      0.004 |             5 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                                               |               -0.454731 |                         0.396612 |                               0.846724 |                         0.580922 |                        0.936119  |                   nan        |                              0.444444 |

The compact interpretation is:

```text
positive interpretable windows: 8
negative interpretable windows: 3
```

Positive candidate windows:

```text
0.097–0.100 s
0.115–0.119 s
0.148–0.151 s
0.154–0.158 s
0.168–0.173 s
0.226–0.229 s
0.251–0.256 s
```

Negative candidate windows:

```text
0.313–0.317 s
0.322–0.326 s
```

---

## 7. Peak positive window

The peak positive inspection window was:

```text
start_time: 0.2049999888539316
end_time: 0.2129999888539316
duration: 0.008000000000000007
interpretability_flag: interpretable_positive_candidate
interpretability_notes: capacity_exceeds_fragmentation;edge_response_high
m_edge__during_median: 0.1854174563045642
C_edge_capacity__during_median: 0.706301588490346
F_route_fragmentation__during_median: 0.5208841321857818
S_edge_response__during_median: 0.7509394425293954
S_power_balance__during_median: 0.6693811355724233
S_transport__during_median: 0.461111797401767
missingness_pressure__during_median: 0.2222222222222222
```

Interpretation:

The peak positive window is interpretable because edge capacity exceeds route fragmentation and edge-response evidence is high. It is not the cleanest low-power positive window, but it is the strongest local edge-capacity point under the v0.1 formula.

The important point is that this window is not accepted merely because `m_edge` is positive. It is accepted because the internal components remain consistent:

```text
capacity_exceeds_fragmentation
edge_response_high
```

This makes the peak positive window a candidate interval for deeper inspection in a later physical trace plot or common-timebase visualization.

---

## 8. Peak negative window

The peak negative inspection window was:

```text
start_time: -1.1146068512601914e-08
end_time: 0.0079999888539314
duration: 0.007999999999999913
interpretability_flag: interpretable_negative_candidate
interpretability_notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before
m_edge__during_median: -0.3538189464014549
C_edge_capacity__during_median: 0.2126359150200278
F_route_fragmentation__during_median: 0.5464740681363519
S_edge_response__during_median: 0.1736299422562544
S_power_balance__during_median: 0.8176482505738526
S_transport__during_median: 0.36359455438167704
missingness_pressure__during_median: 0.4444444444444444
```

Interpretation:

The peak negative window is interpretable because route fragmentation exceeds capacity, power-balance pressure is high, edge response is low, and `m_edge` is lower than before.

This provides an internal control: the v0.1 margin is not merely producing positive excursions. It also identifies coherent negative or route-stressed windows.

---

## 9. Positive-window interpretation

The positive windows are not identical, but they share a structural pattern.

Most positive windows show:

```text
C_edge_capacity > F_route_fragmentation
S_power_balance low or reduced
S_edge_response elevated in several windows
missingness_pressure = 0 or 0.222...
m_edge higher than before
```

The strongest clean positive intervals are especially valuable:

```text
positive_002: 0.115–0.119 s
positive_003: 0.148–0.151 s
positive_004: 0.154–0.158 s
positive_005: 0.168–0.173 s
positive_006: 0.226–0.229 s
```

These windows combine capacity dominance with either elevated edge response, low power-balance pressure, or both.

This supports the working UNNS-H Mode interpretation:

> a positive edge corridor is not merely a high-power state; it is a state where edge-capacity structure exceeds route-fragmentation pressure.

---

## 10. Negative-window interpretation

The negative windows appear later:

```text
negative_001: 0.313–0.317 s
negative_002: 0.322–0.326 s
```

They are interpretable because they show:

```text
F_route_fragmentation > C_edge_capacity
S_power_balance high
m_edge lower than before
```

However, they also have higher missingness pressure and absent Thomson transport values in the inspected table. Therefore, they should be treated as interpretable but less complete than the best positive windows.

This matters for the next stage: negative windows are useful as internal contrast, but cross-shot comparison will need a better weak/negative TokaMark candidate rather than relying only on late-time windows inside shot `12063`.

---

## 11. What this establishes

This inspection establishes five things.

### 11.1 The v0.1 trace has internal diagnostic structure

The positive and negative windows are not arbitrary threshold crossings. They satisfy component-level consistency checks.

### 11.2 Positive windows are coherent enough for cross-shot testing

The positive windows generally show capacity dominance and acceptable missingness. This justifies using v0.1 in a cross-shot comparison.

### 11.3 Negative windows provide an internal contrast

The same trace also contains route-stressed windows where fragmentation dominates capacity.

### 11.4 Missingness does not dominate the positive result

Most positive windows have missingness pressure of `0` or `0.222...`, not high missingness. This supports the claim that positive intervals are not merely missing-data artifacts.

### 11.5 The formula should not be revised immediately

The correct next move is cross-shot comparison, because a formula that passes internal trace inspection must now be tested against another shot.

---

## 12. What this does not establish

This inspection still does not prove that shot `12063` is physically H-mode.

It does not identify the true L-H transition time.

It does not prove that the positive windows are actual L-H transition windows.

It does not validate the positive corridor physically.

It does not establish cross-machine generality.

It does not yet compare this shot against a weaker or negative TokaMark shot.

The correct bounded claim is:

> The first public MAST/TokaMark `m_edge(t)` trace is internally interpretable and ready for cross-shot comparison.

not:

> The positive corridor is validated.

---

## 13. Decision

The decision after this inspection is:

```text
Do not revise the v0.1 formula yet.
Do not claim physical validation yet.
Proceed to cross-shot comparison.
```

The reason is simple:

```text
The trace passed internal interpretability checks.
The next falsification test is whether another shot behaves differently.
```

If a weaker or negative candidate produces the same positive-window pattern, v0.1 is overbroad and must be revised.

If a weaker or negative candidate lacks these coherent positive windows, then shot `12063` becomes more meaningful as a candidate positive-corridor trace.

---

## 14. Recommended next technical step

The next technical move is to select a weaker or negative TokaMark candidate and run the same pipeline.

The sequence should be:

```text
1. Use the metadata candidate scan results to choose a lower-ranked or incomplete candidate.
2. Run tokamark_one_shot_array_probe.py on that shot.
3. Run tokamark_m_edge_t_probe.py on that shot.
4. Run tokamark_m_edge_trace_inspector.py on that shot.
5. Compare against shot 12063.
```

The next component should therefore be a comparator, not a new formula:

```text
components/
  tokamark_cross_shot_m_edge_comparator.py
```

The comparator should compare:

```text
state distribution
positive-window count
negative-window count
m_edge median / max / min
interpretable-positive count
interpretable-negative count
missingness pressure
edge-response dominance
power-balance pressure
transport availability
```

---

## 15. Recommended next document

After the cross-shot comparator is run, the next document should be:

```text
docs/
  21_TOKAMARK_CROSS_SHOT_M_EDGE_COMPARISON.md
```

Its purpose should be:

> Determine whether shot `12063` is structurally special relative to a weaker or negative TokaMark candidate.

---

## 16. Project status update

```text
TCV event-level model:                        complete
TCV full-corpus extension:                    complete
TCV time-resolved positive trace:             missing in TCV
TokaMark metadata access:                     complete
TokaMark candidate scan:                      complete
TokaMark shot 12063 array extraction:         complete
TokaMark shot 12063 first m_edge(t):          complete
TokaMark shot 12063 trace inspection:         complete
internal interpretability of v0.1:            supported
physical positive-corridor validation:        not yet
cross-shot TokaMark comparison:               next
```

---

## 17. Final synthesis statement

The trace-level inspection confirms that the first public MAST/TokaMark `m_edge(t)` probe has internally interpretable structure.

For shot `12063`, the v0.1 normalized margin is mostly boundary-ambiguous, but it contains eight interpretable positive-candidate windows and three interpretable negative-candidate windows. The positive windows generally show edge-capacity dominance over route-fragmentation pressure, while the negative windows show fragmentation dominance with high power-balance pressure.

This result supports carrying the v0.1 margin into cross-shot comparison. It does not yet validate H-mode, identify an L-H transition, or prove the positive corridor physically.

The next decisive test is whether a weaker or negative TokaMark candidate fails to reproduce the same coherent positive-window pattern.
