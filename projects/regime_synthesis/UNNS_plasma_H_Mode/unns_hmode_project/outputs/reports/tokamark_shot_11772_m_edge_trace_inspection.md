# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11772_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     479
time_min: -0.0674000084400177
time_max: 0.4105999915599827
```

State counts:

```text
positive_boundary_margin: 315
negative_leakage_margin: 90
insufficient_data: 59
boundary_ambiguous_margin: 15
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                          |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:--------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| negative_001   | negative_leakage_margin  |  -0.00940001 | 0.00659999 |      0.016 |            17 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high                                            |               -0.339175 |                         0.502979 |                              0.842587  |                         0.716858 |                         0.906372 |                              |                              0.555556 |
| peak_negative  | peak_negative_window     |  -0.00140001 | 0.00659999 |      0.008 |             9 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before |               -0.35237  |                         0.205203 |                              0.840276  |                         0.191395 |                         0.903547 |                              |                              0.555556 |
| positive_001   | positive_boundary_margin |   0.0196     | 0.3336     |      0.314 |           315 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                             |                0.40944  |                         0.557844 |                              0.157325  |                         0.321386 |                         0.118212 |                              |                              0.333333 |
| peak_positive  | peak_positive_window     |   0.3006     | 0.3086     |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                             |                0.562752 |                         0.636083 |                              0.0714993 |                         0.488096 |                         0.013314 |                              |                              0.333333 |
| negative_002   | negative_leakage_margin  |   0.3376     | 0.4096     |      0.072 |            73 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                   |               -0.494507 |                         0.40271  |                              0.902719  |                         0.59353  |                         0.979867 |                              |                              0.555556 |

## 6. Interpretability flags

```text
fragile_negative_candidate: 3
interpretable_positive_candidate: 2
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0094000084400176 → 0.0065999915599823 s
duration: 0.0159999999999999 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high

m_edge: during=-0.3391754236394471 delta_before=0.0 trend=increase
C_edge_capacity: during=0.5029793335273052 delta_before=-0.0027361858040991782 trend=decrease
F_route_fragmentation: during=0.8425874027107527 delta_before=-0.15741259728924728 trend=decrease
S_edge_response: during=0.7168581474450529 delta_before=-0.0060430996234596135 trend=decrease
S_power_balance: during=0.90637225763413 delta_before=-0.0028154380956759706 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.0048828125 delta_before=0.0 trend=increase
softx_lower_proxy: during=7.629394529386528e-05 delta_before=9.536743146155692e-05 trend=decrease
softx_upper_proxy: during=5.7220458904449486e-05 delta_before=-0.00011444091799795052 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-1.3770833382080512e+17 delta_before=1.2741764371919667e+17 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.5555555555555556 delta_before=-0.4444444444444444 trend=flat
```

### peak_negative — peak_negative_window

```text
time: -0.0014000084400176 → 0.0065999915599823 s
duration: 0.0079999999999999 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.3523701964462457 delta_before=-0.014496940835819483 trend=increase
C_edge_capacity: during=0.2052031524889128 delta_before=-0.299801807480006 trend=decrease
F_route_fragmentation: during=0.8402756066840731 delta_before=-0.003221041638087896 trend=decrease
S_edge_response: during=0.1913946849314183 delta_before=-0.5286306546569471 trend=decrease
S_power_balance: during=0.903546729157077 delta_before=-0.003077145333784226 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2148437499973911 delta_before=0.2197265624973911 trend=increase
softx_lower_proxy: during=0.0001144409179783 delta_before=7.629394522116044e-05 trend=decrease
softx_upper_proxy: during=-0.0002861022949428 delta_before=-0.0004005432129476 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-9834031998828544.0 delta_before=1.3926166887294566e+17 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.5555555555555556 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.0195999915599823 → 0.3335999915599826 s
duration: 0.3140000000000003 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4094402484711169 delta_before=0.32581774726779966 trend=increase
C_edge_capacity: during=0.5578435006537126 delta_before=0.2491476284980228 trend=increase
F_route_fragmentation: during=0.1573251731445166 delta_before=-0.07223101601179918 trend=increase
S_edge_response: during=0.3213863381631247 delta_before=0.18179670120872007 trend=increase
S_power_balance: during=0.1182122486581128 delta_before=-0.03889963685392758 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.1855468749799863 delta_before=-0.1367187500354805 trend=decrease
softx_lower_proxy: during=0.0004768371585236 delta_before=0.00041007995626641137 trend=increase
softx_upper_proxy: during=0.0005531311050301 delta_before=0.0006866455097695 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=4.4254406234077135e+19 delta_before=1.048300774200705e+19 trend=decrease
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.3333333333333333 delta_before=-0.22222222222222227 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.3005999915599826 → 0.3085999915599826 s
duration: 0.007999999999999952 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.5627517680583941 delta_before=0.0723537125131955 trend=increase
C_edge_capacity: during=0.6360829681277826 delta_before=0.0 trend=decrease
F_route_fragmentation: during=0.0714993207682609 delta_before=-0.07085365303118049 trend=decrease
S_edge_response: during=0.4880961473624228 delta_before=0.04913116041291321 trend=increase
S_power_balance: during=0.0133139846426893 delta_before=-0.08659890926033169 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.11962890625 delta_before=-0.024414062513457596 trend=decrease
softx_lower_proxy: during=0.0005149841304823 delta_before=-1.907348638370001e-05 trend=increase
softx_upper_proxy: during=0.0003433227539062 delta_before=-0.0002288818373043 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=4.2032398787458105e+19 delta_before=-4.893825100161221e+18 trend=decrease
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.3375999915599826 → 0.4095999915599827 s
duration: 0.07200000000000012 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.494507067266964 delta_before=-0.8348094851719301 trend=decrease
C_edge_capacity: during=0.402709707483676 delta_before=-0.2181679903152393 trend=increase
F_route_fragmentation: during=0.9027191651802112 delta_before=0.6645105326082992 trend=increase
S_edge_response: during=0.5935302633526012 delta_before=-0.046176808573420325 trend=increase
S_power_balance: during=0.97986663398569 delta_before=0.7636513233149683 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.0048828125 delta_before=-0.09521484375 trend=decrease
softx_lower_proxy: during=-0.0012397766092701 delta_before=-0.0016784667944666001 trend=decrease
softx_upper_proxy: during=-0.0006484985344675 delta_before=-0.00194549560151 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-3.4638266653548216e+18 delta_before=-3.456039484202261e+19 trend=decrease
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.5555555555555556 delta_before=0.0 trend=flat
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```