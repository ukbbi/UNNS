# E2-P2 — Addendum 003: scope of the planar sampling window (found during E2-P3, append-only)

E2-P2 `cell_transport.planar_transport(cx_s, cx_t, box)` was called with `box = q[0]`, and `samples_for` bounds the arrangement by the
SQUARE [0, q[0]]².  For boxes with q[0] < q[1] (63 of the 326 geometry rows: 55 ENLARGE, 8 SHRINK) the window therefore did not cover the part of
the box with y > q[0], so the E2-P2 sampling argument was *incomplete as a proof* for those rows.
**Outcome check.**  Every one of the 326 E2-P2 geometry verdicts (union relation EQUAL / U ⊆ U′ / U′ ⊆ U) was recomputed in E2-P3 with the
exact containment engine over the full box [0,q1]×[0,q2] and with independent certificate checking: **0 verdicts changed**.
The E2-P2 numerical results stand; the E2-P2 argument for the rows with q1 < q2 is superseded by the E2-P3 certificates.
