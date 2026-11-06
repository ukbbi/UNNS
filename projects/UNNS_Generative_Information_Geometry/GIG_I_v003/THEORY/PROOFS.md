# GIG-I v003 — Proofs

Conventions: ranks 0..k-1 index the labels of the content C; R(I)=∏_{r∈I}(c_r+1)²/c_r; D(I)=denominator of R(I); P_k = permutohedron, faces = ordered set partitions.

## Lemma F (feasible-family law) — PROVED
Let x be an integer and N a label. Then N | x ⇔ x·R(N) = x(N+1)²/N ∈ ℤ, because gcd(N, (N+1)²) = 1.
Let w = (r_1,…,r_k), I_j = {r_1..r_j}. The state after j steps (if all were applicable) is m·R(I_j), which depends on I_j only.
Induction on j: step j+1 is applicable from the integer state m·R(I_j) ⇔ m·R(I_{j+1}) ∈ ℤ. Hence w is admissible ⇔ m·R(I_j) ∈ ℤ for all j.
Finally m·R(I) ∈ ℤ ⇔ D(I) | m (write R(I)=a/D, gcd(a,D)=1; D | m·a ⇔ D | m). So K(w)=lcm_j D(I_j). ∎

## T16 (ordered-block factorization) — PROVED
Let F=(B_1|…|B_r) and let w=π_1…π_r be a vertex of F (π_i an ordering of B_i). The prefix sets of w are B_<i ∪ U with U a prefix set of π_i (U ≠ ∅; the prefix
B_<i ∪ ∅ = B_≤(i-1) is already the last prefix set of π_{i-1}, resp. ∅ for i=1). By Lemma F, w is admissible from m ⇔ for every i and every nonempty prefix set U of π_i:
m·R(B_<i)·R(U) = s_i·R(U) ∈ ℤ. This is a condition on π_i alone, with the formal entry state s_i (a rational number depending only on m and the *set* B_<i, never on the order chosen inside earlier blocks).
Therefore V(F) ∩ A_C(m) = E_1 × … × E_r. ∎
*Corollaries.* (a) F ∈ X_C(m) ⇔ each E_i is all of S_{B_i} ⇔ for every i every U ⊆ B_i has s_i·R(U) ∈ ℤ, i.e. every Boolean interval [B_<i, B_≤i] ⊆ 𝔉_C(m).
(b) |V(F)∩A_C(m)| = ∏|E_i|; in particular a cube (2,2,2) meets A_C(m) in a *coordinate box* (this recovers v002's T11 and shows why Petrie slices cannot occur).
(c) No counterexample can exist (the statement is an identity). Tested anyway: E9 (993,300 face–source pairs, 0 violations).

## T17 (exact face thresholds) — PROVED
F ∈ X_C(m) ⇔ all vertices admissible ⇔ for every vertex w and every prefix set I of w: D(I) | m. The set of all prefix sets of vertices of F is exactly Pref(F):
a prefix set of a vertex is B_<i ∪ U (U ⊆ B_i nonempty), and conversely every nonempty U ⊆ B_i is the prefix set of the ordering of B_i that lists U first (then the rest), completed by any orderings of the other blocks.
So F ∈ X_C(m) ⇔ lcm{D(I): I∈Pref(F)} | m, and this lcm equals lcm_w K(w) = K_F. Monotonicity: F′ ⊆ F ⇒ V(F′) ⊆ V(F) ⇒ K_{F′} | K_F. ∎
The closed form is evaluated, never assumed: E9 compares it with the lcm of vertex thresholds on 201,369 face–content pairs (0 violations).

## T18 (divisibility filtration) — PROVED
m | m′ and D(I) | m ⇒ D(I) | m′, so A_C(m) ⊆ A_C(m′) and the full subcomplexes are nested. F ∈ X_C(m) ⇔ K_F | m ⇔ v_q(K_F) ≤ v_q(m) for every prime q ⇔ b(F) ≤ v(m) (primes not dividing K_F impose nothing).
For nested complexes X ⊆ X′ over GF(2), rank–nullity gives β_j = f_j − ρ_j − ρ_{j+1} for each, hence Δβ_j = Δf_j − Δρ_j − Δρ_{j+1} (all deltas X′−X). Inclusion and the identity are *checked on every reported cover* (E11). ∎

## T19 (third-boundary-rank obstruction) — PROVED
By v002 T15 (realizable, distinct labels, k ≤ 8) the uncoloured graph determines the 2-skeleton, hence f₀,f₁,f₂, ρ₁ and ρ₂ (ρ₂ is the rank of the 2-face/edge incidence matrix). By rank–nullity β₂ = f₂ − ρ₂ − ρ₃ for each complex, so for isomorphic graphs β₂(X) − β₂(Y) = ρ₃(Y) − ρ₃(X). ∎ (It follows that the missing information is the *rank* of the third boundary map; two complexes can have equal f₃ and different ρ₃, and equal ρ₃ with different f₃.)

## T20 — graph-only reconstruction of 3-cells and higher faces
**T20a (completeness) — PROVED.** Let F be a face of P_k with V(F) ⊆ A. Two vertices of F that differ by a swap of adjacent positions differ inside a block, so the induced subgraph G_A[V(F)] is the face graph ∏ Cay(S_{|B_i|}).
Distance in the swap graph of P_k is the Kendall-tau distance (number of label pairs ordered differently), and a path is a geodesic iff each step swaps a pair that is inverted relative to the target. For u,v ∈ V(F) only pairs inside a block are inverted, so every P_k-geodesic from u to v stays in V(F) ⊆ A; hence d_A(u,v)=d_P(u,v) and every G_A-geodesic is a P_k-geodesic, so lies in V(F). Thus V(F) is convex in G_A. ∎

**T20b (soundness in full P_k) — PROVED (finite verification).** P_k's swap graph is vertex-transitive (relabeling the labels is an automorphism). Let 𝒫 be the face graph of a type. By T20a (A=all arrangements) every face of that type is a convex induced copy of 𝒫; copies through a fixed root number n_faces·|𝒫|/k! if they are exactly the faces. E12 enumerates all induced copies of 𝒫 through the root exhaustively (backtracking with complete adjacency/non-adjacency checks) and tests convexity; the counts agree for **every** face type of dimension ≥ 3 with k ≤ 7 and for the three 3-face types with k = 8. (At k = 8 the type (3,2) has 32 induced copies through the root of which 20 are convex: the 12 extra are Petrie prisms, rejected by convexity.) Hence in P_k the convex induced copies are exactly the faces.
*Extension to P_k-convex sets A (k ≤ 7).* If A is geodesically convex in P_k then G_A distances equal P_k distances; a set S ⊆ A convex in G_A is therefore convex in P_k (a P_k-geodesic between points of S lies in A and is a G_A-geodesic, hence in S), and G_A[S]=P_k[S]. So the convex induced copies in G_A are the faces of P_k contained in A. ∎

**T20c — FINITE-EXACT.** For each set in the domains of E12 the graph-derived cells (dimension 0…k−1) equal the true cells as vertex sets; see RESULTS.

**T20d — OPEN, and exactly where the gap is.** For a non-convex realizable set A, a subset S ⊆ A can be convex in the *sparser* graph G_A (geodesics are longer, because shortcuts leave A) without being convex in P_k. T20a is proved; what is missing is a proof that such an S that is also an induced copy of a face graph is a face. Everything reported in E12/E14 is consistent with this; no counterexample was found. A failure of soundness would break *recognition* but would not by itself produce two complexes with isomorphic graphs and different J₃: T20d is a sufficient route to the graph-determination of J₃, not a necessary one.

**Conditional corollary (PROVED given T20d for a domain 𝒟):** J₃ = ρ₃, f₃, D₃ and every β_j are functions of G(X) on 𝒟, so A₃ ≡ 0 on 𝒟 and GIG-Q3 has a negative answer on 𝒟. T20b gives this unconditionally for P_k-convex sets.

## T21a — PROVED
f₂, ρ₂, ρ₃ are computed from faces of dimension ≤ 3 (∂₃ maps 3-faces to 2-faces), so β₂ = f₂ − ρ₂ − ρ₃ depends only on them. For a cover X ⊂ X′ with no new 2-face: Δf₂ = 0 and ρ₂ is unchanged (the set of rows is unchanged; extra edges add zero columns), so Δβ₂ = −Δρ₃ ≤ 0 (added 3-faces can only enlarge the row space). ∎

## T21b — anchor obstruction (A: content (2,3,4,5,8,9); B: (2,3,6,7,8,9))
Let (z, φ) be the certificate of CERTIFICATES/H2_anchor_{A,B}.json (z: 96 faces = 64 squares + 32 hexagons on 130 arrangements; φ: the six hexagons (2,4,5 | σ) with σ a permutation of {0,1,3}, in rank coordinates — identical for A and B).
1. z is a cycle (∂₂z = 0, checked).
2. **φ(∂F) = 0 for every 3-face F of P_6 except six**: the truncated octahedra ({0,2,4,5}|1|3), ({0,2,4,5}|3|1), ({1,2,4,5}|0|3), ({1,2,4,5}|3|0), ({2,3,4,5}|0|1), ({2,3,4,5}|1|0). (Finite check over all 540 3-faces, E10.)
3. For these six, K_F = 288·2, 288·3, 288·5 for A and 432·2, 432·3, 432·7 for B (T17).
4. Hence if 288 | m (so z ⊂ X(m)) and none of the six lies in X(m), i.e. gcd(m/288,30)=1, then φ∘∂₃ = 0 on C₃(X(m)) and φ(z)=1, so z ∉ im ∂₃: [z] ≠ 0. (Same for B with 432 and 42.) PROVED.
5. If 288·p | m for p ∈ {2,3,5} then z = ∂c with an explicit verified 3-chain c of 34 / 52 / 126 faces (E11 fillings; verified by recomputing ∂₃c = z). FINITE-EXACT.
6. β₂ of every regime of the content is computed (55 and 59 regimes): β₂ > 0 only at the single regimes 288 / 432. FINITE-EXACT; the arithmetic predicate "A(m) equals the anchor's arrangement set" ⇔ "288 | m and gcd(m/288,30)=1" was also verified for all m ≤ 40000.

## Limits of what is claimed
No statement above is asserted for contents with k > 7 beyond what is explicitly marked; T20d and T21c remain open; A₃ is a domain-relative quantity.
