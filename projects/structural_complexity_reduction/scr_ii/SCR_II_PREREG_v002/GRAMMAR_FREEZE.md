# Grammar Freeze — Γ_route v001 retained for SCR-II v002

v002 changes the downstream arithmetic benchmark construction, **not** the structural grammar.

Allowed symbol transitions:

| From | Allowed next |
|---|---|
| A | A, B |
| B | B, C |
| C | A, D |
| D | C, D |

Boundary continuity:

\[
(q_{next}-q_{current}) \bmod 3 \in \{0,1\}.
\]

Persistence:

Within any rolling four-edge window, at most one generator-marked discontinuity candidate is permitted.

Gate order remains:

`G1 Generability -> G2 Boundary continuity -> G3 Structural reachability -> G4 Persistence`

The filter may not access:

- cost;
- cost interval;
- checksum weights or target;
- terminal seal;
- exact-solution labels;
- exact baseline solution density.
