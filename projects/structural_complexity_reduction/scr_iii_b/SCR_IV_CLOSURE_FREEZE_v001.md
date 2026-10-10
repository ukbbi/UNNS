# SCR-IV — Closure and Final Freeze v001

**Date:** 2026-10-10  
**Project:** UNNS Substrate — Structural Complexity Reduction / SCR-IV Certified Structural Optimization  
**Final project verdict:** `SCR_IV_COMPLETE / FINITE_GAP_CERTIFIED / PREDICTIONS_PROVEN`  
**Status:** Closed by research decision; additive closure record. No frozen prior evidence is rewritten.

## 1. Immutable closure set

The following deliverables are designated **frozen**; retain their exact bytes, filenames, histories, and hashes:

| Artifact | SHA-256 | Role |
|---|---|---|
| `SCR_IV_LEAN_v005.zip` | `b8dcd220ff7beb1e8e209627a88820107510aef0dd45d62fcfa30320db0740fd` | Final Lean source, batch certificates, theorem records, logs, manifests, controls |
| `GAP4_EXACT_ADDENDUM_v001.md` | `b6471c06804448be4eafecb78d424a5f7649bbdc38093eda8ddf3d1e45c0440d` | Additive exact-arithmetic correction and interpretation |
| `GAP4_RESULT_FREEZE_v001.md` | `9771ab659c38c098afcbab9a54351c6669564b0377a8be5893db0f3f080b77c3` | Prior SCR-III frozen numerical result; remains unchanged |

SHA-256 of the first two artifacts was recomputed against the attachments in this conversation. The SCR-III freeze hash is recorded in the addendum; the source file was not available here for rehashing. Earlier `SCR_IV_LEAN_v001.zip` through `v004.zip` remain immutable and are not superseded as historical research evidence. The closure record itself is a new additive document, not a modification to any archived package.

## 2. Certified mathematical conclusion

Under the **exact encoded finite Hamiltonian** consisting of 40 spins, 16 local ice-rule vertices and 780 binary64 couplings interpreted as exact dyadic rationals (denominator `2^70`), the recorded Lean 4.34.1 kernel executions establish:

- Ground minimum over the complete `2^40` state space, attained at ID `711243241830`:
  `E0 = -193201942568284180326 / 2^70 A`.
- Lowest energy over non-grammar states, attained at ID `711243241766`:
  `EnonG = -181106494839879485536 / 2^70 A`.
- Exclusion gap:
  `Delta_nonG = 12095447728404694790 / 2^70 A > 0`.
- Frozen directional prediction `delta4 < 1`: **proved**.
- Frozen R2 prediction interval `0.790439676056526 <= delta4 <= 1.0333534753990623`: **proved**.

Lean theorem anchors: `ground_exact_min`, `nongT_exact_min`, `frozen_nonG_not_min`, `gap_exact`, `gap_pos`, `pred_lt1_true`, `pred_r2_true`, and `iv5_final`. The exact frozen non-grammar candidate is **not** the exact encoded minimum: its energy exceeds the corrected value by `928 / 2^70 A`. This correction is vastly below the original solver's stated numerical guard. The original numerical freeze remains the accurate historical record of that solver's output; no causal trace attribution is claimed.

## 3. Execution and verification boundary

- Final theorem and 1,148 batch checks are supported by execution records in `SCR_IV_LEAN_v005.zip/output/author_run/` and earlier v004 logs. Reported Lean axiom audit: only `propext`, `Classical.choice`, and `Quot.sound`; no `sorry` and no `native_decide`.
- The standard `bash RUN_TEST.sh` is a **partial/default** verification, not a full 1,148-batch kernel recheck. The full campaign is `FULL=1 bash RUN_TEST.sh`.
- **Local WSL reproducibility check is explicitly waived by the user** at closure. No WSL execution is represented as completed. Lean runs were performed in the cloud container and are evidenced by supplied logs. This is a deliberate verification-scope decision, not a missing mandatory step or an implicit claim of independent replication.
- No new physical optimization, experiment, held-out transfer study, or alternative-solver benchmark is authorized by this closure.

## 4. Scientific scope and exclusions

The final verdict means that **for the exact encoded finite model**, the recorded formal verification certifies the minimum energy values, strictly positive exclusion gap, and the two previously frozen predictions. It does **not** certify the source physical Hamiltonian as an interval family, the original solver's binary64 pruning, uniqueness or degeneracy of minimizers, thermodynamic-limit positivity, independent physical transfer, or UNNS-specific computational acceleration. Differential geometric grammar correspondence remains tested rather than Lean-proved.

The SCR-III primary outcome `G_PASS / P_FAIL / T_NOT_TESTED / C_NOT_ELIGIBLE` is unchanged. The separate held-out program and six open defaults remain unapproved and unchanged.

## 5. Preservation policy and closure authorization

1. Do not overwrite, delete, reformat, or repackage any frozen SCR-III or SCR-IV v001–v005 artifact.
2. Store this closure record as `scr_iii_b/SCR_IV_CLOSURE_FREEZE_v001.md` alongside the existing artifacts.
3. Future corrections or extensions must be separately named, dated, hashed, and explicitly linked as **addenda**.
4. Keep GitHub unchanged until a separate local-first publication decision.
5. Close SCR-IV at the exact verdict recorded above. Further held-out tests, scalability studies, benchmarking, or manuscript work are distinct projects or phases.

**Closure decision:** `SCR_IV_COMPLETE / FINITE_GAP_CERTIFIED / PREDICTIONS_PROVEN`.
