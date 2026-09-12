# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12055_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     341
time_min: -0.050400011241436
time_max: 0.2895999887585643
```

State counts:

```text
positive_boundary_margin: 154
boundary_ambiguous_margin: 118
insufficient_data: 41
negative_leakage_margin: 28
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                         |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:---------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| negative_001   | negative_leakage_margin  |  -0.00940001 | 0.00459999 |      0.014 |            15 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high                                                     |               -0.282957 |                         0.492949 |                               0.786118 |                         0.727643 |                        0.867101  |                     0.655335 |                              0.444444 |
| peak_negative  | peak_negative_window     |   0.00859999 | 0.0166     |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before          |               -0.323448 |                         0.271957 |                               0.623826 |                         0.250122 |                        0.836253  |                     0.500645 |                              0.222222 |
| negative_002   | negative_leakage_margin  |   0.0106     | 0.0196     |      0.009 |            10 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before          |               -0.311258 |                         0.288773 |                               0.626425 |                         0.248172 |                        0.794754  |                     0.512517 |                              0.222222 |
| positive_001   | positive_boundary_margin |   0.0736     | 0.0776     |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before |                0.213362 |                         0.475704 |                               0.260662 |                         0.363757 |                        0.0112732 |                     0.567975 |                              0        |
| positive_002   | positive_boundary_margin |   0.0796     | 0.2236     |      0.144 |           145 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                            |                0.376682 |                         0.632622 |                               0.246987 |                         0.469659 |                        0.0986326 |                     0.458146 |                              0        |
| peak_positive  | peak_positive_window     |   0.1546     | 0.1626     |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                            |                0.479627 |                         0.658477 |                               0.173594 |                         0.496744 |                        0.117875  |                     0.26314  |                              0        |

## 6. Interpretability flags

```text
interpretable_negative_candidate: 3
interpretable_positive_candidate: 3
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0094000112414359 → 0.004599988758564 s
duration: 0.013999999999999901 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high

m_edge: during=-0.28295725341508 delta_before=0.07532639208673059 trend=increase
C_edge_capacity: during=0.4929491989321476 delta_before=-0.020736209475223477 trend=decrease
F_route_fragmentation: during=0.7861180308172142 delta_before=-0.2138819691827858 trend=decrease
S_edge_response: during=0.7276425021551054 delta_before=-0.025964504412235412 trend=decrease
S_power_balance: during=0.8671010723491887 delta_before=-0.09987345032993455 trend=decrease
S_transport: during=0.6553347212586691 delta_before=None trend=flat
dalpha_proxy: during=-0.0048828125 delta_before=0.0 trend=flat
softx_lower_proxy: during=0.000171661376937 delta_before=-0.0001335144042885 trend=decrease
softx_upper_proxy: during=-8.536503921547594e-15 delta_before=-3.814697266315862e-05 trend=increase
te_profile_gradient_proxy: during=55.734466891062006 delta_before=None trend=flat
ne_profile_gradient_proxy: during=3.707594094516121e+17 delta_before=None trend=flat
density_proxy: during=3.780234500869456e+18 delta_before=-5.574001684801126e+16 trend=increase
nbi_proxy: during=941156.875 delta_before=-166464.0 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=-0.5555555555555556 trend=decrease
```

### peak_negative — peak_negative_window

```text
time: 0.008599988758564 → 0.016599988758564 s
duration: 0.008 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.3234481777973085 delta_before=-0.05094881777392879 trend=decrease
C_edge_capacity: during=0.2719571963553676 delta_before=-0.2116332351085201 trend=decrease
F_route_fragmentation: during=0.6238263903527005 delta_before=-0.14845470243197267 trend=increase
S_edge_response: during=0.2501217399464368 delta_before=-0.4629252801344321 trend=decrease
S_power_balance: during=0.8362532507594 delta_before=-0.0424437950056904 trend=decrease
S_transport: during=0.5006449006416627 delta_before=-0.06431992284268317 trend=increase
dalpha_proxy: during=0.8081054687574911 delta_before=0.8129882812574911 trend=increase
softx_lower_proxy: during=0.0002670288085162 delta_before=0.00017166137686356434 trend=decrease
softx_upper_proxy: during=-0.0003433227539014 delta_before=-0.00032424926759598604 trend=increase
te_profile_gradient_proxy: during=15.63032978134001 delta_before=-17.917499003847908 trend=increase
ne_profile_gradient_proxy: during=1.2724680879804349e+17 delta_before=-1.0125237473794512e+17 trend=increase
density_proxy: during=2.70063981154806e+19 delta_before=2.286653892481096e+19 trend=increase
nbi_proxy: during=1069637.625 delta_before=106229.0 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=-0.2222222222222222 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.010599988758564 → 0.019599988758564 s
duration: 0.009 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.311258368370532 delta_before=-0.08231958569828401 trend=increase
C_edge_capacity: during=0.28877275930544766 delta_before=-0.19393781023313023 trend=increase
F_route_fragmentation: during=0.6264245931119281 delta_before=-0.06577869727176322 trend=increase
S_edge_response: during=0.24817159616000972 delta_before=-0.4571944035707901 trend=decrease
S_power_balance: during=0.7947543017914784 delta_before=-0.08418819027048563 trend=decrease
S_transport: during=0.5125173879447953 delta_before=-0.007262486652388822 trend=increase
dalpha_proxy: during=0.7958984375002796 delta_before=0.8007812500000101 trend=increase
softx_lower_proxy: during=0.0001430511474536 delta_before=-8.58306884667e-05 trend=decrease
softx_upper_proxy: during=-0.0002861022949287 delta_before=-0.00026702880862328605 trend=decrease
te_profile_gradient_proxy: during=14.001646897639475 delta_before=-8.452862834611409 trend=decrease
ne_profile_gradient_proxy: during=2.3679759876555994e+17 delta_before=7.942852818738307e+16 trend=increase
density_proxy: during=3.963039688932563e+19 delta_before=3.5324335521001374e+19 trend=increase
nbi_proxy: during=1086910.5 delta_before=116843.125 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.0735999887585641 → 0.0775999887585641 s
duration: 0.00399999999999999 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;transport_pressure_present;m_edge_higher_than_before

m_edge: during=0.2133617258424954 delta_before=0.03997725667432778 trend=increase
C_edge_capacity: during=0.4757043029524435 delta_before=0.019248154070127588 trend=increase
F_route_fragmentation: during=0.2606615775348535 delta_before=-0.025673604831624897 trend=increase
S_edge_response: during=0.3637574587937917 delta_before=0.006298205672093327 trend=increase
S_power_balance: during=0.0112731572397804 delta_before=0.009343021562216799 trend=increase
S_transport: during=0.5679747928376718 delta_before=-0.06764019806438137 trend=increase
dalpha_proxy: during=0.480957031253151 delta_before=-0.0170898437482771 trend=decrease
softx_lower_proxy: during=0.0002479553221819 delta_before=0.0001096725462903 trend=increase
softx_upper_proxy: during=7.629394534227851e-05 delta_before=0.00011444091800110931 trend=decrease
te_profile_gradient_proxy: during=7.999845495333844 delta_before=-1.9573574133173395 trend=increase
ne_profile_gradient_proxy: during=8.812301374819269e+17 delta_before=3.452883938867469e+16 trend=increase
density_proxy: during=7.021250797340354e+19 delta_before=2.7979250401783316e+18 trend=increase
nbi_proxy: during=1196.528564453125 delta_before=890.6170043945312 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.0795999887585641 → 0.2235999887585642 s
duration: 0.14400000000000013 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3766824834831223 delta_before=0.17646556249822468 trend=increase
C_edge_capacity: during=0.6326216111566909 delta_before=0.16677858692359804 trend=decrease
F_route_fragmentation: during=0.2469869499672358 delta_before=-0.03174594134468439 trend=decrease
S_edge_response: during=0.4696591588930502 delta_before=0.10590170009925853 trend=decrease
S_power_balance: during=0.098632555713169 delta_before=0.09020740691234441 trend=increase
S_transport: during=0.4581464965900244 delta_before=-0.1449678997646282 trend=decrease
dalpha_proxy: during=0.3466796874961883 delta_before=-0.14404296875638667 trend=decrease
softx_lower_proxy: during=0.0003814697265864 delta_before=0.0001335144044045 trend=decrease
softx_upper_proxy: during=0.0009918212891758 delta_before=0.0010490417481807156 trend=decrease
te_profile_gradient_proxy: during=8.13056826070382 delta_before=-1.5806788551860702 trend=decrease
ne_profile_gradient_proxy: during=5.200164991196872e+17 delta_before=-3.5478516180951706e+17 trend=decrease
density_proxy: during=8.94132707331628e+19 delta_before=1.9830114419405226e+19 trend=decrease
nbi_proxy: during=1.2520058155059814 delta_before=-1195.276558637619 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.1545999887585641 → 0.1625999887585641 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4796272933245937 delta_before=0.06956321465338677 trend=increase
C_edge_capacity: during=0.6584774080188728 delta_before=-0.013640077983644416 trend=decrease
F_route_fragmentation: during=0.1735944894136306 delta_before=-0.08559659781185308 trend=decrease
S_edge_response: during=0.4967442410295011 delta_before=-0.01733796312250946 trend=decrease
S_power_balance: during=0.1178752140859757 delta_before=-0.0005587204779079896 trend=increase
S_transport: during=0.2631398033885065 delta_before=-0.19500669320151787 trend=decrease
dalpha_proxy: during=0.2978515624989564 delta_before=0.0 trend=increase
softx_lower_proxy: during=0.0003433227540698 delta_before=5.722045915569998e-05 trend=increase
softx_upper_proxy: during=0.0026512145995441 delta_before=0.0006675720213547998 trend=decrease
te_profile_gradient_proxy: during=7.052272007628914 delta_before=-2.0212357789524775 trend=decrease
ne_profile_gradient_proxy: during=3.198336993242382e+17 delta_before=-2.6204358605444864e+17 trend=decrease
density_proxy: during=9.36024276271754e+19 delta_before=-1.2522118026416947e+17 trend=increase
nbi_proxy: during=-0.6511744260787964 delta_before=-0.2925350964069367 trend=decrease
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