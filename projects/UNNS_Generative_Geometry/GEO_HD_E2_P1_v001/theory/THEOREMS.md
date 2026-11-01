# E2-P1 — Results, with proofs

Labels: **[P]** proved by hand here; **[C]** exact finite computation (certificate id); **[I]** inherited and cited. Notation as in `DEFINITIONS.md`. "Prior art" lines state what was searched (Vol. I/II, FIELD-I v001–v012, GEO-I v002–v012, Papers A/B) — no priority claim is made for elementary statements.

---
## Theorem E2-1 (the three-stage orbit; all k, all primes) **[P]** (+[C] C01–C02, C22–C23)
Let `k ≥ 2`, `p₁ = 2 < p₂ < … < p_k` distinct primes with `pᵢ ≡ 2 (mod 3)`, `P = ∏pᵢ`, `x₀ = P⁴/3`. Then
`L(x₀) = P²`, `G(x₀) = 3`, `x₁ = C(x₀) = 2P⁴/3`, `x₂ = C(x₁) = P⁴`, and

| | x₀ | x₁ | x₂ |
|---|---|---|---|
| reduced denominator b | 3 | 3 | 1 |
| box q | (2,…,2) | (2,…,2) | (2,…,2) |
| fibre size | (3ᵏ−1)/2 | (3ᵏ−1)/2 | 3ᵏ−1 |
| relation lattice | even-sum | even-sum | Zᵏ |
| D | D₀ | = D₀ | ⊋ D₀ |

*Proof.* `d² | P⁴ ⇔ d | P²`, so `d = ∏pᵢ^{αᵢ}`, `α ∈ {0,1,2}ᵏ`. Since `pᵢ ≡ −1 (mod 3)`, `d ≡ (−1)^{Σαᵢ}`; hence `D(x₀)` corresponds to the nonzero even-weight vectors, `(3ᵏ+1)/2 − 1` of them. `pᵢ² ∈ D(x₀)` (α = 2eᵢ) and every d divides P², so `L = P²`. Every `d−1` is divisible by 3, and `4 = 2² ∈ D` has `d−1 = 3`, so `G = 3`. Therefore `C(x₀) = P⁴/3 + P⁴/3 = 2P⁴/3`. In `x₁` the numerator `2P⁴` is prime to 3 (b = 3) and `v₂(2P⁴) = 5`, `⌊5/2⌋ = 2`, so the primes, box and (since `d² | 2P⁴ ⇔ d | P²`) the set `D` are unchanged, hence also `L, G`, and `C(x₁) = 2P⁴/3 + P⁴/3 = P⁴`. For `x₂ = P⁴` the denominator is 1, `D(x₂)` is the set of all divisors `≥ 2` of `P²` (`3ᵏ−1` of them), and the lattice is `Zᵏ`. ∎
*Specimen:* `P = 110`, k = 3: 13 → 13 → 26. *Contrast:* for sets `P` without the prime 2 the orbit is different (data C22/C23: 89 of 135 sampled `P` follow other patterns).
*Prior art:* the C-orbit is the Foundations Vol. II construction; this explicit closed form was not found in the sources.

## Lemma E2-2 (lattice order from group orders) **[P]** (+[C] C24, 405 transitions)
For primes `p₁..p_k` and moduli `b, b'`: `[Zᵏ:Λ_b] = |H_b|`; `Λ_b ∩ Λ_{b'} = Λ_{lcm(b,b')}`; therefore `Λ_b ⊆ Λ_{b'} ⇔ |H_{lcm(b,b')}| = |H_b|`. So the relation between consecutive lattices is computable from three group orders, without enumeration.
*Proof.* `χ_b : Zᵏ → H_b` is onto with kernel `Λ_b`. By the Chinese remainder theorem `χ_b(α)=1 ∧ χ_{b'}(α)=1 ⇔ χ_{lcm}(α)=1`. If `Λ_b ⊆ Λ_{b'}` then `Λ_{lcm} = Λ_b`, so the indices agree. Conversely `Λ_{lcm} ⊆ Λ_b` with equal finite index gives equality, so `Λ_b = Λ_{lcm} ⊆ Λ_{b'}`. ∎

## Lemma E2-3 (denominator floor) **[P from [I]]** (+[C] C25)
Along any C-orbit, every denominator divides `G(x₀)`; hence `Λ_{G(x₀)} ⊆ Λ_{b_n}` for all n (fixed coordinates).
*Proof.* Vol. II ch. 1: `b | G(x)` when `D(x) ≠ ∅` (each `d ≡ 1 mod b`), the reduced denominator of `C(x)` divides `G(x)`, and `G(C(x)) | G(x)`. So `b_{n+1} | G_n | G₀` and `b₀ | G₀`. ∎

## Lemma E2-4 (no shrinking) **[P from [I]]** (+[C] C25)
Let `x' = C(x)` with the same primes and box, and suppose `span_Z F_x = Λ_b`. Then `Λ_b ⊆ Λ_{b'}`: the relation is EQUAL or ENLARGE, never SHRINK.
*Proof.* Vol. II Thm 1.3 (F.T31): `D(x) ⊆ D(x')`, so every `α ∈ F_x` has `∏pᵢ^{αᵢ} ≡ 1 (mod b')`, i.e. `F_x ⊆ Λ_{b'}`; take the span. ∎
In the family of Theorem E2-1, `span F = even-sum lattice` (it contains `2eᵢ` and `eᵢ+eⱼ`, hence `eᵢ−eⱼ`), and the hypothesis holds at every sampled step (405/405). All observed transitions are EQUAL (276) or ENLARGE (129); a denominator can change without changing the lattice (e.g. P = {5,17,29}: b = 3 → 12, EQUAL).

## Theorem E2-5 (Graver sets) **[P]**
For `q = (2,…,2)`, `k ≥ 2`: `G(Zᵏ) = {±eᵢ}` and `G(even-sum) = {±2eᵢ} ∪ {±eᵢ±eⱼ (i<j)}`; they are disjoint.
*Proof.* In `Zᵏ` minimality of `eᵢ` is clear and any nonzero vector dominates some `±eᵢ`. In the even-sum lattice: `eᵢ ∉ Λ`, so `2eᵢ` and `eᵢ±eⱼ` have no proper conformal lattice vector below them (the only candidates are `±eᵢ, ±eⱼ`) and are minimal. Conversely let `λ ∈ Λ ∩ [−2,2]ᵏ` be nonzero. If some `|λᵢ| = 2` and λ ≠ ±2eᵢ then `2·sign(λᵢ)eᵢ ⊏ λ` is a lattice vector, so λ is not minimal. If all `|λᵢ| ≤ 1` and the support has ≥ 3 elements (the support size is even), then `±eᵢ±eⱼ ⊏ λ` for two support indices, so λ is not minimal. ∎ (Classical: the D_k root lattice.) Checked by brute force: C03, C05.

## Theorem E2-6 (abstract transport under a lattice change) **[P]** (+[C] C05, C09)
Let `Λ ⊆ Λ'` (or any two lattices) with the same box q, fibres `F, F'`, region Graver sets `G, G'`, complexes `K, K'`.
1. If `Λ ⊆ Λ'` then `F ⊆ F'` (vertices persist; the new vertices are `F' ∖ F`).
2. A j-cell (j ≥ 1) of `K` is a cell of `K'` iff all of its generators lie in `G ∩ G'`.
3. `G ∩ G' = { g ∈ G : g is ⊑-minimal in Λ' }`; if `Λ' = Zᵏ`: `G ∩ G' = { ±eᵢ : eᵢ ∈ Λ }` (the axes with `pᵢ ≡ 1 mod b`).
*Proof.* (1) trivial. (2) A cell is determined by its vertex set, and its generators are the edge vectors at the lex-minimal vertex, an intrinsic property of the convex hull; the same vertex set is a cell of `K'` iff those vectors are in `G'`. (3) is the definition, and for `Λ'=Zᵏ` `G'={±eᵢ}`. ∎
**Corollary (the E2-P1 specimen) [P]:** for stage 1 → 2 (k = 3, all `pᵢ ≡ 2 (mod 3)`, S = ∅): all 13 vertices persist, **no** edge and **no** cell of positive dimension persists as an abstract cell, although `D(x₁) ⊂ D(x₂)`. Counts [C]: edges 45 lost / 51 new; 2-cells 36 / 33; 3-cells 3 / 7. Stage 0 → 1 is the identity.
*Prior art:* GEO-I v002 Prop C (monotone subcomplex, same lattice) and Thm A (axis side) are related; the transport under a lattice change along a C-step was not found.

## Proposition E2-7 (the target union) **[I] + [P]**
For `Λ' = Zᵏ`: `U(x') = Y_q = { x ∈ [0,q] : maxᵢ xᵢ ≥ 1 }` (GEO-I v002 Prop 2), contractible (star-shaped about q). A convex polytope `P ⊆ [0,q]` lies in `U(x')` iff `P ∩ R = ∅`, `R = [0,1)ᵏ`. [C] C14 checks `U(x₂)` = 7 cubes = `Y` on the 1/6-grid.

## Theorem E2-8 (lost edges are geometrically retained) **[P]** (+[C] C16)
Let `Λ` be the even-sum lattice in `Zᵏ` and `K` any box. Every edge segment `[u, u+g]` of `K_abs` (u, u+g ∈ F, g ∈ G) lies in `Y_q ⊆ U(Zᵏ)`.
*Proof.* Suppose `x = u + tg ∈ R`, `0 ≤ t ≤ 1`. Coordinates of `u` and `u+g` are non-negative integers. Where `g_m ≥ 0`, `x_m ≥ u_m`, so `u_m = 0`. For `g = 2eᵢ` or `eᵢ+eⱼ` this forces `u = 0` (every coordinate is zero or fixed below 1): contradiction. For `g = eᵢ − eⱼ`: all coordinates but j vanish, `u = u_j e_j`, `u_j ≥ 1` (because `(u+g)_j ≥ 0`), and evenness gives `u_j ≥ 2`; then `x_j = u_j − t ≥ 1`: contradiction. ∎
So *abstract edge loss does not imply geometric loss*: 45 edges are lost as cells but all 45 segments lie in `U(x₂)`.

## Proposition E2-9 (cells that leave U) **[P for one cell, C for the classification]** (C16–C18)
k = 3, box (2,2,2): the parallelogram `P((0,0,2); (0,1,−1),(1,0,−1))` has corners `(0,0,2),(0,1,1),(1,0,1),(1,1,0) ∈ F`, Graver generators, and contains `(0,0,2) + ⅔(0,1,−1) + ⅔(1,0,−1) = (⅔,⅔,⅔) ∈ R`. Exactly 6 source cells meet `R` (3 two-cells, 3 three-cells), namely those whose corner set contains `T = {(0,1,1),(1,0,1),(1,1,0)}` [C]; all other 33 two-cells and all 13 vertices and 45 edges lie in `Y`. Hence `U(x₁) ⊄ U(x₂)` although `F_{x₁} ⊂ F_{x₂}` (law L2 false), and `U(x₂) ⊄ U(x₁)` ((1,0,0) ∈ U₂ ∖ U₁, C18). Whether "PARTIAL ⇔ T ⊆ corners" extends to other k or boxes is OPEN.

## Finding E2-10 (topology; finite, exact) **[C]** (C06–C08, C11–C15)
| object | stage 0 (= stage 1) | stage 2 |
|---|---|---|
| f-vector of K_abs | (13, 45, 36, 3) | (26, 51, 33, 7) |
| Betti of K_abs (Q) | (1, 6, 6, 0) | (1, 0, 0, 0) |
| U: maximal cells | 15 two-cells + 3 three-cells | 7 cubes |
| Betti of U (nerve, exact LP) | **(1, 0, 18, 0)** | (1, 0, 0, 0) |
| K_abs embedded? | **no** (Prop D witness; first obstruction already at box (2,1,1)) | yes |
The 18 = b₂ of U₀ is a property of the *realization*: the abstract complex has b₂ = 6. Both are far from the target. No general theorem is claimed for these numbers.

## Theorem E2-11 (verdict on the proposed laws) **[P/C]** — see `results/E2_COUNTEREXAMPLES.json`
* **L1** "occurrence-index inclusion ⇒ Graver-edge persistence": **false** (CE-1: all 45 edges lost; Theorem E2-6).
* **L2** "vertex persistence ⇒ `U(x) ⊆ U(C(x))`": **false** (CE-2: Prop E2-9).
* **L3** "abstract loss ⇒ geometric loss": **false** (CE-3: Theorem E2-8).
* **L4** "topology is monotone under index inclusion": **false** (CE-4: b₂(U) 18 → 0 and b₁(K_abs) 6 → 0 while the fibre grows).
* **L5** "a change of denominator changes the lattice": **false** (CE-5).
