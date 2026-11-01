# E2-P4 Addendum (v002) -- correction of P4-C1 (append-only; E2-P4 v001 untouched)

Origin: research assessment of E2-P4 v001 (received, `SPEC/E2_P4_ASSESSMENT_RECEIVED.md`).  The assessment is correct.  Re-derived and exactly checked here.

**Withdrawn.**  The equality clause of P4-C1 in `theory/THEOREMS.md` (v001): "for Lambda <= E_3 and n >= 4 even, U(Lambda,[0,n]^3) = U(E_3,[0,n]^3) iff conv F(Lambda) contains the ten
target-hull vertices".  The "only if" half is true and trivial; the "if" half is FALSE.

**Counterexample.**  Lambda = 2Z^3 <= E_3, n = 4, Q = [0,4]^3.  F(Lambda) contains all ten vertices of H = {z in [0,4]^3 : z1+z2+z3 >= 2}, so conv F(Lambda) = H = U(E_3,Q) (P4-T1).  The Graver set of Lambda
is {+-2e_i}, so U(Lambda,Q) = { z in [0,4]^3 : max_i z_i >= 2 } (the box with the origin-adjacent 2-cube removed).  The point (1,1,1) is in U(E_3,Q) (sum 3 >= 2) and not in U(Lambda,Q).
Exact separating point used in the record: (4/7,4/7,10/7) in U(E_3,Q) \ U(Lambda,Q).  Recorded in `data/P4_C1_CORRECTION.json`; independently replayed in RUN_VERIFY shard S8.

**Retained (corrected P4-C1).**  Lambda <= E_3, n >= 4 even  =>  U(Lambda,[0,n]^3) <= U(E_3,[0,n]^3).
Proof: U(Lambda) <= conv F(Lambda) (each cell is the convex hull of its corners, all in F(Lambda)) <= conv F(E_3) = U(E_3) (F inclusion; P4-T1).  No equality is asserted.
Equality needs information about actual source coverage of the target hull; containing the hull vertices is necessary, not sufficient.

**Unaffected.**  P4-T2 (all-m containment for P4-F110) uses only the inclusion chain above; P4-A, P4-L, P4-T1 are unchanged.
**Not claimed.**  Any criterion for equality U(Lambda) = U(E_3).
