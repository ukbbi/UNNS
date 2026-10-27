# GEO-I v003 — Mathematics

Abstract and embedded geometry of the modular-move complex. Proofs, exact hypotheses, and the status of every claim.
Status labels used throughout: **[P]** proved here · **[S]** standard result (cited) · **[C]** exact computation, reproduced by `verify.py` · **[O]** open / observed only.

---

## 0. Setting and conventions

A rational fibre is `x = a/b` in lowest terms. Write `a = ∏ p_i^{2e_i}·(rest)`; the **active primes** are `p_1<…<p_k` with `q_i = ⌊v_{p_i}(a)/2⌋ ≥ 1`. (Same coordinates as v002: `geo2lib.coords`.)

* `r_i = p_i mod b`, `o_i = ord_b(r_i)`, `H = ⟨r_1,…,r_k⟩ ≤ (ℤ/b)^×`.
* `φ : ℤ^k → (ℤ/b)^×`, `α ↦ ∏ r_i^{α_i}`. `Λ = ker φ` is a lattice of index `|H|` in ℤ^k (`Λ = ℤ^k` for `b = 1`).
* Box `B = [0,q_1]×…×[0,q_k]`; occurrence set (the fibre) `F = (Λ ∩ B) \ {0}`.
* **Graver basis** `𝒢` of Λ: the nonzero vectors of Λ that are minimal for the conformal order `h ⊑ g ⇔ h_i g_i ≥ 0 and |h_i| ≤ |g_i| ∀i`. `𝒢 = −𝒢`. The v002 moves are the *region* Graver vectors `𝒢_q = 𝒢 ∩ [−q,q]^k`.
* **`K_abs`** (v002's `K_move`): the abstract cell complex whose `m`-cells are `(u; g_1<…<g_m)`, `g_j ∈ 𝒢_q`, rank `m`, all `2^m` corners `u + Σ_{j∈S} g_j` in `F`. Boundary as in v002.
* **`U_x`** (geometric image): the union in ℝ^k of the closed parallelotopes `P(c) = u + Σ[0,1]g_j`, one per cell `c`. Equivalently the union of the *geometrically maximal* cells (`cover_cells`).
* **`K_emb`**: when it exists, a convex-cell complex with `|K_emb| = U_x`, vertex set `F ∪ A`, where `A` are *auxiliary* vertices (never occurrences; each carries provenance = the segments that create it) and every cell of `K_abs` is a union of cells of `K_emb`. Built exactly in the plane (`subdivision.py`) and certified by `validate_planar`.

A cell complex is **embedded** (we say *valid*) when any two closed cells meet in a common face of both (possibly empty). `K_abs` is closed under taking faces, so it is then a polyhedral complex in the usual sense.

All computation is in exact integers / rationals. LP feasibility for cell–cell intersections is solved in exact rational arithmetic (`geometry/exactlp.py`).

**Refinement of v002 Theorem A.** The cell-dimension formula of Theorem A presupposes a *nonempty* realized fibre. For `F = ∅` the dimension is undefined (we assign no value); none of the statements below concern empty fibres.

---

## 1. Embedded ⇒ abstract and geometric topology agree  (G3-T3 baseline)

**Theorem 1 [S + P].** If `K_abs` is embedded, the canonical map `|K_abs| → U_x` (glue the cells along faces, send each cell to its parallelotope) is a continuous bijection from a compact space onto a Hausdorff space, hence a homeomorphism. Therefore `H_*(K_abs;ℚ) = H_*(U_x;ℚ)` and the cellular Betti numbers computed from the abstract boundary operator are the Betti numbers of the geometric set.

*Proof.* Surjective by definition of `U_x`. Injective because two cells meet only in a common face, which is identified with itself in `|K_abs|`. ∎ This is a standard fact of polyhedral topology; no UNNS arithmetic enters. The content of v003 is **when its hypothesis holds** (§3–§5) and **what replaces it when it fails** (§6).

**Corollary 1 (nerve route) [S].** The maximal cells are convex; every nonempty intersection of convex sets is convex, hence contractible, so by the Nerve Theorem (Borsuk 1948; see Tancer, arXiv:1102.0417, §5.1) `U_x` is homotopy equivalent to the nerve of the maximal-cell cover. `verify.py` uses this as a second, independent exact route to `H_*(U_x)`, and as the only route in dimension ≥ 3 when `K_abs` is not embedded.

---

## 2. Elementary lemmas on Graver segments

**Lemma 0 (box bound) [P].** Every `g ∈ 𝒢` satisfies `|g_i| ≤ o_i`. Consequently `𝒢_q = 𝒢 ∩ [−q,q]^k`, and `𝒢` is computed inside `∏[−o_i,o_i]`.
*Proof.* `o_i e_i ∈ Λ`. If `|g_i| > o_i`, then `g' = g − sgn(g_i) o_i e_i ∈ Λ`, `g' ≠ 0` (else `|g_i| = o_i`), and `g' ⊑ g`, `g' ≠ g` — contradicting minimality. ∎

**Lemma 1 (open Graver segments contain no point of Λ) [P].** For `g ∈ 𝒢`, `u ∈ Λ` and `0 < s < 1`, the point `u + sg` is not in Λ.
*Proof.* If `u+sg ∈ Λ` then `w = sg = (u+sg) − u ∈ Λ`, `w ≠ 0`, `w ⊑ g`, `w ≠ g` — contradiction. ∎

**Lemma 2 (no collinear overlap) [P].** Two distinct Graver edges `[u,u+g]`, `[v,v+h]` that are collinear intersect at most in a common endpoint.
*Proof.* Parallel Graver vectors satisfy `h = ±g` (if `h = cg`, `0<|c|<1`, then `±h ⊑ g`). Overlap of interiors means `v − u = sg` with `0<|s|<1` and `v−u ∈ Λ`, contradicting Lemma 1. ∎

**Lemma 3 (no endpoint on an open edge) [P].** An occurrence `v ∈ F` is never in the open segment `(u, u+g)` of a Graver edge. (Lemma 1 with `v − u = sg`.) ∎

**Lemma 4 (crossing points are not lattice points) [P].** If open Graver segments from `u` (direction `g`) and `r` (direction `h`) meet at `P = u+tg = r+λh`, `0<t,λ<1`, then `P ∉ Λ`. (Else `P − u = tg ∈ Λ`, contradicting Lemma 1.) In particular **a crossing point is never an occurrence**, so auxiliary vertices can always be told apart from occurrences, and a crossing is never a “near miss” of an occurrence.

Consequence: the only *edge–edge* intersection types are: shared endpoint, or a transversal interior-interior crossing at a non-lattice point. (`verify.py` checks all four lemmas on 606 `k=2` and 87 `k=3` fibres in smoke mode and ~10⁴ in full mode; zero violations.)

---

## 3. Arithmetic classification of crossings  (G3-T1)

For independent `g,h ∈ 𝒢` define
`M(g,h) = Λ ∩ span_ℚ(g,h)`, `ι(g,h) = [M(g,h) : ℤg+ℤh]`, and the open-parallelogram set
`Ω(g,h) = Λ ∩ { t g − λ h : 0<t<1, 0<λ<1 }`.

**Theorem T1 [P].**
1. *(crossing criterion)* For `u, u+g, r, r+h ∈ F`, the open Graver segments `(u,u+g)` and `(r,r+h)` cross iff `r − u ∈ Ω(g,h)`. The crossing is then at parameters `(t,λ)` determined by `r−u = tg − λh`.
2. *(counting)* `|Ω(g,h)| = ι(g,h) − 1`.
3. *(formulas)* For `k = 2`: `ι(g,h) = |det(g,h)| / |H|`. For general `k`, `ι(g,h)` divides the gcd of the 2×2 minors of `(g,h)`.
4. In particular, **no crossing is possible between Graver edges `g,h` in any box iff `ι(g,h) = 1`**; and a crossing configuration exists in *some* box iff `ι ≥ 2`.

*Proof.* (1) is the definition of an interior meeting point. (2) The cosets of `ℤg+ℤh` in `M` have unique representatives in the half-open parallelogram `{sg+μh : 0 ≤ s,μ < 1}`. A representative with `s = 0` or `μ = 0` lies on the line of `h` or `g` strictly between lattice points, i.e. is an `s'h` or `s'g` in Λ with `0<s'<1` — impossible by Lemma 1. So the `ι−1` nonzero cosets have representatives with `0<s,μ<1`; substituting `λ = 1−μ` and shifting by `h` identifies them with `Ω(g,h)`. (3) For `k=2`, `M = Λ` and `[ℤ²:ℤg+ℤh] = |det|`, `[ℤ²:Λ]=|H|`. In general `M ⊂ ℤ^k ∩ span` and the index of `ℤg+ℤh` in the saturation is the gcd of the 2×2 minors; ι divides it. (4) follows from (1), (2). ∎

`verify.py`: (i) `ι = |det|/|H|` on every Graver pair for `b < 16` (1088 pairs in smoke); (ii) for each `k=2` and `k=3` fibre in the sweep, the set of crossing edge-pairs **predicted from the `(g,h,Ω)` data alone** equals the set found by the exhaustive edge audit (0 mismatches).

**Worked example (82944/5).** `b=5`, `(p_1,p_2)=(2,3)`, `H=(ℤ/5)^×` (order 4), `o=(4,4)`, `|H|=4≠16`. `g=(4,0)`, `h=(2,−2)` are Graver; `det = −8`, `ι = 8/4 = 2`, `Ω = {(1,1)}`, since `(1,1) = ½·(4,0) − ½·(2,−2)`, i.e. `t=λ=½`. With `u=(1,1)`, `r=(2,2)`, `r−u=(1,1)∈Ω`, so the edges `(1,1)–(5,1)` and `(2,2)–(4,0)` cross at `(3,1) ∉ Λ_5`.

---

## 4. Faithful embedding: sufficient and necessary conditions  (G3-T2, G3-T5)

**Theorem T2(a) (direct-product fibres are embedded, every k) [P].** If `|H| = ∏ o_i` (equivalently, the map `⊕ℤ/o_i → H` is an isomorphism), then `Λ = ⊕ o_iℤ`, `𝒢 = {±o_i e_i}`, and `K_abs` is a scaled cubical complex; it is embedded for every box `q`, every `k`.
*Proof.* `⊕o_iℤ ⊂ Λ` has index `∏o_i`; Λ has index `|H|`, so equality. In a diagonal lattice the conformally minimal vectors are the `±o_ie_i`. The cells are axis-parallel boxes with corners in the grid `∏o_iℤ`; two such boxes meet in a box of the grid whose corners lie in both, i.e. in a common face which is itself a cell. ∎
*Special cases.* `b = 1` (all integers; this recovers v002 Theorem A's embedded coordinate picture); `b` prime with `k=1`; any fibre with `r_i=1` axes appended to a direct-product base.

**Theorem T2(b) (k = 2 is completely classified) [P + C].** For `k=2` the following are equivalent:
(i) `K_abs` has no interior edge crossing for **every** box `q`;
(ii) `K_abs` is embedded for every box; (iii) `|H| = o_1 o_2`.
*Proof.* (iii)⇒(ii) is T2(a); (ii)⇒(i) is trivial. (i)⇒(iii): if `|H| < o_1o_2` then `Λ ⊋ o_1ℤ⊕o_2ℤ`; pick `(a,c) ∈ Λ` reduced mod `(o_1,o_2)` nonzero. If `a=0` then `r_2^c=1` with `0<c<o_2`, impossible; likewise `c≠0`. So `0<a<o_1`, `0<c<o_2`. Take the box `q = (o_1, c+o_2)`, `u=(0,o_2)`, `g=(o_1,0)`, `r=(a,c)`, `h=(0,o_2)`. All four points `u, u+g, r, r+h = (a,c+o_2)` are nonzero points of `Λ∩B`. `g,h` are Graver (a vector `(s,0)∈Λ` needs `o_1|s`). The horizontal segment at height `o_2` from `x=0` to `x=o_1` and the vertical segment at `x=a` from `y=c` to `y=c+o_2` cross at `(a,o_2)`, interior to both since `0<a<o_1`, `c<o_2<c+o_2`. ∎
`verify.py` checks (i)⇔(iii) for every residue pair with `b ≤ 59` (full mode) and that the explicit configuration is a genuine crossing of two Graver edges for **every** non-direct pair with `b ≤ 40`.

**Theorem T2(c) (k ≥ 3: edge-crossing freedom does not imply embedding) [P + C].** Let `b = 8`, `(r_1,r_2,r_3) = (3,5,7)` (the Klein-four class; also `b=12`, `(5,7,11)`). Then `Λ = {α : all α_i have the same parity}`, `𝒢 = {±2e_i} ∪ {(±1,±1,±1)}`, and `ι(g,h)=1` for every independent pair, so **no two Graver edges ever cross in any box** — but `K_abs` is non-embedded as soon as `q ≥ (3,3,2)` coordinatewise (or a permutation of it; enlarging the box only adds cells).
*Proof of `ι = 1`.* Λ is invariant under permuting coordinates and flipping signs, so it suffices to treat one pair of each type: `(2e_1,(1,1,1))`: `span∩Λ = {(m,n,n): m≡n (2)} = ℤ·2e_1 + ℤ·(1,1,1)`; `((1,1,1),(1,1,−1))`: `span∩Λ = {(m,m,n): m≡n (2)}` generated by the two; `((1,1,1),(1,−1,−1))`: similarly. `ι=1` in each case.
*Non-embedding.* See Proposition D below with `g_1=(1,1,1)`, `g_2=(1,1,−1)`, `g_1−g_2 = 2e_3 ∈ 𝒢`. The concrete fibre `x = 3^6·5^6·7^4/8 = 27348890625/8` has `K_abs` with Betti numbers `(1,4,3,0)` and the nerve of its image gives `(1,0,10)`. ∎

**Proposition D (diagonal obstruction) [P].** If a 2-face of a cell has generators `g_i, g_j` with `g_i + g_j ∈ 𝒢` (resp. `g_i − g_j ∈ 𝒢`), then `K_abs` contains the edge along the diagonal `u→u+g_i+g_j` (resp. `u+g_j → u+g_i`) — both ends are corners of the face, hence in `F` — and that edge meets the 2-cell in a set which is not a common face of both. So `K_abs` is non-embedded. (In `82944/5` both diagonals of the unique 2-cell are edges; they cross each other.)

**Genuine 3-D crossings [C].** `b=5`, residues `(2,2,3)`, box `(3,3,3)`, `g=(1,0,−3)`, `h=(1,2,−1)`: concrete fibre `x = 5489031744/5` (primes 2,3,7). The two edges cross at a point whose plane is not a coordinate plane; `K_abs` has Betti `(1,12,6,0)`, the nerve of the image `(1,0,0)`.

**Proposition P5 (axes with `r_i = 1` persist crossings) [P + C].** Appending an active prime `p ≡ 1 (mod b)` (so `o=1`) replaces `Λ` by `Λ×ℤ`, adds `±e_{k+1}` to `𝒢`, and leaves every old Graver edge (zero last coordinate) an edge of the new complex: all crossings of the base fibre survive in the slice `α_{k+1}=0`. Hence crossings are not “planar accidents”: they persist into every higher dimension that adds a unit axis.

---

## 5. Higher-dimensional picture  (G3-T5, E10)

* **Preservation of v002 cells.** `3600` (3-cell, f-vector 11/17/8/1), `210⁴` (4-cell, 80/212/210/92/15) and `44100` (no 4-cell, 15/28/18/4) have `b = 1`, hence direct product, hence embedded (T2(a)); their cell counts equal v002's and every pair of maximal cells meets in a common face `[C]`.
* **E10 surveys.** All `k=3` fibres for `b∈{3,4,5,7}` in three boxes and a set of `k=4` fibres are classified exactly (`EMBEDDED`, `NON_EMBEDDED_EDGE_CROSSING`, `NON_EMBEDDED_CELL_ONLY`, or reported `UNRESOLVED`). Every direct-product fibre is embedded (T2(a)); many non-direct fibres are not; edge crossings occur in 3-D and 4-D in planes that are **not** coordinate planes. The phenomenon is therefore genuinely higher-dimensional, not a planar artifact.

---

## 6. When the abstract complex is not embedded  (G3-T4, T3)

**Graph identity (P3) [P + C].** Let `G` be the 1-skeleton of `K_abs` (connected by v002 Theorem B) and `G'` the planar/space arrangement obtained by subdividing every edge at the crossing points. By Lemmas 2–4 crossings are isolated transversal points; at a crossing point `p` through which `m_p` edges pass, subdividing adds one vertex and `m_p` edges. Euler characteristic gives
`β_1(G') = β_1(G) + Σ_p (m_p − 1)`, and `β_0` is unchanged because `G` is connected. Hence **every crossing adds a 1-cycle to the geometric 1-skeleton that the abstract graph does not have**, and the amount is counted exactly by the crossing multiplicities.

**Proposition P2 (planar sets have no 2-homology) [S/P].** For a finite polyhedral set `X ⊂ ℝ²`, `H_2(X;ℚ) = 0`. *Sketch.* Take a nonzero 2-chain `z` with `∂z=0`; the union `W` of the closed faces with nonzero coefficient is compact and nonempty, so some edge `e` lies on the topological boundary of `W`. An edge of a planar subdivision lies on at most two faces, on opposite sides; the face on the other side of `e` has coefficient 0, so the coefficient of `e` in `∂z` is `±c ≠ 0`. Contradiction. ∎ Hence **for every `k=2` fibre `β_2(U_x) = 0`** (also checked on every planar subdivision computed).

**Theorem T4 [P + C] (unavoidable topological change; infinite family).** Let `x_t = 2^{10+2t}·3^4/5`, `t ≥ 0` (`b=5`, `p=(2,3)`, `q=(5+t,2)`).
1. *(P1)* For every `t`, the four points `(1,1),(2,2),(4,0),(5,1)` lie in `F`, `g=(4,0)`, `h=(2,−2)` are Graver, and the edges `(1,1)–(5,1)`, `(2,2)–(4,0)` cross at `(3,1) ∉ Λ_5` (`t=λ=½`). So **every `x_t` is non-embedded** — an infinite family of distinct rational fibres (G3-P1).
 *Proof.* `2^4 = 16 ≡ 1`, `2^2·3^{−2} = 4·4^{−1} = 1 (mod 5)`; no proper conformal sub-vector of `(4,0)` or `(2,−2)` lies in Λ (direct check of the finitely many candidates). All four points have `α_1 ≤ 5 ≤ q_1`, `α_2 ≤ 2 = q_2`. ∎
2. *(P2)* Here `3 ≡ 2³ (mod 5)` and `2` has order 4, so `Λ = {α : α_1 ≡ α_2 (mod 4)}`, the region Graver set is `±(1,1), ±(3,−1), ±(2,−2), ±(4,0)`, and for `q_2=2` the fibre has exactly the rows `α_2 = 0,1,2` with `α_1 ≡ 0,1,2 (mod 4)`. For each cell type (generator set) and each row, the number of admissible base points `u` is the number of terms of an arithmetic progression of step 4 in an interval whose right end moves with `q_1`; so for `q_1` beyond an explicit threshold **each (type,row) count grows by exactly 1 when `q_1` grows by 4**. Hence the numbers of points/edges/squares grow by constants per period, and `verify.py` evaluates them: `(3, 8, 6)` for every period in the range tested, so `χ(K_abs)` grows by `3−8+6 = 1` per period. Since `K_abs` has dimension 2, `β_2(K_abs) = χ − 1 + β_1 ≥ χ − 1 → ∞`. *(Linear growth: [P]; the constants (3,8,6): [C] — they are read off a finite computation after the threshold.)*
3. By P2 (§6), `β_2(U_{x_t}) = 0` for all `t`. Hence **`β_2(K_abs) − β_2(U_{x_t})` is unbounded**; the exact computation gives `β_1(K_abs)=2`, `β_2(K_abs)=⌊t/4⌋` and `H_*(U)` = `(1,0,0)` for `t ≤ 24`.
The exact values `β_1(K_abs)=2`, `β_2(K_abs)=⌊t/4⌋` are computed for the tested range; the **unbounded growth** of `β_2` does not depend on them — it follows from the χ-growth above and `β_1 ≥ 0`.

**Theorem T3 (homology agreement) [P].** (a) If `K_abs` is embedded then `H_*(K_abs) = H_*(U_x)` (Theorem 1). (b) If `K_abs` is non-embedded, agreement of Betti numbers is *accidental*: it can hold (a diagonal inside a 2-cell may change nothing) or fail (E1, every `k=2` crossing case in the scan, the g=11 orbit). In particular **a crossing of two edges in a plane always changes `β_1` of the 1-skeleton** (P3), but the 2-cells can fill in the new cycle, so the *total* `β_1(U)` can differ from `β_1(K_abs)` in either direction relative to the abstract complex.

**Mechanism table `[C]`** (exhaustive `k=2`, `b ≤ 9`, `q ≤ 5` mechanism scan): every non-embedded fibre but one fails through (i) an interior edge crossing, (ii) a Graver diagonal inside a 2-cell, or both; one fibre (`b=5`, residues `(2,3)`, `q=(4,4)`) fails by an edge passing through the interior of a 2-cell *without* being a diagonal of it and without an edge crossing. That third mechanism is **not explained by Proposition D or Theorem T1** — see O2.

---

## 7. Relation to the v002 findings (H1–H4)

| Hypothesis | Status | Evidence |
|---|---|---|
| **H1** Abstract and embedded topology generally agree | **False** (as a general statement) | E1; T4; every crossing fibre in the `k=2` scan changes some Betti number of `U_x`; g=11 orbit |
| **H2** Crossing behaviour is controlled by modular arithmetic | **True**, and *fully classified for `k=2`* (T2(b)); for `k≥3` crossing configurations are exactly governed by `ι(g,h)` (T1), but embedding is also governed by *cell* obstructions (Prop D, Klein-four) not visible in edge data | T1, T2 |
| **H3** Higher-dimensional modular geometry has stable topological patterns | **Partly**: embedded fibres keep their homology under every realization (Thm 1); the *saturation of `β_1` and growth of `β_2`* in `K_abs` disappear in `U_x` (planar `β_2=0`), so those patterns are properties of the attachment rule | T3, T4, E9 |
| **H4** Nontrivial move homology reflects arithmetic rather than arbitrary attachments | **Largely refuted for the v002 headline invariants**, with a caveat: the invariants of `K_abs` are exact and reproducible but are *not* topological invariants of the point set `F`, and the topology of `U_x` depends on the parallelotope-cell model (the clique complex of the same moves gives different groups) | T4; E1 clique `(1,0,0)`; E7/E8 |

What survives: the connectivity theorem (v002 Theorem B), the certified 3-/4-cells, and — new — the fact that for **direct-product fibres and for every integer fibre** the combinatorics is geometrically rigid.

---

## 8. Open problems (explicitly *not* claimed)

* **O1.** For `k=2` and `q_i > o_i` for both `i`, is `U_x` always acyclic? (Observed in the scan; `b_1(U)>0` occurs only on thin sets of boxes such as `b=7`, residues `(3,5)`, `q_1=6` or `q_2=6`.) Unproved.
* **O2.** The non-diagonal “edge through a 2-cell” mechanism (§6): an arithmetic criterion is not known.
* **O3.** For `k≥3`, a complete classification of embedded fibres beyond the direct-product and Klein-four families.
* **O4.** Whether `K_abs` has a canonical *regular* embedded refinement in dimension ≥ 3 (the planar subdivision is exact only for `k=2`; for `k≥3` the nerve gives the homology of `U_x` but no explicit `K_emb`).
* **O5.** The literature check is incomplete: results on lattice Graver bases are cited (Graver 1975; Sturmfels 1996); no source was found for crossing-free-Graver-edge criteria or for the modular fibre complex itself, which is not a statement that none exists (see `PRIOR_ART.md`).
