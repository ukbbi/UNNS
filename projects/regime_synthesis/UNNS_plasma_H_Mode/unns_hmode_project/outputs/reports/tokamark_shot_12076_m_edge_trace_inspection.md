# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12076_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     371
time_min: -0.0690000057220459
time_max: 0.3009999942779544
```

State counts:

```text
boundary_ambiguous_margin: 189
positive_boundary_margin: 72
insufficient_data: 60
negative_leakage_margin: 50
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                 |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:-------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| peak_positive  | peak_positive_window     |        0.193 |      0.201 |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                            |                0.404028 |                        0.720423  |                               0.331475 |                        0.62927   |                         0.386062 |                     0.314571 |                              0.222222 |
| positive_001   | positive_boundary_margin |        0.193 |      0.205 |      0.012 |            13 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before                            |                0.386081 |                        0.698266  |                               0.348676 |                        0.604428  |                         0.386062 |                     0.349495 |                              0.222222 |
| positive_002   | positive_boundary_margin |        0.207 |      0.214 |      0.007 |             8 | interpretable_positive_candidate | capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.349    |                        0.650132  |                               0.294884 |                        0.565677  |                         0.201245 |                     0.43527  |                              0.222222 |
| peak_negative  | peak_negative_window     |        0.227 |      0.235 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before                              |               -0.266008 |                        0.0977298 |                               0.489415 |                        0.0287197 |                         0.499408 |                   nan        |                              0.444444 |
| negative_001   | negative_leakage_margin  |        0.243 |      0.249 |      0.006 |             7 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.471772 |                        0.396336  |                               0.871202 |                        0.568529  |                         0.966036 |                   nan        |                              0.444444 |

## 6. Interpretability flags

```text
interpretable_positive_candidate: 3
interpretable_negative_candidate: 2
```

## 7. Detailed window notes

### peak_positive — peak_positive_window

```text
time: 0.1929999942779543 → 0.2009999942779543 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.4040283266820957 delta_before=0.2791285645778472 trend=increase
C_edge_capacity: during=0.7204234464788609 delta_before=0.03657236391848029 trend=decrease
F_route_fragmentation: during=0.3314749227179361 delta_before=-0.18506814389516002 trend=decrease
S_edge_response: during=0.6292703574199214 delta_before=0.09715479613367362 trend=decrease
S_power_balance: during=0.386062102754917 delta_before=-0.45369950997657477 trend=decrease
S_transport: during=0.3145711208585565 delta_before=-0.0809763611595925 trend=decrease
dalpha_proxy: during=0.2246093749800235 delta_before=-0.16601562510547938 trend=decrease
softx_lower_proxy: during=0.0117683410618675 delta_before=-0.00011444091898229862 trend=decrease
softx_upper_proxy: during=0.0367164611833445 delta_before=-0.004234313961297503 trend=decrease
te_profile_gradient_proxy: during=6.302340252713611 delta_before=-3.3900264531605337 trend=decrease
ne_profile_gradient_proxy: during=6.175202314160022e+17 delta_before=7.33302578398201e+16 trend=decrease
density_proxy: during=1.2878850615805372e+20 delta_before=-1.0844922989405798e+19 trend=decrease
nbi_proxy: during=-0.2928789556026459 delta_before=-1.4645902812480927 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_001 — positive_boundary_margin

```text
time: 0.1929999942779543 → 0.2049999942779543 s
duration: 0.011999999999999983 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;m_edge_higher_than_before

m_edge: during=0.3860814571431559 delta_before=0.2611816950389074 trend=increase
C_edge_capacity: during=0.6982657821443142 delta_before=0.014414699583933599 trend=decrease
F_route_fragmentation: during=0.3486759382978021 delta_before=-0.16786712831529405 trend=decrease
S_edge_response: during=0.6044281093132482 delta_before=0.07231254802700038 trend=decrease
S_power_balance: during=0.386062102754917 delta_before=-0.45369950997657477 trend=decrease
S_transport: during=0.349494980461101 delta_before=-0.04605250155704799 trend=decrease
dalpha_proxy: during=0.2246093749800235 delta_before=-0.16601562510547938 trend=decrease
softx_lower_proxy: during=0.0115203857409389 delta_before=-0.0003623962399108994 trend=decrease
softx_upper_proxy: during=0.0322723388630349 delta_before=-0.008678436281607103 trend=decrease
te_profile_gradient_proxy: during=6.927600415623909 delta_before=-2.764766290250236 trend=decrease
ne_profile_gradient_proxy: during=5.859309073542889e+17 delta_before=4.174093377810682e+16 trend=decrease
density_proxy: during=1.2439582526369328e+20 delta_before=-1.5237603883766235e+19 trend=decrease
nbi_proxy: during=-0.2928789556026459 delta_before=-1.4645902812480927 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.2069999942779543 → 0.2139999942779543 s
duration: 0.007000000000000006 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.34900024426049714 delta_before=0.02131880293099836 trend=decrease
C_edge_capacity: during=0.6501316862090727 delta_before=-0.03795837045991535 trend=decrease
F_route_fragmentation: during=0.294884165264362 delta_before=-0.05379177303344007 trend=increase
S_edge_response: during=0.5656771553010107 delta_before=-0.03328489216849395 trend=decrease
S_power_balance: during=0.20124507520375065 delta_before=-0.13316834760465515 trend=increase
S_transport: during=0.4352698040956746 delta_before=0.08577482363457362 trend=decrease
dalpha_proxy: during=0.21972656248952388 delta_before=-0.00244140626047612 trend=flat
softx_lower_proxy: during=0.00851631164480815 delta_before=-0.00226020813184955 trend=decrease
softx_upper_proxy: during=0.0227451324462054 delta_before=-0.007162094118029899 trend=decrease
te_profile_gradient_proxy: during=10.779740409804628 delta_before=3.8521399941807193 trend=decrease
ne_profile_gradient_proxy: during=3.4393474563296237e+17 delta_before=-1.6297279473322944e+17 trend=decrease
density_proxy: during=1.166834548822864e+20 delta_before=-3.1416213799048315e+18 trend=decrease
nbi_proxy: during=-0.7322951406240463 delta_before=-0.43941618502140045 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### peak_negative — peak_negative_window

```text
time: 0.2269999942779543 → 0.2349999942779543 s
duration: 0.00799999999999998 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.2660080609183866 delta_before=-0.4276795233307136 trend=increase
C_edge_capacity: during=0.0977297790426103 delta_before=-0.5030388372380765 trend=decrease
F_route_fragmentation: during=0.4894149979796579 delta_before=0.08452653157458329 trend=decrease
S_edge_response: during=0.0287196769365938 delta_before=-0.4864633248903551 trend=increase
S_power_balance: during=0.4994084543208165 delta_before=0.030096300224376205 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.498046875067329 delta_before=0.28564453136069706 trend=decrease
softx_lower_proxy: during=-0.0008010864241276 delta_before=-0.0064849853512556 trend=decrease
softx_upper_proxy: during=-0.0017166137703202 delta_before=-0.017433166504102197 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=2.130697843783395e+19 delta_before=-8.596719018548029e+19 trend=decrease
nbi_proxy: during=-0.2928789556026459 delta_before=-0.5857579112052917 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=0.2222222222222222 trend=flat
```

### negative_001 — negative_leakage_margin

```text
time: 0.2429999942779543 → 0.2489999942779543 s
duration: 0.006000000000000005 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.4717721016162355 delta_before=-0.176208693728587 trend=increase
C_edge_capacity: during=0.3963357916827017 delta_before=0.02609837068266152 trend=decrease
F_route_fragmentation: during=0.8712015465749195 delta_before=0.33498857194409626 trend=decrease
S_edge_response: during=0.5685287412757544 delta_before=0.021130558957632828 trend=decrease
S_power_balance: during=0.9660364581594696 delta_before=0.409430476820562 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.0024414062265947 delta_before=-0.014648437512000801 trend=decrease
softx_lower_proxy: during=-0.001220703124169 delta_before=-3.814697191500006e-05 trend=decrease
softx_upper_proxy: during=-0.0011634826658309 delta_before=0.0006294250482928 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=5.224805587912491e+18 delta_before=3.3271100910222705e+18 trend=decrease
nbi_proxy: during=1.1717113256454468 delta_before=1.4645902812480927 trend=decrease
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