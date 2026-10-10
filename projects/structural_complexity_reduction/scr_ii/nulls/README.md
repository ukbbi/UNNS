# Nulls and controls

Required controls:
1. `N0_BASELINE` — no structural pruning.
2. `N1_RANDOM_PREFIX` — deterministic hash-based prefix pruning calibrated to the same leaf-survival fraction.
3. `N2_SYMBOL_SHUFFLE` — per-instance symbol relabeling with the same gate engine.
4. `N3_TRANSITION_PERMUTE` — degree-preserving permutation of Γ_route transitions.
5. `C1_SOLVER_NATIVE` — exact solver with arithmetic forward bounds only; reported separately as a conventional preprocessing baseline.

Nulls use the same primary instances and cannot alter the exact solution predicate.
