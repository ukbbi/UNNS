# Nulls and controls

All nulls operate on the same frozen primary instances.

## N1 — Random prefix pruning

A deterministic prefix hash keyed by a null replicate seed prunes prefixes with a calibrated probability chosen from calibration data to match the SCR leaf-survival fraction by depth.

N1 cannot inspect exact solution labels.

Primary reporting:
- solution preservation rate;
- node reduction;
- time gain.

## N2 — Symbol shuffle

Within each instance, route-symbol labels are permuted by a frozen null seed while arithmetic fields are unchanged. G1→G4 then run normally.

Purpose: test whether SCR depends on actual structural symbol organization rather than generic pruning budget.

## N3 — Transition permutation

Use a degree-preserving permutation of Γ_route's transition destinations, frozen before primary execution.

Purpose: preserve coarse graph degree while destroying the specific route grammar.

## C1 — Solver-native conventional preprocessing

Exact arithmetic forward bounds, no structural grammar.

Purpose: compare SCR with a conventional problem-specific preprocessing strategy.

## Replicates

- N1: 50 replicates per primary instance.
- N2: 12 fixed permutations per primary instance.
- N3: 12 fixed transition permutations per primary instance.

Null outcomes do not affect primary H1–H4 verdicts.
