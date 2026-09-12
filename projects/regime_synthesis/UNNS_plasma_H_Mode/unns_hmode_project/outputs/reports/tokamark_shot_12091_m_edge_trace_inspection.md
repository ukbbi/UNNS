# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12091_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     426
time_min: -0.0690000057220459
time_max: 0.3559999942779545
```

State counts:

```text
negative_leakage_margin: 285
boundary_ambiguous_margin: 79
insufficient_data: 61
positive_boundary_margin: 1
```

## 5. Inspected windows

| window_label   | state                   |   start_time |   end_time |   duration |   point_count | interpretability_flag      | interpretability_notes                                                                                |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median | S_power_balance__during_median   | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------|:------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|:---------------------------------|:-----------------------------|--------------------------------------:|
| negative_001   | negative_leakage_margin |  -0.00900001 |      0.079 |      0.088 |            89 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low                            |               -0.53548  |                        0.242298  |                               0.777778 |                        0.242298  |                                  |                              |                              0.777778 |
| negative_002   | negative_leakage_margin |   0.081      |      0.119 |      0.038 |            39 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity                                              |               -0.396014 |                        0.381764  |                               0.777778 |                        0.381764  |                                  |                              |                              0.777778 |
| peak_positive  | peak_positive_window    |   0.146      |      0.154 |      0.008 |             9 | fragile_positive_candidate | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before |                0.108013 |                        0.885791  |                               0.777778 |                        0.885791  |                                  |                              |                              0.777778 |
| negative_003   | negative_leakage_margin |   0.193      |      0.196 |      0.003 |             4 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before                     |               -0.268891 |                        0.508887  |                               0.777778 |                        0.508887  |                                  |                              |                              0.777778 |
| negative_004   | negative_leakage_margin |   0.217      |      0.22  |      0.003 |             4 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before                     |               -0.376482 |                        0.401296  |                               0.777778 |                        0.401296  |                                  |                              |                              0.777778 |
| negative_005   | negative_leakage_margin |   0.222      |      0.236 |      0.014 |            15 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before                     |               -0.332487 |                        0.445291  |                               0.777778 |                        0.445291  |                                  |                              |                              0.777778 |
| negative_006   | negative_leakage_margin |   0.238      |      0.247 |      0.009 |            10 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before                     |               -0.356623 |                        0.421155  |                               0.777778 |                        0.421155  |                                  |                              |                              0.777778 |
| negative_007   | negative_leakage_margin |   0.249      |      0.268 |      0.019 |            20 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before                     |               -0.368622 |                        0.409156  |                               0.777778 |                        0.409156  |                                  |                              |                              0.777778 |
| negative_008   | negative_leakage_margin |   0.27       |      0.355 |      0.085 |            86 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before   |               -0.741658 |                        0.0361201 |                               0.777778 |                        0.0361201 |                                  |                              |                              0.777778 |
| peak_negative  | peak_negative_window    |   0.28       |      0.288 |      0.008 |             9 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before   |               -0.762499 |                        0.0152788 |                               0.777778 |                        0.0152788 |                                  |                              |                              0.777778 |

## 6. Interpretability flags

```text
fragile_negative_candidate: 9
fragile_positive_candidate: 1
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0090000057220458 → 0.0789999942779542 s
duration: 0.08800000000000001 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low

m_edge: during=-0.5354802357583466 delta_before=0.03718041062226951 trend=increase
C_edge_capacity: during=0.2422975420194311 delta_before=0.0371804106222694 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=-0.2222222222222222 trend=flat
S_edge_response: during=0.2422975420194311 delta_before=0.0371804106222694 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0005149841314545 delta_before=0.00022888183648029996 trend=increase
softx_upper_proxy: during=0.0001716613771022 delta_before=0.00020980834989821044 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=-0.2222222222222222 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.0809999942779542 → 0.1189999942779542 s
duration: 0.038000000000000006 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity

m_edge: during=-0.3960135897651906 delta_before=0.01734715094976841 trend=increase
C_edge_capacity: during=0.3817641880125872 delta_before=0.01734715094976841 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.3817641880125872 delta_before=0.01734715094976841 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0008201599121093 delta_before=0.00017166137656000001 trend=increase
softx_upper_proxy: during=0.0040245056121293 delta_before=-7.62939483301998e-05 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.1459999942779543 → 0.1539999942779543 s
duration: 0.008000000000000007 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.1080129021724128 delta_before=0.044881588947403406 trend=decrease
C_edge_capacity: during=0.8857906799501907 delta_before=0.04488158894740346 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.8857906799501907 delta_before=0.04488158894740346 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0030326843257295 delta_before=0.0008487701402467001 trend=decrease
softx_upper_proxy: during=0.0126838684087691 delta_before=-0.0015163421610341014 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_003 — negative_leakage_margin

```text
time: 0.1929999942779543 → 0.1959999942779543 s
duration: 0.0030000000000000027 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before

m_edge: during=-0.26889087535344136 delta_before=-0.11669454274215896 trend=decrease
C_edge_capacity: during=0.5088869024243364 delta_before=-0.11669454274215896 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.5088869024243364 delta_before=-0.11669454274215896 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.00268936157192015 delta_before=-0.0006484985345099501 trend=decrease
softx_upper_proxy: during=0.0018501281743248 delta_before=-0.0013542175289509002 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_004 — negative_leakage_margin

```text
time: 0.2169999942779543 → 0.2199999942779543 s
duration: 0.0030000000000000027 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before

m_edge: during=-0.3764817437739466 delta_before=-0.1599718733487006 trend=decrease
C_edge_capacity: during=0.40129603400383107 delta_before=-0.15997187334870067 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.40129603400383107 delta_before=-0.15997187334870067 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.00188827514665175 delta_before=-0.00074386596728635 trend=decrease
softx_upper_proxy: during=0.00147819519051605 delta_before=-0.0023746490486712497 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_005 — negative_leakage_margin

```text
time: 0.2219999942779543 → 0.2359999942779543 s
duration: 0.013999999999999985 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before

m_edge: during=-0.3324871726771225 delta_before=-0.10360236802497202 trend=increase
C_edge_capacity: during=0.4452906051006552 delta_before=-0.10360236802497202 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.4452906051006552 delta_before=-0.10360236802497202 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0023269653310768 delta_before=-0.00030517578286130007 trend=increase
softx_upper_proxy: during=0.0011920928949513 delta_before=-0.0009059905924544002 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_006 — negative_leakage_margin

```text
time: 0.2379999942779543 → 0.2469999942779543 s
duration: 0.009000000000000008 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before

m_edge: during=-0.3566232644654921 delta_before=-0.031385519812378804 trend=decrease
C_edge_capacity: during=0.42115451331228565 delta_before=-0.03138551981237886 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.42115451331228565 delta_before=-0.03138551981237886 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0021362304631077503 delta_before=-0.0002670288146769495 trend=decrease
softx_upper_proxy: during=0.00087261200192575 delta_before=-0.00019550323262794997 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_007 — negative_leakage_margin

```text
time: 0.2489999942779543 → 0.2679999942779544 s
duration: 0.0190000000000001 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before

m_edge: during=-0.3686221077804702 delta_before=-0.01374765666443184 trend=decrease
C_edge_capacity: during=0.40915566999730746 delta_before=-0.01374765666443184 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.40915566999730746 delta_before=-0.01374765666443184 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.00205039978156445 delta_before=-8.583068772545022e-05 trend=decrease
softx_upper_proxy: during=0.0007057189950713 delta_before=-0.00011444091730800001 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_008 — negative_leakage_margin

```text
time: 0.2699999942779544 → 0.3549999942779545 s
duration: 0.08500000000000008 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.7416576548181537 delta_before=-0.3469077878827874 trend=decrease
C_edge_capacity: during=0.03612012295962415 delta_before=-0.34690778788278737 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.03612012295962415 delta_before=-0.34690778788278737 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.00102996826177395 delta_before=-0.00280380249749315 trend=decrease
softx_upper_proxy: during=-0.00119209289458725 delta_before=-0.00189781188901525 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### peak_negative — peak_negative_window

```text
time: 0.2799999942779544 → 0.2879999942779544 s
duration: 0.008000000000000007 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.7624989390839397 delta_before=-0.3997360648694793 trend=decrease
C_edge_capacity: during=0.015278838693838 delta_before=-0.39973606486947927 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.015278838693838 delta_before=-0.39973606486947927 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.0010681152349468 delta_before=-0.0032997131358410998 trend=decrease
softx_upper_proxy: during=-0.0020599365227178 delta_before=-0.0024986267077155002 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```