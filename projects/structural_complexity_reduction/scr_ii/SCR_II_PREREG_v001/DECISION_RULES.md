# Decision rules

Evaluate in order.

## D0 — Integrity

Fail as `INVALID_RUN` if any of the following occur:

- source/config hash mismatch;
- primary seed duplication with calibration/design seeds;
- incomplete primary grid;
- non-deterministic generator reproduction;
- baseline exact solver disagreement with independent brute-force unit tests.

## D1 — Preservation

If any primary instance has `S_SCR != S_baseline`:

`PRESERVATION_FAIL`

Stop primary claim escalation. Continue remaining instances only for diagnosis if preregistered run budget allows.

## D2 — Search reduction

If preservation passes but median `R_node < 0.25` at any of d=14,16,18:

`NO_MATERIAL_REDUCTION`

## D3 — Net gain

If D1–D2 pass but median `G_time < 1.10` at d=16 or d=18:

`REDUCTION_WITHOUT_NET_GAIN`

## D4 — Computational transfer

If D1–D3 pass:

`COMPUTATIONAL_TRANSFER_CONFIRMED`

## D5 — Exploratory scaling

If D4 passes and the frozen exploratory scaling rule in `SCALING.md` passes:

`TRANSFER_WITH_SCALING_SIGNAL`

Do not infer P=NP, polynomial-time conversion, quantum-computing replacement, or general complexity-class collapse from any SCR-II verdict.
