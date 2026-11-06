# GIG-I v003 — Definitions (additions to v001/v002; the earlier definitions are unchanged)

Status tags: **[PROVED]** complete argument in PROOFS.md · **[FINITE-EXACT]** exact computation over a stated finite domain ·
**[BOUNDED-NEGATIVE]** exhaustive search of a stated domain found nothing · **[CAND]** supported but not proved · **[OPEN]**.

**D-V1 Content, rank coordinates.** A content is a set C = {c_0 < … < c_{k-1}} of distinct positive integers. A label is addressed by its rank r ∈ {0..k-1};
an *arrangement* is a permutation of the ranks (the order in which the labels are applied).

**D-V2 SELECT-II step.** From an integer state x, label N is applicable iff N | x; the new state is x·R(N), R(N) = (N+1)²/N.
For a set I of ranks put R(I) = ∏_{r∈I} R(c_r) (a rational number; R(∅)=1).

**D-V3 Set threshold.** D(I) = the denominator of R(I) in lowest terms (D(∅)=1).
For an arrangement w with prefix sets I_1 ⊂ I_2 ⊂ … ⊂ I_k: K(w) = lcm_j D(I_j) (equal to v001/v002's threshold, see Lemma F).

**D-V4 Admissible set, history complex.** A_C(m) = { w : K(w) | m }. X_C(m) is the full subcomplex of the permutohedron P_k (v001) spanned by A_C(m):
a face is present iff all its vertices are admissible. Realizable/regime language as in v002 (D-T7…); **the family of all A_C(m) includes ∅** (see CORRECTIONS/V002_T12_SCOPE.md).

**D-V5 Feasible family.** 𝔉_C(m) = { I ⊆ ranks : D(I) | m } (equivalently m·R(I) ∈ ℤ).

**D-V6 Faces and blocks.** A face of P_k is an ordered set partition F = (B_1 | … | B_r) of the ranks; its vertices are the concatenations π_1…π_r
with π_i an ordering of B_i; dim F = Σ(|B_i| − 1). The *combinatorial type* is the multiset of block sizes > 1:
(2)=edge, (2,2)=square, (3)=hexagon, (2,2,2)=cube, (3,2)=hexagonal prism, (4)=truncated octahedron.
**Entry state** of block i: s_i = m·R(B_1∪…∪B_{i-1}) (a rational number; it does not depend on any ordering choice).

**D-V7 Block admissible sets.** E_i = { orderings π of B_i : s_i·R(U) ∈ ℤ for every nonempty prefix set U of π }.

**D-V8 Face threshold.** K_F = lcm_{w∈V(F)} K(w).  Pref(F) = { B_1∪…∪B_{i-1}∪U : 1 ≤ i ≤ r, ∅ ≠ U ⊆ B_i }.

**D-V9 Birth vector and filtration.** For a prime q put b_q(F) = v_q(K_F). Source divisibility m | m′ gives X_C(m) ⊆ X_C(m′). Because X_C(m) depends only on
(min(v_q(m), cap_q))_q over the finitely many primes dividing some D(I), the complexes form a multi-parameter filtration over ℕ^P. A *regime* is a distinct
nonempty A_C(m); a *cover* is a Hasse relation between regimes under inclusion; an *event* is the exact record of a cover (faces born by dimension/type,
Δf, Δrank ∂, Δβ). This is the filtration of source divisibility at FIXED content, not the evolution of a state under SELECT-II.

**D-V10 Chain complex and boundary invariants (GF(2)).** f_j = #j-faces, ∂_j : C_j → C_{j-1}, ρ_j = rank ∂_j (ρ_0 = 0 = ρ_k), β_j = f_j − ρ_j − ρ_{j+1}.
**J₃ = ρ₃ = rank ∂₃; D₃ = f₃ − J₃ = dim ker ∂₃ on 3-chains** (the *defect*: 3-cells whose boundary relations are dependent).
**2-cycle certificate:** (z, φ) with z ∈ ker ∂₂, φ ∈ C²(X;GF(2)) = Hom(C₂,GF(2)), φ(∂₃c) = 0 for every 3-face c, φ(z) = 1. Such a pair proves [z] ≠ 0 in H₂ without computing ranks.

**D-V11 Graph class and ambiguity.** G(X) = uncoloured swap graph. For a domain 𝒟 of complexes and a graph class [G]:
ℛ₃([G];𝒟) = { J₃(X) : X ∈ 𝒟, G(X) ≅ G }, **A₃([G];𝒟) = log₂ |ℛ₃([G];𝒟)|** (domain-relative; 0 iff J₃ is a function of the graph on 𝒟).
H(J₃ | 2-skel) denotes the empirical conditional entropy of J₃ given the T15 data (f₀,f₁,f₂,ρ₁,ρ₂), uniform over the sets of the domain (domain-relative).

**D-V12 Graph-derived complex.** For a swap graph G and k: vertices, edges; 2-cells = 4-cycles and non-Petrie chordless 6-cycles (v002 T15);
d-cells (d ≥ 3) = convex induced subgraphs isomorphic to the graph of a d-face type of P_k; incidences by vertex-set inclusion. Convex = geodesically closed in G.
Everything uses only the uncoloured graph; no generator colours and no arithmetic.
