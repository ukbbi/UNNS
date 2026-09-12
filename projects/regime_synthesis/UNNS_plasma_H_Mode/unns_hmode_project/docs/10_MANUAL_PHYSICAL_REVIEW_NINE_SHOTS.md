# TCV Manual Physical Review — Nine Recurrent Suspect Shots

## Purpose

This report performs the manual physical review requested after the fragment-isolate and suspect-shot mapping stages. It does not run another chamber. It compares the nine recurrent suspect TCV shots against their mapped branch variables, with shot 69807 used as the primary reference case.

Reviewed shots: `69807`, `68001`, `69668`, `69892`, `66445`, `68719`, `69913`, `67992`, `68206`.

## Executive conclusion

The nine shots do not form one anomaly class. They separate into at least four provisional physical corridors:

- **A. Low-density non-LH transport/timing corridor:** 69807, 69668
- **B. High-power power-balance/transport corridor:** 68001, 67992, 68206
- **C. Edge-divertor response corridor:** 69892, 66445, 68719
- **D. Timing-only low-power comparator:** 69913

Shot `69807` is the primary mixed case. It combines power-loss, auxiliary/total-power, transport, and timing fragmentation while remaining low-density and low-divertor. It should be treated as the first candidate failed or non-admissible boundary-route case, not simply as a high-power case.

## Focused manual review table

|   SHOT | ILH pattern   | Times       | Branch label                                          |   Fragment count | Fragment tags                                       |   P_LH |   P_total | P_loss   |   n_e | chi_eff   |   divertor |
|-------:|:--------------|:------------|:------------------------------------------------------|-----------------:|:----------------------------------------------------|-------:|----------:|:---------|------:|:----------|-----------:|
|  69807 | 0;0           | 1.470;1.940 | Primary mixed non-LH transport/timing branch          |                5 | power_balance_branch;transport_branch;timing_branch |  0.218 |     0.951 | 0.778    | 0.267 | 2.619     |      0.019 |
|  68001 | 1;0           | 1.159;2.030 | High-power power-balance + transport branch           |                4 | power_balance_branch;transport_branch               |  0.345 |     1.11  | 0.869    | 0.507 | 2.233     |      0.089 |
|  69668 | 0             | 1.580       | Low-density non-LH transport/timing branch            |                4 | transport_branch;timing_branch                      |  0.216 |     0.744 | 0.779    | 0.266 | 3.042     |      0.019 |
|  69892 | 1;1           | 1.206;1.838 | Edge-divertor response branch                         |                4 | edge_divertor_response_branch                       |  0.374 |     0.964 | 0.719    | 0.566 | 1.624     |      0.089 |
|  66445 | 1;1           | 1.071;1.948 | Edge-divertor response branch with rising edge signal |                4 | edge_divertor_response_branch                       |  0.381 |     0.913 | 0.595    | 0.571 | 1.376     |      0.095 |
|  68719 | 1             | 1.669       | High-density edge-divertor response branch            |                4 | edge_divertor_response_branch                       |  0.477 |     0.671 | —        | 0.798 | —         |      0.139 |
|  69913 | 1             | 1.394       | Timing-only low-power branch                          |                4 | timing_branch                                       |  0.272 |     0.575 | 0.393    | 0.362 | 0.930     |      0.014 |
|  67992 | 1;1           | 1.112;1.930 | Power-balance + transport L-H branch                  |                3 | power_balance_branch;transport_branch               |  0.34  |     1.016 | 0.802    | 0.494 | 2.088     |      0.074 |
|  68206 | 1;1           | 1.004;1.910 | Power-balance branch with density rise                |                3 | power_balance_branch                                |  0.42  |     0.923 | 0.739    | 0.672 | 1.765     |      0.051 |

## Shot-by-shot physical reading

### Shot 69807 — Primary mixed non-LH transport/timing branch

**Priority:** 1 — inspect first

**Mapped branch tags:** `power_balance_branch;transport_branch;timing_branch`

**Fragment variables:** `P_loss_candidate_MW;P_total_aux_candidate_MW;chi_eff_candidate;event_time`

**Physical reading:** Low-density, low-divertor, high-transport case with high/isolated power-loss structure and two non-LH-labelled event rows. Treat as the first candidate failed or non-admissible boundary-route case.

|   SHOT |   TIME |   ILH |     P_LH |   P_total |    P_aux |   P_loss |       dWdt |    Wmhd |      n_e |    H_frac |   He_frac | Z_eff   |   chi_eff |   divertor |    div150 |
|-------:|-------:|------:|---------:|----------:|---------:|---------:|-----------:|--------:|---------:|----------:|----------:|:--------|----------:|-----------:|----------:|
|  69807 |   1.47 |     0 | 0.194588 |  1.05305  | 0.973893 | 0.997083 | -0.0494718 | 8017.44 | 0.224684 | 0.0822496 | 0.024939  | 2.10393 |   3.8157  |  0.0172096 | 0.0157488 |
|  69807 |   1.94 |     0 | 0.24162  |  0.848582 | 0.505917 | 0.558489 | -0.113241  | 9450.47 | 0.310051 | 0.135691  | 0.0249829 | —       |   1.42298 |  0.0201702 | 0.0248279 |

### Shot 68001 — High-power power-balance + transport branch

**Priority:** 2 — compare against 69807

**Mapped branch tags:** `power_balance_branch;transport_branch`

**Fragment variables:** `P_loss_candidate_MW;P_total_aux_candidate_MW;P_total_candidate_MW;chi_eff_candidate`

**Physical reading:** Two-row mixed ILH sequence with high total/loss/aux power, high hydrogen fraction, elevated helium candidate fraction, high transport candidate, and strong divertor signal. Best comparator for 69807 because it shares power/transport fragmentation but has a stronger power and edge-response footprint.

|   SHOT |   TIME |   ILH |     P_LH |   P_total |    P_aux |   P_loss |        dWdt |     Wmhd |      n_e |   H_frac |   He_frac |   Z_eff |   chi_eff |   divertor |    div150 |
|-------:|-------:|------:|---------:|----------:|---------:|---------:|------------:|---------:|---------:|---------:|----------:|--------:|----------:|-----------:|----------:|
|  68001 |  1.159 |     1 | 0.323622 |   1.02284 | 0.845229 | 0.711975 |  0.106951   | 10699.3  | 0.460684 | 0.835884 | 0.0831187 | 1.09799 |   1.76094 |  0.0571379 | 0.0653681 |
|  68001 |  2.03  |     0 | 0.367051 |   1.19638 | 1.02453  | 1.02553  | -0.00107684 |  9443.89 | 0.552914 | 0.845881 | 0.130425  | 2.26091 |   2.70605 |  0.120512  | 0.0831536 |

### Shot 69668 — Low-density non-LH transport/timing branch

**Priority:** 3 — compare against 69807

**Mapped branch tags:** `transport_branch;timing_branch`

**Fragment variables:** `chi_eff_candidate;event_time`

**Physical reading:** Single non-LH-labelled row with low density, low threshold power, low divertor signal, and the highest transport candidate among the reviewed shots. It looks like the closest low-density sibling of 69807, but with less explicit power-balance branching.

|   SHOT |   TIME |   ILH |     P_LH |   P_total |    P_aux |   P_loss |       dWdt |    Wmhd |      n_e |   H_frac |   He_frac |   Z_eff |   chi_eff |   divertor |    div150 |
|-------:|-------:|------:|---------:|----------:|---------:|---------:|-----------:|--------:|---------:|---------:|----------:|--------:|----------:|-----------:|----------:|
|  69668 |   1.58 |     0 | 0.216071 |  0.744312 | 0.758676 | 0.779358 | -0.0180014 | 7722.32 | 0.265899 | 0.086754 | 0.0251548 |  2.2249 |   3.04184 |  0.0187466 | 0.0160032 |

### Shot 69892 — Edge-divertor response branch

**Priority:** 4 — edge/divertor trio

**Mapped branch tags:** `edge_divertor_response_branch`

**Fragment variables:** `divertor_signal_candidate`

**Physical reading:** Two L-H-labelled rows with high density, high hydrogen fraction, moderate threshold power, strong divertor signal, and no transport/power-balance tag. Edge response dominates the branch identity.

|   SHOT |   TIME |   ILH |     P_LH |   P_total | P_aux    | P_loss   |      dWdt |    Wmhd |      n_e |   H_frac |   He_frac |   Z_eff | chi_eff   |   divertor |    div150 |
|-------:|-------:|------:|---------:|----------:|:---------|:---------|----------:|--------:|---------:|---------:|----------:|--------:|:----------|-----------:|----------:|
|  69892 |  1.206 |     1 | 0.363635 |  0.908733 | 0.841285 | 0.719128 | 0.0766229 | 11359.2 | 0.544661 | 0.857687 | 0.0381354 | 1.08267 | 1.62383   |  0.0708555 | 0.0730177 |
|  69892 |  1.838 |     1 | 0.383413 |  1.01859  | —        | —        | 0.0804653 | 10414.9 | 0.586542 | 0.84589  | 0.0423971 | 1.0502  | —         |  0.108055  | 0.106451  |

### Shot 66445 — Edge-divertor response branch with rising edge signal

**Priority:** 4 — edge/divertor trio

**Mapped branch tags:** `edge_divertor_response_branch`

**Fragment variables:** `divertor_signal_candidate`

**Physical reading:** Two L-H-labelled rows with low plasma current, rising total/loss power, rising chi_eff, and strong growth of divertor signal between early and late rows. It is the clearest within-shot edge-response escalation case.

|   SHOT |   TIME |   ILH |     P_LH |   P_total |    P_aux |   P_loss |      dWdt |    Wmhd |      n_e |    H_frac |   He_frac |   Z_eff |   chi_eff |   divertor |    div150 |
|-------:|-------:|------:|---------:|----------:|---------:|---------:|----------:|--------:|---------:|----------:|----------:|--------:|----------:|-----------:|----------:|
|  66445 |  1.071 |     1 | 0.368372 |  0.788706 | 0.591758 | 0.481361 | 0.0815647 | 11707.8 | 0.537958 | 0.0732694 | 0.0251236 | 1.30044 |   1.11768 |  0.0564635 | 0.0740528 |
|  66445 |  1.948 |     1 | 0.394563 |  1.03754  | 0.755786 | 0.707908 | 0.088329  | 10893.4 | 0.604976 | 0.164718  | 0.0252161 | 1.1584  |   1.63501 |  0.132688  | 0.140521  |

### Shot 68719 — High-density edge-divertor response branch

**Priority:** 4 — edge/divertor trio

**Mapped branch tags:** `edge_divertor_response_branch`

**Fragment variables:** `divertor_signal_candidate`

**Physical reading:** Single L-H-labelled row with the highest density group, high P_LH, strong Wmhd, strong divertor signal, and missing/undefined loss-power and chi_eff fields. It may represent an edge-response branch where the power/transport columns are incomplete rather than absent physically.

|   SHOT |   TIME |   ILH |    P_LH |   P_total | P_aux   | P_loss   |      dWdt |    Wmhd |      n_e |    H_frac |   He_frac | Z_eff   | chi_eff   |   divertor |   div150 |
|-------:|-------:|------:|--------:|----------:|:--------|:---------|----------:|--------:|---------:|----------:|----------:|:--------|:----------|-----------:|---------:|
|  68719 |  1.669 |     1 | 0.47704 |  0.671406 | —       | —        | 0.0729057 | 13769.1 | 0.797745 | 0.0892929 | 0.0254265 | —       | —         |   0.138759 | 0.140701 |

### Shot 69913 — Timing-only low-power branch

**Priority:** 5 — secondary timing comparator

**Mapped branch tags:** `timing_branch`

**Fragment variables:** `event_time`

**Physical reading:** Single L-H-labelled timing branch with low total/loss power, low transport candidate, and very low divertor signal. It behaves like a clean timing isolate rather than a power/transport or edge-response branch.

|   SHOT |   TIME |   ILH |     P_LH |   P_total |    P_aux |   P_loss |      dWdt |    Wmhd |      n_e |   H_frac |   He_frac |   Z_eff |   chi_eff |   divertor |    div150 |
|-------:|-------:|------:|---------:|----------:|---------:|---------:|----------:|--------:|---------:|---------:|----------:|--------:|----------:|-----------:|----------:|
|  69913 |  1.394 |     1 | 0.272318 |  0.575489 | 0.402203 | 0.392938 | 0.0425415 | 11400.6 | 0.362429 | 0.326592 | 0.0250545 |   1.438 |  0.930461 |  0.0142754 | 0.0157633 |

### Shot 67992 — Power-balance + transport L-H branch

**Priority:** 5 — secondary power/transport comparator

**Mapped branch tags:** `power_balance_branch;transport_branch`

**Fragment variables:** `P_loss_candidate_MW;chi_eff_candidate`

**Physical reading:** Two L-H-labelled rows with high hydrogen fraction, high loss/total power, and elevated chi_eff. This is the cleaner L-H analogue of the power/transport axis represented more ambiguously by 68001.

|   SHOT |   TIME |   ILH |     P_LH |   P_total |    P_aux |   P_loss |      dWdt |     Wmhd |      n_e |   H_frac |   He_frac |   Z_eff |   chi_eff |   divertor |    div150 |
|-------:|-------:|------:|---------:|----------:|---------:|---------:|----------:|---------:|---------:|---------:|----------:|--------:|----------:|-----------:|----------:|
|  67992 |  1.112 |     1 | 0.317045 |  0.948576 | 0.795193 | 0.722753 | 0.107399  | 10352.1  | 0.447228 | 0.846003 | 0.0253785 | 1.12886 |   1.80657 |  0.0526643 | 0.0597902 |
|  67992 |  1.93  |     1 | 0.362408 |  1.08364  | 0.893152 | 0.881387 | 0.0766436 |  9834.43 | 0.540703 | 0.830766 | 0.0255531 | 1.01344 |   2.37008 |  0.095552  | 0.10417   |

### Shot 68206 — Power-balance branch with density rise

**Priority:** 5 — secondary power comparator

**Mapped branch tags:** `power_balance_branch`

**Fragment variables:** `P_loss_candidate_MW`

**Physical reading:** Two L-H-labelled rows with large density increase and a strong late rise in P_LH/loss power, but without the transport tag. It is the purest power-balance comparator in the suspect set.

|   SHOT |   TIME |   ILH |     P_LH |   P_total |    P_aux |   P_loss |      dWdt |    Wmhd |      n_e |   H_frac |   He_frac |   Z_eff |   chi_eff |   divertor |    div150 |
|-------:|-------:|------:|---------:|----------:|---------:|---------:|----------:|--------:|---------:|---------:|----------:|--------:|----------:|-----------:|----------:|
|  68206 |  1.004 |     1 | 0.35539  |   0.76747 | 0.632966 | 0.557808 | 0.0815143 | 12112.6 | 0.526831 | 0.604945 | 0.0714791 | 1.48827 |   1.44885 |  0.0254958 | 0.0240465 |
|  68206 |  1.91  |     1 | 0.485376 |   1.07872 | 0.95009  | 0.920651 | 0.0463091 | 13659.4 | 0.817966 | 0.597616 | 0.0715562 | 1.52528 |   2.0817  |  0.0766526 | 0.0712935 |

## Required comparisons

### 1. 69807 versus 68001

Both shots participate in power-balance and transport fragmentation, but they are not the same branch. `69807` is low-density, low-divertor, and ILH=0 in both rows; its strongest signal is a mixed power-loss/transport/timing branch. `68001` is higher-density, high-power, high-divertor, and mixed ILH=1/0 across its two rows. This makes `68001` a high-power transition/departure comparator, while `69807` looks closer to a low-density non-LH boundary-route failure or aborted-access case.

### 2. 69807 versus 69668

These two are the closest low-density pair. Both are ILH=0 and have low divertor signal with high transport candidate values. `69668` has the highest chi_eff_candidate in the reviewed set and a single timing/transport branch; `69807` has a broader mixed signature involving power-loss and event-time fragmentation. This suggests that `69668` may be the clean transport/timing isolate, while `69807` is the more complex version where power-balance also enters.

### 3. 69892 / 66445 / 68719 edge-divertor trio

The trio is distinct from the 69807/69668 low-divertor branch. All three are L-H-labelled in the available canonical rows, and their common branch identity is `divertor_signal_candidate`. `66445` shows a strong within-shot rise in divertor signal and chi_eff between its early and late rows. `69892` has high hydrogen fraction, moderate-to-high density, and a strong divertor signal. `68719` is high-density with strong divertor response but missing power-loss/chi_eff values. As a group, they look like an edge-response corridor rather than a transport-loss corridor.

### 4. Secondary comparators

`69913` is timing-only, low-power, low-transport, and low-divertor. It is useful as a clean timing comparator. `67992` is a clean L-H power-balance/transport comparator, while `68206` is a power-balance case with a notable density and P_LH rise but no transport tag. These should be used to prevent over-interpreting `69807` as simply a power case.

## Provisional transition-family taxonomy

| Family | Candidate shots | Defining signature | UNNS reading |
|---|---|---|---|
| Low-density non-LH transport/timing | 69807, 69668 | ILH=0, low density, low divertor, high chi_eff/timing branch | leakage/failed boundary-route corridor |
| High-power power-balance/transport | 68001, 67992, partly 68206 | high total/loss power and transport/power tags | power-loaded access corridor |
| Edge-divertor response | 69892, 66445, 68719 | divertor_signal_candidate branch, L-H-labelled rows | boundary-response corridor |
| Timing-only low-power | 69913 | event_time branch, low power, low chi_eff, low divertor | timing corridor / clean comparator |

## Implication for the H-mode origin question

The manual review strengthens the interpretation that H-mode access is not one scalar total-power threshold. The suspect shots separate according to which physical channel carries the branch: power balance, transport, edge/divertor response, or timing. In UNNS terms, this supports the hypothesis that H-mode is a boundary-admissibility transition with multiple access corridors. Total power contributes, but the decisive structure appears to involve how power, transport, edge response, and timing become route-preserving or fail to do so.

## What not to claim yet

- Do not claim that these shots are faulty or anomalous. They are structurally recurrent branch candidates.
- Do not claim that `69807` proves failed H-mode. It is a candidate low-density, low-divertor, non-LH mixed branch requiring source-notebook review.
- Do not claim physical causality yet. This is a mapped, data-driven taxonomy of candidate transition families.

## Recommended next step

Create a small comparison panel or notebook section focused on the four corridors above. The first manual target should be `69807` versus `69668`, because this isolates the low-density non-LH transport/timing corridor. The second target should be `69807` versus `68001`, because that separates the failed/low-density route from the high-power power/transport route. The third target should be the edge-divertor trio `69892 / 66445 / 68719`, because that likely represents a different physical branch rather than a variant of the 69807 branch.