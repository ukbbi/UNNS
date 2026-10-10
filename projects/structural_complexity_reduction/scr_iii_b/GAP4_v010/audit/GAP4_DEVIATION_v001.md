# GAP4 — Additive execution deviation and witness audit v001

**Record date:** 2026-10-10  
**Status:** `REAL_4X4_COMPLETED / WITNESS_PASS / GAP_INCONCLUSIVE_PENDING_OPTIMALITY_CERTIFICATION`  
**Frozen predictions unchanged:** R2 [0.790439676056526, 1.0333534753990623] and independent delta4 < 1.

## Prospective plan versus execution

- The prediction freeze required a separate execution authorization and proposed an implementation check with numerical certification. The user subsequently explicitly requested the physical attempt; it was carried out with `make_instance_v010.py --authorize-real` and `solver_v010` at 150 seconds per objective. The uploaded package's original prediction freeze continued to say `REAL_4X4_NOT_AUTHORIZED`; therefore this **additive** record documents a procedural deviation, not retroactive compliance.
- The proposed 200-synthetic-instance feasibility campaign, 90% pass fraction, and 28/32-bit correctness gate were **not completed**. Instead the minimal v010 solver passed the public 1x1 and 2x2 tests and a generator guard check, then was run on real 4x4.
- The solver did not emit a machine-checkable optimality proof tree or rigorous interval-arithmetic certificate. A `completed:true` field means its depth-first search finished under the implemented floating-point pruning rule; the output `lower=upper` is an assignment made at completion, not an independent lower-bound proof.
- Do not alter any earlier freezes, source binaries, primary outcomes or prediction values; no replacement experiment was conducted for this record.

## Read-only witness verification

Input: `real_4x4.txt` (40 spins, 16 vertex constraints, 780 pair couplings). Output: `GAP4_FIRST_RUN.jsonl`.

A separate Python witness checker read each spin ID, evaluated all 780 pair terms using `math.fsum`, and calculated 2-in/2-out vertex incidence from the serialized vertex masks. The checker invokes neither the v010 binary nor its branch-and-bound code.

| Check | Ground witness | Non-grammar witness |
|---|---:|---:|
| State ID | 711243241830 | 161487427942 |
| Energy (A units) | -0.16364841082886986 | -0.1534031680911189 |
| Solver `completed` | true | true |
| Visited nodes | 700405 | 1316073 |
| Violated vertices | 0 | 1 |

Gap from witness energies: `0.01024524273775096` A units; normalized candidate about `0.945917 kBT`, inside frozen R2 and below 1. Witness recomputation verifies **feasible energies and membership**, not global optimality. The ground witness is also grammar-admissible, but grammar membership of the ground state alone does not prove that no lower-energy state exists.

## Mathematical and numerical certification distinction

The branch-and-bound code's real-arithmetic relaxation uses a valid form for a partial assignment: assigned-pair energy minus absolute assigned-to-unassigned fields minus absolute unassigned-pair couplings. Under exact arithmetic this lower-bounds every completion. The non-grammar pruning predicate is a permissive feasibility filter based on 4-spin vertex constraints. **Nevertheless**, the implementation uses `double` arithmetic and an ad hoc `1e-11 * max(1,scale)` downward margin rather than formally proved directed-rounding or interval bounds. The margin appears generous compared with observed rounding differences, but no documented worst-case proof or independent proof trace establishes global lower bounds. The completion output copies the best witness energy into `lower` and should not be read as separate numerical certification.

**Frozen-rule adjudication now:** `GAP_INCONCLUSIVE` for R2 and for delta4<1, **with both predictions provisionally supported by the computed candidate gap**. Promotion to `GAP_CONSISTENT` requires a justified globally valid optimality certificate for *both* objectives (including numeric error), independent witness checks already passed. This verdict avoids recasting uncertified floating-point pruning as a physical proof.

## Integrity and follow-up

See `GAP4_WITNESS_REPORT_v001.json` for file hashes, direct pair-energy re-evaluation and per-vertex counts. The script `GAP4_WITNESS_CHECK_v001.py` reproduces that report without running either optimization. Only a targeted solver-bound audit is outstanding; repeating the trillion-state-scale search is not required.
