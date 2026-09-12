# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11823_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     476
time_min: -0.0670000091195106
time_max: 0.4079999908804897
```

State counts:

```text
boundary_ambiguous_margin: 218
positive_boundary_margin: 142
insufficient_data: 58
negative_leakage_margin: 58
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                 |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:-------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| positive_001   | positive_boundary_margin |        0.152 |      0.159 |      0.007 |             8 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present;m_edge_higher_than_before |                0.236397 |                         0.686959 |                               0.449212 |                        0.640515  |                         0.366251 |                     0.631238 |                              0        |
| positive_002   | positive_boundary_margin |        0.161 |      0.165 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present;m_edge_higher_than_before |                0.238997 |                         0.679404 |                               0.453645 |                        0.593529  |                         0.359807 |                     0.65223  |                              0        |
| positive_003   | positive_boundary_margin |        0.167 |      0.176 |      0.009 |            10 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present                           |                0.230448 |                         0.711503 |                               0.482688 |                        0.59837   |                         0.373114 |                     0.701421 |                              0        |
| positive_004   | positive_boundary_margin |        0.178 |      0.182 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present;m_edge_higher_than_before |                0.239847 |                         0.726464 |                               0.482314 |                        0.593306  |                         0.362383 |                     0.709426 |                              0        |
| positive_005   | positive_boundary_margin |        0.188 |      0.195 |      0.007 |             8 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present;m_edge_higher_than_before |                0.283604 |                         0.722588 |                               0.426112 |                        0.566779  |                         0.385433 |                     0.576401 |                              0        |
| positive_006   | positive_boundary_margin |        0.197 |      0.201 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.37245  |                         0.701757 |                               0.333766 |                        0.519839  |                         0.222312 |                     0.519391 |                              0        |
| peak_positive  | peak_positive_window     |        0.213 |      0.221 |      0.008 |             9 | weak_positive_candidate          | capacity_exceeds_fragmentation;m_edge_higher_than_before                                               |                0.328196 |                         0.66793  |                               0.336614 |                        0.456185  |                         0.426065 |                     0.321965 |                              0        |
| positive_007   | positive_boundary_margin |        0.215 |      0.218 |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.370457 |                         0.666062 |                               0.292934 |                        0.448002  |                         0.329    |                     0.321965 |                              0        |
| positive_008   | positive_boundary_margin |        0.222 |      0.225 |      0.003 |             4 | weak_positive_candidate          | capacity_exceeds_fragmentation                                                                         |                0.31218  |                         0.64775  |                               0.33568  |                        0.451292  |                         0.423991 |                     0.321965 |                              0        |
| positive_009   | positive_boundary_margin |        0.228 |      0.237 |      0.009 |            10 | weak_positive_candidate          | capacity_exceeds_fragmentation;m_edge_higher_than_before                                               |                0.309145 |                         0.641951 |                               0.344765 |                        0.439313  |                         0.434907 |                     0.355898 |                              0        |
| positive_010   | positive_boundary_margin |        0.239 |      0.243 |      0.004 |             5 | weak_positive_candidate          | capacity_exceeds_fragmentation                                                                         |                0.262355 |                         0.610683 |                               0.363106 |                        0.419685  |                         0.439939 |                     0.366964 |                              0        |
| positive_011   | positive_boundary_margin |        0.245 |      0.267 |      0.022 |            23 | weak_positive_candidate          | capacity_exceeds_fragmentation                                                                         |                0.244702 |                         0.61182  |                               0.372304 |                        0.422299  |                         0.457148 |                     0.370194 |                              0        |
| peak_negative  | peak_negative_window     |        0.338 |      0.346 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before                              |               -0.342926 |                         0.183432 |                               0.502625 |                        0.0708556 |                         0.515553 |                   nan        |                              0.444444 |
| negative_001   | negative_leakage_margin  |        0.34  |      0.349 |      0.009 |            10 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before  |               -0.316568 |                         0.195741 |                               0.587681 |                        0.244436  |                         0.619511 |                   nan        |                              0.444444 |
| negative_002   | negative_leakage_margin  |        0.353 |      0.356 |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.366563 |                         0.383403 |                               0.749792 |                        0.570847  |                         0.817647 |                   nan        |                              0.444444 |
| negative_003   | negative_leakage_margin  |        0.358 |      0.362 |      0.004 |             5 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high                                             |               -0.221    |                         0.388006 |                               0.609436 |                        0.577552  |                         0.646101 |                   nan        |                              0.444444 |
| negative_004   | negative_leakage_margin  |        0.365 |      0.374 |      0.009 |            10 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.222475 |                         0.389432 |                               0.611144 |                        0.583241  |                         0.648189 |                   nan        |                              0.444444 |
| negative_005   | negative_leakage_margin  |        0.383 |      0.387 |      0.004 |             5 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.218438 |                         0.392416 |                               0.61174  |                        0.586424  |                         0.648917 |                   nan        |                              0.444444 |
| negative_006   | negative_leakage_margin  |        0.389 |      0.394 |      0.005 |             6 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.21555  |                         0.395037 |                               0.611617 |                        0.591104  |                         0.648766 |                   nan        |                              0.444444 |
| negative_007   | negative_leakage_margin  |        0.4   |      0.403 |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high                                             |               -0.20929  |                         0.402093 |                               0.611993 |                        0.601586  |                         0.649225 |                   nan        |                              0.444444 |

## 6. Interpretability flags

```text
interpretable_negative_candidate: 8
interpretable_positive_candidate: 7
weak_positive_candidate: 5
```

## 7. Detailed window notes

### positive_001 — positive_boundary_margin

```text
time: 0.1519999908804895 → 0.1589999908804895 s
duration: 0.007000000000000006 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.23639659998664714 delta_before=0.08409371793243653 trend=increase
C_edge_capacity: during=0.6869594582191143 delta_before=0.03852248894787402 trend=increase
F_route_fragmentation: during=0.44921167446135857 delta_before=-0.05959563506829979 trend=decrease
S_edge_response: during=0.64051516605568 delta_before=-0.031362002350824314 trend=increase
S_power_balance: during=0.36625147303896755 delta_before=7.689084914985767e-05 trend=increase
S_transport: during=0.631237922726338 delta_before=-0.1430651338387321 trend=decrease
dalpha_proxy: during=0.4553222656539211 delta_before=-0.006103515628726908 trend=decrease
softx_lower_proxy: during=0.0003194808964828 delta_before=-5.245208844599996e-05 trend=increase
softx_upper_proxy: during=0.0034713745093566 delta_before=-0.00015258789416549992 trend=decrease
te_profile_gradient_proxy: during=8.01688669449507 delta_before=-2.133359295054831 trend=decrease
ne_profile_gradient_proxy: during=5.734680892592934e+16 delta_before=-584257787369088.0 trend=decrease
density_proxy: during=1.587744312512259e+20 delta_before=-9.575514824905851e+17 trend=increase
nbi_proxy: during=0.0585771463811397 delta_before=0.0 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.1609999908804895 → 0.1649999908804895 s
duration: 0.0040000000000000036 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.23899685250591 delta_before=0.004825330739565287 trend=decrease
C_edge_capacity: during=0.6794044461090538 delta_before=-0.005792635476752017 trend=increase
F_route_fragmentation: during=0.4536445218842324 delta_before=0.004313625063010196 trend=increase
S_edge_response: during=0.5935291446980125 delta_before=-0.04592705230802341 trend=increase
S_power_balance: during=0.3598070626463638 delta_before=-0.0065213012417535965 trend=increase
S_transport: during=0.6522295361015014 delta_before=0.01830702456862121 trend=increase
dalpha_proxy: during=0.48828125 delta_before=0.026855468717352005 trend=increase
softx_lower_proxy: during=0.0002956390373124 delta_before=-7.629394761639996e-05 trend=decrease
softx_upper_proxy: during=0.0016212463411435 delta_before=-0.0014305114698497001 trend=increase
te_profile_gradient_proxy: during=8.01688669449507 delta_before=0.0 trend=flat
ne_profile_gradient_proxy: during=5.734680892592934e+16 delta_before=0.0 trend=flat
density_proxy: during=1.571173616750512e+20 delta_before=-1.689571139891757e+18 trend=decrease
nbi_proxy: during=0.0585771463811397 delta_before=0.0 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.1669999908804895 → 0.1759999908804895 s
duration: 0.009000000000000008 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present

m_edge: during=0.2304476231279644 delta_before=-0.008295450835020701 trend=increase
C_edge_capacity: during=0.7115033562901978 delta_before=0.026306274704391952 trend=increase
F_route_fragmentation: during=0.48268754195854374 delta_before=0.029043020074311365 trend=increase
S_edge_response: during=0.5983704740547574 delta_before=-0.002135895292624701 trend=increase
S_power_balance: during=0.373113653577047 delta_before=0.007432587863125895 trend=increase
S_transport: during=0.7014205636106208 delta_before=0.05529336903199311 trend=increase
dalpha_proxy: during=0.5017089844063809 delta_before=0.013427734526910318 trend=increase
softx_lower_proxy: during=0.00025272369585145 delta_before=-0.00024318694759424997 trend=increase
softx_upper_proxy: during=0.0030899047834342 delta_before=0.0011253356906591 trend=increase
te_profile_gradient_proxy: during=6.995592342719124 delta_before=-1.0212943517759472 trend=decrease
ne_profile_gradient_proxy: during=6.531861500204514e+16 delta_before=7971806076115792.0 trend=increase
density_proxy: during=1.6202413902218763e+20 delta_before=3.490817476793467e+18 trend=increase
nbi_proxy: during=0.0585771463811397 delta_before=0.0 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.1779999908804895 → 0.1819999908804895 s
duration: 0.003999999999999976 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.2398468267409116 delta_before=0.0107372189868995 trend=increase
C_edge_capacity: during=0.7264641669277272 delta_before=0.010084365866604994 trend=increase
F_route_fragmentation: during=0.4823140718638236 delta_before=-0.00140112203767212 trend=decrease
S_edge_response: during=0.5933057897535867 delta_before=-0.005946895465208324 trend=increase
S_power_balance: during=0.3623830621636197 delta_before=-0.0115859006642412 trend=decrease
S_transport: during=0.7094259864226549 delta_before=0.0 trend=flat
dalpha_proxy: during=0.539550781204345 delta_before=0.026855468658876225 trend=increase
softx_lower_proxy: during=-3.814697251357789e-05 delta_before=-0.0002956390389870779 trend=increase
softx_upper_proxy: during=0.0042343139654214 delta_before=0.0010681152362314998 trend=increase
te_profile_gradient_proxy: during=6.557894763386713 delta_before=0.0 trend=flat
ne_profile_gradient_proxy: during=6.873510332037939e+16 delta_before=0.0 trend=flat
density_proxy: during=1.6732176196667284e+20 delta_before=5.310078212204659e+18 trend=increase
nbi_proxy: during=0.0585771463811397 delta_before=0.0 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_005 — positive_boundary_margin

```text
time: 0.1879999908804895 → 0.1949999908804895 s
duration: 0.007000000000000006 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.28360421783828726 delta_before=0.04080609623473386 trend=increase
C_edge_capacity: during=0.7225876760269334 delta_before=-0.013130591443430983 trend=decrease
F_route_fragmentation: during=0.4261124915789234 delta_before=-0.06703065441353351 trend=decrease
S_edge_response: during=0.5667793818609408 delta_before=-0.03894715665992088 trend=decrease
S_power_balance: during=0.3854326913201511 delta_before=-0.0010149800182094881 trend=increase
S_transport: during=0.576401392519578 delta_before=-0.13302459390307686 trend=decrease
dalpha_proxy: during=0.5786132812168979 delta_before=0.024414062514230173 trend=decrease
softx_lower_proxy: during=0.000190734862835 delta_before=1.9073486364399992e-05 trend=decrease
softx_upper_proxy: during=0.004606246950824599 delta_before=0.00018119812180899912 trend=decrease
te_profile_gradient_proxy: during=6.403897154450555 delta_before=-0.15399760893615788 trend=decrease
ne_profile_gradient_proxy: during=4.640930965528435e+16 delta_before=-2.232579366509504e+16 trend=decrease
density_proxy: during=1.676300914153803e+20 delta_before=8.427624685507707e+17 trend=increase
nbi_proxy: during=0.0585771463811397 delta_before=0.0 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_006 — positive_boundary_margin

```text
time: 0.1969999908804895 → 0.2009999908804896 s
duration: 0.004000000000000087 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3724502255038842 delta_before=0.09286518496722007 trend=increase
C_edge_capacity: during=0.7017569995175369 delta_before=-0.018742113288253814 trend=decrease
F_route_fragmentation: during=0.333766190803788 delta_before=-0.1071478814653386 trend=decrease
S_edge_response: during=0.5198385375074293 delta_before=-0.04112421252889731 trend=decrease
S_power_balance: during=0.2223117939552197 delta_before=-0.1641494451324361 trend=decrease
S_transport: during=0.5193908522754203 delta_before=-0.03800702682943424 trend=flat
dalpha_proxy: during=0.5712890624802404 delta_before=-0.0073242186842567 trend=increase
softx_lower_proxy: during=6.994374426427113e-13 delta_before=-0.00017166137640156257 trend=decrease
softx_upper_proxy: during=0.004749298092244 delta_before=5.722045073599993e-05 trend=decrease
te_profile_gradient_proxy: during=6.337898179192223 delta_before=-0.04399931683888347 trend=flat
ne_profile_gradient_proxy: during=3.684111237024666e+16 delta_before=-6378798190024424.0 trend=flat
density_proxy: during=1.6933525802820043e+20 delta_before=1.3921224582527713e+18 trend=decrease
nbi_proxy: during=-0.234308585524559 delta_before=-0.29288573190569867 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.2129999908804896 → 0.2209999908804896 s
duration: 0.008000000000000007 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation;m_edge_higher_than_before

m_edge: during=0.3281963416918098 delta_before=0.06071932501482946 trend=decrease
C_edge_capacity: during=0.6679302815598145 delta_before=-0.01228140697093949 trend=decrease
F_route_fragmentation: during=0.3366135291479396 delta_before=-0.08035829206856387 trend=increase
S_edge_response: during=0.4561848369737906 delta_before=-0.038622897276667234 trend=decrease
S_power_balance: during=0.4260647917596292 delta_before=0.017562993655124204 trend=increase
S_transport: during=0.3219652730135698 delta_before=-0.19742557926183313 trend=flat
dalpha_proxy: during=0.6079101562710877 delta_before=0.019531250021087687 trend=increase
softx_lower_proxy: during=0.0001239776610911 delta_before=0.00012397766182198352 trend=decrease
softx_upper_proxy: during=0.0041580200197818 delta_before=-0.0003623962386320005 trend=decrease
te_profile_gradient_proxy: during=2.372902798279304 delta_before=-3.964995380912611 trend=flat
ne_profile_gradient_proxy: during=5.342967384695104e+16 delta_before=1.6588561476703104e+16 trend=flat
density_proxy: during=1.8015489225016735e+20 delta_before=5.852533268884193e+18 trend=increase
nbi_proxy: during=0.0585771463811397 delta_before=0.0 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_007 — positive_boundary_margin

```text
time: 0.2149999908804896 → 0.2179999908804896 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.37045669336787856 delta_before=0.10221742466075978 trend=increase
C_edge_capacity: during=0.6660618874333344 delta_before=-0.013590131289202723 trend=decrease
F_route_fragmentation: during=0.2929343332659906 delta_before=-0.1223798669088621 trend=decrease
S_edge_response: during=0.4480018690805079 delta_before=-0.03651766906698273 trend=increase
S_power_balance: during=0.32899991202196477 delta_before=-0.07950188608254022 trend=decrease
S_transport: during=0.3219652730135698 delta_before=-0.10859854235167021 trend=flat
dalpha_proxy: during=0.6091308594331741 delta_before=0.020751953121699862 trend=decrease
softx_lower_proxy: during=0.00010490417462413903 delta_before=0.00010490417535502256 trend=increase
softx_upper_proxy: during=0.004024505615981101 delta_before=-0.0004959106424326995 trend=decrease
te_profile_gradient_proxy: during=2.372902798279304 delta_before=-2.378997228547443 trend=flat
ne_profile_gradient_proxy: during=5.342967384695104e+16 delta_before=9953136886021344.0 trend=flat
density_proxy: during=1.8001518390469565e+20 delta_before=5.483387633021223e+18 trend=decrease
nbi_proxy: during=-0.08786571957170965 delta_before=-0.14644286595284933 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_008 — positive_boundary_margin

```text
time: 0.2219999908804896 → 0.2249999908804896 s
duration: 0.0030000000000000027 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation

m_edge: during=0.3121798930417955 delta_before=-0.01601644865001428 trend=increase
C_edge_capacity: during=0.6477495698261536 delta_before=-0.020180711733660872 trend=increase
F_route_fragmentation: during=0.3356803915830897 delta_before=-0.0009331375648499174 trend=increase
S_edge_response: during=0.451292273158234 delta_before=-0.004892563815556583 trend=increase
S_power_balance: during=0.42399115272662946 delta_before=0.0037744771018533574 trend=increase
S_transport: during=0.3219652730135698 delta_before=0.0 trend=flat
dalpha_proxy: during=0.6103515625107911 delta_before=0.0048828124789156435 trend=increase
softx_lower_proxy: during=0.00016212463332075 delta_before=0.00014305114556034524 trend=increase
softx_upper_proxy: during=0.00448226928583695 delta_before=0.00024795531928784986 trend=decrease
te_profile_gradient_proxy: during=2.372902798279304 delta_before=0.0 trend=flat
ne_profile_gradient_proxy: during=5.342967384695104e+16 delta_before=0.0 trend=flat
density_proxy: during=1.837139410205341e+20 delta_before=3.559048770366767e+18 trend=increase
nbi_proxy: during=0.0585771463811397 delta_before=0.0 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_009 — positive_boundary_margin

```text
time: 0.2279999908804896 → 0.2369999908804896 s
duration: 0.00899999999999998 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation;m_edge_higher_than_before

m_edge: during=0.3091446027200103 delta_before=0.0007646620096721235 trend=decrease
C_edge_capacity: during=0.6419514552860868 delta_before=-0.010647013058057708 trend=increase
F_route_fragmentation: during=0.3447654233162375 delta_before=0.00618156355765398 trend=increase
S_edge_response: during=0.43931269484803026 delta_before=-0.012862133514782714 trend=increase
S_power_balance: during=0.43490715617413667 delta_before=0.004463851946409858 trend=increase
S_transport: during=0.3558977126161253 delta_before=0.033932439602555486 trend=increase
dalpha_proxy: during=0.6616210937339402 delta_before=0.04638671871262201 trend=increase
softx_lower_proxy: during=0.00011444091764010607 delta_before=-9.536743450993922e-06 trend=increase
softx_upper_proxy: during=0.00407218933210125 delta_before=-0.0002384185772222507 trend=decrease
te_profile_gradient_proxy: during=4.0394942733377235 delta_before=1.6665914750584196 trend=increase
ne_profile_gradient_proxy: during=4.110727606571843e+16 delta_before=-1.2322397781232608e+16 trend=decrease
density_proxy: during=1.887532666934222e+20 delta_before=6.631638412233277e+18 trend=increase
nbi_proxy: during=0.0585771463811397 delta_before=0.0 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_010 — positive_boundary_margin

```text
time: 0.2389999908804896 → 0.2429999908804896 s
duration: 0.0040000000000000036 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation

m_edge: during=0.2623554030193638 delta_before=-0.025789950261089933 trend=decrease
C_edge_capacity: during=0.6106833169178263 delta_before=-0.025594297125782317 trend=decrease
F_route_fragmentation: during=0.3631060016289897 delta_before=0.0022547788908059974 trend=decrease
S_edge_response: during=0.4196852708238304 delta_before=-0.020780031721300718 trend=decrease
S_power_balance: during=0.4399386477912121 delta_before=0.002732444822779123 trend=decrease
S_transport: during=0.3669635780509873 delta_before=0.0 trend=flat
dalpha_proxy: during=0.6860351562037859 delta_before=0.019531250053437588 trend=increase
softx_lower_proxy: during=7.62939453125e-05 delta_before=3.968878719597113e-13 trend=increase
softx_upper_proxy: during=0.0037574768084342 delta_before=-0.0004386901841928999 trend=decrease
te_profile_gradient_proxy: during=4.224671103899681 delta_before=0.0 trend=flat
ne_profile_gradient_proxy: during=3.973812075669325e+16 delta_before=0.0 trend=flat
density_proxy: during=1.9077269132164678e+20 delta_before=2.0026768671103058e+18 trend=decrease
nbi_proxy: during=0.0585771463811397 delta_before=0.0 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_011 — positive_boundary_margin

```text
time: 0.2449999908804896 → 0.2669999908804896 s
duration: 0.021999999999999992 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation

m_edge: during=0.244702408115116 delta_before=-0.016724425868555715 trend=decrease
C_edge_capacity: during=0.6118198408812261 delta_before=-0.008365061898856663 trend=decrease
F_route_fragmentation: during=0.3723040215935011 delta_before=0.008631464465223448 trend=increase
S_edge_response: during=0.4222988112440735 delta_before=-0.006437997665920903 trend=decrease
S_power_balance: during=0.4571483805383071 delta_before=0.015950720526454965 trend=increase
S_transport: during=0.3701938896694731 delta_before=0.003230311618485804 trend=increase
dalpha_proxy: during=0.6933593749879654 delta_before=0.02929687497652711 trend=increase
softx_lower_proxy: during=0.0001239776614528 delta_before=4.768371653718787e-05 trend=increase
softx_upper_proxy: during=0.0040245056160102 delta_before=0.00022888183426919952 trend=increase
te_profile_gradient_proxy: during=3.162695900563577 delta_before=-1.0619752033361038 trend=decrease
ne_profile_gradient_proxy: during=4.692542426350387e+16 delta_before=7187303506810624.0 trend=increase
density_proxy: during=1.9843144951608325e+20 delta_before=7.658758194436473e+18 trend=increase
nbi_proxy: during=0.0585771463811397 delta_before=0.0 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```