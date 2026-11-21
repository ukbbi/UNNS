# MUG-I theorem register (cumulative)

v001 items M1–M10 are unchanged (see ../MUG-I_v001/REGISTER.md), with these scope notes: M8/M9 concern whole-lattice and rational similarities (NOTES.md C1, C2); the helicity remark in v001 means the label (C3).

| ID | Statement | Level | Evidence | Status |
|----|-----------|-------|----------|--------|
| N1 | Rational similarity M: admissible set {m : Mm integral} is a finite-index sublattice; whole lattice iff M integral | label | proof; W1 | proved + verified |
| N2 | 3-torus ray carry by sqrt(rho) exists iff sf(rho|u|^2) not 7 mod 8; target class = [sqrt sf(rho sigma)] | field (restricted) | Legendre + Davenport–Cassels; W2 (3640 cases) | proved; rational-target step cites Davenport–Cassels |
| N3 | Explicit sqrt3 carry e1 -> (1,1,1) is an exact periodic Maxwell solution; R unique up to rotation about target axis | field | W3 symbolic | verified (instance) |
| N4 | Rank-2 support {e1,e2}: carry by sqrt(rho) iff rho sum of two squares; rank 3 iff alpha rational | field | Witt cancellation proof; W4 (rho<=40) | proved + verified |
| N5 | General rank-2 support: carry iff alpha^2 Q embeds in I3 (Hilbert-symbol test) | field | W5, 249 random cases agree with exhaustive search | test implemented, sample-verified; not exhaustive |
| N6 | Conducting box: no irrational rotation-dilation carry maps a box eigenmode to a box eigenmode (maps fixing the box and origin) | field | polytope-edge argument; W6, W6b | proved (necessity), instance-verified |
| N7 | Helicity: label preserved; integrated helicity divided by alpha | field | W7 symbolic, both handedness | verified |

Controls: ordinary Maxwell dilation and rotation symmetry account for each individual map; the induced content is the selection by support shape (N4, N5) and by boundary (N6). No coupling or energy transfer is claimed.
