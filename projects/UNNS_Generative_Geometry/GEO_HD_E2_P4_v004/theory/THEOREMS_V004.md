# E2-P4 v004 -- a proof explaining geometric containment (continuation of THEOREMS.md, _V002, _V003; all preserved)

Status vocabulary: PROVED (complete argument) / CHECKED (finite computation) / OPEN.  Everything proved here is elementary.  No prior-art search was done (see audit).  C3 is NOT claimed.
Notation: Lambda <= Lambda' lattices of Z^k, Q = prod [0,q_c], F(M) = (M cap Q) \ {0}; a cell P(u;g_1..g_j) has independent generators g_i Graver in Lambda (conformally minimal) and all 2^j corners in F(Lambda);
U(M,Q) = union of cells.  For a vector g, g^- = componentwise min(g,0) and g^+ = componentwise max(g,0), so g = g^+ + g^-.

## P4-Z2  Explicit zero-vertex criterion (PROVED, any dimension)
Let C = P(u;g_1..g_j) be a cell (corners in Q) and m(C) = u + sum_i g_i^- the coordinatewise minimum of its corners.  A zero-vertex decomposition of C (vectors s_i in Lambda' conformally below g_i with u + sum s_i = 0) exists  <=>  m(C) = 0 and g_i^- in Lambda' for every i;  and then s_i = g_i^-.
*Proof.*  (=>)  Fix a coordinate c.  Each s_{i,c} lies between 0 and g_{i,c}, so  s_{i,c} >= min(g_{i,c},0).  Hence 0 = u_c + sum_i s_{i,c} >= u_c + sum_i min(g_{i,c},0) = m_c.  But m_c is the c-th coordinate of the corner u + sum_{i: g_{i,c}<0} g_i, which is >= 0.  So all inequalities are equalities: m_c = 0 and s_{i,c} = min(g_{i,c},0) for all i.  (<=) take s_i = g_i^-, conformally below g_i.  QED
**Corollary P4-Z2.a (robust form).**  A cell has 2^j representations (base corner, generator signs), for which the negative part of the outgoing generator (+-g_i)^- is g_i^- or -g_i^+.  Because P4-Z1 is valid for every representation, C <= U(Lambda',Q) unless
   m(C) = 0 (the cell touches every coordinate hyperplane)  and  g_i^+, g_i^- in Lambda' for all i.   (*)
Cells satisfying (*) are *hard*.  (Checked: P4-Z2 agrees with the brute-force search on all 19,258 planar and 26,434 spatial maximal cells of the lattice scans.)
**Corollary P4-Z1.a (edges).**  Hard 1-cells do not exist (v002 proof), consistent with (*).

## P4-P1  Planar containment: CP3-A is TRUE  (PROVED)
**Theorem.**  Let Lambda <= Lambda' be rank-two lattices of Z^2 and Q = [0,a] x [0,b] any box.  Then U(Lambda,Q) <= U(Lambda',Q).  In particular CP3-A holds for every planar FIELD-I transition (the relation lattices are nested and the coordinates do not change).
*Proof.*  Points and edges are covered (a point of F(Lambda) is a point of F(Lambda'); edges by P4-Z1.a).  Let C be a 2-cell with generators g,h.  If (*) fails, C <= U(Lambda',Q) by P4-Z1/Z2.  So let C be hard: m(C) = 0 and g^+,g^-,h^+,h^- in Lambda'.
Let R' = Lambda' cap (axes) = k'Z x l'Z with k',l' >= 1 minimal (exists: finite index).  Then k'e_1 and l'e_2 are Graver in Lambda' (a vector of Lambda' conformally below k'e_1 is (t,0) with 0 < t <= k', so t = k').
(1) *Axis corners.*  m(C) = 0 gives a corner A with x = 0 and a corner B with y = 0; both are nonzero, so A = (0,y0), B = (x0,0) with x0,y0 > 0, and A,B are in Lambda.
(2) *A,B are opposite corners.*  If A,B were adjacent, w = B - A = (x0,-y0) = +-g or +-h would be Graver in Lambda; but B = (x0,0) and -A = (0,-y0) are nonzero elements of Lambda conformally below w and different from w: contradiction.
(3) *Shape.*  Name the other corners D = A + g', E = A + h' where {g',h'} = {+-g,+-h} are the edge vectors at A, so B = A + g' + h'.  Corners in Q give g'_1,h'_1 >= 0 and, from g'_2 + h'_2 = -y0 with y0 + g'_2 >= 0, y0 + h'_2 >= 0, also g'_2,h'_2 <= 0.  Write g' = (g1,-g2), h' = (h1,-h2) with g1,h1,g2,h2 >= 0, g1 + h1 = x0, g2 + h2 = y0; D = (g1,h2), E = (h1,g2).
(4) *D,E are off the axes.*  If g1 = 0, then D = (0,h2) is nonzero so h2 > 0, and h' = B - D = (x0,-h2) is Graver in Lambda although B = (x0,0) and -D = (0,-h2) lie in Lambda and are conformally below it: contradiction.  If h2 = 0 then D = (g1,0), g1 > 0, g2 = y0 and g' = (g1,-y0) = D + (-A) splits conformally: contradiction.  The same two arguments for E (h1 = 0 resp. g2 = 0) give  g1,h1,g2,h2 > 0.
(5) *Hardness gives divisibility.*  g'^+ = (g1,0), h'^+ = (h1,0), -g'^- = (0,g2), -h'^- = (0,h2) are in Lambda' (they are the parts g^+,..; note {g'^+,g'^-,h'^+,h'^-} = {g^+,g^-,h^+,h^-} up to sign), so k' | g1, k' | h1, l' | g2, l' | h2; thus g1,h1 >= k', g2,h2 >= l', x0 >= 2k', y0 >= 2l', and x0 in k'Z, y0 in l'Z.
(6) *Half-plane.*  All four corners satisfy x/k' + y/l' >= 2:  A: y0/l' >= 2;  B: x0/k' >= 2;  D = (g1,h2): >= 1 + 1;  E = (h1,g2): >= 2.  C is the convex hull of its corners, so every p in C has p_1/k' + p_2/l' >= 2, hence p_1 >= k' or p_2 >= l'.
(7) *Covering by the R'-grid.*  C <= [0,x0] x [0,y0] <= Q (x0 <= a, y0 <= b as B,A are corners).  The rectangles R_ij = [ik',(i+1)k'] x [jl',(j+1)l'] (0 <= i < x0/k', 0 <= j < y0/l') lie in Q, have all corners in R' cap Q, and all corners are nonzero except for R_00; so each R_ij with (i,j) != (0,0) is the cell P(corner;k'e_1,l'e_2) of U(Lambda',Q).  A point p of C lies in some R_ij; if p in R_00 only, then p_1 < k' and p_2 < l', contradicting (6); if p in R_00 and in another rectangle we are done; points on the far edges of R_00 lie in R_10 or R_01 (they exist since x0 >= 2k', y0 >= 2l').  Hence C <= U(Lambda',Q).  QED
*Remarks.*  (a) The proof shows what a zero vertex *means*: it forces the source cell to be a fat parallelogram spanning the two axes at distance >= (2k',2l') from the origin in the R'-metric, hence entirely inside the region already covered by the axis grid of the target.  This is the "explanation" of CP3-A: the deleted origin can only matter for cells that reach both axes, and such cells lie outside the origin rectangle of the target's axis lattice.
(b) The proof uses only: Graver minimality of the generators in Lambda (steps 2,4), nestedness (Lambda <= Lambda'), and P4-Z1 (soundness of the zonotopal-tiling argument).  It does not use arithmetic of FIELD-I and holds for every box.
(c) Checked: all robustly flagged planar cells of the lattice scans have exactly the structure (1)-(6) (results/P4_HARD_CELLS_*.json, RUN_VERIFY S17).

## P4-S3  The slab criterion is complete; S1 failures are impossible  (PROVED)
Let Lambda' have a free coordinate i (e_i in Lambda'), q_i >= 1, and Lambda <= Lambda'.  Then
   U(Lambda,Q) <= U(Lambda',Q)   <=>   there is no point p in U(Lambda,Q) with p_i < 1 whose planar part (the other two coordinates) lies outside U(Lambda'_2,Q').
*Proof.*  By P4-S2, U(Lambda',Q) = U(Lambda'_2,Q') x [0,1) union U0(Lambda'_2,Q') x [1,q_i].  (=>) is immediate.  (<=)  Let p in C, a source cell.  If p_i < 1 the hypothesis gives p in U(Lambda').  If p_i >= 1 we show proj_i(p) in U0(Lambda'_2,Q'): the projection of C is a zonogon with base proj(u) and generators proj(g_l) in Lambda'_2 (since e_i in Lambda'), its corners lie in Lambda'_2 cap Q' (origin allowed), and by the tiling argument of P4-Z1 (conformal Graver decomposition of each proj(g_l) in Lambda'_2, a fine zonotopal tiling of proj(u) + sum [0,1] proj(g_l) -- a zonogon containing proj(C)), every tile is a Graver cell with all vertices in Lambda'_2 cap Q' (coordinates between the minimum and maximum of the projected corner coordinates).  Origin-allowed cells impose no further condition, so proj(C) <= U0(Lambda'_2,Q').  QED
*Consequences.*  (i) the v002 slab criterion (S1.a) is both sufficient and necessary; (ii) the "S1" failure mechanism of v003 does not exist; (iii) the 57 recorded failures are *all* the possible type of failure for free-coordinate targets.

## Corrections to earlier statements (append-only)
* **P4-K1 (v003) is FALSE as a lattice statement** ("no free target coordinate => no zero-vertex decomposition").  Counterexample (from the v003 assessment): Lambda = {a even, b - a = 0 mod 6, c even}, Lambda' = E_3, Q = (6,6,2), cell u = (0,6,0), g = (2,-4,0), h = (4,-2,0): m(C) = 0, g^- = (0,-4,0), h^- = (0,-2,0) in Lambda'.  Re-verified here (S17).  The cell lies in the plane z_3 = 0 where the nested planar sublattices satisfy P4-P1, hence it IS contained.  My v003 random search reported "0 zero-vertex flagged" for no-free-coordinate targets because its boxes were too small (flagged cells need box >= (2k',2l') in two coordinates); the sentence "no zero-vertex decomposition occurred at all" in v003 must be read as an artifact of that scope.
* The v003 statement that the 17/40 planar flagged examples without a free coordinate block the reduction to rectangular targets stays correct, but is superseded by P4-P1, which proves planar containment directly.

## Status of the open obligations
| Item | Status |
|---|---|
| CP3-A (planar nested lattices, all boxes) | **PROVED** (P4-P1) |
| Converse of slab criterion / S1 failures | **PROVED** (P4-S3): complete for free-coordinate targets |
| 21 UNAVAILABLE_COST rows | resolved CONTAINED (v003) |
| Preservation for 3D targets WITHOUT a free coordinate | OPEN.  P4-Z2 gives the exact shape of any obstruction: a hard cell touching all three coordinate planes with all g_i^+-,g_i^- in the target.  A 3D analogue of steps (2)-(7) is not proved. |
| Prior-art audit | NOT DONE |
| P4-T3 (parameter-family classification), P4-T4 | OPEN |
