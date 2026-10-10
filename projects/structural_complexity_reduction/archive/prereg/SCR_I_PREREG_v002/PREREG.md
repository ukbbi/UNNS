# SCR-I-A v002 preregistration

## Question

Can the frozen UNNS structural gate chain G1→G2→G3→G4 reduce the number of downstream viability evaluations while preserving **every** candidate that an independent, source-defined viability oracle accepts?

The comparison is:

`baseline: all candidates → viability oracle`

versus

`SCR: all candidates → G1→G2→G3→G4 → viability oracle on survivors`.

The downstream oracle is not allowed to use the SCR gate verdict as its target label.

## Frozen population

For each primary seed, generate one 40,000-candidate adversarial P4 pool using the pinned Chamber LIII generator. The 2,500 and 10,000 cells are prefixes of that same pool. Frozen primary seeds are `2026100801` through `2026100805`.

## Primary success conditions

A cell can support SCR calibration only if target recall is exactly 1.0, downstream evaluations are reduced, identity re-evaluation matches exactly, and at least one preregistered net-cost measure exceeds unity. Any lost baseline target is `TARGET_LOSS` regardless of the contraction fraction.

No primary outcome permits changing the target oracle, gates, thresholds, candidate generator, seed list, or pool sizes.
