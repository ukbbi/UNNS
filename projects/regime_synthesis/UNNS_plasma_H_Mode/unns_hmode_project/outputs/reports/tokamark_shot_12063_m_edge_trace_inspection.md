# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12063_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     426
time_min: -0.0680000111460685
time_max: 0.3569999888539318
```

State counts:

```text
boundary_ambiguous_margin: 209
positive_boundary_margin: 110
insufficient_data: 59
negative_leakage_margin: 48
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                            |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:----------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| peak_negative  | peak_negative_window     | -1.11461e-08 | 0.00799999 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before                             |               -0.353819 |                         0.212636 |                               0.546474 |                         0.17363  |                        0.817648  |                     0.363595 |                              0.444444 |
| positive_001   | positive_boundary_margin |  0.097       | 0.1        |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before                    |                0.250337 |                         0.63988  |                               0.383785 |                         0.372179 |                        0.276923  |                     0.580207 |                              0        |
| positive_002   | positive_boundary_margin |  0.115       | 0.119      |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before |                0.327917 |                         0.649378 |                               0.324168 |                         0.657676 |                        0.104338  |                     0.612101 |                              0        |
| positive_003   | positive_boundary_margin |  0.148       | 0.151      |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                            |                0.305896 |                         0.693833 |                               0.383724 |                         0.628243 |                        0.319432  |                     0.488398 |                              0.222222 |
| positive_004   | positive_boundary_margin |  0.154       | 0.158      |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                            |                0.293961 |                         0.69252  |                               0.399742 |                         0.61817  |                        0.32686   |                     0.512073 |                              0.222222 |
| positive_005   | positive_boundary_margin |  0.168       | 0.173      |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                            |                0.3587   |                         0.643511 |                               0.282544 |                         0.58263  |                        0.0294515 |                     0.54488  |                              0.222222 |
| peak_positive  | peak_positive_window     |  0.205       | 0.213      |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high                                                                                 |                0.185417 |                         0.706302 |                               0.520884 |                         0.750939 |                        0.669381  |                     0.461112 |                              0.222222 |
| positive_006   | positive_boundary_margin |  0.226       | 0.229      |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                            |                0.324377 |                         0.553458 |                               0.226864 |                         0.562636 |                        0.19931   |                     0.254105 |                              0.222222 |
| positive_007   | positive_boundary_margin |  0.251       | 0.256      |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                               |                0.317629 |                         0.564742 |                               0.232088 |                         0.534338 |                        0.157848  |                     0.345388 |                              0.222222 |
| negative_001   | negative_leakage_margin  |  0.313       | 0.317      |      0.004 |             5 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                                               |               -0.468495 |                         0.388034 |                               0.854965 |                         0.575412 |                        0.946192  |                   nan        |                              0.444444 |
| negative_002   | negative_leakage_margin  |  0.322       | 0.326      |      0.004 |             5 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                                               |               -0.454731 |                         0.396612 |                               0.846724 |                         0.580922 |                        0.936119  |                   nan        |                              0.444444 |

## 6. Interpretability flags

```text
interpretable_positive_candidate: 8
interpretable_negative_candidate: 3
```

## 7. Detailed window notes

### peak_negative — peak_negative_window

```text
time: -1.1146068512601914e-08 → 0.0079999888539314 s
duration: 0.007999999999999913 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.3538189464014549 delta_before=-0.1135280114103002 trend=increase
C_edge_capacity: during=0.2126359150200278 delta_before=-0.22428438690468963 trend=decrease
F_route_fragmentation: during=0.5464740681363519 delta_before=-0.284312709277755 trend=decrease
S_edge_response: during=0.1736299422562544 delta_before=-0.4489782386926613 trend=decrease
S_power_balance: during=0.8176482505738526 delta_before=0.08890265057213409 trend=decrease
S_transport: during=0.36359455438167704 delta_before=None trend=decrease
dalpha_proxy: during=0.300292968763976 delta_before=0.305175781263976 trend=increase
softx_lower_proxy: during=-7.629394524786079e-05 delta_before=-9.536743157518508e-05 trend=increase
softx_upper_proxy: during=-0.000305175781293 delta_before=-0.00040054321306285474 trend=decrease
te_profile_gradient_proxy: during=19.67809287905363 delta_before=None trend=decrease
ne_profile_gradient_proxy: during=8.968438592085683e+16 delta_before=None trend=increase
density_proxy: during=-4768581929664512.0 delta_before=9.416860107381146e+17 trend=increase
nbi_proxy: during=0.6151038408279419 delta_before=0.5125864893198013 trend=increase
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=decrease
```

### positive_001 — positive_boundary_margin

```text
time: 0.0969999888539315 → 0.0999999888539315 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.25033684111989035 delta_before=0.13109174658938577 trend=increase
C_edge_capacity: during=0.6398801141276869 delta_before=-0.012543779155342882 trend=decrease
F_route_fragmentation: during=0.38378484935566004 delta_before=-0.15081566267470248 trend=decrease
S_edge_response: during=0.372179130190581 delta_before=-0.01509993718252678 trend=increase
S_power_balance: during=0.27692259320542256 delta_before=-0.31302670682711764 trend=decrease
S_transport: during=0.5802073758749227 delta_before=-0.047396001466777804 trend=increase
dalpha_proxy: during=0.25024414062192524 delta_before=-0.00976562498535316 trend=increase
softx_lower_proxy: during=0.0017738342283212 delta_before=0.00011444091789275003 trend=increase
softx_upper_proxy: during=0.0089645385736387 delta_before=0.0009346008295001498 trend=decrease
te_profile_gradient_proxy: during=13.432558691320384 delta_before=-0.3304771929735697 trend=increase
ne_profile_gradient_proxy: during=4.047716117499104e+17 delta_before=-7.826294796381069e+16 trend=decrease
density_proxy: during=8.08377529376262e+19 delta_before=1.2470001175258726e+18 trend=increase
nbi_proxy: during=-0.7761056572198868 delta_before=-0.8786230087280273 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.1149999888539315 → 0.1189999888539316 s
duration: 0.004000000000000087 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.3279167060326796 delta_before=0.10828227232591889 trend=decrease
C_edge_capacity: during=0.649378038773813 delta_before=0.024276086702274102 trend=decrease
F_route_fragmentation: during=0.3241676024935022 delta_before=-0.08268602422934745 trend=increase
S_edge_response: during=0.6576757299173926 delta_before=0.13693681985670414 trend=increase
S_power_balance: during=0.1043377849224745 delta_before=-0.26518952446036204 trend=increase
S_transport: during=0.6121012170906146 delta_before=0.08687927493967651 trend=increase
dalpha_proxy: during=0.0805664062362103 delta_before=-0.039062500010454054 trend=decrease
softx_lower_proxy: during=0.002136230469127 delta_before=-4.291533844349993e-05 trend=decrease
softx_upper_proxy: during=0.0094795227018811 delta_before=0.0010395050014721016 trend=decrease
te_profile_gradient_proxy: during=14.669662096914871 delta_before=3.977076102146336 trend=increase
ne_profile_gradient_proxy: during=5.935007376856901e+17 delta_before=1.3036920923797837e+17 trend=increase
density_proxy: during=7.200107474221374e+19 delta_before=-8.659555668270776e+17 trend=decrease
nbi_proxy: during=-1.1421421766281128 delta_before=-0.732073038816452 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.1479999888539316 → 0.1509999888539316 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3058963565978856 delta_before=0.18458074659698911 trend=increase
C_edge_capacity: during=0.6938331397029065 delta_before=0.00936579691835282 trend=increase
F_route_fragmentation: during=0.38372435420156537 delta_before=-0.17979346554808107 trend=increase
S_edge_response: during=0.6282426627813815 delta_before=0.015555342312139508 trend=increase
S_power_balance: during=0.31943234129275555 delta_before=-0.37647244617758624 trend=decrease
S_transport: during=0.48839799281142754 delta_before=0.004205461716175418 trend=increase
dalpha_proxy: during=0.057373046866837946 delta_before=0.001220703109160448 trend=decrease
softx_lower_proxy: during=0.0045394897469829 delta_before=0.0005912780770610995 trend=increase
softx_upper_proxy: during=0.0022411346441227 delta_before=8.583068726300026e-05 trend=increase
te_profile_gradient_proxy: during=13.174678351289117 delta_before=2.3320849416010674 trend=increase
ne_profile_gradient_proxy: during=4.7436295017703296e+17 delta_before=-5.677958806634931e+16 trend=decrease
density_proxy: during=6.353318154285036e+19 delta_before=-1.3752691440222208e+17 trend=decrease
nbi_proxy: during=-0.4100691378116607 delta_before=-1.0251729786396027 trend=flat
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.1539999888539316 → 0.1579999888539316 s
duration: 0.0040000000000000036 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.293960911084007 delta_before=0.0025104312548437924 trend=increase
C_edge_capacity: during=0.6925201829677213 delta_before=-0.0007411042605293128 trend=decrease
F_route_fragmentation: during=0.3997417817098074 delta_before=-0.002069025689280024 trend=decrease
S_edge_response: during=0.6181699651853239 delta_before=-0.006676561078637677 trend=increase
S_power_balance: during=0.326859699200452 delta_before=-0.0015941660823028947 trend=decrease
S_transport: during=0.5120726552164039 delta_before=0.02675379275016687 trend=decrease
dalpha_proxy: during=0.0634765625 delta_before=0.0097656249841978 trend=increase
softx_lower_proxy: during=0.0049781799307275 delta_before=0.0004005432130368006 trend=increase
softx_upper_proxy: during=0.0025177001949878 delta_before=0.00019073486276439998 trend=increase
te_profile_gradient_proxy: during=16.80676231519787 delta_before=4.010621737470256 trend=increase
ne_profile_gradient_proxy: during=3.5991724155390374e+17 delta_before=-1.2288225885637498e+17 trend=decrease
density_proxy: during=6.47063384594548e+19 delta_before=1.209119742925734e+18 trend=decrease
nbi_proxy: during=-0.4100691378116607 delta_before=0.0 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_005 — positive_boundary_margin

```text
time: 0.1679999888539316 → 0.1729999888539316 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3586997320432074 delta_before=0.26353668124972884 trend=increase
C_edge_capacity: during=0.6435111486147526 delta_before=-0.01180747988198294 trend=increase
F_route_fragmentation: during=0.28254412209717883 delta_before=-0.279325439565438 trend=increase
S_edge_response: during=0.5826297495851407 delta_before=-0.006380940088352549 trend=increase
S_power_balance: during=0.0294515417461861 delta_before=-0.6503608764541522 trend=increase
S_transport: during=0.5448797159926649 delta_before=0.04372159058362368 trend=decrease
dalpha_proxy: during=0.13916015624139075 delta_before=0.04150390623278155 trend=flat
softx_lower_proxy: during=0.0074958801260113 delta_before=0.0013732910156249003 trend=increase
softx_upper_proxy: during=0.0037097930903734998 delta_before=0.0002956390380409999 trend=increase
te_profile_gradient_proxy: during=18.244493261127815 delta_before=2.5808473621019683 trend=increase
ne_profile_gradient_proxy: during=3.6628607291422016e+17 delta_before=-2.0672208228705856e+16 trend=decrease
density_proxy: during=5.848207130433579e+19 delta_before=-1.7457231987222774e+18 trend=increase
nbi_proxy: during=-1.1421421766281128 delta_before=-1.7572460174560547 trend=flat
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.2049999888539316 → 0.2129999888539316 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high

m_edge: during=0.1854174563045642 delta_before=-0.014611507939250007 trend=decrease
C_edge_capacity: during=0.706301588490346 delta_before=-0.01341932864139761 trend=decrease
F_route_fragmentation: during=0.5208841321857818 delta_before=0.018889352498724477 trend=decrease
S_edge_response: during=0.7509394425293954 delta_before=0.02258966300283105 trend=decrease
S_power_balance: during=0.6693811355724233 delta_before=0.02318898951159043 trend=decrease
S_transport: during=0.461111797401767 delta_before=0.0 trend=increase
dalpha_proxy: during=0.06103515625 delta_before=-0.019531249979806695 trend=decrease
softx_lower_proxy: during=0.0081062316887327 delta_before=-0.0009346008312631996 trend=increase
softx_upper_proxy: during=0.0144577026370414 delta_before=-0.0028991699207661006 trend=decrease
te_profile_gradient_proxy: during=20.715411925866352 delta_before=0.4072653806349642 trend=decrease
ne_profile_gradient_proxy: during=2.2496824857915782e+17 delta_before=6.661053922009171e+16 trend=increase
density_proxy: during=4.6478405995765694e+19 delta_before=-6.356641758033478e+18 trend=decrease
nbi_proxy: during=0.6151038408279419 delta_before=0.0 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_006 — positive_boundary_margin

```text
time: 0.2259999888539317 → 0.2289999888539317 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.32437719559856293 delta_before=0.16998918307364524 trend=decrease
C_edge_capacity: during=0.5534580612234816 delta_before=-0.006566553569874012 trend=decrease
F_route_fragmentation: during=0.22686420954575004 delta_before=-0.18131210245506357 trend=increase
S_edge_response: during=0.5626359724255752 delta_before=0.00011225225593713972 trend=decrease
S_power_balance: during=0.19931023795800384 delta_before=-0.493201171998072 trend=increase
S_transport: during=0.2541045995790594 delta_before=0.08083921005400574 trend=increase
dalpha_proxy: during=0.05493164064702285 delta_before=-0.003662109358438796 trend=increase
softx_lower_proxy: during=0.0054836273205371 delta_before=3.814697318915011e-05 trend=increase
softx_upper_proxy: during=0.0061321258524216 delta_before=-0.0030994415300939987 trend=decrease
te_profile_gradient_proxy: during=12.11539556642975 delta_before=1.7357518329091626 trend=increase
ne_profile_gradient_proxy: during=2.0079203057814688e+17 delta_before=6.658372001087715e+16 trend=decrease
density_proxy: during=3.8812144733981245e+19 delta_before=-1.865237913638273e+18 trend=decrease
nbi_proxy: during=-0.7761056572198868 delta_before=-1.3912094980478287 trend=flat
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_007 — positive_boundary_margin

```text
time: 0.2509999888539317 → 0.2559999888539317 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.31762914771719253 delta_before=0.08954510776332142 trend=increase
C_edge_capacity: during=0.5647420777973468 delta_before=-0.05241798404883702 trend=decrease
F_route_fragmentation: during=0.2320876723625757 delta_before=-0.17490575641246373 trend=decrease
S_edge_response: during=0.5343377884754725 delta_before=-0.11486865368279697 trend=decrease
S_power_balance: during=0.1578480309102906 delta_before=-0.16807011991209841 trend=decrease
S_transport: during=0.3453878824354376 delta_before=-0.14990072412882377 trend=decrease
dalpha_proxy: during=0.08300781248199884 delta_before=0.01464843750540415 trend=increase
softx_lower_proxy: during=0.00447273254678455 delta_before=-0.0013828277539255501 trend=decrease
softx_upper_proxy: during=0.00250816345182025 delta_before=-0.00100135802828505 trend=decrease
te_profile_gradient_proxy: during=20.0871906310771 delta_before=-3.6013395398812307 trend=decrease
ne_profile_gradient_proxy: during=1.1478586689649648e+17 delta_before=-8.499760324263357e+16 trend=decrease
density_proxy: during=4.6463070007581475e+19 delta_before=4.959276828339479e+18 trend=increase
nbi_proxy: during=-0.7761056572198868 delta_before=-0.36603651940822607 trend=flat
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### negative_001 — negative_leakage_margin

```text
time: 0.3129999888539317 → 0.3169999888539317 s
duration: 0.0040000000000000036 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.4684953639034577 delta_before=-0.3060253454404514 trend=increase
C_edge_capacity: during=0.3880335694335384 delta_before=0.001197690617947278 trend=increase
F_route_fragmentation: during=0.8549652912214896 delta_before=0.31126492464021926 trend=decrease
S_edge_response: during=0.5754121654738567 delta_before=0.002852036984819506 trend=increase
S_power_balance: during=0.9461921460608328 delta_before=0.3804349078936011 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.0024414062642708 delta_before=-1.4909991644107556e-13 trend=flat
softx_lower_proxy: during=-0.0012779235838728 delta_before=7.629394586189994e-05 trend=increase
softx_upper_proxy: during=-0.0013351440425202 delta_before=0.00032424926913620007 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-4.936969936435151e+18 delta_before=-8.48910937573294e+16 trend=decrease
nbi_proxy: during=0.6151038408279419 delta_before=1.0251729786396027 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.3219999888539318 → 0.3259999888539318 s
duration: 0.0040000000000000036 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.4547309208216006 delta_before=-0.028112635853785484 trend=decrease
C_edge_capacity: during=0.3966123028839524 delta_before=-0.0029757095314518756 trend=decrease
F_route_fragmentation: during=0.8467238629091743 delta_before=0.01390928861907359 trend=increase
S_edge_response: during=0.5809221929098132 delta_before=0.0029573225782579815 trend=decrease
S_power_balance: during=0.93611928923467 delta_before=0.017000241645534486 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.0048828125 delta_before=-7.101550250632194e-12 trend=increase
softx_lower_proxy: during=-0.0012016296377587 delta_before=7.629394583444989e-05 trend=decrease
softx_upper_proxy: during=-0.0012969970691742 delta_before=-3.8146970013400085e-05 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-4.083669748443775e+18 delta_before=-5.500669756786606e+17 trend=decrease
nbi_proxy: during=0.6151038408279419 delta_before=0.0 trend=increase
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```