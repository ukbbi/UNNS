# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11768_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     416
time_min: -0.0672000050544738
time_max: 0.3477999949455265
```

State counts:

```text
positive_boundary_margin: 222
negative_leakage_margin: 96
insufficient_data: 58
boundary_ambiguous_margin: 40
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                          |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:--------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| negative_001   | negative_leakage_margin  |  -0.00920001 | 0.0118     |      0.021 |            22 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high                                            |               -0.432277 |                         0.367809 |                              0.919192  |                         0.540293 |                        1         |                              |                              0.555556 |
| peak_negative  | peak_negative_window     |  -0.00120001 | 0.00679999 |      0.008 |             9 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before |               -0.587954 |                         0.157792 |                              0.919192  |                         0.161818 |                        1         |                              |                              0.555556 |
| positive_001   | positive_boundary_margin |   0.0518     | 0.2728     |      0.221 |           222 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                             |                0.430895 |                         0.569283 |                              0.107555  |                         0.310757 |                        0.0539703 |                              |                              0.333333 |
| peak_positive  | peak_positive_window     |   0.0888     | 0.0968     |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                          |                0.588937 |                         0.680636 |                              0.0855033 |                         0.567928 |                        0.03043   |                              |                              0.333333 |
| negative_002   | negative_leakage_margin  |   0.2758     | 0.3478     |      0.072 |            73 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                   |               -0.47371  |                         0.404458 |                              0.880237  |                         0.589831 |                        0.952388  |                              |                              0.555556 |

## 6. Interpretability flags

```text
fragile_negative_candidate: 3
interpretable_positive_candidate: 2
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0092000050544738 → 0.0117999949455261 s
duration: 0.0209999999999999 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high

m_edge: during=-0.43227736121720683 delta_before=0.0011797819434841705 trend=increase
C_edge_capacity: during=0.3678090117392878 delta_before=-0.11792576429194018 trend=decrease
F_route_fragmentation: during=0.9191919191919192 delta_before=-0.08080808080808077 trend=decrease
S_edge_response: during=0.5402934385142839 delta_before=-0.18830872553255817 trend=decrease
S_power_balance: during=1.0 delta_before=0.0 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.058593749992322496 delta_before=0.0634765624923225 trend=increase
softx_lower_proxy: during=1.4305114824417816e-05 delta_before=-4.768371571258065e-06 trend=increase
softx_upper_proxy: during=-8.583068840995791e-05 delta_before=-8.583068839307019e-05 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=8.0645274631091e+17 delta_before=1.4878713667733422e+18 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.5555555555555556 delta_before=-0.4444444444444444 trend=flat
```

### peak_negative — peak_negative_window

```text
time: -0.0012000050544738 → 0.0067999949455261 s
duration: 0.0079999999999999 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.5879544115244626 delta_before=-0.1603187815990182 trend=decrease
C_edge_capacity: during=0.1577915545356174 delta_before=-0.3337647347308573 trend=decrease
F_route_fragmentation: during=0.9191919191919192 delta_before=0.0 trend=decrease
S_edge_response: during=0.1618183311247076 delta_before=-0.5755161027750045 trend=decrease
S_power_balance: during=1.0 delta_before=0.0 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.23681640625 delta_before=0.24169921875 trend=increase
softx_lower_proxy: during=-8.269158469943749e-14 delta_before=-3.814697246815575e-05 trend=increase
softx_upper_proxy: during=-0.0003242492675565 delta_before=-0.0003242492676849049 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.5655880097204795e+18 delta_before=1.1942829330205243e+18 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.5555555555555556 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.0517999949455262 → 0.2727999949455264 s
duration: 0.22100000000000022 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4308951628359574 delta_before=0.3218009169657468 trend=increase
C_edge_capacity: during=0.5692833190860334 delta_before=0.07628000231847626 trend=decrease
F_route_fragmentation: during=0.10755529682323005 delta_before=-0.2798746137981402 trend=decrease
S_edge_response: during=0.31075693875610116 delta_before=-0.18449621218386253 trend=decrease
S_power_balance: during=0.05397029727638615 delta_before=-0.34548107496454794 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.20019531250443506 delta_before=0.06347656250443506 trend=increase
softx_lower_proxy: during=0.0008821487429101 delta_before=4.768372447100009e-06 trend=decrease
softx_upper_proxy: during=0.0004196166975183 delta_before=-0.0002479553224671 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=5.70220957845097e+19 delta_before=2.1077275065628754e+19 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=increase
```

### peak_positive — peak_positive_window

```text
time: 0.0887999949455262 → 0.0967999949455262 s
duration: 0.007999999999999993 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.5889372958580423 delta_before=0.04617483231845809 trend=decrease
C_edge_capacity: during=0.6806356051981364 delta_before=0.06086150029345028 trend=decrease
F_route_fragmentation: during=0.0855032973037693 delta_before=0.009099071818243681 trend=increase
S_edge_response: during=0.5679281953858317 delta_before=-0.04714404727327459 trend=decrease
S_power_balance: during=0.0304299559638662 delta_before=0.01112108777785345 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.1538085937439996 delta_before=0.009765625008329754 trend=increase
softx_lower_proxy: during=0.001792907715263 delta_before=-0.0006580352777451001 trend=decrease
softx_upper_proxy: during=0.0010871887206568 delta_before=-0.00010490417489695007 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=5.660953043446583e+19 delta_before=1.667022355429335e+18 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.2757999949455264 → 0.3477999949455265 s
duration: 0.07200000000000006 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.4737099838226258 delta_before=-0.7722109469497429 trend=decrease
C_edge_capacity: during=0.4044578395501438 delta_before=-0.012654254935643705 trend=increase
F_route_fragmentation: during=0.8802368020339821 delta_before=0.7527964039142431 trend=increase
S_edge_response: during=0.5898306140361264 delta_before=0.40952869650251406 trend=increase
S_power_balance: during=0.9523881901402992 delta_before=0.9089298230064892 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.0048828124862103 delta_before=-0.2246093749483174 trend=decrease
softx_lower_proxy: during=-0.0009918212881094 delta_before=-0.0011157989487058 trend=increase
softx_upper_proxy: during=-0.0008010864263185 delta_before=-0.0005245208751020001 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.0926086738744967e+19 delta_before=-4.50778986618395e+19 trend=decrease
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