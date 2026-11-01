# ROUTE_TOPOLOGY -- Stage C (D8, D-Q2): the topology of route complexes

Statuses as in THRESHOLDS.md. Same-author caveat; C3 NOT claimed. Fixed-source scope. Numerical Betti numbers are NOT theorems; each theorem below has a proof, and each census table is labelled FINITE-EXACT.

## Complexes (contents of DISTINCT labels, k labels)
* **Permutohedral route complex K_A.** The faces of the permutohedron P_k are the ordered set partitions (B_1|..|B_j) of the labels; the vertices of a face are the arrangements listing B_1 first, then B_2, ...; dim = k-j. For a set A of arrangements (here A = A(m), the admissible ones) K_A is the *full subcomplex*: a face is kept iff all its vertices are in A. Its 1-skeleton is the swap graph; a square is two independent legal swaps (Independence Lemma, v001); a hexagon is a braid relation and is filled when all six words are admissible.
* **Cubical route complex Q_A.** The subcomplex of faces all of whose blocks have size <= 2 (products of edges): vertices = admissible histories, edges = legal swaps, squares/cubes = independent swaps. Braid hexagons are never filled.
* **Repeated labels** need a separate construction (sub-multiset chains); not constructed here: OPEN.
Prefix-set picture: faces of P_k <-> flags of subsets; a facet of P_k is (S | C minus S) = all words with prefix set S; hence the non-admissible vertex set is R = union of the facets F_S over the infeasible S.

## T-DUAL (Alexander duality; PROVED)
For nonempty A != S_k, K_A is a subcomplex of the sphere bdry P_k = S^{k-2}. Its complement is the union of the open stars of the vertices of R = S_k minus A; any family of these open stars has nonempty intersection iff the vertices lie in a common proper face, and then the intersection is the open star of the smallest such face (contractible). By the nerve theorem the complement is homotopy equivalent to the nerve N(R) (simplices = subsets of R inside a common proper face), and Alexander duality over GF(2) gives
   H~_i(K_A) = H~^{k-3-i}(N(R)).
Consequences: b~_{k-2}(K_A) = 0; b~_{k-3}(K_A) = (number of components of N(R)) - 1, where two non-admissible arrangements are linked iff they share a proper prefix set. k=3: b_1 = 0 (a proper subcomplex of the hexagon is a union of arcs). k=4: b_2 = 0 and b_1 = c(R)-1. k=5: b_3 = 0 and b_2 = c(R)-1.
(Verifier X4: all realized patterns k=4 and 3,173 complexes; builder census 27 + 1405 + 4817 patterns for k=3,4,5, 0 violations; the verifier computes the components with its own prefix-set test, independent of the builder.)

## T-LOWER (PROVED): lower sets are contractible
Fix a total order tau on the labels, giving the weak order on arrangements (u <= v iff the inversion set of u is contained in that of v). If A is a lower set of the weak order (closed under swapping an adjacent inverted pair into a non-inverted one), K_A is empty or contractible.
*Proof.* A proper nonempty lower set contains the bottom (sorted) word b. Induct on |A|. Let v != b be maximal in A. The permutohedron is simple, so the faces through v correspond to subsets J of the k-1 adjacent position pairs of v (the intervals of J are the blocks). If J contains an ascent of v, the face contains the up-neighbour of v, which is not in A by maximality; if J consists of descents only, the face's vertices are permutations inside decreasing runs of v, all <= v, hence in A. Since A is proper and a lower set, v is not the top, so Desc(v) is a proper subset of the positions and the link of v in K_A is the full simplex on Desc(v) (contractible, non-empty because v != b). K_A = K_{A minus v} union star(v), star(v) is a cone over its link, and the intersection is contractible; hence K_A ~ K_{A minus v}. A = S_k is a single cell. QED
**Corollary (acyclic feeding digraph => contractible route complexes).** By Lemma NF the admissible set of a content with acyclic feeding digraph is closed under inversion-reducing adjacent swaps with respect to any linear extension, i.e. it is a weak-order lower set (verifier X2: every instance checked), so *every route complex of such a content, at every source, is empty or contractible*. (Verifier X4: all k=4 instances; builder: 9156 / 8085 / 1502 content-source pairs for k=3,4,5.)

## T-SPHERE (PROVED for the topology; the arithmetic hypothesis is FINITE-EXACT)
Let C = E u O be a partition into nonempty sets and assume the infeasible proper subsets at m are exactly E and O (equivalently R = F_E u F_O, the facets E|O and O|E). Then K_A is homotopy equivalent to S^{k-3}: over GF(2) its Betti numbers are 1 in degree 0 and 1 in degree k-3 (for k=3: 2 in degree 0, i.e. two points = the antipodal pair).
*Proof.* Two vertices v in F_E and w in F_O have no common proper prefix set (a proper prefix set of v of size s <= |E| lies in E, of size s >= |E| contains E, and symmetrically for w; equality is impossible unless the set is all of C). So N(R) has exactly two components, each a full simplex (all vertices of a facet lie in the proper face F_E, resp. F_O). By T-DUAL, H~_{k-3}(K_A) has rank 1 and all other reduced groups vanish. QED
(Verifier X4: all (k, |E|) with k=3..5 (and a sample of k=6 in --full); the arithmetic family below.)
**Arithmetic realisation (FINITE-EXACT).** C = {2,3} u X with X a set of labels n >= 8, n = 2 or 3 mod 6 and source m = prod X: the infeasible proper subsets are exactly E = {labels = 2 mod 6} and O = {labels = 3 mod 6}. Checked for 1702 contents with |X| <= 4 (|C| <= 6; labels <= 61, and <= 44 for |X| = 4) in the builder, 120+ contents in the verifier by direct simulation of admissibility. Betti numbers (builder, |C| <= 5): 18 contents with (2,0,0), 153 with (1,1,0,0), 816 with (1,0,1,0,0).
**Examples.** {2,3,8,9} at m = 72: swap graph CONNECTED (one class), 16 admissible arrangements, Betti (1,1,0,0): an unfilled loop of legal swaps. {2,3,8,9,14} at m = 1008 = 8*9*14: 96 admissible arrangements, Betti (1,0,1,0,0): a 2-dimensional void. Both are invisible to the connectivity classification.
**Loop family (FINITE-EXACT).** For {2,3,N,M} with 4 <= N < M <= 60 a first Betti number appears at some source iff N, M >= 8 and N, M = 2 or 3 (mod 6); at m = N*M the swap graph is connected with Betti (1,1,0,0) (builder: the converse over 1596 pairs 4 <= N < M <= 60; verifier: the converse over 630 pairs with N < M < 39, and the loop at m = NM for 8 <= N < M < 60 with N, M = 2,3 mod 6).

## Cubical versus permutohedral (FINITE-EXACT computation)
Full P_3: cubical b = (1,1,0) (the hexagon is an unfilled loop) while the permutohedral complex is a disc. Full P_4: cubical (1,7,0,0), permutohedral (1,0,0,0). So a cube-only complex reports loops that are mere braid relations. For {2,3,8,9,14} at 1008 the cubical complex has Betti (1,19,0,0,0): nineteen loops and no 2-void, while the permutohedral complex has (1,0,1,0,0). The genuine obstruction (the void) is seen only after the braid hexagons are filled. For {2,3,8,9} at 72 the two complexes agree.

## Census (FINITE-EXACT; contents of distinct labels; every lcm-closure source)
k=3, labels <= 30: 16,378 (content,source) pairs: Betti (1,0,0) 16,251; (2,0,0) 127.
k=4, labels <= 18: 27,751 pairs: (1,0,0,0) 27,321; (1,1,0,0) 16; (2,0,0,0) 405; (3,0,0,0) 7; (4,0,0,0) 2.
k=5, labels <= 11: 8,884 pairs: (1,0,0,0,0) 8,617; (1,1,0,0,0) 21; (2,0,0,0,0) 235; (3,0,0,0,0) 11.
In the targeted set {2,3} u (3 labels n >= 8, n = 2,3 mod 6, <= 44): Betti vectors (1,0,1,0,0) (the void), (1,j,0,0,0) for j = 1..4, and up to 7 components occur; no b_3 or b_4.
No b_i > 0 for i >= 2 occurs outside the void in these ranges; whether b_2 > 0 occurs for other reasons, and the full list of realizable homotopy types, are OPEN.

## Statement of the general conjecture (OPEN)
Is K_A always a wedge of spheres? (Every complex found has homology of a wedge of spheres.) Which families F(m) of infeasible subsets occur as F(m) of an arithmetic content? Is every sphere S^j, 0 <= j <= k-3, realized?
