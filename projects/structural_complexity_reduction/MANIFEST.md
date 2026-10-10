# Canonical Manifest — SCR-I v003

**Project:** Structural Complexity Reduction  
**Canonical benchmark:** `SCR-I-A v003`  
**Active preregistration:** `SCR_I_PREREG_v003`  
**Primary status:** `COMPLETE` — 15/15 cells  
**Outcome:** `STRUCTURAL_COMPRESSION_CONFIRMED_ABOVE_REPRESENTATION_FLOOR`  
**Cleanup/alignment date:** 2026-10-07

## Scientific result snapshot

- median candidate reduction: 92.03%
- minimum basin recall: 1.000
- median time gain: 8.39×
- median operation gain: 6.73×
- median viable-target fraction among survivors: 99.15%
- median target-recall enrichment vs rate-matched null: 1.889×

## Canonical execution surface

```text
RUN_DASHBOARD.bat
RUN_VALIDATE_V003.bat
RUN_SETUP_V003.bat
RUN_SCR_I_A_v003.bat
SCR_I_PREREG_v003/
adapters/scr_i_a_v003_adapter.py
src/scr_i_v003/
scripts/
```

The completed primary is frozen; the canonical runner and dashboard refuse a rerun.

## Canonical results

```text
output/PRIMARY_RESULT_v003.json
output/gate_audit_v003.csv
output/null_results_v003.csv
output/timing_trials_v003.csv
output/RUN_ENVIRONMENT_v003.json
output/RUN_PROGRESS_v003.json
output/checkpoints/SCR_I_A_v003_checkpoint.completed.json
output/reports/v003/SCR_I_V003_RESULT_RECORD.md
output/reports/v003/SCR_I_V003_ANALYSIS.md
output/reports/v003/SCR_I_V003_NULL_ANALYSIS.md
output/exports/v003/SCR_I_V003_FINAL.json
```

SHA-256 sidecars freeze the raw primary result and consolidated final JSON.

## Historical preservation

Frozen but inactive v001/v002 preregistrations are retained under `archive/prereg/`. Decisive transition evidence is retained under `archive/history/`. Superseded engines/installers are removed.

## Validation state

`RUN_VALIDATE_V003.bat` verifies:

- v003 pinned source lock;
- active v003 preregistration;
- archived v001/v002 preregistration integrity;
- design-preservation audit;
- exact 15-cell completed primary grid;
- result freeze hashes;
- consolidated final record;
- active unit/regression tests.

Latest validation: **PASS WITH DOCUMENTED COMPATIBILITY NOTES**.

Documented notes:

- frozen schema `basin_count_base` ↔ completed output `basin_count`;
- negative-space audit is aggregate rather than candidate-level.

See `docs/ALIGNMENT.md`, `docs/SCHEMA_COMPATIBILITY.md`, and `docs/NEGATIVE_SPACE_STATUS.md`.

## Inventory

Files before root checksum inventory: **139**  
Bytes before root checksum inventory: **913132**

`SHA256SUMS.txt` provides the complete cleaned-tree checksum inventory (excluding itself).
