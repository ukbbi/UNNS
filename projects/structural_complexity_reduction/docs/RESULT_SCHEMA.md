# SCR-I v003 Result Schema

Canonical primary records are the dictionaries in `output/PRIMARY_RESULT_v003.json`. Core fields:

```text
engine
preregistration
optimization
benchmark
pool_size
seed
n0
n1
target_count_base
candidate_target_recall
r_candidate
r_eval
g_time
g_ops
t_base_median
t_scr_median
t_filter_median
t_downstream_scr_median
basin_count
basin_recall
min_target_survivors_per_basin
min_basin_geometric_coverage
max_basin_centroid_drift
unclustered_target_fraction
signature_strata_count
signature_stratum_recall
verdict
```

Matched nulls are stored in `output/null_results_v003.csv`; timing trials in `output/timing_trials_v003.csv`; gate short-circuit audit in `output/gate_audit_v003.csv`.

The consolidated machine-readable scientific record is `output/exports/v003/SCR_I_V003_FINAL.json`.
