# MIXED_CAP — mixed-corner classification and the complete cover (G12-T3..T7)

Boundary Omega of `H_Q` from `B=(d,0)` to `A=(0,d)` lies in `R* C* T*` (R: `x>=d,y<d`; C: `x>=d,y>=d`; T: `x<d,y>=d`; no N points; no R→T step). Edges are L-eligible (both `x>=d`) or D-eligible (both `y>=d`), many both.
Cells: L-cells (shift `(-d,0)`), D-cells (shift `(0,-d)`), a bottom cell (first edge, `u>=1`) and its transpose (last edge, `v>=1`). Together with `H_0 = H_Q ∩ [0,d]^2` they cover `H_Q` up to a null set; closedness of `U_Q` then gives equality.
The "corner pentagon" of v011 does not occur as a separate region: the corner `(d,d)` is either an Omega vertex or lies on the `C→T` bridging edge, which carries a D-cell. The residual set `K_Q = H_Q \ (H_R ∪ H_T)` needs no separate proof: the single family covers `H_Q \ H_0` for one-sided boxes (`u=0` or `v=0`; horizontal T3, vertical T4 by transposition) and mixed boxes (T5–T7) alike. Degenerate boxes (flat top, collinear Omega points, `v=0`) are handled by the same proof (collinear points are Omega vertices; flat edges give null cells).
Full proof: MATHEMATICS.md §3–§5. Support: exact cover for all `d<=12` boxes (certificates), exact cover of all boxes `d<=22`, adversarial boxes to `d=399` (a standalone `d=13..30` sweep was interrupted: PARTIAL, unused).
Status: PROVED+CHECKED.
