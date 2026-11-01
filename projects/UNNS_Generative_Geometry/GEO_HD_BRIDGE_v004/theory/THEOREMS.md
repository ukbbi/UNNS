# Theorem register — GEO_HD_BRIDGE_v004 (A4-T1 … A4-T7)

Status: **PROVED**, **PROVED-SCOPED**, **FINITE-EXACT**, **COUNTEREXAMPLE**, **OPEN**, **NOT-TESTED**. Verifier shards Z1–Z8 (new) vs Z0 (integrity). C3 NOT claimed; novelty NOT assessed; same author.

| id | statement | status | doc |
|---|---|---|---|
| A4-T1 | `D(x)={P}`, `D(y)={P,p_iq}`; `e_i−e_j` primitive at both, dormant at `x`, active at `y` (activation, not creation); `|Gr(x)|=k(k−1)+2` | **PROVED** (+11 instances, 51 more k=2) | INFINITE_FAMILIES |
| A4-T2 | `K_move(y)=K_{k+1}`, no 2-cells, `β₁=k(k−1)/2`; `K_axis(y)` discrete; `K_move(x)=pt`; B4-1: `β₁=1` | **PROVED**; `|Gr(y)|=(k+1)(k+2)` **FINITE-EXACT** (k=2..5) | INFINITE_FAMILIES |
| A4-T3a | Lemma M: `D(x)⊆D(C(x))`; every activation/creation is a D-event | **PROVED** | DYNAMIC_ACTIVATION |
| A4-T3b | Progression lemma; necessary conditions T3-N and the blocking criterion | **PROVED** | DYNAMIC_ACTIVATION |
| A4-T3c | Some members of the A4 family are joined by actual FIELD-I orbits (`3025/3→12100/3`, 8 steps; k=3 ℓ=7: 375 steps, `β₁ 0→3`); table: 40 REACHED / 929 BLOCKED / 24 UNRESOLVED / 0 OVERSHOT of 993 | **FINITE-EXACT** | DYNAMIC_ACTIVATION |
| A4-T3d | Step-level activation without excursion (ℓ=5 tower 5→6; ℓ=29 23→24) | **FINITE-EXACT** | DYNAMIC_ACTIVATION |
| A4-T3e | "q²>ℓ ⇒ y unreachable" (initial conjecture) | **COUNTEREXAMPLE** (ℓ=3,q=2) | DYNAMIC_ACTIVATION |
| A4-T3f | Infinitely many reached members; "not blocked ⇒ reached"; closed form of first event | **OPEN** | OPEN_PROBLEMS |
| A4-T4a | Persistence: `E_g` is monotone along orbits (activity interval `[n_g,∞)`) | **PROVED** (Lemma M) | PRIMITIVE_RELATIONS |
| A4-T4b | Primitivity (`g∈Gr`) and move edges / `K_move` topology are **not** persistent: excursion of `e_5−e_{11}`; `β₁` drops at 57 of 474 scan events; integer collapse | **COUNTEREXAMPLE** (finite-exact witnesses) | MOVE_TOPOLOGY |
| A4-T4c | Activation does not necessarily change Betti numbers: 80 of 474 step-activation events (ℓ=5,7,11,13; 382 orbits) leave the Betti vector unchanged; first: ℓ=5, S=36, step 3→4 | **COUNTEREXAMPLE** to "activation ⇒ topology change" (general); holds in the A4 family and the ℓ=5/29 events listed | MOVE_TOPOLOGY |
| A4-T5 | G=11: `|F_k|=2k+7` (period-5 slice structure from `ord_11(3)=5`); `β₁=8`, `β₂=17` stable, `β₃` period-5 growth `(0,3,1,1,4)` | `|F_k|` **PROVED**; Betti laws **FINITE-EXACT** k≤45, **not extrapolated** | COLLECTIVE_TOWERS |
| A4-T6 | G=5: `(1,6,5,0)` for 7≤k≤45 vs G=11 unbounded-looking `β₃`; scaling laws fix `D` (hence realised complex) but not dormancy or Betti pattern; ℓ=29 stays finite-exact | **FINITE-EXACT** | COLLECTIVE_TOWERS |
| A4-T7 | Obstruction: `K_move` of integer endpoints is contractible, histories there have 2–3 components; no identification; no map claimed | **PROVED** (obstruction); connection **OPEN** | HISTORY_CONNECTION |

Corrections: none to earlier releases in this one. The v004 spec's "(G=35)" wording is corrected to ℓ=29, G=29, `(P,ρ²)=(35,900)` (SOURCE_CROSSWALK).
