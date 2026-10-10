# GAP4_EXACT_ADDENDUM_v001 — SCR-IV exact-arithmetic addendum to SCR-III-GAP-4X4

**Record date:** 2026-10-10 · **Status:** additive; supersedes nothing. `GAP4_RESULT_FREEZE_v001.md` (sha256 `9771ab659c38c098afcbab9a54351c6669564b0377a8be5893db0f3f080b77c3`) and everything it freezes remain unchanged and remain the record of what the original numerical experiment produced.

## 1. Linked records
| Record | sha256 |
|---|---|
| `scr_iii_b/GAP4_RESULT_FREEZE_v001.md` | `9771ab65…77c3` (full value above) |
| `GAP4_v010/PREDICTION_FREEZE_v001.md` (δ₄ definition, ranges) | `7d8e8ac5f12903c0712643afc4a3668211ee81357a3a554dc6082c3afbdb5947` |
| `GAP4_v010/output/real_4x4.txt` (instance) | `3d47ed1256da7620292a5fe4c64e0bc226b9836768ac87df0ff4fdbf91c5f7a2` |
| `GAP4_v010/physical_energy_v005.py` (k_B, A(T)) | `3364d5524d9f7f020cb35a9cb3dc8136ef056b8f00ada1e229e60021378ad8ac` |
| `SCR_IV_LEAN_v004.zip` (IV-4B certificates and batch theorems) | `fc2197ff5ef947736d75f23ae28291675cf3ffb940a1094bb8e4b2f26e4fa262` |
| `SCR_IV_LEAN_v005.zip` (IV-5; see its MANIFEST) | recorded in the delivery message and in `MANIFEST_SCR_IV_v005.json` of the package |
Toolchain: Lean 4.34.1 (commit 5045d0056413), core only, kernel checks; axioms limited to propext, Classical.choice, Quot.sound.

## 2. What is established (exact encoded model: 780 binary64 couplings read as exact dyadic rationals over 2^70; A(792 K) = the frozen binary64 1.0095767595046513e-18 J as an exact dyadic; k_B = 1.380649e-23 J/K exact)
| Quantity | SCR-III frozen record | SCR-IV exact |
|---|---|---|
| Ground minimum E₀ (all 2^40 configurations) | −0.16364841082886986 A, id 711243241830 | **−193201942568284180326 / 2^70 A**, same witness (`ground_exact_min`) |
| Non-grammar minimum | −0.1534031680911189 A, id 161487427942 | **−181106494839879485536 / 2^70 A**, id **711243241766** (ground witness with spin 6 flipped; vertex 3 has 3 inward arms) (`nongT_exact_min`) |
| Frozen non-grammar value as exact rational | — | −181106494839879484608 / 2^70; **not** the minimum (`frozen_nonG_not_min`); lies above the true minimum by 928/2^70 A ≈ 7.86e-19 A |
| Exclusion gap Δ | 0.01024524273775096 A | **12095447728404694790 / 2^70 A** > 0 (frozen-value numerator: 12095447728404695718). Both round to 0.010245242737750961 A in binary64; Lean: \|Δ − 0.01024524273775096\| < 2e-17 A |
| δ₄ = Δ/(k_B·792 K) | 0.9459172223430824 | exact fraction `delta4Num/delta4Den` (SCR_IV_V5.lean); ≈ 0.94591722234308(26); Lean: \|δ₄ − 0.9459172223430824\| < 3e-16 |
| δ₄ < 1 | confirmed | **proved** (1 − δ₄ > 0.054) |
| 0.790439676056526 ≤ δ₄ ≤ 1.0333534753990623 | confirmed | **proved** (margin to the upper endpoint > 0.0874, to the lower > 0.155) |

The original excluded-state value is valid at the solver's reported numerical resolution (the audit's 1e-11 pruning guard is ≈ 10^7 times the 7.9e-19 A difference), but it is not the exact minimum of the encoded model. Neither verdict (R2 `GAP_CONSISTENT`, directional `DELTA4_LT_1_CONFIRMED`) changes: the frozen value gives the same two exact verdicts (`frozen_value_same_verdicts`), and the correction moves δ₄ by less than 1e-15 (`correction_effect_on_delta4`). The reported δ₄ digits …824 versus the exact …826 differ by floating-point evaluation of the original expression, not by the 928/2^70 correction (the frozen numerator gives the same double 0.9459172223430826).
Why the original solver kept the higher state has not been established from its execution trace; the recorded guard size is consistent with it.

## 3. Lean theorem identifiers
`ground_exact_min`, `nongT_exact_min`, `frozen_nonG_not_min`, `nonGT_min_of_frontier` (v004); `gap_exact`, `gap_pos`, `pred_lt1_true`, `pred_r2_true`, `margin_*`, `gap_matches_reported_Delta`, `delta4_matches_reported`, `frozen_value_same_verdicts`, `correction_effect_on_delta4`, `iv5_of_minima`, and the unconditional `iv5_final` (v005; `iv5_final` imports the accepted IV-4B theorems and does not re-run the 1,148 batches).

## 4. Limits (unchanged by this addendum)
1. Exact statements about the encoded dyadic model only. The binary64 pruning of the original solver is not formalised; the SCR-III audit's numerical argument for it is not replaced.
2. A(792 K) is taken as the frozen binary64 value returned by the v005 module; its derivation from the physical parameters is not re-done in Lean. The prediction range endpoints are the frozen decimal literals read as exact rationals.
3. Minimum values are certified, not the sets of minimisers; nothing is claimed about uniqueness or degeneracy of the ground or the first excluded energy (the first excluded level is the corrected state's energy; its degeneracy was not computed).
4. Grammar convention agrees with the geometric ice rule by differential testing (`scripts/diff_test.py`), not by proof.
5. The recorded Lean executions were run in Claude's cloud container, not yet independently in the author's WSL (`FULL=1 bash RUN_TEST.sh` re-runs everything, ≈1.5 h).
6. This is a model-conditional finite-size result, as in the original freeze. It authorizes no new physical runs and makes no claim of a UNNS-specific computational advantage.
