# SCR_IV_CLOSURE_v001: closure record for SCR-IV

**Record prepared:** 2026-10-11 · **Closure effective:** 2026-10-10 (date of the reported Lean certification)
**Status:** additive. It modifies no earlier record. **Scope: closes SCR-IV only. SCR-III is not closed by this record** (see section 6).

**Verdict:** `SCR_IV_COMPLETE / FINITE_GAP_CERTIFIED / PREDICTIONS_PROVEN`, for the exact encoded model of the frozen 4×4 instance, in the recorded Lean execution.

## 1. Frozen artifacts
| Artifact | Status | sha256 |
|---|---|---|
| `SCR_IV_LEAN_v005.zip` | Frozen | `b8dcd220ff7beb1e8e209627a88820107510aef0dd45d62fcfa30320db0740fd` |
| `GAP4_EXACT_ADDENDUM_v001.md` | Frozen | `b6471c06804448be4eafecb78d424a5f7649bbdc38093eda8ddf3d1e45c0440d` |
| `SCR_IV_LEAN_v004.zip` | Preserved unchanged | `fc2197ff5ef947736d75f23ae28291675cf3ffb940a1094bb8e4b2f26e4fa262` |
| `SCR_IV_LEAN_v001–v003.zip` | Preserved unchanged | see `MANIFEST.md` / package manifests |
| `GAP4_RESULT_FREEZE_v001.md` | Original numerical freeze, preserved | `9771ab659c38c098afcbab9a54351c6669564b0377a8be5893db0f3f080b77c3` |

## 2. Three evidence layers (keep them separate in every downstream text)
| Layer | What it establishes | Description to use |
|---|---|---|
| SCR-III numerical investigation | 3×3 structural contraction; primary-window physical-sufficiency failure; frozen 4×4 numerical results | Audited numerical and experimental evidence. Not Lean-certified. |
| SCR-IV Lean certification | Exact 4×4 encoded-model minima, exclusion gap, corrected witness, prediction inequalities | Machine-checked mathematical results, recorded execution |
| Scientific interpretation | What the findings suggest about generative admissibility within UNNS | Interpretation, distinguished from theorems |

## 3. Certified results (exact encoded model; Lean 4.34.1; axioms limited to propext, Classical.choice, Quot.sound)
* `ground_exact_min`: E₀ = −193201942568284180326/2⁷⁰ A (confirms the frozen ground value and witness 711243241830).
* `nongT_exact_min`, `frozen_nonG_not_min`: the exact non-grammar minimum is −181106494839879485536/2⁷⁰ A at id 711243241766; the frozen non-grammar value is 928/2⁷⁰ A (≈ 7.86e-19 A) above it and is not the exact minimum. It remains valid at the originally reported numerical resolution.
* `gap_pos`, `gap_exact`: Δ = 12095447728404694790/2⁷⁰ A > 0.
* `pred_lt1_true`, `pred_r2_true`, `iv5_final`: δ₄ < 1 and 0.790439676056526 ≤ δ₄ ≤ 1.0333534753990623. Both verdicts are unchanged by the correction.

## 4. Interpretation of the δ₄ < 1 result (two-sided)
The confirmed prediction δ₄ < 1 (1 − δ₄ > 0.054) confirms the predicted finite exclusion-gap behavior. It also shows that, for this model, the ice-rule grammar cannot preserve every state inside the registered 1 k_BT window: exact physical target preservation fails. Both readings are recorded; neither is to be omitted.

## 5. Evidence statements and wording rules
* The Hamiltonian is the **frozen model Hamiltonian** derived from the common v005 source. Do not describe it as independently specified or of independent provenance. Grammar membership and energy minimization are distinct calculations, not independent provenance.
* The 928/2⁷⁰ A discrepancy is described as "not distinguishable at the original solver's resolution" (recorded guard 1e-11 A). The causal explanation has not been established from the solver's execution trace.
* "Prospective" is stated together with the deviation record (`GAP4_DEVIATION_v001.md`): the planned feasibility campaign was not completed prospectively, the certification audit followed the run, and an earlier exploratory verdict was `GAP_INCONCLUSIVE`. The prediction itself was frozen before the real 4×4 evaluation.
* The correction changes an exact value and the identity of the minimiser; it changes no verdict and moves δ₄ by less than 1e-15.
* No claim that proof-carrying optimization originated with UNNS; no claim of a UNNS-specific computational advantage; no claim that UNNS is a universal substrate. Those are hypotheses.

## 6. Limits and archival facts
1. **Independent re-verification waived (archival fact, by decision of the author).** The Lean runs recorded in the v004/v005 packages were executed in Claude's cloud container. Re-running `FULL=1 bash RUN_TEST.sh` in the author's WSL (≈ 1.5 h) was deliberately waived and is not a closure condition. Anyone may run it later; a successful run would add a re-verification note and would not alter this record.
2. Exact-arithmetic statements about the encoded dyadic model only. The original solver's binary64 pruning is not formalised; the SCR-III numerical audit is not replaced.
3. A(792 K) is the frozen binary64 value of `physical_energy_v005.A_joule(792.0)`, taken exactly; its physical derivation is not formalised. Range endpoints are the frozen decimal literals read as exact rationals.
4. Minimum values are certified, not minimiser sets; uniqueness and degeneracy of the ground state and of the first excluded level are not claimed.
5. Grammar convention versus the geometric ice rule: differential testing, not proof.
6. **SCR-III remains open on:** the held-out discrimination study, the synthetic feasibility campaign, and the six defaults awaiting confirmation in `SCR_III_HELDOUT_FREEZE_v001.md` (T1/T2 mapping, B=1 SE, patch handling, prefix sub-instances, threading, execution host). Closing SCR-IV does not close these.
7. The 3×3 figures (2,604 of 16,777,216 retained; 16 of 26 target states excluded) are SCR-III results; they are not Lean-certified and were not re-checked here.

## 7. Suggested manuscript paragraph
**Principal result.** We evaluate a generative structural-admissibility grammar against a frozen model Hamiltonian for a 40-spin square-ice system, in three evidence layers. Audited numerical work (SCR-III) shows strong combinatorial contraction in the 3×3 case and a preregistered failure of physical sufficiency at the primary energy window. Machine-checked mathematics (SCR-IV, Lean 4) then certifies, for the exact encoded 4×4 Hamiltonian, the global ground energy, the exact minimum over grammar-excluded configurations, and a strictly positive exclusion gap Δ = 12095447728404694790/2⁷⁰ A, and proves that the normalized gap satisfies two prospectively frozen predictions (δ₄ < 1 and δ₄ within the frozen interval). The certification also corrects the identity and value of the excluded-state minimum by 928/2⁷⁰ A, a difference not resolvable at the original solver's declared precision, without changing any verdict. The result δ₄ < 1 confirms the predicted finite gap and simultaneously shows that the grammar does not preserve every state within the 1 k_BT window. These are finite-model results; they do not establish that structural contraction implies physical completeness, a computational advantage, or a universal organizing principle.
