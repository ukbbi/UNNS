# A5-T3 — Arithmetic criterion for realised moves to appear or disappear

Notation. For a state `x` with occurrence set `D=D(x)`, an occurrence `d` corresponds to the fibre point `α` (exponent vector of d). The origin `0` corresponds to `1`. K(x)=K_move(x) is the frozen GEO-I move complex.

## Theorem A5-T3.1 (divisor-interval rule) — PROVED
Two occurrences `u≠v` in `D` are joined by an edge of `K_move` **iff the divisor interval `[gcd(u,v), lcm(u,v)]` contains no element of `D∪{1}` other than u and v.**
*Proof.* (1) The exponent-box of `e(u),e(v)` is `{w : gcd(u,v) | w | lcm(u,v)}` (componentwise min/max of valuations). (2) For `u,v∈F` the vector `g=v−u` is region-Graver (conformally minimal in Λ_b) iff the hull box contains no point of `F∪{0}` other than u,v: a lattice point `u+h` with `0≠h⊑g`, `h≠g` lies in the hull box ⊂ B and in Λ_b, hence in `F∪{0}`; conversely a point of `F∪{0}` in the hull box gives such an h. (3) `F` ↔ `D` bijectively, `0` ↔ `1`. ∎ (This is v003 R3-T1a transcribed to divisors.)
**Definition (K(D) for arbitrary D⊂ℕ≥2).** vertices D; edges by the rule; cells = parallelotopes `P(u;g₁..g_j)` (lex-positive, linearly independent generators) with all 2^j vertices in D and **all 1-faces edges**. For occurrence sets of states this equals the frozen move complex — *intrinsic-Graver lemma*: for `g∈Graver(Λ_b)` every pair `(v,v+g)` inside F is an edge, so “generators are moves” and “all 1-faces are edges” coincide. **FINITE-EXACT**: identical cell vectors and Betti numbers (GF(2) and GF(2³¹−1)) to the frozen engine on 1,722 + 61 states (towers, orbits ℓ=5,7,11,13, activation family) and an independent vector/box implementation (Z3). Consequence: **the whole topology of K_move(x) is a function of D(x) alone**; b enters only through which D occurs.

## Corollaries (PROVED)
* **Coprime non-adjacency.** `gcd(u,v)=1 ⇒ 1∈[gcd,lcm]` ⇒ no edge. So K(D) lies in the “gcd>1 graph” on D.
* **Comparable pairs.** If `u|v`: edge ⇔ u,v consecutive in the divisibility order of D∪{1}.
* **Positive-primitive moves** = divisibility-minimal elements of D.

## Theorem A5-T3.2 (transition law for a growth D⊆D′) — PROVED
Let `N=D′∖D` (the new occurrences, e.g. from the stage sieve). Then
1. **Non-edges persist.** (They are blocked by a point of D∪{1}⊂D′∪{1}.)
2. **An old edge {u,v} dies ⇔ some w∈N lies in its divisor interval** (`gcd(u,v)|w|lcm(u,v)`).
3. **Every new edge and every new cell contains a new vertex.** (Old–old edges of K(D′) are old edges by 1.)
4. **A cell dies ⇔ one of its edges dies** (definition via 1-faces), and by the intrinsic-Graver lemma all g-parallel edges of a cell die together (**parallel-edge rigidity**, states only).
5. **K°=K(D)∩K(D′)=K(D)∖Dead is a subcomplex of both**; K′=K°∪New.
6. **Move level.** A realised move `g=e(v)−e(u)` (a ratio v/u) disappears iff *every* pair realising it is pierced; it can appear only through a pair containing a new vertex. Vertex activation (N≠∅) is therefore necessary for every move change, edge loss needs a *piercing* new occurrence, and a new 2-cell needs a new vertex with new edges closing a parallelogram: the three effects are separable and each has an arithmetic test (membership of N in an interval; Q-divisibility of `Y_τ`).
**Finite-exact audit (Z4):** all five statements verified on every one of 2,576 D-events (ℓ=5,7,11,13; S<1500; 24 steps) — 0 violations.

## Corollary A5-T3.3 — event localisation (PROVED)
At a stage end `τ`, `N={d∉D₀: Q(d)|Y_τ}` and `Dead_1={ {u,v}∈E(K(D₀)) : ∃d∈N, gcd(u,v)|d|lcm(u,v)}`. Both are evaluated from the **old** complex and the congruence data of the stage; the new complex is not built.

## Reading the v004 phenomena in this language
* “Activation without topological change” (80 of 474) is not exceptional: **every** D-event changes the complex (a vertex is added), so Type I (no change at all) never occurs among D-events; whether *Betti numbers* change depends on the cells attached (HOMOLOGY_UPDATES.md).
* “Primitivity and K_move topology are not persistent” = old edges can be pierced (2.). Persistence of occurrence vertices (Lemma M) and non-persistence of edges are the same fact seen at two levels.
* Dormant Graver relations (primitive in Λ_b but with no realising pair) are *not* a function of D; they depend on b and the box. This release treats **realised** moves only.
