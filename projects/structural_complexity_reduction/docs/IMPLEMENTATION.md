# Canonical v003 Implementation

Active implementation:

```text
adapters/scr_i_a_v003_adapter.py
src/scr_i_v003/
scripts/setup_scr_i_v003.py
scripts/run_v003_regression.py
scripts/run_scr_i_a_v003.py
```

`src/scr_i_v003/runner.py` uses `safe_io.safe_dump` for Windows-safe checkpoint/output persistence. Basin geometry is cached once per seed/pool cell and reused for matched-null replicates. These are implementation-only optimizations validated by `tests/test_v003_opt.py` and `tests/test_v003_safe_io.py`.

The completed primary result is frozen; the canonical runner refuses a rerun when `RUN_PROGRESS_v003.json` reports `COMPLETE` 15/15.
