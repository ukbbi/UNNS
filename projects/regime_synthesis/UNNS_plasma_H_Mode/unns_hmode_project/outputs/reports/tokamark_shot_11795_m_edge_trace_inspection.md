# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11795_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     496
time_min: -0.0668000057339668
time_max: 0.4281999942660336
```

State counts:

```text
boundary_ambiguous_margin: 243
positive_boundary_margin: 141
insufficient_data: 58
negative_leakage_margin: 54
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                           |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| positive_001   | positive_boundary_margin |       0.0242 |     0.0292 |      0.005 |             6 | fragile_positive_candidate       | high_missingness_pressure;capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.343332 |                         0.511052 |                               0.167719 |                         0.511052 |                        0.0815336 |                              |                              0.555556 |
| positive_002   | positive_boundary_margin |       0.0392 |     0.0492 |      0.01  |            11 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                           |                0.268215 |                         0.545103 |                               0.27761  |                         0.702678 |                        0.265227  |                              |                              0.333333 |
| positive_003   | positive_boundary_margin |       0.0632 |     0.0702 |      0.007 |             8 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                           |                0.441555 |                         0.548057 |                               0.127315 |                         0.693983 |                        0.0815336 |                              |                              0.333333 |
| positive_004   | positive_boundary_margin |       0.0802 |     0.0882 |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                           |                0.542719 |                         0.659298 |                               0.127315 |                         0.734338 |                        0.0815336 |                              |                              0.333333 |
| positive_005   | positive_boundary_margin |       0.1162 |     0.1212 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                                                      |                0.228363 |                         0.663792 |                               0.441811 |                         0.677998 |                        0.465917  |                              |                              0.333333 |
| positive_006   | positive_boundary_margin |       0.1392 |     0.1492 |      0.01  |            11 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                           |                0.413804 |                         0.723289 |                               0.27761  |                         0.699539 |                        0.265227  |                              |                              0.333333 |
| peak_positive  | peak_positive_window     |       0.1582 |     0.1662 |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                                                      |                0.299818 |                         0.727723 |                               0.427904 |                         0.645906 |                        0.44892   |                              |                              0.333333 |
| positive_007   | positive_boundary_margin |       0.1602 |     0.1702 |      0.01  |            11 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                                                      |                0.325268 |                         0.742965 |                               0.427904 |                         0.659016 |                        0.44892   |                              |                              0.333333 |
| positive_008   | positive_boundary_margin |       0.1812 |     0.1882 |      0.007 |             8 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                           |                0.439207 |                         0.727082 |                               0.27761  |                         0.632943 |                        0.265227  |                              |                              0.333333 |
| positive_009   | positive_boundary_margin |       0.2022 |     0.2082 |      0.006 |             7 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                           |                0.458169 |                         0.729094 |                               0.27761  |                         0.647825 |                        0.265227  |                              |                              0.333333 |
| positive_010   | positive_boundary_margin |       0.2202 |     0.2292 |      0.009 |            10 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                           |                0.419459 |                         0.697109 |                               0.27761  |                         0.62424  |                        0.265227  |                              |                              0.333333 |
| positive_011   | positive_boundary_margin |       0.2412 |     0.2472 |      0.006 |             7 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                           |                0.430386 |                         0.680793 |                               0.27761  |                         0.599603 |                        0.265227  |                              |                              0.333333 |
| positive_012   | positive_boundary_margin |       0.2622 |     0.2672 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                           |                0.375346 |                         0.662122 |                               0.27761  |                         0.572012 |                        0.265227  |                              |                              0.333333 |
| positive_013   | positive_boundary_margin |       0.2822 |     0.2852 |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                           |                0.463357 |                         0.632465 |                               0.169108 |                         0.557492 |                        0.132613  |                              |                              0.333333 |
| positive_014   | positive_boundary_margin |       0.2992 |     0.3032 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                           |                0.437138 |                         0.704117 |                               0.27761  |                         0.680117 |                        0.265227  |                              |                              0.333333 |
| negative_001   | negative_leakage_margin  |       0.3252 |     0.3282 |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                                              |               -0.36834  |                         0.486976 |                               0.878788 |                         0.422742 |                        1         |                              |                              0.333333 |
| negative_002   | negative_leakage_margin  |       0.3362 |     0.3662 |      0.03  |            31 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before  |               -0.486803 |                         0.268352 |                               0.652009 |                         0.10391  |                        0.70748   |                              |                              0.555556 |
| peak_negative  | peak_negative_window     |       0.3532 |     0.3612 |      0.008 |             9 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before  |               -0.535093 |                         0        |                               0.574065 |                         0        |                        0.578178  |                              |                              0.555556 |
| negative_003   | negative_leakage_margin  |       0.4052 |     0.4082 |      0.003 |             4 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.307001 |                         0.612191 |                               0.919192 |                         0.612191 |                        1         |                              |                              0.555556 |
| positive_015   | positive_boundary_margin |       0.4212 |     0.4242 |      0.003 |             4 | fragile_positive_candidate       | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.294311 |                         0.612325 |                               0.318014 |                         0.612325 |                        0.265227  |                              |                              0.555556 |

## 6. Interpretability flags

```text
interpretable_positive_candidate: 14
fragile_negative_candidate: 3
fragile_positive_candidate: 2
interpretable_negative_candidate: 1
```

## 7. Detailed window notes

### positive_001 — positive_boundary_margin

```text
time: 0.0241999942660332 → 0.0291999942660332 s
duration: 0.0049999999999999975 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3433322076277935 delta_before=0.27514744387458456 trend=increase
C_edge_capacity: during=0.5110516228604818 delta_before=0.019921678301672352 trend=increase
F_route_fragmentation: during=0.1677194152326882 delta_before=-0.258834104462058 trend=increase
S_edge_response: during=0.5110516228604818 delta_before=0.019921678301672352 trend=increase
S_power_balance: during=0.081533606272051 delta_before=-0.3163527943425154 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.4614257812378315 delta_before=-0.019531250023852476 trend=decrease
softx_lower_proxy: during=0.00025749206531225 delta_before=0.00011444091778284999 trend=increase
softx_upper_proxy: during=0.0002145767212187 delta_before=0.00016689300526358443 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-11.661662101745604 delta_before=-6.807957231998442 trend=increase
missingness_pressure: during=0.5555555555555556 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.0391999942660332 → 0.0491999942660332 s
duration: 0.010000000000000002 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.2682149989858819 delta_before=0.1896683213621455 trend=increase
C_edge_capacity: during=0.5451031094520303 delta_before=0.010839253208658639 trend=increase
F_route_fragmentation: during=0.2776099263818019 delta_before=-0.1781072522378333 trend=flat
S_edge_response: during=0.7026783152398186 delta_before=0.018508981732270335 trend=decrease
S_power_balance: during=0.2652269470592393 delta_before=-0.21768664162401857 trend=flat
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.35400390625 delta_before=-0.03173828128876022 trend=decrease
softx_lower_proxy: during=0.0004386901875908 delta_before=6.675720436889997e-05 trend=decrease
softx_upper_proxy: during=0.0020217895511824 delta_before=-0.00022888183559690006 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-7.708555221557617 delta_before=-4.684647560119629 trend=flat
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.0631999942660332 → 0.0701999942660333 s
duration: 0.0070000000000000895 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4415554323416314 delta_before=0.3684252985686315 trend=decrease
C_edge_capacity: during=0.5480567651833647 delta_before=0.013762813386507533 trend=increase
F_route_fragmentation: during=0.1273153748286478 delta_before=-0.3284018037909874 trend=increase
S_edge_response: during=0.6939834799769572 delta_before=0.05027387488775659 trend=increase
S_power_balance: during=0.081533606272051 delta_before=-0.40137998241120687 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.29785156247501077 delta_before=-0.036621093770218716 trend=decrease
softx_lower_proxy: during=0.00123977661136535 delta_before=0.00017166137602134994 trend=increase
softx_upper_proxy: during=0.0004959106441853 delta_before=0.00013351440439119994 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-11.661662101745604 delta_before=-8.637754440307615 trend=increase
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.0801999942660333 → 0.0881999942660333 s
duration: 0.007999999999999993 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.5427190966113887 delta_before=0.4119309468377847 trend=increase
C_edge_capacity: during=0.6592980584100004 delta_before=0.05025457707321446 trend=increase
F_route_fragmentation: during=0.1273153748286478 delta_before=-0.3478877305809747 trend=decrease
S_edge_response: during=0.7343382528326313 delta_before=-0.003622054771464378 trend=decrease
S_power_balance: during=0.081533606272051 delta_before=-0.4251961151545247 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2416992187332287 delta_before=0.007324218715171693 trend=increase
softx_lower_proxy: during=0.001354217529342 delta_before=3.8146972983149965e-05 trend=decrease
softx_upper_proxy: during=0.0005531311041474 delta_before=-4.768370741250029e-06 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-11.661662101745604 delta_before=-9.150281012058256 trend=decrease
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_005 — positive_boundary_margin

```text
time: 0.1161999942660333 → 0.1211999942660333 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.22836336374316174 delta_before=0.11746120760039953 trend=increase
C_edge_capacity: during=0.6637922498814474 delta_before=0.006403585246537502 trend=decrease
F_route_fragmentation: during=0.4418107965514781 delta_before=-0.09185010509101482 trend=decrease
S_edge_response: during=0.6779980030884576 delta_before=-0.008527032827140513 trend=decrease
S_power_balance: during=0.4659168994888436 delta_before=-0.11226123955568479 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2685546875068203 delta_before=-0.0048828124732777645 trend=increase
softx_lower_proxy: during=0.0007867813110751501 delta_before=-8.106231714594993e-05 trend=decrease
softx_upper_proxy: during=0.00043869018534219996 delta_before=1.9073486379699955e-05 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-3.3896788358688354 delta_before=-2.415877878665924 trend=decrease
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_006 — positive_boundary_margin

```text
time: 0.1391999942660333 → 0.1491999942660333 s
duration: 0.010000000000000009 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4138041309589484 delta_before=0.412241375340248 trend=increase
C_edge_capacity: during=0.7232889945261274 delta_before=0.055900806949672366 trend=increase
F_route_fragmentation: during=0.2776099263818019 delta_before=-0.3729665881216003 trend=flat
S_edge_response: during=0.6995394328874658 delta_before=0.04776142766855673 trend=increase
S_power_balance: during=0.2652269470592393 delta_before=-0.45584805214862256 trend=flat
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3002929687656531 delta_before=0.014648437469588105 trend=increase
softx_lower_proxy: during=0.0004768371581405 delta_before=-0.0001907348634303 trend=increase
softx_upper_proxy: during=0.0014877319335317 delta_before=0.0011634826664672 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-7.708555221557617 delta_before=-9.80991506576538 trend=flat
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.1581999942660333 → 0.1661999942660333 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.2998182401424213 delta_before=0.18612382900498553 trend=increase
C_edge_capacity: during=0.7277226546257424 delta_before=0.027572525067194986 trend=increase
F_route_fragmentation: during=0.427904414483321 delta_before=-0.18370023284332765 trend=decrease
S_edge_response: during=0.645906344892488 delta_before=0.0019794973162621243 trend=decrease
S_power_balance: during=0.4489202102944294 delta_before=-0.2245225068085116 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3076171875860924 delta_before=0.0024414063280794873 trend=increase
softx_lower_proxy: during=0.0003623962405978 delta_before=-0.00016212463358789995 trend=decrease
softx_upper_proxy: during=0.0010871887208376 delta_before=0.0005626678462647999 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-3.7554500102996826 delta_before=-4.831756353378296 trend=decrease
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_007 — positive_boundary_margin

```text
time: 0.1601999942660333 → 0.1701999942660333 s
duration: 0.010000000000000009 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.3252678442769257 delta_before=0.2176082265623674 trend=decrease
C_edge_capacity: during=0.7429645791447826 delta_before=0.04337973757505831 trend=increase
F_route_fragmentation: during=0.427904414483321 delta_before=-0.18370023284332765 trend=increase
S_edge_response: during=0.6590162883383327 delta_before=0.01517380821598957 trend=increase
S_power_balance: during=0.4489202102944294 delta_before=-0.2245225068085116 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.33203125 delta_before=0.026855468708071872 trend=increase
softx_lower_proxy: during=0.0003623962405978 delta_before=-0.00016212463358789995 trend=decrease
softx_upper_proxy: during=0.0013160705561677 delta_before=0.0008106231688963999 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-3.7554500102996826 delta_before=-4.831756353378296 trend=increase
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_008 — positive_boundary_margin

```text
time: 0.1811999942660334 → 0.1881999942660334 s
duration: 0.007000000000000006 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4392068488473255 delta_before=0.3414375584847809 trend=decrease
C_edge_capacity: during=0.7270817265757652 delta_before=-0.0031125062940194903 trend=increase
F_route_fragmentation: during=0.2776099263818019 delta_before=-0.35348065453322347 trend=increase
S_edge_response: during=0.6329428685505527 delta_before=-0.002311578808381287 trend=increase
S_power_balance: during=0.2652269470592393 delta_before=-0.4320319110961621 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3576660156344664 delta_before=0.006103515598333775 trend=increase
softx_lower_proxy: during=0.0002622604370331 delta_before=-9.536742751000012e-06 trend=increase
softx_upper_proxy: during=0.0012397766116989 delta_before=0.00012397766075155 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-7.708555221557617 delta_before=-9.297388315200806 trend=increase
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_009 — positive_boundary_margin

```text
time: 0.2021999942660334 → 0.2081999942660334 s
duration: 0.005999999999999978 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4581692109672312 delta_before=0.3832724865283236 trend=increase
C_edge_capacity: during=0.7290944424190454 delta_before=0.027619945311338823 trend=increase
F_route_fragmentation: during=0.2776099263818019 delta_before=-0.3729665881216003 trend=decrease
S_edge_response: during=0.6478247127934432 delta_before=0.032726124894275066 trend=increase
S_power_balance: during=0.2652269470592393 delta_before=-0.45584805214862256 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3808593750603765 delta_before=-0.024414062449571006 trend=flat
softx_lower_proxy: during=0.0012779235825299 delta_before=0.00049591064331 trend=increase
softx_upper_proxy: during=0.0003623962392909 delta_before=-0.00017166137706730005 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-7.708555221557617 delta_before=-9.80991506576538 trend=decrease
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_010 — positive_boundary_margin

```text
time: 0.2201999942660334 → 0.2291999942660334 s
duration: 0.009000000000000008 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4194586530087715 delta_before=0.3233473126551899 trend=decrease
C_edge_capacity: during=0.6971091160017991 delta_before=-0.010606871678431107 trend=decrease
F_route_fragmentation: during=0.2776099263818019 delta_before=-0.3339947209448468 trend=flat
S_edge_response: during=0.6242396564264416 delta_before=-0.0017343744945754747 trend=decrease
S_power_balance: during=0.2652269470592393 delta_before=-0.4082157700437017 trend=flat
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3808593750223346 delta_before=0.007324218761709467 trend=increase
softx_lower_proxy: during=0.0010013580323926 delta_before=9.536744907299999e-06 trend=decrease
softx_upper_proxy: during=0.0002622604364297 delta_before=-6.198883090469999e-05 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-7.708555221557617 delta_before=-8.78486156463623 trend=flat
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### positive_011 — positive_boundary_margin

```text
time: 0.2411999942660334 → 0.2471999942660334 s
duration: 0.006000000000000005 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4303864845749462 delta_before=0.3389095331906779 trend=increase
C_edge_capacity: during=0.6807929786190284 delta_before=0.0011440230961948794 trend=increase
F_route_fragmentation: during=0.2776099263818019 delta_before=-0.29502284753623637 trend=flat
S_edge_response: during=0.5996030886859769 delta_before=-0.014903180122536552 trend=increase
S_power_balance: during=0.2652269470592393 delta_before=-0.3605834803220668 trend=flat
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3930664063539817 delta_before=0.00488281263784951 trend=increase
softx_lower_proxy: during=0.0008392333995206 delta_before=-6.675720137100003e-05 trend=increase
softx_upper_proxy: during=0.0002670288085937 delta_before=-0.00011444091810059999 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-7.708555221557617 delta_before=-7.759807899594307 trend=flat
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```