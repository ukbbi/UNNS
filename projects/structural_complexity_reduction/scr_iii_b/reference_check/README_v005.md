# PREFLIGHT_v005 — SCR-III-B physical energy and Hamiltonian convention lock

Additive package. Nothing in SCR-III-A, v001–v004, `references/` or GitHub is modified. No SPEC/preregistration is frozen; no transfer experiment is run.

## Run (Ubuntu / WSL, from the project root)

```bash
python3 scr_iii_b/reference_check/validate_v005.py      # ~10 s; needs g++ and Python 3 (no numpy, no GSL)
python3 scr_iii_b/reference_check/test_v005.py          # unit tests of the evaluator
```

Inputs read (never written): `scr_iii_b/references/public_code/{SPMMC_Code,MMC_Code}.zip`, `scr_iii_b/references/square_ice_model/Dryad_README.md`, and (optional regression A11) `scr_iii_b/models/physical_energy.py`.
Outputs: `scr_iii_b/output/validation/v005/` (REPORT, SOURCE_AUDIT, PARAMETERS, GROUND_STATES, TEMPERATURE, TESTS, MANIFEST).
Exit code: 0 PASS/PARTIAL, 1 FAIL, 2 BLOCKED.

## Files
- `physical_energy_v005.py` — independent evaluator (joules and normalized energy, pair contributions, ΔE, deterministic encoding bit i = 1 ⇔ s_i = +1).
- `source_probe_v005.cpp` — original SPMMC v1.00 functions copied verbatim (each block carries original line range and SHA-256; test P2 re-checks byte identity) plus a small driver. Not the unmodified simulator.
- `validate_v005.py` — orchestrator; `test_v005.py` — unit tests.

## Evidence levels (always reported separately)
UNMODIFIED_SIMULATOR_EXECUTION (not performed) · VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE · SOURCE_DERIVED_INDEPENDENT_PYTHON · PREVIOUSLY_TRANSCRIBED_V002_V004_FORMULAS · STATIC_SOURCE_TEXT_ANALYSIS.

## Tolerance policy
Normalized quantities 1e-11; Python-only joule quantities 1e-12 relative; comparisons against the source's rounded constant 0.910179 use 2e-6 and the known systematic ratio is tested directly. The v004 normalized 1e-12 absolute tolerance is not applied to joules.

## Scope
Selected model: SPMMC v1.00 all-pair dumbbell model, template parameters, free-boundary 1×1 and 2×2 patches, 0 < T < Tc. The source has no total-energy routine; H = A(T) Σ K s s is reconstructed and verified against the verbatim flip update. The verdict is about this model only; it is not a transfer result and says nothing about the published 24×24 arrays. Unresolved items are listed in `REPORT_v005.md`.
