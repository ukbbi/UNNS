# Output — Canonical v003

Raw completed SCR-I-A v003 records remain at the output root.

```text
PRIMARY_RESULT_v003.json
gate_audit_v003.csv
null_results_v003.csv
timing_trials_v003.csv
PRE_FLIGHT_v003.json
RUN_ENVIRONMENT_v003.json
RUN_PROGRESS_v003.json
SUMMARY_v003.md
```

Additional layers:

- `v003_phase1/` — frozen design-preservation audit;
- `checkpoints/` — completed resumable-run checkpoint;
- `reports/v003/` — human-readable consolidated record;
- `exports/v003/` — canonical machine-readable final record.

Do not overwrite the completed primary result.
