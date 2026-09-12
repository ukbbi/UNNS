# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11946_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     546
time_min: -0.0588000118732452
time_max: 0.4861999881267552
```

State counts:

```text
boundary_ambiguous_margin: 433
positive_boundary_margin: 63
insufficient_data: 50
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                                           |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median |   S_transport__during_median |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|-----------------------------:|--------------------------------------:|
| positive_001   | positive_boundary_margin |       0.3522 |     0.4102 |      0.058 |            59 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                                              |               0.313524  |                         0.507755 |                               0.180351 |                        0.256257  |                       0.106208   |                      0.34695 |                              0        |
| peak_negative  | peak_negative_window     |       0.4122 |     0.4202 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before                                                        |               0.0352135 |                         0.13474  |                               0.234394 |                        0.0120284 |                       0.187716   |                    nan       |                              0.444444 |
| peak_positive  | peak_positive_window     |       0.4812 |     0.4862 |      0.005 |             6 | fragile_positive_candidate       | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |               0.473827  |                         0.576018 |                               0.102195 |                        0.57746   |                       0.00144654 |                    nan       |                              0.555556 |
| positive_002   | positive_boundary_margin |       0.4822 |     0.4852 |      0.003 |             4 | fragile_positive_candidate       | high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before |               0.475152  |                         0.577342 |                               0.10219  |                        0.577342  |                       0.00144204 |                    nan       |                              0.555556 |

## 6. Interpretability flags

```text
fragile_positive_candidate: 2
interpretable_positive_candidate: 1
interpretable_negative_candidate: 1
```

## 7. Detailed window notes

### positive_001 — positive_boundary_margin

```text
time: 0.3521999881267551 → 0.4101999881267552 s
duration: 0.05800000000000005 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3135244316367809 delta_before=0.1545988506211928 trend=increase
C_edge_capacity: during=0.507755358416609 delta_before=-0.1040967754459684 trend=decrease
F_route_fragmentation: during=0.1803511256153796 delta_before=-0.26870156303160697 trend=decrease
S_edge_response: during=0.2562569211365185 delta_before=-0.0399630478569552 trend=increase
S_power_balance: during=0.1062083540841273 delta_before=-0.5379467357705957 trend=decrease
S_transport: during=0.3469504524371123 delta_before=-0.006789321368134871 trend=decrease
dalpha_proxy: during=0.3686523437433728 delta_before=-0.18798828123784345 trend=decrease
softx_lower_proxy: during=0.001049041748461 delta_before=-0.0144004821768406 trend=decrease
softx_upper_proxy: during=0.0017547607423204 delta_before=-0.0041770935057906 trend=increase
te_profile_gradient_proxy: during=6.976319924581048 delta_before=-0.21495461599971577 trend=increase
ne_profile_gradient_proxy: during=8.013570733745316e+17 delta_before=-3.914896547418112e+16 trend=decrease
density_proxy: during=1.07757294032559e+20 delta_before=-3.4177368971370578e+19 trend=decrease
nbi_proxy: during=255.9915008544922 delta_before=-934594.0709991455 trend=decrease
missingness_pressure: during=0.0 delta_before=0.0 trend=increase
```

### peak_negative — peak_negative_window

```text
time: 0.4121999881267552 → 0.4201999881267552 s
duration: 0.008000000000000007 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;edge_response_low;m_edge_lower_than_before

m_edge: during=0.0352135047895804 delta_before=-0.23653123120225045 trend=increase
C_edge_capacity: during=0.1347398863970444 delta_before=-0.25853627543216706 trend=increase
F_route_fragmentation: during=0.2343935591673967 delta_before=0.11634702555247091 trend=increase
S_edge_response: during=0.0120283779421357 delta_before=-0.26905527146315994 trend=increase
S_power_balance: during=0.1877155846613862 delta_before=0.13826053727652068 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.5517578124879382 delta_before=0.25146484373321853 trend=decrease
softx_lower_proxy: during=-0.0020790100097468 delta_before=-0.0017213821410250003 trend=decrease
softx_upper_proxy: during=-0.0029373168943411 delta_before=-0.0062561035158774005 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=2.2360530479568912e+19 delta_before=-7.209393069820268e+19 trend=decrease
nbi_proxy: during=-196.33392333984372 delta_before=-392.7636470794678 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.4811999881267552 → 0.4861999881267552 s
duration: 0.0050000000000000044 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4738268848825628 delta_before=0.3890073444577939 trend=increase
C_edge_capacity: during=0.5760180625265064 delta_before=0.18742322211124923 trend=increase
F_route_fragmentation: during=0.10219547342179415 delta_before=-0.20183129989562498 trend=decrease
S_edge_response: during=0.5774600028318548 delta_before=0.0002950229589563369 trend=increase
S_power_balance: during=0.00144653824754085 delta_before=-0.27137630815276154 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.0048828125 delta_before=0.0 trend=flat
softx_lower_proxy: during=-0.0016593933101472 delta_before=-7.629394295499995e-05 trend=increase
softx_upper_proxy: during=-0.0013923645019747 delta_before=0.0001716613769957001 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=6.553243233172849e+17 delta_before=-1.4632916468954563e+18 trend=flat
nbi_proxy: during=8.834420084953308 delta_before=5.854545712471008 trend=decrease
missingness_pressure: during=0.5555555555555556 delta_before=0.11111111111111116 trend=increase
```

### positive_002 — positive_boundary_margin

```text
time: 0.4821999881267552 → 0.4851999881267552 s
duration: 0.0030000000000000027 s
flag: fragile_positive_candidate
notes: high_missingness_pressure;capacity_exceeds_fragmentation;edge_response_high;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.4751519285243555 delta_before=0.3903323880995866 trend=increase
C_edge_capacity: during=0.5773418785909863 delta_before=0.18874703817572908 trend=increase
F_route_fragmentation: during=0.10218995006663059 delta_before=-0.20183682325078853 trend=increase
S_edge_response: during=0.5773418785909863 delta_before=0.0012718490698010454 trend=increase
S_power_balance: during=0.0014420377357584001 delta_before=-0.271380808664544 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-0.004882812498617601 delta_before=1.3823994032824416e-12 trend=flat
softx_lower_proxy: during=-0.0016307830808764 delta_before=-7.629394508110003e-05 trend=decrease
softx_upper_proxy: during=-0.00155448913565625 delta_before=4.7683715970050144e-05 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=None delta_before=None trend=na
nbi_proxy: during=1.3689956665039062 delta_before=-1.6108787059783936 trend=increase
missingness_pressure: during=0.5555555555555556 delta_before=0.11111111111111116 trend=flat
```

## 8. Main conclusion

The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.

If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.

## 9. Next document

```text
docs/
  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md
```