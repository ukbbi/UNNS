# SCR-I v003 Metrics

## Candidate contraction

`R_candidate = 1 - N1/N0`

## Downstream evaluation reduction

In SCR-I-A v003 the downstream oracle is evaluated only on survivors, so `R_eval` equals the candidate reduction under the frozen cost model.

## Net gains

`G_time = T_base / (T_filter + T_downstream,SCR)`

`G_ops = C_base / (C_gate + C_downstream,SCR)`

## Basin/class preservation

Primary metrics:

- `basin_recall`;
- `min_target_survivors_per_basin`;
- `min_basin_geometric_coverage`;
- `max_basin_centroid_drift`;
- `unclustered_target_fraction`;
- `signature_stratum_recall`.

## Selective enrichment

Secondary but scientifically important:

- `candidate_target_recall`;
- viable-target fraction among survivors;
- enrichment of SCR target recall over the rate-matched random-null median;
- empirical placement of SCR recall relative to all null replicates.

## Reporting rule

Always distinguish:

1. candidate contraction;
2. basin/class preservation;
3. target enrichment;
4. computational gain;
5. matched-null behavior.

Do not promote one layer into another.
