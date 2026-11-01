# E2-P4 v005 -- planar theorem re-proved from scratch; the three-dimensional boundary (continuation of THEOREMS*.md up to _V004, all preserved)

Status vocabulary: PROVED (complete argument, elementary except where a cited standard fact is named) / CHECKED (finite exact computation) / OPEN / FALSE.
C3 is **not** claimed. Nothing here is called new: no prior-art search beyond the limited one in `PRIOR_ART_AUDIT_V005.md` has been done, and all arguments are elementary.
Same-author caveat: every check in this release was written by the author of the proofs; three code routes (below) share no code, but none is external verification.

## 0. Conventions (inherit THEOREMS_V004.md)
Lambda <= Lambda' are full-rank lattices of Z^k, Q = prod[0,q_c], F(M) = (M cap Q) \ {0}. A *Graver vector* of M is a nonzero w in M that is conformally minimal:
no nonzero w' in M, w' != w, with w'_c w_c >= 0 and |w'_c| <= |w_c| for all c ("w' <= w conformally"). A *j-cell* of M is P(u; g_1..g_j) = u + sum [0,1] g_i, g_i Graver in M and
linearly independent, all 2^j corners in F(M). U(M,Q) = union of the closed cells; U^0(M,Q) = the same with corners allowed to be 0. The orientation of a generator and the choice of base corner do not change the
set P(u; g_1..g_j). g^+ = max(g,0), g^- = min(g,0), supp(v) = {c : v_c != 0}.

## 1. Tools

### L1  Conformal decomposition (PROVED)
Every v in M is a finite sum of Graver vectors of M, each conformally <= v.
*Proof.* Induction on |v|_1. v = 0: empty sum. Else the set of nonzero lattice vectors conformally <= v is finite and nonempty (it contains v); a member g of minimal L1-norm is Graver
(a nonzero w' <= g would also be <= v and shorter). v - g is conformally <= v and shorter; apply induction; conformal order is transitive. QED

### T0  Explicit tiling lemma (PROVED, given the standard fact SF below; CHECKED exactly, RUN_VERIFY S1)
Let V = (v_1..v_n) be nonzero integer vectors spanning a d-dimensional rational subspace (work in lattice coordinates of the span, so v_i in Z^d), Z(V) = sum [0,1] v_i.
If n = d, Z(V) is one parallelotope (A = empty). Otherwise choose integer heights w_i so generic that for every d-subset S with det(V_S) != 0 and every i not in S, the lifted vector
v~_i = (v_i, w_i) in R^{d+1} is not in span(v~_s : s in S) (each such condition is a nontrivial linear condition on w: the coefficient of w_i is 1, so finitely many hyperplanes are avoided).
For each such S let nu_S in R^{d+1} be a normal of span(v~_S), signed so that its last coordinate is negative (it is nonzero: it equals +-det(V_S)), and
A_S = { i not in S : nu_S . v~_i > 0 }.   Put  T_S = sum_{i in A_S} v_i + Z(V_S).
**Claim.** (a) the T_S cover Z(V); (b) the T_S have pairwise disjoint interiors (a fine zonotopal tiling); (c) every vertex of every T_S is a *subset sum* sum_{i in A} v_i, A subset of {1..n}.
*Proof.* (c) is the definition of T_S. For a linear functional nu, the face of the lifted zonotope Z~ = sum[0,1] v~_i on which nu is maximal is sum_{nu.v~_i>0} v~_i + sum_{nu.v~_i=0}[0,1]v~_i (the sum is separable).
By genericity, the facets of Z~ are exactly sum_{i in A_S} v~_i + Z(v~_S) for the d-subsets S with det(V_S) != 0 (a facet normal is orthogonal to d independent generators, and genericity forbids a further generator from lying in
their span). Such a facet is *lower* iff nu_S has negative last coordinate, so the lower facets are the lifted T_S, and the vertical projection pi (drop the last coordinate) is injective on each (S is independent in R^d) with image T_S.
**SF (standard fact).** For a full-dimensional polytope the lower facets project onto the shadow pi(Z~) with disjoint interiors (regular subdivision induced by a lifting; see the polytopal-subdivision chapter of Ziegler, *Lectures on Polytopes* -- section number not re-checked here). Since pi(Z~) = Z(V), (a),(b) follow.
(This is the lifting construction behind the Bohne-Dress correspondence; see PRIOR_ART_AUDIT_V005.) QED
*Exact checks (CHECKED).* For random configurations (d = 1,2,3, with parallel and repeated vectors) the tile-volume sum equals the zonotope volume sum_S |det V_S| and 60 random points of Z(V) are each found in a tile (RUN_VERIFY S1).

### Z  Zero-vertex criterion (PROVED; this is P4-Z1/P4-Z2 with a complete argument)
Let C = P(u; g_1..g_j) be a cell of U(Lambda,Q), Lambda <= Lambda'.
**Z.1 (sufficient).** Suppose there are no vectors s_i in Lambda', each conformally <= g_i (possibly 0 or g_i), with u + sum s_i = 0. Then C <= U(Lambda',Q).
*Proof.* By L1 write each g_i = sum_t h_{i,t}, h_{i,t} Graver in Lambda' and conformally <= g_i. Z' = u + sum_{i,t}[0,1]h_{i,t} contains C (the segment [0,g_i] lies in sum_t[0,h_{i,t}]).
Tile Z' by T0. A tile vertex is u + sum of a sub-collection of the h's, i.e. u + sum_i s_i with s_i a partial sum of the pieces of g_i: in Lambda', conformally <= g_i. Coordinate c of the vertex lies between
u_c + sum_i min(g_{i,c},0) and u_c + sum_i max(g_{i,c},0), which are coordinates of two corners of C, hence in [0,q_c]: the vertex is in Q. It is nonzero by hypothesis. So every tile (generators Graver in Lambda', independent)
is a cell of U(Lambda',Q), and C <= Z' <= U(Lambda',Q). QED
**Z.2 (explicit form).** A zero-vertex decomposition exists iff m(C) := u + sum_i g_i^- = 0 and g_i^- in Lambda' for all i; then s_i = g_i^-.
*Proof.* (=>) coordinatewise, s_{i,c} >= min(g_{i,c},0), so 0 = u_c + sum_i s_{i,c} >= m_c; but m_c is the c-th coordinate of a corner of C, hence >= 0. So equality holds throughout: m_c = 0 and s_{i,c} = min(g_{i,c},0). (<=) take s_i = g_i^-. QED
**Z.3 (robust form; hard cells).** C has 2^j representations (base corner, generator signs); Z.1 applies to each. Hence C <= U(Lambda',Q) unless
  m(C) = 0 (C touches every coordinate hyperplane) and g_i^+ and g_i^- in Lambda' for all i.   (H)
Cells satisfying (H) are *hard*. Only hard cells can escape; hard 1-cells do not exist (Graver minimality, see LG).

### LG  Adjacent corners overlap in support (PROVED)
If P, P' are corners of a cell of U(Lambda,Q) differing by one generator w = P' - P, then supp(P) cap supp(P') != empty.
*Proof.* P, P' are nonzero and >= 0. If the supports were disjoint then P' and -P are conformally <= w (on supp(P'): w_c = P'_c >= 0 = P_c; on supp(P): w_c = -P_c <= 0 = P'_c; zero elsewhere), both lie in Lambda,
both are nonzero, and P' != w (else P = 0), -P != w (else P' = 0): w is not Graver. QED

### H1  A hard cell is a Minkowski sum of segments (PROVED)
Let C be hard with generators g_i and put a_i = -g_i^- >= 0, b_i = g_i^+ >= 0 (both in Lambda', supp(a_i) cap supp(b_i) = empty, g_i = b_i - a_i). Then the base corner is u = sum a_i and
  C = sum_i [a_i, b_i],   C <= Z^0 := sum_i ([0,a_i] + [0,b_i]) <= [0, Q_C],
where Q_C = sum_i(a_i + b_i) is the top corner of C. In a fine tiling of Z^0 by Graver pieces of the a_i,b_i (T0, Z.1) **every tile not containing the origin is a cell of U(Lambda',Q_C)**; the origin is the only vertex that is not
a nonzero subset sum. So the only part of C that can fail to lie in U(Lambda',Q_C) is C intersect St(0), the star of the origin in the tiling.
*Proof.* u + sum lambda_i g_i = sum_i[(1-lambda_i)a_i + lambda_i b_i]; the rest is Z.1 with the decomposition s_i = g_i^-. QED
(This is the precise form of "the deleted origin matters only for cells that touch every coordinate plane".)

## 2. The planar theorem

### P5-P1  (= P4-P1) Planar monotonicity (PROVED)
Lambda <= Lambda' <= Z^2 (rank 2), Q = [0,a] x [0,b] any box. Then U(Lambda,Q) <= U(Lambda',Q).
*Proof.* 0-cells are trivial; edges are covered by Z.1 (a hard 1-cell does not exist: Z.2 would need u + s = 0 with s in Lambda' conformally <= g; for a cell of Lambda this reads
-u = s, a nonzero element of Lambda conformally <= g, and s != g because u + g != 0 -- contradicting Graver minimality of g in Lambda). Let C = P(u;g,h) be a 2-cell. If it is not hard, Z.3 applies. Let it be hard.
Let k', l' >= 1 be minimal with k'e_1, l'e_2 in Lambda' (finite index). k'e_1 and l'e_2 are Graver in Lambda' (a conformally smaller nonzero vector of Lambda' is (t,0), 0 < t <= k', so t = k').
(1) m(C) = 0 gives corners A = (0,y0), B = (x0,0) with x0, y0 > 0 (nonzero, in Q), both in Lambda.
(2) A, B are not adjacent: supp(A) = {2}, supp(B) = {1} are disjoint (LG). So they are opposite corners; write D, E for the other two.
(3) Shape. With edge vectors g', h' at A (B = A + g' + h'), membership of D = A+g', E = A+h' in Q gives g'_1, h'_1 >= 0, and y0 + g'_2, y0 + h'_2 >= 0 with g'_2 + h'_2 = -y0, so g'_2, h'_2 <= 0. Write g' = (g1,-g2), h' = (h1,-h2),
all four numbers >= 0, g1 + h1 = x0, g2 + h2 = y0, D = (g1,h2), E = (h1,g2).
(4) g1, h1, g2, h2 > 0. D is adjacent to both A and B and nonzero, so by LG supp(D) meets {2} and {1}: D has both coordinates positive: g1 > 0 and h2 > 0. The same for E = (h1,g2): h1 > 0 and g2 > 0.
(5) Hardness: g'^+ = (g1,0), g'^- = (0,-g2), h'^+ = (h1,0), h'^- = (0,-h2) are in Lambda' (they are g^+-, h^+- up to sign). Hence k' | g1, h1 and l' | g2, h2, so g1,h1 >= k', g2,h2 >= l', x0 = g1+h1 in k'Z, x0 >= 2k', y0 in l'Z, y0 >= 2l'.
(6) The four corners satisfy x/k' + y/l' >= 2 (A: y0/l' >= 2; B: x0/k' >= 2; D: g1/k' + h2/l' >= 2; E likewise). By convexity every p in C has p_1/k' + p_2/l' >= 2, so **p_1 >= k' or p_2 >= l'**.
(7) The rectangles R_ij = [ik',(i+1)k'] x [jl',(j+1)l'], 0 <= i < x0/k', 0 <= j < y0/l', tile [0,x0] x [0,y0] <= Q; their corners are in Lambda' cap Q and nonzero except for the corner 0 of R_00, so each R_ij, (i,j) != (0,0),
is the cell P(corner; k'e_1, l'e_2) of U(Lambda',Q). A point p of C has p_1 >= k' (then p lies in some R_ij with i >= 1, because x0/k' >= 2) or p_2 >= l' (some R_ij with j >= 1). Hence C <= U(Lambda',Q). QED
*Audit notes (this release re-derived the proof without looking at the v004 text and compared).* Step (2)/(4) of v004 (two ad hoc Graver contradictions) are exactly LG applied to the pairs (A,B), (D,B), (D,A), (E,B), (E,A); the covering step (7) is now stated without the
"only in R_00" case distinction. No gap found. The proof uses: L1 (Graver decomposition), T0 (tiling), nestedness, and Graver minimality; it does not use any FIELD-I arithmetic and holds for every box.
*Independent corroboration (CHECKED).* `src/planar_audit.py` (from-scratch exact polygon arithmetic) tests 1,530 planar hard cells (1,529 hard-driven over seeds 100-103, 1 random) (48,000 random nested pairs, targets of index <= 6, sources of index <= 8, each cell against U(Lambda',Q_C), Q_C its own bounding box)
and 2,334 ordinary 2-cells (random seed 7): 0 containment failures, 0 violations of the structure (1)-(6) (results/P5_PLANAR_AUDIT.json).

### P5-P1.a  Scope of the FIELD-I corollary (PROVED; scope correction)
For a *fixed-coordinate planar* FIELD-I transition x -> C(x) (same primes, same box) the relation lattices are Lambda_x and Lambda_{C(x)} in Z^2. P5-P1 gives U(Lambda_x,Q) <= U(Lambda_{C(x)},Q) **if Lambda_x <= Lambda_{C(x)}**.
FIELD-I only guarantees inclusion of the finite occurrence fibres (E2-P2 exhibited shrinking and incomparable full lattices), so the theorem does not by itself settle planar transitions with incomparable lattices; this distinction is to be kept in the theorem registry.

### P5-F1  Cells in a coordinate plane (PROVED)
Let Lambda <= Lambda' <= Z^3 and let C be a cell of U(Lambda,Q) contained in {x_i = 0}. Then C <= U(Lambda',Q).
*Proof.* Graver(Lambda cap H) = Graver(Lambda) cap H for H = {x_i = 0} (a vector conformally below one with x_i = 0 has x_i = 0), so C is a cell of the planar pair Lambda cap H <= Lambda' cap H (both of rank 2), and
P5-P1 gives C <= U(Lambda' cap H, Q cap H) <= U(Lambda',Q), the latter because Graver(Lambda' cap H) is Graver in Lambda' with the same corner conditions. QED
So in 3D a failing cell is never contained in a coordinate plane: its escape needs a genuinely spatial position.

## 3. Dilation

### P5-D1  Diagonal-dilation invariance (PROVED)
For D = diag(t_1..t_k), t_c positive integers: Graver(D M) = D Graver(M), F(DM, DQ) = D F(M,Q), cells map to cells, so U(DLambda, DQ) = D U(Lambda,Q), and
U(Lambda,Q) <= U(Lambda',Q)  <=>  U(DLambda,DQ) <= U(DLambda',DQ).
*Proof.* D is a linear bijection M -> DM preserving the sign pattern and monotone in absolute value coordinatewise, hence the conformal order; it maps the box [0,Q] onto [0,DQ] and 0 to 0. QED
**Consequence.** The property "no free coordinate" (e_c not in Lambda') is *not* invariant under D: the axis orders k_c of Lambda' become t_c k_c. Every containment failure with a free coordinate becomes a failure
with axis orders >= 2 (indeed arbitrary) -- see P5-C1.

## 4. The three-dimensional boundary: the conjecture is FALSE

### P5-C1  (PROVED; hand-checkable; confirmed by three code routes) Failure with no free coordinate
Let E_3 = {z in Z^3 : z_1+z_2+z_3 even}, Lambda = 2E_3 <= Lambda' = 2Z^3 (axis orders (2,2,2): **no free coordinate**), Q = (2,4,2). Then U(Lambda,Q) is **not** contained in U(Lambda',Q).
*Proof.* Graver(E_3) = {2e_i, e_i +- e_j}, so Graver(2E_3) = 2 Graver(E_3). Let g = (0,2,-2) = 2(0,1,-1), h = (2,-2,0) = 2(1,-1,0), u = (0,2,2). The corners (0,2,2), (0,4,0), (2,0,2), (2,2,0) are nonzero points
of 2E_3 cap Q, so C = P(u;g,h) is a 2-cell of U(Lambda,Q). The point p = u + (1/6) g + (1/3) h = (2/3, 5/3, 5/3) lies in C.
U(2Z^3, Q): Graver = {2e_i}, so every cell is P(c; 2e_i, i in I) with c in 2Z^3. A cell containing p must have, for each coordinate i with 0 < p_i < 2 (all three), the generator 2e_i with base coordinate c_i = 0;
that cell is [0,2]^3 whose corner 0 is excluded. So p is not in U(2Z^3,Q) and C is not contained. QED
(Equivalent unscaled statement, P5-D1 with t = 2: E_3 <= Z^3, Q = (1,2,1), p = (1/3,5/6,5/6). The point (2/3,2/3,2/3) is also a witness. Geometrically C slices the open unit cube, the one cell of the axis grid that the deleted origin removes.)

### P5-C2  Infinite family (PROVED)
For every failing triple (Lambda,Lambda',Q) and every positive integers t_1..t_k the dilated triple fails (P5-D1). In particular each of the 57 recorded v002/v003 failures (all with a free coordinate) generates failures with *all* axis orders >= 2.
(CHECKED: CE0, CE1, CE2 = dilations by 1, 2, 3 of the same configuration, `src/ce_check.py`.)

### P5-C3  (CHECKED exactly, three routes) Failure for a target that is not split in any coordinate
Lambda = 2E_3 <= Lambda' = BCC := {z : z_1 = z_2 = z_3 (mod 2)} (index 4, axis orders (2,2,2), not split in any coordinate), Q = (2,4,2): NOT_CONTAINED, witness (5/6, 5/3, 3/2) in C, certified by the pinned E2-P3 engine
and by that engine's independent certificate checker, and by brute force from the definitions (`src/mini.py`). Also failing: Lambda' = E_2 x 2Z (split in coordinate 2). The same source cell IS contained in the target E_3 (index 2, not split): see §6.
So *"no free coordinate"* and even *"no split coordinate"* are both insufficient for preservation: **the 3D preservation conjecture of the v004 assessment (Lambda <= Lambda' <= Z^3, e_1,e_2,e_3 not in Lambda' => U <= U') is FALSE.**

## 5. Split targets: the exact criterion

### P5-S4  Generalised slab theorem (PROVED)
Let Lambda' = Lambda'_2 (+) k Z e_3 with Lambda'_2 a rank-2 lattice in the (x_1,x_2)-plane and k >= 1 (coordinate 3 is *split with period k*; k = 1 is the free-coordinate case). Let Q = (Q', q_3), J = floor(q_3/k),
U = U(Lambda'_2,Q') (origin excluded), U^0 = U^0(Lambda'_2,Q') (origin allowed). Then
  (i)  U(Lambda',Q) = [U x [0,k]]  union  [U^0 x [k, kJ]]   if J >= 1,   and   U x {0}   if J = 0;
  (ii) for every Lambda <= Lambda' and every cell C of U(Lambda,Q):   C <= U(Lambda',Q)  <=>  proj_{12}( C cap {x_3 <= k} ) <= U(Lambda'_2,Q').
So the whole 3D decision is a planar decision about a convex polygon (no "S1" failures).
*Proof.* Graver(Lambda') = {(g,0) : g Graver in Lambda'_2} cup {+-k e_3} (a vector (a,t), a != 0 != t, has (a,0) in Lambda' conformally below it). Cells are therefore (planar cell C_2) x {z} or C_2 x [z,z+k], z in kZ, 0 <= z, z+k <= q_3.
The corner (v,z) is zero iff v = 0 and z = 0. For z = 0 the planar factor must avoid the origin (a cell of U); for z >= k it may contain it (a cell of U^0). Taking the union over z gives (i).
(ii) Corners of C have third coordinate in kZ (they lie in Lambda'), so C <= {x_3 <= kJ} and the heights of C lie in [0,kJ]. The part with x_3 < k is covered iff its planar part lies in U; the part with k <= x_3 <= kJ iff its planar part lies in U^0.
The planar part of the second kind is always covered: proj(C) is the zonogon proj(u) + sum[0,1] proj(g_l), proj(g_l) in Lambda'_2, its corners in Lambda'_2 cap Q'; decomposing each proj(g_l) by L1 and tiling by T0 gives tiles whose vertices are subset sums lying
between corner coordinates of proj(C) (as in Z.1) -- origin allowed -- so proj(C) <= U^0. Closedness of U gives (ii) with the closed truncation. QED
**Corollaries.** (a) k = 1 recovers P4-S3 (slab criterion complete; no S1 failures). (b) Every split target has the dilation family of P5-C2 and every dilated free-coordinate target Z x Lambda'_2 with period k is split.
(c) For split targets the failing cells are exactly the hard cells whose truncated projection leaves U; the 57+ failures recorded earlier are all of this type.
*Checked.* (I) the union identity (i) holds pointwise on 36 (lattice, k, box) cases, 30,240 rational grid points (mini.py, brute force; 0 mismatches); (II) criterion (ii) against the pinned exact engine on every hard cell (bounding box <= min(3k_c, cap)) of the index-2 sources in 24 split targets (Lambda'_2 of index <= 3, 8 lattices, times k = 1,2,3; m = 2)
(results/P5_SPLIT_SLAB.json): 574 hard cells, 291 not contained, 0 disagreements between criterion and engine.

## 6. Finite exact census of the no-free-coordinate class (CHECKED; sampling-screened, failures exact)
Scope: targets Lambda' of index 2..6 without a free coordinate (96 lattices), sources Lambda of index 2..5 in Lambda' (8,256 pairs), every hard cell with bounding box <= Q_max = (min(3k_c,12))_c: **24,178 hard cells** (6,825 planar-type 2-cells, 17,353 3-cells), each tested against its own worst box Q_C.
* **192 hard cells fail** (each uncovered sample point re-verified exactly: 0 floating-point false alarms); the failing targets are **19 of 96**: all **12 split** targets (12/12) and **7 of 84 non-split** targets (BCC and six index-6 lattices).
* **77 non-split targets have no failure at all** among 19,794 hard cells (including E_3 and every index-3 and index-5 target). This is a finite sample, *not* a theorem; the v004 sentence "no zero-vertex decomposition occurred" is still an artefact of box scope (corrected in v004, kept).
* The extended run (sources of index 6..9 in all 18 clean targets of index <= 4): 7,794 pairs, 19,877 hard cells, 0 failures, 0 float alarms (results/P5_SCAN3D_EXT.json); still a finite sample.

## 7. Status of the open obligations
| Item | Status |
|---|---|
| CP3-A planar (nested rank-2 lattices, all boxes) | PROVED (P5-P1), independently re-derived; exact corroboration 1,530 hard cells |
| FIELD-I planar corollary | PROVED only for Lambda_x <= Lambda_{C(x)} (P5-P1.a) |
| 3D, target without a free coordinate | **FALSE** (P5-C1/C2); infinite families |
| 3D, target not split in any coordinate | **FALSE in general** (P5-C3, BCC); finite census: 77/84 clean targets |
| 3D, split target | PROVED complete criterion (P5-S4) |
| 3D, which non-split targets preserve U? | OPEN (P5-Q1): target property that avoids the origin-cube hole; classification unknown |
| Hard cells in coordinate planes | PROVED contained (P5-F1) |
| Prior-art audit | LIMITED search done (no source found for the realized-union monotonicity; ingredients standard); NOT a novelty clearance |
| External review of T0/SF, L1, P5-P1 steps (2)-(5) | pending |
| P4-T3, P4-T4 | OPEN (untouched) |
