# Arithmetic controls and interpretation

This release deliberately uses two simple alternatives. They are **not** a claim of causal or physical discrimination.

1. Lucas recurrence: `L_1=1`, `L_2=3`, `L_(n+2)=L_(n+1)+L_n`, evaluated over indices 1..48.
2. Shifted sequence `A_n=F_n+1`, over the same 48 indices. Unlike Fibonacci, this is not assumed to satisfy the same homogeneous recurrence.

All are fed into the **same** exact `T_N` arithmetic and the same `1..3` path search. Routes may pass through integers absent from the external sequences. Recorded per-control paths are in `results/controls_48.json`.

| Data | 1 step | 2 steps | 3 steps |
|---|---:|---:|---:|
| Fibonacci | 1 | 4 | 3 |
| Lucas | 2 | 1 | 0 |
| Fibonacci+1 | 3 | 0 | 0 |

**Scope:** Small deterministic comparison. No p-values are reported. The finite control shows the overlay is sensitive to the external integer values and their order; it does not show substrate-specific emergence beyond ordinary number theory.

For v002, predeclare a more meaningful comparison family with size, prime-factor and divisibility profiles matched to Fibonacci as closely as feasible, while avoiding post-hoc selection.
