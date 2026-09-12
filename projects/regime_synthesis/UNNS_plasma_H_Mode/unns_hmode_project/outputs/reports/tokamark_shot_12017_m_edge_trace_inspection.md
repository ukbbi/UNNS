# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12017_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     546
time_min: -0.0692000091075897
time_max: 0.4757999908924107
```

State counts:

```text
boundary_ambiguous_margin: 271
positive_boundary_margin: 161
insufficient_data: 60
negative_leakage_margin: 54
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                            |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:----------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| positive_001   | positive_boundary_margin |       0.1378 |     0.1418 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                               |               0.283828  |                         0.576603 |                               0.290168 |                         0.51758  |                        0.235986  |                     0.408833 |                              0        |
| positive_002   | positive_boundary_margin |       0.1738 |     0.1788 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before |               0.319192  |                         0.675871 |                               0.34072  |                         0.623214 |                        0.199975  |                     0.562189 |                              0        |
| positive_003   | positive_boundary_margin |       0.1838 |     0.1978 |      0.014 |            15 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                            |               0.379826  |                         0.684088 |                               0.290449 |                         0.639652 |                        0.205945  |                     0.353729 |                              0        |
| peak_positive  | peak_positive_window     |       0.1888 |     0.1968 |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                            |               0.430705  |                         0.692381 |                               0.282391 |                         0.651472 |                        0.205945  |                     0.353729 |                              0        |
| positive_004   | positive_boundary_margin |       0.2028 |     0.2078 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                            |               0.470419  |                         0.665412 |                               0.184398 |                         0.608508 |                        0.199975  |                     0.287691 |                              0        |
| positive_005   | positive_boundary_margin |       0.2098 |     0.2148 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present                           |               0.33798   |                         0.729521 |                               0.392565 |                         0.729001 |                        0.206403  |                     0.663099 |                              0        |
| positive_006   | positive_boundary_margin |       0.2258 |     0.2328 |      0.007 |             8 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                            |               0.366005  |                         0.674933 |                               0.312229 |                         0.606013 |                        0.219363  |                     0.467008 |                              0        |
| positive_007   | positive_boundary_margin |       0.2408 |     0.2458 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high                                                                                 |               0.284011  |                         0.658605 |                               0.365266 |                         0.568475 |                        0.384874  |                     0.467151 |                              0        |
| positive_008   | positive_boundary_margin |       0.2478 |     0.2528 |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before |               0.308259  |                         0.678203 |                               0.393639 |                         0.593758 |                        0.248705  |                     0.62323  |                              0        |
| positive_009   | positive_boundary_margin |       0.2648 |     0.2678 |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                               |               0.387299  |                         0.585835 |                               0.205091 |                         0.404641 |                        0.16507   |                     0.280289 |                              0        |
| positive_010   | positive_boundary_margin |       0.2698 |     0.2728 |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                               |               0.334502  |                         0.593703 |                               0.250268 |                         0.410769 |                        0.277392  |                     0.269024 |                              0        |
| positive_011   | positive_boundary_margin |       0.2758 |     0.2798 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                               |               0.391849  |                         0.600241 |                               0.208393 |                         0.416603 |                        0.0857124 |                     0.359575 |                              0        |
| positive_012   | positive_boundary_margin |       0.2908 |     0.2938 |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                               |               0.255289  |                         0.56586  |                               0.310571 |                         0.325802 |                        0.317667  |                     0.372491 |                              0        |
| positive_013   | positive_boundary_margin |       0.3338 |     0.3388 |      0.005 |             6 | weak_positive_candidate          | capacity_exceeds_fragmentation;m_edge_higher_than_before                                                                          |               0.247493  |                         0.50597  |                               0.266218 |                         0.198659 |                        0.395786  |                     0.196556 |                              0        |
| positive_014   | positive_boundary_margin |       0.3418 |     0.3448 |      0.003 |             4 | weak_positive_candidate          | capacity_exceeds_fragmentation;m_edge_higher_than_before                                                                          |               0.235134  |                         0.551943 |                               0.319271 |                         0.277349 |                        0.392275  |                     0.314956 |                              0        |
| negative_001   | negative_leakage_margin  |       0.3928 |     0.3958 |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before                             |              -0.220465  |                         0.383774 |                               0.611648 |                         0.256261 |                        0.789104  |                     0.574228 |                              0        |
| negative_002   | negative_leakage_margin  |       0.4428 |     0.4458 |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                                               |              -0.336368  |                         0.380848 |                               0.718087 |                         0.570789 |                        0.778897  |                   nan        |                              0.444444 |
| negative_003   | negative_leakage_margin  |       0.4478 |     0.4528 |      0.005 |             6 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high                                                                        |              -0.334945  |                         0.382393 |                               0.71701  |                         0.572002 |                        0.77758   |                   nan        |                              0.444444 |
| peak_negative  | peak_negative_window     |       0.4658 |     0.4738 |      0.008 |             9 | weak_negative_candidate          | fragmentation_exceeds_capacity;m_edge_lower_than_before                                                                           |              -0.0920659 |                         0.38421  |                               0.474236 |                         0.576314 |                        0.480857  |                   nan        |                              0.444444 |

## 6. Interpretability flags

```text
interpretable_positive_candidate: 13
interpretable_negative_candidate: 3
weak_positive_candidate: 2
weak_negative_candidate: 1
```

## 7. Detailed window notes

### positive_001 — positive_boundary_margin

```text
time: 0.1377999908924104 → 0.1417999908924104 s
duration: 0.0040000000000000036 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.2838279793150526 delta_before=0.1830261075762225 trend=increase
C_edge_capacity: during=0.5766032355628499 delta_before=-0.026094039395504587 trend=decrease
F_route_fragmentation: during=0.2901684379884711 delta_before=-0.2152835393902907 trend=decrease
S_edge_response: during=0.5175800282394758 delta_before=-0.06610185267077173 trend=decrease
S_power_balance: during=0.2359856099517105 delta_before=-0.2947448834389136 trend=increase
S_transport: during=0.4088331411337809 delta_before=-0.195557141223065 trend=decrease
dalpha_proxy: during=0.3613281250465123 delta_before=0.004882812509242884 trend=increase
softx_lower_proxy: during=0.0053024291986736 delta_before=0.0014495849593180003 trend=increase
softx_upper_proxy: during=0.0025367736810876 delta_before=-0.0012207031260797001 trend=increase
te_profile_gradient_proxy: during=10.635695512011234 delta_before=-0.8808291518148419 trend=increase
ne_profile_gradient_proxy: during=4.050252575595872e+17 delta_before=-2.322962404519973e+17 trend=decrease
density_proxy: during=1.0537078205423863e+20 delta_before=8.580588743163904e+16 trend=decrease
nbi_proxy: during=-0.4393558800220489 delta_before=-0.8787117600440978 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.1737999908924105 → 0.1787999908924105 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.31919227441871934 delta_before=0.0774551320325787 trend=decrease
C_edge_capacity: during=0.6758705926529289 delta_before=0.0031783523884598708 trend=increase
F_route_fragmentation: during=0.34071954015419537 delta_before=-0.09182812985569988 trend=increase
S_edge_response: during=0.6232137335074737 delta_before=-0.008002679931192525 trend=increase
S_power_balance: during=0.19997474631172 delta_before=-0.15002525368827999 trend=increase
S_transport: during=0.5621888103511801 delta_before=-0.04061974033491367 trend=increase
dalpha_proxy: during=0.54199218745878 delta_before=0.08300781246315914 trend=increase
softx_lower_proxy: during=0.01179695129473345 delta_before=0.0020694732665535003 trend=increase
softx_upper_proxy: during=0.006570816038701801 delta_before=0.0018215179429713502 trend=increase
te_profile_gradient_proxy: during=15.901467525867197 delta_before=-1.589937839212439 trend=increase
ne_profile_gradient_proxy: during=4.447532552826071e+17 delta_before=-1.2270970439331584e+16 trend=decrease
density_proxy: during=1.2742537562240215e+20 delta_before=2.817969137152688e+18 trend=increase
nbi_proxy: during=-0.4393558800220489 delta_before=-0.4393558800220489 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.1837999908924105 → 0.1977999908924105 s
duration: 0.013999999999999985 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3798258549342294 delta_before=0.06431989893394846 trend=decrease
C_edge_capacity: during=0.684087773190869 delta_before=0.0006608679744785073 trend=increase
F_route_fragmentation: during=0.2904492476325361 delta_before=-0.06362927361173332 trend=increase
S_edge_response: during=0.6396518308439848 delta_before=0.005918970836094939 trend=increase
S_power_balance: during=0.2059452739902135 delta_before=0.005970527678493515 trend=increase
S_transport: during=0.3537293386390059 delta_before=-0.21343603952235213 trend=decrease
dalpha_proxy: during=0.4418945312693801 delta_before=-0.10009765619364858 trend=decrease
softx_lower_proxy: during=0.0108718872084806 delta_before=0.0007629394535756985 trend=increase
softx_upper_proxy: during=0.0149917602545118 delta_before=0.0073623657235541 trend=increase
te_profile_gradient_proxy: during=11.937718814862 delta_before=-4.403584015935911 trend=decrease
ne_profile_gradient_proxy: during=3.370771758565192e+17 delta_before=-1.0719226149449562e+17 trend=increase
density_proxy: during=1.3017158623267966e+20 delta_before=8.589824640837222e+17 trend=decrease
nbi_proxy: during=-0.4393558800220489 delta_before=0.0 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.1887999908924105 → 0.1967999908924105 s
duration: 0.00799999999999998 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4307045084088724 delta_before=0.16057916350778134 trend=increase
C_edge_capacity: during=0.6923809380260894 delta_before=0.008954032809698864 trend=decrease
F_route_fragmentation: during=0.2823907385422982 delta_before=-0.10856976690143383 trend=decrease
S_edge_response: during=0.6514724323576586 delta_before=0.01773957234976875 trend=decrease
S_power_balance: during=0.2059452739902135 delta_before=-0.2941092661320683 trend=increase
S_transport: during=0.3537293386390059 delta_before=-0.09131712561880678 trend=decrease
dalpha_proxy: during=0.4370117187796394 delta_before=-0.11718749999820088 trend=decrease
softx_lower_proxy: during=0.0111007690404425 delta_before=0.0010871887187614004 trend=increase
softx_upper_proxy: during=0.0153160095212563 delta_before=0.002841949461852001 trend=increase
te_profile_gradient_proxy: during=11.09109758260754 delta_before=-3.57228421906842 trend=decrease
ne_profile_gradient_proxy: during=3.427565379519435e+17 delta_before=5679362095424320.0 trend=increase
density_proxy: during=1.3113231310475126e+20 delta_before=1.5331062372127212e+18 trend=increase
nbi_proxy: during=-0.4393558800220489 delta_before=-0.8787117600440978 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.2027999908924105 → 0.2077999908924105 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4704189778464527 delta_before=0.05239212212109251 trend=increase
C_edge_capacity: during=0.6654115310951372 delta_before=-0.022871650212343386 trend=increase
F_route_fragmentation: during=0.1843983248364559 delta_before=-0.07453947763984009 trend=decrease
S_edge_response: during=0.6085077679069977 delta_before=-0.04296466445066094 trend=increase
S_power_balance: during=0.19997474631172 delta_before=-0.005970527678493515 trend=decrease
S_transport: during=0.2876908719938849 delta_before=-0.07167707597929773 trend=decrease
dalpha_proxy: during=0.44067382810952294 delta_before=0.008544921888816726 trend=decrease
softx_lower_proxy: during=0.01170158386400225 delta_before=0.0006008148235597498 trend=increase
softx_upper_proxy: during=0.0148963928236186 delta_before=-0.0008010864238106995 trend=decrease
te_profile_gradient_proxy: during=7.725331067375817 delta_before=-1.7111021183285962 trend=increase
ne_profile_gradient_proxy: during=3.205213971471464e+17 delta_before=-7.470524556094534e+16 trend=decrease
density_proxy: during=1.2976340793403061e+20 delta_before=-3.4299924935448986e+17 trend=increase
nbi_proxy: during=-0.4393558800220489 delta_before=0.0 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_005 — positive_boundary_margin

```text
time: 0.2097999908924105 → 0.2147999908924105 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present

m_edge: during=0.33798006008502157 delta_before=-0.1253018843644813 trend=increase
C_edge_capacity: during=0.7295213133258807 delta_before=0.04581878648513693 trend=increase
F_route_fragmentation: during=0.39256533858594256 delta_before=0.17861226200703767 trend=decrease
S_edge_response: during=0.7290013232969168 delta_before=0.0938806472133984 trend=increase
S_power_balance: during=0.2064025897922716 delta_before=0.006427843480551615 trend=decrease
S_transport: during=0.6630993249553163 delta_before=0.2879525050764393 trend=increase
dalpha_proxy: during=0.44555664067765155 delta_before=0.006103515728880127 trend=flat
softx_lower_proxy: during=0.0109195709243112 delta_before=-0.0005054473837985997 trend=decrease
softx_upper_proxy: during=0.012521743774167201 delta_before=-0.0023555755651098985 trend=decrease
te_profile_gradient_proxy: during=16.40189584198515 delta_before=6.723025047695739 trend=increase
ne_profile_gradient_proxy: during=4.8670678555905434e+17 delta_before=9.098331106662854e+16 trend=decrease
density_proxy: during=1.3225494526303614e+20 delta_before=2.1485380796510372e+18 trend=increase
nbi_proxy: during=-0.4393558800220489 delta_before=0.0 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_006 — positive_boundary_margin

```text
time: 0.2257999908924105 → 0.2327999908924105 s
duration: 0.0069999999999999785 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.36600494198632033 delta_before=0.08507272752689743 trend=increase
C_edge_capacity: during=0.6749330087043998 delta_before=-0.016705900365487136 trend=decrease
F_route_fragmentation: during=0.31222860371291716 delta_before=-0.09135574958679665 trend=decrease
S_edge_response: during=0.6060134100554407 delta_before=-0.0333172779237868 trend=decrease
S_power_balance: during=0.2193627723769174 delta_before=-0.2968972126222281 trend=decrease
S_transport: during=0.4670075995584684 delta_before=0.020251972535488383 trend=decrease
dalpha_proxy: during=0.4638671875831041 delta_before=0.00976562506148787 trend=increase
softx_lower_proxy: during=0.0115680694566509 delta_before=0.0006961822519587994 trend=increase
softx_upper_proxy: during=0.0071525573760901 delta_before=-0.0029182434057468 trend=decrease
te_profile_gradient_proxy: during=9.898505984872612 delta_before=-1.9546389059329528 trend=decrease
ne_profile_gradient_proxy: during=4.792567696364152e+17 delta_before=6.201026688526758e+16 trend=decrease
density_proxy: during=1.3845895281690175e+20 delta_before=1.8508958839655465e+18 trend=increase
nbi_proxy: during=-0.4393558800220489 delta_before=-0.8787117600440978 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_007 — positive_boundary_margin

```text
time: 0.2407999908924105 → 0.2457999908924105 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high

m_edge: during=0.284011257583702 delta_before=-0.06647527831657468 trend=decrease
C_edge_capacity: during=0.6586045960610485 delta_before=-0.003952232567351999 trend=decrease
F_route_fragmentation: during=0.36526559576079254 delta_before=0.04123461971559966 trend=increase
S_edge_response: during=0.568474728652363 delta_before=-0.013782329038580787 trend=decrease
S_power_balance: during=0.3848740618934886 delta_before=0.15624575328365942 trend=increase
S_transport: during=0.4671505415534579 delta_before=0.049651201417234225 trend=decrease
dalpha_proxy: during=0.4943847655610253 delta_before=0.01586914042238291 trend=increase
softx_lower_proxy: during=0.010805130007535399 delta_before=-0.001306533808713501 trend=increase
softx_upper_proxy: during=0.0059700012211052 delta_before=-0.00022888183733530028 trend=decrease
te_profile_gradient_proxy: during=10.540222504878848 delta_before=1.3972507045858915 trend=increase
ne_profile_gradient_proxy: during=4.1494360903942195e+17 delta_before=1.581006380050976e+16 trend=decrease
density_proxy: during=1.4466956183858053e+20 delta_before=4.047803679145738e+18 trend=increase
nbi_proxy: during=0.0 delta_before=0.4393558800220489 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_008 — positive_boundary_margin

```text
time: 0.2477999908924105 → 0.2527999908924105 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.30825928888594406 delta_before=0.07773161478743945 trend=increase
C_edge_capacity: during=0.6782025383397396 delta_before=0.018063865326258144 trend=increase
F_route_fragmentation: during=0.393639308493108 delta_before=-0.03961901057827211 trend=increase
S_edge_response: during=0.5937584833641245 delta_before=0.022590835270558385 trend=increase
S_power_balance: during=0.24870533871052097 delta_before=-0.2859689187610646 trend=increase
S_transport: during=0.623230308322013 delta_before=0.1628347517681964 trend=increase
dalpha_proxy: during=0.517578124922815 delta_before=0.026855468661227566 trend=decrease
softx_lower_proxy: during=0.009937286376954551 delta_before=-0.0011634826703236494 trend=increase
softx_upper_proxy: during=0.00543594360018945 delta_before=-0.0007629394582510506 trend=increase
te_profile_gradient_proxy: during=16.01463011398244 delta_before=5.780261877220006 trend=increase
ne_profile_gradient_proxy: during=3.718380795127074e+17 delta_before=-1.5930599108785664e+16 trend=increase
density_proxy: during=1.5066250714037826e+20 delta_before=6.090282867181486e+18 trend=increase
nbi_proxy: during=-0.4393558800220489 delta_before=-0.8787117600440978 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_009 — positive_boundary_margin

```text
time: 0.2647999908924106 → 0.2677999908924106 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3872988382150788 delta_before=0.07057684386597607 trend=increase
C_edge_capacity: during=0.5858346960722586 delta_before=-0.042754006178781556 trend=decrease
F_route_fragmentation: during=0.20509112093216542 delta_before=-0.1061205408396429 trend=decrease
S_edge_response: during=0.40464051673117196 delta_before=-0.09348384177309738 trend=decrease
S_power_balance: during=0.16507004597954744 delta_before=-0.09371747304090394 trend=decrease
S_transport: during=0.2802887069130594 delta_before=-0.1286566911239112 trend=decrease
dalpha_proxy: during=0.612792968806392 delta_before=0.05126953120863753 trend=increase
softx_lower_proxy: during=0.007963180544043099 delta_before=-0.0013065338103407011 trend=decrease
softx_upper_proxy: during=0.004520416257808 delta_before=-0.0004959106464407 trend=decrease
te_profile_gradient_proxy: during=5.629969883691345 delta_before=-3.5997405399763274 trend=decrease
ne_profile_gradient_proxy: during=3.379837035797767e+17 delta_before=-1.6376797916134592e+16 trend=decrease
density_proxy: during=1.5766641380149743e+20 delta_before=3.928546249950626e+18 trend=increase
nbi_proxy: during=-0.732173517346382 delta_before=-0.29281763732433314 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_010 — positive_boundary_margin

```text
time: 0.2697999908924106 → 0.2727999908924106 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.33450162380516824 delta_before=0.04335593064169507 trend=increase
C_edge_capacity: during=0.5937032836930468 delta_before=-0.015392784105320634 trend=decrease
F_route_fragmentation: during=0.25026829578710863 delta_before=-0.08135784223143439 trend=decrease
S_edge_response: during=0.4107686703317024 delta_before=-0.0363850702473677 trend=decrease
S_power_balance: during=0.27739192959808767 delta_before=-0.12910337098004143 trend=decrease
S_transport: during=0.2690235137832182 delta_before=-0.024495738783834153 trend=increase
dalpha_proxy: during=0.650634765669432 delta_before=0.054931640587605246 trend=increase
softx_lower_proxy: during=0.00866889953643055 delta_before=-0.0008487701389129996 trend=decrease
softx_upper_proxy: during=0.0052070617670344 delta_before=-9.536743272099343e-06 trend=decrease
te_profile_gradient_proxy: during=6.413224068080375 delta_before=0.37529947428417465 trend=increase
ne_profile_gradient_proxy: during=3.107200853117061e+17 delta_before=-2.9848361135054336e+16 trend=decrease
density_proxy: during=1.6291666098896503e+20 delta_before=7.14244512621894e+18 trend=increase
nbi_proxy: during=-0.4393558800220489 delta_before=-0.4393558800220489 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_011 — positive_boundary_margin

```text
time: 0.2757999908924106 → 0.2797999908924106 s
duration: 0.0040000000000000036 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3918488304041352 delta_before=0.0649334314890756 trend=decrease
C_edge_capacity: during=0.600241371079013 delta_before=0.014776395495691097 trend=increase
F_route_fragmentation: during=0.2083925406748777 delta_before=-0.04463026397389011 trend=increase
S_edge_response: during=0.416602643093257 delta_before=0.013953143642986332 trend=increase
S_power_balance: during=0.0857124436905598 delta_before=-0.19178723557929267 trend=increase
S_transport: during=0.3595746949368315 delta_before=0.08053150168006129 trend=increase
dalpha_proxy: during=0.6811523438537581 delta_before=0.03662109380290901 trend=increase
softx_lower_proxy: during=0.0073051452638745 delta_before=-0.0006484985369102003 trend=increase
softx_upper_proxy: during=0.004405975339061 delta_before=-7.629394639060028e-05 trend=increase
te_profile_gradient_proxy: during=9.730986596951404 delta_before=3.797914080497244 trend=decrease
ne_profile_gradient_proxy: during=3.120082569364033e+17 delta_before=-6728248331079296.0 trend=increase
density_proxy: during=1.6647658057254096e+20 delta_before=3.5098698142795694e+18 trend=increase
nbi_proxy: during=-1.024991154670715 delta_before=-0.5856352746486662 trend=increase
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