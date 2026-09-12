# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11876_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     537
time_min: -0.0694000050425529
time_max: 0.4665999949574475
```

State counts:

```text
boundary_ambiguous_margin: 271
positive_boundary_margin: 116
negative_leakage_margin: 89
insufficient_data: 61
```

## 5. Inspected windows

| window_label   | state                    |   start_time |    end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                 |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|------------:|-----------:|--------------:|:---------------------------------|:-------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| negative_001   | negative_leakage_margin  | -0.00540001  | -0.00140001 |      0.004 |             5 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.275139 |                         0.441384 |                               0.718288 |                        0.662077  |                         0.779142 |                              |                              0.444444 |
| peak_negative  | peak_negative_window     | -0.000400005 |  0.00759999 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.28198  |                         0.321228 |                               0.573658 |                        0.481842  |                         0.602372 |                              |                              0.444444 |
| negative_002   | negative_leakage_margin  |  0.00259999  |  0.00659999 |      0.004 |             5 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.397059 |                         0.291678 |                               0.718288 |                        0.3585    |                         0.779142 |                              |                              0.444444 |
| positive_001   | positive_boundary_margin |  0.1246      |  0.1276     |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.272997 |                         0.511588 |                               0.240725 |                        0.579999  |                         0.244836 |                              |                              0.222222 |
| positive_002   | positive_boundary_margin |  0.1666      |  0.1706     |      0.004 |             5 | weak_positive_candidate          | capacity_exceeds_fragmentation                                                                         |                0.248928 |                         0.59486  |                               0.332177 |                        0.54338   |                         0.356611 |                              |                              0.222222 |
| positive_003   | positive_boundary_margin |  0.1786      |  0.1816     |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.422335 |                         0.616261 |                               0.196163 |                        0.511597  |                         0.190372 |                              |                              0.222222 |
| positive_004   | positive_boundary_margin |  0.1886      |  0.1916     |      0.003 |             4 | weak_positive_candidate          | capacity_exceeds_fragmentation                                                                         |                0.257384 |                         0.631467 |                               0.371935 |                        0.532109  |                         0.405204 |                              |                              0.222222 |
| positive_005   | positive_boundary_margin |  0.1996      |  0.2026     |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.496354 |                         0.645793 |                               0.142284 |                        0.548707  |                         0.124521 |                              |                              0.222222 |
| positive_006   | positive_boundary_margin |  0.2056      |  0.2136     |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high                                                      |                0.279564 |                         0.649406 |                               0.369843 |                        0.558132  |                         0.402647 |                              |                              0.222222 |
| peak_positive  | peak_positive_window     |  0.2386      |  0.2466     |      0.008 |             9 | weak_positive_candidate          | capacity_exceeds_fragmentation;m_edge_higher_than_before                                               |                0.249094 |                         0.644637 |                               0.397358 |                        0.508284  |                         0.436278 |                              |                              0.222222 |
| positive_007   | positive_boundary_margin |  0.2406      |  0.2436     |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.409527 |                         0.64714  |                               0.236813 |                        0.517415  |                         0.240056 |                              |                              0.222222 |
| negative_003   | negative_leakage_margin  |  0.3866      |  0.3896     |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before                              |               -0.251642 |                         0.182552 |                               0.434398 |                        0.0601866 |                         0.432165 |                              |                              0.444444 |
| negative_004   | negative_leakage_margin  |  0.4086      |  0.4126     |      0.004 |             5 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.292695 |                         0.349073 |                               0.647131 |                        0.479574  |                         0.692173 |                              |                              0.444444 |
| negative_005   | negative_leakage_margin  |  0.4256      |  0.4296     |      0.004 |             5 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.275989 |                         0.390309 |                               0.666704 |                        0.577609  |                         0.716094 |                              |                              0.444444 |
| negative_006   | negative_leakage_margin  |  0.4496      |  0.4596     |      0.01  |            11 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.279495 |                         0.391297 |                               0.665316 |                        0.583628  |                         0.714398 |                              |                              0.444444 |

## 6. Interpretability flags

```text
interpretable_negative_candidate: 7
interpretable_positive_candidate: 5
weak_positive_candidate: 3
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0054000050425528 → -0.0014000050425528 s
duration: 0.004 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.2751394585375779 delta_before=-0.03871166176284027 trend=increase
C_edge_capacity: during=0.4413844953543602 delta_before=0.00025446314486998745 trend=decrease
F_route_fragmentation: during=0.718287554188732 delta_before=-0.12640255884209417 trend=decrease
S_edge_response: during=0.6620767430315403 delta_before=0.00038169471730487015 trend=decrease
S_power_balance: during=0.7791415785763515 delta_before=0.057420750467739534 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.0048828124975029 delta_before=2.4970997491990943e-12 trend=increase
softx_lower_proxy: during=9.536743179436148e-05 delta_before=-9.536743109538515e-06 trend=decrease
softx_upper_proxy: during=0.0002288818358798 delta_before=9.536743185380002e-05 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=2.518937158769705e+17 delta_before=-3.676656932120166e+16 trend=increase
nbi_proxy: during=2.379222631454468 delta_before=1.9032976627349858 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=-0.2777777777777778 trend=flat
```

### peak_negative — peak_negative_window

```text
time: -0.0004000050425528 → 0.0075999949574471 s
duration: 0.0079999999999999 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.2819802013518369 delta_before=-0.04172539290709487 trend=decrease
C_edge_capacity: during=0.3212282988825588 delta_before=-0.12002896489936637 trend=decrease
F_route_fragmentation: during=0.5736582048363709 delta_before=-0.11572202122528163 trend=increase
S_edge_response: during=0.4818424483238382 delta_before=-0.1800434473490497 trend=decrease
S_power_balance: during=0.6023723738123545 delta_before=-0.1303932401191341 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.319824218761479 delta_before=0.3247070312602304 trend=increase
softx_lower_proxy: during=2.655448289642232e-13 delta_before=-0.00010013580308358591 trend=increase
softx_upper_proxy: during=-0.0004005432129337 delta_before=-0.0005626678464956 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.1268379002122795e+19 delta_before=1.1002149853642881e+19 trend=increase
nbi_proxy: during=-0.2562672793865204 delta_before=-1.0982883870601654 trend=increase
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.0025999949574471 → 0.0065999949574471 s
duration: 0.004 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.3970592553061732 delta_before=-0.1827595124498711 trend=increase
C_edge_capacity: during=0.2916780034845339 delta_before=-0.14945202872495633 trend=decrease
F_route_fragmentation: during=0.718287554188732 delta_before=0.06505389917540538 trend=decrease
S_edge_response: during=0.3585001799935053 delta_before=-0.3031948683207301 trend=decrease
S_power_balance: during=0.7791415785763515 delta_before=0.07951032121438428 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.5322265625113299 delta_before=0.5346679687636778 trend=increase
softx_lower_proxy: during=-9.536743240493984e-06 delta_before=-0.00010490417503485546 trend=increase
softx_upper_proxy: during=-0.0004005432129337 delta_before=-0.0005340576169597 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=2.603382070708483e+19 delta_before=2.578192699120786e+19 trend=increase
nbi_proxy: during=2.379222631454468 delta_before=2.6354899108409886 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.1245999949574472 → 0.1275999949574472 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.2729973536329928 delta_before=0.2803527074378262 trend=increase
C_edge_capacity: during=0.5115875137805386 delta_before=0.01186680823216646 trend=increase
F_route_fragmentation: during=0.2407247494650931 delta_before=-0.2734757035538546 trend=decrease
S_edge_response: during=0.5799991972758429 delta_before=0.01779430455072517 trend=increase
S_power_balance: during=0.2448364221857311 delta_before=-0.3342480821213779 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3759765624852226 delta_before=0.01953125004097772 trend=increase
softx_lower_proxy: during=0.001258850097227 delta_before=0.0004005432120095001 trend=increase
softx_upper_proxy: during=0.0057506561280738 delta_before=0.00046730041647569977 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=9.023667739901821e+19 delta_before=1.2357411184574464e+18 trend=increase
nbi_proxy: during=-6.771634817123413 delta_before=-11.053498983383179 trend=flat
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.1665999949574472 → 0.1705999949574472 s
duration: 0.0040000000000000036 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation

m_edge: during=0.248927531062189 delta_before=-0.01737594026933681 trend=increase
C_edge_capacity: during=0.5948598475929845 delta_before=0.008205265154116015 trend=decrease
F_route_fragmentation: during=0.3321766128163905 delta_before=0.015387332383405505 trend=decrease
S_edge_response: during=0.5433803398558108 delta_before=-0.03327042213724363 trend=decrease
S_power_balance: during=0.3566109218373168 delta_before=0.0188067395797179 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.5078124999736132 delta_before=0.02929687499068262 trend=increase
softx_lower_proxy: during=0.0020408630360699 delta_before=-0.0004768371612516001 trend=decrease
softx_upper_proxy: during=0.0039291381839402 delta_before=0.0012588501042212004 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.160290519497132e+20 delta_before=3.154551636647477e+18 trend=increase
nbi_proxy: during=-1.7206517457962036 delta_before=0.5849674940109253 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.1785999949574472 → 0.1815999949574472 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.42233488175229905 delta_before=0.19155073006367795 trend=increase
C_edge_capacity: during=0.616261351108383 delta_before=0.02644513849380259 trend=increase
F_route_fragmentation: during=0.19616327847325177 delta_before=-0.15334517682462823 trend=decrease
S_edge_response: during=0.5115971869688266 delta_before=0.0027223978928297976 trend=decrease
S_power_balance: during=0.1903724020845917 delta_before=-0.18742188278565672 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.5834960937454311 delta_before=0.03662109369958966 trend=increase
softx_lower_proxy: during=0.00133991241443995 delta_before=-0.00010967254719634997 trend=decrease
softx_upper_proxy: during=0.009660720826212 delta_before=0.0028514862075686995 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.2220035562972224e+20 delta_before=3.321263987697402e+18 trend=increase
nbi_proxy: during=-8.893102645874023 delta_before=-7.611982583999634 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.1885999949574472 → 0.1915999949574472 s
duration: 0.0030000000000000027 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation

m_edge: during=0.25738373739657827 delta_before=-0.026730200991724018 trend=increase
C_edge_capacity: during=0.6314672585901635 delta_before=0.005968040362103855 trend=decrease
F_route_fragmentation: during=0.3719348030164989 delta_before=0.0224263477186189 trend=decrease
S_edge_response: during=0.5321089730460692 delta_before=0.010318525114785704 trend=decrease
S_power_balance: during=0.405204265415227 delta_before=0.027409980544978618 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.6689453124950939 delta_before=0.04150390619718569 trend=increase
softx_lower_proxy: during=0.0008201599117494 delta_before=-0.00024795532233079997 trend=decrease
softx_upper_proxy: during=0.023612976073953247 delta_before=0.009098052977660647 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.2520868101596851e+20 delta_before=1.9039319268429496e+18 trend=increase
nbi_proxy: during=-0.9884595274925232 delta_before=0.29266053438186646 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_005 — positive_boundary_margin

```text
time: 0.1995999949574473 → 0.2025999949574473 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.49635369533940554 delta_before=0.2637790208714566 trend=increase
C_edge_capacity: during=0.6457927025344075 delta_before=0.015351416583345823 trend=decrease
F_route_fragmentation: during=0.1422844650320381 delta_before=-0.2567571574158477 trend=decrease
S_edge_response: during=0.5487065843120309 delta_before=0.030537655552163256 trend=decrease
S_power_balance: during=0.12452051898977495 delta_before=-0.3138143035082583 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.6115722655948457 delta_before=-0.0610351562707625 trend=decrease
softx_lower_proxy: during=0.00064849853499725 delta_before=-5.722045910570004e-05 trend=decrease
softx_upper_proxy: during=0.0218200683606709 delta_before=-0.0020313262929161496 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.2839538237261218e+20 delta_before=8.129349171124634e+16 trend=increase
nbi_proxy: during=-10.577625274658203 delta_before=-10.687454134225845 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_006 — positive_boundary_margin

```text
time: 0.2055999949574473 → 0.2135999949574473 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high

m_edge: during=0.2795635443007926 delta_before=-0.08824530778607931 trend=decrease
C_edge_capacity: during=0.6494063919554187 delta_before=0.007157680150016388 trend=decrease
F_route_fragmentation: during=0.3698428476546261 delta_before=0.0941101852314628 trend=increase
S_edge_response: during=0.5581319339538027 delta_before=0.015399394754909035 trend=decrease
S_power_balance: during=0.4026474310840492 delta_before=0.1150235597273434 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.60302734375 delta_before=-0.019531249979576337 trend=increase
softx_lower_proxy: during=0.0007057189949617 delta_before=0.00020980835019119995 trend=increase
softx_upper_proxy: during=0.0202560424767331 delta_before=-0.0015640258839936007 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.28045975169491e+20 delta_before=-1.6083656091108966e+17 trend=increase
nbi_proxy: during=-1.2811200618743896 delta_before=3.6603429317474365 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.2385999949574473 → 0.2465999949574473 s
duration: 0.008000000000000007 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation;m_edge_higher_than_before

m_edge: during=0.2490944825365366 delta_before=0.05984719106629621 trend=increase
C_edge_capacity: during=0.6446368911211597 delta_before=0.019345269774578178 trend=decrease
F_route_fragmentation: during=0.3973584373738857 delta_before=-0.034793270443801816 trend=decrease
S_edge_response: during=0.5082844498822466 delta_before=0.006810335198378148 trend=decrease
S_power_balance: during=0.4362775962964776 delta_before=-0.042525108320202176 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.6396484375116688 delta_before=0.03417968752314782 trend=increase
softx_lower_proxy: during=0.0006103515621389 delta_before=0.00017166137728619998 trend=decrease
softx_upper_proxy: during=0.0146102905271643 delta_before=-0.0006294250475126998 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.3949884892421974e+20 delta_before=2.521048221095035e+18 trend=increase
nbi_proxy: during=-1.2811200618743896 delta_before=-1.757045030593872 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_007 — positive_boundary_margin

```text
time: 0.2405999949574473 → 0.2435999949574473 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.40952735792373995 delta_before=0.18211130514833776 trend=increase
C_edge_capacity: during=0.6471404405400536 delta_before=0.021848819193472035 trend=decrease
F_route_fragmentation: during=0.23681317042222275 delta_before=-0.18030015243771738 trend=decrease
S_edge_response: during=0.5174154943302318 delta_before=0.017165084574963796 trend=decrease
S_power_balance: during=0.24005560335555626 delta_before=-0.22036685297943231 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.6250000000404949 delta_before=0.019531250029165004 trend=increase
softx_lower_proxy: during=0.0007820129377669 delta_before=0.00037193298291149997 trend=increase
softx_upper_proxy: during=0.0146198272715995 delta_before=-0.0005626678454109003 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.3945342589985305e+20 delta_before=1.87542378935799e+18 trend=increase
nbi_proxy: during=-8.893102645874023 delta_before=-8.636835366487503 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### negative_003 — negative_leakage_margin

```text
time: 0.3865999949574474 → 0.3895999949574474 s
duration: 0.0030000000000000027 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.25164230034964363 delta_before=-0.009412589403037436 trend=increase
C_edge_capacity: during=0.1825521148567435 delta_before=-0.010747661469741598 trend=increase
F_route_fragmentation: during=0.4343977378067667 delta_before=-0.009033532282849699 trend=increase
S_edge_response: during=0.06018657877068035 delta_before=-0.022407826529225246 trend=increase
S_power_balance: during=0.4321651363317272 delta_before=-0.011040983901260792 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=1.0900878903950204 delta_before=0.1306152341450204 trend=decrease
softx_lower_proxy: during=-0.0007152557383031 delta_before=-0.00015258789241310005 trend=increase
softx_upper_proxy: during=-0.0012588500971221 delta_before=-1.907348684940008e-05 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=9.356723885704007e+19 delta_before=-1.242646051479896e+18 trend=decrease
nbi_proxy: during=-0.2562672793865204 delta_before=1.0248527824878693 trend=increase
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