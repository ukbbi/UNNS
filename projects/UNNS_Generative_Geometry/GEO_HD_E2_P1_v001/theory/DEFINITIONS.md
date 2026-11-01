# E2-P1 — Definitions (scope-locked)

Spec: GEO_HD_1_SPEC_v003 (HD-H0/H1, criterion C3). Scope tags follow GEO-I: **A0** occurrence arithmetic, **C** the FIELD-I collective map. SELECT-II is not used in this package.

## 1. Arithmetic objects (kept distinct)
* **State.** A positive rational `x = a/b` in lowest terms.
* **Occurrence indices.** `D(x) = { d ≥ 2 : d² | a, d ≡ 1 (mod b) }` (Vol. I Thm 1.2). Occurrences are the pairs `(N,M)=(d−1, a(d−1)/(b d²))` with `M(N+1)²/N = x`.
* **Collective map (scope C).** `L = lcm D(x)`, `G = gcd{ d−1 : d ∈ D(x) }`, `C(x) = x + L²/G` (defined when `D(x) ≠ ∅`). Never identified with a SELECT-II edge.
* **Orbit.** `x_0 = 110⁴/3`, `x_{n+1} = C(x_n)`. Stages: **0** = x₀, **1** = x₁, **2** = x₂.

## 2. Fibre in exponent coordinates (GEO-I v002 §1)
For `a = ∏ pᵢ^{eᵢ}` keep the primes with `qᵢ = ⌊eᵢ/2⌋ ≥ 1`; box `B = ∏ {0..qᵢ}`. Character `χ_b(α) = ∏ pᵢ^{αᵢ} mod b` (negative exponents through inverses; `gcd(a,b)=1`). **Relation lattice** `Λ_b = ker χ_b ⊂ Zᵏ`, index `[Zᵏ:Λ_b] = |H_b|`, `H_b = ⟨p₁,…,p_k⟩ ⊆ (Z/b)^×`. **Fibre** `F_x = (Λ_b ∩ B) ∖ {0}`; the map `α ↦ ∏ pᵢ^{αᵢ}` is a bijection `F_x → D(x)`.

## 3. Moves and cells (GEO-I v002 §1, v003/v004 §0)
* **Conformal order** `g ⊑ h` iff `gᵢhᵢ ≥ 0` and `|gᵢ| ≤ |hᵢ|` for all i.
* **Region Graver set** `G_x` = the ⊑-minimal nonzero vectors of `Λ_b ∩ [−q,q]`. `oriented(G)` keeps one of each ± pair (lex-positive).
* **Cell.** For lex-positive, independent `g₁<…<g_j` in `oriented(G_x)` and a base `u`, `P(u; g₁..g_j)` has the `2^j` corners `u + Σ_{i∈S} gᵢ`; it is a j-cell if all corners lie in `F_x`. A cell is determined by its vertex set (base = lex-minimal vertex; generators = edge vectors from it).
* **K_abs(x)** — the (face-closed) abstract complex of all cells, with the boundary `∂P = Σᵢ(−1)^{i−1}[P(u+gᵢ; ĝᵢ) − P(u; ĝᵢ)]`; `∂∂ = 0` is checked.
* **U(x)** — the union in R³ of the closed parallelotopes (the *geometric image*).
* **K_emb** — the exact subdivision of U when K_abs is embedded (any two closed cells meet in a common face). Not constructed here in dimension 3.
* K_abs, U, K_emb are three different objects; **every topological statement names its object**.

## 4. Transport notions (this package)
For a step `x → x'` with the same primes and box:
* **Vertex persistence:** `F_x ⊆ F_{x'}` (identity on exponent vectors).
* **Move survival:** `G_x ∩ G_{x'}`.
* **Abstract cell status:** PRESERVED (the same vertex set is a cell of K_abs(x')), LOST (a cell of K_abs(x) that is not one of K_abs(x')), NEW (a cell of K_abs(x') not in K_abs(x)).
* **Geometric status of a source cell P w.r.t. U(x'):** CONTAINED (`P ⊆ U(x')`) or PARTIAL (`P ⊄ U(x')`).
* **Lattice relation** between `Λ_b` and `Λ_{b'}` on `[−q,q]ᵏ`: EQUAL, ENLARGE (`Λ_b ⊊ Λ_{b'}`), SHRINK, INCOMPARABLE, or COORDINATES_CHANGE (primes/box differ: out of scope).
* **Corner region** `R = {x ∈ Rᵏ : xᵢ < 1 ∀i}` and `Y_q = {x ∈ [0,q] : maxᵢ xᵢ ≥ 1}`.

## 5. Gates
| gate | meaning |
|---|---|
| EXACT_PASS | all declared computations and certificates verify (`RUN_VERIFY.py`) |
| THEOREM_PASS | a new general result is rigorously established beyond the frozen baseline |
| COUNTEREXAMPLE | a proposed general law is falsified with an exact witness |
| OPEN | exact evidence, no general theorem |
| UNAVAILABLE | a required computation could not be completed |

Exact arithmetic only (int / Fraction). Cross-reference to inherited statuses: PROVED, PROVED+CHECKED, CHECKED, CONJECTURE, OPEN as in the GEO-I and Foundations registries.
