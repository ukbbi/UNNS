# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12079_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     381
time_min: -0.0694000050425529
time_max: 0.3105999949574474
```

State counts:

```text
negative_leakage_margin: 260
insufficient_data: 61
boundary_ambiguous_margin: 47
positive_boundary_margin: 13
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag      | interpretability_notes                                                                                |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median | S_power_balance__during_median   | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------|:------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|:---------------------------------|:-----------------------------|--------------------------------------:|
| negative_001   | negative_leakage_margin  |  -0.00940001 |     0.1606 |      0.17  |           171 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low                            |               -0.659219 |                        0.118559  |                               0.777778 |                        0.118559  |                                  |                              |                              0.777778 |
| peak_positive  | peak_positive_window     |   0.1806     |     0.1886 |      0.008 |             9 | fragile_positive_candidate | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before |                0.199601 |                        0.977378  |                               0.777778 |                        0.977378  |                                  |                              |                              0.777778 |
| positive_001   | positive_boundary_margin |   0.1846     |     0.1876 |      0.003 |             4 | fragile_positive_candidate | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before |                0.222169 |                        0.999947  |                               0.777778 |                        0.999947  |                                  |                              |                              0.777778 |
| positive_002   | positive_boundary_margin |   0.1916     |     0.1986 |      0.007 |             8 | fragile_positive_candidate | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before |                0.220325 |                        0.998103  |                               0.777778 |                        0.998103  |                                  |                              |                              0.777778 |
| negative_002   | negative_leakage_margin  |   0.2256     |     0.3096 |      0.084 |            85 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before   |               -0.764304 |                        0.0134735 |                               0.777778 |                        0.0134735 |                                  |                              |                              0.777778 |
| peak_negative  | peak_negative_window     |   0.2356     |     0.2436 |      0.008 |             9 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before   |               -0.777778 |                        0         |                               0.777778 |                        0         |                                  |                              |                              0.777778 |

## 6. Interpretability flags

```text
fragile_negative_candidate: 3
fragile_positive_candidate: 3
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0094000050425528 → 0.1605999949574472 s
duration: 0.17 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low

m_edge: during=-0.6592190485191067 delta_before=0.0420771148018011 trend=increase
C_edge_capacity: during=0.118558729258671 delta_before=0.0420771148018011 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=-0.2222222222222222 trend=flat
S_edge_response: during=0.118558729258671 delta_before=0.0420771148018011 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0008392333984375 delta_before=0.0008392333985073802 trend=increase
softx_upper_proxy: during=0.0004291534418044 delta_before=0.0004291534418044 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=-0.2222222222222222 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.1805999949574472 → 0.1885999949574472 s
duration: 0.008000000000000007 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.1996006202417916 delta_before=0.1498742489333064 trend=increase
C_edge_capacity: during=0.9773783980195694 delta_before=0.14987424893330636 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.9773783980195694 delta_before=0.14987424893330636 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.01216888427794 delta_before=0.0010871887253863007 trend=decrease
softx_upper_proxy: during=0.0242996215803436 delta_before=0.006484985348273499 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.1845999949574472 → 0.1875999949574472 s
duration: 0.0030000000000000027 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.22216883194056047 delta_before=0.12107136504966308 trend=decrease
C_edge_capacity: during=0.9999466097183383 delta_before=0.12107136504966298 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.9999466097183383 delta_before=0.12107136504966298 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.01199722290083665 delta_before=-5.722045538674933e-05 trend=increase
softx_upper_proxy: during=0.02764701843265695 delta_before=0.008783340457113951 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.1915999949574472 → 0.1985999949574473 s
duration: 0.0070000000000000895 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.22032475832872994 delta_before=0.02072413808693835 trend=increase
C_edge_capacity: during=0.9981025361065078 delta_before=0.020724138086938404 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.9981025361065078 delta_before=0.020724138086938404 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.011777877806302201 delta_before=-0.0003910064716377993 trend=decrease
softx_upper_proxy: during=0.028028488160823 delta_before=0.003881454469867502 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.2255999949574473 → 0.3095999949574474 s
duration: 0.0840000000000001 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.7643042952040989 delta_before=-0.5934151204539717 trend=decrease
C_edge_capacity: during=0.0134734825736788 delta_before=-0.5934151204539718 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.0134734825736788 delta_before=-0.5934151204539718 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.0011444091781064 delta_before=-0.0084495544413502 trend=decrease
softx_upper_proxy: during=-0.001068115234375 delta_before=-0.0153732299797088 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### peak_negative — peak_negative_window

```text
time: 0.2355999949574473 → 0.2435999949574473 s
duration: 0.008000000000000007 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.7777777777777778 delta_before=-0.436792674943475 trend=decrease
C_edge_capacity: during=0.0 delta_before=-0.4367926749434749 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.0 delta_before=-0.4367926749434749 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.0012874603271935 delta_before=-0.006208419798212199 trend=decrease
softx_upper_proxy: during=-0.0018501281738281 delta_before=-0.0108337402354231 trend=increase
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