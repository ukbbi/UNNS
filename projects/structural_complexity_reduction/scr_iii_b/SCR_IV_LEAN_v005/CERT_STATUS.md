# SCR-IV v005 — Certification status (IV-5 on top of IV-4B)

**Date:** 2026-10-10 · **Toolchain:** Lean 4.34.1 (commit 5045d0056413), core only (no Mathlib) · **Built and run in:** Claude's cloud container (2 cores, 8 GB), not yet in your WSL. v001–v004 packages are unchanged.

| Stage | Verdict | Basis |
|---|---|---|
| IV-1 | MODEL_FORMALIZED (unchanged) | v001 sources byte-identical |
| IV-2 | WITNESSES_CERTIFIED (unchanged; see finding below) | 25 theorems. They certify the witnesses of the FROZEN SCR-III values. |
| IV-3 | PRUNING_THEOREM_PROVEN (unchanged) | 44 theorems |
| IV-4A | CERTIFICATE_DESIGN_AND_CHECKER_PROVEN (unchanged) | 24 theorems |
| **IV-4B** | **GLOBAL_OPTIMA_CERTIFIED (exact encoded model), with one correction to the frozen non-grammar value** | below |
| **IV-5** | **EXACT_GAP_AND_PREDICTIONS_CERTIFIED (exact encoded model)** | `SCR_IV_V5.lean`, `SCR_IV_V5Final.lean`; see section IV-5 below and `GAP4_EXACT_ADDENDUM_v001.md` |

## IV-4B results (kernel-checked, only propext / Classical.choice / Quot.sound; no sorry, no native_decide)

* `ground_exact_min : ObjAll claimedGroundNum` — claimedGroundNum = −193201942568284180326 / 2^70 is the exact minimum of the encoded Hamiltonian over all 2^40 configurations. Attained by id 711243241830 (IV-2). **The frozen SCR-III ground energy is confirmed.**
* `frozen_nonG_not_min : ¬ ObjNonGrammar claimedNonGNum` (unconditional) — the frozen SCR-III non-grammar value −181106494839879484608 / 2^70 is **not** the exact minimum over non-grammar configurations.
* `nongT_exact_min : ObjNonGrammar claimedNonGTrue` — the exact non-grammar minimum is −181106494839879485536 / 2^70, attained by id 711243241766 (the ground witness with spin 6 flipped; vertex 3 has 3 inward arms, all other vertices 2). Facts: `nonGTrue_valid`, `nonGTrue_not_in_grammar`, `nonGTrue_violating_vertex`, `nonGTrue_counts`, `nonGTrue_energy_exact`, `nonGTrue_one_flip`, `frozen_minus_true` (= 928).

### The finding
The frozen value exceeds the true non-grammar minimum by 928/2^70 ≈ 7.9e-19 A (relative ≈ 7.7e-17 of the gap). The frozen witness 161487427942 is therefore not a minimiser. This is far below the original solver's outward guard (1e-11, recorded in the SCR-III audit), so a floating-point branch-and-bound with that guard cannot separate the two states; the frozen value is correct to the solver's resolution, not in exact arithmetic. (This explanation is consistent with the recorded guard but was not re-derived from the solver trace.) The exact gap numerator changes from 12095447728404695718 to 12095447728404694790 (units 2^-70 A). Both give Δ = 0.010245242737750961 A when rounded to binary64. δ₄ was NOT recomputed here (IV-5); the change is below double resolution, so no change in reported precision is expected, but that is unverified. No frozen file was modified.

## IV-5 results (kernel-checked; exact-arithmetic lemmas need no axioms, the core theorem uses propext/Quot.sound, the final theorem the three allowed axioms)
* `iv5_final : ∀ U0 Un, ObjAll U0 → ObjNonGrammar Un → U0 = claimedGroundNum ∧ Un = claimedNonGTrue ∧ Un − U0 = 12095447728404694790 ∧ 0 < Un − U0 ∧ PredLt1 U0 Un ∧ PredR2 U0 Un` — obtained from `iv5_of_minima` applied to the accepted `ground_exact_min` and `nongT_exact_min`; the 1,148 batches are imported, not re-run.
* Exact Δ = 12095447728404694790/2^70 A > 0. δ₄ = Δ·A(792 K)/(k_B·792 K) as an exact fraction: δ₄ < 1 (1 − δ₄ > 0.054) and 0.790439676056526 ≤ δ₄ ≤ 1.0333534753990623 (margins > 0.0874 upper, > 0.155 lower). Both predictions hold for the corrected AND the frozen value; the correction moves δ₄ by < 1e-15.
* The reported δ₄ = 0.9459172223430824 agrees with the exact value to < 3e-16; the exact double is …826 (floating-point evaluation in the original, independent of the 928/2^70 correction). Reported Δ agrees to < 2e-17 A.
* Controls (`tests/neg5_*`, five false claims rejected: frozen gap numerator for the corrected pair, δ₄ below its value, false lower range bound, δ₄ < 0.9, wrong temperature; `tests/pos5.lean` true twins compile).
* Default `RUN_TEST.sh` verifies the conditional core; `iv5_final` needs the batch modules (`FULL=1`). Recorded author run: `output/author_run/axiom_audit_iv5_final.txt`.

## How IV-4B was certified
* Certificates: untrusted exact-integer Python (`scripts/gen4b.py`), D0 = 14 → 16384 frontier prefixes per objective. Ground: 503,096 proof nodes (max 985 per prefix). Corrected non-grammar: 1,135,204 nodes (max 2,519 per prefix). Files in `certs/` (sha256 in MANIFEST_SCR_IV_v004.json).
* Checking: 344 (ground) and 804 (non-grammar) batch modules `Bat/B?_NNN.lean`, each one `decide +kernel` theorem `batchOK … = true`; assembled in `Fin_g.lean`/`Fin_n.lean` through `batches_cover` and `ground_min_of_frontier` / `nonGT_min_of_frontier`. All batches accepted (logs/*.json).
* Measured kernel cost: ground 1945 s wall / 3808 s CPU, peak 3.3 GB per process; non-grammar 3451 s wall / 6760 s CPU, peak 2.5 GB (2 concurrent processes). That is ≈ 7.6 and 6.0 ms CPU per node, against the IV-4A estimate of 4.3–5.4 ms, so the total (2.9 CPU-hours) is close to the ~3 h estimate and well inside the 3× stop limit.
* Controls on the real instance (`tests/neg4b_*`, all rejected by the kernel; `tests/pos4b_*`, all compile): ground with U+1, tampered token, truncated, trailing junk, wrong rows, wrong prefix; corrected non-grammar with U+1, with the FROZEN value claimedNonGNum, and with the leaf rule removed.
* Earlier attempts that failed and why (kept for honesty): D0 = 12 with 4,700-node batches and unbounded `lake build` parallelism were OOM-killed (batches cost ≈1.5 MB per node in one theorem, more than the 0.5–0.7 MB/node of standalone prefix theorems). The delivered configuration (D0 = 14, ≤1,500 nodes per batch, 2 concurrent Lean processes via `scripts/verify_batches.py`) completed without a failure. A sibling-prefix swap was ACCEPTED by the checker; that is correct (the checker recomputes every bound from the prefix) and is not a control.

## Limits (keep reading these)
1. Exact-arithmetic statements about the encoded dyadic model (kShift = 70). The binary64 rounding and 1e-11 guard of the original solver are not formalised; the physical couplings are the double values read from real_4x4.txt, taken exactly.
2. Minimum VALUES are certified, not the set of minimisers (non-strict pruning). In particular nothing here says the ground state is unique.
3. The grammar convention (2-in/2-out at the 16 listed vertices) is the frozen-file convention; agreement with the geometric ice rule is evidenced by `scripts/diff_test.py`, not proved.
4. The certificate generator, the diagnostic, the batch writer and the runner are untrusted; only the Lean kernel's acceptance matters. The recorded run used `scripts/verify_batches.py`, which compiles each batch to an .olean with `lean -o`, not `lake build SCR_IV_B` (see 5).
5. `lake build SCR_IV_B` starts too many parallel Lean processes for 8 GB and was OOM-killed; use `scripts/verify_batches.py` (or `FULL=1 bash RUN_TEST.sh`).
6. Full re-verification in `RUN_TEST.sh` is opt-in (`FULL=1`, ~1.5 h). A default run regenerates the certificates, checks they equal the shipped ones, audits the V4 theorems and runs the controls, but does NOT re-check the 1,148 batches.
7. A(792 K) is the frozen binary64 value from `physical_energy_v005.A_joule(792.0)` (verified equal in Python), taken exactly; its physical derivation is not formalised. Range endpoints are the frozen decimal literals read as exact rationals.
