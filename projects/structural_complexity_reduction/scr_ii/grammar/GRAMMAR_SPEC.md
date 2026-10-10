# Frozen Structural Grammar — Γ_route v001

The grammar is frozen before any primary instance is generated.

## Route-symbol transitions

Allowed directed transitions:

- `A -> A, B`
- `B -> B, C`
- `C -> A, D`
- `D -> C, D`

All other symbol transitions are structurally non-generable.

## Boundary-phase continuity

For consecutive phases `q_i, q_{i+1} in {0,1,2}`, allowed motion is:

\[
q_{i+1}-q_i \pmod 3 \in \{0,1\}.
\]

A direct backward jump by `2 mod 3` is inadmissible.

## Persistence rule

Within any rolling window of four accepted edges, at most one edge may be marked as a boundary discontinuity candidate by the generator metadata.

## Common-refinement reachability

A prefix survives only if the frozen structural automaton admits at least one suffix of the remaining depth that can terminate in an accepting structural state.

This reachability test is computed from Γ_route alone. Arithmetic checksum/cost/terminal-seal solution constraints are prohibited from the reachability calculation.

## Gates

- **G1 Generability:** route-symbol transition belongs to Γ_route.
- **G2 Boundary continuity:** phase progression satisfies the frozen phase rule.
- **G3 Structural reachability:** at least one Γ_route-compatible suffix can reach an accepting structural state.
- **G4 Persistence:** rolling discontinuity budget is satisfied.

Gate order is frozen as `G1 -> G2 -> G3 -> G4`.
