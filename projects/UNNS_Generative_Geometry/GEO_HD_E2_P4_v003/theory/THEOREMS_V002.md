# E2-P4 v002 theorems (continuation of theory/THEOREMS.md; v001 text is preserved unchanged).  Status: PROVED / FINITE-EXACT / OPEN.

All proved statements below are elementary.  Nothing here is claimed to satisfy GEO-HD-1 criterion C3.  Notation as in `theory/DEFINITIONS.md`:
for a lattice Lambda of Z^k and box Q = prod [0,q_i], F(Lambda,Q) = (Lambda cap Q) \ {0}; Graver set = conformally minimal nonzero vectors of Lambda;
a *cell* is P(u;g_1..g_j) = u + sum [0,1] g_i with g_i Graver (independent) and all 2^j corners in F; U(Lambda,Q) = union of cells.

## P4-C1 (corrected)  (PROVED; supersedes the v001 statement)
Lambda <= E_3 (even coordinate sum), n >= 4 even  =>  U(Lambda,[0,n]^3) <= U(E_3,[0,n]^3).  The v001 equality clause is WITHDRAWN (counterexample 2Z^3; see
`ERRATA/E2_P4_ADDENDUM_V002_P4C1_CORRECTION.md`).

## P4-Z1  Zero-vertex sufficient condition for containment  (PROVED, elementary)
Let Lambda <= Lambda' be lattices of Z^k, Q a box, C = P(u;g_1..g_j) a cell of U(Lambda,Q).  Call a *zero-vertex decomposition* of C a choice of vectors s_1..s_j in Lambda',
each conformally below g_i (componentwise between 0 and g_i, extremes allowed), with u + s_1 + ... + s_j = 0.
**If C has no zero-vertex decomposition, then C <= U(Lambda',Q).**  Hence if no maximal cell of U(Lambda,Q) has one, U(Lambda,Q) <= U(Lambda',Q).
*Proof.*  Write each g_i as a conformal sum of Graver elements of Lambda' (g_i is in Lambda <= Lambda'; Graver bases conformally generate): g_i = sum_a h_{i,a}, all h_{i,a} in Lambda',
conformally minimal in Lambda', each conformally below g_i; each |h_{i,a}| <= |g_i| <= q, so every h lies in the Graver set of Lambda' computed in [-q,q].  Put Z' = sum_{i,a} [0,1] h_{i,a}.
Since lambda_i g_i = sum_a lambda_i h_{i,a}, we have C <= u + Z'.  Take a fine zonotopal tiling of u + Z' by parallelepipeds (it exists for every vector configuration, repeated or parallel vectors
allowed); each tile is v + sum_{a in B} [0,1] h_a for a linearly independent set B of pieces, and every tile vertex is u + sum of a sub-multiset of the pieces, i.e. of the form
u + s_1 + ... + s_j with s_i the sum of a subset of the pieces of g_i; such an s_i is in Lambda' and conformally below g_i.  Coordinatewise, u_c + sum_i s_{i,c} lies between the minimum and
the maximum of the corner coordinates of C, so every tile vertex lies in Q.  By hypothesis no tile vertex is 0.  Hence every tile has all corners in F(Lambda',Q), its generators are independent Graver
elements of Lambda', i.e. each tile is a cell of U(Lambda',Q), and C <= union of tiles <= U(Lambda',Q).  QED
*Remarks.*  (a) The condition reads only (u,g_i) and a membership oracle for Lambda'; the target complex is never built.  (b) It is one-sided: a flagged cell can still be contained
(51 planar and 18 spatial flagged lattice-level runs are CONTAINED); the screen is a sufficient condition, not a criterion.

### P4-Z1.a  Edges never obstruct  (PROVED)
For j = 1 (edges) a zero-vertex decomposition never exists, so every edge of U(Lambda,Q) lies in U(Lambda',Q).
*Proof.*  Suppose u + s = 0 with s in Lambda' conformally below g.  If g_c >= 0 then s_c >= 0 and u_c >= 0 force u_c = s_c = 0.  If g_c < 0 then s_c in [g_c,0] and u_c = -s_c; the corner u+g >= 0 gives
g_c >= s_c, so s_c = g_c.  Thus s = g^- (the negative part of g) and u = -g^-, so g^- = -u is in Lambda and is conformally below g.  By Graver minimality of g in Lambda, g^- is 0 or g.
g^- = 0 gives u = 0, excluded; g^- = g gives u + g = 0, a corner equal to 0, excluded.  QED

## P4-S1  Slab lemma  (PROVED, elementary)
Let Lambda' be a lattice of Z^3 containing e_i (*free coordinate i*; arithmetically, for FIELD-I targets Lambda'_{b'} = ker chi_{b'}: prime p_i = 1 mod b'), let Q = prod [0,q_j] with q_i >= 1,
Lambda'_2 = Lambda' cap {z_i = 0} (a planar lattice in the other two coordinates), Q' the planar box.  Then Lambda' = Lambda'_2 (+) Z e_i and, for 0 < c < 1,
**(x',c) is in U(Lambda',Q)  iff  x' is in U(Lambda'_2,Q')**  (x' placed in the two non-i coordinates).
*Proof.*  Graver elements of Lambda' are the (g,0) with g Graver in Lambda'_2 and +-e_i: if v = (v',v_i) has v' != 0 and v_i != 0 then (v',0) and (0,v_i) are conformally below v, so v is not minimal;
(g,0) is minimal in Lambda' iff g is minimal in Lambda'_2.  A cell containing a point with 0 < c < 1 must contain the generator e_i (all other generators have i-th coordinate 0, so its c-range is a single
integer), and its base has c = 0 (base coordinates are >= 0 and its c-range is [c_0,c_0+1] containing c).  Such a cell is C_2 x [0,1] with C_2 = P(u';g'_1..) planar; its corners are (v',0),(v',1) for the corners v'
of C_2.  They are in F(Lambda',Q) iff v' in Lambda'_2 cap Q' and (v',0) != 0, i.e. iff all corners of C_2 are in F(Lambda'_2,Q'), i.e. C_2 is a cell of U(Lambda'_2,Q'); the corners (v',1) are automatically nonzero and inside Q (q_i >= 1).
Conversely every planar cell C_2 of U(Lambda'_2,Q') gives the cell C_2 x [0,1].  So U(Lambda',Q) cap {0 < c < 1} = U(Lambda'_2,Q') x (0,1).  QED
**Corollary P4-S1.a (obstruction criterion, sufficient).**  Under the hypotheses above, if some point p in U(Lambda,Q) has 0 < p_i < 1 and its planar part is not in U(Lambda'_2,Q'), then U(Lambda,Q) is NOT contained in U(Lambda',Q).
The obstruction is a *planar target gap times the thin slab above the free coordinate*; it is inherited from the planar target and is not a new genuinely three-dimensional coupling phenomenon.

## Finite-exact results (scope recorded in `data/SEARCH_LIMITS_V002.json`)
* **P4-E3 planar.**  Lattice scan: all 1,938 sublattice pairs Lambda < Lambda' of Z^2 with [Z^2:Lambda] <= 24 in all boxes [1,6]^2: 42,287 exact runs, 0 failures (51 runs zero-vertex flagged, all CONTAINED).
  The 846 open-class rows of the E2-P3 reference corpus (including the 62 E2-P2 cases: 14 hollow-box, 48 sub-threshold): 564 hull-covered, 282 hollow rows, **all 282 zero-vertex free, hence contained by P4-Z1**; 0 failures.
  New window (13 primes <= 41, boxes [1,7]^2, b up to 4000, beyond the E2-P3 window q <= 6, b <= 400): 1,443 residual rows, 0 zero-vertex flagged, 0 failures.  **CP3-A remains OPEN as a general statement**; P4-Z1 reduces it to the question
  whether every planar pair that is not hull-covered has no zero-vertex cell, or is contained anyway (the 51 flagged lattice-level planar runs show the screen is not necessary).
* **P4-E4 spatial.**  Lattice level (lattice-only candidates, never FIELD-I results): 153 nonrectangular targets of index 2..6, 2,608 pairs, 23,302 box runs: 36 NOT_CONTAINED, all with free coordinate, all zero-vertex flagged, all slab witnesses (planar target with 4 fibre points = E2 in box (2,2) for 51 of the 57 lattice-level + FIELD-I failures; a 3-point planar target in boxes (3,2)/(2,3) for the other 6).
  FIELD-I (pool of 6 primes, q <= 3, b <= 100, odd exponents allowed): 191,376 states, 3,845 rows with nonrectangular target: 21 NOT_CONTAINED (exact witnesses, all essential 3D: full coordinate support, all coordinate-face restrictions contained),
  116 exact CONTAINED (63 with a free coordinate, 53 without), 3,687 proved by P4-Z1, **21 UNAVAILABLE_COST** (box (3,3,3), recorded, not decided).  On the 1,418 free-coordinate rows a slab witness exists exactly for the 21 NOT_CONTAINED rows (0 contradictions; the 21 unavailable rows have none).
  On the 2,427 rows with no free coordinate (indecomposable-type targets): **0 failures** (2,374 proved by P4-Z1, 53 exact CONTAINED).

## OPEN
CP3-A (general planar); converse of P4-S1.a beyond the scope above (a complete predictor); the 21 UNAVAILABLE_COST rows; a proved preservation theorem for targets without a free coordinate;
prior-art audit; P4-T3 (parameter-family classification) and P4-T4 (higher dimension).
