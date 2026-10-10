# CTX_SCR_III_B

**Project:** Structural Complexity Reduction (SCR)  
**Next phase:** SCR-III-B — Physical Transfer  
**Context date:** 2026-10-08  
**Predecessor frozen result:** `SCR_III_A_RESULT_v002.md`  
**SCR-III-A final verdict:** `COUPLING_MAP_ONLY`

## 1. Where the project stands

The SCR program now has three empirical positions.

### SCR-I — aligned structural target

A structurally aligned benchmark demonstrated that strong pruning can coexist with preservation when the target is genuinely aligned with the grammar.

### SCR-II — independent arithmetic target

A deliberately independent target showed the opposite boundary: extreme contraction can destroy the target almost completely. Problem-aligned C1 pruning preserved the target, proving that the failure was not caused by pruning in general.

### SCR-III-A v002 — controlled coupling ruler

SCR-III-A constructed a declared shared generative channel and measured its realized coverage C independently of survival.

Final outcome:

```text
study verdict: COUPLING_MAP_ONLY
H1: PASS
H3a: PASS
H3b: PASS
H4: FAIL
H5: PASS
TRANSFER_CONFIRMED: false
COUPLING_LAW_CANDIDATE: false
generated main cells: 660/900
```

All six realized-C primary panels pass the preregistered dose-response test, so delivered coupling reproducibly improves preservation.

No tested condition reaches `VALID_STRUCTURAL_REDUCTION`.

## 2. The scientific transition

SCR-III-A asked:

> Can target preservation be made to respond systematically when grammar and target share a controlled generative cause?

Answer: **yes**.

SCR-III-B must now ask the harder question:

> Does comparable grammar–target alignment exist naturally in a real physical system when the grammar is frozen without access to the target?

This is a transfer experiment, not another synthetic coupling sweep.

## 3. Three objects must remain independent

SCR-III-B must keep separate:

\[
G = \text{frozen physical structural grammar},
\]

\[
T = \text{independently solved or measured target},
\]

\[
P(G,T) = \text{preregistered preservation relation}.
\]

The grammar must be defined from generative/local structural information without using target membership or target outcomes.

The target must come from an independent exact solver, trusted physical computation, or measurement protocol.

The preservation tolerance must be frozen before primary execution.

## 4. Estimator doctrine carried forward

### E1

SCR-III-A result:

```text
MAE = 0.156610
Spearman = 0.599110
PASS = false
```

E1 is **not** the deployment estimator for SCR-III-B. Retain it only as a negative/secondary baseline if useful.

### E2

SCR-III-A result:

```text
MAE = 0.073719
Spearman = 0.899616
PASS = true
median estimator-cost / baseline-time = 0.408569
```

E2 is the preferred applicability estimator for SCR-III-B because it predicts the held-out instance using a charged local sample rather than assuming family-level transfer.

Its cost must be included explicitly. E2 passing predictive thresholds does not by itself imply net computational gain.

## 5. Physical benchmark requirements

The first SCR-III-B benchmark should satisfy all of the following:

1. **Finite or controllably finite ground truth.** Exact or high-confidence independent target evaluation must be feasible on the preregistered primary set.
2. **Nontrivial structure.** The grammar must reject some states/routes; a grammar that admits everything is not informative.
3. **Independent grammar construction.** Grammar rules must be frozen from local/generative physics without using the target labels.
4. **Independent target.** The target must not simply restate the grammar constraint.
5. **Problem-aligned control.** A C1-like conventional pruner/control should exist where possible.
6. **Preservation first.** No contraction or speedup claim counts if the target relation fails.
7. **Charged applicability estimation.** E2 sampling cost must be recorded separately and included in end-to-end gain claims.
8. **Null structure.** At minimum include a rate-matched random control and a physically meaningful structural null/permutation where possible.
9. **Frozen scale progression.** Audit and primary scales/instances must be separated before outcome inspection.
10. **No complexity-class language.** The physical experiment tests transfer, not asymptotic complexity classes.

## 6. Tautology guard

A physical law/constraint may be used to construct the grammar, but the target may not simply ask whether that same law/constraint holds.

Example: if a spin-ice local ice rule contributes to G, then “is this an ice-rule state?” is not an acceptable target T.

Safer independent targets include, depending on the chosen system:

- exact low-energy sector not identical to the grammar rule;
- correlation structure;
- independently solved transition pathway;
- spectral/response class;
- propagation or relaxation outcome;
- observable ordering obtained from an independent solver.

This guard is mandatory for SCR-III-B.

## 7. Relationship to the SCR-III-A map

The synthetic coverage C is ground truth available only in SCR-III-A.

A real physical benchmark will generally not provide a knob called C.

SCR-III-B therefore must not manufacture an artificial C after seeing the target.

Instead:

1. freeze G;
2. define T independently;
3. use a small preregistered calibration/audit subset where necessary;
4. apply E2 to estimate applicability on held-out instances;
5. measure actual preservation and reduction on the independently solved held-out primary set;
6. compare the physical outcomes to the qualitative regions learned in SCR-III-A.

Any “effective coupling” quantity introduced for the physical benchmark must have an operational definition frozen before primary results.

## 8. Preservation doctrine

For an exact discrete target:

\[
S_T^{SCR} = S_T^{baseline}.
\]

For a continuous physical observable:

\[
|O_{SCR} - O_{baseline}| \le \epsilon,
\]

with \(\epsilon\) justified and frozen before primary execution.

The decision hierarchy remains:

```text
INVALID_RUN
→ PRESERVATION_FAIL
→ NO_MATERIAL_REDUCTION
→ REDUCTION_WITHOUT_NET_GAIN
→ VALID_STRUCTURAL_REDUCTION
→ TRANSFER_CONFIRMED
```

`COUPLING_LAW_CANDIDATE` from the synthetic ruler is not automatically transferable to a physical system.

## 9. UPI

UPI/H-UPI remains outside the primary pruning rule.

If used in SCR-III-B, it should enter only as a **blinded secondary explanatory diagnostic** after grammar and target protocols are frozen. It may test whether rejection/admissibility correlates with structural-risk bands, but it must not define the primary target or retroactively tune G.

## 10. Benchmark-selection direction

Do not choose the first physical benchmark merely because it is easy to make tautologically aligned.

A strong first candidate should allow:

- exact finite enumeration or an independently trusted solver;
- a local physical/generative grammar;
- a target observable not identical to that grammar;
- enough instances/scales for audit/holdout separation;
- a conventional problem-aligned control.

Frustrated-lattice / spin-ice style systems remain plausible **only if the target is independent of the local rule** (for example correlation structure or transition/low-energy behavior rather than ice-rule membership itself).

No benchmark is frozen by this context file.

## 11. Files that must remain frozen

Do not modify:

```text
SCR_III_COUPLING_SPEC_v001.md
SCR_III_STRUCTURE_v001.md
scr_iii/SCR_III_PREREG_v001/
all v001 preflight/audit outputs

SCR_III_COUPLING_SPEC_v002.md
SCR_III_STRUCTURE_v002.md
scr_iii/SCR_III_PREREG_v002/
all v002 preflight/audit/primary/null/estimator/report outputs
SCR_III_A_RESULT_v002.md
SCR_III_A_FREEZE_v002.json
```

SCR-III-B must be a new branch/version with new seeds/instances.

## 12. Immediate next work

The next task is **benchmark selection**, not engine modification.

For each candidate physical system, answer:

```text
1. What is G?
2. What information is forbidden when freezing G?
3. What is T?
4. How is T solved/measured independently?
5. What is the preservation relation?
6. What is the C1 problem-aligned control?
7. What does E2 sample?
8. What is its charged cost?
9. What is the audit/primary separation?
10. What result would falsify physical transfer?
```

After one benchmark is selected, create:

```text
SCR_III_B_SPEC_v001.md
SCR_III_B_PREREG_v001.md
```

and only then build a physical adapter/engine.

## 13. Material to carry into the next conversation

Minimum required:

```text
CTX_SCR_III_B.md
SCR_III_A_RESULT_v002.md
SCR_III_A_FREEZE_v002.json
FINAL_ANALYSIS_v002.json
SUMMARY_v002.md
```

For implementation work also include or keep locally available:

```text
SCR_III_COUPLING_SPEC_v002.md
SCR_III_STRUCTURE_v002.md
scr_iii/SCR_III_PREREG_v002/
SCR_III_ENGINE_v002 package/source
ESTIMATOR_RESULT_v002.json
NULL_RESULT_v002.json
```

The frozen scientific position is:

\[
\boxed{
\text{controlled coupling affects preservation reproducibly,}
\quad
\text{but physical transfer remains untested.}
}
\]
