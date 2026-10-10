# PREFLIGHT_v006 — Energy-Window Feasibility and Non-Tautology Gate (SCR-III-B)

Additive package; extract into the project root (it adds `scr_iii_b/feasibility/` and `scr_iii_b/output/validation/v006/`).
Requires the frozen **v005** files already in place (`scr_iii_b/reference_check/`, `scr_iii_b/output/validation/v005/`). They are only read; v006 verifies them against the local `MANIFEST_v005.json` (test F1) and imports `physical_energy_v005.py` read-only (no bytecode written). No g++, numpy or network needed.

```bash
python3 scr_iii_b/feasibility/validate_v006.py    # ~1 min; exit 0 PASS/LIMITED, 1 FAIL, 2 BLOCKED
python3 scr_iii_b/feasibility/test_v006.py        # unit tests
```

## What it does
1. Exhaustively enumerates the 1×1 (16) and 2×2 (4,096) spaces with the frozen v005 Hamiltonian (joules, E−E0, ice membership, violated vertices, vertex types) and checks them against the v005 record (C1–C3).
2. Groups numerically degenerate levels (relative tolerance 1e-9; unrounded energies kept), evaluates every target-set transition, and classifies windows: ground-only, ice-excited preserved, first non-ice threshold (expected failure), defect-accessible (W1–W4).
3. Compares the real incidence grammar with structural nulls: degree-preserving swaps and free random 4-sets, plus unchanged and perturbed controls; Hamiltonian and targets are hash-checked unchanged (N1–N4).
4. Reports cost and constructive-generation measurements separately from contraction (K1, X1), and answers the six non-tautology questions (T1).

## Reading the verdict
`FEASIBILITY_PASS` means only that a verified non-ground preservation window exists whose target set is not identical to the grammar set, and all controls ran. It is **not** physical-transfer confirmation, rests on the spectral gap of the frozen Hamiltonian (guaranteed alignment), and freezes nothing. Windows found here are exploratory; primary windows must be frozen separately, before any primary comparison.

## Out of scope
Downstream solver costs (C_downstream), the E2 charged local estimator (requirements only), 3×3 energy windows, the 24×24 arrays, v1.01 parameters, size disorder, the unmodified simulator.
