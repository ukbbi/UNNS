# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12082_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     254
time_min: -0.0692000091075897
time_max: 0.1837999908924105
```

State counts:

```text
negative_leakage_margin: 140
insufficient_data: 61
boundary_ambiguous_margin: 53
```

## 5. Inspected windows

| window_label   | state                   |   start_time |   end_time |   duration |   point_count | interpretability_flag      | interpretability_notes                                                                              |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median | S_power_balance__during_median   | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------|:----------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|:---------------------------------|:-----------------------------|--------------------------------------:|
| negative_001   | negative_leakage_margin |  -0.00920001 |     0.0178 |      0.027 |            28 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before |              -0.453263  |                        0.324515  |                               0.777778 |                        0.324515  |                                  |                              |                              0.777778 |
| negative_002   | negative_leakage_margin |   0.0218     |     0.0278 |      0.006 |             7 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity                                            |              -0.281081  |                        0.496697  |                               0.777778 |                        0.496697  |                                  |                              |                              0.777778 |
| negative_003   | negative_leakage_margin |   0.0298     |     0.0338 |      0.004 |             5 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before                   |              -0.245943  |                        0.531834  |                               0.777778 |                        0.531834  |                                  |                              |                              0.777778 |
| negative_004   | negative_leakage_margin |   0.0858     |     0.0898 |      0.004 |             5 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity                                            |              -0.213635  |                        0.564143  |                               0.777778 |                        0.564143  |                                  |                              |                              0.777778 |
| peak_positive  | peak_positive_window    |   0.0888     |     0.0968 |      0.008 |             9 | fragile_positive_candidate | high_missingness_pressure;edge_response_high;m_edge_higher_than_before                              |              -0.0885657 |                        0.689212  |                               0.777778 |                        0.689212  |                                  |                              |                              0.777778 |
| negative_005   | negative_leakage_margin |   0.1108     |     0.1828 |      0.072 |            73 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before |              -0.682459  |                        0.0953192 |                               0.777778 |                        0.0953192 |                                  |                              |                              0.777778 |
| peak_negative  | peak_negative_window    |   0.1178     |     0.1258 |      0.008 |             9 | fragile_negative_candidate | high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before |              -0.727003  |                        0.0507751 |                               0.777778 |                        0.0507751 |                                  |                              |                              0.777778 |

## 6. Interpretability flags

```text
fragile_negative_candidate: 6
fragile_positive_candidate: 1
```

## 7. Detailed window notes

### negative_001 — negative_leakage_margin

```text
time: -0.0092000091075896 → 0.0177999908924103 s
duration: 0.0269999999999999 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.4532625096480749 delta_before=-0.030167627553369603 trend=increase
C_edge_capacity: during=0.32451526812970277 delta_before=-0.030167627553369603 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=-0.2222222222222222 trend=flat
S_edge_response: during=0.32451526812970277 delta_before=-0.030167627553369603 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=9.059906008416708e-05 delta_before=-0.00010013580303983292 trend=increase
softx_upper_proxy: during=-0.00015258789075305 delta_before=-0.0001335144043987199 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=-0.2222222222222222 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.0217999908924103 → 0.0277999908924103 s
duration: 0.005999999999999998 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity

m_edge: during=-0.2810812153723633 delta_before=0.014633782371433701 trend=decrease
C_edge_capacity: during=0.4966965624054145 delta_before=0.014633782371433812 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.4966965624054145 delta_before=0.014633782371433812 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0008392333981667 delta_before=0.00032424926650990006 trend=decrease
softx_upper_proxy: during=7.629394528600375e-05 delta_before=0.00019073486278820375 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_003 — negative_leakage_margin

```text
time: 0.0297999908924103 → 0.0337999908924103 s
duration: 0.004 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;m_edge_lower_than_before

m_edge: during=-0.2459434831498392 delta_before=-0.005306427507054595 trend=decrease
C_edge_capacity: during=0.5318342946279385 delta_before=-0.0053064275070545674 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.5318342946279385 delta_before=-0.0053064275070545674 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0008201599122246 delta_before=-2.8610229005700022e-05 trend=decrease
softx_upper_proxy: during=0.0002098083496821 delta_before=0.00012397766120510076 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_004 — negative_leakage_margin

```text
time: 0.0857999908924104 → 0.0897999908924104 s
duration: 0.0040000000000000036 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity

m_edge: during=-0.2136351337577288 delta_before=0.0008434764309480647 trend=increase
C_edge_capacity: during=0.564142644020049 delta_before=0.0008434764309480647 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.564142644020049 delta_before=0.0008434764309480647 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0006866455080867 delta_before=-0.00015258789041669993 trend=decrease
softx_upper_proxy: during=0.000381469726631 delta_before=0.00016689300513940002 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.0887999908924104 → 0.0967999908924104 s
duration: 0.007999999999999993 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;edge_response_high;m_edge_higher_than_before

m_edge: during=-0.0885657340480815 delta_before=0.1295003200772345 trend=increase
C_edge_capacity: during=0.6892120437296962 delta_before=0.12950032007723444 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.6892120437296962 delta_before=0.12950032007723444 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=0.0010108947757679 delta_before=0.00020980834998700001 trend=increase
softx_upper_proxy: during=0.0005340576175115 delta_before=0.00026702880882825003 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### negative_005 — negative_leakage_margin

```text
time: 0.1107999908924104 → 0.1827999908924105 s
duration: 0.0720000000000001 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.6824585381644928 delta_before=-0.5742045700410366 trend=decrease
C_edge_capacity: during=0.095319239613285 delta_before=-0.5742045700410366 trend=decrease
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.095319239613285 delta_before=-0.5742045700410366 trend=decrease
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.0003623962404204 delta_before=-0.0005912780771778 trend=decrease
softx_upper_proxy: during=-0.0006103515625 delta_before=-0.0063705444352656 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=None delta_before=None trend=na
missingness_pressure: during=0.7777777777777778 delta_before=0.0 trend=flat
```

### peak_negative — peak_negative_window

```text
time: 0.1177999908924104 → 0.1257999908924104 s
duration: 0.007999999999999993 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.7270026339094273 delta_before=-0.013442237931547973 trend=increase
C_edge_capacity: during=0.0507751438683504 delta_before=-0.01344223793154796 trend=increase
F_route_fragmentation: during=0.7777777777777778 delta_before=0.0 trend=flat
S_edge_response: during=0.0507751438683504 delta_before=-0.01344223793154796 trend=increase
S_power_balance: during=None delta_before=None trend=na
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=None delta_before=None trend=na
softx_lower_proxy: during=-0.0004196166989192 delta_before=-7.629394498429997e-05 trend=increase
softx_upper_proxy: during=-0.0008964538577013 delta_before=-9.536743170260006e-05 trend=decrease
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