# PRIMARY_AUTHORIZATION_v001 — SCR-III-B Primary Execution

**Date:** 2026-10-10
**Authorized by:** Igor (project owner), explicit instruction in session: "complete the minimal manifest check, explicitly authorize the frozen primary run, and proceed without further unnecessary gates"; skip a separate PRIMARY_GATE_v001 milestone.
**Status:** PRIMARY_EXECUTION_AUTHORIZED (frozen protocol only)

## Scope
Execute exactly the protocol in `SCR_III_B_SPEC_v001_FINAL.md` (sha256 8a7d9178…80af) and `SCR_III_B_PREREG_v001_FINAL.md` (sha256 cd7e0c76…9f88), per `PRIMARY_FREEZE_v001.md` / `RATIFY_v001.md`. Real 3×3 at W = k_B·792 K (primary) and 0.5×, 2× (sensitivity). The W>0 guard is lifted ONLY through the `--unblind-after-freeze` flag of the frozen v009 binaries, ONLY by the driver below. No other change to frozen files; GitHub untouched. Hypotheses reported independently as (G, P, T, C); T = NOT_TESTED.

## Pre-execution check (automated, built into the driver; aborts on any failure)
Final-document hashes vs PRIMARY_MANIFEST; v005–v009 manifest hashes (code and outputs); seed 20261010; tau_rel 1e-9; W and E0 constants; compile flags (`-std=c++17 -O2 -Wall -Wextra`, as in v009); guard blocks the W>0 real-3×3 request without the flag. No numerical benchmarks, null tests or solver-equivalence experiments are repeated.

## Disclosed deviations / additions (none alters a frozen scientific input)
1. No primary driver existed in v009. `scr_iii_b/primary_exec/primary_run_v001.py` (sha256 973e4e83e91342d63bfd29231f0a0d09371b9edcbe4d5d7687d41d0abf58aa48) is new orchestration code that calls the frozen v009 solvers, instance builders, seed derivation and cost accounting unchanged.
2. `cost_audit_v009.py` still contains the rejected nominal-95% bootstrap; the driver does not use it. H-C is decided only by the ratified rule (median ≥ 1.20 AND min ≥ 1.20 over 15 paired B0/G2 rounds, charged totals per `cost_audit_v009.charged`, E0 treated as a common given input). A deployment scenario adding a cert_b1 E0 certification to G2 is reported separately and does not decide C.
3. An independent numpy whole-space audit (float64) cross-checks the target set, grammar set and Δ_nonG. It is an offline scientific audit, not a solver arm.
4. Timing is run only if H-P PASSES (C is NOT_ELIGIBLE otherwise). Environment is this driver's host (Linux VM on the user's computer, 2 CPUs), not the earlier container or WSL runs.
5. v005 original Dryad sources and PREFLIGHT_v005–v009 zips are not on disk; verification uses the extracted-tree manifests.
6. Nulls: 1000 valid N1 + 1000 valid N2, cap 5000 draws each, descriptive only.

## Addendum A (2026-10-10) — first execution attempt aborted; driver revised
The first launch of the driver (sha256 973e4e83…8aa48) completed the pre-execution check, the numpy audit and the per-window solver runs (primary window: 26 target states, 16 outside the grammar), then was terminated by the host sandbox during the null phase, before any result file was written. Its partial artifacts are retained unaltered in `scr_iii_b/output/primary/aborted_run_1/`. The driver was revised ONLY to add checkpoint/resume (phase A results, generated nulls, per-null rows); no scientific logic, parameter or decision rule changed. Revised driver sha256: 2df1613432aa9d79e59246c239ec0b98cf5a885e4ba462c53d5d964f40d0c18b. The full run is repeated from the start under the revised driver; the aborted attempt's values are not used for any verdict.
