# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11941_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     521
time_min: -0.0590000078082084
time_max: 0.460999992191792
```

State counts:

```text
boundary_ambiguous_margin: 262
positive_boundary_margin: 209
insufficient_data: 50
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                              |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| positive_001   | positive_boundary_margin |        0.172 |      0.366 |      0.194 |           195 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before |               0.389744  |                         0.613808 |                               0.218547 |                         0.35002  |                        0.146573  |                     0.347755 |                              0        |
| peak_positive  | peak_positive_window     |        0.333 |      0.341 |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before |               0.456473  |                         0.624163 |                               0.175448 |                         0.340735 |                        0.19724   |                     0.185894 |                              0        |
| positive_002   | positive_boundary_margin |        0.375 |      0.379 |      0.004 |             5 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before |               0.208469  |                         0.357063 |                               0.150312 |                         0.164127 |                        0.0782482 |                     0.205257 |                              0.222222 |
| positive_003   | positive_boundary_margin |        0.39  |      0.396 |      0.006 |             7 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before |               0.287994  |                         0.406182 |                               0.114565 |                         0.261556 |                        0.0412584 |                     0.269125 |                              0.444444 |
| peak_negative  | peak_negative_window     |        0.398 |      0.406 |      0.008 |             9 | fragile_negative_candidate       | edge_response_low;m_edge_lower_than_before                                          |               0.0560975 |                         0.278893 |                               0.251246 |                         0.215166 |                        0.208313  |                   nan        |                              0.444444 |

## 6. Interpretability flags

```text
interpretable_positive_candidate: 4
fragile_negative_candidate: 1
```

## 7. Detailed window notes

### positive_001 — positive_boundary_margin

```text
time: 0.1719999921917917 → 0.3659999921917919 s
duration: 0.1940000000000002 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3897438187313758 delta_before=0.31944330045859815 trend=decrease
C_edge_capacity: during=0.6138081649604715 delta_before=0.0860187596522407 trend=decrease
F_route_fragmentation: during=0.2185467311475075 delta_before=-0.2389421558879456 trend=increase
S_edge_response: during=0.3500195738973665 delta_before=-0.05097538893363662 trend=decrease
S_power_balance: during=0.1465726244510639 delta_before=-0.5534273755489361 trend=increase
S_transport: during=0.3477553782123381 delta_before=0.03111340702244242 trend=increase
dalpha_proxy: during=0.4565429687448771 delta_before=0.05859374999601552 trend=decrease
softx_lower_proxy: during=0.0030899047866417 delta_before=-0.0020217895487932005 trend=decrease
softx_upper_proxy: during=0.0025177001952103 delta_before=0.00022888183578140004 trend=decrease
te_profile_gradient_proxy: during=11.05473991412518 delta_before=-3.969052573484788 trend=decrease
ne_profile_gradient_proxy: during=6.698948191630623e+17 delta_before=1.3158029910677504e+17 trend=increase
density_proxy: during=1.1123634233688877e+20 delta_before=3.786261528832691e+19 trend=increase
nbi_proxy: during=-1.947084903717041 delta_before=-1484494.0720849037 trend=increase
missingness_pressure: during=0.0 delta_before=0.0 trend=increase
```

### peak_positive — peak_positive_window

```text
time: 0.3329999921917919 → 0.3409999921917919 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4564734385975061 delta_before=0.03963448544865872 trend=decrease
C_edge_capacity: during=0.6241631220407539 delta_before=-0.0305766500835275 trend=decrease
F_route_fragmentation: during=0.1754483267751929 delta_before=-0.06575541711540919 trend=increase
S_edge_response: during=0.3407354026526564 delta_before=-0.050428094826022896 trend=increase
S_power_balance: during=0.1972402238874885 delta_before=-0.02052721025901802 trend=decrease
S_transport: during=0.1858943467103181 delta_before=-0.1323465389000689 trend=increase
dalpha_proxy: during=0.4101562500080773 delta_before=-0.01220703123793826 trend=decrease
softx_lower_proxy: during=0.001468658447101 delta_before=-0.0002670288089586001 trend=decrease
softx_upper_proxy: during=0.0077819824219381 delta_before=0.0006866455076274995 trend=increase
te_profile_gradient_proxy: during=7.699147045074131 delta_before=0.1883015902396803 trend=increase
ne_profile_gradient_proxy: during=6.203055019558395e+17 delta_before=-2.020631548278482e+17 trend=decrease
density_proxy: during=1.237907508207886e+20 delta_before=-5.084458426185023e+18 trend=decrease
nbi_proxy: during=-0.922460675239563 delta_before=-5.271204113960266 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.3749999921917919 → 0.3789999921917919 s
duration: 0.0040000000000000036 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.208468567812546 delta_before=0.014239683007063908 trend=decrease
C_edge_capacity: during=0.3570629233888955 delta_before=-0.14127613935654348 trend=decrease
F_route_fragmentation: during=0.1503117594840271 delta_before=-0.16481352076614517 trend=decrease
S_edge_response: during=0.1641266745811105 delta_before=-0.19082427823362133 trend=decrease
S_power_balance: during=0.0782482134211827 delta_before=-0.020922773932620806 trend=decrease
S_transport: during=0.2052574055687452 delta_before=-0.3493012028557205 trend=decrease
dalpha_proxy: during=0.3735351562455548 delta_before=0.012207031249878098 trend=increase
softx_lower_proxy: during=-0.0002574920654124 delta_before=-0.00013351440425420002 trend=decrease
softx_upper_proxy: during=0.0007343292231813 delta_before=-0.0014019012452959 trend=decrease
te_profile_gradient_proxy: during=6.524335818246392 delta_before=-2.003920104422029 trend=increase
ne_profile_gradient_proxy: during=4.4233495910101984e+17 delta_before=-5.0700891881025376e+17 trend=decrease
density_proxy: during=9.431389081518368e+19 delta_before=-5.182640416498909e+18 trend=decrease
nbi_proxy: during=6.984345436096191 delta_before=6.588936507701874 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.3899999921917919 → 0.3959999921917919 s
duration: 0.006000000000000005 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.287993806860283 delta_before=0.11010836751799688 trend=increase
C_edge_capacity: during=0.4061815859117798 delta_before=0.05793321181739658 trend=decrease
F_route_fragmentation: during=0.1145649787289622 delta_before=-0.0542642388067172 trend=decrease
S_edge_response: during=0.2615559605252337 delta_before=0.09963690759971702 trend=decrease
S_power_balance: during=0.0412584307921885 delta_before=-0.0162214466602026 trend=decrease
S_transport: during=0.269124913186364 delta_before=0.0 trend=flat
dalpha_proxy: during=0.285644531268323 delta_before=-0.09521484373838551 trend=increase
softx_lower_proxy: during=-0.0010395050052878 delta_before=-0.0005626678472346 trend=decrease
softx_upper_proxy: during=-0.0012969970704556 delta_before=-0.0008392333986511999 trend=decrease
te_profile_gradient_proxy: during=8.470485838430136 delta_before=0.0 trend=flat
ne_profile_gradient_proxy: during=4.870052976581079e+17 delta_before=0.0 trend=flat
density_proxy: during=8.515093034520543e+19 delta_before=-4.018046496451592e+18 trend=decrease
nbi_proxy: during=0.3954089283943176 delta_before=3.9534719586372375 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=0.2222222222222222 trend=increase
```

### peak_negative — peak_negative_window

```text
time: 0.3979999921917919 → 0.4059999921917919 s
duration: 0.008000000000000007 s
flag: fragile_negative_candidate
notes: edge_response_low;m_edge_lower_than_before

m_edge: during=0.0560974610482085 delta_before=-0.1837694753556384 trend=decrease
C_edge_capacity: during=0.2788929382218078 delta_before=-0.08673658790483024 trend=increase
F_route_fragmentation: during=0.251246342362439 delta_before=0.13668136363347677 trend=increase
S_edge_response: during=0.2151662859365174 delta_before=0.0 trend=increase
S_power_balance: during=0.20831343078866 delta_before=0.1670549999964715 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3173828124696085 delta_before=0.012207031215041297 trend=decrease
softx_lower_proxy: during=-0.0014495849610483 delta_before=-0.0004577636719322001 trend=decrease
softx_upper_proxy: during=-0.002517700195092 delta_before=-0.0012207031246364002 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.1674040518655869e+19 delta_before=-7.347688982654956e+19 trend=decrease
nbi_proxy: during=-0.1903820633888244 delta_before=-0.5857909917831421 trend=decrease
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