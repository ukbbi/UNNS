# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11830_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     376
time_min: -0.0672000050544738
time_max: 0.3077999949455264
```

State counts:

```text
boundary_ambiguous_margin: 147
negative_leakage_margin: 86
positive_boundary_margin: 85
insufficient_data: 58
```

## 5. Inspected windows

| window_label   | state                    |   start_time |    end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                           |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|------------:|-----------:|--------------:|:---------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| positive_001   | positive_boundary_margin |  -0.00920001 | -0.00320001 |      0.006 |             7 | fragile_positive_candidate       | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure                           |                0.299996 |                         0.666667 |                               0.366671 |                         1        |                      0.300005    |                   nan        |                              0.666667 |
| positive_002   | positive_boundary_margin |   0.0268     |  0.0958     |      0.069 |            70 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                              |                0.324826 |                         0.513876 |                               0.192528 |                         0.462645 |                      0.0319097   |                     0.309894 |                              0.222222 |
| peak_positive  | peak_positive_window     |   0.0648     |  0.0728     |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                              |                0.37245  |                         0.540046 |                               0.15357  |                         0.444838 |                      5.46313e-06 |                     0.288714 |                              0.222222 |
| negative_001   | negative_leakage_margin  |   0.2148     |  0.2948     |      0.08  |            81 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                    |               -0.26207  |                         0.666709 |                               0.926373 |                         0.995067 |                      0.984085    |                     0.67379  |                              0.666667 |
| peak_negative  | peak_negative_window     |   0.2338     |  0.2418     |      0.008 |             9 | fragile_negative_candidate       | high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before  |               -0.450563 |                         0.262831 |                               0.869306 |                         0.114564 |                      0.914336    |                   nan        |                              0.666667 |
| positive_003   | positive_boundary_margin |   0.3038     |  0.3078     |      0.004 |             5 | fragile_positive_candidate       | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |                0.304381 |                         0.670219 |                               0.365496 |                         1        |                      0.298569    |                   nan        |                              0.666667 |

## 6. Interpretability flags

```text
fragile_positive_candidate: 2
interpretable_positive_candidate: 2
fragile_negative_candidate: 2
```

## 7. Detailed window notes

### positive_001 — positive_boundary_margin

```text
time: -0.0092000050544738 → -0.0032000050544738 s
duration: 0.005999999999999999 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure

m_edge: during=0.29999612634065 delta_before=-5.961717263192057e-07 trend=decrease
C_edge_capacity: during=0.6666666666666666 delta_before=0.0 trend=decrease
F_route_fragmentation: during=0.3666705403260166 delta_before=-0.6333294596739834 trend=increase
S_edge_response: during=1.0 delta_before=0.0 trend=decrease
S_power_balance: during=0.3000047344725388 delta_before=7.286543322049255e-07 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.0048828125 delta_before=-2.1616996387363585e-12 trend=increase
softx_lower_proxy: during=None delta_before=None trend=na
softx_upper_proxy: during=None delta_before=None trend=na
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-3.460821425198203e+17 delta_before=2.122318575619277e+16 trend=decrease
nbi_proxy: during=-1.2741320133209229 delta_before=1.7574234008789062 trend=increase
missingness_pressure: during=0.6666666666666667 delta_before=-0.33333333333333326 trend=flat
```

### positive_002 — positive_boundary_margin

```text
time: 0.0267999949455262 → 0.0957999949455262 s
duration: 0.069 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.32482630864554635 delta_before=0.16898609251109842 trend=decrease
C_edge_capacity: during=0.5138759657550047 delta_before=0.17942627626955043 trend=increase
F_route_fragmentation: during=0.19252756101844537 delta_before=0.016409333911025004 trend=increase
S_edge_response: during=0.4626454366887073 delta_before=0.1477219829965556 trend=increase
S_power_balance: during=0.0319096630246236 delta_before=-0.06318945754320869 trend=increase
S_transport: during=0.30989362807759546 delta_before=0.10989362807759545 trend=increase
dalpha_proxy: during=0.45776367187207434 delta_before=-0.007324218802307658 trend=increase
softx_lower_proxy: during=None delta_before=None trend=na
softx_upper_proxy: during=None delta_before=None trend=na
te_profile_gradient_proxy: during=7.527672208679412 delta_before=5.299033644488497 trend=decrease
ne_profile_gradient_proxy: during=8322386633645760.0 delta_before=5670965106597632.0 trend=increase
density_proxy: during=8.20306966654841e+19 delta_before=2.1993225426170806e+19 trend=increase
nbi_proxy: during=0.9224921464920044 delta_before=3.0749735832214355 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=-0.2222222222222222 trend=decrease
```

### peak_positive — peak_positive_window

```text
time: 0.0647999949455262 → 0.0727999949455262 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.372450346369062 delta_before=0.04145837391854479 trend=decrease
C_edge_capacity: during=0.5400460434068379 delta_before=0.04503623705644633 trend=increase
F_route_fragmentation: during=0.1535700994360012 delta_before=-0.010303062020352416 trend=increase
S_edge_response: during=0.4448378141772486 delta_before=-0.007852195261733919 trend=increase
S_power_balance: during=5.463126920377554e-06 delta_before=-0.017565126400997323 trend=decrease
S_transport: during=0.2887138771634909 delta_before=-0.011029420500374087 trend=increase
dalpha_proxy: during=0.4638671875051431 delta_before=0.009765625051357307 trend=increase
softx_lower_proxy: during=None delta_before=None trend=na
softx_upper_proxy: during=None delta_before=None trend=na
te_profile_gradient_proxy: during=7.276113921055167 delta_before=-0.2515582876242455 trend=increase
ne_profile_gradient_proxy: during=6293367705184240.0 delta_before=-689414746770160.0 trend=increase
density_proxy: during=8.752225147087644e+19 delta_before=6.52591817019936e+18 trend=increase
nbi_proxy: during=-1.1274902820587158 delta_before=-2.04998242855072 trend=decrease
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### negative_001 — negative_leakage_margin

```text
time: 0.2147999949455263 → 0.2947999949455264 s
duration: 0.0800000000000001 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.2620703759350767 delta_before=-0.06493089096248511 trend=increase
C_edge_capacity: during=0.6667089928262065 delta_before=0.13160711909016065 trend=increase
F_route_fragmentation: during=0.9263725096920205 delta_before=0.19370419139979966 trend=increase
S_edge_response: during=0.9950672092866004 delta_before=0.5979708496756688 trend=increase
S_power_balance: during=0.98408491925321 delta_before=0.07659065177557012 trend=increase
S_transport: during=0.6737903241821331 delta_before=0.0 trend=decrease
dalpha_proxy: during=0.0024414062375181 delta_before=-0.881347656272809 trend=decrease
softx_lower_proxy: during=None delta_before=None trend=na
softx_upper_proxy: during=None delta_before=None trend=na
te_profile_gradient_proxy: during=13.949578498432018 delta_before=0.6822890711408576 trend=decrease
ne_profile_gradient_proxy: during=1.3160355648766592e+16 delta_before=0.0 trend=decrease
density_proxy: during=7.183509686493118e+18 delta_before=-1.4416678155947763e+20 trend=decrease
nbi_proxy: during=1674802.625 delta_before=16689.5 trend=decrease
missingness_pressure: during=0.6666666666666667 delta_before=0.44444444444444453 trend=increase
```

### peak_negative — peak_negative_window

```text
time: 0.2337999949455264 → 0.2417999949455264 s
duration: 0.008000000000000007 s
flag: fragile_negative_candidate
notes: high_missingness_pressure;fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.4505628349403782 delta_before=-0.027227375929382958 trend=increase
C_edge_capacity: during=0.2628306310185048 delta_before=0.0271538855086203 trend=increase
F_route_fragmentation: during=0.8693055996526259 delta_before=0.21094044643775456 trend=increase
S_edge_response: during=0.1145640646644492 delta_before=0.019731162840451608 trend=increase
S_power_balance: during=0.9143364736495058 delta_before=0.21295482138460675 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.8740234375785505 delta_before=-0.15136718742696553 trend=decrease
softx_lower_proxy: during=None delta_before=None trend=na
softx_upper_proxy: during=None delta_before=None trend=na
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=2.6291189990868124e+19 delta_before=-5.832270808900593e+19 trend=decrease
nbi_proxy: during=1673408.375 delta_before=5219.625 trend=increase
missingness_pressure: during=0.6666666666666667 delta_before=0.22222222222222232 trend=flat
```

### positive_003 — positive_boundary_margin

```text
time: 0.3037999949455264 → 0.3077999949455264 s
duration: 0.0040000000000000036 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3043813299943004 delta_before=0.3094167696728437 trend=increase
C_edge_capacity: during=0.6702186911701987 delta_before=0.0017492705152490906 trend=decrease
F_route_fragmentation: during=0.3654959764514897 delta_before=-0.3072545648360686 trend=decrease
S_edge_response: during=1.0 delta_before=3.5016434196677437e-13 trend=flat
S_power_balance: during=0.2985691564036726 delta_before=-0.3755333570218617 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.0048828124860612 delta_before=-0.0024414062360612002 trend=flat
softx_lower_proxy: during=None delta_before=None trend=na
softx_upper_proxy: during=None delta_before=None trend=na
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=6.223486501863293e+18 delta_before=3.9203746795329946e+17 trend=decrease
nbi_proxy: during=9248.9580078125 delta_before=-897178.2919921875 trend=decrease
missingness_pressure: during=0.6666666666666667 delta_before=0.0 trend=flat
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```