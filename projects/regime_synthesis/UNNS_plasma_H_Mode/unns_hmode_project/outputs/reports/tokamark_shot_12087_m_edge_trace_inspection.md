# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12087_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     381
time_min: -0.0690000057220459
time_max: 0.3109999942779544
```

State counts:

```text
negative_leakage_margin: 223
boundary_ambiguous_margin: 98
insufficient_data: 60
```

## 5. Inspected windows

| window_label   | state                   |   start_time |   end_time |   duration |   point_count | interpretability_flag      | interpretability_notes                                                                                |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median | S_power_balance__during_median   | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------|:------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|:---------------------------------|:-----------------------------|--------------------------------------:|
| negative_001   | negative_leakage_margin |  -0.00900001 |      0.105 |      0.114 |           115 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low                            |               -0.534831 |                        0.242947  |                               0.777778 |                        0.242947  |                                  |                              |                              0.777778 |
| negative_002   | negative_leakage_margin |   0.107      |      0.121 |      0.014 |            15 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity                                              |               -0.243986 |                        0.533791  |                               0.777778 |                        0.533791  |                                  |                              |                              0.777778 |
| peak_positive  | peak_positive_window    |   0.161      |      0.169 |      0.008 |             9 | fragile_positive_candidate | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before |                0.100954 |                        0.878731  |                               0.777778 |                        0.878731  |                                  |                              |                              0.777778 |
| negative_003   | negative_leakage_margin |   0.223      |      0.311 |      0.088 |            89 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before   |               -0.735776 |                        0.0420021 |                               0.777778 |                        0.0420021 |                                  |                              |                              0.777778 |
| peak_negative  | peak_negative_window    |   0.236      |      0.244 |      0.008 |             9 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before   |               -0.777778 |                        0         |                               0.777778 |                        0         |                                  |                              |                              0.777778 |

## 6. Interpretability flags

```text
fragile_negative_candidate: 4
fragile_positive_candidate: 1
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0090000057220458 → 0.1049999942779542 s
duration: 0.114 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low

m_edge: during=-0.5348308178108204 delta_before=0.0646172479124748 trend=increase
C_edge_capacity: during=0.2429469599669573 delta_before=0.06461724791247472 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=-0.2222222222222222 trend=flat
S_edge_response: during=0.2429469599669573 delta_before=0.06461724791247472 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0005054473883792 delta_before=0.0002956390388223 trend=increase
softx_upper_proxy: during=0.0005149841301378 delta_before=0.0005149841300591847 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=-0.2222222222222222 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.1069999942779542 → 0.1209999942779542 s
duration: 0.013999999999999999 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity

m_edge: during=-0.2439864118364939 delta_before=0.09887503156039684 trend=increase
C_edge_capacity: during=0.5337913659412838 delta_before=0.09887503156039684 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.5337913659412838 delta_before=0.09887503156039684 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0010299682612004 delta_before=0.00015735626289795014 trend=increase
softx_upper_proxy: during=0.0086975097651987 delta_before=0.0026988983150531 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.1609999942779543 → 0.1689999942779543 s
duration: 0.008000000000000007 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.10095356603871 delta_before=0.0018656716767469078 trend=decrease
C_edge_capacity: during=0.8787313438164879 delta_before=0.001865671676746894 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.8787313438164879 delta_before=0.001865671676746894 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0032997131335182 delta_before=0.0005722045896585999 trend=increase
softx_upper_proxy: during=0.0127601623527661 delta_before=-0.0032234191864061006 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_003 — negative_leakage_margin

```text
time: 0.2229999942779543 → 0.3109999942779544 s
duration: 0.08800000000000008 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.7357756761059728 delta_before=-0.5874505757215518 trend=decrease
C_edge_capacity: during=0.0420021016718049 delta_before=-0.5874505757215518 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.0420021016718049 delta_before=-0.5874505757215518 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.0008773803717192 delta_before=-0.0033569335957035 trend=decrease
softx_upper_proxy: during=-0.0009346008294177 delta_before=-0.0077629089352969005 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### peak_negative — peak_negative_window

```text
time: 0.2359999942779543 → 0.2439999942779543 s
duration: 0.008000000000000007 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.7777777777777778 delta_before=-0.3762912769270448 trend=decrease
C_edge_capacity: during=0.0 delta_before=-0.3762912769270448 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.0 delta_before=-0.3762912769270448 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.001182556152162 delta_before=-0.0029182434169857 trend=decrease
softx_upper_proxy: during=-0.0016784667981423 delta_before=-0.0029754638693564 trend=decrease
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