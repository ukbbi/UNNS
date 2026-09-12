# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11776_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     523
time_min: -0.0672000050544738
time_max: 0.4547999949455266
```

State counts:

```text
positive_boundary_margin: 345
negative_leakage_margin: 82
insufficient_data: 59
boundary_ambiguous_margin: 37
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                          |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:--------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| negative_001   | negative_leakage_margin  |  -0.00920001 | 0.00579999 |      0.015 |            16 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high                                            |               -0.558338 |                       0.286521   |                              0.85001   |                         0.377054 |                        0.890753  |                              |                              0.666667 |
| positive_001   | positive_boundary_margin |   0.0178     | 0.3328     |      0.315 |           316 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                          |                0.52893  |                       0.69249    |                              0.164239  |                         0.578049 |                        0.101971  |                              |                              0.444444 |
| peak_positive  | peak_positive_window     |   0.3108     | 0.3188     |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                          |                0.703118 |                       0.793817   |                              0.0836203 |                         0.813109 |                        0.0034371 |                              |                              0.444444 |
| positive_002   | positive_boundary_margin |   0.3398     | 0.3498     |      0.01  |            11 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                          |                0.297848 |                       0.600203   |                              0.302355  |                         0.565079 |                        0.27078   |                              |                              0.444444 |
| positive_003   | positive_boundary_margin |   0.3588     | 0.3718     |      0.013 |            14 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                             |                0.274399 |                       0.527006   |                              0.24599   |                         0.420106 |                        0.201889  |                              |                              0.444444 |
| negative_002   | negative_leakage_margin  |   0.3888     | 0.4538     |      0.065 |            66 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before |               -0.835965 |                       0.0886873  |                              0.923169  |                         0.118486 |                        0.98017   |                              |                              0.666667 |
| peak_negative  | peak_negative_window     |   0.3958     | 0.4038     |      0.008 |             9 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before |               -0.909249 |                       0.00740562 |                              0.918582  |                         0        |                        0.974564  |                              |                              0.666667 |

## 6. Interpretability flags

```text
interpretable_positive_candidate: 4
fragile_negative_candidate: 3
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0092000050544738 → 0.0057999949455261 s
duration: 0.014999999999999899 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high

m_edge: during=-0.5583379015119225 delta_before=0.009769403884127614 trend=increase
C_edge_capacity: during=0.28652129797245474 delta_before=0.004134884022048757 trend=increase
F_route_fragmentation: during=0.8500101134336993 delta_before=-0.14998988656630075 trend=decrease
S_edge_response: during=0.37705443200630506 delta_before=-0.003095962904979932 trend=decrease
S_power_balance: during=0.8907531016041508 delta_before=-0.0005910738933696535 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=1.4305114715521153e-05 delta_before=7.152557366612071e-05 trend=increase
softx_upper_proxy: during=-3.8146972632374255e-05 delta_before=-3.814697256482338e-05 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-2.499389078978429e+18 delta_before=3.066386747018445e+16 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.6666666666666667 delta_before=-0.33333333333333326 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.0177999949455262 → 0.3327999949455265 s
duration: 0.3150000000000003 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.5289298797676015 delta_before=0.3359587048906132 trend=increase
C_edge_capacity: during=0.6924902379952911 delta_before=0.2239870576757581 trend=increase
F_route_fragmentation: during=0.16423888876566506 delta_before=-0.11129311667687947 trend=decrease
S_edge_response: during=0.5780485672564344 delta_before=0.19562975001544758 trend=increase
S_power_balance: during=0.1019709875037141 delta_before=-0.08664220433347007 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0009298324587282999 delta_before=0.00069618225129645 trend=increase
softx_upper_proxy: during=0.00043869018585605 delta_before=0.0007438659669763 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=4.950171112842881e+19 delta_before=1.5575324377795789e+19 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.4444444444444444 delta_before=-0.22222222222222232 trend=decrease
```

### peak_positive — peak_positive_window

```text
time: 0.3107999949455264 → 0.3187999949455264 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.7031183333263079 delta_before=0.096573752323029 trend=decrease
C_edge_capacity: during=0.7938174508622705 delta_before=0.10194428836834368 trend=increase
F_route_fragmentation: during=0.0836202534500516 delta_before=-0.004307963699108908 trend=increase
S_edge_response: during=0.8131091617771433 delta_before=0.21424983085807625 trend=increase
S_power_balance: during=0.0034370998957421 delta_before=-0.005265288965577501 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0009536743164062 delta_before=0.00015258788943349998 trend=increase
softx_upper_proxy: during=0.0043487548854819 delta_before=0.0038337707556546003 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=4.3532994664860746e+19 delta_before=-3.4602686457273303e+18 trend=decrease
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.3397999949455265 → 0.3497999949455265 s
duration: 0.010000000000000009 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.297847738431612 delta_before=0.1663459658147303 trend=increase
C_edge_capacity: during=0.6002031354511418 delta_before=0.14029269733073246 trend=increase
F_route_fragmentation: during=0.3023553970195297 delta_before=-0.026053268483997805 trend=decrease
S_edge_response: during=0.5650785412573358 delta_before=0.2300541830490756 trend=increase
S_power_balance: during=0.2707800531473265 delta_before=-0.03184288370266397 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-5.722045838298161e-05 delta_before=0.0001335144051341184 trend=increase
softx_upper_proxy: during=0.00160217285204 delta_before=0.0016784667968796439 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=2.966371540967568e+19 delta_before=1.651952449059029e+18 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.3587999949455265 → 0.3717999949455265 s
duration: 0.013000000000000012 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.27439920314283284 delta_before=0.09412242963564643 trend=increase
C_edge_capacity: during=0.5270055271710063 delta_before=0.05421666799132335 trend=decrease
F_route_fragmentation: during=0.2459901783806376 delta_before=-0.058474947238623204 trend=decrease
S_edge_response: during=0.420106393288608 delta_before=0.10145730729109692 trend=decrease
S_power_balance: during=0.2018892303664584 delta_before=-0.07146937995831709 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.00024795532271065 delta_before=0.00014305114658265004 trend=increase
softx_upper_proxy: during=0.00057220459128505 delta_before=0.00069618225180055 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=3.3237649368459248e+19 delta_before=3.707704941465305e+18 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.3887999949455265 → 0.4537999949455266 s
duration: 0.06500000000000011 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.8359650125139662 delta_before=-0.796332421411297 trend=decrease
C_edge_capacity: during=0.08868734510787304 delta_before=-0.17880530907207834 trend=decrease
F_route_fragmentation: during=0.9231691260819206 delta_before=0.6555442503939687 trend=increase
S_edge_response: during=0.1184856255874289 delta_before=0.012353550178470799 trend=increase
S_power_balance: during=0.9801696726186435 delta_before=0.801220750481517 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.00140190124128245 delta_before=-0.00023841856919835014 trend=decrease
softx_upper_proxy: during=-0.0008392333983728 delta_before=1.907348470460001e-05 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-7.138162528428753e+18 delta_before=-4.156591448669972e+19 trend=decrease
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.6666666666666667 delta_before=0.0 trend=flat
```

### peak_negative — peak_negative_window

```text
time: 0.3957999949455265 → 0.4037999949455265 s
duration: 0.008000000000000007 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.9092492085870484 delta_before=-0.4465701783341808 trend=decrease
C_edge_capacity: during=0.0074056206291178 delta_before=-0.1097083714631949 trend=decrease
F_route_fragmentation: during=0.9185824986975994 delta_before=0.33878947635241907 trend=increase
S_edge_response: during=0.0 delta_before=-0.0109649123045562 trend=flat
S_power_balance: during=0.9745637947044732 delta_before=0.4140760266529565 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.0016593933109547 delta_before=-0.0001525878907685 trend=decrease
softx_upper_proxy: during=-0.0024032592765312 delta_before=0.00026702880724970013 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-6.847339503858745e+18 delta_before=-2.148153140630153e+19 trend=decrease
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.6666666666666667 delta_before=0.0 trend=flat
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```