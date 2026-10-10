# Downstream solver freeze

## Baseline arm

Depth-first exact enumeration of the complete binary decision tree.

At each leaf, evaluate the frozen independent solution predicate.

The baseline solver may maintain accumulated arithmetic state required to evaluate checksum/cost efficiently, but it may not use Γ_route.

## SCR arm

Use the identical DFS and identical leaf solution checker.

Before expanding a child prefix, evaluate G1→G4. If the prefix fails, prune that subtree.

## Solver-native conventional control

`C1_SOLVER_NATIVE` may use exact arithmetic forward bounds derived from remaining minimum/maximum cost and modular checksum reachability. It is reported separately and is not substituted for the baseline arm.

## Equality requirement

The baseline and SCR arms must return solution sets in canonical lexicographic bit-string form. Preservation is exact set equality, not equal counts.
