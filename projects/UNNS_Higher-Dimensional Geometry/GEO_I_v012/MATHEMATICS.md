# GEO-I v012 — Mathematics: universal planar cap closure

Status words: PROVED, PROVED+CHECKED, CHECKED, FALSE, CORRECTED, OPEN, UNAVAILABLE. A finite computation is never called a proof; every theorem below carries a proof, and the machine checks are listed as support only.

## 0. Setting and notation

`d >= 2`, `s` a unit mod `d`, `t = s^-1`. `Gamma = {(i,j) in Z^2 : j = s i (mod d)}`, index `d` in `Z^2`.
For a box `Q = (Q1,Q2)`: `F_Q = Gamma ∩ [0,Q1]x[0,Q2] \ {0}`, `H_Q = conv F_Q`, `H_0 = H_(d,d)`.
`g in Gamma\{0}` is **Graver** if no `h in Gamma\{0,g}` is conformal to `g` (`h_i g_i >= 0`, `|h_i| <= |g_i|`).
A **cell** `P(w;g,h) = conv{w, w+g, w+h, w+g+h}` with `g,h` Graver and independent and all four corners in `F_Q`.
`U_Q` = union of all cells (and Graver segments) inside the box `Q`; `U_Q ⊆ H_Q`, and `U_Q` is monotone in `Q`.
Transposition `(i,j) -> (j,i)` maps `(Gamma_s, Q)` to `(Gamma_t, Q^T)` and preserves Graver vectors, cells and `U`.

Inherited (PROVED+CHECKED, frozen): **G5-C1** (`s = ±1`, all `d`: `U = H` for every box), **G7-T1** (`max(Q) >= 2d`: `U_Q = H_Q`), **G10-R1** (`H_0 ⊆ U_Q` for `Q >= (d,d)`, `Q != (d,d)`).

Remaining case after these: `d >= 5`, `2 <= s <= d-2`, and a *small box* `Q = (d+u, d+v)`, `0 <= u,v < d`, `(u,v) != (0,0)`. (For `d <= 4` every unit is `±1`.) Put `a = d-s`, `c = d-t`; `a,c in [2,d-2]`, and `ac = 1 (mod d)`.
`Gamma = {(i,j): j + a i = 0 (mod d)} = {(i,j): i + c j = 0 (mod d)}`.

## 1. G12-T1 — arithmetic strip inequality (G11-A)  [PROVED+CHECKED]

**Theorem.** Let `M = (x,y) in Gamma` with `0 < x,y < d` and `Gamma ∩ [0,x]x[0,y] = {0, M}` (Pareto-minimal). Then
`max( y + (d-s) x , x + (d-t) y ) >= x y.`

*Proof.* Write `D1 = y + a x`, `D2 = x + c y`; both are multiples of `d` (membership in `Gamma`); put `b = D1/d`, `b' = D2/d`, positive integers. Suppose `D1 < xy` and `D2 < xy`.

*Step 1: `y > a` and `x > c`.* `y + a x < x y` gives `y(x-1) > a x`; `x = 1` is impossible, so `y > a x/(x-1) > a`. Symmetrically `x > c`.

*Step 2: `b = 1`.* Suppose `b >= 2`. Take `r = ceil((d-y)/a)`. Because `y > a` the interval `[(d-y)/a, d/a]` has length `y/a > 1`, so `r <= d/a`; and `r >= 1`. Put `R = (x - r, (b-1)d - a(x-r))`. Then `R in Gamma` (its coordinates satisfy `j + a i = (b-1)d`). Using `b d = y + a x`: `R_y = y - d + a r`, so `R_y >= 0` (as `r >= (d-y)/a`) and `R_y <= y` (as `a r <= d`). Also `R_x = x - r >= 0` because `(d-y)/a < x` (this is `d < y + a x = b d`, true for `b >= 2`) and `x` is an integer. Hence `R in [0,x]x[0,y]`, `R != M` (`r >= 1`), `R != 0` (`R_y = 0 = R_x` would force `(b-1)d = 0`). This contradicts Pareto-minimality. So `b = 1`: `y + a x = d`. By the transposed argument (swap `x<->y`, `a<->c`) `b' = 1`: `x + c y = d`.

*Step 3.* Now `y = d - a x` and `x = d - c y`, so `x = d - c d + a c x`, i.e. `x (a c - 1) = d (c - 1)`. Since `ac = 1 (mod d)` and `ac >= 4`, `ac - 1 = m d` with `m >= 1`, hence `m x = c - 1` and `x <= c - 1`, contradicting `x > c`. ∎

Used where: `M` is the first boundary step from `B` (a record minimum, hence Pareto-minimal, G12-L5) and, transposed, the last step into `A`. Support: every Pareto-minimal point for `5 <= d <= 60` (6,022 points, tests) and 984 ARITH certificates (every unit pair, `d = 5..60`, checker12 verifies the inequality, the record property and Pareto-minimality for every `u`).

## 2. G12-T2 — uniform strip-boundary Graver theorem  [PROVED+CHECKED]

**Theorem (reflection lemma).** Let `w, w2` be consecutive Gamma-points on the boundary of `H_Q` (all Gamma-points of the boundary are listed, collinear ones included) and `(w,w2) != (B,A)`. Then `e = w2 - w` is Graver.

*Proof.* Let `h in Gamma\{0,e}` be conformal to `e`. Then `w + h` lies in the axis-parallel rectangle spanned by `w,w2`, hence in the box; it is non-zero unless `0 in {corner of that rectangle}`, which forces `(w,w2) = (B,A)` (`w = (d,0)`, `w2 = (0,d)`). The same holds for `w2 - h`. The two points `w + h` and `w2 - h` are symmetric about the midpoint of `[w,w2]`, so they lie on opposite closed sides of the line `ℓ = w w2`. `ℓ` supports `H_Q` and both points are in `F_Q`, so both lie on `ℓ`; hence `h` is parallel to `e`, `h = λe`, `0<λ<1`, and `w + h` is a Gamma-point of `ℓ` strictly between `w` and `w2`, contradicting consecutiveness. ∎

The pair `(B,A)` is never consecutive on `∂H_Q` for a box containing `(d,d)` (§4: `(d,d)` would lie strictly outside the supporting line `BA`).
Also `(d,0)` and `(0,d)` are Graver (a conformal vector `(i,0)` has `d | i`). The vectors `g1 = (1,s-d)` and `g2 = (d-t,-1)` are Graver: a conformal `(i,j)` has `i in {0,1}` (resp. `j in {0,-1}`); `i = 0` forces `d | j`, `|j| < d`; `i = 1` forces `j = s-d`. This closes the "unproved uniform Graver step" assumption of v011.

## 3. Structure of the boundary Omega

`B = (d,0)`, `A = (0,d)`, `C0 = (d,d)`, all in `F_Q`. **Omega** = ccw list of boundary Gamma-points of `H_Q` from `B` to `A`. Types: `R = {x>=d, y<d}`, `T = {x<d, y>=d}`, `C = {x>=d, y>=d}`, `N = {x<d, y<d}`.

**G12-L1 (lower-left chain).** For a lower-left edge `ℓ` of `H_0` with primitive direction `e = (e1,-|e2|)` put `φ(z) = (e1 z2 + |e2| z1)/d`; it is integer valued on Gamma and positive on the non-zero quadrant; `ℓ = {φ = k}` and `H_0 ⊆ {φ >= k}`, `k >= 1`. Let `q in F_Q`. Subtract `(d,0)` if `q1 > d`, `(0,d)` if `q2 > d`, repeatedly; each step keeps `q` in `Gamma`, in the box, non-zero, and strictly lowers `φ` (both generators have `φ > 0`). The result `q'` is a non-zero Gamma-point of `[0,d]^2`, so `φ(q) >= φ(q') >= k`. Hence **all of `F_Q` lies on the far side of every lower-left edge line of `H_0`**, the lower-left chain of `H_0` is a boundary chain of `H_Q`, and
`H_Q ∩ [0,d]^2 = H_0`  (S1).
*Proof of equality:* `H_0 = [0,d]^2 ∩ ⋂{φ_ℓ >= k_ℓ}` (its upper right boundary is `B – C0 – A`), and `H_Q ⊆ ⋂{φ_ℓ >= k_ℓ}`; the reverse inclusion is `H_0 ⊆ H_Q`. ∎

**G12-L2 (no N-points).** Inside the open square the boundary of `H_Q` is the lower-left chain (S1), and that arc is the complement of Omega on `∂H_Q`. So every Omega point has `x>=d` or `y>=d` (S2).

**G12-L3 (flags).** `∂H_Q ∩ {x>=d}` is the arc cut off by the chord of the line `x = d` (which has `B` as lowest endpoint), so it is an *initial* segment of Omega; `∂H_Q ∩ {y>=d}` is cut off by the chord of `y = d` (left end `A`), a *final* segment (S3). So Omega ∈ `R* C* T*`, and the heights along the ascending right chain are non-decreasing.

**G12-L4 (no R→T step).** Suppose consecutive `w in R`, `w2 in T`: `w1 >= d > w2_1`, `w2_2 >= d > w_2`. Then `C0` lies strictly between them coordinate-wise. The point `ρ = w + w2 - C0` is in Gamma and (coordinate-wise `>= (w2_1, w_2)` and `< (w1, w2_2)`) in the box; it is non-zero unless `(w,w2) = (B,A)`. `ρ` is the reflection of `C0` in the midpoint of the edge: if `C0` is strictly inside the supporting line, `ρ` is strictly outside, impossible; if `C0` is on the line it is strictly between `w` and `w2` (it differs from both), contradicting consecutiveness. For `(B,A)`: `C0` would lie strictly beyond the supporting line `BA`. ∎ (S4)

Consequence (edge classes): an Omega edge `w->w2` is `R→R`, `R→C`, `C→C` (both `x>=d`: *L-eligible*), `C→C`, `C→T`, `T→T` (both `y>=d`: *D-eligible*). Nothing else occurs. `C→C` edges are both.

**G12-L5 (first and last step).** Let `u >= 1`, and `M = (x_M, y_M)` the minimum of `s i mod d` over `1<=i<=u`, attained at `i = x_M` (a strict record). Then Omega's first step is `B -> B + M` (S5).
*Proof.* Points of `F_Q` right of `B` are `(d+i, r_i)` or `(d+i, r_i + d)` with `r_i = s i mod d`; the others have polar angle `>= π/2` from `B`. The first edge has minimal polar angle, so it is the point minimising `r_i / i` (the `+d` points have larger slope). *Claim:* `y_M/x_M <= r_i/i` for all `i <= u`. For `i < x_M`, `r_i > y_M` (record) so the ratio is larger. If `i > x_M` and `r_i/i < y_M/x_M`, then `P' = (i - x_M, r_i - y_M)` is a Gamma point with positive coordinates `<d`, again of slope `< y_M/x_M`, and `i - x_M <= u`; iterating (descent in `i`) ends at some `i'' <= x_M`: `i'' = x_M` gives slope equal to `y_M/x_M`, and `i'' < x_M` gives a larger slope — both contradictions. Finally, no Gamma point lies strictly between `B` and `B+M` on the ray: it would be `B + (i,r_i)` with `i < x_M` and the same slope, impossible. ∎
`M` is Pareto-minimal in Gamma (record + `d`-periodicity) and `0 < x_M <= u < d`, `0 < y_M < d`; also `y_M <= s` (take `i = 1`). Transposed: for `v >= 1` the last step is `a1 -> A` with `a1 = A + (y', x')`, where `(x',y')` is the record minimum for `(d,t,Q^T)`; in particular `a1` has `x < d`: `a1 in T`.

## 4. Why (B,A) is not an Omega edge
`C0 in F_Q` lies on the *outer* side of the line `BA`, but `BA` would be a supporting line of `H_Q`. So Omega has at least one interior point.

## 5. G12-T3 / T4 / T5 / T6 / T7 — the cell family and the cover

**Cells.**
* *L-cells* `P(w; w2-w, (-d,0))` for each Omega edge `w->w2` with `w1,w2_1 >= d` **except the first edge** (`w != B`). Corners `w - (d,0)`, `w2 - (d,0)` are non-negative, non-zero, in the box, in Gamma. Generators Graver (§2).
* *D-cells* `P(w; w2-w, (0,-d))` for each edge with both `y >= d`, **except the last edge** (`w2 != A`).
* *Bottom cell* (only `u >= 1`): `P(B - g; g, M)` with `g in {g1, g2}` chosen by G12-T1 so that `cr(g,M) = g_x y_M - g_y x_M >= x_M y_M`. Corners: for `g1`: `(d-1, d-s)`, `(d-1+x_M, d-s+y_M)` (inside the box because `y_M <= s`); for `g2`: `(t,1)`, `(t+x_M, 1+y_M)` (inside because `y_M <= d-1`). `M` is Graver by §2.
* *Left cell* (only `v >= 1`): the transpose of the bottom cell for `(d,t,Q^T)`.

**Bottom cell contains the bottom triangle** `Δ = conv{B, B+M, (d,y_M)}`. Relative to `B`: `(0,y_M) = αM - βg` with `β = x_M y_M / cr(g,M) in (0,1]` and `α = g_x y_M/(g_x y_M - g_y x_M) in [0,1]`. ∎

**Theorem (G12-T3..T7).** For `d >= 5`, `2 <= s <= d-2`, `Q = (d+u,d+v) != (d,d)`, `0<=u,v<d`: `H_Q ⊆ U_Q`, hence `U_Q = H_Q`.

*Proof.* `U_Q` is a finite union of closed cells and segments, hence closed; `H_Q \ U_Q` is relatively open in `H_Q`; if it is non-empty it has positive area. So it suffices to cover `H_Q` up to a null set. `H_Q ∩ [0,d]^2 = H_0 ⊆ U_Q` (S1, G10-R1). Remaining: `z in H_Q` with `z1 > d` (Case 1) or `z2 > d` (Case 2); Case 2 is Case 1 for the transposed box (the cell family is transposition-symmetric: L↔D, bottom↔left), so only Case 1 is proved.

Let `z1 > d`. The horizontal ray to the right leaves `H_Q` at a point of the ascending right chain, on an Omega edge `e` at height `z2`, at distance `λ = x_exit - z1 < u < d`.
* `z2 < d`. The lower endpoint of `e` has `y < d`, so it is `B` or of type `R`; the upper endpoint is not `N` (S2) and not `T` (S4), so both endpoints have `x >= d`. If `e` is not the first edge, the L-cell of `e` contains `z` (`z = p - (λ,0)`, `0<=λ<=d`). If `e` is the first edge `B -> B+M`, `z` lies in `Δ`, which the bottom cell contains.
* `z2 >= d`. If `e` is L-eligible and not first: L-cell. Otherwise `e` crosses `x = d`, so by S3/S4 it is a `C→T` edge, hence D-eligible; since `z1` is strictly between the abscissae of the endpoints (`x_T < d < z1 < x_exit`), the vertical ray up from `z` also leaves through `e`, at distance `<= (d+v) - d = v < d`; so the D-cell of `e` contains `z`, provided `e` is not the last edge. The last edge exists only for `v >= 1` and lies in `T` (G12-L5), whereas `e` has an endpoint of type `C`; so `e` is not the last edge. For `v = 0` the set `{z2 > d}` is empty and `{z2 = d}` is null.
Cell corners are in `F_Q` by construction; generators are Graver (§2); hence all cells lie in `U_Q`. ∎

**Remarks.** (i) The "corner pentagon" and "top triangle" of v011 do not occur: the point `C` always sits on the bridging edge `C→T` or is itself an Omega vertex (G12-L4); T5 is the classification Omega ∈ `R* C* T*` with edges as above, T6 is the absence of a residual pentagon, T7 is the assembled mixed cover. (ii) The residual formulation `K_Q = H_Q \ (H_R ∪ H_T)` of the review is subsumed: the single family above covers `H_Q \ H_0` directly, for one-sided and mixed boxes alike; no separate residual argument is required. (iii) The hull-chain classification as `u` grows (G12-L1 in the specification) was not needed and is not claimed.

## 6. G12-T8 — universal planar stabilization  [PROVED+CHECKED]

**Theorem.** For every `d >= 2`, every unit `s`, every `Q1,Q2 >= d` with `Q != (d,d)`: `U_{d,s,Q} = conv(F_{d,s,Q})`.
*Assembly.* (a) `s = ±1`: G5-C1. (b) `max(Q) >= 2d`: G7-T1. (c) otherwise `d >= 5`, `2<=s<=d-2`, `Q = (d+u,d+v)` with `0<=u,v<d`, `(u,v) != (0,0)`: §5 (G10-R1 supplies `H_0`). Conditional on the three inherited results, all PROVED+CHECKED in v005–v010; no other hypothesis is used. For `Q = (d,d)` the hollow-box exception of v010 (`H_0` is not covered by cells in the exceptional configurations) stands unchanged. The planar *stabilization* problem for this family is therefore closed **by proof** (modulo the inherited results); the broader geometric organisation of the occurrence geometry remains open and is not claimed.

## 7. Computational support (CHECKED only)
* `cap_cover.verify`: legitimacy of every cell and exact rational proof that `H_Q \ (H_0 ∪ cells)` has no area, all `d<=12` boxes (2,130 CAPCOVER2 certificates), exact cover of every small box `d<=22` (29,206 boxes), structure lemmas S1–S6 on all boxes `d<=16` (7,464), 19,731 adversarial boxes up to `d=399`, 3,000 random boxes (`31<=d<=250`) (`experiments/cap_attack12.py`, `output/data/v12_cap.json`).
* No GAP certificate was produced: no box with an uncovered region was found.
* A separate standalone sweep `13<=d<=30` was interrupted and is recorded **PARTIAL** (`output/data/v12_sweep_13_30_PARTIAL.json`); it is not used by any proof or check.
