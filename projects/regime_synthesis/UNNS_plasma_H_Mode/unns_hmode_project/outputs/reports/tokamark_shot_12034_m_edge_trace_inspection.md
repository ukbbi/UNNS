# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12034_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     604
time_min: -0.0572000071406364
time_max: 0.5457999928593641
```

State counts:

```text
boundary_ambiguous_margin: 287
positive_boundary_margin: 227
insufficient_data: 49
negative_leakage_margin: 41
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                           |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| peak_negative  | peak_negative_window     |       0.0958 |     0.1028 |      0.007 |             8 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                                              |               -0.218133 |                         0.369162 |                               0.598666 |                         0.450878 |                        0.68232   |                              |                              0.222222 |
| negative_001   | negative_leakage_margin  |       0.0978 |     0.1018 |      0.004 |             5 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                                              |               -0.24662  |                         0.369664 |                               0.616284 |                         0.451134 |                        0.703854  |                              |                              0.222222 |
| negative_002   | negative_leakage_margin  |       0.1198 |     0.1518 |      0.032 |            33 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                                              |               -0.224963 |                         0.405444 |                               0.639592 |                         0.46721  |                        0.732341  |                              |                              0.222222 |
| peak_positive  | peak_positive_window     |       0.2828 |     0.2908 |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                           |                0.545064 |                         0.677612 |                               0.126157 |                         0.570861 |                        0.104809  |                              |                              0.222222 |
| positive_001   | positive_boundary_margin |       0.2868 |     0.4488 |      0.162 |           163 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                              |                0.397014 |                         0.607717 |                               0.213974 |                         0.303537 |                        0.212141  |                              |                              0.222222 |
| positive_002   | positive_boundary_margin |       0.4818 |     0.5448 |      0.063 |            64 | fragile_positive_candidate       | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.476073 |                         0.577104 |                               0.10103  |                         0.577104 |                        2.465e-05 |                              |                              0.555556 |

## 6. Interpretability flags

```text
interpretable_negative_candidate: 3
interpretable_positive_candidate: 2
fragile_positive_candidate: 1
```

## 7. Detailed window notes

### peak_negative — peak_negative_window

```text
time: 0.0957999928593636 → 0.1027999928593637 s
duration: 0.007000000000000103 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.21813342927643076 delta_before=-0.3757569853898338 trend=decrease
C_edge_capacity: during=0.36916225831383376 delta_before=0.022340059386470656 trend=increase
F_route_fragmentation: during=0.5986659307132769 delta_before=0.4123516014674453 trend=increase
S_edge_response: during=0.45087793844703283 delta_before=-0.00431625108565975 trend=decrease
S_power_balance: during=0.6823200881557336 delta_before=0.5039852906824333 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.30883789062462386 delta_before=0.01586914062539635 trend=increase
softx_lower_proxy: during=0.0006103515625377001 delta_before=0.00011444091770510011 trend=increase
softx_upper_proxy: during=0.00025272369382455 delta_before=0.000195503234840175 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=4.66585257916047e+19 delta_before=4.9927723505680384e+17 trend=increase
nbi_proxy: during=1285365.4375 delta_before=1258964.44921875 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### negative_001 — negative_leakage_margin

```text
time: 0.0977999928593637 → 0.1017999928593637 s
duration: 0.0040000000000000036 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.2466199587554083 delta_before=-0.29119740171862396 trend=increase
C_edge_capacity: during=0.36966445699198 delta_before=0.009992150134152389 trend=increase
F_route_fragmentation: during=0.6162844157473883 delta_before=0.3024504331570907 trend=decrease
S_edge_response: during=0.451133600307195 delta_before=-0.0045030479221265796 trend=decrease
S_power_balance: during=0.7038537920863143 delta_before=0.3696616405253331 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3100585937508063 delta_before=0.017089843753047507 trend=increase
softx_lower_proxy: during=0.0006675720214536 delta_before=0.0001716613767442 trend=increase
softx_upper_proxy: during=0.0002098083496093 delta_before=9.059906008083282e-05 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=4.626760762648848e+19 delta_before=-1.2142346710181478e+17 trend=increase
nbi_proxy: during=1332747.25 delta_before=909100.265625 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.1197999928593637 → 0.1517999928593637 s
duration: 0.032000000000000015 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.2249627376147974 delta_before=-0.09247311446718501 trend=increase
C_edge_capacity: during=0.405443952393443 delta_before=0.022894277543729913 trend=increase
F_route_fragmentation: during=0.639592334174287 delta_before=0.1287070982419789 trend=increase
S_edge_response: during=0.4672095159030484 delta_before=0.03905796529400146 trend=increase
S_power_balance: during=0.7323412479414125 delta_before=0.15730867562908524 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3344726562521142 delta_before=-0.014648437502324196 trend=decrease
softx_lower_proxy: during=0.0014305114745549 delta_before=0.0006294250487406 trend=increase
softx_upper_proxy: during=0.0007438659667665 delta_before=0.0003623962402636 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=5.638800083170152e+19 delta_before=6.009328025051595e+18 trend=increase
nbi_proxy: during=1474408.5 delta_before=429285.75 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.2827999928593638 → 0.2907999928593638 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.5450636344276578 delta_before=0.526778741420181 trend=increase
C_edge_capacity: during=0.6776118823067855 delta_before=-0.013927322509626028 trend=decrease
F_route_fragmentation: during=0.1261567416162326 delta_before=-0.5472451759661155 trend=decrease
S_edge_response: during=0.5708605258289889 delta_before=-0.03727359937076913 trend=decrease
S_power_balance: during=0.1048088570371238 delta_before=-0.6688552150696968 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.6127929687412925 delta_before=0.019531249999762856 trend=increase
softx_lower_proxy: during=0.0146007537853021 delta_before=-0.0009059905990021003 trend=decrease
softx_upper_proxy: during=0.007038116455051 delta_before=-0.0009727478025629002 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.5309260375962367e+20 delta_before=5.532443443806061e+18 trend=increase
nbi_proxy: during=393.9477233886719 delta_before=-1711230.6772766113 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.2867999928593638 → 0.448799992859364 s
duration: 0.1620000000000002 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3970143857514779 delta_before=0.3863450701328747 trend=decrease
C_edge_capacity: during=0.6077174736293152 delta_before=-0.0813038474992771 trend=decrease
F_route_fragmentation: during=0.2139736125897344 delta_before=-0.4629289109673202 trend=increase
S_edge_response: during=0.3035373835893764 delta_before=-0.29057603398175985 trend=decrease
S_power_balance: during=0.2121405882269593 delta_before=-0.5658020022933914 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.6445312500224429 delta_before=0.05126953128091327 trend=increase
softx_lower_proxy: during=0.0024795532222142 delta_before=-0.0126838684087942 trend=decrease
softx_upper_proxy: during=0.0015258789062048 delta_before=-0.0059509277347846 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.9223303627737976e+20 delta_before=4.2925391345212195e+19 trend=increase
nbi_proxy: during=0.3514847159385681 delta_before=-1705299.523515284 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.481799992859364 → 0.5447999928593641 s
duration: 0.06300000000000011 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4760725005747465 delta_before=0.4064952920767012 trend=increase
C_edge_capacity: during=0.5771039440097772 delta_before=0.41226413866084854 trend=increase
F_route_fragmentation: during=0.10103026919640885 delta_before=-2.348565162749172e-06 trend=flat
S_edge_response: during=0.5771039440097772 delta_before=0.5643205158151893 trend=increase
S_power_balance: during=2.4650005487422233e-05 delta_before=-0.00036388365390897776 trend=flat
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.00244140625 delta_before=-1.638183593777105 trend=decrease
softx_lower_proxy: during=-0.0019073486328682501 delta_before=-0.0006008148196683502 trend=increase
softx_upper_proxy: during=-0.00120162963862375 delta_before=0.0014686584472504499 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-2.284837007522583 delta_before=-4.980424880981445 trend=flat
missingness_pressure: during=0.5555555555555556 delta_before=0.11111111111111116 trend=flat
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```