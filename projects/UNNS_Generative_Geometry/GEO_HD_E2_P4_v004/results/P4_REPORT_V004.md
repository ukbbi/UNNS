# E2-P4 v004 report -- a proof explaining geometric containment

**Main result (PROVED, P4-P1): planar CP3-A is true.**  For every pair of rank-two lattices Lambda <= Lambda' of Z^2 and every box Q, U(Lambda,Q) <= U(Lambda',Q).  Hence every planar FIELD-I transition with nested relation lattices (ENLARGE, and unchanged coordinates) preserves the realized geometry.

**Why (the explanation).**
1. P4-Z2 (explicit zero-vertex criterion): a source cell can fail to be covered by target cells only if its coordinatewise minimum corner is the origin (it touches every coordinate hyperplane) and all positive/negative parts of its generators lie in the target lattice ("hard cell").  Proof: coordinate-by-coordinate squeeze of u + sum s_i = 0 between 0 and the minimum corner.
2. In the plane a hard cell reaches both axes at corners A = (0,y0), B = (x0,0).  Graver minimality in Lambda forbids A,B adjacent and forbids the other corners from lying on an axis.  Divisibility by the target's axis orders (k',l') then puts all four corners in x/k' + y/l' >= 2 -- outside the origin rectangle of the target's own axis grid, which already consists of target cells.
So the deleted origin cannot hurt: the only cells that see it lie in a region the target covers anyway.

**Also proved (P4-S3).**  For targets with a free coordinate, the v002 slab criterion is complete: U <= U' iff no source point with free coordinate < 1 has planar part outside U(Lambda'_2,Q').  The "S1" failure type cannot occur (projection of a source cell is always inside the origin-allowed planar union).

**Corrections recorded.**  P4-K1 (v003) is false as a lattice statement (assessment counterexample, re-verified; its cell is contained by P4-P1).  The v003 remark that no-free-coordinate targets had no zero-vertex cells was a sampling artifact of small boxes.

**Checks (finite, supporting the proof, not replacing it).**  P4-Z2 vs brute force: 45,692 cells builder-side, 3,023 more with independent code, 0 mismatches.  Hard-cell structure (1)-(6) holds on all 183 robustly flagged planar cells found (pairs index <= 10, boxes 2..8) and 17 re-checked independently with grid containment (RUN_VERIFY S17).

**Honest scope.**  P4-P1 rests on P4-Z1 (zonotopal-tiling soundness), whose proof is elementary but has not been externally reviewed; builder and verifier share an author; no prior-art search was done, so nothing is claimed as new; C3 NOT claimed.
**Still open.**  Preservation for 3D targets with no free coordinate (P4-Z2 gives the exact shape of any obstruction: a hard cell touching all three coordinate planes; a 3D analogue of the planar argument is not proved); P4-T3/T4; prior-art audit.
