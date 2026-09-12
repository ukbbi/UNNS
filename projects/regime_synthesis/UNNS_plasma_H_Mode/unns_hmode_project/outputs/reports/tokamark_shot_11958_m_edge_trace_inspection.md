# TokaMark m_edge(t) Trace Inspection

## 1. Purpose

This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.

This is trace-level triage. It is not formula revision and not physical validation.

## 2. Input

```text
outputs\reports\tokamark_shot_11958_m_edge_t_probe.csv
```

## 3. Settings

```text
minimum interval duration: 0.003 s
context width before/after: 0.01 s
```

## 4. Global trace summary

```text
rows:     453
time_min: -0.0580000057816505
time_max: 0.3939999942183498
```

State counts:

```text
boundary_ambiguous_margin: 186
negative_leakage_margin: 114
positive_boundary_margin: 103
insufficient_data: 50
```

## 5. Inspected windows

| window_label   | state                    |   start_time |   end_time |   duration |   point_count | interpretability_flag            | interpretability_notes                                                                                |   m_edge__during_median |   C_edge_capacity__during_median |   F_route_fragmentation__during_median |   S_edge_response__during_median |   S_power_balance__during_median | S_transport__during_median   |   missingness_pressure__during_median |
|:---------------|:-------------------------|-------------:|-----------:|-----------:|--------------:|:---------------------------------|:------------------------------------------------------------------------------------------------------|------------------------:|---------------------------------:|---------------------------------------:|---------------------------------:|---------------------------------:|:-----------------------------|--------------------------------------:|
| positive_001   | positive_boundary_margin |        0.047 |      0.141 |      0.094 |            95 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                   |                0.29327  |                         0.340141 |                              0.0495264 |                        0.239342  |                       0.0111496  |                              |                              0.222222 |
| peak_positive  | peak_positive_window     |        0.131 |      0.139 |      0.008 |             9 | interpretable_positive_candidate | capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before                   |                0.33533  |                         0.38285  |                              0.0473508 |                        0.210789  |                       0.00849051 |                              |                              0.222222 |
| negative_001   | negative_leakage_margin  |        0.271 |      0.276 |      0.005 |             6 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                   |               -0.206003 |                         0.60225  |                              0.811311  |                        0.38339   |                       0.94222    |                              |                              0.222222 |
| negative_002   | negative_leakage_margin  |        0.312 |      0.393 |      0.081 |            82 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before                   |               -0.416776 |                         0.384653 |                              0.798761  |                        0.574845  |                       0.877498   |                              |                              0.444444 |
| peak_negative  | peak_negative_window     |        0.319 |      0.327 |      0.008 |             9 | interpretable_negative_candidate | fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before |               -0.516838 |                         0.146632 |                              0.719888  |                        0.0438182 |                       0.781098   |                              |                              0.444444 |

## 6. Interpretability flags

```text
interpretable_negative_candidate: 3
interpretable_positive_candidate: 2
```

## 7. Detailed window notes

### positive_001 — positive_boundary_margin

```text
time: 0.0469999942183495 → 0.1409999942183496 s
duration: 0.09400000000000011 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.2932703682029122 delta_before=0.09719434805994229 trend=increase
C_edge_capacity: during=0.3401410028487597 delta_before=0.0573484035826039 trend=increase
F_route_fragmentation: during=0.0495264064817968 delta_before=-0.03978465507663861 trend=decrease
S_edge_response: during=0.2393420682324293 delta_before=-0.1602476445837062 trend=decrease
S_power_balance: during=0.0111495585394801 delta_before=-0.0486256895381138 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3002929687470997 delta_before=0.1342773437446857 trend=increase
softx_lower_proxy: during=0.0003433227534293 delta_before=0.0003242492670793374 trend=increase
softx_upper_proxy: during=5.72204589545965e-05 delta_before=0.00030517578122849653 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=4.424696034133384e+19 delta_before=1.2521880531903717e+19 trend=increase
nbi_proxy: during=-0.4027391672134399 delta_before=0.5856371521949768 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### peak_positive — peak_positive_window

```text
time: 0.1309999942183496 → 0.1389999942183496 s
duration: 0.008000000000000007 s
flag: interpretable_positive_candidate
notes: capacity_exceeds_fragmentation;low_power_balance_pressure;m_edge_higher_than_before

m_edge: during=0.3353295189764969 delta_before=0.02523733372689635 trend=increase
C_edge_capacity: during=0.382850376316051 delta_before=0.0319014065272496 trend=increase
F_route_fragmentation: during=0.0473508215300266 delta_before=0.004496591233395901 trend=increase
S_edge_response: during=0.210788761245091 delta_before=0.06645699840862371 trend=increase
S_power_balance: during=0.0084905102650942 delta_before=0.005495833729706 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.3271484375 delta_before=-0.053710937502846 trend=decrease
softx_lower_proxy: during=0.0007057189941406 delta_before=0.0 trend=decrease
softx_upper_proxy: during=0.0002002716065054 delta_before=7.629394537629999e-05 trend=increase
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=5.344267746172679e+19 delta_before=1.8416291999666668e+18 trend=increase
nbi_proxy: during=4082.395263671875 delta_before=2815.7852783203125 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### negative_001 — negative_leakage_margin

```text
time: 0.2709999942183497 → 0.2759999942183497 s
duration: 0.0050000000000000044 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.20600270951301602 delta_before=-0.009724937947848233 trend=decrease
C_edge_capacity: during=0.6022501884298104 delta_before=-0.005097819828202899 trend=increase
F_route_fragmentation: during=0.8113110087495805 delta_before=0.007359618433056436 trend=increase
S_edge_response: during=0.38338968188574146 delta_before=-0.019107597708462043 trend=increase
S_power_balance: during=0.9422196279778824 delta_before=0.008995089195957595 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.45166015624998646 delta_before=0.021972656238460064 trend=decrease
softx_lower_proxy: during=0.019912719726615402 delta_before=-0.00011444091724409702 trend=decrease
softx_upper_proxy: during=0.01201629638676515 delta_before=-0.0005340576170777492 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=1.1379769425621156e+20 delta_before=2.523511127141253e+18 trend=increase
nbi_proxy: during=1583865.1875 delta_before=-14747.6875 trend=increase
missingness_pressure: during=0.2222222222222222 delta_before=0.0 trend=flat
```

### negative_002 — negative_leakage_margin

```text
time: 0.3119999942183498 → 0.3929999942183498 s
duration: 0.08100000000000002 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;m_edge_lower_than_before

m_edge: during=-0.416775789700106 delta_before=-0.23191619105893538 trend=decrease
C_edge_capacity: during=0.3846526197792499 delta_before=-0.2753517456011222 trend=decrease
F_route_fragmentation: during=0.7987606716071227 delta_before=-0.0442543890641931 trend=decrease
S_edge_response: during=0.5748454705569992 delta_before=0.1258013639920279 trend=increase
S_power_balance: during=0.8774976109766068 delta_before=-0.10290307685168631 trend=decrease
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=-2.1345230270846266e-12 delta_before=-0.4443359374984347 trend=decrease
softx_lower_proxy: during=-0.0014066696168079 delta_before=-0.0240659713777132 trend=decrease
softx_upper_proxy: during=-0.00152587890645785 delta_before=-0.018787384032312553 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=-5.949920862047044e+18 delta_before=-1.3590890552637994e+20 trend=decrease
nbi_proxy: during=1535241.25 delta_before=-30211.875 trend=decrease
missingness_pressure: during=0.4444444444444444 delta_before=0.2222222222222222 trend=flat
```

### peak_negative — peak_negative_window

```text
time: 0.3189999942183498 → 0.3269999942183498 s
duration: 0.008000000000000007 s
flag: interpretable_negative_candidate
notes: fragmentation_exceeds_capacity;power_balance_pressure_high;edge_response_low;m_edge_lower_than_before

m_edge: during=-0.51683781162963 delta_before=-0.18463841371183143 trend=increase
C_edge_capacity: during=0.1466316979113514 delta_before=-0.397451025591996 trend=increase
F_route_fragmentation: during=0.7198883229045109 delta_before=-0.15140065094642507 trend=increase
S_edge_response: during=0.0438182156930073 delta_before=-0.2723058695620138 trend=increase
S_power_balance: during=0.7810980736734146 delta_before=-0.19114797596477628 trend=increase
S_transport: during=None delta_before=None trend=na
dalpha_proxy: during=0.8911132812306198 delta_before=0.3442382812249074 trend=decrease
softx_lower_proxy: during=-0.0015926361083454 delta_before=-0.0204181671146791 trend=decrease
softx_upper_proxy: during=-0.00213623046875 delta_before=-0.0119781494135881 trend=decrease
te_profile_gradient_proxy: during=None delta_before=None trend=na
ne_profile_gradient_proxy: during=None delta_before=None trend=na
density_proxy: during=2.0940137378342765e+19 delta_before=-1.1107786312890763e+20 trend=decrease
nbi_proxy: during=1554739.5 delta_before=6688.75 trend=decrease
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