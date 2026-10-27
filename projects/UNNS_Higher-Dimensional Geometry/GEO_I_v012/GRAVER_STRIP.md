# GRAVER_STRIP — uniform strip-boundary Graver theorem (G12-T2)

Every step between consecutive boundary Gamma-points of `H_Q` is a Graver vector of `Gamma_{d,s}` (except the impossible pair `(B,A)`).
Mechanism: if `h` were conformal to the step `e`, the points `w+h` and `w2-h` lie in the box, are mirror images through the edge midpoint, and so cannot both be on the inner closed side of the supporting line unless they lie on it — then a Gamma-point sits strictly inside the edge, contradicting consecutiveness (MATHEMATICS.md §2).
Also: `(d,0)`, `(0,d)`, `(1,s-d)`, `(d-t,-1)` are Graver (direct).
Support: `K.graver_scan` exact scan of every step in every box `d<=16` (structure check S6), included in CAPCOVER2 certificates (the checker re-scans each generator).
Status: PROVED+CHECKED.
