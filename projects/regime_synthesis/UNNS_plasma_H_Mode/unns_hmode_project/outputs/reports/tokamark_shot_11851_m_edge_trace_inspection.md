# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11851_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     415
time_min: -0.0680000111460685
time_max: 0.3459999888539318
```

State counts:

```text
boundary_ambiguous_margin: 173
negative_leakage_margin: 118
positive_boundary_margin: 65
insufficient_data: 59
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| peak_negative  | peak_negative_window     |  -0.00100001 | 0.00699999 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before |               -0.402811 |                         0.309915 |                              0.703167  |                        0.306955  |                        0.760661  |                              |                              0.444444 |
| negative_001   | negative_leakage_margin  |   0.00499999 | 0.00799999 |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low                          |               -0.331294 |                         0.277851 |                              0.636128  |                        0.264561  |                        0.678724  |                              |                              0.444444 |
| negative_002   | negative_leakage_margin  |   0.013      | 0.02       |      0.007 |             8 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before |               -0.325868 |                         0.289416 |                              0.629342  |                        0.198194  |                        0.670431  |                              |                              0.444444 |
| negative_003   | negative_leakage_margin  |   0.08       | 0.083      |      0.003 |             4 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before |               -0.284077 |                         0.334699 |                              0.618776  |                        0.104421  |                        0.7069    |                              |                              0.222222 |
| negative_004   | negative_leakage_margin  |   0.097      | 0.103      |      0.006 |             7 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before |               -0.215145 |                         0.442155 |                              0.6573    |                        0.21131   |                        0.753984  |                              |                              0.222222 |
| positive_001   | positive_boundary_margin |   0.188      | 0.194      |      0.006 |             7 | weak_positive_candidate          | capacity_exceeds_fragmentation;m_edge_higher_than_before                                              |                0.25198  |                         0.641377 |                              0.388843  |                        0.488381  |                        0.42587   |                              |                              0.222222 |
| peak_positive  | peak_positive_window     |   0.201      | 0.209      |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                           |                0.255393 |                         0.691443 |                              0.450132  |                        0.641383  |                        0.500779  |                              |                              0.222222 |
| positive_002   | positive_boundary_margin |   0.203      | 0.212      |      0.009 |            10 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                           |                0.288064 |                         0.682443 |                              0.399869  |                        0.646778  |                        0.439346  |                              |                              0.222222 |
| positive_003   | positive_boundary_margin |   0.214      | 0.218      |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high                                                     |                0.221737 |                         0.663092 |                              0.442167  |                        0.641388  |                        0.491044  |                              |                              0.222222 |
| positive_004   | positive_boundary_margin |   0.256      | 0.259      |      0.003 |             4 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                   |                0.495112 |                         0.573094 |                              0.0723002 |                        0.510845  |                        0.0389842 |                              |                              0.222222 |
| negative_005   | negative_leakage_margin  |   0.271      | 0.276      |      0.005 |             6 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before |               -0.454185 |                         0.155362 |                              0.615254  |                        0.0420018 |                        0.653211  |                              |                              0.444444 |
| negative_006   | negative_leakage_margin  |   0.28       | 0.289      |      0.009 |            10 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                   |               -0.406605 |                         0.393289 |                              0.801535  |                        0.568693  |                        0.880889  |                              |                              0.444444 |
| negative_007   | negative_leakage_margin  |   0.291      | 0.3        |      0.009 |            10 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                   |               -0.382317 |                         0.388159 |                              0.770586  |                        0.577148  |                        0.843062  |                              |                              0.444444 |
| negative_008   | negative_leakage_margin  |   0.302      | 0.32       |      0.018 |            19 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high                                            |               -0.337538 |                         0.388192 |                              0.723572  |                        0.577398  |                        0.785601  |                              |                              0.444444 |
| negative_009   | negative_leakage_margin  |   0.326      | 0.33       |      0.004 |             5 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                   |               -0.337825 |                         0.388422 |                              0.727214  |                        0.580534  |                        0.790051  |                              |                              0.444444 |
| negative_010   | negative_leakage_margin  |   0.332      | 0.337      |      0.005 |             6 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                   |               -0.326286 |                         0.393402 |                              0.720599  |                        0.581233  |                        0.781966  |                              |                              0.444444 |
| negative_011   | negative_leakage_margin  |   0.341      | 0.346      |      0.005 |             6 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                   |               -0.417085 |                         0.389472 |                              0.817707  |                        0.582591  |                        0.900654  |                              |                              0.444444 |

## 6. Interpretability flags

```text
interpretable_negative_candidate: 12
interpretable_positive_candidate: 4
weak_positive_candidate: 1
```

## 7. Detailed window notes

### peak_negative — peak_negative_window

```text
time: -0.0010000111460685 → 0.0069999888539314 s
duration: 0.0079999999999999 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.4028112070268075 delta_before=-0.1226179569017648 trend=increase
C_edge_capacity: during=0.3099150851809766 delta_before=-0.11484145961135878 trend=decrease
F_route_fragmentation: during=0.7031674068783597 delta_before=-0.0039252258580495525 trend=decrease
S_edge_response: during=0.306955422951268 delta_before=-0.3062221253934625 trend=decrease
S_power_balance: during=0.7606613985303408 delta_before=-0.004790704447980021 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2978515625 delta_before=0.302734375 trend=increase
softx_lower_proxy: during=-0.0001907348631112 delta_before=-9.536743164614906e-05 trend=decrease
softx_upper_proxy: during=-0.0001049041749927 delta_before=-0.00018119812023415513 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-3.993439975977779e+17 delta_before=2.0585365932867584e+17 trend=increase
nbi_proxy: during=0.9520930051803588 delta_before=0.7324150651693344 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

### negative_001 — negative_leakage_margin

```text
time: 0.0049999888539314 → 0.0079999888539314 s
duration: 0.003000000000000001 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low

m_edge: during=-0.33129405720491056 delta_before=0.053937068159670254 trend=increase
C_edge_capacity: during=0.2778506213786748 delta_before=-0.1227082851016571 trend=increase
F_route_fragmentation: during=0.6361277485504786 delta_before=-0.07095932560350104 trend=decrease
S_edge_response: during=0.2645612038492584 delta_before=-0.3128491394841456 trend=increase
S_power_balance: during=0.6787240383518196 delta_before=-0.08672806462650118 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.34057617187637895 delta_before=0.30883789062637895 trend=decrease
softx_lower_proxy: during=-0.00021457672108829998 delta_before=-0.00011920928962324905 trend=decrease
softx_upper_proxy: during=-0.0003528594971582 delta_before=-0.0003337860107281663 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=2.9788984968451457e+19 delta_before=3.0490389824088834e+19 trend=increase
nbi_proxy: during=0.5858854725956916 delta_before=-0.3662075325846672 trend=flat
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.0129999888539314 → 0.0199999888539315 s
duration: 0.007000000000000102 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.3258681025947934 delta_before=-0.02763113672041717 trend=increase
C_edge_capacity: during=0.2894155631575721 delta_before=0.04566313912689912 trend=increase
F_route_fragmentation: during=0.6293422373359681 delta_before=0.08003266397901865 trend=increase
S_edge_response: during=0.1981941963410423 delta_before=0.0063630098900479826 trend=increase
S_power_balance: during=0.6704306357563066 delta_before=0.09781770041880056 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.4211425781282424 delta_before=0.0012207031665181223 trend=decrease
softx_lower_proxy: during=0.00041007995596495004 delta_before=0.0004959106444975623 trend=increase
softx_upper_proxy: during=-4.768371506750011e-06 delta_before=0.00031948089615865 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=4.844729926860092e+19 delta_before=9.547061663002264e+18 trend=increase
nbi_proxy: during=0.9520930051803588 delta_before=0.7324150651693344 trend=increase
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

### negative_003 — negative_leakage_margin

```text
time: 0.0799999888539315 → 0.0829999888539315 s
duration: 0.0030000000000000027 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.2840774837245118 delta_before=-0.10539457013538461 trend=decrease
C_edge_capacity: during=0.3346989022179435 delta_before=-0.004569937771229882 trend=decrease
F_route_fragmentation: during=0.6187763859424553 delta_before=0.10388636544828034 trend=increase
S_edge_response: during=0.1044212005685113 delta_before=-0.008542549115993794 trend=decrease
S_power_balance: during=0.7068995334358406 delta_before=0.12697222443678702 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.5249023437613112 delta_before=0.00854492187781375 trend=increase
softx_lower_proxy: during=0.0009346008298189499 delta_before=0.00012874603275659995 trend=decrease
softx_upper_proxy: during=0.00026702880863460003 delta_before=2.8610229189700027e-05 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=8.987696997096804e+19 delta_before=2.789716086365356e+18 trend=increase
nbi_proxy: during=0.9520930051803588 delta_before=0.7324150651693344 trend=flat
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### negative_004 — negative_leakage_margin

```text
time: 0.0969999888539315 → 0.1029999888539315 s
duration: 0.0059999999999999915 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.2151451847486945 delta_before=-0.08558995782314463 trend=decrease
C_edge_capacity: during=0.4421552572316755 delta_before=0.03011627540982237 trend=increase
F_route_fragmentation: during=0.6573004419803701 delta_before=0.12178888556549072 trend=increase
S_edge_response: during=0.2113095816780003 delta_before=0.009673643678609456 trend=increase
S_power_balance: during=0.7539844908155141 delta_before=0.14885308235782202 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.4980468750062985 delta_before=-0.00854492185002953 trend=decrease
softx_lower_proxy: during=0.0011825561525359 delta_before=1.9073486541399927e-05 trend=decrease
softx_upper_proxy: during=0.0068092346186601 delta_before=0.00111579894999055 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.0086247651710127e+20 delta_before=8.726678654123229e+18 trend=increase
nbi_proxy: during=0.9520930051803588 delta_before=0.7324150651693344 trend=flat
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.1879999888539316 → 0.1939999888539316 s
duration: 0.006000000000000005 s
flag: weak_positive_candidate
notes: capacity_exceeds_fragmentation;m_edge_higher_than_before

m_edge: during=0.2519803507337002 delta_before=0.13827361380452738 trend=increase
C_edge_capacity: during=0.6413773111655195 delta_before=0.04536897405801654 trend=increase
F_route_fragmentation: during=0.3888431629193278 delta_before=-0.11670975776834208 trend=decrease
S_edge_response: during=0.4883813328161202 delta_before=0.09519762543773119 trend=increase
S_power_balance: during=0.4258700386297957 delta_before=-0.1426452594946404 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.478515624971377 delta_before=-0.014648437547183202 trend=decrease
softx_lower_proxy: during=0.011978149406534 delta_before=-0.00015258789887850031 trend=decrease
softx_upper_proxy: during=0.0170326232907875 delta_before=0.004444122315244098 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=7.874886116475876e+19 delta_before=-5.618838669470204e+18 trend=decrease
nbi_proxy: during=-0.5124955773353577 delta_before=-0.732173517346382 trend=flat
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.2009999888539316 → 0.2089999888539316 s
duration: 0.00799999999999998 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.2553930761025281 delta_before=0.038616968113881794 trend=increase
C_edge_capacity: during=0.6914426120123691 delta_before=0.023812766714013334 trend=decrease
F_route_fragmentation: during=0.4501323163739635 delta_before=0.0612891534546357 trend=decrease
S_edge_response: during=0.641383372799273 delta_before=0.12207640968528843 trend=decrease
S_power_balance: during=0.5007790039632394 delta_before=0.07490896533344366 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2758789061880378 delta_before=-0.16601562504220263 trend=decrease
softx_lower_proxy: during=0.0093078613300333 delta_before=-0.0019264221179892994 trend=decrease
softx_upper_proxy: during=0.0149536132783988 delta_before=-0.0018882751501775995 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=7.1932021013942895e+19 delta_before=-4.93461698155171e+18 trend=decrease
nbi_proxy: during=0.2196779400110244 delta_before=0.732173517346382 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.2029999888539316 → 0.2119999888539316 s
duration: 0.00899999999999998 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.2880640916034523 delta_before=0.08957119363956112 trend=decrease
C_edge_capacity: during=0.6824432193530379 delta_before=0.006310116628763129 trend=increase
F_route_fragmentation: during=0.3998686205423013 delta_before=-0.08268243974562489 trend=increase
S_edge_response: during=0.6467780374250773 delta_before=0.06320106866528075 trend=increase
S_power_balance: during=0.4393455979467634 delta_before=-0.10105631524465275 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2575683593953389 delta_before=-0.10864257812478662 trend=decrease
softx_lower_proxy: during=0.008897781372671651 delta_before=-0.0019931793235865494 trend=decrease
softx_upper_proxy: during=0.01440048217705395 delta_before=-0.0022888183627568504 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=7.010174317202139e+19 delta_before=-5.421106896377479e+18 trend=decrease
nbi_proxy: during=-0.14640881866216665 delta_before=-0.36608675867319107 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.2139999888539316 → 0.2179999888539316 s
duration: 0.0040000000000000036 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high

m_edge: during=0.2217365319843784 delta_before=-0.013109478826219212 trend=decrease
C_edge_capacity: during=0.6630915069117683 delta_before=-0.02506842329030612 trend=decrease
F_route_fragmentation: during=0.4421669781239084 delta_before=-0.0063722860231462675 trend=increase
S_edge_response: during=0.6413882676538546 delta_before=-0.010037992267349138 trend=decrease
S_power_balance: during=0.4910435905465054 delta_before=-0.007788349583845389 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2124023438243762 delta_before=-0.03906249991537811 trend=decrease
softx_lower_proxy: during=0.0085449218748357 delta_before=-0.00022888183794280044 trend=decrease
softx_upper_proxy: during=0.0108146667480468 delta_before=-0.0021171569829866992 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=6.729231064314675e+19 delta_before=-1.718448713283666e+18 trend=increase
nbi_proxy: during=0.2196779400110244 delta_before=0.0 trend=flat
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.2559999888539317 → 0.2589999888539317 s
duration: 0.0030000000000000027 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4951123288070455 delta_before=0.37474776250123437 trend=increase
C_edge_capacity: during=0.5730935407896505 delta_before=0.013614920944178488 trend=increase
F_route_fragmentation: during=0.0723001879228384 delta_before=-0.386896748310948 trend=decrease
S_edge_response: during=0.510844530141806 delta_before=0.03429994382589979 trend=increase
S_power_balance: during=0.038984180300753096 delta_before=-0.4728738034911587 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.17944335939929965 delta_before=-0.018310546850700354 trend=decrease
softx_lower_proxy: during=0.00410079956278475 delta_before=0.00066757202287845 trend=increase
softx_upper_proxy: during=0.00191688537507225 delta_before=0.0004863739004629501 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=5.486315852388316e+19 delta_before=-3.072193817680544e+18 trend=increase
nbi_proxy: during=-2.856279134750366 delta_before=-3.0759570747613907 trend=flat
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### negative_005 — negative_leakage_margin

```text
time: 0.2709999888539317 → 0.2759999888539317 s
duration: 0.0050000000000000044 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.4541854822241766 delta_before=-0.4914885000275023 trend=increase
C_edge_capacity: during=0.15536208959698 delta_before=-0.41651583758932326 trend=increase
F_route_fragmentation: during=0.6152536456335377 delta_before=0.056927121710895756 trend=increase
S_edge_response: during=0.042001768342937694 delta_before=-0.4915879118999412 trend=increase
S_power_balance: during=0.6532112458977807 delta_before=0.04569672480690601 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.799560546919493 delta_before=0.6237792969441586 trend=decrease
softx_lower_proxy: during=-0.00111103057826495 delta_before=-0.00618457794106125 trend=decrease
softx_upper_proxy: during=-0.0021934509301674 delta_before=-0.0050735473644383 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=2.5619779812436476e+19 delta_before=-3.1935990328893374e+19 trend=decrease
nbi_proxy: during=0.2196779400110244 delta_before=0.0 trend=increase
missingness_pressure: during=0.4444444444444444 delta_before=0.2222222222222222 trend=flat
```

### negative_006 — negative_leakage_margin

```text
time: 0.2799999888539317 → 0.2889999888539317 s
duration: 0.009000000000000008 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.40660466569479103 delta_before=-0.01380613303666256 trend=increase
C_edge_capacity: during=0.393289193291884 delta_before=0.030835947688642118 trend=decrease
F_route_fragmentation: during=0.8015350750804706 delta_before=0.21902726064914502 trend=decrease
S_edge_response: during=0.5686930449776777 delta_before=0.13416744799058422 trend=increase
S_power_balance: during=0.8808885485551432 delta_before=0.2676999852378439 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-1.0842021724855125e-13 delta_before=-0.2832031248993318 trend=decrease
softx_lower_proxy: during=-0.0015926361082444999 delta_before=-0.00016212463393569998 trend=decrease
softx_upper_proxy: during=-0.0021362304679313 delta_before=7.191001266670938e-13 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-1.5641295075462344e+18 delta_before=-1.8035332661119025e+19 trend=decrease
nbi_proxy: during=0.9520930051803588 delta_before=0.7324150651693344 trend=decrease
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