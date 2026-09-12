# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12007_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     446
time_min: -0.0692000091075897
time_max: 0.3757999908924107
```

State counts:

```text
positive_boundary_margin: 171
boundary_ambiguous_margin: 169
insufficient_data: 60
negative_leakage_margin: 46
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                            |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:----------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| positive_001   | positive_boundary_margin |       0.1048 |     0.1088 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before |                0.388029 |                         0.693033 |                               0.29814  |                       0.680352   |                       0.00245226 |                    0.645565  |                              0        |
| positive_002   | positive_boundary_margin |       0.1118 |     0.1318 |      0.02  |            21 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before |                0.424059 |                         0.735905 |                               0.32531  |                       0.673149   |                       0.013191   |                    0.632938  |                              0        |
| positive_003   | positive_boundary_margin |       0.1338 |     0.1368 |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present                                                      |                0.220797 |                         0.722455 |                               0.500212 |                       0.603828   |                       0.47891    |                    0.637623  |                              0        |
| positive_004   | positive_boundary_margin |       0.1408 |     0.1598 |      0.019 |            20 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before |                0.360633 |                         0.764757 |                               0.405519 |                       0.587513   |                       0.280778   |                    0.605504  |                              0        |
| positive_005   | positive_boundary_margin |       0.1648 |     0.2238 |      0.059 |            60 | weak_positive_candidate          | capacity_exceeds_fragmentation;m_edge_higher_than_before                                                                          |                0.39511  |                         0.686202 |                               0.300544 |                       0.480662   |                       0.466686   |                    0.254401  |                              0        |
| peak_positive  | peak_positive_window     |       0.1958 |     0.2038 |      0.008 |             9 | weak_positive_candidate          | capacity_exceeds_fragmentation                                                                                                    |                0.380088 |                         0.661968 |                               0.27958  |                       0.4501     |                       0.46828    |                    0.152519  |                              0        |
| positive_006   | positive_boundary_margin |       0.2348 |     0.2378 |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure                                                                         |                0.32547  |                         0.661547 |                               0.335419 |                       0.478314   |                       0.245585   |                    0.48601   |                              0        |
| positive_007   | positive_boundary_margin |       0.2478 |     0.2568 |      0.009 |            10 | weak_positive_candidate          | capacity_exceeds_fragmentation;m_edge_higher_than_before                                                                          |                0.298284 |                         0.625457 |                               0.329704 |                       0.40404    |                       0.372936   |                    0.351274  |                              0        |
| positive_008   | positive_boundary_margin |       0.2608 |     0.2708 |      0.01  |            11 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                               |                0.350337 |                         0.548707 |                               0.19963  |                       0.257079   |                       0.268958   |                    0.165907  |                              0        |
| positive_009   | positive_boundary_margin |       0.2728 |     0.2758 |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                               |                0.378178 |                         0.520706 |                               0.142143 |                       0.173682   |                       0.277843   |                    0.0427236 |                              0        |
| positive_010   | positive_boundary_margin |       0.2818 |     0.2868 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                               |                0.360867 |                         0.501767 |                               0.1471   |                       0.163065   |                       0.0792232  |                    0.233888  |                              0        |
| peak_negative  | peak_negative_window     |       0.3008 |     0.3088 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before                                                         |               -0.210068 |                         0.201831 |                               0.429403 |                       0.00867554 |                       0.427358   |                    0.0989566 |                              0.444444 |
| negative_001   | negative_leakage_margin  |       0.3028 |     0.3058 |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before                                                         |               -0.391152 |                         0.122741 |                               0.50897  |                       0.00119289 |                       0.523309   |                  nan         |                              0.444444 |
| negative_002   | negative_leakage_margin  |       0.3528 |     0.3578 |      0.005 |             6 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                                               |               -0.308816 |                         0.394641 |                               0.703457 |                       0.584148   |                       0.761015   |                  nan         |                              0.444444 |

## 6. Interpretability flags

```text
interpretable_positive_candidate: 8
weak_positive_candidate: 3
interpretable_negative_candidate: 3
```

## 7. Detailed window notes

### positive_001 — positive_boundary_margin

```text
time: 0.1047999908924104 → 0.1087999908924104 s
duration: 0.00399999999999999 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.3880293478731216 delta_before=0.232121242277669 trend=increase
C_edge_capacity: during=0.6930334192916561 delta_before=0.026599821074617225 trend=increase
F_route_fragmentation: during=0.298140238155764 delta_before=-0.21448988000471209 trend=decrease
S_edge_response: during=0.6803521474208024 delta_before=0.016739020347036004 trend=decrease
S_power_balance: during=0.0024522570170607 delta_before=-0.3540994771332929 trend=increase
S_transport: during=0.6455651526219143 delta_before=-0.08681593445923197 trend=decrease
dalpha_proxy: during=0.3710937499739113 delta_before=-0.12207031256656331 trend=increase
softx_lower_proxy: during=0.0022888183595799 delta_before=0.0004100799567287 trend=increase
softx_upper_proxy: during=0.0106048583990076 delta_before=-0.0007724761955708488 trend=decrease
te_profile_gradient_proxy: during=12.07924504560425 delta_before=-1.6083327348993368 trend=decrease
ne_profile_gradient_proxy: during=6.908363719987589e+17 delta_before=3.4296269240203776e+16 trend=increase
density_proxy: during=1.0876061158704416e+20 delta_before=3.4667997447963443e+18 trend=increase
nbi_proxy: during=-1.0981959104537964 delta_before=-1.0981959104537964 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.1117999908924104 → 0.1317999908924104 s
duration: 0.020000000000000004 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.4240586569506842 delta_before=0.13169892985710407 trend=decrease
C_edge_capacity: during=0.7359047272599593 delta_before=0.042871307968303185 trend=increase
F_route_fragmentation: during=0.3253095234114141 delta_before=-0.0715098630200639 trend=increase
S_edge_response: during=0.6731491049761271 delta_before=0.00021846747502640707 trend=decrease
S_power_balance: during=0.0131910107719494 delta_before=-0.2230646953427542 trend=increase
S_transport: during=0.6329379375383893 delta_before=-0.012627215083524934 trend=increase
dalpha_proxy: during=0.3857421874927697 delta_before=0.0073242187168302 trend=increase
softx_lower_proxy: during=0.0026512145989455 delta_before=0.0003814697258986998 trend=decrease
softx_upper_proxy: during=0.0105857849152889 delta_before=-0.0007057189902141998 trend=decrease
te_profile_gradient_proxy: during=10.75709484062617 delta_before=-1.3221502049780796 trend=increase
ne_profile_gradient_proxy: during=7.726351296969905e+17 delta_before=8.179875769823155e+16 trend=increase
density_proxy: during=1.1047780245902564e+20 delta_before=1.8811060654503363e+18 trend=increase
nbi_proxy: during=-1.0981959104537964 delta_before=-0.7320693731307983 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.1337999908924104 → 0.1367999908924104 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present

m_edge: during=0.22079704217299978 delta_before=-0.11703684283161309 trend=decrease
C_edge_capacity: during=0.7224547304953639 delta_before=-0.011630255882637663 trend=decrease
F_route_fragmentation: during=0.5002124509695562 delta_before=0.10910798710511915 trend=decrease
S_edge_response: during=0.603828228934097 delta_before=-0.047635060441148624 trend=decrease
S_power_balance: during=0.4789100239701167 delta_before=0.23274899622804113 trend=increase
S_transport: during=0.6376229328920533 delta_before=-0.012434704782498085 trend=decrease
dalpha_proxy: during=0.4003906250227717 delta_before=0.002441406283840708 trend=increase
softx_lower_proxy: during=0.002822875975875 delta_before=-6.675720341270007e-05 trend=decrease
softx_upper_proxy: during=0.0040721893311702 delta_before=-0.004186630248529649 trend=decrease
te_profile_gradient_proxy: during=11.133316550215852 delta_before=0.39534780750018683 trend=increase
ne_profile_gradient_proxy: during=7.475516226967145e+17 delta_before=-7.719988867560922e+16 trend=decrease
density_proxy: during=1.1332260407794257e+20 delta_before=9.855450485337457e+17 trend=increase
nbi_proxy: during=0.366126537322998 delta_before=0.732253074645996 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.1407999908924104 → 0.1597999908924104 s
duration: 0.01899999999999999 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.3606326488639259 delta_before=0.13830388329108148 trend=increase
C_edge_capacity: during=0.7647573593507034 delta_before=0.04278396591700018 trend=increase
F_route_fragmentation: during=0.4055186140876237 delta_before=-0.09461470711701503 trend=decrease
S_edge_response: during=0.5875133059571824 delta_before=-0.011818916455157868 trend=increase
S_power_balance: during=0.28077795567535835 delta_before=-0.20127595190472075 trend=decrease
S_transport: during=0.6055038969972198 delta_before=-0.01867148298730925 trend=decrease
dalpha_proxy: during=0.41503906251591405 delta_before=0.00976562506063744 trend=increase
softx_lower_proxy: during=0.0041198730445888496 delta_before=0.0012016296373408494 trend=increase
softx_upper_proxy: during=0.0014495849609706501 delta_before=-0.00234603881766635 trend=increase
te_profile_gradient_proxy: during=9.844273479148782 delta_before=-0.7612383276869856 trend=decrease
ne_profile_gradient_proxy: during=7.878682680200219e+17 delta_before=1.221948718052032e+16 trend=increase
density_proxy: during=1.2203793137402066e+20 delta_before=8.44420971890108e+18 trend=increase
nbi_proxy: during=-0.366126537322998 delta_before=-0.732253074645996 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_005 — positive_boundary_margin

```text
time: 0.1647999908924105 → 0.2237999908924105 s
duration: 0.059000000000000025 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation;m_edge_higher_than_before

m_edge: during=0.395109836312443 delta_before=0.020084977445742003 trend=decrease
C_edge_capacity: during=0.6862018445012559 delta_before=-0.08665531489228218 trend=decrease
F_route_fragmentation: during=0.3005444564456278 delta_before=-0.09817537546177363 trend=increase
S_edge_response: during=0.4806622728178357 delta_before=-0.11593838575056514 trend=decrease
S_power_balance: during=0.4666861821677132 delta_before=0.18852092854530555 trend=increase
S_transport: during=0.2544007518622545 delta_before=-0.3487452315581855 trend=decrease
dalpha_proxy: during=0.5468750000250824 delta_before=0.11840820314152906 trend=increase
softx_lower_proxy: during=0.00658988952431825 delta_before=0.0012207031270804504 trend=decrease
softx_upper_proxy: during=0.0082874298094766 delta_before=0.006084442138330449 trend=increase
te_profile_gradient_proxy: during=8.98906308858399 delta_before=-0.8552103905647925 trend=decrease
ne_profile_gradient_proxy: during=3.030222208367928e+17 delta_before=-5.0949915505661926e+17 trend=decrease
density_proxy: during=1.1129278246776576e+20 delta_before=-1.233046875164744e+19 trend=decrease
nbi_proxy: during=0.366126537322998 delta_before=0.732253074645996 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.1957999908924105 → 0.2037999908924105 s
duration: 0.00799999999999998 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation

m_edge: during=0.3800883111099311 delta_before=-0.0747824165499858 trend=decrease
C_edge_capacity: during=0.6619679402819303 delta_before=-0.018020106392436674 trend=increase
F_route_fragmentation: during=0.2795797219679509 delta_before=0.0414517126218204 trend=increase
S_edge_response: during=0.4500996748917954 delta_before=0.0025244100462130104 trend=increase
S_power_balance: during=0.4682798595267235 delta_before=0.21277236663482474 trend=increase
S_transport: during=0.1525193728462683 delta_before=0.01776704979628499 trend=decrease
dalpha_proxy: during=0.5371093750401155 delta_before=-0.1440429687001945 trend=decrease
softx_lower_proxy: during=0.0046157836902974 delta_before=-0.0020599365216062 trend=increase
softx_upper_proxy: during=0.0106430053697617 delta_before=-0.0008392333991732014 trend=increase
te_profile_gradient_proxy: during=7.191362335933086 delta_before=0.09451679880095654 trend=increase
ne_profile_gradient_proxy: during=2.485962401722421e+17 delta_before=-2.151178205924189e+16 trend=decrease
density_proxy: during=1.0822134951213164e+20 delta_before=-5.791805042658902e+18 trend=decrease
nbi_proxy: during=0.366126537322998 delta_before=0.732253074645996 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_006 — positive_boundary_margin

```text
time: 0.2347999908924105 → 0.2377999908924105 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure

m_edge: during=0.32546959901648753 delta_before=-0.014625316039492853 trend=decrease
C_edge_capacity: during=0.6615466448701658 delta_before=-0.00898517391816045 trend=decrease
F_route_fragmentation: during=0.3354187109594733 delta_before=0.004981807227127488 trend=increase
S_edge_response: during=0.4783142984722605 delta_before=0.0002965089310135727 trend=decrease
S_power_balance: during=0.2455852630254041 delta_before=0.0015291973215488808 trend=increase
S_transport: during=0.4860097253363683 delta_before=0.11851954355802263 trend=decrease
dalpha_proxy: during=0.5688476562783926 delta_before=0.012207031289532821 trend=increase
softx_lower_proxy: during=0.00575065612935225 delta_before=0.00018119812405604976 trend=decrease
softx_upper_proxy: during=0.00220298767116425 delta_before=-0.0007343292238021501 trend=increase
te_profile_gradient_proxy: during=13.875551232894548 delta_before=2.824948618362754 trend=decrease
ne_profile_gradient_proxy: during=2.3169316239307942e+17 delta_before=-3.261807526713875e+16 trend=increase
density_proxy: during=1.1249930296520344e+20 delta_before=1.3515284889552814e+18 trend=increase
nbi_proxy: during=-0.366126537322998 delta_before=0.0 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_007 — positive_boundary_margin

```text
time: 0.2477999908924105 → 0.2567999908924105 s
duration: 0.009000000000000008 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation;m_edge_higher_than_before

m_edge: during=0.2982840626630575 delta_before=0.1185222329857119 trend=increase
C_edge_capacity: during=0.6254569797711 delta_before=0.024280439781187324 trend=increase
F_route_fragmentation: during=0.329703634830565 delta_before=-0.09911165158287472 trend=decrease
S_edge_response: during=0.40404026235291285 delta_before=0.03365492903519035 trend=increase
S_power_balance: during=0.37293569149070616 delta_before=-0.3340410738365168 trend=decrease
S_transport: during=0.35127397274421346 delta_before=0.08687734189291518 trend=increase
dalpha_proxy: during=0.6408691405540627 delta_before=0.03784179682740019 trend=increase
softx_lower_proxy: during=0.00494956970214795 delta_before=0.0006961822510675496 trend=increase
softx_upper_proxy: during=0.0021553039573052497 delta_before=7.629394735624972e-05 trend=decrease
te_profile_gradient_proxy: during=9.995434449471185 delta_before=0.43989510118407793 trend=increase
ne_profile_gradient_proxy: during=3.492220003698107e+17 delta_before=9.927881698764352e+16 trend=increase
density_proxy: during=1.168054830807835e+20 delta_before=5.095770201811583e+18 trend=increase
nbi_proxy: during=0.0 delta_before=-1.0981959104537964 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_008 — positive_boundary_margin

```text
time: 0.2607999908924105 → 0.2707999908924106 s
duration: 0.010000000000000064 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3503369162670298 delta_before=0.10298184830569337 trend=decrease
C_edge_capacity: during=0.5487071506360591 delta_before=-0.07540485933270547 trend=decrease
F_route_fragmentation: during=0.1996297853087109 delta_before=-0.16329998741381951 trend=decrease
S_edge_response: during=0.25707900780704 delta_before=-0.1435922113830766 trend=decrease
S_power_balance: during=0.2689575295468203 delta_before=-0.22406618578225712 trend=increase
S_transport: during=0.1659074663433152 delta_before=-0.18344721434578387 trend=decrease
dalpha_proxy: during=0.7446289062251717 delta_before=0.092773437523473 trend=increase
softx_lower_proxy: during=0.0032806396471656 delta_before=-0.0015449523953458 trend=increase
softx_upper_proxy: during=0.0016784667975516 delta_before=-0.000438690188762 trend=increase
te_profile_gradient_proxy: during=7.352683048669178 delta_before=-2.8594333674543986 trend=decrease
ne_profile_gradient_proxy: during=2.067484154654884e+17 delta_before=-1.371595485798142e+17 trend=decrease
density_proxy: during=1.2063356915232748e+20 delta_before=2.1360608216990515e+18 trend=increase
nbi_proxy: during=-0.366126537322998 delta_before=-0.732253074645996 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_009 — positive_boundary_margin

```text
time: 0.2727999908924106 → 0.2757999908924106 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3781780341750671 delta_before=0.02784111790803734 trend=decrease
C_edge_capacity: during=0.5207061334644217 delta_before=-0.02206521869695688 trend=decrease
F_route_fragmentation: during=0.14214260647842597 delta_before=-0.057487178830284924 trend=increase
S_edge_response: during=0.17368208443826544 delta_before=-0.06643881059896417 trend=decrease
S_power_balance: during=0.27784316304037604 delta_before=0.008885633493555756 trend=increase
S_transport: during=0.042723580272830505 delta_before=-0.1144131952460961 trend=decrease
dalpha_proxy: during=0.8227539061413901 delta_before=0.05615234375372702 trend=increase
softx_lower_proxy: during=0.00285148620620675 delta_before=-0.0003337860114677499 trend=decrease
softx_upper_proxy: during=0.001077651980583 delta_before=-0.00039100646648570006 trend=decrease
te_profile_gradient_proxy: during=4.822834608089877 delta_before=-2.3002751990510975 trend=decrease
ne_profile_gradient_proxy: during=2.1150947779119475e+17 delta_before=1.6828926091133376e+16 trend=increase
density_proxy: during=1.237735192745581e+20 delta_before=2.84088295947554e+18 trend=increase
nbi_proxy: during=-0.366126537322998 delta_before=0.0 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_010 — positive_boundary_margin

```text
time: 0.2817999908924106 → 0.2867999908924106 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3608672371256413 delta_before=0.021291098492079497 trend=decrease
C_edge_capacity: during=0.5017673570710173 delta_before=-0.021921258817159672 trend=decrease
F_route_fragmentation: during=0.1471000765285887 delta_before=-0.05261416116463499 trend=increase
S_edge_response: during=0.16306474338511395 delta_before=-0.015607358598814847 trend=decrease
S_power_balance: during=0.07922321953002501 delta_before=-0.2056252999369874 trend=increase
S_transport: during=0.2338881581263659 delta_before=0.14177463288016862 trend=decrease
dalpha_proxy: during=0.9240722655928229 delta_before=0.07934570315746836 trend=increase
softx_lower_proxy: during=0.00163078308023425 delta_before=-0.0005626678453655499 trend=increase
softx_upper_proxy: during=0.0007534027109401 delta_before=-0.0002384185787354001 trend=increase
te_profile_gradient_proxy: during=7.11376685721091 delta_before=1.4526828190815504 trend=decrease
ne_profile_gradient_proxy: during=2.905788577713486e+17 delta_before=3.66819387580025e+16 trend=decrease
density_proxy: during=1.358005755934975e+20 delta_before=1.037568661104309e+19 trend=increase
nbi_proxy: during=-1.0981959104537964 delta_before=-0.7320693731307983 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### peak_negative — peak_negative_window

```text
time: 0.3007999908924106 → 0.3087999908924106 s
duration: 0.008000000000000007 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.2100675221423936 delta_before=-0.3228621325734363 trend=increase
C_edge_capacity: during=0.201830607751565 delta_before=-0.2373099422625218 trend=increase
F_route_fragmentation: during=0.4294034969756257 delta_before=0.12177190617764011 trend=decrease
S_edge_response: during=0.0086755350129231 delta_before=-0.08872170872662599 trend=increase
S_power_balance: during=0.4273579321979587 delta_before=-0.07852511819444874 trend=decrease
S_transport: during=0.0989565800919292 delta_before=-0.05118132290776639 trend=flat
dalpha_proxy: during=1.6601562500278777 delta_before=0.4760742187914846 trend=decrease
softx_lower_proxy: during=-0.0013351440449498 delta_before=-0.0023078918481068003 trend=decrease
softx_upper_proxy: during=-0.00244140625 delta_before=-0.0026035308819343 trend=increase
te_profile_gradient_proxy: during=5.966208986860806 delta_before=-0.7042194985719323 trend=flat
ne_profile_gradient_proxy: during=2.849288855508296e+17 delta_before=0.0 trend=flat
density_proxy: during=4.702186380704979e+19 delta_before=-9.37383184682755e+19 trend=decrease
nbi_proxy: during=-0.366126537322998 delta_before=-0.732253074645996 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=0.4444444444444444 trend=increase
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```