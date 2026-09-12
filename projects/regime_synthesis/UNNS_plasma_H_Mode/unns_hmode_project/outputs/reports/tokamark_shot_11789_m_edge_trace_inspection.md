# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11789_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     506
time_min: -0.0672000050544738
time_max: 0.4377999949455265
```

State counts:

```text
boundary_ambiguous_margin: 245
positive_boundary_margin: 149
insufficient_data: 59
negative_leakage_margin: 53
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                          |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:--------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| positive_001   | positive_boundary_margin |       0.1348 |     0.1398 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                                                     |                0.233495 |                        0.732506  |                               0.511341 |                        0.730916  |                         0.550898 |                              |                              0.333333 |
| positive_002   | positive_boundary_margin |       0.1478 |     0.1528 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                                                     |                0.279521 |                        0.780575  |                               0.511341 |                        0.760102  |                         0.550898 |                              |                              0.333333 |
| peak_positive  | peak_positive_window     |       0.1508 |     0.1588 |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                                                     |                0.264729 |                        0.77607   |                               0.511341 |                        0.740788  |                         0.550898 |                              |                              0.333333 |
| positive_003   | positive_boundary_margin |       0.1578 |     0.1648 |      0.007 |             8 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high                                                                               |                0.253271 |                        0.764612  |                               0.511341 |                        0.719433  |                         0.550898 |                              |                              0.333333 |
| positive_004   | positive_boundary_margin |       0.1668 |     0.1718 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                                                     |                0.28964  |                        0.79152   |                               0.511341 |                        0.733828  |                         0.550898 |                              |                              0.333333 |
| positive_005   | positive_boundary_margin |       0.1758 |     0.1808 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high                                                                               |                0.257058 |                        0.767639  |                               0.511341 |                        0.70926   |                         0.550898 |                              |                              0.333333 |
| positive_006   | positive_boundary_margin |       0.1878 |     0.1958 |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high                                                                               |                0.231027 |                        0.740423  |                               0.511341 |                        0.685703  |                         0.550898 |                              |                              0.333333 |
| positive_007   | positive_boundary_margin |       0.1978 |     0.2028 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                                                     |                0.249494 |                        0.743769  |                               0.511341 |                        0.679284  |                         0.550898 |                              |                              0.333333 |
| positive_008   | positive_boundary_margin |       0.2168 |     0.2208 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                                                     |                0.232389 |                        0.722643  |                               0.511341 |                        0.658263  |                         0.550898 |                              |                              0.333333 |
| positive_009   | positive_boundary_margin |       0.2518 |     0.2548 |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                                                     |                0.217815 |                        0.713518  |                               0.511341 |                        0.637123  |                         0.550898 |                              |                              0.333333 |
| positive_010   | positive_boundary_margin |       0.3078 |     0.3118 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                                                     |                0.23619  |                        0.74753   |                               0.511341 |                        0.767496  |                         0.550898 |                              |                              0.333333 |
| negative_001   | negative_leakage_margin  |       0.3498 |     0.3608 |      0.011 |            12 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before |               -0.511338 |                        0.0486748 |                               0.551745 |                        0.0486748 |                         0.550898 |                              |                              0.555556 |
| peak_negative  | peak_negative_window     |       0.3618 |     0.3698 |      0.008 |             9 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low                                                      |               -0.215792 |                        0.0105171 |                               0.429263 |                        0.0105171 |                         0.401198 |                              |                              0.555556 |

## 6. Interpretability flags

```text
interpretable_positive_candidate: 11
fragile_negative_candidate: 2
```

## 7. Detailed window notes

### positive_001 — positive_boundary_margin

```text
time: 0.1347999949455263 → 0.1397999949455263 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.23349513291826712 delta_before=0.024763442293261523 trend=increase
C_edge_capacity: during=0.732506246151772 delta_before=0.04047880686657401 trend=increase
F_route_fragmentation: during=0.5113409330608133 delta_before=0.0 trend=flat
S_edge_response: during=0.7309163231424363 delta_before=0.039684419182062225 trend=increase
S_power_balance: during=0.5508981774446978 delta_before=0.0 trend=flat
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.21728515621586114 delta_before=0.006103515579903962 trend=increase
softx_lower_proxy: during=0.0008392333981134 delta_before=-0.00020980834976395003 trend=increase
softx_upper_proxy: during=0.0017452239985182002 delta_before=0.0012397766102674001 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.0 delta_before=0.0 trend=flat
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.1477999949455263 → 0.1527999949455263 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.27952097467361425 delta_before=0.038479107631539666 trend=decrease
C_edge_capacity: during=0.7805750783664629 delta_before=0.04079591550872996 trend=increase
F_route_fragmentation: during=0.5113409330608133 delta_before=0.0 trend=increase
S_edge_response: during=0.7601023981595416 delta_before=0.024495534494763493 trend=increase
S_power_balance: during=0.5508981774446978 delta_before=0.0 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.22705078124571393 delta_before=-2.0311863302424626e-11 trend=flat
softx_lower_proxy: during=0.00073909759529685 delta_before=-8.106231681244999e-05 trend=decrease
softx_upper_proxy: during=0.00263214111265915 delta_before=0.00045776367106685 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.0 delta_before=0.0 trend=increase
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.1507999949455263 → 0.1587999949455263 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.2647292859908673 delta_before=0.009162762201282093 trend=decrease
C_edge_capacity: during=0.7760702190516806 delta_before=0.02233811826380594 trend=decrease
F_route_fragmentation: during=0.5113409330608133 delta_before=0.0 trend=flat
S_edge_response: during=0.7407875075327199 delta_before=0.018181915767411905 trend=decrease
S_power_balance: during=0.5508981774446978 delta_before=0.0 trend=flat
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2416992187415771 delta_before=0.014648437499441003 trend=increase
softx_lower_proxy: during=0.0005912780757153 delta_before=-0.00015258789055189995 trend=decrease
softx_upper_proxy: during=0.0030517578127585 delta_before=0.0008201599131225997 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.0 delta_before=0.0 trend=flat
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.1577999949455263 → 0.1647999949455263 s
duration: 0.007000000000000006 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high

m_edge: during=0.2532711794198235 delta_before=-0.002295344369761698 trend=increase
C_edge_capacity: during=0.7646121124806369 delta_before=-0.010626353228293528 trend=increase
F_route_fragmentation: during=0.5113409330608133 delta_before=0.0 trend=decrease
S_edge_response: during=0.7194328819638474 delta_before=-0.021354625568872576 trend=increase
S_power_balance: during=0.5508981774446978 delta_before=0.0 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2331542969051696 delta_before=0.001220703155169589 trend=decrease
softx_lower_proxy: during=0.00037670135511305 delta_before=-0.00021457672118745 trend=increase
softx_upper_proxy: during=0.00275611877470925 delta_before=-0.00012397766064454986 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.0 delta_before=0.0 trend=decrease
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.1667999949455263 → 0.1717999949455263 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.2896398466634279 delta_before=0.0478267738146482 trend=decrease
C_edge_capacity: during=0.7915201142525898 delta_before=0.016281648543659433 trend=increase
F_route_fragmentation: during=0.5113409330608133 delta_before=0.0 trend=increase
S_edge_response: during=0.7338275637481 delta_before=-0.001923536112647839 trend=increase
S_power_balance: during=0.5508981774446978 delta_before=0.0 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.25024414062977046 delta_before=0.013427734354278159 trend=increase
softx_lower_proxy: during=0.0006628036499022 delta_before=0.0002241134638289 trend=increase
softx_upper_proxy: during=0.0027561187746590497 delta_before=0.00014305114825104983 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.0 delta_before=0.0 trend=increase
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_005 — positive_boundary_margin

```text
time: 0.1757999949455263 → 0.1807999949455263 s
duration: 0.004999999999999977 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high

m_edge: during=0.25705835407593336 delta_before=-0.028447210415862623 trend=decrease
C_edge_capacity: during=0.7676388720429839 delta_before=-0.018554858909586414 trend=decrease
F_route_fragmentation: during=0.5113409330608133 delta_before=0.0 trend=increase
S_edge_response: during=0.7092599367088965 delta_before=-0.022736643847262483 trend=decrease
S_power_balance: during=0.5508981774446978 delta_before=0.0 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.26000976563878964 delta_before=0.008544921958259954 trend=increase
softx_lower_proxy: during=0.0002861022954919 delta_before=-0.0003337860101376 trend=decrease
softx_upper_proxy: during=0.0028419494624189 delta_before=0.00019073486323409978 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.0 delta_before=0.0 trend=increase
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_006 — positive_boundary_margin

```text
time: 0.1877999949455263 → 0.1957999949455263 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high

m_edge: during=0.2310265808008869 delta_before=-0.02464700638192402 trend=decrease
C_edge_capacity: during=0.7404228214203347 delta_before=-0.009809585496550755 trend=decrease
F_route_fragmentation: during=0.5113409330608133 delta_before=0.0 trend=increase
S_edge_response: during=0.6857028540835889 delta_before=0.0036736093522121704 trend=decrease
S_power_balance: during=0.5508981774446978 delta_before=0.0 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2880859375288465 delta_before=0.017089843806686766 trend=decrease
softx_lower_proxy: during=0.0006008148220778 delta_before=0.00025749206861380003 trend=decrease
softx_upper_proxy: during=0.0020408630353064 delta_before=-0.00015258789338939982 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.0 delta_before=0.0 trend=increase
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_007 — positive_boundary_margin

```text
time: 0.1977999949455263 → 0.2027999949455263 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.24949351983622636 delta_before=0.01846693903533947 trend=decrease
C_edge_capacity: during=0.7437688595454486 delta_before=0.0014013456837483895 trend=decrease
F_route_fragmentation: during=0.5113409330608133 delta_before=0.0 trend=increase
S_edge_response: during=0.6792840418606001 delta_before=-0.008160481973974232 trend=decrease
S_power_balance: during=0.5508981774446978 delta_before=0.0 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.29174804692462597 delta_before=0.0036621093957794892 trend=increase
softx_lower_proxy: during=0.00140190124314205 delta_before=0.00073432922127335 trend=decrease
softx_upper_proxy: during=0.0011825561541652001 delta_before=-0.0008583068811412 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.0 delta_before=0.0 trend=increase
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_008 — positive_boundary_margin

```text
time: 0.2167999949455263 → 0.2207999949455263 s
duration: 0.0040000000000000036 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.2323888412066923 delta_before=0.029957636860820286 trend=increase
C_edge_capacity: during=0.7226429642187834 delta_before=0.008870826812098054 trend=decrease
F_route_fragmentation: during=0.5113409330608133 delta_before=0.0 trend=decrease
S_edge_response: during=0.6582625890646043 delta_before=0.016777316305917944 trend=decrease
S_power_balance: during=0.5508981774446978 delta_before=0.0 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2856445312392664 delta_before=-0.002441406228979981 trend=decrease
softx_lower_proxy: during=0.0013160705575566 delta_before=7.629394843829997e-05 trend=decrease
softx_upper_proxy: during=0.0006008148194608 delta_before=6.675720276250001e-05 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.0 delta_before=0.0 trend=decrease
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_009 — positive_boundary_margin

```text
time: 0.2517999949455264 → 0.2547999949455264 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.21781480146898674 delta_before=0.05306135164028933 trend=increase
C_edge_capacity: during=0.7135180512508996 delta_before=0.006434310217670269 trend=decrease
F_route_fragmentation: during=0.5113409330608133 delta_before=0.0 trend=decrease
S_edge_response: during=0.6371231712492419 delta_before=0.007726618709221422 trend=decrease
S_power_balance: during=0.5508981774446978 delta_before=0.0 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.30029296873765365 delta_before=0.01464843745232225 trend=decrease
softx_lower_proxy: during=0.00119209289634375 delta_before=0.00016212463922844994 trend=decrease
softx_upper_proxy: during=0.0003385543804839 delta_before=6.198882854210002e-05 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.0 delta_before=0.0 trend=decrease
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_010 — positive_boundary_margin

```text
time: 0.3077999949455264 → 0.3117999949455264 s
duration: 0.0040000000000000036 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.2361895206949849 delta_before=0.07463529478738318 trend=decrease
C_edge_capacity: during=0.7475304537557982 delta_before=0.030470331915086413 trend=decrease
F_route_fragmentation: during=0.5113409330608133 delta_before=-0.024496459592653563 trend=increase
S_edge_response: during=0.7674962939910571 delta_before=0.05254909497628579 trend=decrease
S_power_balance: during=0.5508981774446978 delta_before=-0.02994011727990986 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3247070312781079 delta_before=0.1269531250143928 trend=increase
softx_lower_proxy: during=0.0012016296406577 delta_before=-7.629394214450007e-05 trend=increase
softx_upper_proxy: during=0.0056838989265498 delta_before=0.0051689147953655 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.0 delta_before=-1.464686632156372 trend=increase
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### negative_001 — negative_leakage_margin

```text
time: 0.3497999949455265 → 0.3607999949455265 s
duration: 0.01100000000000001 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.5113383568949668 delta_before=-0.3605946743420054 trend=decrease
C_edge_capacity: during=0.048674751084468046 delta_before=-0.21834376728557436 trend=decrease
F_route_fragmentation: during=0.5517449734648538 delta_before=0.04040404040404055 trend=increase
S_edge_response: during=0.048674751084468046 delta_before=-0.06654410520804906 trend=decrease
S_power_balance: during=0.5508981774446978 delta_before=0.0 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=1.0278320310162867 delta_before=0.12695312464312136 trend=decrease
softx_lower_proxy: during=-0.0011253356916089 delta_before=-0.0007534027086324 trend=decrease
softx_upper_proxy: during=-0.0007438659689261501 delta_before=-0.00042915344277735004 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.0 delta_before=0.0 trend=increase
missingness_pressure: during=0.5555555555555556 delta_before=0.22222222222222227 trend=increase
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```