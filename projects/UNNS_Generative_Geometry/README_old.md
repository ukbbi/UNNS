# GEO-HD-1 — Higher-Dimensional Generative Geometry of the UNNS Substrate

**Local research work area — 30 October 2026.** Not a frozen GEO-I release, not Paper C, and not an authorized change to any GitHub repository.

## Installation / merge

This ZIP has **no wrapper directory**. Extract its contents **into** your existing local folder:

`D:\UNNS_SUBSTRATE(desktop)\TRANSFER\Bulk_2\REGIME_SYNTHESIS\UNNS_ENTANGLE_I\GEO_HD_NEXT_MILESTONE\`

Do not extract into a new subdirectory named `GEO_HD_NEXT_MILESTONE` under the existing one. The package preserves the existing `Scripts/` filenames, `GEO_HD_1.pdf`, and context markdown in its layout. If Windows asks whether to replace a pre-existing file, compare it or keep the newer local copy; this package does not require overwriting locally modified scripts. **It does not write to GitHub or any frozen release.**

## Start here

1. Read `STATUS.md` and `DEFINITIONS.md`. They supersede the claims in the preserved `GEO_HD_1.pdf` where corrected.
2. Run `RUN_WINDOWS.bat` from the project folder (Python 3; built-in libraries only for the new project code).
3. Optional original user checks: `python Scripts\geo_hd_1_check_factorization.py` (requires `sympy`).
4. Run `python Scripts\EXPLORE_PARITY_CELLS.py` for **exploratory** candidate parallelotope counts (not proofs of coverage/topology); `--save` refreshes `results/provisional_parity_cells.json`.
5. Review `EXPERIMENT_PLAN.md`, then conduct the independent Paper-A-compatible Graver-cell analysis for the 13-point 3D parity fibre before investigating 40-point 4D.

## Scientific scope

- **Proved / derivable:** occurrence-fibre bijection (Volume I); SELECT-II square-root transport formula, index-gain and label-recovery corollaries; coordinate-cell origin-deletion obstruction under the explicitly stated grammar; parity-lattice Graver basis.
- **Computationally checked:** exact 6/72/900 and parity 3D/4D benchmarks; originally supplied scripts report 43,376 SELECT-II edges for m<=5000.
- **Inherited, scoped:** FIELD-I `C(x)` monotonicity (Volume II Thm 1.3) and eventual regime-I three-step scaling (Thm 2.4). These are **not** SELECT-II laws.
- **Open:** 3D/4D **nontrivial** Graver-cell coverage, embedding and higher homology; cross-fibre cellular maps; arithmetic-specific history invariants.

## Directory guide

- `src/`: executable exact arithmetic and finite combinatorial baseline, with a **provisional** general cell grammar (`cells.py`).
- `tests/`: deterministic standard-library `unittest` suite; `RUN_WINDOWS.bat` / `RUN_CHECKS.py` runs it.
- `Scripts/`: the two original, **unaltered** audit scripts, both requiring `sympy`.
- `data/`: exact generated benchmarks, no invented points or labels.
- `ERRATA/`: NEW *proposed* Paper A remark correction; does not alter frozen Paper A.
- `references/registry_errata_READ_ONLY/`: user's existing FIELD-I F.T71 erratum, retained separately because it is unrelated to Paper A.
- `figures/`, `results/`: output destinations, not evidence by themselves.

## Reference / authority policy

The source of truth for Paper A/B and SELECT/FIELD remains the frozen original source. `GEO_HD_1.pdf` is retained as the initial **superseded working specification**, not as a corrected document. The scope corrections are in `STATUS.md` / `THEOREM_REGISTRY.md`. The provisional higher-dimensional cell grammar must be checked against Paper A's exact 2D conventions before treating results as a generalization. Do not assert originality without a literature comparison.
