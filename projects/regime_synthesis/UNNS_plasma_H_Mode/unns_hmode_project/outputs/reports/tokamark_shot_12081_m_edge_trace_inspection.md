# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12081_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     390
time_min: -0.0690000057220459
time_max: 0.3199999942779544
```

State counts:

```text
negative_leakage_margin: 251
boundary_ambiguous_margin: 71
insufficient_data: 60
positive_boundary_margin: 8
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag      | interpretability_notes                                                                                |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median | S_power_balance__during_median   | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------|:------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|:---------------------------------|:-----------------------------|--------------------------------------:|
| negative_001   | negative_leakage_margin  |  -0.00900001 |      0.116 |      0.125 |           126 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low                            |               -0.576063 |                       0.201715   |                               0.777778 |                       0.201715   |                                  |                              |                              0.777778 |
| negative_002   | negative_leakage_margin  |   0.128      |      0.134 |      0.006 |             7 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before                     |               -0.235918 |                       0.54186    |                               0.777778 |                       0.54186    |                                  |                              |                              0.777778 |
| negative_003   | negative_leakage_margin  |   0.149      |      0.153 |      0.004 |             5 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before                     |               -0.260656 |                       0.517122   |                               0.777778 |                       0.517122   |                                  |                              |                              0.777778 |
| peak_positive  | peak_positive_window     |   0.18       |      0.188 |      0.008 |             9 | fragile_positive_candidate | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before |                0.17946  |                       0.957237   |                               0.777778 |                       0.957237   |                                  |                              |                              0.777778 |
| positive_001   | positive_boundary_margin |   0.184      |      0.187 |      0.003 |             4 | fragile_positive_candidate | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before |                0.222222 |                       1          |                               0.777778 |                       1          |                                  |                              |                              0.777778 |
| positive_002   | positive_boundary_margin |   0.194      |      0.197 |      0.003 |             4 | fragile_positive_candidate | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before |                0.21954  |                       0.997318   |                               0.777778 |                       0.997318   |                                  |                              |                              0.777778 |
| negative_004   | negative_leakage_margin  |   0.211      |      0.215 |      0.004 |             5 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before                     |               -0.225235 |                       0.552543   |                               0.777778 |                       0.552543   |                                  |                              |                              0.777778 |
| negative_005   | negative_leakage_margin  |   0.217      |      0.32  |      0.103 |           104 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before   |               -0.72643  |                       0.0513478  |                               0.777778 |                       0.0513478  |                                  |                              |                              0.777778 |
| peak_negative  | peak_negative_window     |   0.244      |      0.251 |      0.007 |             8 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before   |               -0.773646 |                       0.00413183 |                               0.777778 |                       0.00413183 |                                  |                              |                              0.777778 |

## 6. Interpretability flags

```text
fragile_negative_candidate: 6
fragile_positive_candidate: 3
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0090000057220458 → 0.1159999942779542 s
duration: 0.125 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low

m_edge: during=-0.5760627907742253 delta_before=0.05694991314771303 trend=increase
C_edge_capacity: during=0.20171498700355245 delta_before=0.056949913147712944 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=-0.2222222222222222 trend=flat
S_edge_response: during=0.20171498700355245 delta_before=0.056949913147712944 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0008106231687343 delta_before=0.0008583068844585272 trend=increase
softx_upper_proxy: during=0.0002288818357122 delta_before=0.0003051757808849396 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=-0.2222222222222222 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.1279999942779542 → 0.1339999942779542 s
duration: 0.006000000000000005 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before

m_edge: during=-0.235918087126042 delta_before=-0.06664771968750821 trend=increase
C_edge_capacity: during=0.5418596906517358 delta_before=-0.06664771968750816 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.5418596906517358 delta_before=-0.06664771968750816 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0016593933110127 delta_before=0.0004959106454397002 trend=increase
softx_upper_proxy: during=0.0066566467283985 delta_before=-0.0022125244128669997 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_003 — negative_leakage_margin

```text
time: 0.1489999942779543 → 0.1529999942779543 s
duration: 0.0040000000000000036 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before

m_edge: during=-0.2606556022015019 delta_before=-0.103226713032569 trend=decrease
C_edge_capacity: during=0.5171221755762758 delta_before=-0.10322671303256903 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.5171221755762758 delta_before=-0.10322671303256903 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0048255920393652 delta_before=0.0008392333974565 trend=decrease
softx_upper_proxy: during=0.0027847290033914 delta_before=-0.0033760070807180996 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.1799999942779543 → 0.1879999942779543 s
duration: 0.008000000000000007 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.1794596374714802 delta_before=0.165476398011392 trend=increase
C_edge_capacity: during=0.957237415249258 delta_before=0.1654763980113919 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.957237415249258 delta_before=0.1654763980113919 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0088310241694001 delta_before=-0.0006675720221505001 trend=decrease
softx_upper_proxy: during=0.0100898742687571 delta_before=0.0056076049817910005 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.1839999942779543 → 0.1869999942779543 s
duration: 0.0030000000000000027 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.2222222222222222 delta_before=0.1725309180152737 trend=flat
C_edge_capacity: during=1.0 delta_before=0.17253091801527365 trend=flat
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=1.0 delta_before=0.17253091801527365 trend=flat
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.00905990600478785 delta_before=-0.00022888183538775052 trend=decrease
softx_upper_proxy: during=0.0119209289541187 delta_before=0.0066566467287069 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.1939999942779543 → 0.1969999942779543 s
duration: 0.0030000000000000027 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.2195401558921684 delta_before=0.02104576425317492 trend=decrease
C_edge_capacity: during=0.9973179336699463 delta_before=0.02104576425317506 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.9973179336699463 delta_before=0.02104576425317506 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0085926055913539 delta_before=0.0004482269281765993 trend=decrease
softx_upper_proxy: during=0.0101280212398878 delta_before=9.536743091270034e-05 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_004 — negative_leakage_margin

```text
time: 0.2109999942779543 → 0.2149999942779543 s
duration: 0.0040000000000000036 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before

m_edge: during=-0.2252349146837033 delta_before=-0.1322742146183484 trend=decrease
C_edge_capacity: during=0.5525428630940744 delta_before=-0.13227421461834843 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.5525428630940744 delta_before=-0.13227421461834843 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0063323974606067 delta_before=-0.0010108947780763993 trend=decrease
softx_upper_proxy: during=0.0018692016610565 delta_before=-0.0015258789056665002 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_005 — negative_leakage_margin

```text
time: 0.2169999942779543 → 0.3199999942779544 s
duration: 0.10300000000000009 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.7264299926984501 delta_before=-0.5206315587361469 trend=decrease
C_edge_capacity: during=0.051347785079327704 delta_before=-0.5206315587361469 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.051347785079327704 delta_before=-0.5206315587361469 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.0010108947729909 delta_before=-0.007610321043261099 trend=decrease
softx_upper_proxy: during=-0.0010299682633498 delta_before=-0.0028991699244063 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### peak_negative — peak_negative_window

```text
time: 0.2439999942779543 → 0.2509999942779544 s
duration: 0.0070000000000000895 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.7736459457308524 delta_before=-0.3658782750486924 trend=decrease
C_edge_capacity: during=0.004131832046925301 delta_before=-0.3658782750486924 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.004131832046925301 delta_before=-0.3658782750486924 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.0011730194093651 delta_before=-0.004854202271144499 trend=decrease
softx_upper_proxy: during=-0.0020408630372027 delta_before=-0.0028228759779113 trend=decrease
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