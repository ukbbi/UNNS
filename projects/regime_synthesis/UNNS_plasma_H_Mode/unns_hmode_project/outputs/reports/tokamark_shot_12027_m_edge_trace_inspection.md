# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_12027_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     463
time_min: -0.0572000071406364
time_max: 0.4047999928593639
```

State counts:

```text
negative_leakage_margin: 243
positive_boundary_margin: 128
insufficient_data: 48
boundary_ambiguous_margin: 44
```

## 5. Inspected windows

| window_label   | state                    |   start_time |    end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                           |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|------------:|-----------:|--------------:|:---------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| peak_positive  | peak_positive_window     |  -0.0132     | -0.00620001 |      0.007 |             8 | fragile_positive_candidate       | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure                           |                0.501086 |                        0.602571  |                              0.550744  |                        0.602571  |                      0.000580564 |                              |                              0.777778 |
| positive_001   | positive_boundary_margin |  -0.00920001 |  0.00279999 |      0.012 |            13 | fragile_positive_candidate       | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure                           |                0.499129 |                        0.600614  |                              0.101485  |                        0.600614  |                      0.000580822 |                              |                              0.555556 |
| positive_002   | positive_boundary_margin |   0.0298     |  0.0348     |      0.005 |             6 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                              |                0.231515 |                        0.312798  |                              0.0812821 |                        0.386231  |                      0.000580305 |                              |                              0.444444 |
| positive_003   | positive_boundary_margin |   0.0368     |  0.0428     |      0.006 |             7 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                              |                0.22148  |                        0.282562  |                              0.0610812 |                        0.390021  |                      0.000580736 |                              |                              0.333333 |
| positive_004   | positive_boundary_margin |   0.0448     |  0.0908     |      0.046 |            47 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                              |                0.261998 |                        0.323594  |                              0.0610815 |                        0.348947  |                      0.000581081 |                              |                              0.333333 |
| negative_001   | negative_leakage_margin  |   0.0978     |  0.1078     |      0.01  |            11 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before                            |               -0.282795 |                        0.343675  |                              0.635855  |                        0.225781  |                      0.703082    |                              |                              0.333333 |
| negative_002   | negative_leakage_margin  |   0.1168     |  0.3478     |      0.231 |           232 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before                            |               -0.372829 |                        0.492808  |                              0.86386   |                        0.295672  |                      0.976506    |                              |                              0.333333 |
| peak_negative  | peak_negative_window     |   0.3288     |  0.3368     |      0.008 |             9 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before  |               -0.841023 |                        0.0645454 |                              0.893104  |                        0.0645454 |                      0.968115    |                              |                              0.555556 |
| positive_005   | positive_boundary_margin |   0.3528     |  0.4048     |      0.052 |            53 | fragile_positive_candidate       | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.472538 |                        0.573588  |                              0.101802  |                        0.573588  |                      0.000967909 |                              |                              0.555556 |

## 6. Interpretability flags

```text
fragile_positive_candidate: 3
interpretable_positive_candidate: 3
interpretable_negative_candidate: 2
fragile_negative_candidate: 1
```

## 7. Detailed window notes

### peak_positive — peak_positive_window

```text
time: -0.0132000071406364 → -0.0062000071406363 s
duration: 0.0070000000000001 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure

m_edge: during=0.50108587874485 delta_before=None trend=decrease
C_edge_capacity: during=0.6025708809035621 delta_before=None trend=decrease
F_route_fragmentation: during=0.55074389314229 delta_before=-0.44925610685771 trend=decrease
S_edge_response: during=0.6025708809035621 delta_before=None trend=decrease
S_power_balance: during=0.0005805639799989 delta_before=None trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.004882812499878 delta_before=None trend=flat
softx_lower_proxy: during=0.00028610229490395 delta_before=None trend=decrease
softx_upper_proxy: during=2.384185790268184e-05 delta_before=None trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.3294908404350281 delta_before=None trend=decrease
missingness_pressure: during=0.7777777777777778 delta_before=-0.2222222222222222 trend=decrease
```

### positive_001 — positive_boundary_margin

```text
time: -0.0092000071406364 → 0.0027999928593636 s
duration: 0.012 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure

m_edge: during=0.4991288347492058 delta_before=-0.004539563991546425 trend=decrease
C_edge_capacity: during=0.6006143656284446 delta_before=-0.004541819396887581 trend=decrease
F_route_fragmentation: during=0.1014853193910187 delta_before=-0.8985146806089813 trend=decrease
S_edge_response: during=0.6006143656284446 delta_before=-0.004541819396887581 trend=decrease
S_power_balance: during=0.0005808224655661 delta_before=-3.015092130300009e-06 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.0048828125 delta_before=-2.4400013259873177e-13 trend=increase
softx_lower_proxy: during=0.0002288818359468 delta_before=-0.00020980834959139999 trend=decrease
softx_upper_proxy: during=-0.000152587890623 delta_before=-0.0002670288085765 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.7688118815422058 delta_before=-5.124438583850861 trend=decrease
missingness_pressure: during=0.5555555555555556 delta_before=-0.4444444444444444 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.0297999928593636 → 0.0347999928593636 s
duration: 0.0050000000000000044 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.231515182212955 delta_before=0.05859593662451401 trend=decrease
C_edge_capacity: during=0.31279816416964684 delta_before=0.03839423365484712 trend=decrease
F_route_fragmentation: during=0.08128210092317385 delta_before=-0.02020258400318485 trend=decrease
S_edge_response: during=0.3862308681546682 delta_before=0.1118269376398685 trend=increase
S_power_balance: during=0.0005803054943835 delta_before=2.584856241000114e-07 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.1647949218837947 delta_before=-0.08911132812230393 trend=decrease
softx_lower_proxy: during=0.00011444091798282658 delta_before=-3.814697273387343e-05 trend=increase
softx_upper_proxy: during=-0.0003242492675449 delta_before=-0.00013351440421780002 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=-0.1098302826285362 delta_before=0.4393211379647255 trend=increase
missingness_pressure: during=0.4444444444444444 delta_before=-0.11111111111111116 trend=decrease
```

### positive_003 — positive_boundary_margin

```text
time: 0.0367999928593636 → 0.0427999928593636 s
duration: 0.006000000000000005 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.2214796120419042 delta_before=0.004341696503475795 trend=increase
C_edge_capacity: during=0.2825620192200034 delta_before=-0.007760955977360096 trend=increase
F_route_fragmentation: during=0.061081208541683 delta_before=-0.0404000931759496 trend=increase
S_edge_response: during=0.3900210460204546 delta_before=0.03075392562894763 trend=increase
S_power_balance: during=0.0005807363657607 delta_before=1.7238576179999694e-07 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.1611328125035219 delta_before=-0.024414062499786587 trend=decrease
softx_lower_proxy: during=0.0003433227538407 delta_before=0.0002098083495539 trend=decrease
softx_upper_proxy: during=-0.000419616699183 delta_before=-0.00013351440428669998 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=0.6224769949913025 delta_before=0.2929861545562744 trend=increase
missingness_pressure: during=0.3333333333333333 delta_before=-0.22222222222222227 trend=flat
```

### positive_004 — positive_boundary_margin

```text
time: 0.0447999928593636 → 0.0907999928593636 s
duration: 0.046000000000000006 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.2619979512417698 delta_before=0.04486003570334138 trend=increase
C_edge_capacity: during=0.3235936053343799 delta_before=0.04537525676185322 trend=increase
F_route_fragmentation: during=0.0610814904751983 delta_before=2.8193351529759436e-07 trend=increase
S_edge_response: during=0.3489467168755109 delta_before=-0.041074329144943744 trend=decrease
S_power_balance: during=0.0005810809511683 delta_before=3.445854075999951e-07 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.19775390625 delta_before=0.036621093746478095 trend=increase
softx_lower_proxy: during=0.0002670288086578 delta_before=5.7220459056500005e-05 trend=increase
softx_upper_proxy: during=-3.814697264513269e-05 delta_before=0.0002098083496001673 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=1.2081329822540283 delta_before=0.5856559872627258 trend=increase
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### negative_001 — negative_leakage_margin

```text
time: 0.0977999928593637 → 0.1077999928593637 s
duration: 0.010000000000000009 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.2827950933909597 delta_before=-0.3627781570386239 trend=increase
C_edge_capacity: during=0.3436752719453168 delta_before=0.00951855018189729 trend=increase
F_route_fragmentation: during=0.6358549220331919 delta_before=0.3751091676441115 trend=decrease
S_edge_response: during=0.2257811556527067 delta_before=-0.029330364793134805 trend=decrease
S_power_balance: during=0.7030819417442716 delta_before=0.45846676045391394 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3002929687508335 delta_before=0.025634765624661215 trend=increase
softx_lower_proxy: during=0.0007057189940841 delta_before=0.0002670288084914 trend=increase
softx_upper_proxy: during=0.0003433227538968 delta_before=0.00016212463379429998 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=1193968.875 delta_before=779208.28125 trend=decrease
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.1167999928593637 → 0.3477999928593639 s
duration: 0.2310000000000002 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.37282902881710284 delta_before=-0.19978196944510634 trend=decrease
C_edge_capacity: during=0.4928079834980067 delta_before=0.15995161657469842 trend=increase
F_route_fragmentation: during=0.8638598226627374 delta_before=0.35664556045098694 trend=increase
S_edge_response: during=0.2956719309443503 delta_before=0.0919105315364746 trend=increase
S_power_balance: during=0.9765062920621942 delta_before=0.43065182343301767 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.40527343750092154 delta_before=0.08544921874836015 trend=decrease
softx_lower_proxy: during=0.010967254638941451 delta_before=0.010204315185809651 trend=decrease
softx_upper_proxy: during=0.0117778778074797 delta_before=0.0114727020261155 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=1658679.8125 delta_before=731934.125 trend=increase
missingness_pressure: during=0.3333333333333333 delta_before=0.0 trend=increase
```

### peak_negative — peak_negative_window

```text
time: 0.3287999928593639 → 0.3367999928593639 s
duration: 0.008000000000000007 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.8410233712963902 delta_before=-0.08957238355514863 trend=increase
C_edge_capacity: during=0.0645453506479027 delta_before=-0.07358058868540748 trend=increase
F_route_fragmentation: during=0.8931044297727376 delta_before=0.006083183547960669 trend=increase
S_edge_response: during=0.0645453506479027 delta_before=-0.07358058868540748 trend=increase
S_power_balance: during=0.9681152907098892 delta_before=0.004311392186671648 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.864257812484279 delta_before=0.319824218734279 trend=decrease
softx_lower_proxy: during=-0.0016021728516088 delta_before=-0.0118827819779556 trend=decrease
softx_upper_proxy: during=-0.0019836425785763 delta_before=-0.0069427490236738006 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=1644418.5 delta_before=7327.625 trend=increase
missingness_pressure: during=0.5555555555555556 delta_before=0.0 trend=flat
```

### positive_005 — positive_boundary_margin

```text
time: 0.3527999928593639 → 0.4047999928593639 s
duration: 0.05199999999999999 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4725384046986675 delta_before=0.7349957680021556 trend=increase
C_edge_capacity: during=0.5735877862538696 delta_before=0.011360963154866122 trend=increase
F_route_fragmentation: during=0.1018020268497619 delta_before=-0.7167476606723473 trend=decrease
S_edge_response: during=0.5735877862538696 delta_before=0.011360963154866122 trend=increase
S_power_balance: during=0.0009679093595855 delta_before=-0.8760249185995357 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.0048828124978315 delta_before=-0.0073242187519379 trend=decrease
softx_lower_proxy: during=-0.0016593933104083 delta_before=0.00038146972678919974 trend=increase
softx_upper_proxy: during=-0.0015830993652669 delta_before=0.0003051757811367 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=658.66015625 delta_before=-1488888.46484375 trend=decrease
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