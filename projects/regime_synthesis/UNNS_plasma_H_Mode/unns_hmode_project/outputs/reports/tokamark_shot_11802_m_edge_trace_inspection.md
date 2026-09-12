# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11802_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     496
time_min: -0.0676000043749809
time_max: 0.4273999956250195
```

State counts:

```text
positive_boundary_margin: 237
boundary_ambiguous_margin: 166
insufficient_data: 58
negative_leakage_margin: 35
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                 |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:-------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| positive_001   | positive_boundary_margin |       0.0274 |     0.0324 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.270049 |                         0.526718 |                               0.253718 |                         0.626988 |                         0.233788 |                              |                              0.444444 |
| positive_002   | positive_boundary_margin |       0.0484 |     0.0534 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.300276 |                         0.506986 |                               0.205378 |                         0.737438 |                         0.201634 |                              |                              0.222222 |
| positive_003   | positive_boundary_margin |       0.0624 |     0.0784 |      0.016 |            17 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.461655 |                         0.656551 |                               0.194897 |                         0.8601   |                         0.188824 |                              |                              0.222222 |
| peak_positive  | peak_positive_window     |       0.0674 |     0.0754 |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.515628 |                         0.667194 |                               0.160242 |                         0.865187 |                         0.146469 |                              |                              0.222222 |
| positive_004   | positive_boundary_margin |       0.0874 |     0.0934 |      0.006 |             7 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.373673 |                         0.54071  |                               0.162441 |                         0.553199 |                         0.149156 |                              |                              0.222222 |
| positive_005   | positive_boundary_margin |       0.1074 |     0.1124 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.399861 |                         0.547824 |                               0.151677 |                         0.507605 |                         0.136    |                              |                              0.222222 |
| positive_006   | positive_boundary_margin |       0.1234 |     0.1374 |      0.014 |            15 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.394858 |                         0.609948 |                               0.192155 |                         0.5016   |                         0.185474 |                              |                              0.222222 |
| positive_007   | positive_boundary_margin |       0.1434 |     0.1584 |      0.015 |            16 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.437463 |                         0.647326 |                               0.1995   |                         0.561731 |                         0.194451 |                              |                              0.222222 |
| positive_008   | positive_boundary_margin |       0.1614 |     0.1784 |      0.017 |            18 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.466926 |                         0.682015 |                               0.240065 |                         0.569735 |                         0.24403  |                              |                              0.222222 |
| positive_009   | positive_boundary_margin |       0.1824 |     0.1914 |      0.009 |            10 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.403018 |                         0.677136 |                               0.261291 |                         0.507304 |                         0.269973 |                              |                              0.222222 |
| positive_010   | positive_boundary_margin |       0.1934 |     0.1964 |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.459806 |                         0.663357 |                               0.195208 |                         0.486596 |                         0.189204 |                              |                              0.222222 |
| positive_011   | positive_boundary_margin |       0.2054 |     0.2094 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.34713  |                         0.625005 |                               0.295039 |                         0.429146 |                         0.311221 |                              |                              0.222222 |
| positive_012   | positive_boundary_margin |       0.2114 |     0.2154 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.405918 |                         0.616788 |                               0.205566 |                         0.420349 |                         0.201865 |                              |                              0.222222 |
| positive_013   | positive_boundary_margin |       0.2174 |     0.2214 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure                                              |                0.323058 |                         0.623178 |                               0.304651 |                         0.444886 |                         0.322968 |                              |                              0.222222 |
| positive_014   | positive_boundary_margin |       0.2244 |     0.2334 |      0.009 |            10 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.321865 |                         0.616681 |                               0.298719 |                         0.438925 |                         0.315718 |                              |                              0.222222 |
| positive_015   | positive_boundary_margin |       0.2364 |     0.2394 |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.332422 |                         0.611449 |                               0.274873 |                         0.436462 |                         0.286573 |                              |                              0.222222 |
| positive_016   | positive_boundary_margin |       0.2424 |     0.2464 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.37839  |                         0.610206 |                               0.231816 |                         0.425362 |                         0.233948 |                              |                              0.222222 |
| positive_017   | positive_boundary_margin |       0.2484 |     0.2534 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.423883 |                         0.611325 |                               0.190913 |                         0.424322 |                         0.183955 |                              |                              0.222222 |
| positive_018   | positive_boundary_margin |       0.2554 |     0.2584 |      0.003 |             4 | weak_positive_candidate          | capacity_exceeds_fragmentation                                                                         |                0.27713  |                         0.609701 |                               0.342033 |                         0.417976 |                         0.368657 |                              |                              0.222222 |
| positive_019   | positive_boundary_margin |       0.2624 |     0.2664 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.381633 |                         0.609088 |                               0.223697 |                         0.410834 |                         0.224025 |                              |                              0.222222 |
| positive_020   | positive_boundary_margin |       0.2684 |     0.2724 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.345889 |                         0.612446 |                               0.263544 |                         0.409207 |                         0.272727 |                              |                              0.222222 |
| positive_021   | positive_boundary_margin |       0.2824 |     0.2854 |      0.003 |             4 | weak_positive_candidate          | capacity_exceeds_fragmentation;m_edge_higher_than_before                                               |                0.291961 |                         0.634782 |                               0.343611 |                         0.414741 |                         0.370587 |                              |                              0.222222 |
| positive_022   | positive_boundary_margin |       0.2884 |     0.2974 |      0.009 |            10 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.371685 |                         0.645265 |                               0.271557 |                         0.439739 |                         0.28252  |                              |                              0.222222 |
| positive_023   | positive_boundary_margin |       0.3004 |     0.3174 |      0.017 |            18 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure                                              |                0.339709 |                         0.673326 |                               0.304406 |                         0.506516 |                         0.322669 |                              |                              0.222222 |
| peak_negative  | peak_negative_window     |       0.3584 |     0.3664 |      0.008 |             9 | weak_negative_candidate          | fragmentation_exceeds_capacity;m_edge_lower_than_before                                                |               -0.191429 |                         0.319944 |                               0.448415 |                         0.407565 |                         0.449297 |                              |                              0.444444 |
| negative_001   | negative_leakage_margin  |       0.3604 |     0.3634 |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.401439 |                         0.317335 |                               0.72686  |                         0.406483 |                         0.789619 |                              |                              0.444444 |
| negative_002   | negative_leakage_margin  |       0.3744 |     0.3774 |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.299493 |                         0.387547 |                               0.689407 |                         0.572756 |                         0.743843 |                              |                              0.444444 |
| negative_003   | negative_leakage_margin  |       0.3814 |     0.3844 |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.333794 |                         0.391428 |                               0.721082 |                         0.580054 |                         0.782557 |                              |                              0.444444 |

## 6. Interpretability flags

```text
interpretable_positive_candidate: 22
interpretable_negative_candidate: 3
weak_positive_candidate: 2
weak_negative_candidate: 1
```

## 7. Detailed window notes

### positive_001 — positive_boundary_margin

```text
time: 0.0273999956250191 → 0.0323999956250191 s
duration: 0.005000000000000001 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.2700487603817783 delta_before=0.2002971020354063 trend=increase
C_edge_capacity: during=0.5267181894378747 delta_before=0.06982637358886407 trend=decrease
F_route_fragmentation: during=0.2537176236529797 delta_before=-0.1334225338496589 trend=decrease
S_edge_response: during=0.6269875923575801 delta_before=0.10319950693689162 trend=increase
S_power_balance: during=0.23378837564087585 delta_before=-0.14061749587469474 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.4406738281139868 delta_before=0.018310546831935115 trend=increase
softx_lower_proxy: during=0.0037193298345642 delta_before=0.0013542175313704 trend=increase
softx_upper_proxy: during=0.004234313966118151 delta_before=0.0036239624030154505 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=6.417330621742527e+19 delta_before=1.7563005005814825e+18 trend=increase
nbi_proxy: during=-1.1276901960372925 delta_before=-4.173402905464172 trend=increase
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=decrease
```

### positive_002 — positive_boundary_margin

```text
time: 0.0483999956250191 → 0.0533999956250191 s
duration: 0.0049999999999999975 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3002758598268024 delta_before=0.11164795495997948 trend=decrease
C_edge_capacity: during=0.5069855848195173 delta_before=-0.028123075853834 trend=increase
F_route_fragmentation: during=0.2053775065636249 delta_before=-0.11437476482201359 trend=increase
S_edge_response: during=0.7374379640176085 delta_before=0.004376813702382298 trend=increase
S_power_balance: during=0.20163423641726996 delta_before=-0.13979137922690554 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.33447265626080813 delta_before=-0.019531250001490752 trend=increase
softx_lower_proxy: during=0.0052928924560930995 delta_before=0.00041007995622359926 trend=increase
softx_upper_proxy: during=0.004291534423794549 delta_before=-0.000801086425939351 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=7.759904468098875e+19 delta_before=5.973044141334987e+18 trend=increase
nbi_proxy: during=-1.1276901960372925 delta_before=-4.173402905464172 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.0623999956250191 → 0.0783999956250192 s
duration: 0.016000000000000104 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4616546506552325 delta_before=0.22589321049037747 trend=decrease
C_edge_capacity: during=0.656551200927999 delta_before=0.0963299904327849 trend=decrease
F_route_fragmentation: during=0.1948965502727664 delta_before=-0.1020194835927822 trend=increase
S_edge_response: during=0.8600998378398083 delta_before=0.045770995752619004 trend=decrease
S_power_balance: during=0.1888241787284429 delta_before=-0.1246904799467338 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2661132812240977 delta_before=-0.05126953129826389 trend=increase
softx_lower_proxy: during=0.0098037719724538 delta_before=0.002975463868501501 trend=decrease
softx_upper_proxy: during=0.0091552734389776 delta_before=0.003356933595664399 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=9.378011750231704e+19 delta_before=9.759388353442087e+18 trend=increase
nbi_proxy: during=0.4100691378116607 delta_before=-2.635643571615219 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.0673999956250192 → 0.0753999956250192 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.5156277931958535 delta_before=0.2035309409424968 trend=decrease
C_edge_capacity: during=0.6671941082818156 delta_before=0.03967467429773297 trend=increase
F_route_fragmentation: during=0.1602421830923006 delta_before=-0.16517607680940521 trend=increase
S_edge_response: during=0.8651871164451114 delta_before=0.006359098279844599 trend=decrease
S_power_balance: during=0.1464688410634292 delta_before=-0.2018818716559396 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2563476562602864 delta_before=-0.012207031249329148 trend=increase
softx_lower_proxy: during=0.0100326538086348 delta_before=0.002164840697748251 trend=increase
softx_upper_proxy: during=0.009460449218913 delta_before=0.0015354156504648487 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=9.468946639504592e+19 delta_before=7.775930949585338e+18 trend=increase
nbi_proxy: during=-0.76142817735672 delta_before=-5.563484489917755 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.0873999956250192 → 0.0933999956250192 s
duration: 0.006000000000000005 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.373672597130704 delta_before=0.07632569462915578 trend=decrease
C_edge_capacity: during=0.5407100371053463 delta_before=0.02807228294199582 trend=increase
F_route_fragmentation: during=0.1624406614966276 delta_before=-0.08971530654108131 trend=increase
S_edge_response: during=0.5531985870421119 delta_before=0.04251747334449896 trend=increase
S_power_balance: during=0.1491558702242733 delta_before=-0.10965204132798834 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3002929687615535 delta_before=-0.012207031260957235 trend=increase
softx_lower_proxy: during=0.0014495849608012 delta_before=0.0006294250532123 trend=increase
softx_upper_proxy: during=0.0009155273439785 delta_before=0.0007534027098797001 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=8.444109443440627e+19 delta_before=5.576916490126361e+18 trend=increase
nbi_proxy: during=-1.640276551246643 delta_before=-4.539069056510925 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_005 — positive_boundary_margin

```text
time: 0.1073999956250192 → 0.1123999956250192 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.39986125996909916 delta_before=0.13734382690601066 trend=decrease
C_edge_capacity: during=0.5478244509096526 delta_before=-0.0032563515092459694 trend=decrease
F_route_fragmentation: during=0.15167704237493412 delta_before=-0.1233872963923503 trend=increase
S_edge_response: during=0.5076048233235124 delta_before=-0.01867345311354951 trend=decrease
S_power_balance: during=0.13600033574220338 delta_before=-0.1508066955906504 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.33203124998309824 delta_before=0.014648437489471366 trend=increase
softx_lower_proxy: during=0.00092983245873115 delta_before=-0.00019550323455215003 trend=decrease
softx_upper_proxy: during=0.0002098083491843 delta_before=-0.00010490417530399998 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=9.57843776661713e+19 delta_before=-5.421999699819397e+17 trend=decrease
nbi_proxy: during=-1.1276901960372925 delta_before=-4.173402905464172 trend=flat
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_006 — positive_boundary_margin

```text
time: 0.1233999956250192 → 0.1373999956250192 s
duration: 0.013999999999999999 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3948580244741505 delta_before=0.1325478897531499 trend=decrease
C_edge_capacity: during=0.609947522466497 delta_before=0.056543862684434676 trend=increase
F_route_fragmentation: during=0.1921553136517528 delta_before=-0.1007827053296681 trend=increase
S_edge_response: during=0.5016003479269593 delta_before=0.010810694179702707 trend=increase
S_power_balance: during=0.1854737784138707 delta_before=-0.12317886206959439 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3442382812947233 delta_before=0.0073242187456766805 trend=increase
softx_lower_proxy: during=0.0002574920659354 delta_before=-0.00036239624227400003 trend=decrease
softx_upper_proxy: during=0.0006294250501028 delta_before=0.0006961822519549745 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.1011515713590605e+20 delta_before=9.329162647632888e+18 trend=increase
nbi_proxy: during=1.1421421766281128 delta_before=-3.807141423225403 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_007 — positive_boundary_margin

```text
time: 0.1433999956250192 → 0.1583999956250192 s
duration: 0.014999999999999986 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.43746270323138536 delta_before=0.11755707255686287 trend=increase
C_edge_capacity: during=0.647326033533171 delta_before=0.04019791209458978 trend=increase
F_route_fragmentation: during=0.19950046343265382 delta_before=-0.09127976493408346 trend=increase
S_edge_response: during=0.5617305526303749 delta_before=0.02214733191352991 trend=increase
S_power_balance: during=0.19445118370163866 delta_before=-0.11156415714165752 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.36743164060785605 delta_before=0.006103515646616264 trend=decrease
softx_lower_proxy: during=2.3841858465849566e-05 delta_before=-0.00016689300508395042 trend=increase
softx_upper_proxy: during=0.00405311584424565 delta_before=0.0011920928965337505 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.2078552605733264e+20 delta_before=9.168823065977553e+18 trend=increase
nbi_proxy: during=1.1421421766281128 delta_before=-3.807141423225403 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_008 — positive_boundary_margin

```text
time: 0.1613999956250192 → 0.1783999956250193 s
duration: 0.0170000000000001 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.46692649929472807 delta_before=0.056918910289256774 trend=increase
C_edge_capacity: during=0.6820153444301192 delta_before=0.011588947297925145 trend=increase
F_route_fragmentation: during=0.240064635162275 delta_before=-0.02098367306725618 trend=increase
S_edge_response: during=0.5697351463574328 delta_before=-0.013982376843211908 trend=increase
S_power_balance: during=0.24402961581562005 delta_before=-0.025646711526646437 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.38330078120583566 delta_before=0.014648437464333086 trend=increase
softx_lower_proxy: during=0.00013351440413415002 delta_before=5.7220458755554985e-05 trend=decrease
softx_upper_proxy: during=0.00418663024888845 delta_before=-0.0005054473878302497 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.321113138600765e+20 delta_before=7.768546629493178e+18 trend=increase
nbi_proxy: during=2.0204673409461975 delta_before=-0.8783251643180847 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_009 — positive_boundary_margin

```text
time: 0.1823999956250193 → 0.1913999956250193 s
duration: 0.009000000000000008 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.40301791354233985 delta_before=0.02965628671104603 trend=decrease
C_edge_capacity: during=0.6771362194548676 delta_before=-0.008765997351656729 trend=increase
F_route_fragmentation: during=0.261291221425039 delta_before=-0.020470558428543062 trend=increase
S_edge_response: during=0.5073043597113174 delta_before=-0.023895587747542302 trend=increase
S_power_balance: during=0.26997322124788725 delta_before=-0.025019571412663755 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3942871094373992 delta_before=0.0061035156038783955 trend=decrease
softx_lower_proxy: during=0.00045299530236315 delta_before=0.00030994415483095 trend=decrease
softx_upper_proxy: during=0.0021076202392243497 delta_before=-0.0009822845475140505 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.3542521111986779e+20 delta_before=1.9891748643211837e+18 trend=increase
nbi_proxy: during=2.0204673409461975 delta_before=-1.0252453684806824 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_010 — positive_boundary_margin

```text
time: 0.1933999956250193 → 0.1963999956250193 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.45980649102472254 delta_before=0.027132290771336665 trend=decrease
C_edge_capacity: during=0.6633571436847304 delta_before=-0.013251442656618151 trend=decrease
F_route_fragmentation: during=0.19520763894418747 delta_before=-0.04561302405230852 trend=increase
S_edge_response: during=0.48659598300749307 delta_before=-0.017138592605038805 trend=decrease
S_power_balance: during=0.18920439821573526 delta_before=-0.05574925161948824 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.4235839843705073 delta_before=0.025634765553198713 trend=increase
softx_lower_proxy: during=0.0010013580315363 delta_before=0.0005340576128075999 trend=increase
softx_upper_proxy: during=0.00091552734368975 delta_before=-0.0010681152348121499 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.3744710745023159e+20 delta_before=1.7146839854701445e+18 trend=increase
nbi_proxy: during=-0.6882660090923309 delta_before=-1.8304081857204437 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_011 — positive_boundary_margin

```text
time: 0.2053999956250193 → 0.2093999956250193 s
duration: 0.0040000000000000036 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.347130137592831 delta_before=0.06562240108623063 trend=increase
C_edge_capacity: during=0.6250054114155101 delta_before=-0.018436503862581777 trend=increase
F_route_fragmentation: during=0.2950390184308717 delta_before=-0.09816873507940899 trend=decrease
S_edge_response: during=0.4291464134676712 delta_before=-0.018128165907225935 trend=increase
S_power_balance: during=0.3112205286994605 delta_before=-0.1199840095414999 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.4980468749897543 delta_before=0.04394531232994292 trend=decrease
softx_lower_proxy: during=0.0009918212880288 delta_before=3.8146972237500004e-05 trend=increase
softx_upper_proxy: during=0.0003242492679783 delta_before=-0.00022888183553729994 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.3909662997859325e+20 delta_before=2.2556700946153472e+17 trend=increase
nbi_proxy: during=3.04571270942688 delta_before=-3.807141065597534 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```