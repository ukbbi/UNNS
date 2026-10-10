# Metrics

Primary preservation metrics:

- `basin_recall`
- `min_target_survivors_per_basin`
- `min_basin_geometric_coverage`
- `max_basin_centroid_drift`
- `unclustered_target_fraction`
- `signature_stratum_recall`

Compression/computation metrics:

- `R_candidate = 1 - N_survivor/N0`
- `R_eval = 1 - Q_scr/Q_base`
- gate primitive evaluations
- median baseline wall time
- median SCR wall time including filter cost
- `G_time = T_base/T_scr`
- operation-count gain

Diagnostic only:

- candidate-level target recall (not a preservation requirement in v003)
