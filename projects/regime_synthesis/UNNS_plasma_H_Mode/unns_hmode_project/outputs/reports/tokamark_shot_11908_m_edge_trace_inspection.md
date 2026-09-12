# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11908_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     548
time_min: -0.0608000084757804
time_max: 0.48619999152422
```

State counts:

```text
boundary_ambiguous_margin: 233
negative_leakage_margin: 133
positive_boundary_margin: 131
insufficient_data: 51
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                           |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| negative_001   | negative_leakage_margin  |       0.0132 |     0.1432 |      0.13  |           131 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before                            |               -0.401273 |                         0.299326 |                              0.699604  |                        0.293303  |                      0.802098    |                              |                              0.222222 |
| peak_negative  | peak_negative_window     |       0.0202 |     0.0282 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before                            |               -0.559161 |                         0.161596 |                              0.718029  |                        0.107286  |                      0.778826    |                              |                              0.444444 |
| positive_001   | positive_boundary_margin |       0.2692 |     0.3842 |      0.115 |           116 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                              |                0.462536 |                         0.706615 |                              0.24518   |                        0.460237  |                      0.250282    |                              |                              0.222222 |
| peak_positive  | peak_positive_window     |       0.3232 |     0.3312 |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure                                                                        |                0.452404 |                         0.710055 |                              0.259893  |                        0.440534  |                      0.268264    |                              |                              0.222222 |
| positive_002   | positive_boundary_margin |       0.3872 |     0.3922 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure                                                                        |                0.234366 |                         0.298341 |                              0.0723076 |                        0.0337621 |                      0.0389932   |                              |                              0.222222 |
| positive_003   | positive_boundary_margin |       0.3982 |     0.4012 |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                              |                0.209513 |                         0.32099  |                              0.113374  |                        0.173056  |                      0.0398026   |                              |                              0.444444 |
| positive_004   | positive_boundary_margin |       0.4822 |     0.4862 |      0.004 |             5 | fragile_positive_candidate       | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.473376 |                         0.574732 |                              0.101358  |                        0.574732  |                      0.000425549 |                              |                              0.555556 |

## 6. Interpretability flags

```text
interpretable_positive_candidate: 4
interpretable_negative_candidate: 2
fragile_positive_candidate: 1
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: 0.0131999915242195 → 0.1431999915242197 s
duration: 0.1300000000000002 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.4012728074222005 delta_before=-0.32303181644829604 trend=decrease
C_edge_capacity: during=0.2993258524824027 delta_before=0.18176748591813963 trend=increase
F_route_fragmentation: during=0.6996037943697128 delta_before=0.4922019897389237 trend=increase
S_edge_response: during=0.2933030964803647 delta_before=0.25964267589215 trend=increase
S_power_balance: during=0.8020981323332417 delta_before=0.6473724698832649 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.327148437502226 delta_before=-0.26855468750267586 trend=decrease
softx_lower_proxy: during=0.0003814697265551 delta_before=0.0003719329834022342 trend=increase
softx_upper_proxy: during=0.0001907348632663 delta_before=0.0004673004150144 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=4.715822084108006e+19 delta_before=5.080513378464563e+17 trend=increase
nbi_proxy: during=1275778.75 delta_before=1269140.4733886719 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=-0.2222222222222222 trend=decrease
```

### peak_negative — peak_negative_window

```text
time: 0.0201999915242195 → 0.0281999915242195 s
duration: 0.007999999999999997 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.5591605215181406 delta_before=-0.2618733056715694 trend=increase
C_edge_capacity: during=0.1615962409353052 delta_before=0.04128007954002265 trend=increase
F_route_fragmentation: during=0.7180290175708702 delta_before=0.30086671627663214 trend=decrease
S_edge_response: during=0.1072861074894022 delta_before=0.07369492511931795 trend=increase
S_power_balance: during=0.7788255893767426 delta_before=0.36772598656032807 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.4760742187580146 delta_before=-0.09643554686581146 trend=decrease
softx_lower_proxy: during=-3.814697260955731e-05 delta_before=-3.814697261398438e-05 trend=increase
softx_upper_proxy: during=-0.0001716613769393 delta_before=6.67572021884e-05 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=4.4413435197872144e+19 delta_before=-3.503116613861769e+18 trend=decrease
nbi_proxy: during=1189698.875 delta_before=659387.078125 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.2691999915242198 → 0.3841999915242199 s
duration: 0.1150000000000001 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4625359128763197 delta_before=0.47398069787613495 trend=increase
C_edge_capacity: during=0.7066148771834309 delta_before=0.012967822003612794 trend=decrease
F_route_fragmentation: during=0.2451800072587368 delta_before=-0.4632526386714798 trend=decrease
S_edge_response: during=0.46023723365155694 delta_before=-0.01025769577032587 trend=decrease
S_power_balance: during=0.2502817372668512 delta_before=-0.5661976694873643 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.4479980468788557 delta_before=-0.05249023436122391 trend=increase
softx_lower_proxy: during=0.02157211303558745 delta_before=-0.004463195801739449 trend=decrease
softx_upper_proxy: during=0.01535415649442405 delta_before=-0.002079010009364451 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.5370386185592295e+20 delta_before=9.200704505136546e+18 trend=decrease
nbi_proxy: during=9.141890525817871 delta_before=-1137163.2331094742 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.3231999915242198 → 0.3311999915242198 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure

m_edge: during=0.4524041661830697 delta_before=-0.003609356367826666 trend=decrease
C_edge_capacity: during=0.7100553835801078 delta_before=-0.008013445683849652 trend=decrease
F_route_fragmentation: during=0.2598927938713606 delta_before=0.0021595742920733074 trend=increase
S_edge_response: during=0.4405337997930826 delta_before=-0.017946645041130194 trend=decrease
S_power_balance: during=0.2682640320156136 delta_before=0.002639479690311808 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.4443359375215417 delta_before=-0.014648437470787479 trend=increase
softx_lower_proxy: during=0.0214576721182534 delta_before=-0.002040863036865001 trend=increase
softx_upper_proxy: during=0.0133705139162802 delta_before=-0.001049041747902501 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.599762150525711e+20 delta_before=7.012069435443773e+17 trend=increase
nbi_proxy: during=168.001220703125 delta_before=-81.80545043945307 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.3871999915242199 → 0.3921999915242199 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure

m_edge: during=0.2343659142376081 delta_before=-0.07546813477868419 trend=decrease
C_edge_capacity: during=0.29834052590624316 delta_before=-0.16322073427795764 trend=decrease
F_route_fragmentation: during=0.0723075620195253 delta_before=-0.07941964914838319 trend=decrease
S_edge_response: during=0.033762147377728646 delta_before=-0.16093864103781486 trend=decrease
S_power_balance: during=0.03899319308559265 delta_before=-0.09706846007024605 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.5236816406169904 delta_before=-0.006103515630732748 trend=increase
softx_lower_proxy: during=-0.0011968612672115 delta_before=-0.0061941146876012 trend=decrease
softx_upper_proxy: during=-0.0017166137695138499 delta_before=-0.011978149414150551 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=7.389871526352257e+19 delta_before=-5.080856206190104e+19 trend=increase
nbi_proxy: during=22.452497959136963 delta_before=12.877755641937254 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.3981999915242199 → 0.4011999915242199 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.20951261461913245 delta_before=0.001637429641059951 trend=decrease
C_edge_capacity: during=0.3209901021471647 delta_before=0.03429878786304674 trend=increase
F_route_fragmentation: during=0.11337383158016814 delta_before=0.03231409331311405 trend=increase
S_edge_response: during=0.17305573206472796 delta_before=0.09535184324675067 trend=increase
S_power_balance: during=0.039802584276995706 delta_before=0.0028457053932553072 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.40283203124881406 delta_before=-0.07568359374886846 trend=decrease
softx_lower_proxy: during=-0.0012207031251230001 delta_before=0.00013351440415569995 trend=decrease
softx_upper_proxy: during=-0.00044345855706475 delta_before=0.00138759613054285 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=9.907570854931412e+19 delta_before=2.279941154091198e+19 trend=increase
nbi_proxy: during=11.839285135269165 delta_before=3.872269868850708 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=0.2222222222222222 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.48219999152422 → 0.48619999152422 s
duration: 0.0040000000000000036 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4733764982648001 delta_before=0.4072626027451958 trend=increase
C_edge_capacity: during=0.5747318479629973 delta_before=0.18782759604478216 trend=increase
F_route_fragmentation: during=0.1013582772915648 delta_before=-0.22054701939639001 trend=increase
S_edge_response: during=0.5747318479629973 delta_before=0.0 trend=increase
S_power_balance: during=0.0004255487884557 delta_before=-0.2942488261758347 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.0024414062527647 delta_before=0.0024414062445247 trend=decrease
softx_lower_proxy: during=-0.0016307830809353 delta_before=8.583068861729997e-05 trend=increase
softx_upper_proxy: during=-0.0016403198243915 delta_before=0.00017166137684449987 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=4.312103271484375 delta_before=4.099755764007568 trend=increase
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