# GEO-I v005 — Programme A: uniform planar stabilization (G5-C1, G5-C2)

Labels: **PROVED** (hand proof in this file, every ingredient re-derived by exact computation), **PROVED+CHECKED**, **CHECKED** (exact finite computation, not a proof for all parameters), **FALSE**, **OPEN**, **UNAVAILABLE**, **CORRECTED**.
Frozen conventions of v004: `Γ_(d,s) = {(i,j) ∈ Z² : j ≡ s·i (mod d)}`, box `Q = (Q1,Q2)`, `F_Q = (Γ ∩ [0,Q]) ∖ {0}`, Graver moves = conformally minimal vectors of Γ, cells = parallelograms `P(u;g,h)` / segments / points with all corners in `F_Q`, `U_Q` = union of the cells, `H_Q = conv(F_Q)`.
By the v004 scaling reduction S1 every planar fibre is `(d,s,Q)`; nothing below modifies SELECT-I/II, FIELD-I or the occurrence arithmetic.

## 0. Status table

| ID | Statement | Status |
|---|---|---|
| G5-C1 (s = ±1) | `d ≥ 2`, `Q ≥ (d,d)`, `Q ≠ (d,d)` ⇒ `U_Q = conv(F_Q)` | **PROVED+CHECKED** (all `d ≥ 2`, all such `Q`) — new in v005 |
| G5-C1 (general s) | same statement for every unit `s` mod `d` | **CHECKED** for every `(d,s)` with `2 ≤ d ≤ 21` (translation lemma S4 + exact base window); **OPEN** beyond |
| G5-C2 (s = −1) | `β₁(U_(d,d)) = d` | **PROVED+CHECKED** (v004 fan graph; re-verified `d ≤ 40`) |
| G5-C2 (s = +1, d ≥ 3) | `β₁(U_(d,d)) = 2` | **PROVED+CHECKED** — new in v005 |
| G5-C2 (other s) | `β₁(U_(d,d)) = 2` for `s ≢ ±1` | **CHECKED** `d ≤ 21`; **OPEN** in general |

No counterexample to the corrected stabilization statement exists in the examined range, and a proof now exists for the two families `s = ±1`, for **all** `d`. The question "uniform theorem rather than individual certificates?" therefore has a positive answer for `s = ±1` and remains open for general `s`.

## 1. Explicit Graver sets for s = ±1  [PROVED]

**Lemma G.** (a) `s = −1` (`Γ = {i+j ≡ 0 (d)}`): `Graver = ±{(1,−1)} ∪ ±{(k, d−k) : 0 ≤ k ≤ d}`.
(b) `s = +1` (`Γ = {i ≡ j (d)}`): `Graver = ±{(1,1), (d,0), (0,d)} ∪ ±{(k, −(d−k)) : 1 ≤ k ≤ d−1}`.

*Proof (a).* Let `g = (a,b) ∈ Γ`. If `g` lies in the mixed-sign quadrants (`a>0>b` or `a<0<b`) then `±(1,−1) ⊑ g` (conformal order: same signs, smaller or equal absolute values) and `(1,−1) ∈ Γ`, so the only minimal vectors there are `±(1,−1)`. If `a,b ≥ 0`, then `a+b = md`, `m ≥ 1`; if `m ≥ 2` put `a' = min(a,d)`, `b' = d − a'`; then `0 ≤ a' ≤ a`, `0 ≤ b' ≤ b` (because `a + b ≥ d`) and `(a',b') ∈ Γ`, `(a',b') ≠ g`, so `g` is not minimal. If `m = 1`, `(a,b) = (k,d−k)` and no smaller non-zero vector of `Γ` fits below it (sums `< d`). The case `a,b ≤ 0` is the negative.
*(b)* Mixed signs: `(a,−b')`, `a,b' > 0`, `a ≡ −b' (d)`; minimal iff `a + b' = d` (otherwise split off `(a'', −(d − a''))` with `a'' = min(a,d−1)`..., and for `a + b' = d` nothing smaller is in `Γ`). Same signs: `(1,1) ⊑ (a,b)` whenever `a,b ≥ 1`; so the minimal ones are `(1,1)` and the axis vectors `(d,0)`, `(0,d)`. ∎ (Machine-checked against the generic enumeration for `d ≤ 14`: `tests/test_geo5.py`, `verify.py`.)

## 2. Theorem L — uniform stabilization for s = ±1  [PROVED+CHECKED]

**Theorem L.** Let `d ≥ 2`, `s ∈ {+1,−1}`, `Q = (Q1,Q2)` with `Q1, Q2 ≥ d` and `Q ≠ (d,d)`. Then `U_Q = conv(F_Q)`; in particular `U_Q` is contractible. (No translation lemma is needed; the proof works for every such `Q` directly.)

**Coordinates.** Let `D(i,j) = (i+j)/d` if `s = −1`, `D(i,j) = (j−i)/d` if `s = +1`; `D` takes integer values exactly on `Γ`, so `F` splits into *layers* `L_m = F ∩ {D = m}`. Use the linear coordinates `(D, p)` with `p = i`. Then
* `s = −1`: layer `m` (`1 ≤ m ≤ M = ⌊(Q1+Q2)/d⌋`) is `{(m,p) : α_m ≤ p ≤ β_m}`, `α_m = max(0, md − Q2)`, `β_m = min(Q1, md)`; the in-layer step is `e = (1,−1)`, a Graver vector, which moves `p ↦ p+1`; a *bridge* from `(m,p)` to `(m+1,q)` is the vector `(a, d−a)`, `a = q − p ∈ [0,d]`, Graver by Lemma G.
* `s = +1`: layers `−⌊Q1/d⌋ ≤ m ≤ ⌊Q2/d⌋`, `α_m = max(0,−md)` (and `α_0 = 1`, the origin being removed), `β_m = min(Q1, Q2 − md)`; `e = (1,1)`; the bridge is `(a, a+d)`, `a = q − p ∈ [−d, 0]`, Graver by Lemma G (`(−k, d−k)`, `0 ≤ k ≤ d`).

In `(D,p)`-coordinates the parallelogram `P((m,p); e, bridge to (m+1,q))` meets the level `D = m+λ` (`0 ≤ λ ≤ 1`) in the interval `[p + λ(q−p), p + λ(q−p) + 1]`.

**Step 1 — slices.** `H ∩ {D = m} = conv(L_m)` for every layer. (⊇ clear. ⊆: `H` lies in the box, and the box meets the line `D = m` exactly in `[α_m,β_m]`, except for `s=+1`, `m = 0`, where the box slice is `[0,β_0]` but the origin is removed. There every point of `H` with `D = 0` is a convex combination `Σ t_x x` of points of `F`; let `t_0`, `t_+`, `t_−` be the weights on layers `0`, `>0`, `<0`. Balance `Σ t_x D(x) = 0` gives `w := Σ_{m>0} t m = Σ_{m<0} t|m|`, hence `w ≥ t_+` and `w ≥ t_−`. Points of layer `0` have `i ≥ 1`, of layer `m < 0` have `i ≥ |m| d`, all others `i ≥ 0`; so `i ≥ t_0 + d·w ≥ t_0 + d(1−t_0)/2 ≥ 1` since `d ≥ 2`.)
The lower boundary `lo(D) = min{p : (D,p) ∈ H}` is convex and piecewise linear with breakpoints only at vertices of `H`, i.e. at integer `D` (vertices lie in `F`); so on `[m, m+1]` it is linear, hence equal to the chord from `(m,α_m)` to `(m+1,α_{m+1})`; likewise the upper boundary. Therefore
`H = ⋃_m T_m`, `T_m := H ∩ {m ≤ D ≤ m+1} = conv(L_m ∪ L_{m+1})` (a trapezoid, possibly a triangle).

**Step 2 — two layers with ≥ 2 points each.** Consider the lattice points `(p,q)` with `α_m ≤ p ≤ β_m − 1`, `α_{m+1} ≤ q ≤ β_{m+1} − 1`, and the *band* `q − p ∈ [alo, ahi]` (`[0,d]` for `s=−1`, `[−d,0]` for `s=+1`). Every such pair gives a cell `P((m,p); e, h(q−p))`. The start pair `(α_m, α_{m+1})` and the end pair `(β_m − 1, β_{m+1} − 1)` lie in the band, because `α_{m+1} − α_m` and `β_{m+1} − β_m` lie in the band (direct from the formulas). A monotone lattice path (steps `p ↦ p+1` or `q ↦ q+1`) from start to end that stays in the band always exists: while both coordinates are unfinished, step `p` if that keeps `q−p ≥ alo`, otherwise step `q` (possible since the band has width `d ≥ 1`); if `p` is finished, `q − p < (β_{m+1}−1) − (β_m − 1) ≤ ahi` so a `q`-step is allowed; if `q` is finished, `q − p > (\text{end}) \ge alo` so a `p`-step is allowed. Along the path consecutive cells have slice intervals shifted by `1−λ` or `λ`, both `≤ 1`, so at every level `λ` the union of the intervals is one interval, from the slice start `(1−λ)α_m + λα_{m+1}` of the first cell to the slice end of the last cell, which are exactly the endpoints of the slice of `T_m`. Hence `T_m ⊆ U`.

**Step 3 — an extreme layer with one point.** A layer has one point only if it is the top layer with `Q1+Q2 = Md` (`s=−1`), the top layer with `Q2 ≡ 0 (d)`, or (swap symmetry `(i,j) ↔ (j,i)`, which preserves `Γ_(d,1)`) the bottom layer with `Q1 ≡ 0 (d)` (`s = +1`). *Top apex `P`, neighbouring layer `[α,β]`:* the triangle `T = conv(P, v_α, v_β)` is half of the parallelogram with corners `P, v_α, v_β, u := v_α + v_β − P`, and it suffices that `u ∈ F` and that the generators `v_α − u`, `v_β − u` are Graver:
* `s = −1`: `P = (Q1,Q2)`, `M ≥ 3` (`M = 2` would force `Q = (d,d)`), `α = Q1 − d`, `β = Q1`, `u = (Q1−d, Q2−d)` — the corner of the `d × d` square `[Q1−d,Q1]×[Q2−d,Q2]` with generators `(d,0)`, `(0,d)`; `u ≠ 0` since `D(u) = M−2 ≥ 1`.
* `s = +1`: `P = (0,Q2)`, `Q2 = Md`; `β = d`, `α ∈ {0,1}` (`α = 1` iff `M = 1`); `u = (α + d, α + (M−1)d)` lies in the box (`α + d ≤ Q1` because `α = 1` forces `Q2 = d` and then `Q1 ≥ d+1` since `Q ≠ (d,d)`), `u ≠ 0`; the generators are `(−d, 0)` and `(−α, d−α)` (Graver).

**Step 4.** Layers strictly between the extremes always have ≥ 2 points; at most one apex per end occurs, and both ends cannot be single when the stack has only the layers `−1,0,1` unless `Q=(d,d)`. So every `T_m` is covered (Step 2 or 3) and `H = ⋃ T_m ⊆ U ⊆ H`. ∎

**Where the proof breaks — the hollow box.** For `Q = (d,d)` the top apex needs `u = (d,0)`-type corners that are removed (`s=−1`: `M = 2`, `u` would be the origin; `s=+1`: both end layers are single points and layer `0` starts at `i = 1`). This is exactly why `Q = (d,d)` is the unique exceptional box.

**Machine check (every sentence of Steps 2–3 on real data).** `theory/uniform_coverage.py` builds *exactly the cells used by the proof* (monotone path cells and apex cells) and verifies (i) every cell is a legitimate cell of `K_abs` (corners in `F`, generators Graver, independent), (ii) the exact rational union of these cells covers `conv(F)` (polygon subtraction in `mpq`). `experiments/layer_cover_check.py` ran it on every box `Q ∈ [d, 3d+2]²` for `s = ±1`, `2 ≤ d ≤ 14`: `8229` boxes, **0 failures** (`output/certificates/layer_cover_s_pm1.jsonl`).

## 3. G5-C2 — the hollow box `Q = (d,d)`  [s = ±1 PROVED+CHECKED]

`U` is a compact planar set, `β₂ = 0`, so `β₁(U)` = number of bounded components of the complement.

**s = −1** (v004, re-verified): `F = {(i,d−i)} ∪ {(d,d)}`, edges = `d` antidiagonal steps + `d+1` spokes, no 2-cell: `V = d+2`, `E = 2d+1`, `β₁ = E − V + 1 = d`.

**s = +1, d ≥ 3 (new).** `F = {(i,i) : 1 ≤ i ≤ d} ∪ {A=(d,0), B=(0,d)}`. The only 2-cells are `P_i = conv{A,(i,i),B,(d−i,d−i)}`, `1 ≤ i < d/2` (a parallelogram needs two points off the diagonal, i.e. `A` and `B`, and its diagonals `AB` and `(i,i)(j,j)` must bisect at `(d/2,d/2)`, i.e. `i + j = d`); they are nested and `P_1` (corners `A,(1,1),B,(d−1,d−1)`) contains all of them. The edges not inside `P_1` are exactly `A–(d,d)`, `B–(d,d)` and `(d−1,d−1)–(d,d)`. Each meets `P_1` only in its endpoint other than `(d,d)` (`P_1 ∩ {x = d} = {A}`, `P_1 ∩ {y = d} = {B}`, and `x+y` is maximised on `P_1` at `(d−1,d−1)` alone, `2d−2 > d`). So `U = P_1 ∪ {(d,d)} ∪ 3 arcs`, `χ(U) = 1 + 1 − 3 = −1`, `U` connected, hence `β₁ = 2`. ∎ (`theory/hollow_box.py` recomputes the cell structure from the definitions for `3 ≤ d ≤ 40` and checks each claim; `conv(F) ∖ P_1` is the non-convex quadrilateral `A,(d,d),B,(d−1,d−1)` (area `d`), split into **two triangular holes** by the spur `(d−1,d−1)–(d,d)`.)

**General s.** `β₁ = 2` was recomputed (exact planar arrangement) for every `(d,s)` with `d ≤ 12` (`output/data/hollow_betti.json`) and by the search for every type with `d ≤ 21` (`output/data/stabilization_extended.jsonl`): **CHECKED, 0 mismatches**. Structural reading: in the hollow box the corner `(d,d)` is joined only to the corner points `A`, `B` and to the points `(d,d) − g`, `g` a *positive* Graver vector; the number of such `g` is the number of Hilbert-basis elements of the open first quadrant of `Γ` (continued-fraction data of `s/d`), and for `s ≠ −1` the computation shows that the 2-cells fill in everything except two holes (observation, **CHECKED**). A proof for general `s` is **OPEN** (see §5).

## 4. Corrected stabilization statement after v005

> **Theorem (corrected G4-C1, v005 form).** Let `d ≥ 2`, `Q1, Q2 ≥ d`. (i) If `Q ≠ (d,d)` then `U = conv(F)`, hence `β₁(U) = 0`: **PROVED for `s = ±1`, all `d`; CHECKED for all `(d,s)`, `d ≤ 21`; OPEN beyond.** (ii) If `Q = (d,d)`, then `U` is hollow and `β₁ = B(d,s)` (`d` if `s ≡ −1`, otherwise `2`): proved for `s = ±1`, checked `d ≤ 21`. For `d = 1`, `U` is always contractible (v004, proved).

## 5. What is *not* proved, and why the s = ±1 proof does not simply extend

For a general unit `s` the layers (level sets of `D = (j − s i)/d`, in-layer step `(1,s)`) still exist and `H = ⋃ T_m` still holds (Step 1 uses only convexity and integrality of `D` at vertices). What fails is Step 2: the bridges are the Graver vectors `h` with `D(h) = 1`, and their `p`-offsets form only a *short* interval of consecutive integers — for `(d,s) = (5,2)` the Graver vectors with `D = 1` are `(−3,−1), (−2,1), (−1,3), (0,5)` (offsets `−3…0`), for `(7,3)` and `(8,3)` again offsets `−3…0` — whereas the layer end points shift by more than that, so the band condition of Step 2 fails (for `s = ±1` the bridges `(k,d−k)` give the full band of `d+1` offsets, which is exactly what makes the argument work). Genuine two-bridge cells `P(u;h_a,h_b)` (determinant `d·|a−b|`, spanning three layers) must then be used in the bulk, not only at the apex. The base-window certificates show that the full Graver cell family always suffices for `d ≤ 21`. A proof would need a uniform description of the covering cells in terms of the continued fraction of `s/d` (Hirzebruch–Jung / Hilbert basis of the two sign cones). That is the next theorem to attack; nothing is claimed for it.

The earlier experiment that tried to cover `conv(F)` with fundamental (area `d`) cells alone failed on 921 of the 5068 window boxes examined cumulatively for `3 ≤ d ≤ 10` (scratch exploration, not shipped), which is evidence that multi-layer cells are essential in general.

## 6. Reproduction

```
python experiments/stabilization_search.py DMIN DMAX OUT.jsonl [SHARD NSHARD]   # base-window certificates (resumable)
python experiments/layer_cover_check.py DMAX OUT.jsonl                            # s = ±1 proof cells
python experiments/hollow_homology.py DMAX OUT.json                               # beta_1 at (d,d)
python verify.py [--smoke]
```
Certificates: `output/data/stabilization_certificates.jsonl` (v004, `d ≤ 13`), `output/data/stabilization_extended.jsonl` (v005, `14 ≤ d ≤ 21`), `output/certificates/layer_cover_s_pm1.jsonl`.
