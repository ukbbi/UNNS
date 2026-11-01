# E2-P4 theorems (v001).  Status vocabulary: PROVED (complete argument, finite parts exactly certified) / FINITE-EXACT / OPEN.

Nothing here is claimed to satisfy GEO-HD-1 criterion C3.  All results are elementary or specialisations of E2-P3 / GEO-I v012 reductions.

## P4-A  Arithmetic of P4-F110  (PROVED, elementary)
For every integer m >= 1:  x_m = 2*110^(4m)/9 satisfies C(x_m) = 110^(4m)/3 = y_m; the active primes (2,5,11) and the box Q_m = [0,2m]^3 are the
same for x_m and y_m.
*Proof.*  num(x_m) = 2^(4m+1) 5^(4m) 11^(4m), so d^2 | num iff d = 2^a 5^b 11^c with a,b,c <= 2m.  Mod 9: 5 = 2^5 = 2^(-1), 11 = 2, ord_9(2)=6, so
2^a 5^b 11^c = 2^(a-b+c) and d = 1 (mod 9) iff a-b+c = 0 (mod 6).  Every d in D is 1 mod 9, hence 9 | G.  10 = 2*5 and 55 = 5*11 are in D
(exponent vectors (1,1,0), (0,1,1)); gcd(10-1, 55-1) = gcd(9,54) = 9, so G | 9 and G = 9.  10^(2m) and 55^(2m) are in D (vectors (2m,2m,0),
(0,2m,2m)); lcm = 110^(2m), and every d in D divides 110^(2m); so L = 110^(2m).  C(x_m) = (2+1)*110^(4m)/9 = 110^(4m)/3.  num(y_m)=110^(4m):
v_p = 4m for p = 2,5,11, box (2m,2m,2m).  QED.   (Reproduced for m = 1..12 by exact enumeration; m = 1,2,3 also by the frozen FIELD-I engine and
m = 1,2,3 by the independent brute-force audit.)

## P4-L  Relation lattices  (PROVED, elementary)
Lambda_9 = { a-b+c = 0 mod 6 },  Lambda_3 = { a+b+c = 0 mod 2 } = E_3,  Lambda_9 strictly inside Lambda_3.  Orders mod 9: (6,6,6), |H_9| = 6 < 216;
orders mod 3: (2,2,2), |H_3| = 2 < 8.  **Both lattices are nonrectangular.**
*Proof.*  Step 1 of P4-A for Lambda_9;  mod 3 all of 2,5,11 are -1, so chi_3 = (-1)^(a+b+c).  a-b+c = 0 mod 6 implies a+b+c = (a-b+c)+2b even; (2,0,0) is in
E_3 and not in Lambda_9.  QED.

## P4-T1  Hull theorem for E_3  (PROVED; finite part exactly certified and independently replayed)
Let n >= 4 be even, Q = [0,n]^3.  Then U(E_3, Q) = conv F(E_3,Q) = { z in [0,n]^3 : z1+z2+z3 >= 2 }.  (For n = 2 this FAILS: 94 gap pieces, m=1.)
*Proof.*
(1) *Hull.*  F contains all cube vertices except 0 (even coordinate sums) and (2,0,0),(0,2,0),(0,0,2).  The polytope cube cap {sum >= 2} has exactly these 10
vertices (exact vertex enumeration, n = 2..12) and every point of F satisfies its inequalities, so conv F equals it.
(2) *Cube tiling.*  2e_i are Graver moves of E_3 (E_3's Graver basis is {2e_i, e_i +- e_j}; checked by brute force).  For every w in (2Z)^3 cap [0,n-2]^3, w != 0, the
eight corners w + {0,2}^3 have even sum, lie in the box and are nonzero, so C(w) is a 3-cell of K_abs.  These cubes tile [0,n]^3 minus the corner cube C(0).
(3) *Corner.*  C(0) cap H' = [0,2]^3 cap {sum >= 2}.  For n = 4 the engine decomposes H'_4 into pieces each inside one maximal cell of the box-4 complex
(exact certificate, results/P4_CERTIFICATES.json:n4_target_hull_cover, 0 gap nodes, independently replayed by RUN_VERIFY S4).  Cells of the box-4 complex are cells of the
box-n complex for all n >= 4: the Graver set of E_3 in [-n,n]^3 is the same for every n >= 2 (a conformally minimal vector lies in the box of its own size), and F(E_3,4) is inside
F(E_3,n).  (Checked: cells(4) in cells(6) in cells(8).)  Since H'_n cap [0,2]^3 = H'_4 cap [0,2]^3, the corner is covered.   QED
*Scope.*  Elementary: parallelotope tiling plus one finite exact certificate.  It is the three-dimensional analogue of the planar GEO-I v012 hull-coverage regime (G12-T8).

## P4-T2  P4-F110 realized transport  (PROVED for all m >= 1; scoped theorem)
For every m >= 1:  U(Lambda_9, Q_m) is strictly contained in U(Lambda_3, Q_m); transport class **SOURCE_CONTAINED**; and U(Lambda_3,Q_m) is not contained in U(Lambda_9,Q_m).
*Proof.*  m = 1: direct exact certificates (2 source maximal cells covered by 18 target maximal cells; independent replay).  m >= 2: U(Lambda_9) is inside conv F(Lambda_9)
(cells are convex hulls of corners in F), which is inside conv F(Lambda_3) (F inclusion, P4-L), which equals U(Lambda_3) by P4-T1 (n = 2m >= 4).  Strictness and the reverse
direction: (2,0,0) is a vertex of conv F(Lambda_3) lying in F(Lambda_3) (so in U(Lambda_3)) but not in F(Lambda_9); a vertex of H' that lies in conv F(Lambda_9) subset H' must be
a vertex of conv F(Lambda_9), hence in F(Lambda_9) -- contradiction; therefore (2,0,0) is not in U(Lambda_9).  (Exact point certificates for m=1,2,3 in results/P4_CERTIFICATES.json.)  QED
*Direct cross-check.*  m = 2: the exact engine independently returns CONTAINED (see results/P4_GEOMETRY.json:geometry_m2 when the opt-in stage m2 has been run).  m >= 3 direct: UNAVAILABLE_COST.

## P4-C1  Predictive criterion for E_3 targets  (PROVED; the only P4-T5 instance delivered)
*Input:* a lattice Lambda subset of E_3 (any sublattice, FIELD-I realised or not) and an even n >= 4.  *Prediction:* U(Lambda,[0,n]^3) is contained in U(E_3,[0,n]^3), with equality iff
conv F(Lambda) contains the 10 vertices of P4-T1.  *Proof:* P4-T1 plus U(Lambda) inside conv F(Lambda).  *Cost:* O(|F|) lattice-point tests, no cell reconstruction.
*Unsupported:* targets that are not hull-covered (e.g. n = 2, planar hollow boxes), where F inclusion does not imply geometric containment.

## P4-O1  Holes are not obstructions  (FINITE-EXACT observation, falsification P4-F4)
At m = 1 the target Lambda_3 is NOT hull-covered (94 gap pieces certified) yet U(Lambda_9,Q_1) misses every gap piece.  So existence of target holes does not imply noncontainment.
This is an observation about one specimen, not a theorem.

## Not proved / not attempted in this release
* CP3-A for planar hollow-box and sub-threshold targets (P4-E3 NOT STARTED);  P4-T3 (parameter-family classification beyond P4-F110), P4-T4 (essentially 3D coupled-target
  obstruction theory) and a coupled-target census (P4-E4) are NOT STARTED.  Prior-art / novelty review (P4-E5) is partial: see SOURCE_OVERLAP.md.
