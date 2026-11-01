# E2-P4 v003 report -- theorem-focused continuation (assessment priorities 1-5)

Question: *when does lattice inclusion force realized geometric containment?*

| Priority | Outcome |
|---|---|
| 1. CP3-A (planar) | **OPEN.**  New adversarial scan: 9,497 pairs (source index <= 48), boxes [1,8]^2, 309,764 exact-or-screened runs, 233 flagged (all contained), 0 failures.  The tempting reduction to rectangular targets fails (17/40 flagged planar examples have no free coordinate). |
| 2. No free coordinate in 3D | **Conjecture P4-K1, not proved.**  304,731 random runs, 0 zero-vertex flagged => all proved contained; no counterexample. |
| 3. Converse of slab criterion | **PROVED for free-coordinate targets:** P4-S2 gives U(Lambda') exactly (planar unions glued along the free axis); containment <=> no S0 failure and no S1 failure.  All 57 recorded failures are S0 (the v002 slab obstruction); S1 failures are not excluded (P4-H0 false) but never occur in scope. |
| 4. 21 UNAVAILABLE_COST rows | **RESOLVED: all CONTAINED** via P4-S2 (independent grid corroboration, S16).  The spatial scan has no unresolved row. |
| 5. Prior art | **Not done.**  No literature search; everything proved is elementary and not claimed as new. |

Characterization of how failure happens (within free-coordinate targets, proved): a source point with free-axis coordinate below 1 whose planar part is not in U(Lambda'_2), or a point with coordinate >= 1 whose planar part is not in the origin-allowed union U0.  Planar failures of the first kind are the only ones observed.
New elementary facts: P4-S2 (with its corollaries); P4-H0 is false (counterexample E_2, box (1,2)).
Honest status: C3 NOT claimed.  Builder and verifier share an author.  Project STATUS/CHANGELOG/MANIFEST untouched.  v001 and v002 preserved.
