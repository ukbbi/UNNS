# CONTEXT — GEO-I v010 (handoff)

Frozen definitions: `Γ = {(i,j): j ≡ s i mod d}`, `F`, `T1`, `T2`, cells `P(u;g,h)` (Graver generators, corners in `F`), `U0`; binary box `C = ker M`, circuits, cells `(S,x)`, collision, shortening, minimal box, witness rank. Not modified in v010.

State: hollow-box complement proved (G10-Z, `d ≥ 5`); cap (G10-T2) open; binary criterion/reduction proved; nullity six classified; W2 (⇒ universal rank three) open.

Next questions: (1) cap — a cell cover of `H_Q ∖ H_0` using the Graver hull steps of the enlarged hull, treating the two new chains jointly; (2) W2 — merge a partition of `1` into more than two circuits using rigidity; (3) nullity 7 exhaustive classification (≈ 10^5–10^6 affine orbits; needs a faster orbit generator); (4) prove G10-K for all `t`.

Lessons: shipped verify reports must be regenerated per release (v009's was stale); Z²-primitive subdivision is not the right chain subdivision for F (use the F points on each hull edge); a failed deletion loop on dead coordinates requires `len(D) < len(cur)`.
