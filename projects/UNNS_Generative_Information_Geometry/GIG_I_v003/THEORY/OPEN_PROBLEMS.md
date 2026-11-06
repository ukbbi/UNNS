# GIG-I v003 — Open problems

**GIG-Q3 (status: narrowed, still open in general).** Are there two admissible (realizable, distinct-label) history complexes with isomorphic uncoloured swap graphs and different Betti vectors?
*v003 result:* β₀,β₁ are graph invariants (v002 T15, k ≤ 8). By T19 any counterexample must differ in ρ₃ (equivalently β₂). T20 shows that graph-only recognition determines every face (hence ρ₃ and all β_j) on all verified domains and for every P_k-convex set (k ≤ 7). A counterexample would therefore have to be a realizable cube-product set with a convex-in-G_A induced face copy that is not a face (T20d), or lie outside the verified domains (k ≥ 8, or k = 6 beyond the sample, or k = 5 beyond L ≤ 16).

**GIG-Q5 (new).** Does the uncoloured swap graph determine rank ∂₃? *Yes on every verified domain* (A₃ ≡ 0 on the exhaustive k=4 and k=5 domains); general proof reduces to T20d.

**GIG-Q6 (new).** What is the minimal extra data, beyond graph connectivity and accessibility, needed for higher boundaries? *Within realizable sets, none was found to be needed beyond the graph itself*; but the information is not carried by the 2-skeleton data: the cells are recovered only from the graph's convex induced 3-dimensional structure. Without arithmetic (non-CP sets) generator colours suffice (v002 T13) and graph alone fails (Z1).

**Q7 (T21c).** A closed-form arithmetic law for all H₂ changes. Known: β₂ depends only on faces of dimension ≤ 3 (T21a); for the two anchors the law is the threshold-lattice statement of T21b. Open: a general description of when a class created by new 2/3-faces survives, in terms of the primes dividing the K_F.

**Q8 (T20d).** Soundness of graph recognition for non-convex realizable cube-product sets.

**Q9.** Why are the H₂ certificates of the two anchors identical in rank coordinates (same 96-face z, same 6-face φ, same six obstructed truncated octahedra) while the sources differ (288 vs 432)? Conjecture: the cycle lives in the combinatorial sub-pattern determined by the three labels (ranks 2,4,5) whose block {2,4,5} supports the hexagon caps, and only the identities of the three "unlocking" primes change.

**Q10.** The targeted k=7 probe (E14) finds further β₂ = 1 regimes in extensions of both anchors. Their mechanism (same hole-filler pattern or new ones) is not analysed here.

**Q11 (separating radius).** If T20d holds, the radius-6 rooted ball determines the set of cells through a vertex (3-cells have diameter ≤ 6, convexity of a set of diameter ≤ 6 can be tested inside the ball of radius 6). The global rank ρ₃ nevertheless needs the whole graph. Whether a *local* radius suffices for Betti numbers (v002's fine radius-2 profile for k=6, radius 3 for k=5) is unaffected by v003.

**Q12 (new, from E14).** First nonzero β₃ in the programme: four k=7 regimes (contents (2,3,4,5,8,9,14|15), (2,3,6,7,8,9,14|15), sources 4032, 4320, 6048, 6480) have Betti vector (1,0,0,1,0,0,0); other regimes reach β₂ = 2 and 3. These regimes have N ≥ 2160 and were *not* graph-reconstructed (E14 graph checks are restricted to N ≤ 400), so T20c does not cover them. Their arithmetic mechanism is unanalysed.

**Q13 (new, from E13).** The T15 data (f₀,f₁,f₂,ρ₁,ρ₂) do *not* determine J₃ in general: in the exhaustive k=5, L ≤ 16 domain one 2-skeleton-data class contains two J₃ values (H(J₃ | 2-skel) = 0.0006 bits), while the full graph separates them (A₃ ≡ 0). Is this the first instance of a general phenomenon (third-boundary information carried by the graph but not by its 2-skeleton)?
