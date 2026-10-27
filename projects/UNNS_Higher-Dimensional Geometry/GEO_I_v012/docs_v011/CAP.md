# GEO-I v011 — Programme A: the cap (partial result; the universal cap theorem remains OPEN)

**Setting (frozen).** `Γ = {(i,j): j ≡ s i (mod d)}`, `t = s⁻¹`, `d ≥ 5`, `2 ≤ s ≤ d−2`, `gcd(s,d)=1`. Small box `Q = (d+u, d+v)`, `0 ≤ u,v < d`, `(u,v) ≠ (0,0)`; `F_Q = Γ ∩ [0,Q]∖0`, `H_Q = conv F_Q`, cap `C_Q = H_Q ∖ H_0`, `U_Q` = union of cells `P(w;g,h)` (Graver `g,h`, all corners in `F_Q`) and Graver segments. By G10-R1, `H_0 ⊆ U_Q`. **Target G11-C1/T1:** `C_Q ⊆ U_Q`. Consequence G11-T2: complete planar stabilization `U = H` (needs only G11-C1).

## 1. Result of this release (honest summary)
| Statement | Status |
|---|---|
| G11-C1/T1 universal cap, G11-T2 stabilization | **OPEN** |
| G11-L3 one-sided cap (`v=0`, `1≤u<d`; `u=0` by transposition) — explicit cell family | **CHECKED** (exact, 39,590 triples `d≤60`; 544 independent certificates `d≤16`) |
| G11-A arithmetic lemma behind the bottom cell | **CHECKED** (657,526 triples `d≤150`), no proof |
| G11-L4 mixed corner pentagon | **CHECKED**, non-degenerate boxes only (345 boxes, `d≤15`) |
| G11-L2 cap-cell generation for mixed boxes | **OPEN** |
| G11-R1 re-run of G10-T2 with an independent engine | **CHECKED** (686 boxes `d≤9`; inherited record `d≤22`) |

A failed proof is not a falsification: nothing here refutes the cap; the evidence (inherited record `d≤22`, 26,636 boxes at `d≤20` in v008, plus the above) is uniformly positive.

## 2. The one-sided cap (`Q = (d+u, d)`, `1 ≤ u < d`)
**2.1 Geometry.** Let `W_u = conv({(0,0),(0,d)} ∪ {(i, s i mod d): 1 ≤ i ≤ u})`. Then `H_Q = H_0 ∪ K` with `K = W_u + (d,0)` (the cap) and disjoint interiors (checked exactly as an area identity in every CAPCOVER certificate). `M = (x_m, y_m)` is the record minimum of `a_i = s i mod d` over `i ≤ u` (the first Γ-point after the origin on `∂W_u`, counter-clockwise); `M` is Pareto-minimal, hence Graver.
**2.2 The cell family.** Let `w_0 = M, w_1, …, w_r = A=(0,d)` be the Γ-points of `∂W_u` from `M` to `A` (counter-clockwise).
* *Sweep cells* `P(w_i; w_{i+1} − w_i, (d,0))` (corner set `{w_i, w_{i+1}, w_i+(d,0), w_{i+1}+(d,0)}`): all corners lie in `F_Q` (`x ≤ u+d`, translation by `(d,0)` is a Graver symmetry); the steps are Graver (verified by scan in every instance; the expected reason is the reflection lemma of G10-Z). Their union contains every row `y ∈ [y_m, d]` of `K`: on that row `K = [x_left+d, x_right+d]` with `x_left = 0` and `x_right ≤ u < d`, while the sweep of the right boundary point covers `[x_right, x_right + d] ⊇ [d, x_right + d]`.
* *Bottom cell.* Rows `y < y_m` of `K` form the triangle `B + conv{0, M, (0,y_m)}`. Take `g ∈ {g_1 = (1, s−d), u* = (d−t, −1)}` (both Graver, the first/last lower-left hull steps of `H_0`, G10-Z) and the cell with corners `p = B−g, B, p+M, B+M` — all in `F_Q` since `p ∈ {P_{d−1}, P_t}` and `M_x ≤ u`. Writing `(0,y_m) = −a g + b M` one finds `a = x_m y_m / cr`, `b = y_m g_x / cr` with `cr = g_x y_m − g_y x_m` (a multiple of `d`); `b ≤ 1` holds automatically for both choices, so the triangle lies in the cell iff **`cr(g,M) ≥ x_m y_m`**.
**2.3 Lemma G11-A (CHECKED, not proved).** `max( y_m + x_m(d−s), (d−t) y_m + x_m ) ≥ x_m y_m` for every `d, s, u`. Exhaustively true for `d ≤ 150` (657,526 triples). Partial results obtained: failure of both inequalities forces `d−t < x_m ≤ t` and `d−s < y_m < s`; no contradiction was derived. If G11-A is proved, G11-L3 becomes PROVED (given the Graver property of the boundary steps).
**2.4 A route that does not work.** The single cell `P(P_t; u*, M)` does **not** contain the bottom triangle in many boxes (numerical tests); the two-option lemma above replaced it.
**2.5 Verification.** `theory/cap_cells.py::verify` constructs the cells and checks (i) corners in `F_Q`, (ii) both generators Graver (box scan), (iii) independence, (iv) exact rational cover of `K`, (v) `area(H_Q) = area(H_0) + area(K)`. 39,590 triples `d ≤ 60`, 0 failures. The same checks are re-run by the standalone `certificates/checker11.py` on `C10_capcover.json` (544 boxes, `d ≤ 16`).

## 3. The mixed case (`u, v ≥ 1`)
Strategy (not completed): `H_Q = H_0 ∪ S_R ∪ S_T`, `S_R = H_Q ∩ {x ≥ d}` covered by horizontal sweeps from the first hull vertex after `B` up to the last hull vertex `E` with `x ≥ d`; `S_T` by transposition; leftover = the *corner region* near `C = (d,d)` bounded by the bridging hull edge `[E, E']` and the top triangle above the last sweep vertex. For the non-degenerate corner pentagon `(E,(d,E_y),C,(E'_x,d),E')` (`E_y<d`, `E'_x<d`) the union of all cells covers it in all 345 boxes with `d ≤ 15`; the other 4,681 mixed boxes (`E_y ≥ d` or `E'_x ≥ d`) were not analysed separately, and no uniform cell family for the corner was found. **G11-L2 and G11-C1 stay OPEN.**

## 4. What would close the cap
(1) Prove G11-A (elementary lattice statement about the Pareto chain of `Γ`); (2) prove the Graver property of the boundary steps of `W_u` (reflection lemma); (3) a uniform cell family for the corner pentagon and the top triangle; then G11-T1 and G11-T2 follow.
