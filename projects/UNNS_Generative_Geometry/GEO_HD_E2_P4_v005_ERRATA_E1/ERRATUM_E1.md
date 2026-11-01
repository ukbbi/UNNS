# Erratum E1 to GEO_HD_E2_P4_v005 -- P5-S4(ii) boundary (append-only; v005 files are NOT modified)

Source: external audit of v005 (reproduced here independently with the v005 code).

## Error
P5-S4(ii) states, for a split target Lambda' = Lambda'_2 (+) kZ e_3 and a cell C of U(Lambda,Q), Lambda <= Lambda':
  C <= U(Lambda',Q)  <=>  proj_12( C cap {x_3 <= k} ) <= U(Lambda'_2,Q').
This is false for cells with no point below height k. The proof's last line ("closedness of U gives (ii) with the closed truncation") is valid only when C cap {x_3 < k} is nonempty: then C cap {x_3<k} is convex and its closure is C cap {x_3<=k}.

## Counterexample (audit case, reproduced)
Lambda = 2Z^2 (+) 2Z, Lambda' = Z^2 (+) 2Z (k = 2), Q = (2,2,2), C = [0,2]^2 x {2} = P((0,0,2); (2,0,0),(0,2,0)).
C is a valid source cell and the engine says CONTAINED (so does the brute-force union: (1/2,1/2,2) is in U(Lambda',Q)). The v005 criterion says NOT contained, because proj(C) contains (1/2,1/2) which is outside the origin-excluded planar union U.
Reason: at height x_3 = k the target already contains the corner (0,0,k) != 0, so the slice at height k is U^0, not U (see (i)).

## Corrected statement (PROVED)
P5-S4(ii)' : C <= U(Lambda',Q)  <=>  [ min_{x in C} x_3 >= k ]  or  [ proj_12( C cap {x_3 <= k} ) <= U(Lambda'_2,Q') ].
Equivalently: C <= U' iff proj_12( C cap {x_3 < k} ) <= U.  (A cell with min x_3 >= k is always contained: its planar part lies in U^0 by the tiling argument already given in the proof of (ii), and the slice heights k..kJ are covered by U^0 x [k,kJ] by (i).)
Proof of the corrected form: by (i), the slice at height z<k is U, at z>=k it is U^0. Slices at z>=k are covered (argument in v005). So C <= U' iff proj(C cap {z<k}) <= U. If C cap {z<k} is nonempty its closure is C cap {z<=k} and U is closed, giving the closed form; if empty the condition is vacuous.

## What remains valid
* Hard cells have min x_3 = 0 < k, so the closed form is correct for them: all 574 hard-cell comparisons of v005 stand. The 3D census failures (192 hard cells) are unaffected; all P5-C1/C2/C3, P5-D1, P5-F1, P5-P1 results are unaffected. P5-S4(i) (union identity) is unaffected.
* Corollary (c) of P5-S4 ("failing cells are exactly the hard cells whose truncated projection leaves U") remains true: only cells with a point below height k can fail, and those fail iff the truncated projection leaves U; non-hard cells with min x_3 < k and with the closed form failing are also possible in principle (the statement is about hard cells for the census).

## New regression evidence
* regress_audit_case.py: engine CONTAINED vs v005 criterion False (the audit case): reproduces the error.
* regress_allcells.py (ALLCELLS_RESULT.json): ALL cells (not only hard), L2 in {Z^2, (1,1;0,2), (1,0;0,2)}, k = 1,2, three boxes each, sources of index 2: 6,890 cells; v005 criterion wrong on 422; corrected criterion wrong on 0 (engine verdict as reference).

## Record reconciliation
The archive shows 63 stored passing checks; the device run showed 64. The 64th is S0 "v004 baseline zip sha256 unchanged", which runs only when GEO_HD_E2_P4_v004.zip sits next to the release folder (it does on the device). Not a discrepancy in the mathematics.

Status: P5-S4(ii) superseded by (ii)'. Same-author correction following an external audit finding.
