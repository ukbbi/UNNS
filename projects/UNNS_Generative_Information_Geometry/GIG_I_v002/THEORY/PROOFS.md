# GIG-I v002 — Proofs

Notation as in `DEFINITIONS.md`. All arithmetic statements are about positive integers; `R(N)=(N+1)²/N`.

---
## GIG-T11 — Cubical admissibility factorization

**Hypotheses.** A source `m_0∈ℤ_{>0}`. A *block word* `β=u_1u_2⋯u_r`, where each block `u_i` is either a single label `x`, or an ordered pair of two distinct labels `(a,b)`; the block `u_i` may be replaced by the swapped block `(b,a)` independently of the other blocks. Let `d` be the number of pair blocks and `Q_d={0,1}^d` the orientation choices. (This is exactly a commuting cube of the permutohedron; labels outside the pairs may even repeat.)

**Claim.** `Adm(m_0)∩Q_d = G×E_1×⋯×E_d` where `G∈{0,1}` and `E_i⊆{0,1}` are computed from the *formal* states below. In particular `|Adm∩Q_d|∈{0}∪{1,2,4,…,2^d}` and the slice is a coordinate sub-box.

**Proof.** (1) *Commutation of exit states.* Extend `τ_N(x)=x·R(N)` to `x∈ℚ`. For an integer `x` with `N|x`, `T_N(x)=τ_N(x)`. Hence for an admissible block, orientation `(a,b)` or `(b,a)`, the exit state is `x R(a)R(b)` — the same rational number, because multiplication in ℚ commutes: `T_aT_b(x)=T_bT_a(x)=xR(a)R(b)` whenever either order is admissible.

(2) *Formal states.* Put `s_1=m_0`, `s_{i+1}=s_i·∏_{x∈u_i}R(x)∈ℚ`. These numbers do not depend on any orientation choice. For a single-letter block `x` call it *locally admissible* at `s_i` if `s_i∈ℤ` and `x|s_i`; for a pair block put `E_i={o∈{0,1}: the order o is admissible step-by-step starting from s_i}`, where "admissible from a non-integer" is false by convention. Let `G=1` iff all single-letter blocks are locally admissible at their `s_i`.

(3) *Induction.* Let `o∈Q_d`. The word `β(o)` is admissible from `m_0` ⇔ `G=1` and `o_i∈E_i` for all `i`. (⇒) Run the word: by induction, if blocks `1..i−1` were admissible, the actual state before block `i` is an integer equal to `s_i` by (1); admissibility of block `i` then says exactly that it is locally admissible at `s_i`. (⇐) if `G=1` and `o_i∈E_i` for all `i`, blocks are admissible one after the other, the state before block `i` being `s_i` (by (1) again). ∎ The product form follows; `|E_i|∈{0,1,2}` gives the power-of-two law; for `d=3` the counts are `0,1,2,4,8`.

**Corollaries.** (a) *Square closure:* if three vertices of a commuting square are admissible, so is the fourth (a product set containing three corners of a square is the whole square). (b) *Petrie obstruction:* a Petrie 6-cycle uses six vertices of a `Q_3`, and a domino also six; both are impossible as `A∩Q_3`; any realizable `A` containing them contains all 8 vertices. (c) Every realizable set has the cube-product property (CP). (d) The statement is *not* a claim that every hexagonal configuration is forbidden: braid hexagons (6 vertices of a 2-face of type 3-block) are not inside a commuting cube and do occur (E5: four exactly realizable braid hexagons in the census).

**Executed form of the proof.** `cube_factor.formal_factors` computes `(G,E_1..E_d)` from the formal states; `E5`/the tests check `restriction(A_C(m),Q)=G×∏E_i` for 4.3·10⁶ (source, cube) pairs and the box/size law for every commuting cube of dimension ≥2 against every realizable set of the censuses.

---
## GIG-T12 — Threshold closure

Let `K(w)|m ⇔ w∈A_C(m)` (frozen law D-T7).

*(i) Realizable ⇒ closed.* If `S=A_C(m)≠∅`, `K(w)|m` for all `w∈S`, so `L(S)|m`. If `K(v)|L(S)` then `K(v)|m`, so `v∈S`. Thus `cl_K(S)⊆S`; and `S⊆cl_K(S)` trivially (`K(w)|L(S)`).
*(ii) Closed ⇒ realizable.* If `cl_K(S)=S` then `A_C(L(S))={v:K(v)|L(S)}=cl_K(S)=S`.
*(iii) Minimal source.* From (i), every realizing `m` is a multiple of `L(S)`; `L(S)` realizes `S` by (ii). So `L(S)` is the unique divisibility-minimal realizing source, hence also the numerically smallest.
*(iv) Closure operator.* Extensive: shown in (i). Monotone: `S⊆S'⇒L(S)|L(S')⇒cl(S)⊆cl(S')`. Idempotent: `L(cl S)` divides `L(S)` (every `K(v)` with `v∈cl S` divides `L(S)`) and is divisible by `L(S)` (as `S⊆cl S`), so `L(cl S)=L(S)` and `cl(cl S)=cl S`. Hence `cl_K(S)` is a closed set containing `S`, and any realizable `T⊇S` has `L(S)|L(T)`... precisely `cl_K(S)⊆cl_K(T)=T`: it is the **smallest realizable superset**.
*(v) Intersections.* `A_C(m)∩A_C(m')={w: K(w)|m and K(w)|m'}=A_C(gcd(m,m'))`.
*(vi) Squarefree sources.* If a squarefree `m` realizes `S`, `L(S)|m` is squarefree. Conversely if `L(S)` is squarefree, `m=L(S)` realizes `S` and is a squarefree (complete-history) source. ∎
*(vii) Level-set form used by the engine.* `A_C(m)=⋂_q M_{q,v_q(m)}` (levels of the per-prime exponents), so all `A_C(m)` are obtained from the finitely many exponent patterns `(e_q)`; the census enumerates every pattern, which is why no closure cap is needed (v001 needed one for the lcm-closure of thresholds).

---
## GIG-T13 — Reconstruction from the coloured swap graph

**Hypotheses.** Distinct labels; `A⊆S_k` arbitrary; `G_A` with colours `1..k−1`.

*Lemma 1 (faces are parabolic cosets).* Faces of `P_k` ↔ pairs `(J,xW_J)` with `|J|=dim`; the vertex set of the face `(B_1|…|B_r)` is `{x s: s∈W_J}` where `J` = positions interior to blocks. The subgraph of the permutohedron graph spanned by the colours in `J` has the cosets `xW_J` as its connected components (the Cayley graph of `W_J` w.r.t. its Coxeter generators is connected, and a `J`-coloured edge never leaves a coset).
*Lemma 2.* `xW_J⊆A` ⇔ the connected component of `x` in the `J`-coloured subgraph of `G_A` has `|W_J|` elements. (⇒) the whole coset is in `A`, so it lies in one component of size `|W_J|`. (⇐) the component is contained in the coset, whose size is `|W_J|`, so it equals the coset.
*Proof of the theorem.* (a) By Lemma 2 the faces of `K_A` are read off from `(G_A,colours)`. (b) For faces `F,F'` of `P_k`, `F'⊂F` as vertex sets ⇔ `F'` is a face of `F` (a face of the polytope whose vertices are in `F` is a face of `F`); dimension drops by one iff `|J'|=|J|−1`, and `J'⊆J`. So boundary matrices over `GF(2)` are determined. (c) `β_j=f_j−rank∂_j−rank∂_{j+1}` (rank–nullity). (d) Let `φ:G_A→G_B` be a bijection with `colour(φ(e))=σ(colour(e))`, `σ` a diagram automorphism (`id` or `j↦k−j`). `σ` maps runs of consecutive colours to runs of the same length, so `|W_{σ(J)}|=|W_J|`, and `φ` maps `J`-components onto `σ(J)`-components preserving size and inclusion. Hence `φ` induces a dimension-preserving isomorphism of the face posets of `K_A` and `K_B`, and an isomorphism of chain complexes. ∎

*Sharpness (what the uncoloured graph forgets).* Without colours the statement is false for arbitrary `A`: the Petrie 6-cycle (β=(1,1,0,…)) and the braid hexagon (β=(1,0,…)) have isomorphic uncoloured graphs (certificate `Z1`). The theorem T11 shows that arithmetic realizability excludes exactly this configuration.

---
## GIG-T14 — Graph isomorphism ⇒ equal graph-derived profiles

The v001 quantities — class sizes (component sizes), balls `B_r(w)` (sets of vertices within graph distance `≤ r`), the product `P_r=∏_w|B_r(w)|`, `I_r=log₂P_r/N`, within-class entropies, fine and scalar signatures — are defined by the graph metric only. A graph isomorphism preserves components and distances, so it maps balls onto balls bijectively; therefore every one of these is equal for isomorphic graphs, at every radius. Contrapositive: a difference in any profile at some radius proves the graphs non-isomorphic (this is how W1–W6 are non-isomorphic; the certificates store the exact negative isomorphism result). ∎

---
## GIG-T15 — Graph-only recovery of the 2-skeleton under arithmetic admissibility

**Hypotheses.** `A` has CP (every realizable set, by T11); `k≤8`, where the classification below was verified exhaustively.

*Step 1 (4-cycles).* Every 4-cycle of the permutohedron graph is a square face (two commuting colours): the only relation of length 4 among distinct consecutive Coxeter generators is `(xy)²=1`, i.e. `m(x,y)=2` (v001 test `test_four_cycles_are_square_faces`; the E5 enumeration also finds no other closed reduced 4-word). In `G_A` such a 4-cycle has all four vertices in `A`, so the square is a face of `K_A`. Hence squares ↔ 4-cycles of `G_A`.
*Step 2 (6-cycles; E5).* The 6-cycles of `P_k` fall into exactly four types (no other type for `k≤8`): braid hexagon (chordless), cube-petrie (chordless), cube-domino (one chord), mixed-domino (one chord).
*Step 3 (recognising braid hexagons).* In `P_k` a vertex `u∉H` adjacent to two vertices `x≠y` of a braid hexagon `H=xW`, `W=⟨s_i,s_{i+1}⟩`, would give `x⁻¹y=s_cs_d∈W` with `c≠d`, `c∉{i,i+1}`; but such a product moves a position outside `{i,i+1,i+2}` while `W` fixes them. So no outside vertex touches two hexagon vertices. In a Petrie cycle, each of the two removed antipodal cube vertices is adjacent to three cycle vertices; by CP (six vertices of `Q_3` in `A` ⇒ all eight) these vertices belong to `A`. So in `G_A` a chordless 6-cycle is a braid hexagon iff no outside vertex is adjacent to two of its vertices.
*Step 4.* Therefore the 2-skeleton of `K_A` (vertices, edges, squares, hexagons) is a function of the uncoloured graph; so are `f_0,f_1,f_2`, the boundary map `∂_2` and — cellular homology in degrees ≤1 depends only on the 2-skeleton — `β_0` and `β_1`. (Petrie cycles are boundaries of the three squares at a removed vertex, so including or excluding them in the span does not change `β_1`; the engine excludes them from `f_2` and includes them in the span.) ∎

*Consequence for GIG-Q3.* A realizable pair with isomorphic uncoloured graphs and different homology must differ in `β_j` for some `j≥2`.
