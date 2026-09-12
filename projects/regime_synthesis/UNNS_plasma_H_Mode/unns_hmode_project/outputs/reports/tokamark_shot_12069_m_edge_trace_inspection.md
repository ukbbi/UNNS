# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12069_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     336
time_min: -0.0284000113606452
time_max: 0.306599988639355
```

State counts:

```text
positive_boundary_margin: 151
boundary_ambiguous_margin: 122
negative_leakage_margin: 44
insufficient_data: 19
```

## 5. Inspected windows

| window_label   | state                    |   start_time |    end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                 |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|------------:|-----------:|--------------:|:---------------------------------|:-------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| negative_001   | negative_leakage_margin  |  -0.00540001 | -0.00240001 |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.251865 |                         0.470528 |                              0.722585  |                         0.705262 |                        0.784394  |                  nan         |                              0.444444 |
| positive_001   | positive_boundary_margin |   0.0756     |  0.0816     |      0.006 |             7 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.322401 |                         0.515142 |                              0.204114  |                         0.388014 |                        0.130311  |                    0.297381  |                              0.222222 |
| positive_002   | positive_boundary_margin |   0.0966     |  0.1056     |      0.009 |            10 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.382146 |                         0.56704  |                              0.185194  |                         0.518131 |                        0.108014  |                    0.265918  |                              0.222222 |
| positive_003   | positive_boundary_margin |   0.1156     |  0.1196     |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.407265 |                         0.546397 |                              0.136969  |                         0.536622 |                        0.0477709 |                    0.208159  |                              0.222222 |
| positive_004   | positive_boundary_margin |   0.1396     |  0.1506     |      0.011 |            12 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure                                              |                0.31991  |                         0.580943 |                              0.24219   |                         0.54154  |                        0.299685  |                    0.199211  |                              0.222222 |
| positive_005   | positive_boundary_margin |   0.1526     |  0.1626     |      0.01  |            11 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.463441 |                         0.625337 |                              0.170349  |                         0.577572 |                        0.127021  |                    0.185054  |                              0.222222 |
| positive_006   | positive_boundary_margin |   0.1646     |  0.2116     |      0.047 |            48 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                            |                0.373389 |                         0.737312 |                              0.348367  |                         0.639236 |                        0.514265  |                    0.218012  |                              0.222222 |
| peak_positive  | peak_positive_window     |   0.2126     |  0.2206     |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high                                                      |                0.342306 |                         0.713107 |                              0.367931  |                         0.633908 |                        0.564446  |                    0.20865   |                              0.222222 |
| positive_007   | positive_boundary_margin |   0.2136     |  0.2306     |      0.017 |            18 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                            |                0.35742  |                         0.677011 |                              0.364021  |                         0.595754 |                        0.533517  |                    0.236196  |                              0.222222 |
| positive_008   | positive_boundary_margin |   0.2356     |  0.2416     |      0.006 |             7 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.42586  |                         0.545004 |                              0.118165  |                         0.420067 |                        0.146275  |                    0.0509439 |                              0.222222 |
| positive_009   | positive_boundary_margin |   0.2456     |  0.2496     |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure                                              |                0.391732 |                         0.485014 |                              0.0901251 |                         0.396638 |                        0.0113875 |                  nan         |                              0.444444 |
| negative_002   | negative_leakage_margin  |   0.2576     |  0.2606     |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.275217 |                         0.390843 |                              0.651309  |                         0.486505 |                        0.697278  |                  nan         |                              0.444444 |
| peak_negative  | peak_negative_window     |   0.2596     |  0.2676     |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.28505  |                         0.377763 |                              0.664724  |                         0.485649 |                        0.713676  |                  nan         |                              0.444444 |
| negative_003   | negative_leakage_margin  |   0.2836     |  0.2866     |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.258958 |                         0.422009 |                              0.682833  |                         0.579953 |                        0.735808  |                  nan         |                              0.444444 |

## 6. Interpretability flags

```text
interpretable_positive_candidate: 10
interpretable_negative_candidate: 4
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0054000113606452 → -0.0024000113606452 s
duration: 0.003 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.25186492701663943 delta_before=-0.0006485355077565091 trend=decrease
C_edge_capacity: during=0.4705277808149211 delta_before=0.010646551671054882 trend=decrease
F_route_fragmentation: during=0.7225851578808086 delta_before=-0.27741484211919143 trend=decrease
S_edge_response: during=0.7052621112628548 delta_before=0.015440267547055408 trend=decrease
S_power_balance: during=0.7843942053111117 delta_before=0.0029997989393784064 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.00366210937506095 delta_before=0.00122070312493905 trend=decrease
softx_lower_proxy: during=0.0002574920654167 delta_before=0.000181198120102453 trend=decrease
softx_upper_proxy: during=3.337860106663516e-05 delta_before=-4.768371584850277e-06 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-2.0616359791265055e+18 delta_before=-3.320926437627658e+17 trend=increase
nbi_proxy: during=0.4613277614116668 delta_before=0.0 trend=flat
missingness_pressure: during=0.4444444444444444 delta_before=-0.5555555555555556 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.0755999886393548 → 0.0815999886393548 s
duration: 0.006000000000000005 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3224009362737563 delta_before=0.17364068833614146 trend=increase
C_edge_capacity: during=0.515142260558481 delta_before=0.0002785957970327102 trend=decrease
F_route_fragmentation: during=0.2041136904226756 delta_before=-0.16575018793922178 trend=decrease
S_edge_response: during=0.3880142400780484 delta_before=0.030394788940135253 trend=increase
S_power_balance: during=0.1303111631428825 delta_before=-0.38074607141331307 trend=decrease
S_transport: during=0.2973806448925153 delta_before=-0.022945210724404308 trend=decrease
dalpha_proxy: during=0.4248046875016313 delta_before=-0.0830078124988744 trend=decrease
softx_lower_proxy: during=0.0001811981200717 delta_before=4.291534422274997e-05 trend=decrease
softx_upper_proxy: during=-7.629394531662929e-05 delta_before=2.861022947783536e-05 trend=increase
te_profile_gradient_proxy: during=11.05274736721922 delta_before=-2.5380962882487967 trend=decrease
ne_profile_gradient_proxy: during=5.885666463632741e+17 delta_before=-2.5871869290482176e+16 trend=decrease
density_proxy: during=6.670828085279772e+19 delta_before=-6.979172047540716e+17 trend=decrease
nbi_proxy: during=-0.5638450980186462 delta_before=-1.025172859430313 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.2222222222222222 trend=increase
```

### positive_002 — positive_boundary_margin

```text
time: 0.0965999886393548 → 0.1055999886393548 s
duration: 0.008999999999999994 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.38214596172515347 delta_before=0.22766385760065083 trend=decrease
C_edge_capacity: during=0.567040334626571 delta_before=0.024676389398338716 trend=decrease
F_route_fragmentation: during=0.18519409910046955 delta_before=-0.21353029989135722 trend=increase
S_edge_response: during=0.5181306689889138 delta_before=0.058350386506599794 trend=increase
S_power_balance: during=0.10801350000886055 delta_before=-0.3811696161123256 trend=increase
S_transport: during=0.2659182896971109 delta_before=-0.07963144120491905 trend=increase
dalpha_proxy: during=0.1843261718733093 delta_before=-0.1110839843769727 trend=decrease
softx_lower_proxy: during=0.00050544738760335 delta_before=0.00030517578111925004 trend=decrease
softx_upper_proxy: during=0.00047683715825065 delta_before=0.0004529953003232421 trend=increase
te_profile_gradient_proxy: during=9.065960517691124 delta_before=-0.5377083836537437 trend=increase
ne_profile_gradient_proxy: during=5.776067888916326e+17 delta_before=-1.2426738873763942e+17 trend=increase
density_proxy: during=5.652738152270817e+19 delta_before=-6.189016812332515e+18 trend=decrease
nbi_proxy: during=-0.5638450980186462 delta_before=-1.025172859430313 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.1155999886393548 → 0.1195999886393548 s
duration: 0.00399999999999999 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4072645126064265 delta_before=0.21141955490257128 trend=decrease
C_edge_capacity: during=0.5463973980456811 delta_before=-0.0062627671576069854 trend=decrease
F_route_fragmentation: during=0.1369693049549254 delta_before=-0.22283741655252684 trend=increase
S_edge_response: during=0.5366217564096636 delta_before=0.004101942380408952 trend=decrease
S_power_balance: during=0.0477709221303686 delta_before=-0.45590361306950655 trend=increase
S_transport: during=0.2081589141783507 delta_before=-0.02793990404302521 trend=decrease
dalpha_proxy: during=0.1391601562514636 delta_before=-0.006103515622806199 trend=increase
softx_lower_proxy: during=0.0007057189941348 delta_before=0.00026702880858515 trend=increase
softx_upper_proxy: during=0.000152587890625 delta_before=-0.00029563903810035 trend=decrease
te_profile_gradient_proxy: during=7.122694664337757 delta_before=-2.323135807919197 trend=decrease
ne_profile_gradient_proxy: during=4.821606198814192e+17 delta_before=-3.934134787556589e+16 trend=decrease
density_proxy: during=4.895540778105202e+19 delta_before=-2.906490818304934e+18 trend=decrease
nbi_proxy: during=-0.8566067218780518 delta_before=-1.3179344832897186 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.1395999886393548 → 0.1505999886393548 s
duration: 0.01100000000000001 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure

m_edge: during=0.31990953140160505 delta_before=-0.044034317180933646 trend=decrease
C_edge_capacity: during=0.5809432827023504 delta_before=0.027221642376197286 trend=increase
F_route_fragmentation: during=0.242190387445749 delta_before=0.0726423137576902 trend=increase
S_edge_response: during=0.5415395148580835 delta_before=0.016130220875141266 trend=increase
S_power_balance: during=0.29968533904284184 delta_before=0.16923240220452113 trend=increase
S_transport: during=0.19921086006310812 delta_before=0.012811504366160215 trend=decrease
dalpha_proxy: during=0.12329101562409195 delta_before=-0.006103515622519845 trend=flat
softx_lower_proxy: during=0.0007820129394782 delta_before=0.00020980834960800001 trend=increase
softx_upper_proxy: during=0.0002670288085605 delta_before=-1.907348634809996e-05 trend=increase
te_profile_gradient_proxy: during=9.74382015781462 delta_before=3.1386082926948458 trend=increase
ne_profile_gradient_proxy: during=4.265825178352436e+17 delta_before=-9919011590847232.0 trend=decrease
density_proxy: during=5.60064131222586e+19 delta_before=3.226437706871472e+18 trend=increase
nbi_proxy: during=-0.05125866830348971 delta_before=0.5125864297151566 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_005 — positive_boundary_margin

```text
time: 0.1525999886393548 → 0.1625999886393548 s
duration: 0.009999999999999981 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4634409746588163 delta_before=0.19364887340778758 trend=increase
C_edge_capacity: during=0.6253368976426814 delta_before=0.035674017757968635 trend=increase
F_route_fragmentation: during=0.1703491271242683 delta_before=-0.1500891656840907 trend=decrease
S_edge_response: during=0.5775718194350374 delta_before=0.027002568440697927 trend=increase
S_power_balance: during=0.1270213388312594 delta_before=-0.35762271422959413 trend=decrease
S_transport: during=0.1850542279387727 delta_before=-0.006916781949457801 trend=increase
dalpha_proxy: during=0.1147460937518499 delta_before=-0.007324218747228509 trend=decrease
softx_lower_proxy: during=0.0012397766114032 delta_before=0.0003623962402739999 trend=decrease
softx_upper_proxy: during=0.0004959106444581 delta_before=0.00022888183579449997 trend=decrease
te_profile_gradient_proxy: during=7.823835054669028 delta_before=-1.971481498683958 trend=increase
ne_profile_gradient_proxy: during=4.319395616165632e+17 delta_before=2.213597146910989e+16 trend=increase
density_proxy: during=6.357996796163549e+19 delta_before=6.106067456109838e+18 trend=increase
nbi_proxy: during=-0.5638450980186462 delta_before=-1.025172859430313 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_006 — positive_boundary_margin

```text
time: 0.1645999886393548 → 0.2115999886393549 s
duration: 0.0470000000000001 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.373388578481883 delta_before=0.06843471101658971 trend=decrease
C_edge_capacity: during=0.7373118211948124 delta_before=0.10458422170097437 trend=increase
F_route_fragmentation: during=0.3483668367526178 delta_before=0.027983806575229697 trend=increase
S_edge_response: during=0.6392356268240746 delta_before=0.05566092814355739 trend=increase
S_power_balance: during=0.5142653675378381 delta_before=0.029621314476984628 trend=increase
S_transport: during=0.21801174848795704 delta_before=0.02934270847809975 trend=increase
dalpha_proxy: during=0.12939453124724876 delta_before=0.01220703124823136 trend=increase
softx_lower_proxy: during=0.0006008148193444 delta_before=-0.0006580352784099 trend=decrease
softx_upper_proxy: during=0.004940032958928449 delta_before=0.00446319580077115 trend=increase
te_profile_gradient_proxy: during=10.906991507870789 delta_before=2.650700453076329 trend=decrease
ne_profile_gradient_proxy: during=4.676474340528111e+17 delta_before=3.035746330155891e+16 trend=increase
density_proxy: during=8.183415676299588e+19 delta_before=1.7534162616795005e+19 trend=increase
nbi_proxy: during=0.4613277614116668 delta_before=0.0 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.2125999886393549 → 0.2205999886393549 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high

m_edge: during=0.3423064440148888 delta_before=-0.1427765278342083 trend=increase
C_edge_capacity: during=0.7131074013471436 delta_before=-0.05610513327973521 trend=increase
F_route_fragmentation: during=0.3679314460295148 delta_before=0.06469563468119899 trend=decrease
S_edge_response: during=0.6339077093020136 delta_before=-0.023854064674932562 trend=increase
S_power_balance: during=0.5644455093251751 delta_before=0.3217874058396518 trend=decrease
S_transport: during=0.2086503121641954 delta_before=-0.1069256059305658 trend=increase
dalpha_proxy: during=0.1635742187475334 delta_before=0.01708984375109099 trend=increase
softx_lower_proxy: during=0.0009155273438984 delta_before=0.0006008148194467 trend=increase
softx_upper_proxy: during=0.0088500976564453 delta_before=0.0024414062502322005 trend=decrease
te_profile_gradient_proxy: during=9.096812070539167 delta_before=0.23537547786974145 trend=decrease
ne_profile_gradient_proxy: during=3.352543957232712e+17 delta_before=-3.369532066115424e+17 trend=decrease
density_proxy: during=7.58746586049151e+19 delta_before=-1.1219469426384437e+19 trend=decrease
nbi_proxy: during=0.4613277614116668 delta_before=1.025172859430313 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_007 — positive_boundary_margin

```text
time: 0.2135999886393549 → 0.2305999886393549 s
duration: 0.017000000000000015 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.357420397970175 delta_before=0.015113953955286197 trend=increase
C_edge_capacity: during=0.6770113534750966 delta_before=-0.08378953081840024 trend=decrease
F_route_fragmentation: during=0.36402056058575394 delta_before=-0.006780396746500772 trend=decrease
S_edge_response: during=0.5957542399241209 delta_before=-0.047848800992338236 trend=decrease
S_power_balance: during=0.5335166726072406 delta_before=-0.03092883671793456 trend=decrease
S_transport: during=0.23619588659403623 delta_before=-0.06512323897048838 trend=increase
dalpha_proxy: during=0.1745605468762807 delta_before=0.0280761718774801 trend=increase
softx_lower_proxy: during=0.0008153915405455 delta_before=0.0005006790160938001 trend=decrease
softx_upper_proxy: during=0.00617980957023305 delta_before=-0.00022888183598005016 trend=decrease
te_profile_gradient_proxy: during=9.08073391954128 delta_before=0.219297326871855 trend=decrease
ne_profile_gradient_proxy: during=2.6188912034467392e+17 delta_before=-4.043310149712599e+17 trend=decrease
density_proxy: during=7.2845257779787596e+19 delta_before=-1.3929747996666233e+19 trend=decrease
nbi_proxy: during=0.4613277614116668 delta_before=0.0 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_008 — positive_boundary_margin

```text
time: 0.2355999886393549 → 0.2415999886393549 s
duration: 0.005999999999999978 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4258601963338566 delta_before=0.07254352793140467 trend=increase
C_edge_capacity: during=0.5450036235290107 delta_before=-0.035467029716058085 trend=decrease
F_route_fragmentation: during=0.1181645429648329 delta_before=-0.0873699119997846 trend=decrease
S_edge_response: during=0.4200669938701923 delta_before=-0.0400141562448279 trend=decrease
S_power_balance: during=0.1462749711928866 delta_before=-0.012078421787964394 trend=decrease
S_transport: during=0.0509438536342336 delta_before=-0.198085170519247 trend=decrease
dalpha_proxy: during=0.2026367187391579 delta_before=-1.343061772907106e-11 trend=increase
softx_lower_proxy: during=-3.81469726086044e-05 delta_before=-0.0004196166991761044 trend=decrease
softx_upper_proxy: during=1.907348625363904e-05 delta_before=-0.001430511474642761 trend=decrease
te_profile_gradient_proxy: during=4.546238294238506 delta_before=-3.011293470064791 trend=decrease
ne_profile_gradient_proxy: during=1.6820851558375568e+17 delta_before=-8481127770404160.0 trend=decrease
density_proxy: during=6.956302205682975e+19 delta_before=-1.6010736479953224e+18 trend=increase
nbi_proxy: during=-0.5638450980186462 delta_before=0.0 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=increase
```

### positive_009 — positive_boundary_margin

```text
time: 0.2455999886393549 → 0.2495999886393549 s
duration: 0.0040000000000000036 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure

m_edge: during=0.3917319286026633 delta_before=-0.014579944655464472 trend=decrease
C_edge_capacity: during=0.4850138041035901 delta_before=-0.04008200754162494 trend=decrease
F_route_fragmentation: during=0.0901250870711325 delta_before=-0.029018340124021505 trend=increase
S_edge_response: during=0.396638447557017 delta_before=-0.0016806082701256164 trend=decrease
S_power_balance: during=0.0113874520992854 delta_before=-0.1348875190936012 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2758789062373758 delta_before=0.05126953124146191 trend=decrease
softx_lower_proxy: during=-0.0007438659666878 delta_before=-0.0004959106443952 trend=decrease
softx_upper_proxy: during=-0.0012969970703125 delta_before=-0.0010490417478972 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=5.46721469658594e+19 delta_before=-1.4753779185126212e+19 trend=decrease
nbi_proxy: during=-0.8566067218780518 delta_before=-0.2927616238594055 trend=increase
missingness_pressure: during=0.4444444444444444 delta_before=0.2222222222222222 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.2575999886393549 → 0.2605999886393549 s
duration: 0.0030000000000000027 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.275217390414082 delta_before=-0.2809624484843475 trend=decrease
C_edge_capacity: during=0.3908432453900649 delta_before=-0.027573222354958127 trend=decrease
F_route_fragmentation: during=0.6513085808040766 delta_before=0.299009034035512 trend=increase
S_edge_response: during=0.48650505278894773 delta_before=0.02791272167282316 trend=decrease
S_power_balance: during=0.6972783888839948 delta_before=0.36545548604340355 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.1403808593742546 delta_before=-0.047607421849887116 trend=increase
softx_lower_proxy: during=-0.00071048736577115 delta_before=-2.384185846524998e-05 trend=decrease
softx_upper_proxy: during=-0.0012493133544862 delta_before=0.0001239776610933998 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.6094741367338566e+19 delta_before=-8.607944592462991e+17 trend=decrease
nbi_proxy: during=0.4613277614116668 delta_before=1.025172859430313 trend=flat
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