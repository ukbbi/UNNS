# Primary metrics

For each seed × pool-size cell:

`R_candidate = 1 - N1/N0`, where N0 is the nominal candidate count and N1 the number surviving G1→G4.

`R_eval = 1 - Q_scr/Q_base`, where the downstream evaluation counts are `Q_base=N0` and `Q_scr=N1`.

`target_recall = |T_base ∩ T_scr| / |T_base|` with exact candidate identity matching. Required value: 1.0.

`G_time = median(T_base) / median(T_filter + T_downstream_scr)`.

The operation proxy counts 20 replicate-regime steps plus six viability checks per downstream candidate, while each actually executed gate predicate contributes one unit. `G_ops = C_base / C_scr` includes gate work.

Report medians and median absolute deviations for timings. Candidate and target counts are exact integers, not estimates.
