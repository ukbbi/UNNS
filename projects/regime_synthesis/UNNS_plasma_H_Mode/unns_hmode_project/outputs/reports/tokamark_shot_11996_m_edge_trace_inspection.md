# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11996_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     541
time_min: -0.0562000051140785
time_max: 0.4837999948859219
```

State counts:

```text
boundary_ambiguous_margin: 338
positive_boundary_margin: 130
insufficient_data: 47
negative_leakage_margin: 26
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                              |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| peak_negative  | peak_negative_window     |       0.0448 |     0.0528 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before |               -0.208353 |                         0.249912 |                               0.458265 |                         0.367385 |                         0.656083 |                     0.405776 |                              0        |
| negative_001   | negative_leakage_margin  |       0.0468 |     0.0548 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before |               -0.208353 |                         0.251066 |                               0.45975  |                         0.382832 |                         0.656083 |                     0.413682 |                              0        |
| negative_002   | negative_leakage_margin  |       0.0908 |     0.1008 |      0.01  |            11 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before |               -0.236203 |                         0.431621 |                               0.667825 |                         0.471344 |                         0.720905 |                     0.762661 |                              0        |
| positive_001   | positive_boundary_margin |       0.2848 |     0.4108 |      0.126 |           127 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before |                0.438483 |                         0.640565 |                               0.212364 |                         0.354008 |                         0.210173 |                   nan        |                              0.222222 |
| peak_positive  | peak_positive_window     |       0.3878 |     0.3958 |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before |                0.455014 |                         0.599549 |                               0.131391 |                         0.352283 |                         0.111206 |                   nan        |                              0.222222 |

## 6. Interpretability flags

```text
interpretable_negative_candidate: 3
interpretable_positive_candidate: 2
```

## 7. Detailed window notes

### peak_negative — peak_negative_window

```text
time: 0.0447999948859215 → 0.0527999948859215 s
duration: 0.008 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.2083525655432795 delta_before=-0.20846121227185818 trend=decrease
C_edge_capacity: during=0.2499119578126165 delta_before=-0.02660267624375362 trend=increase
F_route_fragmentation: during=0.458264523355896 delta_before=0.17470658571999964 trend=increase
S_edge_response: during=0.367384841448271 delta_before=-0.015521097978832998 trend=increase
S_power_balance: during=0.656082918882204 delta_before=0.49845192519587955 trend=increase
S_transport: during=0.4057759104568121 delta_before=-0.050473944377871005 trend=increase
dalpha_proxy: during=0.1489257812391139 delta_before=-0.009765625014123397 trend=decrease
softx_lower_proxy: during=0.0004386901855341 delta_before=7.629394531119999e-05 trend=increase
softx_upper_proxy: during=0.0001716613768947 delta_before=0.0003623962401684 trend=increase
te_profile_gradient_proxy: during=17.288530402762643 delta_before=3.584107376623951 trend=decrease
ne_profile_gradient_proxy: during=3.0293860220909416e+16 delta_before=-3.4470839544338035e+17 trend=increase
density_proxy: during=3.4307489575448084e+19 delta_before=-1.648893607710556e+17 trend=increase
nbi_proxy: during=1287518.75 delta_before=1274237.1220703125 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### negative_001 — negative_leakage_margin

```text
time: 0.0467999948859215 → 0.0547999948859215 s
duration: 0.008 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.2083525655432795 delta_before=-0.1693126916011336 trend=increase
C_edge_capacity: during=0.2510663496209794 delta_before=0.007886571376125112 trend=increase
F_route_fragmentation: during=0.4597502277354786 delta_before=0.1761922900995822 trend=increase
S_edge_response: during=0.3828315404047698 delta_before=0.03060444416237529 trend=increase
S_power_balance: during=0.656082918882204 delta_before=0.4235181147974929 trend=increase
S_transport: during=0.4136815993795544 delta_before=0.0017524190080953073 trend=increase
dalpha_proxy: during=0.1342773437516618 delta_before=-0.01708984374739289 trend=decrease
softx_lower_proxy: during=0.0004386901855341 delta_before=7.629394531119999e-05 trend=decrease
softx_upper_proxy: during=0.0001811981202072 delta_before=0.00037193298348089997 trend=increase
te_profile_gradient_proxy: during=14.760609734688405 delta_before=1.0561867085497134 trend=decrease
ne_profile_gradient_proxy: during=1.8488962588298374e+17 delta_before=-7.128021553863494e+16 trend=increase
density_proxy: during=3.4307489575448084e+19 delta_before=-1.773512255602729e+17 trend=increase
nbi_proxy: during=1287518.75 delta_before=1083220.53125 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.0907999948859216 → 0.1007999948859216 s
duration: 0.010000000000000009 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.2362031930459068 delta_before=-0.08148022774046612 trend=increase
C_edge_capacity: during=0.4316213681917576 delta_before=0.09014277089994144 trend=increase
F_route_fragmentation: during=0.6678245612376645 delta_before=0.17951033150273193 trend=increase
S_edge_response: during=0.4713435519615917 delta_before=0.1079349737845745 trend=decrease
S_power_balance: during=0.720905085047541 delta_before=0.020476469462605285 trend=increase
S_transport: during=0.7626607422548399 delta_before=0.3645708080888476 trend=increase
dalpha_proxy: during=0.1977539062530493 delta_before=0.01708984375232772 trend=increase
softx_lower_proxy: during=0.0011253356933127 delta_before=0.00036239624016530005 trend=increase
softx_upper_proxy: during=0.0004768371581853 delta_before=0.00025749206536960004 trend=increase
te_profile_gradient_proxy: during=19.873573227379143 delta_before=1.3736354884972428 trend=decrease
ne_profile_gradient_proxy: during=5.3388648169406426e+17 delta_before=5.053066480430308e+17 trend=increase
density_proxy: during=4.558490326461632e+19 delta_before=2.654476156148908e+18 trend=increase
nbi_proxy: during=1600927.75 delta_before=77933.75 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.2847999948859218 → 0.4107999948859219 s
duration: 0.1260000000000001 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4384832130611349 delta_before=0.5517128858159939 trend=decrease
C_edge_capacity: during=0.6405653661718016 delta_before=-0.03610656695333514 trend=decrease
F_route_fragmentation: during=0.2123641406187937 delta_before=-0.5774910511027591 trend=decrease
S_edge_response: during=0.3540079060652109 delta_before=-0.07456352250621773 trend=decrease
S_power_balance: during=0.2101734558180318 delta_before=-0.7058223957922614 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3051757812540928 delta_before=-0.10009765624933603 trend=decrease
softx_lower_proxy: during=0.0203704833986242 delta_before=-0.027256011964142696 trend=decrease
softx_upper_proxy: during=0.018615722656154 delta_before=-0.0271224975586363 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.2132574250833804e+20 delta_before=-4.3262879842288435e+18 trend=decrease
nbi_proxy: during=5.003382682800293 delta_before=-1742431.6216173172 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=increase
```

### peak_positive — peak_positive_window

```text
time: 0.3877999948859219 → 0.3957999948859219 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4550136272498426 delta_before=0.0033793488300167263 trend=increase
C_edge_capacity: during=0.5995491300218317 delta_before=-0.00437556538898598 trend=decrease
F_route_fragmentation: during=0.131390910192812 delta_before=-0.019290399935295383 trend=decrease
S_edge_response: during=0.3522831137944936 delta_before=0.0042950083758444 trend=increase
S_power_balance: during=0.1112061741862764 delta_before=-0.0235771554764721 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.2319335937545401 delta_before=-0.007324218747692679 trend=decrease
softx_lower_proxy: during=0.0131797790522498 delta_before=4.7683715608051735e-05 trend=increase
softx_upper_proxy: during=0.0075149536133347 delta_before=0.00022888183618375094 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.019224672989285e+20 delta_before=-4.62520121535601e+18 trend=decrease
nbi_proxy: during=3.2489943504333496 delta_before=-8.193133354187012 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```