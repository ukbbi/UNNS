# SCR-I-A Frozen Metrics

## Symbols

```text
N0      candidate count before pruning
N1      survivors after all gates
Q_base  downstream candidate evaluations in baseline arm
Q_scr   downstream candidate evaluations in SCR arm
T0      baseline target-positive set
T1      SCR-arm target-positive set
T_base  baseline wall time
T_enc   SCR structural encoding time
T_gate  SCR gate time
T_down  SCR downstream evaluation time
T_scr   T_enc + T_gate + T_down
```

## Primary metrics

### Target recall

```text
Recall_target = |T0 ∩ T1| / |T0|
```

Hard success condition: `Recall_target = 1`.

### Candidate reduction

```text
R_candidate = 1 - N1/N0
```

### Downstream evaluation reduction

```text
R_eval = 1 - Q_scr/Q_base
```

For exhaustive baseline and one downstream evaluation per candidate, `Q_base = N0`; nevertheless both are recorded explicitly.

### Net time gain

```text
G_time = T_base / T_scr
```

Interpretation:

```text
>1 net speedup
=1 parity
<1 slowdown
```

### Net operation gain

```text
G_ops = C_base / (C_filter + C_downstream)
```

The implementation must document the operation-count proxy used.

## Gate diagnostics

For each gate `g`:

```text
reject_g = count failing g
unique_reject_g = count failing only g in full audit
first_reject_g = count first rejected at g in timed order
```

Also export the 4×4 gate failure-overlap matrix.

## Target enrichment

```text
TargetRate_base = |T0|/N0
TargetRate_survivors = |T1|/N1
Enrichment = TargetRate_survivors / TargetRate_base
```

Enrichment is secondary and cannot substitute for exact target recall.

## Memory

```text
R_memory = 1 - M_scr/M_base
```

using peak resident set size when available.

## Null comparison

For rate-matched random replicate `j`:

```text
Recall_random_j
G_time_random_j
```

Primary structural-control summary:

```text
P_random_perfect = fraction of random replicates with Recall_random_j = 1
```

A favorable SCR-specific result has `Recall_target,SCR = 1` and low `P_random_perfect` at comparable rejection rate.

## Scaling report

For every pool size and seed report:

```text
R_candidate
R_eval
G_time
G_ops
Recall_target
```

Never report only an aggregate mean.
