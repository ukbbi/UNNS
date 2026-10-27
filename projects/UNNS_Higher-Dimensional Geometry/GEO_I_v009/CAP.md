# GEO-I v009 — Programme B: small-box cap coverage (G9-CAP / G9-T2)

**Status: OPEN (B-OPEN).** The cap statement is stated independently of G9-T1. No proof was obtained and no counterexample exists in the completed survey.

## 1. Statement
For `d ≥ 3`, every unit `s`, every nonexceptional small box `Q = (d+u, d+v)`, `0 ≤ u,v < d`, `(u,v) ≠ (0,0)`: `C_Q := H_Q \ H_0 ⊆ U_Q`, where `H_Q = conv F_Q`, `H_0 = conv F_{(d,d)}`.

## 2. Frozen ingredients (v008)
* G8-T1: the two hollow-box triangles lie in every enlarged `U_Q` (explicit Graver parallelograms `R1`, `R2` and their transposes).
* G8-S: for `u,v ≥ 1`, the box is squareless (no cell with a corner at `(d,d)` on both sides) iff `v < m_s(u)`, `m_s(u) = min_{1≤i≤u}(s·i mod d)`; `N_sq = 2(d−1) + Σ(m_s(u)−1)` counts squareless boxes.
* Extension points over the square: `R_i = (d+i, a_i)`, `T_j = (c_j, d+j)` (`c_j = t·j mod d`) and `K = (d,d) + Γ ∩ [1,u]×[1,v]` (empty iff squareless).
* G8-R1: conditional on G9-C1, `H_0 ⊆ U_Q`.

## 3. Proof programme B1–B5 — what was and was not obtained
B1 (cap boundary, one-sided and asymmetric enlargements) and B2 (squareless cap via the staircase) rest on the v008 ingredients above. A uniform local-to-global proof (B3–B5: the non-squareless case, corner compatibility of horizontal and vertical enlargement, uniformity in `(d,s,u,v)`) was **not** obtained. Reason: for the cap, the covering cells are not those near `(d,d)` alone; the cap is covered by cells whose corners are the new extension points *and* old points of `F`, and the required corner compatibility involves the whole record-minimum chain `m_s`, i.e. the same continued-fraction data as G9-C1. A proof of the cap that avoids any statement about the old square is therefore expected to be as hard as G9-C1; none is claimed.

## 4. Adversarial verification (CHECKED within scope — not a proof)
| Survey | scope | result |
|---|---|---|
| v008 `small_attack` | `d = 3..14` (6,586 boxes), `d = 15..20` (20,050 boxes), all units | every box: `H_Q ⊆ U_Q` (exact) |
| v009 `cap_attack` (`experiments/cap_attack.py`) | `d = 21..22`, all units, all `d²−1` boxes (`10,110` boxes) | all boxes covered, 0 cap failures |

Since `H_Q ⊆ U_Q` implies the cap statement, every covered box confirms G9-CAP. The script also tests the cap statement separately (uncovered area outside `H_0`) so that a failure of the full coverage that is confined to `H_0` would be reported as such. The squareless boxes are included (their count equals the G8-S formula in each `(d,s)`).

## 5. Labels
*Counterexample found:* none. *No counterexample within completed scope:* above. *Search incomplete:* all `d` beyond the ranges. *General theorem proved:* no.
