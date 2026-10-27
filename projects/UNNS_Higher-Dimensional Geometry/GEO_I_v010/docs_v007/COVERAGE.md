# GEO-I v007 — Programme A: coverage `U = conv(F)`

Status vocabulary: PROVED, PROVED+CHECKED, CHECKED, FALSE, CORRECTED, OPEN, UNAVAILABLE. TARGET is not a status.

## 0. Result in one paragraph

**Theorem A-COL (G7-T1, new, PROVED+CHECKED).** For every `d ≥ 2`, every unit `s` and every box `Q = (Q₁,Q₂)` with `Q₂ ≥ 2d`: `U = conv(F)`. By transposition the same holds when `Q₁ ≥ 2d`. This is a general-`d`, general-`s` coverage theorem for every box with `max(Q) ≥ 2d` (all thick and thin boxes). It replaces the v006 statement, which was only CHECKED window by window and whose "corner-sail" hypothesis HYP-LL is false (§5). **G7-C1 is therefore reduced to the small boxes** `Q ∈ [d,2d−1]² ∖ {(d,d)}`; there it stays **OPEN** (CHECKED for `d ≤ 30` by v006, and a squareless-zone search to `d ≤ 32` found no counterexample, §6). Acceptance label for Programme A: **A-PARTIAL** (a new general theorem plus a precise reduction; not A-PROVED).

## 1. Setting (frozen definitions)

`Γ = Γ_{d,s} = {(i,j) ∈ Z² : j ≡ s·i (mod d)}`, `1 ≤ s ≤ d−1`, `gcd(s,d)=1`. `F = (Γ ∩ [0,Q]) ∖ {0}`; `H = conv(F)`. Graver = conformally minimal nonzero element of `Γ`. Cells of `K_abs`: points, Graver segments with endpoints in `F`, parallelograms `P(u;g,h)` with independent Graver `g,h` and all four corners in `F`. `U` = union of cells; always `U ⊆ H`.

*Graver vectors used.* `(0,d)`, `(1,s)`, `(1,s−d)` are Graver: a `γ = (a,b) ∈ Γ` conformally below `(1,s)` has `a ∈ {0,1}`, `0 ≤ b ≤ s < d`; `a = 0 ⇒ d | b ⇒ b = 0`; `a = 1 ⇒ b ≡ s ⇒ b = s`. Same for `(1,s−d)` (`s−d ≤ b ≤ 0`). `(0,k)` with `0<k<d` is not in `Γ`.

## 2. The column-strip construction (replaces the v006 "corner-sail")

Column `i` (`0 ≤ i ≤ Q₁`): bottom `b_i = s·i mod d` for `i ≥ 1`, and `b₀ := d` (the origin is removed). `K_i = ⌊(Q₂−b_i)/d⌋`, so column `i` of `F` has exactly `K_i+1` points `(i, b_i + kd)`, `0 ≤ k ≤ K_i`. `B_i = (i,b_i)`, `T_i = (i,b_i+K_i d)`. Cells (all in `K_abs`, §3):

* **(S)** `P(B_i + k(0,d); (1,δ_i),(0,d))`, `0 ≤ k < min(K_i,K_{i+1})`, `δ_i = b_{i+1}−b_i ∈ {s, s−d}`.
* **(M)** `P(T_i; T_{i+1}−T_i, (0,−d))` whenever `K_i ≠ K_{i+1}`.
* **(L)** `P(B_i; B_{i'}−B_i, (0,d))` for every *lower hull piece* (two bottoms consecutive among the bottoms lying on one edge of the lower boundary of `H`).
* **(Up)** `P(T_i; T_{i'}−T_i, (0,−d))` for every upper hull piece.

`theory/corner_sail.py` builds these cells; `check_lemmas` recomputes every lemma below on an instance.

## 3. Proof of Theorem A-COL

Let `Q₂ = qd + ρ`, `0 ≤ ρ < d`.

**Lemma 1 (every column has ≥ 2 points).** `b_i ≤ d` for all `i`, so `K_i = ⌊(Q₂−b_i)/d⌋ ≥ ⌊d/d⌋ = 1`. (This is where `Q₂ ≥ 2d` is used; for `i = 0` it needs `b₀ = d`.)

**Lemma 2 (steps).** (a) `K_i = q` if `b_i ≤ ρ` and `q−1` otherwise (`b_i ∈ [0,d]`), so `|K_i−K_{i+1}| ≤ 1`. (b) `b_{i+1} ≡ b_i + s (mod d)`, with `b_{i+1} ∈ [0,d−1]`, hence `δ_i ∈ {s,s−d}` (for `i = 0`: `b₁ − b₀ = s − d`). (c) If `K_i = K_{i+1}+1` then `b_i ≤ ρ < b_{i+1}`, so `δ_i = s` and `T_{i+1}−T_i = (1, s−d)`. If `K_i+1 = K_{i+1}` then `b_{i+1} ≤ ρ < b_i`, so `δ_i = s−d` and `T_{i+1}−T_i = (1,s)`. In both cases `T_{i+1}−T_i` is Graver (§1).

**Lemma 3 (legitimacy of S and M).** The corners of an (S)-cell are `(i,b_i+kd), (i+1,b_{i+1}+kd), (i,b_i+(k+1)d), (i+1,b_{i+1}+(k+1)d)`, all in `F` because `k+1 ≤ min(K_i,K_{i+1})`; generators `(1,δ_i),(0,d)` are independent Graver. For (M): the corners `T_i, T_{i+1}, T_i−(0,d), T_{i+1}−(0,d)` are in `F` by Lemma 1, and `T_{i+1}−T_i` is Graver by Lemma 2(c).

**Lemma E (hull pieces are Graver).** Let `p,p'` be two points of `F` that are consecutive points of `F` on one edge of `∂H` (no point of `F` on the open segment), `g = p'−p`. Then `g` is Graver, except possibly when the origin is involved, which does not occur (below). *Proof.* Suppose `0 ≠ γ ∈ Γ`, `γ ≠ g`, conformally below `g`. Then `p+γ` lies in the closed rectangle with opposite corners `p,p'`, which lies in the box. Also `p'−γ = p + (g−γ)` is in the rectangle, and `g−γ` is also conformally below `g`. Neither point is `0` unless the rectangle contains the origin, i.e. `p = (0,d)`, `γ = (0,−d)`, `p' = (i',0)`; then `i' ≥ d` and `(d,0) ∈ F` lies on or below the line from `(0,d)` to `(i',0)`; for `p,p'` to span a hull edge, `i' = d` and every `(i, b_i)` must lie on or above that line, forcing `b₁ = s = d−1`, i.e. `s = −1`; but then `(1,d−1) ∈ F` lies on the segment, contradicting consecutiveness. So both points `p+γ` and `p+g−γ` are in `F ⊆ H`, hence on one closed side of the supporting line of the edge; they are symmetric about the midpoint of `pp'` (their sum is `2p+g`), so both lie on the line, hence on the segment `pp'`; they are neither endpoint (`γ ≠ 0,g`), contradicting consecutiveness. ∎ The same argument applies to the upper hull with tops (the tops have `y > Q₂−d ≥ d > 0`, so `0` never occurs).

**Lemma 4 (hull edges consist of bottoms / tops).** Every point of `F` on the lower boundary of `H` is the bottom of its column, so lower hull pieces are pairs of bottoms; likewise for tops. (Otherwise a lower point of the same column lies below.)

**Lemma 5 (sliver height).** `0 ≤ l(x)` (all points of `F` have `y ≥ 0`) and `b_i ≤ d` give `PB(x) − l(x) ≤ d` for the polyline `PB` through the bottoms; and `T_i.y > Q₂−d`, `u(x) ≤ Q₂` give `u(x) − PT(x) < d` for the polyline `PT` through the tops (`l,u` = lower and upper boundary of `H`).

**Legitimacy of L and Up.** Corners `B_i, B_{i'}, B_i+(0,d), B_{i'}+(0,d)` are in `F` by Lemma 1; generators `B_{i'}−B_i` (Lemma E) and `(0,d)` are independent Graver. Same for `Up`.

**Covering.** `H ∩ {x = x₀} = {l(x₀) ≤ y ≤ u(x₀)}` and columns `0` and `Q₁` are nonempty, so `H` lies over `x ∈ [0,Q₁]`. Fix a slab `i ≤ x ≤ i+1`, `m = min(K_i,K_{i+1})`. Over the slab, the interval `[l,u]` is the union of: `[l, PB]`, contained in the (L)-cell of the lower hull piece above `x` (Lemma 5: the cell is `{l ≤ y ≤ l+d}` over that piece, and the lower-hull pieces tile `[0,Q₁]`); `[PB, PB + md]`, the union of the (S)-cells; `[PB+md, PT]`, empty if `K_i = K_{i+1}` and otherwise the triangle `(T_i−(0,d), T_i, T_{i+1})` (resp. its mirror), which lies in the (M)-cell; and `[PT, u]`, contained in the (Up)-cell. Hence `H ⊆ ∪ cells ⊆ U ⊆ H`. ∎

**Remarks.** (i) The proof uses `gcd(s,d)=1` only through the stated setting; the machine check also passes for non-unit `s` (`d ≤ 8`, 1086 boxes) and for `Q₁ < d` (755 boxes). These are CHECKED remarks, not claims. (ii) The cell count is `O(|F|)` (one strip cell per elementary column parallelogram plus `O(Q₁)` mismatch and sliver cells), much smaller than the generic enumeration (`certificates/D5_cost.json`: 7–15× fewer cells on the benchmark boxes). (iii) The exceptional edge `(0,d)–(d,0)` of `∂H` exists only for `s = −1`, where `F` has points on it; the proof never uses it as a hull piece.

## 4. Machine verification of Theorem A-COL

`experiments/coverage_attack.py acol 12` recomputed, for every `d ≤ 12`, every unit `s`, `Q₁ ∈ [d,3d]`, `Q₂ ∈ [2d,3d]`, **8063 boxes**: all strip cells are legitimate cells, the exact rational polygon subtraction leaves nothing uncovered, and every lemma of §3 holds (`corner_sail.check_lemmas`). `verify.py` regenerates `d ≤ 5` (smoke) / `d ≤ 9` (full) and 25 / 120 random boxes with `14 ≤ d ≤ 45`, and re-checks the shipped record. Independent second path: the standalone checker `certificates/checker.py` re-derives `F`, Graver status and an explicit finite subdivision of `conv(F)` into convex pieces (`certificates/D1_coverage.json`).

## 5. HYP-LL: classification with exact witnesses (stays FALSE)

HYP-LL (v006): *every step `(m_i,m_{i+1})` of every corner sail has a legitimate completion by `(0,±d)` or `(±d,0)` pointing into the box.* `ML.corner_chain` gives the sail; `coverage_lemmas.hypll_step_failures(d,s,Q)` returns the failing steps (each is an exact witness). Results for all boxes `Q ≥ (d,d)`, `Q ≠ (d,d)`, `Q ∈ [d,3d)²`, `d ≤ 10` (6602 boxes): **571 boxes have a failing step**: 368 with `r₁ = 0` or `r₂ = 0`, and 203 *small* boxes with `r₁,r₂ > 0` (all with `max(Q) < 2d`). **No box with `r₁,r₂>0` and `max(Q) ≥ 2d` fails.** Smallest witness: `(d,s,Q) = (3,1,(3,4))`, corner `(0,0)`, step `(0,3) → (1,1)`: the completions `(0,3)` and `(3,0)` both leave the box (corners `(0,6)` resp. `(4,1)`). This does **not** falsify G7-C1: Theorem A-COL covers every thick and thin box with a different cell family, and small boxes need their own treatment. HYP-LL is retained in the registry as **FALSE**.

## 6. What remains: small boxes `Q ∈ [d,2d−1]²`

Let `(r₁,r₂) = (Q₁−d, Q₂−d)`. A box is *squareless* if `Γ ∩ [0,r₁]×[0,r₂] = {0}` (then no `d×d` square cell exists). Structure observed: for non-squareless small boxes the union of the vertical and the horizontal "double-column" bands covers `H` (exact check, 1920 boxes, `3 ≤ d ≤ 11`, `experiments/band_hulls.py`, record `output/data/v7_band_hulls.json`); small boxes are certified box by box by v006 (`small_boxes.py` family test with generic fallback; CHECKED for `d ≤ 30`). No proof of the band structure is claimed. Squareless small boxes are exactly the hollow box's `F` plus single-point extension columns/rows; minimal covers there need larger-determinant mixed cells (greedy covers for `d = 11, s = 3` use `(0,11),(11,0),(1,−8),(1,3),(7,−1),(3,−2)`), so the strip family does **not** cover them (1014 of 1586 squareless boxes uncovered for `3 ≤ d ≤ 13`). Adversarial search (exact generic routine on every squareless small box): **3 ≤ d ≤ 32 — 29,890 squareless boxes** (1,888 for `d ≤ 14`, 9,244 for `15 ≤ d ≤ 24`, 18,758 for `25 ≤ d ≤ 32`), **0 counterexample candidates, 0 unresolved** (`output/data/v7_sqless_*.json`). A counterexample would need an exact rational `z ∈ conv(F)∖U` with independent certificates; none was found. **No proof for the squareless zone is claimed.**
