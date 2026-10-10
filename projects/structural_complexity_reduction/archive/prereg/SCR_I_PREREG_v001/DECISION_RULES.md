# SCR-I-A Decision Rules

## POSITIVE — SCR_CALIBRATION_SUPPORTED

Assign only if all conditions hold on the combined primary experiment:

1. source and config integrity pass;
2. at least one baseline Mode-C positive target exists;
3. `Recall_target = 1.000000`;
4. `R_eval > 0`;
5. median `G_time > 1` across primary seed×size cells **or** preregistered `G_ops > 1` with timing classified as noisy/indeterminate;
6. no primary integrity failure;
7. IDENTITY control reproduces baseline exactly.

A positive verdict may be qualified as `NO_RANDOM_ADVANTAGE` if rate-matched random pruning also preserves every target sufficiently often that H5 is not supported.

## NEGATIVE — TARGET_LOSS

Assign if at least one baseline target is rejected by the frozen structural filter:

```text
Recall_target < 1
```

This has priority over computational gain. A faster filter that loses a valid target fails SCR-I-A.

## NEGATIVE — NO_WORK_REDUCTION

Assign if target recall is perfect but:

```text
R_eval <= 0
```

## NEGATIVE — NET_SLOWDOWN

Assign if target recall is perfect and downstream evaluations fall, but after filter cost:

```text
G_time <= 1
AND G_ops <= 1
```

## NULL-COMPATIBLE — NO_STRUCTURAL_ADVANTAGE

Assign as a qualifier when SCR preserves targets but rate-matched random pruning performs equivalently under the frozen control criterion.

This does not erase candidate contraction; it means the experiment does not establish that the contraction is structurally selective.

## INDETERMINATE — NO_TARGETS

Assign if no Mode-C positive targets occur across the entire primary baseline corpus.

## INVALID — TECHNICAL

Assign when a preregistered integrity condition fails. Technical invalidity is not converted into a scientific negative or positive result.

## No post-hoc rescue

After an outcome-bearing run, do not:

- relax a gate threshold;
- reorder primary gates;
- delete a difficult seed;
- change target definition;
- reclassify a target as non-target;
- omit filter cost;
- replace a failed result with a new configuration under the same version.

Any scientific redesign starts `SCR_I_PREREG_v002` or later.
