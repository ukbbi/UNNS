# GAP4_v010 — minimal 64-bit exact-search prototype

This is an **additive, guarded solver prototype** for SCR-III-GAP-4X4. It uses the unchanged frozen `physical_energy_v005.py` as a byte-identical source-derived implementation. No real 4×4 energy was computed in packaging.

## Ubuntu/WSL

Extract `GAP4_v010.zip` under `structural_complexity_reduction/scr_iii_b/` as `GAP4_v010/`.

```bash
cd scr_iii_b/GAP4_v010
bash RUN_TEST.sh
```

The tests compile the C++17 solver and check public 1×1 and 2×2 instances only. The 4×4 instance generator is blocked unless an explicit `--authorize-real` flag is supplied; **do not supply that flag now**. This interface is a safety guard, not an authorization system.

## Solver method and limitations

- 64-bit vertex masks and state IDs, with explicit limit `n<=63`, per-vertex orientation masks for 'in' arrows.
- C++ depth-first exact Ising energy minimization: all assigned-pair contributions exact to floating-point arithmetic, a **conservative analytical bound** on unassigned couplings, and separate searches for global E0 and lowest non-grammar state.
- Per-objective CPU time cap (`1..1800` seconds). On interruption, emits incumbent (if any) and a *root relaxation bound*. Both are weak but mathematically directed energy bounds, subject to floating-point error.
- The code uses double-precision arithmetic and a heuristic outward guard. **It does not implement rigorous directed-rounding interval arithmetic.** A completed search or tight interval needs a further rigorous numerical/witness check before calling the 4×4 finding *CERTIFIED* under the frozen protocol.
- The partial objective output gives normalized energies H/A, not joules; multiply by the same frozen v005 A(792 K) before constructing delta4. Do not confuse lower bounds with reached optima.
- Generic branch-and-bound can be very slow at n=40. This package does not promise 4×4 feasibility or a scientific PASS.
- The solver reads pair couplings from text; physical geometry is generated using v005 source-derived code. The n=40 real matrix must not be generated yet.

## Files

`PREDICTION_FREEZE_v001.md` — locked predictions and no-run boundary; `physical_energy_v005.py` — unchanged source-derived physics; `make_instance_v010.py` — instance builder and 4×4 safety gate; `solver_v010.cpp` — guarded 64-bit search; `test_v010.py`, `RUN_TEST.sh` — public-only smoke and geometry tests; `MANIFEST_v010.json` — file hashes.

## Honest development status

`V010_PROTOTYPE_BUILT / SMALL_PUBLIC_TESTS_PASS / 4X4_NOT_RUN / FULL_CERTIFICATION_NOT_ESTABLISHED`.
