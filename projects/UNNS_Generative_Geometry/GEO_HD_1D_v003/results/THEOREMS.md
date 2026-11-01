# THEOREMS -- GEO_HD_1D_v003 (continues v001 D-T0..D-T5 and v002 D-T7..D-T10, all preserved byte-identical)

Fixed-source scope throughout. Same-author caveat. C3 NOT claimed. Novelty NOT assessed. Statuses: PROVED (written proof + independent verifier corroboration), FINITE-EXACT (exhaustive in a stated box), OPEN.
Items marked [user] were proposed in the review note / v002 specification and are re-proved here; everything else is new in this release.

| id | statement | status | where |
|---|---|---|---|
| D6-T1 | K(w) divides m <=> admissible; K(w) divides P(C); only gcd(m,P(C)) matters [user: first part = v002 D-T7] | PROVED | THRESHOLDS.md |
| (P) | K(w) = lcm of kappa(prefix sets); admissible histories = maximal chains of feasible subsets | PROVED | THRESHOLDS.md |
| D6-T2 | induced-subgraph monotonicity; saturation (P(C) divides m) => complete connected graph | PROVED | THRESHOLDS.md |
| D7-T1 | connectivity iff some path threshold divides m [v002 D-T8] | PROVED | v002 |
| Lemma NF | x does not feed y, (x,y) admissible => (y,x) admissible | PROVED | CONNECTIVITY.md |
| F2 | swap classes factor over SCC blocks of the feeding digraph | PROVED | CONNECTIVITY.md |
| F1 | acyclic feeding digraph => <= 1 class at every source; universal minimal threshold | PROVED | CONNECTIVITY.md |
| D-T9 converse | {2,3,N} has a split source iff N = 2,3 mod 6, N >= 8 (v002: FINITE-EXACT) | PROVED | CONNECTIVITY.md |
| Block-size | distinct labels: a split needs an SCC block with >= 3 labels | PROVED | CONNECTIVITY.md |
| Hub | hub-descent => never splits | PROVED | CONNECTIVITY.md |
| T3 | exact 3-label classification (antipodal pair; b does not divide m; kappa{a,c} does not divide m) | PROVED | OBSTRUCTIONS.md |
| T-DUAL | H~_i(K_A) = H~^{k-3-i}(N(R)); b_{k-2}=0; b_{k-3} = c(R)-1 | PROVED | ROUTE_TOPOLOGY.md |
| T-LOWER | weak-order lower sets give contractible K_A; acyclic feeding => all route complexes contractible | PROVED | ROUTE_TOPOLOGY.md |
| T-SPHERE | infeasible family = {E, O} complementary pair => K_A ~ S^{k-3} | PROVED (topology) | ROUTE_TOPOLOGY.md |
| T-SPHERE-arith | C = {2,3} u X (X in {n>=8, n=2,3 mod 6}), m = prod X: infeasible family is exactly {E, O} (1702 contents, |X|<=4) | FINITE-EXACT | ROUTE_TOPOLOGY.md |
| Loop family | {2,3,N,M}, 4<=N<M<=60: a first Betti number occurs iff N,M >= 8 and N,M = 2,3 mod 6; connected with Betti (1,1,0,0) at m=NM | FINITE-EXACT | ROUTE_TOPOLOGY.md |
| Void | {2,3,8,9,14} at m=1008 has Betti (1,0,1,0,0); cubical complex (1,19,0,0,0) | FINITE-EXACT | ROUTE_TOPOLOGY.md |
| D9-orthant | d in D(m) iff m in the orthant v >= 2 nu(d); |Delta| closed form; refinement chain | PROVED | OCCURRENCE_BRIDGE.md |
| D9-tables | restricted class counts, 72^r, r<=3 | FINITE-EXACT | OCCURRENCE_BRIDGE.md |

## Proof-status notes
* T3, F2, T-LOWER, T-DUAL, T-SPHERE are hand proofs (in the theory files) corroborated by an independent verifier that does not import the builder. They have not been reviewed by a human.
* The v002 STATUS.json still says FINITE-EXACT for the D-T9 converse; v002 is frozen. The upgrade lives only in this release.
