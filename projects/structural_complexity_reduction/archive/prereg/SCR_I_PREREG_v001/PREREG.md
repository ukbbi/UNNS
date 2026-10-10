# SCR-I-A Preregistration

## 1. Frozen status

This document freezes **SCR-I-A — Mechanism-Space Reduction Calibration** before outcome-bearing execution.

No gate threshold, target definition, metric, null, seed policy, stopping rule, or success criterion may be changed after the first outcome-bearing run. Any scientific change starts a new preregistration version.

## 2. Research question

Can an upstream UNNS structural gate set reduce downstream Mode-C mechanism evaluation work while preserving all independently defined target mechanisms and producing a net advantage over matched non-structural pruning?

The conceptual paired design is:

```text
BASELINE
candidate universe S0
→ downstream Mode-C evaluator
→ target set T0

SCR
same S0
→ frozen G1∧G2∧G3∧G4 filter
→ survivors S1
→ same downstream Mode-C evaluator
→ target set T1
```

The downstream evaluator must be identical between arms. The filter may not query the downstream target label.

## 3. Scope and scientific status

SCR-I-A is a calibration experiment because its gate family originates in the same broader P3/P4 mechanism program as the downstream Mode-C domain. Therefore:

- a positive result validates **structural contraction plus computational accounting** in the pinned mechanism domain;
- it does **not** establish a complexity-class result;
- it does **not** establish polynomial reduction of an exponential search space;
- it does **not** establish generality outside the pinned mechanism domain;
- it does **not** support claims about replacing quantum computation.

A later independent benchmark must supply the first strong cross-domain computational test.

## 4. Frozen source domain

The benchmark is derived from the pinned Phase P3/P4 mechanism program. Source files and Git blob SHAs are frozen in `SOURCE_LOCK.md` and `config/scr_i_prereg_v001.json`.

The source domain includes:

- three Tier-1 operator pairs from Chamber LII;
- Mode-C curvature-responsive interaction evaluation;
- the P4 mechanism representation and generator variables;
- the P3/P4 gate vocabulary G1–G4;
- the P4 baseline gate thresholds.

## 5. Candidate universe

The primary SCR-I-A corpus is a deterministic generated mechanism pool using the P4 baseline generator distribution:

```text
50% boundary-focused
30% pathological
20% broad coverage
```

Primary pool size per seed: `N = 10,000` mechanisms.

Primary seeds:

```text
2026100601
2026100602
2026100603
2026100604
2026100605
```

This yields 50,000 primary candidate records before filtering.

Three ordered pool-size levels are also frozen for refinement/scaling:

```text
N = 2,500
N = 10,000
N = 40,000
```

The five seeds are used at every level.

## 6. Frozen structural gate set

The primary filter is the conjunction:

```text
G_SCR = G1 ∧ G2 ∧ G3 ∧ G4
```

with the P4 baseline configuration:

```text
G1: curvature_method == "turning_angle"
G2: delta_kappa > 0.05
G3:
    has_bifurcation == true
    AND
    [ sharpness >= 0.10 and temporal_signature_valid
      OR
      0.08 <= sharpness < 0.10 and temporal_quality >= 0.70 ]
G4: locality_score < 0.10
```

These thresholds are not tuned in SCR-I-A.

## 7. Downstream target oracle

The target oracle is the pinned Chamber-LII Mode-C evaluation, not the gate conjunction itself.

A candidate is a **Mode-C positive target** if, under the frozen Mode-C evaluation and shared-seed baseline comparison, it satisfies the Chamber-LII emergence criterion:

```text
SAIF/Mode-C reaches R4
AND flat/shared-seed baseline does not reach R4
AND delta_kappa > 0.05
```

The downstream implementation must use the pinned Chamber-LII logic, including its shared-seed baseline and existing regime thresholds. SCR-I-A may wrap that logic for batch execution but may not redefine it.

Because `delta_kappa > 0.05` also appears in G2, target/gate independence is partial rather than complete. This is why SCR-I-A is classified as a calibration benchmark and not a generalization benchmark.

## 8. Primary hypotheses

### H1 — Candidate contraction

The structural filter produces nonzero candidate reduction:

```text
R_candidate > 0
```

### H2 — Exact target preservation

Every baseline Mode-C positive target survives the SCR filter:

```text
Recall_target = 1.000000
```

This is a hard requirement. One false rejection is a primary failure.

### H3 — Search/evaluation reduction

The SCR arm reduces the number of downstream Mode-C evaluations:

```text
R_eval > 0
```

### H4 — Net computational gain

After counting structural encoding and all gate costs:

```text
G_time = T_base / T_scr > 1
```

or, if timing noise prevents a stable wall-time verdict, the operation-count analogue must satisfy:

```text
G_ops > 1
```

### H5 — Structural advantage over rate-matched random pruning

At identical rejection count, SCR preserves more targets than random pruning. The strict primary comparison is:

```text
Recall_target,SCR = 1
AND
median(Recall_target,RANDOM) < 1
```

If rate-matched random pruning also preserves all targets in every replicate, H5 is not supported even if H1–H4 pass.

## 9. Primary endpoints

The primary endpoints, in order, are:

1. `Recall_target` — exact preservation, must equal 1.
2. `R_eval` — downstream evaluation reduction.
3. `G_time` — net wall-time gain including filter cost.
4. `G_ops` — machine-independent computational-work gain.
5. `Recall_target_random` — rate-matched random control comparison.

`R_candidate` is required but cannot alone produce a positive SCR verdict.

## 10. Secondary endpoints

- per-gate reject count;
- unique reject fraction per gate;
- gate-overlap matrix;
- target enrichment among survivors;
- peak memory ratio;
- gain across N = 2,500 / 10,000 / 40,000;
- seed-to-seed dispersion;
- survivor composition by generator mode;
- rejection reason distribution;
- UPI association after primary lock.

## 11. Cost accounting

The SCR-arm cost is:

```text
T_scr = T_encode + T_gate + T_downstream_survivors
```

No per-instance work required to compute gate inputs may be omitted.

The baseline cost is:

```text
T_base = T_downstream_all_candidates
```

Report both warm-cache and cold-start execution if implementation startup materially affects results. Primary inference uses the median of repeated steady-state trials on the same machine.

## 12. Timing protocol

For each seed and pool size:

- one untimed warm-up;
- five timed baseline runs;
- five timed SCR runs;
- arm order alternates by seed;
- record wall clock with a monotonic high-resolution timer;
- record CPU time when available;
- no other intentional heavy workload during timing;
- report raw trials, median, and median absolute deviation.

No timing outlier is deleted unless the process fails an explicit integrity check. Retained anomalies remain in raw exports.

## 13. Null controls

Required nulls are frozen in `NULLS.md`:

- IDENTITY;
- RATE_MATCHED_RANDOM;
- ORDER_SHUFFLED;
- GATE_LABEL_PERMUTED diagnostic control.

Random controls use 100 replicates per seed at `N=10,000` and 30 replicates per seed at the other pool sizes.

## 14. UPI blinding

UPI is computed only after the primary SCR result record for a candidate pool is finalized.

UPI:

- cannot prune;
- cannot alter gate order;
- cannot alter target definition;
- cannot determine the primary verdict.

See `UPI_BLIND.md`.

## 15. Negative-space preservation

Every rejected candidate remains in the export with:

```text
candidate_id
generator_mode
seed
pool_size
G1/G2/G3/G4 verdicts
first_reject_gate
all_reject_gates
structural observables
target label from baseline oracle
representation/source IDs
```

Deletion of rejected candidates invalidates the run.

## 16. Stopping rule

The primary experiment ends after all frozen seeds, sizes, timing repetitions, and required null replicates complete or are classified as explicit technical failures.

Do not stop early for a favorable or unfavorable result.

## 17. Integrity failures

A run is technically invalid if any of the following occurs:

- upstream source lock cannot be verified;
- different downstream evaluator logic is used between arms;
- candidate IDs differ between baseline and SCR arms before filtering;
- gate thresholds differ from the frozen config;
- filter reads the downstream target label;
- random-control rejection count differs from the SCR rejection count;
- missing rejected-candidate records;
- seed reproduction fails;
- result JSON fails schema validation.

Technical invalidity is not a scientific negative result; it must be repaired and rerun under the same frozen preregistration if no scientific parameter changes.

## 18. Interpretation boundary

A positive SCR-I-A result supports:

> Within the pinned P3/P4 mechanism domain, frozen structural gates can reduce downstream Mode-C evaluation work while preserving the frozen target set, with filter cost explicitly counted.

It does not support broader complexity-theoretic claims. Those require later independent benchmarks.
