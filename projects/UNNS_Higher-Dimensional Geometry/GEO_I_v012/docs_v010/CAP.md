# GEO-I v010 — Programme B: the cap (G10-L3, G10-L4, G10-T2, G10-T3) — OPEN

**Status: G10-T2 OPEN; G10-T3 OPEN (valid only if T1 and T2 are both proved; T1 is now proved, T2 is not).**

Setting: small boxes `Q = (d+u, d+v)`, `0 ≤ u,v < d`, `(u,v) ≠ (0,0)`; `H_Q = conv F_Q`, `C_Q = H_Q ∖ H_0`.
* Now unconditional (G10-R1): `H0 ⊆ U_Q`. What remains is `C_Q ⊆ U_Q`.
* The squareless boxes (v008, `v < m_s(u)`) were handled by the staircase (G8-S).
* **Attempt in v010** (bounded). The lower-left chain of `H_Q` coincides with that of `H0`; the new top and right chains consist of Graver steps (same reflection argument as Lemma 2). But `C_Q` lies between two chains with a corner interaction, and the cell that covers a point depends on `(u,v)` and on whether `Q` is squareless; no uniform tiling analogous to the zonogon was found. G10-L3 (cell extension) and G10-L4 (corner compatibility) are therefore **not** claimed.
* **Evidence (v009, inherited):** survey `d = 3..22`, all boxes, all units: every cap point covered (no counterexample). Not a proof.
* **Reduction:** G10-T2 ⇒ G10-T3 (`U = H` for all `d`, units `s`, `Q ≥ (d,d)`, `Q ≠ (d,d)`), using G10-R1, G7-T1 (`max Q ≥ 2d`) and the trivial `s = ±1` cases.
