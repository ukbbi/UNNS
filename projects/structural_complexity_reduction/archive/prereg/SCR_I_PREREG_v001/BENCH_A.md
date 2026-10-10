# SCR-I-A — Mechanism-Space Reduction Calibration

## Benchmark role

Benchmark A is the calibration bridge between the previously established P3/P4 mechanism-space contraction program and the new SCR computational program.

It converts the older statement

```text
structural gates contract mechanism space
```

into the stronger computational question

```text
Does gate contraction reduce downstream work after filter cost is counted,
and does it preserve the independently evaluated Mode-C target set?
```

## Candidate record

Each mechanism candidate must expose at least:

```text
candidate_id
gamma0
beta
d
kmax
curvature_method
locality_mode
bifurcation_spoof
regime_flip_injector
family
composition
delta_kappa
has_bifurcation
sharpness
temporal_signature_valid
temporal_quality
locality_score
generator_mode
seed
```

The generator logic is pinned to the P4 baseline source. A Python/JS batch adapter may be written, but its output must be regression-checked against the pinned source on a fixed test seed before primary execution.

## Pool construction

Primary generator mixture:

```text
boundary = 0.50
pathological = 0.30
broad = 0.20
```

Frozen continuous parameter ranges inherited from P4:

```text
gamma0 ∈ [0, 2]
beta   ∈ [0, 2]
d      ∈ [0, 5]
kmax   ∈ [0, 6]
```

Frozen categorical mechanism axes inherited from P4:

```text
curvature_methods:
  turning_angle, finite_diff, smoothed, biased, wrong_metric

locality_modes:
  local, bounded_nonlocal, nonlocal_global, teleport

bifurcation_spoofs:
  none, remote_step, hysteresis_loop

regime_flip_injectors:
  none, seed_sensitive, gamma_sensitive

families:
  flat, saif, curvature_gated, logit_sigmoid

compositions:
  utility_count, logit_sigmoid
```

## Baseline arm

For every candidate:

1. construct candidate deterministically;
2. run the pinned downstream Mode-C evaluation;
3. run the shared-seed flat baseline required by Chamber LII;
4. classify the candidate as target-positive or target-negative;
5. record downstream evaluation cost.

No structural candidate may be skipped.

## SCR arm

For the identical candidate pool:

1. compute required structural observables;
2. apply G1, G2, G3, G4 in the frozen order;
3. preserve all rejection records;
4. run the identical downstream Mode-C evaluator only on survivors;
5. compare target set with the baseline target set;
6. add filter cost to SCR-arm cost.

## Gate order

The primary gate order is frozen as:

```text
G1 → G2 → G3 → G4
```

Gate order affects early-termination cost. Therefore it is part of the preregistration and may not be optimized after observing primary results.

A secondary offline calculation may compute hypothetical alternative orders **without** changing the primary verdict.

## Downstream target definition

The pinned Chamber-LII emergence definition is used:

```text
Mode-C/SAIF R4 = coverage_abs_delta_ge_0_20 >= 0.25
flat baseline not R4 = baseline coverage_abs_delta_ge_0_20 < 0.25
curvature increase = kappa_modeC > kappa_baseline + 0.05
```

Target-positive iff all three conditions hold.

## Preservation rule

Let `T0` be all target-positive candidates found by exhaustive baseline evaluation and `T1` the target-positive candidates found after SCR filtering.

```text
Recall_target = |T0 ∩ T1| / |T0|
```

Required:

```text
Recall_target = 1.0
```

If `T0` is empty for a seed/pool, that seed is not sufficient for preservation inference. The experiment is not stopped; all seeds run. Overall preservation is evaluated on the union across all primary pools. If the entire primary experiment yields no targets, the preservation endpoint is INDETERMINATE and SCR-I-A cannot receive a positive verdict.

## Work accounting

Primary native work units:

```text
Q_base = number of downstream candidate evaluations in baseline arm
Q_scr  = number of downstream candidate evaluations in SCR arm
Q_gate = primitive gate evaluations actually executed with early termination
```

Report:

```text
R_eval = 1 - Q_scr/Q_base
G_ops  = C_base/(C_gate + C_downstream)
```

`C_gate` must be defined from actual primitive operations or an implementation-independent proxy before the main run. Wall time remains co-primary because operation weighting is imperfect.

## Refinement/scaling levels

Frozen candidate-pool sizes:

```text
2,500
10,000
40,000
```

A structurally meaningful reduction should not appear only at one isolated pool size.

No monotonic scaling law is required for success in SCR-I-A, but the direction and magnitude across levels must be reported.
