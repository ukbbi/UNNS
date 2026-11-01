# v005 counterexamples and corrected conjectures (append-only; keeps all earlier records)

## CE-A  The v004 three-dimensional conjecture is FALSE
Conjecture (v004 assessment, "P5-K2" here): Lambda <= Lambda' <= Z^3, e_1,e_2,e_3 not in Lambda'  =>  U(Lambda,Q) <= U(Lambda',Q).
Counterexample: Lambda = 2E_3, Lambda' = 2Z^3, Q = (2,4,2); source cell C = P((0,2,2); (0,2,-2), (2,-2,0)); witness p = (2/3,5/3,5/3) in C, not in U(2Z^3,Q) (hand proof: THEOREMS_V005 P5-C1).
Mechanism: C is a hard cell lying in the plane x+y+z = 4, passing through the open cube (0,2)^3, which is the only cell of the axis grid 2Z^3 removed by the deleted origin; the target has no other cell there.
Why the search missed it earlier: the sampled boxes (sum <= 8) and sources (index <= 36, targets of index <= 12) did contain such pairs only for very specific lattices; v003 reported "0 zero-vertex flagged" for no-free targets because its boxes were too small (already corrected in v004).
Recorded as: FALSE (P5-C1), with an infinite family by dilation (P5-C2).

## CE-B  "No split coordinate" is also insufficient
Lambda = 2E_3 <= Lambda' = BCC = {z_1 = z_2 = z_3 mod 2}, Q = (2,4,2): NOT_CONTAINED (engine certificate verified by the independent checker). BCC is not split in any coordinate.

## CE-C  Free-coordinate pairs are not special
CE0 (E_3 <= Z^3, Q = (1,2,1)) is the unscaled form of CE-A; the 57 earlier failures with a free coordinate are all dilatable to targets with axis orders >= 2 (P5-D1).

## Contrast
2E_3 <= E_3, Q = (2,4,2): the same cell is contained; E_3 itself (non-split, index 2) shows no failure among 3,000+ hard cells in the census. The distinction between E_3 and BCC is not yet explained (P5-Q1).

## Corrections to earlier statements
* P4-K1 (v003, lattice version) stays FALSE (v004). New: its "geometric" replacement "no free coordinate => U preserved" is also FALSE.
* The scope sentence "every planar FIELD-I transition" in the v004 closing remark of P4-P1 is replaced by: fixed-coordinate planar transitions with Lambda_x <= Lambda_{C(x)} (P5-P1.a).
* The v004 statement "3D preservation for targets without a free coordinate: OPEN" is resolved negatively; the question is re-posed as P5-Q1 for targets that are not split (below).

## Open question P5-Q1
Characterise the lattices Lambda' <= Z^3 (equivalently, after P5-D1, the normalised lattices D^{-1} Lambda' containing Z^3) for which U(Lambda,Q) <= U(Lambda',Q) holds for ALL Lambda <= Lambda' and all boxes Q.
Data: among 84 non-split targets of index 2..6 without a free coordinate, 77 show no failure (including E_3 and every target of index 3 and 5); the 7 failing ones are BCC and six lattices of index 6.
Not claimed: that the 77 preserve U.
