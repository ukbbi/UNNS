# SCR-I-A Null and Control Plan

## N0 — IDENTITY

No candidate is removed.

Purpose:

- verify paired-arm equivalence;
- verify downstream evaluator determinism;
- verify instrumentation overhead.

Required result:

```text
T_identity = T0
Recall_identity = 1
N1 = N0
```

Any mismatch invalidates the run.

## N1 — RATE_MATCHED_RANDOM

For each SCR pool, remove exactly the same number of candidates as SCR but choose rejected IDs uniformly without replacement.

Rules:

- random control never sees structural metrics or target labels;
- 100 replicates per seed at N=10,000;
- 30 replicates per seed at N=2,500 and N=40,000;
- control seed = deterministic hash of `{primary_seed, replicate_id, "N1"}`.

Primary comparison: target recall at identical rejection count.

## N2 — ORDER_SHUFFLED

Randomly permute candidate structural-field assignments across candidate IDs before gate application while preserving each field's marginal distribution as far as the implementation permits.

The downstream target labels remain attached to the original candidate IDs.

Purpose: test whether the joint structural organization, not merely marginal gate rates, carries preservation information.

Frozen replicates: 30 per primary seed at N=10,000.

## N3 — GATE_LABEL_PERMUTED diagnostic

Permute the association between gate outcomes and candidate IDs after all gate outcomes have been computed, keeping the same total number of each gate pass/fail outcome.

This is an offline diagnostic, not a timed arm.

Purpose: test whether apparent gate-specific enrichment survives destruction of candidate-level alignment.

## Adversarial reporting

The P4 generator already includes pathological mechanisms. Report preservation and rejection separately for:

```text
boundary
pathological
broad
```

Do not treat pathological candidates as a null; they are part of the primary universe.
