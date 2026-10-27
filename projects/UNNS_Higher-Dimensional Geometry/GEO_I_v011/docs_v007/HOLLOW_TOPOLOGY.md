# GEO-I v007 — Programme C: the hollow box `Q = (d,d)`

## 0. Result

* **Theorem G7-T3 (new, PROVED+CHECKED).** For every `d ≥ 3` and **every unit `s`** (including `s = −1`), with `t = s⁻¹ mod d`, the two triangles
  `T₁ = conv(A, P_{d−t}, C)` and `T₂ = conv(B, P_{d−1}, C)` (`A=(0,d)`, `B=(d,0)`, `C=(d,d)`, `P_i = (i, s·i mod d)`; so `P_{d−t} = (d−t,d−1)`, `P_{d−1} = (d−1,d−s)`), each of area `d/2`, satisfy `∂Tᵢ ⊂ U` and `int Tᵢ ∩ U = ∅`. Consequently `R²∖U` has **at least two bounded components** (`int T₁`, `int T₂`) and `β₁(U_{(d,d)}) ≥ 2`. (v006 had only the hole structure as CHECKED for `d ≤ 45`; the lower bound is now a theorem for all `d`.)
* **G7-T4 / G7-C1H (CHECKED, OPEN in general).** `conv(F) ∖ U = int T₁ ∪ int T₂` (total area `d`) and `β₁ = 2` for `s ≢ −1`, `d ≥ 3`: exact for `d ≤ 45` (v006 record, inherited), Betti numbers recomputed through the v005 chain complex for `d ≤ 10` (smoke/full) and shipped to `d ≤ 20`. The covering of `H ∖ (T₁ ∪ T₂)` by cells is **not proved** for all `(d,s)`. For `s = −1` the complex is the fan graph with `β₁ = d` (v005 Theorem H1, inherited); the two-triangle complement is not forced there and is not claimed.

## 1. Notation and the fibre

`Γ = {(i,j): j ≡ s i (mod d)}`, `F = Γ ∩ [0,d]² ∖ 0`. **Lemma H0.** `F = {P_i : 1 ≤ i ≤ d−1} ∪ {A,B,C}`, `|F| = d+2`. *Proof.* For `1 ≤ i ≤ d−1`, `s i mod d ∈ [1,d−1]` (unit), so column `i` has the single point `P_i` with `y ≤ d`. Column `0`: `(0,d)` (the origin is removed). Column `d`: `(d,0)`, `(d,d)`. ∎ In particular `F ∩ {y = d} = {A, C}` (unit `s`).

**Height and lattice coordinates.** For `p = (x,y) ∈ F` put `a(p) = d − y ∈ {0,…,d}`; `a(p) = 0 ⇔ p ∈ {A,C}`. Let `u = P_{d−t} − A = (d−t,−1)`, `w = C − A = (d,0)`; `u,w ∈ Γ` and `|det(u,w)| = d` = covolume, so `(u,w)` is a basis of `Γ`. For `p ∈ Γ`, `p − A = a·u + b·w` with `a = d − y` and `b = (x − a(d−t))/d`, both **integers**. In `(a,b)`-coordinates `T₁ = {a,b ≥ 0, a+b ≤ 1}`, `A = (0,0)`, `P_{d−t} = (1,0)`, `C = (0,1)`. By transposition `(x,y) ↦ (y,x)` (which maps `Γ_{d,s}` to `Γ_{d,t}`, preserves boxes `(d,d)`, cells and Graver vectors, and maps `T₂(s)` to `T₁(t)`), everything proved for `T₁` holds for `T₂`.

## 2. Proof of G7-T3

**Lemma H1 (boundary).** The edges of `T₁` are `A→P_{d−t} = u = (d−t,−1)`, `P_{d−t}→C = (t,1)`, `A→C = (d,0)`; all are Graver and have endpoints in `F`; so they are 1-cells and `∂T₁ ⊂ U`. *Proof.* `γ = (a',b') ∈ Γ` conformally below `(d−t,−1)` has `0 ≤ a' ≤ d−t`, `b' ∈ {−1,0}`; `b' = 0 ⇒ a' ≡ 0 ⇒ a' = 0`; `b' = −1 ⇒ s a' ≡ −1 ⇒ a' ≡ −t ⇒ a' = d−t`. Similarly `(t,1)` (`b' = 1 ⇒ a' ≡ t`), and `(d,0)` is Graver (`(k,0) ∈ Γ ⇔ d | k`). ∎

**Lemma H2 (no 1-cell meets `int T₁`).** Let `p,q ∈ F`, `q−p` Graver, and suppose the segment `[p,q]` meets `int T₁ ⊂ {0 < a < 1}`. Since `a` is integer-valued on `F` and affine, w.l.o.g. `a(p) = 0 < 1 ≤ a(q)`, so `p ∈ {A,C}`.
* `p = A`: points of the segment have coordinates `λ(a_q, b_q)`, `λ ∈ (0,1]`; lying in `int T₁` needs `b_q ≥ 1`. Then `q − A = (a_q(d−t) + b_q d, −a_q)` and `u = (d−t,−1)` satisfies `0 ≤ d−t ≤ q_x`, `1 ≤ a_q`; so `u` is conformally below `q−A` and `u ≠ q−A` (as `b_q ≥ 1`): `q−A` is not Graver. Contradiction.
* `p = C = (0,1)` in `(a,b)`-coordinates: points `(λ a_q, 1 + λ(b_q−1))`; `a + b = 1 + λ(a_q + b_q − 1) < 1` needs `a_q + b_q ≤ 0`, i.e. `b_q ≤ −a_q`. Then `q_x = a_q(d−t) + b_q d ≤ a_q(d−t) − a_q d = −a_q t < 0`, impossible for `q ∈ F`. ∎

**Lemma H3 (2-cells).** No parallelogram cell `K` meets `int T₁`. *Proof.* No vertex of `K` lies in `int T₁` (`a` is an integer on `F`), and no edge meets it (H2); so `int T₁` (connected) lies entirely in `int K` or entirely outside `K`. If it meets `K` it lies in `int K`, hence `A, C ∈ T₁ ⊂ K`. As `a ≥ 0` on `K` and `a(A) = a(C) = 0`, `K ∩ {a = 0}` is a face of `K` containing `[A,C]`: an edge, inside the box segment `[0,d]×{d}`, hence equal to `[A,C]`; so one generator is `±(d,0)`. For the other generator `h`, the corners `A+h, C+h ∈ F ⊂ [0,d]²` force `h_x = 0`, so `h ∈ Γ ∩ {x = 0} = {0}×dZ`, Graver, i.e. `h = (0,−d)` (`K` lies below `y = d`); then `A + h = (0,0) ∉ F`. Contradiction. ∎

**Proof of the theorem.** `int Tᵢ` is open, connected, bounded, disjoint from `U` (Lemmas H2, H3 and points), and `∂Tᵢ ⊂ U` (H1); hence `int Tᵢ` is open and closed in `R²∖U`, i.e. a bounded component. `int T₁ ≠ int T₂`, so they are two distinct components. For a compact polyhedron `U ⊂ R²`, Alexander duality gives `β₁(U) = #(bounded components of R²∖U)`; hence `β₁ ≥ 2`. ∎

*What the proof uses:* only that `s` is a unit (for `F ∩ {y=d} = {A,C}` and `(u,w)` a basis) and `d ≥ 3` (so that `T₁, T₂` are nondegenerate and distinct from the s = −1 collapse of the boundary into the fan; the argument also runs for `d = 2`, which is not claimed).

## 3. Machine verification

`theory/hollow_geometry.py` recomputes, for a given `(d,s)`, `F`, the triangles, primitivity (`Γ ∩ T = vertices`), the Graver status of the edges, **every** Graver segment between points of `F` and **every** parallelogram cell against the open triangles with exact rational arithmetic. `experiments/hollow_attack.py` ran all unit classes: `3 ≤ d ≤ 50` (772 classes) and `51 ≤ d ≤ 64` (486 classes): **0 failures**. `certificates/D3_hollow.json` + `certificates/checker.py` (own implementation) validate eight sample classes (including `s = −1`). Third path: the v005 exact uncovered-region routine gives total complement area `2d` (area2) on `d ∈ {5,7,8,9}`.

## 4. Open parts (not claimed)

1. `H ∖ (T₁ ∪ T₂) ⊂ U` for all `(d,s)` (upper bound `β₁ = 2`): CHECKED to `d = 45` (v006). 2. Whether the complement for `s = −1` has a uniform description (it has `d` bounded components, v005 H1). 3. Higher Betti numbers `β₂ = 0` are inherited from planarity (`U ⊂ R²`).
