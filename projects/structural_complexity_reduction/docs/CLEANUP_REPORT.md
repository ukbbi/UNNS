# Cleanup and Alignment Report — 2026-10-07

## Outcome

The project was reduced from **280 files / 1,667,488 bytes** to **141 files / 913,982 bytes** before this report and regenerated checksum inventory were added. The active tree now contains only the canonical v003 implementation, completed v003 outputs, current scientific documentation, required pinned references, tests, and a compact read-only archive of the v001/v002 preregistration history.

## Removed from the active tree

- all `__pycache__` and `.pyc` files;
- stale checkpoint `.tmp` residue;
- duplicate `output.zip`;
- initial synthetic smoke-test/example scaffolding;
- superseded v001 and v002 execution engines and adapters;
- obsolete v001/v002 setup/run batch files;
- package-install notes, patch notes, old package manifests and package SHA lists;
- unused v001 root configs and fixture files;
- unused copied source-lock files that are not part of the v003 lock;
- obsolete v001/v002 phase-setup artifacts except the decisive transition records.

## Preserved intentionally

- `SCR_I_PREREG_v003/` — active frozen preregistration;
- `archive/prereg/SCR_I_PREREG_v001/` — content unchanged, validation PASS;
- `archive/prereg/SCR_I_PREREG_v002/` — content unchanged, validation PASS;
- decisive v001/v002 transition audit JSONs under `archive/history/`;
- all completed v003 raw primary, null, timing, gate-audit, environment, progress and checkpoint records;
- consolidated v003 reports and final JSON;
- v003 pinned source-lock files;
- UPI reference and diagnostic code, still secondary/non-pruning.

## Canonical active path

```text
SCR_I_PREREG_v003/
adapters/scr_i_a_v003_adapter.py
src/scr_i_v003/
scripts/setup_scr_i_v003.py
scripts/run_v003_regression.py
scripts/run_scr_i_a_v003.py
dashboard/
output/
```

## Alignment fixes applied

- root README, context, structure, changelog and scientific docs updated to the completed v003 state;
- dashboard now uses basin-level v003 semantics rather than stale candidate-recall/v001 text;
- dashboard recognizes the primary run as **COMPLETE/FROZEN** and disables rerun;
- canonical runner uses Windows-safe persistence directly and exits cleanly;
- canonical runner refuses rerun after the 15/15 primary result is complete;
- result/final JSON SHA-256 freeze markers added;
- v001/v002 historical dashboard pointer updated to the archive path;
- current source-lock README corrected to v003 sources;
- one canonical `RUN_VALIDATE_V003.bat` now checks project alignment.

## Validation

Critical checks: **PASS**

- v003 source lock;
- v003 preregistration;
- archived v001 preregistration;
- archived v002 preregistration;
- design-preservation audit marker;
- primary progress `COMPLETE` 15/15;
- exact frozen primary seed × size grid;
- primary-result SHA-256 freeze marker;
- consolidated final record and SHA-256 marker;
- 9/9 active unit/regression tests;
- dashboard JavaScript syntax;
- no generated cache/tmp clutter in the distributed tree.

## Documented non-blocking compatibility notes

1. **Frozen schema field name:** `SCR_I_PREREG_v003/schema/result_schema.json` requires `basin_count_base`; the completed runner writes the semantically identical value as `basin_count`. The frozen preregistration is not edited post hoc. Mapping is documented in `docs/SCHEMA_COMPATIBILITY.md`.
2. **Negative-space depth:** v003 preserves aggregate gate rejection counts, not every rejected candidate record. This does not enter the frozen primary verdict; the limitation is documented in `docs/NEGATIVE_SPACE_STATUS.md`.

These two items are transparent documentation/interface limitations, not contradictions in the completed v003 primary result.
