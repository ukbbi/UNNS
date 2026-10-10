# SCR-I-A Frozen Run Plan

## Phase 0 — Source verification

1. verify pinned upstream blob SHAs;
2. record local file SHA-256 values;
3. validate preregistration package;
4. freeze software/environment record.

## Phase 1 — Adapter regression

Build the batch adapter for the pinned P4 generator and LII Mode-C downstream evaluator.

Before primary execution, run a fixed regression seed and verify:

- deterministic candidate generation;
- exact G1–G4 verdict agreement with the pinned gate logic;
- exact downstream target classification agreement on a hand-audited sample;
- IDENTITY arm exact equality.

Adapter bug fixes are allowed before the first outcome-bearing primary run. No gate or target changes are allowed.

## Phase 2 — Primary baseline

For each pool size in `2500, 10000, 40000` and each primary seed:

1. generate complete candidate pool;
2. persist candidates before evaluation;
3. run exhaustive downstream Mode-C oracle;
4. persist target labels and raw downstream metrics;
5. record timing/work/memory.

## Phase 3 — Primary SCR arm

On the byte-identical candidate pool:

1. apply timed gate chain G1→G2→G3→G4 with early termination;
2. persist negative-space records;
3. downstream-evaluate survivors only;
4. compute target recall;
5. record filter and downstream costs separately.

## Phase 4 — Full gate audit

Outside primary timing, evaluate all four gates on all candidates to obtain overlap and unique-rejection statistics.

## Phase 5 — Null controls

Run N0–N3 exactly as frozen in `NULLS.md`.

## Phase 6 — Primary lock

Generate `PRIMARY_RESULT.json`, validate against schema, compute SHA-256, and mark the primary result frozen.

## Phase 7 — UPI analysis

Only after Phase 6 may UPI be joined or computed.

## Phase 8 — Synthesis

Produce:

```text
PRIMARY_RESULT.json
SUMMARY.md
candidate_results.csv
gate_audit.csv
null_results.csv
timing_trials.csv
upi_secondary.csv (after primary lock)
RUN_ENVIRONMENT.json
```

No primary verdict is rewritten after UPI analysis.
