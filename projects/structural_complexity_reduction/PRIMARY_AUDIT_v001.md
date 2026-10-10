# PRIMARY_AUDIT_v001 — Follow-up checks after external audit (2026-10-10)

No primary verdict, frozen document or protocol rule was changed. Scope: implementation checks recommended by the audit.

## 1. Driver revision comparison
- The original driver file was not saved before editing. It was reconstructed by mechanically reversing the three edits; the reconstruction hashes to exactly **973e4e83e91342d63bfd29231f0a0d09371b9edcbe4d5d7687d41d0abf58aa48**, the hash recorded in the authorization. Stored as `output/primary/aborted_run_1/primary_run_v001.original_973e4e83.py` (the reversal was checked only by this hash match).
- Unified diff: `output/primary/aborted_run_1/driver_revision.diff` (sha256 7f412306…c82097). Lines removed from the original are only: the audit-log overwrite guard/truncation, the null-generation call, and the null-row mapping. All were replaced by checkpoint/resume equivalents. Phase A code (windows, audit, G/P/C logic, timing, H-C rule) is unchanged apart from indentation inside a cache wrapper. No constant, tolerance, window, seed or decision rule differs.
- Revised driver: 2df16134…0c18b.
- Note: after the abort, the phase-A and window results were recomputed from scratch under the revised driver; the aborted run's values were not used. Both runs gave the same window results (26 / 2 / 434 targets), seen in the logs.

## 2. Direct check of excluded states against the frozen v005 module
Script used `reference_check/physical_energy_v005.py` (frozen v005 code) with: energies from the explicit charge-position (dumbbell Coulomb) model in joules at 792 K, and 2-in/2-out from vertex geometry (`ice_ok_geometric`), independent of the incidence masks and K-matrix used by the solvers and the numpy audit.
- All 26 primary target ids lie within W + tau of the frozen E0 (minimum energy equals E0 to 1e-15 relative).
- Geometric ice-rule: 10 of the 26 satisfy it, 16 do not; the 16 are exactly the reported false-exclusion ids.
- Each of the 16 lies 0.94290 k_BT above E0; minimum 0.9428984210312306 vs reported Δ_nonG/kT 0.9428984210312401 (difference ~1e-14).
- 0.5 kT: 2 targets, both in grammar; 2 kT: 434 targets, 146 in grammar (geometric), matching the report. 3,000 random geometrically-excluded states: none below Δ_nonG.
- Limits: this checks the excluded states and window membership of the reported targets. Completeness of the target sets (no missing states) rests on the C++ scans and the numpy audit, which agree. Both share the v005 physical model and geometry, so a common-model error is not excluded; verifier remains cross-validated, not independently authored.

## 3. Wording
See Erratum E1 in `PRIMARY_RESULT_v001.md`. The workbook's "Solvers agree" column header was renamed to "Solvers match their expected set" and its kT conversion is noted as a display value.
