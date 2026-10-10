# SCR-I Dashboard v003

Canonical local control and analysis surface for the completed SCR-I-A v003 benchmark.

- reads `SCR_I_PREREG_v003/`;
- verifies pinned source lock and design-preservation audit;
- reads the frozen `PRIMARY_RESULT_v003.json`;
- disables primary rerun once `RUN_PROGRESS_v003.json` reports `COMPLETE` 15/15;
- exposes raw outputs and provenance read-only.
