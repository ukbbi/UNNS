# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12046_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     451
time_min: -0.0680000111460685
time_max: 0.3819999888539318
```

State counts:

```text
positive_boundary_margin: 181
boundary_ambiguous_margin: 143
negative_leakage_margin: 68
insufficient_data: 59
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                 |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:-------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| negative_001   | negative_leakage_margin  |  -0.00600001 | 0.00899999 |      0.015 |            16 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.321779 |                         0.375057 |                               0.711235 |                         0.542327 |                         0.770521 |                   nan        |                              0.444444 |
| peak_negative  | peak_negative_window     |  -0.00100001 | 0.00699999 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.335927 |                         0.321168 |                               0.600927 |                         0.462416 |                         0.635702 |                   nan        |                              0.444444 |
| positive_001   | positive_boundary_margin |   0.095      | 0.098      |      0.003 |             4 | weak_positive_candidate          | capacity_exceeds_fragmentation;m_edge_higher_than_before                                               |                0.220857 |                         0.607162 |                               0.381263 |                         0.507993 |                         0.372787 |                     0.487516 |                              0        |
| positive_002   | positive_boundary_margin |   0.105      | 0.119      |      0.014 |            15 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                            |                0.272684 |                         0.673479 |                               0.390302 |                         0.588076 |                         0.37883  |                     0.463798 |                              0        |
| positive_003   | positive_boundary_margin |   0.127      | 0.137      |      0.01  |            11 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                            |                0.348433 |                         0.695016 |                               0.331747 |                         0.619881 |                         0.361582 |                     0.439733 |                              0        |
| positive_004   | positive_boundary_margin |   0.144      | 0.165      |      0.021 |            22 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present;m_edge_higher_than_before |                0.364608 |                         0.780479 |                               0.413286 |                         0.686261 |                         0.36749  |                     0.557675 |                              0        |
| positive_005   | positive_boundary_margin |   0.167      | 0.183      |      0.016 |            17 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present;m_edge_higher_than_before |                0.305167 |                         0.82086  |                               0.515891 |                         0.741971 |                         0.394591 |                     0.748826 |                              0        |
| positive_006   | positive_boundary_margin |   0.188      | 0.258      |      0.07  |            71 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                            |                0.344553 |                         0.753181 |                               0.372136 |                         0.638974 |                         0.422334 |                     0.435767 |                              0        |
| peak_positive  | peak_positive_window     |   0.195      | 0.203      |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                            |                0.404131 |                         0.762472 |                               0.346253 |                         0.663879 |                         0.451617 |                     0.377645 |                              0        |
| positive_007   | positive_boundary_margin |   0.26       | 0.274      |      0.014 |            15 | weak_positive_candidate          | capacity_exceeds_fragmentation;m_edge_higher_than_before                                               |                0.288763 |                         0.634162 |                               0.330788 |                         0.396402 |                         0.392244 |                     0.357114 |                              0        |
| positive_008   | positive_boundary_margin |   0.282      | 0.285      |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                    |                0.320557 |                         0.481445 |                               0.168549 |                         0.137951 |                         0.23543  |                     0.134791 |                              0        |
| positive_009   | positive_boundary_margin |   0.287      | 0.29       |      0.003 |             4 | weak_positive_candidate          | capacity_exceeds_fragmentation                                                                         |                0.247709 |                         0.515888 |                               0.271846 |                         0.146794 |                         0.38594  |                     0.217968 |                              0        |
| negative_002   | negative_leakage_margin  |   0.328      | 0.331      |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.296615 |                         0.392954 |                               0.692051 |                         0.568161 |                         0.747075 |                   nan        |                              0.444444 |
| negative_003   | negative_leakage_margin  |   0.334      | 0.343      |      0.009 |            10 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.28902  |                         0.384392 |                               0.672961 |                         0.572177 |                         0.723742 |                   nan        |                              0.444444 |
| negative_004   | negative_leakage_margin  |   0.347      | 0.356      |      0.009 |            10 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.272085 |                         0.383619 |                               0.656708 |                         0.57451  |                         0.703878 |                   nan        |                              0.444444 |
| negative_005   | negative_leakage_margin  |   0.366      | 0.372      |      0.006 |             7 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.35348  |                         0.394686 |                               0.747582 |                         0.577154 |                         0.814946 |                   nan        |                              0.444444 |

## 6. Interpretability flags

```text
interpretable_positive_candidate: 7
interpretable_negative_candidate: 6
weak_positive_candidate: 3
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0060000111460685 → 0.0089999888539314 s
duration: 0.014999999999999899 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.3217785764791613 delta_before=-0.07380118545555608 trend=increase
C_edge_capacity: during=0.3750566499708692 delta_before=-0.04362869722673535 trend=decrease
F_route_fragmentation: during=0.7112346821411807 delta_before=-0.2887653178588193 trend=decrease
S_edge_response: during=0.5423268392563589 delta_before=-0.062175875191237906 trend=decrease
S_power_balance: during=0.7705214016293443 delta_before=0.05546582399410449 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.06469726562369554 delta_before=0.0683593749998509 trend=increase
softx_lower_proxy: during=0.00015258789036685 delta_before=-9.536743169879998e-05 trend=decrease
softx_upper_proxy: during=-9.536743168225331e-05 delta_before=3.8146972562446685e-05 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=9.365950657430815e+17 delta_before=-1.860839592249262e+17 trend=increase
nbi_proxy: during=1.244882196187973 delta_before=0.7324176803231239 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=-0.5555555555555556 trend=flat
```

### peak_negative — peak_negative_window

```text
time: -0.0010000111460685 → 0.0069999888539314 s
duration: 0.0079999999999999 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.3359270705515963 delta_before=-0.06570941061124774 trend=increase
C_edge_capacity: during=0.321168345156799 delta_before=-0.09761477591529633 trend=decrease
F_route_fragmentation: during=0.6009274908191742 delta_before=-0.14032288939319837 trend=decrease
S_edge_response: during=0.4624161325498624 delta_before=-0.14227234923924742 trend=decrease
S_power_balance: during=0.6357015011246696 delta_before=-0.10661764245021832 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.1538085937473538 delta_before=0.1586914062450058 trend=increase
softx_lower_proxy: during=0.0001525878907065 delta_before=3.653999845754097e-13 trend=decrease
softx_upper_proxy: during=-0.0001525878908556 delta_before=-0.0003051757812971 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=8.251499415412408e+17 delta_before=-1.65356240896e+17 trend=increase
nbi_proxy: during=-0.4393183887004852 delta_before=-1.3178079426288605 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.0949999888539315 → 0.0979999888539315 s
duration: 0.0030000000000000027 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation;m_edge_higher_than_before

m_edge: during=0.22085735443991425 delta_before=0.07419896583049376 trend=increase
C_edge_capacity: during=0.6071620284374835 delta_before=0.03703962730462851 trend=decrease
F_route_fragmentation: during=0.38126272549392026 delta_before=-0.03734144604330636 trend=decrease
S_edge_response: during=0.5079928167451748 delta_before=0.03512012844986073 trend=decrease
S_power_balance: during=0.37278698902214746 delta_before=-0.0454567689554114 trend=decrease
S_transport: during=0.48751601394796606 delta_before=0.005564800165896333 trend=decrease
dalpha_proxy: during=0.24169921875928005 delta_before=-0.024414062478924164 trend=increase
softx_lower_proxy: during=0.0027465820313686 delta_before=0.0007438659682658501 trend=increase
softx_upper_proxy: during=0.0109767913819585 delta_before=0.0018215179441582498 trend=increase
te_profile_gradient_proxy: during=11.467813788311606 delta_before=0.43535095001304214 trend=decrease
ne_profile_gradient_proxy: during=4.4943284700781696e+17 delta_before=6450276229949440.0 trend=increase
density_proxy: during=8.169232416105929e+19 delta_before=-4.536936819924664e+17 trend=decrease
nbi_proxy: during=-0.5125870257616043 delta_before=-0.6590265035629272 trend=flat
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.1049999888539315 → 0.1189999888539316 s
duration: 0.014000000000000096 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.2726840536740252 delta_before=0.07028486511695411 trend=decrease
C_edge_capacity: during=0.6734793822742653 delta_before=0.06701312203127319 trend=increase
F_route_fragmentation: during=0.3903024355244655 delta_before=-0.015156172550438052 trend=increase
S_edge_response: during=0.5880763598726999 delta_before=0.09690851136113982 trend=increase
S_power_balance: during=0.3788296793503507 delta_before=-0.016427465754117965 trend=increase
S_transport: during=0.4637982139423703 delta_before=0.02418726122463749 trend=increase
dalpha_proxy: during=0.1196289062700137 delta_before=-0.11718749999213611 trend=decrease
softx_lower_proxy: during=0.002613067625994 delta_before=-7.610999504248372e-13 trend=increase
softx_upper_proxy: during=0.01157760620222 delta_before=0.0011634826661571004 trend=increase
te_profile_gradient_proxy: during=9.271890155321271 delta_before=0.03167191484549292 trend=increase
ne_profile_gradient_proxy: during=5.545950287742419e+17 delta_before=7.34230273909319e+16 trend=increase
density_proxy: during=7.65580534600895e+19 delta_before=-4.44812266867943e+18 trend=decrease
nbi_proxy: during=-0.4393183887004852 delta_before=0.0 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.1269999888539316 → 0.1369999888539316 s
duration: 0.010000000000000009 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.3484327577782911 delta_before=0.14244118206558437 trend=decrease
C_edge_capacity: during=0.6950155494106425 delta_before=-0.0221631270515118 trend=decrease
F_route_fragmentation: during=0.3317472504804802 delta_before=-0.19561553033909757 trend=decrease
S_edge_response: during=0.619880833546856 delta_before=-0.0707663003580199 trend=decrease
S_power_balance: during=0.3615815013961632 delta_before=-0.16851497006179916 trend=increase
S_transport: during=0.4397326780202344 delta_before=-0.18784463930059414 trend=decrease
dalpha_proxy: during=0.0708007812424343 delta_before=-0.006103515636050355 trend=decrease
softx_lower_proxy: during=0.0043106079105577 delta_before=0.0006008148189189993 trend=increase
softx_upper_proxy: during=0.0101280212389468 delta_before=-0.0015640258812521478 trend=decrease
te_profile_gradient_proxy: during=7.457571418545001 delta_before=-6.350349426472684 trend=decrease
ne_profile_gradient_proxy: during=5.577912674709618e+17 delta_before=-4957669691187392.0 trend=increase
density_proxy: during=7.18382326720936e+19 delta_before=5.908313692784558e+17 trend=decrease
nbi_proxy: during=-0.4393183887004852 delta_before=-2.1968854367733 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.1439999888539316 → 0.1649999888539316 s
duration: 0.02100000000000002 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.364608058554017 delta_before=0.05005996658025952 trend=increase
C_edge_capacity: during=0.7804793048529735 delta_before=0.0782817718168185 trend=increase
F_route_fragmentation: during=0.41328632617269007 delta_before=0.029900228813380947 trend=decrease
S_edge_response: during=0.686261369435743 delta_before=0.06638053588888704 trend=increase
S_power_balance: during=0.36748980514358986 delta_before=-0.06293511737474444 trend=decrease
S_transport: during=0.5576753148622475 delta_before=0.12794458107052142 trend=increase
dalpha_proxy: during=0.10131835938332964 delta_before=0.028076171844383144 trend=increase
softx_lower_proxy: during=0.00822067260696065 delta_before=0.0031089782698780506 trend=increase
softx_upper_proxy: during=0.012817382812961749 delta_before=0.0035476684580870495 trend=increase
te_profile_gradient_proxy: during=12.704007842307245 delta_before=5.3106970268782305 trend=increase
ne_profile_gradient_proxy: during=5.110842407256789e+17 delta_before=-5.678184929653818e+16 trend=decrease
density_proxy: during=7.536194313874362e+19 delta_before=5.805412598564258e+18 trend=increase
nbi_proxy: during=-0.4393183887004852 delta_before=-0.585757866501808 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_005 — positive_boundary_margin

```text
time: 0.1669999888539316 → 0.1829999888539316 s
duration: 0.015999999999999986 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.3051665957295461 delta_before=0.009397941959431999 trend=increase
C_edge_capacity: during=0.8208597920945484 delta_before=0.037385590346684205 trend=increase
F_route_fragmentation: during=0.5158905813488502 delta_before=0.022105459991187126 trend=decrease
S_edge_response: during=0.7419705356141031 delta_before=0.04903716553646509 trend=increase
S_power_balance: during=0.394591075882398 delta_before=-0.14287777203931312 trend=decrease
S_transport: during=0.7488260474897092 delta_before=0.17925272454381724 trend=increase
dalpha_proxy: during=0.2539062499818125 delta_before=0.1196289062404218 trend=increase
softx_lower_proxy: during=0.0090789794923945 delta_before=0.0005531311025068 trend=increase
softx_upper_proxy: during=0.0243377685537091 delta_before=0.010890960694099498 trend=increase
te_profile_gradient_proxy: during=19.22354305851329 delta_before=5.128742149259965 trend=increase
ne_profile_gradient_proxy: during=4.969779127785789e+17 delta_before=3804050668858816.0 trend=decrease
density_proxy: during=8.109893972578114e+19 delta_before=3.6073041366865674e+18 trend=increase
nbi_proxy: during=-0.4393183887004852 delta_before=-2.1968854367733 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_006 — positive_boundary_margin

```text
time: 0.1879999888539316 → 0.2579999888539317 s
duration: 0.07000000000000012 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.3445526202296375 delta_before=0.03938602450009143 trend=increase
C_edge_capacity: during=0.7531810558848103 delta_before=-0.052629828880085716 trend=decrease
F_route_fragmentation: during=0.372135707183754 delta_before=-0.14375487416509625 trend=decrease
S_edge_response: during=0.6389735426109737 delta_before=-0.07841964681054991 trend=decrease
S_power_balance: during=0.4223342737436927 delta_before=0.0549917293295939 trend=decrease
S_transport: during=0.4357669877635114 delta_before=-0.2865810038173814 trend=decrease
dalpha_proxy: during=0.2636718749807012 delta_before=-0.039062500019298785 trend=increase
softx_lower_proxy: during=0.0139427185077601 delta_before=0.0016593933141876988 trend=increase
softx_upper_proxy: during=0.0200653076192468 delta_before=-0.007476806635158099 trend=decrease
te_profile_gradient_proxy: during=14.925031343794718 delta_before=-3.571271876320349 trend=decrease
ne_profile_gradient_proxy: during=2.335522461022738e+17 delta_before=-2.040564639432686e+17 trend=decrease
density_proxy: during=7.59253944694672e+19 delta_before=-1.8905882537282765e+18 trend=increase
nbi_proxy: during=0.1464394778013229 delta_before=0.7322951406240463 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.1949999888539316 → 0.2029999888539316 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.4041310346479213 delta_before=0.07116154240951178 trend=increase
C_edge_capacity: during=0.7624724947951196 delta_before=-0.013812656183350813 trend=increase
F_route_fragmentation: during=0.3462528333985165 delta_before=-0.1148387789469349 trend=decrease
S_edge_response: during=0.663879123453098 delta_before=-0.023675068326047155 trend=increase
S_power_balance: during=0.4516168661679174 delta_before=0.0459994082447312 trend=decrease
S_transport: during=0.3776452752667619 delta_before=-0.25329340220209745 trend=decrease
dalpha_proxy: during=0.224609375 delta_before=-0.06103515625 trend=decrease
softx_lower_proxy: during=0.0153923034654189 delta_before=0.0023841857912151997 trend=increase
softx_upper_proxy: during=0.0256347656257075 delta_before=0.00019073486288340158 trend=increase
te_profile_gradient_proxy: during=13.768321892193246 delta_before=-4.437085392562533 trend=increase
ne_profile_gradient_proxy: during=1.9830939507051197e+17 delta_before=-1.3876438146952144e+17 trend=increase
density_proxy: during=7.511206372816873e+19 delta_before=2.3512880238129316e+18 trend=decrease
nbi_proxy: during=0.7321973443031311 delta_before=0.5857578665018082 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_007 — positive_boundary_margin

```text
time: 0.2599999888539317 → 0.2739999888539317 s
duration: 0.013999999999999957 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation;m_edge_higher_than_before

m_edge: during=0.2887629151573915 delta_before=0.01502625697497989 trend=decrease
C_edge_capacity: during=0.6341620608280409 delta_before=-0.01580861551657553 trend=decrease
F_route_fragmentation: during=0.3307878835741091 delta_before=-0.04057060291578818 trend=decrease
S_edge_response: during=0.3964021832633697 delta_before=-0.0586417739339416 trend=decrease
S_power_balance: during=0.392244368815707 delta_before=-0.046315157512640204 trend=increase
S_transport: during=0.3571137944096954 delta_before=-0.004142340847948511 trend=decrease
dalpha_proxy: during=0.3833007813120705 delta_before=0.053710937525844604 trend=increase
softx_lower_proxy: during=0.0067710876463868 delta_before=-0.0032997131318545005 trend=decrease
softx_upper_proxy: during=0.0066757202142672 delta_before=0.0004005432124087995 trend=decrease
te_profile_gradient_proxy: during=11.781654901384227 delta_before=-2.090695636161053 trend=decrease
ne_profile_gradient_proxy: during=2.8764876645718445e+17 delta_before=3.3363817396347264e+16 trend=decrease
density_proxy: during=8.790522456497036e+19 delta_before=5.748106052524573e+18 trend=decrease
nbi_proxy: during=-0.5858556628227234 delta_before=-0.7322951406240463 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_008 — positive_boundary_margin

```text
time: 0.2819999888539317 → 0.2849999888539317 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.32055652103277066 delta_before=0.10363435505937146 trend=increase
C_edge_capacity: during=0.4814451865749414 delta_before=0.010405524648165687 trend=increase
F_route_fragmentation: during=0.16854865618397144 delta_before=-0.09198625509968364 trend=decrease
S_edge_response: during=0.13795139190171907 delta_before=-0.0025887405310342226 trend=increase
S_power_balance: during=0.2354298098895941 delta_before=-0.18723730825845059 trend=decrease
S_transport: during=0.1347909085833044 delta_before=-0.0027551157493027056 trend=increase
dalpha_proxy: during=0.4895019531710176 delta_before=0.023193359484748377 trend=increase
softx_lower_proxy: during=-0.00023841858097754998 delta_before=1.9073485155450033e-05 trend=increase
softx_upper_proxy: during=1.1031280733710472e-12 delta_before=5.7220459579283305e-05 trend=decrease
te_profile_gradient_proxy: during=8.89028927582089 delta_before=2.2071262477075297 trend=increase
ne_profile_gradient_proxy: during=1.2913767274141549e+17 delta_before=-6.572828922176333e+16 trend=decrease
density_proxy: during=7.264076840823056e+19 delta_before=2.809021311525847e+18 trend=increase
nbi_proxy: during=-2.12383371591568 delta_before=-2.270273193717003 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_009 — positive_boundary_margin

```text
time: 0.2869999888539317 → 0.2899999888539317 s
duration: 0.0030000000000000027 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation

m_edge: during=0.24770902590503113 delta_before=-0.010465367547545068 trend=decrease
C_edge_capacity: during=0.5158879498614677 delta_before=0.0372095637461346 trend=increase
F_route_fragmentation: during=0.27184584958510727 delta_before=0.032128286940813766 trend=increase
S_edge_response: during=0.14679383217170466 delta_before=0.007050246143941952 trend=decrease
S_power_balance: during=0.38593997138272595 delta_before=0.015224647476369368 trend=increase
S_transport: during=0.21796814950186288 delta_before=0.07309568101340178 trend=increase
dalpha_proxy: during=0.5249023437500339 delta_before=0.034179687394486846 trend=increase
softx_lower_proxy: during=8.106231629586654e-05 delta_before=0.00030994415176946655 trend=decrease
softx_upper_proxy: during=0.00027179717926470004 delta_before=0.0003194808940717494 trend=decrease
te_profile_gradient_proxy: during=11.141650850387384 delta_before=2.943253806819852 trend=increase
ne_profile_gradient_proxy: during=9.014765547144851e+16 delta_before=-5.708259690733805e+16 trend=increase
density_proxy: during=8.13752250076087e+19 delta_before=9.873539650637791e+18 trend=increase
nbi_proxy: during=-0.5125870257616043 delta_before=0.07326863706111908 trend=increase
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