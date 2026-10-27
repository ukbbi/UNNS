# GEO-I v002 — Mathematics

Definitions are ours (introduced here); theorems are proved from them or from cited Volume results. Status labels: **PROVED**, **PROVED+CHECKED** (proof here and exact computation), **CHECKED** (finite exact computation only), **MEASURED** (statistic, not a claim of law), **CONJECTURE**, **OPEN**. Scope tags: A0 (occurrence arithmetic), A2 (SELECT-II), C (collective map). No SELECT-II and C trajectories are combined.

## 1. Definitions

For reduced `x = a/b`, `a = ∏ pᵢ^{eᵢ}`, keep primes with `qᵢ = ⌊eᵢ/2⌋ ≥ 1` (k of them). `B = ∏{0..qᵢ}`, `χ_b(α) = ∏ pᵢ^{αᵢ} mod b` (negative exponents via inverses; each pᵢ is a unit because gcd(a,b)=1), `Λ_b = ker χ_b ⊂ Z^k` (`Λ_1 = Z^k`). **Fibre** `F_x = (B ∩ Λ_b) ∖ {0}`; this is `D(x)` of Vol. I (A0, Rational-Fibre Theorem) written in exponent coordinates.

**Cells.** For lex-positive, pairwise-distinct, linearly independent vectors `g₁<…<g_j` and a base `u` (the lex-minimal vertex), the parallelotope `P(u; g₁..g_j)` has the 2^j vertices `u + Σ_{i∈S} gᵢ`. It is a *j-cell* of a complex if all 2^j vertices lie in `F_x` and every `gᵢ` is an allowed move. Boundary: `∂P = Σᵢ (−1)^{i−1} [P(u+gᵢ; ĝᵢ) − P(u; ĝᵢ)]`; ∂∂ = 0 is verified on every complex built.

* **K_axis(x)**: allowed moves = unit vectors (ordinary cubical complex).
* **K_move(x)**: allowed moves = **region Graver set** `G_x`: the conformally minimal nonzero vectors of `Λ_b` inside `[−q,q]`. (`g ⊑ h` iff `gᵢhᵢ ≥ 0` and `|gᵢ| ≤ |hᵢ|`; only vectors in `[−q,q]` can be differences of box points, and a vector of that region is ⊑-minimal in `Λ_b` iff it is ⊑-minimal in `Λ_b ∩ [−q,q]`.) These are the Graver-basis elements that can occur as edges of the fibre.
* **Dimensions.** `d_amb = k`; `d_aff` = rank of `{u − u₀ : u ∈ F}`; `d_cell` = largest j for which a j-cell exists.

Move edges are geometric relations in the lattice; they are **not** SELECT-II or FIELD-I transitions.

## 2. Theorems

**Prop 1 (cell dimension, integer fibres; T1) — PROVED + CHECKED.** For b = 1 and k ≥ 1: `d_cell = k` if `max qᵢ ≥ 2`, and `d_cell = k−1` if `q₁=…=q_k=1`.
*Proof.* A k-cell is a unit k-cube `∏{cᵢ, cᵢ+1}` inside `B`; it avoids the origin iff some `cᵢ ≥ 1`, which requires `qᵢ ≥ 2`. If all `qᵢ = 1`, the only unit k-cube is `B` itself (it contains 0), but the far facet `{x₁=1}` is a (k−1)-cube avoiding 0 (k=1: a single vertex, d_cell = 0). ∎ Checked by builder for all 19 / 69 sorted patterns (k≤3,q≤3 / k≤4,q≤4) and all integers 2..3000.

**Prop 2 (integer fibre complexes are contractible) — PROVED + CHECKED.** For b = 1, K_axis(x) is homotopy-equivalent to a point.
*Proof.* K_axis is the union of the closed unit cubes of `[0,q]` that do not have the origin as a vertex; its realization is `Y = {x ∈ [0,q] : some xᵢ ≥ 1}`. `Y` is star-shaped about `c = q` (if `xᵢ ≥ 1` then `xᵢ + t(qᵢ − xᵢ) ≥ xᵢ ≥ 1`), hence contractible. ∎

**Thm A (coordinate complex of a rational cut; GEO-T3, axis side) — PROVED + CHECKED.** Let `S = {i : pᵢ ≡ 1 (mod b)}`, `T` the other axes, `Λ_T = {α_T : ∏_{i∈T} pᵢ^{αᵢ} ≡ 1}`. Then K_axis(x) is homotopy-equivalent to a **discrete** set with
`#components = |(Λ_T ∩ B_T) ∖ {0}| + [S ≠ ∅]`,
all Betti numbers in degree ≥ 1 vanish, and `d_cell = |S|` if `(Λ_T∩B_T)∖{0} ≠ ∅` or `max_{i∈S} qᵢ ≥ 2`, `d_cell = |S|−1` if `S ≠ ∅` otherwise, and `d_cell = 0` if `S = ∅`.
*Proof.* If α and α+eᵢ both lie in `Λ_b` then `pᵢ ≡ 1`, so every edge, hence every cell, of K_axis moves only along S-axes: each cell lies in one slice `α_T = const`. Because `pₛ ≡ 1` for s∈S, `χ_b(α_S, α_T) = χ_T(α_T)` does not depend on `α_S`. A slice is therefore nonempty iff `α_T ∈ Λ_T ∩ B_T`; for `α_T ≠ 0` it is the full box `B_S` (a point if S = ∅), for `α_T = 0` it is the punctured box `B_S ∖ {0}` (empty if S = ∅). Boxes are convex and punctured boxes are contractible (Prop 2). The dimension statement follows slice by slice (Prop 1 for the punctured slice). ∎
*Checked* on all 8,203 corpus fibres (components, d_cell, Betti numbers mod 2 and mod 2³¹−1).

**Cor A1 (evolution) — COROLLARY (C-scope; uses v001 Thm 3.2 / Vol. II T51 + T61; verified only on the g = 11 orbit).** Along an eventual regime `x_{n+P} = p^{2s}x_n`, `b`, `S`, `T` are constant. If `p ∈ T` then `#components(K_axis(x_{n+mP}))` is quasi-linear in m (layer-count argument of v001 Thm 3.2 applied to T-slices); if `p ∈ S` it is eventually periodic in m. For g = 11 benchmark `S = ∅`, `p = 3 ∈ T`: components = R at every one of 60 steps.

**Thm B (Graver-move connectivity; GEO-T2) — PROVED + CHECKED.** If `F_x ≠ ∅`, the graph on `F_x` with edges `{u, v}` whenever `v − u ∈ G_x` is connected.
*Proof.* (1) *Conformal decomposition.* Every nonzero `λ ∈ Λ_b ∩ [−q,q]` is a sum `λ = g₁+…+g_r` of elements of `G_x`, each conformal to λ: pick a ⊑-minimal `g ⊑ λ` in the finite set `Λ_b ∩ [−q,q]`, then `λ − g` is again in `Λ_b ∩ [−q,q]`, conformal to λ and smaller in ℓ¹; induct. (Classical: Graver 1975.) (2) For `u ≠ v` in F, `v − u ∈ Λ_b ∩ [−q,q]`; write `v − u = Σ gⱼ` as in (1). The partial points `wⱼ = u + g₁+…+gⱼ` lie in `Λ_b`, and coordinatewise between `uᵢ` and `vᵢ`, hence in B. They lie in F unless some `wⱼ = 0`. (3) *Origin lemma.* Suppose `wⱼ = 0`. Then `Σ_{≤j} g = −u` and `Σ_{>j} g = v`; each partial sum of conformal terms is conformal to `v − u`, so `−u` and `v` are conformal to `v − u`. For i with `uᵢ > 0`: `vᵢ − uᵢ ≤ 0`; for i with `vᵢ > 0`: `vᵢ − uᵢ ≥ 0`. If both held, `vᵢ = uᵢ`, so all gⱼ have 0 in coordinate i and `−uᵢ = Σ(gⱼ)ᵢ = 0`, contradiction. So `supp u ∩ supp v = ∅` and `u + v ∈ B ∩ Λ_b`, `u+v ≠ 0`. Then `u → u+v → v` is a path of Graver moves in F: add a conformal decomposition of `v` (points stay ≥ u coordinatewise, so nonzero and ≤ u+v), then add a conformal decomposition of `−u` (points stay ≥ v and ≤ u+v; nonzero because ≥ v ≠ 0). ∎
*Relation to known work.* Part (1)–(2) is the standard fact that Graver bases connect all bounded fibres of a lattice (Graver 1975; Sturmfels 1996; Diaconis–Sturmfels 1998); the only addition here is the origin lemma, needed because the origin is removed. *Checked* on 8,203 corpus fibres (connected in every case) and on 411 sampled fibres the region Graver set was verified complete (every lattice vector in `[−q,q]` decomposes conformally into region Graver vectors).

**Prop C (monotone subcomplex) — PROVED + CHECKED.** If `eᵢ ∈ Λ_b` (i.e. `pᵢ ≡ 1`), then `±eᵢ ∈ G_x` (unit vectors are minimal), so K_axis ⊂ K_move and `d_cell(move) ≥ d_cell(axis)`; if `Λ_b = Z^k`, `G_x = {±eᵢ}` and the complexes coincide. Strict inequality occurs on 264 of 8,203 corpus fibres (e.g. 2304/5: 0 → 1).

**Prop D1 (SELECT-II geometry change; A2) — PROVED + CHECKED.** With `v(m') = v(m) − v(N) + 2v(N+1)` (v001 Thm 2.1), `k(m') − k(m) ∈ [−ω(N), ω(N+1)]`. The geometry is **not monotone**: `36 → 162 (N=2)` lowers `d_amb` 2 → 1, and `72 → 384 (N=3)` lowers it 2 → 1. Over the 3,124 SELECT-II edges with endpoints ≤ 5000: `Δd_amb` takes values −1:69, 0:962, +1:1890, +2:194, +3:9; `Δd_cell`: −1:48, 0:1666, +1:1218, +2:188, +3:4.

**Cor D2 (C-scope; v001 Cor 3.3).** In an eventual regime `d_amb` and `d_cell` of `x_n` are eventually periodic in n (period dividing P): only the p-axis grows, and `b` is constant.

## 3. Measured structure and conjectures

**M1 (MEASURED / CONJECTURE).** Over 8,203 corpus fibres, `b₁(K_move) = max(0, |G⁺| − k)` on 8,086 and is smaller on 117 (all small fibres, R ≤ 4); it never exceeds it in the corpus. **But the upper bound fails on orbit states**: 9 of 420 tracked C-orbit states have `b₁ > |G⁺| − k` (e.g. the g = 11 orbit from `L = 2·3³·5⁴` at n = 8: R = 4, `|G⁺| = 4`, k = 3, `b₁ = 2 > 1`). So the inequality is false in general; equality in the "saturated" regime (fibre large enough to realise every relation cycle) is the live conjecture. *Heuristic reading (unproved):* `|G⁺| − k` is the rank of the relation lattice among the Graver moves; each relation is a cycle of moves not filled by commutation squares, so `b₁` counts independent such syzygies. Smallest examples: 1600/3 (three points, triangle `(1,1),(2,0),(1,−1)`: `(2,0) = (1,1)+(1,−1)` is a non-conformal sum) and 19600/3 (an unfilled pentagon).
**M2 (MEASURED).** `H_{≥2}(K_move)` is nonzero on **no** corpus fibre (≤ 300 points) but becomes large along G > 1 orbits (g = 11 benchmark: `b₂` = 0, 1, 4, 7, 16, 17 at n = 0, 10, 20, 30, 40, 50 while `b₁` saturates at 8). Not understood; could be a boundary effect of the finite box.
**M3 (MEASURED, a caution).** Topology depends on the cell structure: the *clique complex* of the same move graph is acyclic on the g = 11 orbit at all 15 sampled steps (while `b₁ ≥ 6` for the cubical complex), and is nontrivial on 16 corpus fibres, 13 of them with b = 2, where `Λ = Z^k` and the grid's unfilled 4-cycles are the cause. Neither complex is canonical; any topological claim must name its cell definition.
**M4 (MEASURED).** Dimension triples `(d_amb, d_cell axis, d_cell move)` over the corpus: 17 patterns observed (e.g. `(2,0,0)` 2,538 fibres; `(1,1,1)` 156; `(2,0,2)` 3). All are in `output/verify_full.json`.

## 4. Open problems

1. Prove or refute M1 (equality of `b₁` with the Graver relation rank in a saturated regime) and characterise the 117 deficits and 9 excesses.
2. Explain `H₂` growth along orbits; compute exact `b₂(n)` growth law.
3. Does `b₁(K_move(x_n))` become eventually constant along every persistent G > 1 orbit? (Over steps 45–59, `b₁` is constant in 5 of the 6 G > 1 orbits tracked and still increasing in one, g = 19.)
4. GEO-T4 beyond data: a theorem relating a topological invariant of `K_move` to the eventual `(P, s, p)` of the C-orbit — none found.
5. Composite/even g (open problem O12.2 of Vol. II): whether the non-cyclic structure of `(Z/g)^×` shows up in `Λ_g` and `G_x` was **not** tested here.

## 5. Previous-work comparison (references from memory; not re-verified in this session)

* Graver bases / conformal decomposition: J. E. Graver, *On the foundations of linear and integer linear programming I*, Math. Programming 9 (1975); B. Sturmfels, *Gröbner Bases and Convex Polytopes*, AMS 1996; R. Hemmecke, *On the positive sum property and the computation of Graver test sets*, Math. Programming 96 (2003). Software: 4ti2.
* Markov bases and fibre connectivity: P. Diaconis, B. Sturmfels, *Algebraic algorithms for sampling from conditional distributions*, Ann. Statist. 26 (1998).
* Cubical homology: T. Kaczynski, K. Mischaikow, M. Mrozek, *Computational Homology*, Springer 2004.
**Assessment.** Thm B is, up to the origin lemma, an instance of known Graver/Markov-basis theory; Prop 1–2 and Thm A are elementary. What is specific to UNNS is the identification of the occurrence fibre with `B ∩ ker χ_b`, the exact classification of its coordinate complex, and the data on K_move and its behaviour under SELECT-II and C. No priority claim is made.
