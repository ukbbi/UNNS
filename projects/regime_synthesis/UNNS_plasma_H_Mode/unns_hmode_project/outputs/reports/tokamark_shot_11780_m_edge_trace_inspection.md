# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11780_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     499
time_min: -0.0672000050544738
time_max: 0.4307999949455265
```

State counts:

```text
positive_boundary_margin: 248
negative_leakage_margin: 101
boundary_ambiguous_margin: 92
insufficient_data: 58
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                          |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:--------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| negative_001   | negative_leakage_margin  | -0.00920001  | 0.00879999 |      0.018 |            19 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                   |               -0.443533 |                         0.461717 |                              0.919192  |                        0.692576  |                      1           |                              |                              0.555556 |
| peak_negative  | peak_negative_window     | -0.000200005 | 0.00679999 |      0.007 |             8 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                   |               -0.481744 |                         0.39987  |                              0.878131  |                        0.560072  |                      0.949815    |                              |                              0.555556 |
| positive_001   | positive_boundary_margin |  0.0728      | 0.3198     |      0.247 |           248 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                          |                0.420646 |                         0.657684 |                              0.248136  |                        0.561965  |                      0.229203    |                              |                              0.333333 |
| peak_positive  | peak_positive_window     |  0.1428      | 0.1508     |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before                          |                0.629477 |                         0.700872 |                              0.0613403 |                        0.648042  |                      0.000897344 |                              |                              0.333333 |
| negative_002   | negative_leakage_margin  |  0.3468      | 0.3518     |      0.005 |             6 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before |               -0.336841 |                         0.36429  |                              0.693606  |                        0.0464357 |                      0.724284    |                              |                              0.555556 |
| negative_003   | negative_leakage_margin  |  0.3578      | 0.4308     |      0.073 |            74 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                   |               -0.503742 |                         0.398762 |                              0.905351  |                        0.591439  |                      0.983083    |                              |                              0.555556 |

## 6. Interpretability flags

```text
fragile_negative_candidate: 4
interpretable_positive_candidate: 2
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0092000050544738 → 0.0087999949455261 s
duration: 0.017999999999999898 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.4435330750995526 delta_before=-0.0025043669842140792 trend=increase
C_edge_capacity: during=0.4617170632468417 delta_before=-0.01644614782973891 trend=decrease
F_route_fragmentation: during=0.9191919191919192 delta_before=-0.08080808080808077 trend=decrease
S_edge_response: during=0.6925755948702627 delta_before=-0.024669221744608283 trend=decrease
S_power_balance: during=1.0 delta_before=0.0 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.085449218752497 delta_before=0.090332031252497 trend=increase
softx_lower_proxy: during=-3.814697245155919e-05 delta_before=6.95890556550588e-14 trend=decrease
softx_upper_proxy: during=-0.0001907348642327 delta_before=-0.00016212463468984932 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.1137222658091908e+18 delta_before=8.35619044584325e+17 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.5555555555555556 delta_before=-0.4444444444444444 trend=flat
```

### peak_negative — peak_negative_window

```text
time: -0.0002000050544738 → 0.0067999949455261 s
duration: 0.0069999999999999 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.4817438617931092 delta_before=-0.038672167422908854 trend=increase
C_edge_capacity: during=0.39986953093007516 delta_before=-0.07625069389164357 trend=decrease
F_route_fragmentation: during=0.8781313897828391 delta_before=-0.041060529409080115 trend=decrease
S_edge_response: during=0.5600718517224552 delta_before=-0.1541084855101229 trend=decrease
S_power_balance: during=0.9498149085000134 delta_before=-0.05018509149998662 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.34667968748013533 delta_before=0.35156249998013533 trend=increase
softx_lower_proxy: during=-2.8610229294193535e-05 delta_before=4.7683716995901735e-06 trend=decrease
softx_upper_proxy: during=-0.0005245208739125 delta_before=-0.0005102157591765971 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=7.211921204393804e+18 delta_before=7.110608079841919e+18 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.5555555555555556 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.0727999949455262 → 0.3197999949455264 s
duration: 0.24700000000000022 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.42064626607640604 delta_before=0.23020193165103392 trend=decrease
C_edge_capacity: during=0.6576840699374018 delta_before=0.14710633453248212 trend=increase
F_route_fragmentation: during=0.2481358990050409 delta_before=-0.0773641931086429 trend=increase
S_edge_response: during=0.561965180951455 delta_before=-0.09319870278512643 trend=decrease
S_power_balance: during=0.22920313582097596 delta_before=-0.09455623602167468 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.5505371093910258 delta_before=0.14526367190341793 trend=increase
softx_lower_proxy: during=0.0009346008294942 delta_before=-0.0006294250494511499 trend=decrease
softx_upper_proxy: during=0.00071525573722905 delta_before=-7.629394536785004e-05 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.2568326541888874e+20 delta_before=6.19143683742525e+19 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.1427999949455263 → 0.1507999949455263 s
duration: 0.00799999999999998 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.6294768398515451 delta_before=0.03019836708982404 trend=increase
C_edge_capacity: during=0.7008715431808958 delta_before=0.040987009813114095 trend=increase
F_route_fragmentation: during=0.0613402511477607 delta_before=0.0007341905417000971 trend=increase
S_edge_response: during=0.6480417764801893 delta_before=0.036894183455324914 trend=increase
S_power_balance: during=0.0008973439954112 delta_before=0.0008973439954112 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.4858398437265202 delta_before=0.01220703119551203 trend=decrease
softx_lower_proxy: during=0.0008296966554884 delta_before=-6.675720305089996e-05 trend=increase
softx_upper_proxy: during=0.0023078918455773 delta_before=0.0008773803734138 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.0660962379548644e+20 delta_before=5.919146081341424e+18 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.3467999949455265 → 0.3517999949455265 s
duration: 0.0050000000000000044 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.3368411413033096 delta_before=-0.1839371299462816 trend=decrease
C_edge_capacity: during=0.3642904610981681 delta_before=-0.05231102999281201 trend=decrease
F_route_fragmentation: during=0.6936063883433686 delta_before=0.11704067506327887 trend=increase
S_edge_response: during=0.04643569164725215 delta_before=-0.037228013402322145 trend=decrease
S_power_balance: during=0.7242843511851049 delta_before=0.09366699791684696 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=1.087646484367248 delta_before=-0.013427734382752021 trend=decrease
softx_lower_proxy: during=-0.0010108947743601 delta_before=-0.0005722045873138 trend=decrease
softx_upper_proxy: during=-0.0007438659674055 delta_before=-0.0003242492672246 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.7195938766342272e+20 delta_before=8.461744730340852e+18 trend=increase
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.5555555555555556 delta_before=0.22222222222222227 trend=increase
```

### negative_003 — negative_leakage_margin

```text
time: 0.3577999949455265 → 0.4307999949455265 s
duration: 0.07300000000000001 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.5037417373204909 delta_before=-0.247181127400612 trend=decrease
C_edge_capacity: during=0.3987619640168951 delta_before=0.10010341443152121 trend=increase
F_route_fragmentation: during=0.9053509716071579 delta_before=0.4524546404249121 trend=increase
S_edge_response: during=0.5914394346438512 delta_before=0.5826675048124244 trend=increase
S_power_balance: during=0.9830832862852918 delta_before=0.5530001160748925 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.00244140625 delta_before=-1.1279296874841978 trend=decrease
softx_lower_proxy: during=-0.00134468078557675 delta_before=-2.8610228442349983e-05 trend=increase
softx_upper_proxy: during=-0.0008296966552734 delta_before=0.0013446807883493001 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=4.206502789452399e+18 delta_before=-1.3503218409144948e+20 trend=decrease
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.5555555555555556 delta_before=0.0 trend=flat
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```