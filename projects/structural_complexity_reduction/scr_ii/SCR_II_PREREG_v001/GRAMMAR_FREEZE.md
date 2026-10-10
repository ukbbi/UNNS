# Grammar Freeze — Γ_route v001

## Allowed symbol transitions

| From | Allowed next |
|---|---|
| A | A, B |
| B | B, C |
| C | A, D |
| D | C, D |

## Boundary rule

For phases `q ∈ {0,1,2}`:

\[
(q_{next}-q_{current}) mod 3 \in \{0,1\}.
\]

## Persistence rule

In any rolling four-edge window, at most one generator-marked boundary-discontinuity candidate is permitted.

## Structural reachability

G3 performs suffix feasibility only inside Γ_route. It may use:

- current route symbol;
- current boundary phase;
- remaining depth;
- persistence-window state.

It may not use:

- checksum target or accumulated checksum;
- cost interval or accumulated cost;
- terminal solution seal;
- exact-solution labels.

## Frozen gate order

`G1 Generability -> G2 Boundary continuity -> G3 Structural reachability -> G4 Persistence`

No weighted composite score is permitted in v001.
