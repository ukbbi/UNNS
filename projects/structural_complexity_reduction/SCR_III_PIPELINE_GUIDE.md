# SCR_III_PIPELINE_GUIDE

**Project:** Structural Complexity Reduction (SCR)  
**Scope:** General reproduction guide for `scr_iii`  
**Status:** Reproduction guide — does not modify or supersede frozen specifications, preregistrations, results, or freeze records  
**Current completed lineage:** SCR-III-A v001 → closed pre-primary; SCR-III-A v002 → `COUPLING_MAP_ONLY`  
**Platform:** Windows-first workflow using the supplied `.bat` runners

---

## 1. Purpose

This guide explains how to reproduce the SCR-III pipeline from a clean local project copy while preserving the frozen experimental logic.

SCR-III is not a single run. It is a staged pipeline:

```text
SPEC / STRUCTURE / PREREG
→ VALIDATE
→ optional ACCEPTANCE PREFLIGHT
→ AUDIT
→ AUDIT FREEZE
→ PRIMARY
→ NULLS
→ ESTIMATORS
→ SUMMARY
→ FINAL RESULT / FREEZE
```

The ordering matters. Later stages are intentionally blocked unless the required earlier freeze/pass records exist.

This guide is operational only. The scientific rules are defined by the frozen specification and preregistration files for each version.

---

## 2. Core reproduction rule

Always reproduce the project **version-by-version**.

Do not mix:

- v001 design files with v002 engine runners;
- v001 audit outputs with v002 primary outputs;
- v001 seeds with v002 seeds;
- stale draft copies with the canonical root specifications.

The canonical design documents are the files at the project root:

```text
SCR_III_COUPLING_SPEC_v001.md
SCR_III_STRUCTURE_v001.md

SCR_III_COUPLING_SPEC_v002.md
SCR_III_STRUCTURE_v002.md
```

The preregistrations are versioned separately under:

```text
scr_iii\
├─ SCR_III_PREREG_v001\
└─ SCR_III_PREREG_v002\
```

---

## 3. Current project layout

A normal completed project should contain approximately:

```text
structural_complexity_reduction\
│
├─ SCR_III_COUPLING_SPEC_v001.md
├─ SCR_III_STRUCTURE_v001.md
├─ SCR_III_COUPLING_SPEC_v002.md
├─ SCR_III_STRUCTURE_v002.md
├─ CTX_SCR_III_B.md
│
├─ RUN_SCR_III_VALIDATE.bat
├─ RUN_SCR_III_AUDIT.bat
├─ RUN_SCR_III_FREEZE_AUDIT.bat
├─ RUN_SCR_III_PRIMARY.bat
├─ RUN_SCR_III_NULLS.bat
├─ RUN_SCR_III_ESTIMATORS.bat
├─ RUN_SCR_III_SUMMARY.bat
│
├─ RUN_SCR_III_V002_VALIDATE.bat
├─ RUN_SCR_III_V002_ACCEPTANCE.bat
├─ RUN_SCR_III_V002_AUDIT.bat
├─ RUN_SCR_III_V002_FREEZE_AUDIT.bat
├─ RUN_SCR_III_V002_PRIMARY.bat
├─ RUN_SCR_III_V002_NULLS.bat
├─ RUN_SCR_III_V002_ESTIMATORS.bat
├─ RUN_SCR_III_V002_SUMMARY.bat
│
└─ scr_iii\
   ├─ compat.py
   ├─ engine_common.py
   ├─ generator\
   ├─ nulls\
   ├─ analysis\
   ├─ scripts\
   ├─ tests\
   ├─ SCR_III_PREREG_v001\
   ├─ SCR_III_PREREG_v002\
   └─ output\
      ├─ audit\
      └─ v002\
         ├─ preflight\
         ├─ audit\
         ├─ primary\
         ├─ nulls\
         ├─ estimators\
         └─ reports\
```

Exact helper-module names may differ slightly by engine package revision, but the versioned runners and frozen output records are the authoritative reproduction landmarks.

---

## 4. Frozen branches and files

The following material is read-only during SCR-III reproduction:

```text
SCR_I_PREREG_v003\
scr_ii\
```

SCR-III imports frozen SCR-II components and verifies their hashes before execution.

Within SCR-III itself, once a version is frozen:

```text
SCR_III_COUPLING_SPEC_v00X.md
SCR_III_STRUCTURE_v00X.md
scr_iii\SCR_III_PREREG_v00X\
frozen audit results
frozen audit-freeze records
completed primary/null/estimator outputs
final analysis and result records
```

must not be edited to obtain a more favorable result.

A changed scientific design requires a new version.

---

## 5. Important stale-file warning

There should be no duplicate noncanonical coupling specification inside the `scr_iii` folder.

For example, the old stale draft:

```text
scr_iii\SCR_III_COUPLING_SPEC_v001.md
```

should not be present.

The canonical v001 specification belongs at the project root:

```text
SCR_III_COUPLING_SPEC_v001.md
```

The same principle applies to future versions: keep canonical specifications at the project root unless a versioned structure explicitly says otherwise.

---

# PART I — SCR-III-A v001

## 6. Historical role of v001

SCR-III-A v001 was the first controlled coupling-gradient implementation.

Its audit closed pre-primary on PG5:

```text
CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED
```

That historical result is frozen.

The failure was later interpreted as an audit-resolution problem: d=10 did not reliably receive the intended dose, while d=12 showed the expected response.

v001 must therefore be reproduced as a **closed pre-primary branch**.

Do not run the v001 primary merely to see what would happen.

---

## 7. v001 runner order

Use:

```text
RUN_SCR_III_VALIDATE.bat
```

Then:

```text
RUN_SCR_III_AUDIT.bat
```

Expected historical outcome:

```text
SCR-III audit CLOSED_PRE_PRIMARY: PG5
```

Because the audit did not pass, do not continue to:

```text
RUN_SCR_III_FREEZE_AUDIT.bat
RUN_SCR_III_PRIMARY.bat
RUN_SCR_III_NULLS.bat
RUN_SCR_III_ESTIMATORS.bat
RUN_SCR_III_SUMMARY.bat
```

for a historical reproduction of the frozen v001 result.

The absence of a valid audit-pass record is intentional and should block primary.

---

## 8. v001 expected validation outputs

Validation writes preflight material under the v001 audit/output area.

The decisive success marker is normally:

```text
PREFLIGHT_PASS_v001.json
```

If only a general preflight report exists and no pass record is produced, inspect the report before continuing.

A correctly installed v001 engine passed its preflight tests and frozen source/design hash checks before the audit.

---

# PART II — SCR-III-A v002

## 9. Scientific role of v002

v002 repairs the audit design without changing the C-MASK construction itself.

Key frozen changes from v001 include:

```text
audit depth: d=14 only
audit families: 30
primary families: 30 per depth
primary depths: 14, 16, 18
q: 0.0, 0.1, 0.2, 0.3, 0.4
sigma: 0.8, 0.9
MAX_ATTEMPTS: 64
n_dose_min: 6
n_acc_min: 21
PG5: realized-C trend
DOSE_NOT_RESOLVED: closing verdict
```

v002 completed with final study verdict:

```text
COUPLING_MAP_ONLY
```

---

## 10. v002 full runner order

The canonical v002 reproduction order is:

```text
1. RUN_SCR_III_V002_VALIDATE.bat
2. RUN_SCR_III_V002_ACCEPTANCE.bat
3. RUN_SCR_III_V002_AUDIT.bat
4. RUN_SCR_III_V002_FREEZE_AUDIT.bat
5. RUN_SCR_III_V002_PRIMARY.bat
6. RUN_SCR_III_V002_NULLS.bat
7. RUN_SCR_III_V002_ESTIMATORS.bat
8. RUN_SCR_III_V002_SUMMARY.bat
```

Do not skip stages.

---

# STAGE A — VALIDATE

## 11. Run validation

From the project root, run:

```text
RUN_SCR_III_V002_VALIDATE.bat
```

Validation checks the installed engine against the frozen v002 design.

It should verify at least:

- canonical design hashes;
- frozen SCR-II source hashes;
- immutable SCR-III v001 implementation hashes reused by v002;
- seed uniqueness / separation;
- schema/config consistency;
- deterministic construction;
- firewall / stream-separation assumptions;
- v002-specific unit tests.

The runner should pause at the end so the result remains visible.

Expected terminal status:

```text
PASS
Exit code: 0
```

Do not proceed if validation fails.

---

## 12. Validation outputs

The v002 validation/preflight output is stored under:

```text
scr_iii\output\v002\preflight\
```

Important records include:

```text
ENGINE_PREFLIGHT_v002.json
ENGINE_PREFLIGHT_PASS_v002.json
```

The pass file is the operational authorization to continue to the acceptance-only preflight.

---

# STAGE B — ACCEPTANCE-ONLY PREFLIGHT

## 13. Purpose

Run:

```text
RUN_SCR_III_V002_ACCEPTANCE.bat
```

This stage remeasures common-attempt acceptance using the **real installed engine** and dedicated burned preflight seeds.

It is deliberately restricted.

It may inspect:

- accepted vs infeasible family;
- accepted attempt index;
- attempts examined;
- baseline multiplicity;
- free-subspace density;
- deterministic provenance.

It must not use:

- SCR recall;
- EI;
- exact preservation;
- target survival under the filter;
- H1 / PG5 statistics.

This stage has **no tuning authority**.

---

## 14. Expected acceptance-preflight result

The completed reference run produced:

```text
d=14: 19/30 accepted
d=16: 22/30 accepted
d=18: 22/30 accepted
```

All depths cleared the common-attempt acceptance floor of 0.5.

d=14 raised:

```text
STRICT_VALIDITY_POWER_RISK
```

because 19/30 is below the strict condition-validity planning count of 21, but this is diagnostic only.

Do not change:

```text
MAX_ATTEMPTS
q
sigma
density band
M_min
seed counts
```

in response to this stage.

---

## 15. Acceptance-preflight output

Expected file:

```text
scr_iii\output\v002\preflight\ACCEPTANCE_PREFLIGHT_v002.json
```

The preflight seeds are burned after use and must never be reused in audit or primary.

---

# STAGE C — AUDIT

## 16. Run audit

After validation and acceptance preflight complete, run:

```text
RUN_SCR_III_V002_AUDIT.bat
```

The v002 audit uses:

```text
depth = 14
families = 30
sigma = 0.8, 0.9
q = 0.0 ... 0.4
```

The key v002 distinction is that dose response is tested against **realized coverage C**, not nominal q.

---

## 17. Dose-delivered rule

For accepted family `i`:

```text
DOSE_DELIVERED iff max_q C_i(q) > 0
```

This classification is structure + mask only.

It does not use recall or preservation outcomes.

Both d=14 sigma panels must contain at least:

```text
n_dose_min = 6
```

dose-delivered accepted families.

Otherwise the audit closes:

```text
CLOSED_PRE_PRIMARY — DOSE_NOT_RESOLVED
```

If dose is resolved but the realized-C trend fails:

```text
CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED
```

---

## 18. Expected reference audit result

The completed v002 audit passed.

Reference outcome:

```text
SCR-III v002 audit: PASS
Exit code: 0
```

Reference common-attempt acceptance:

```text
22/30 accepted at d=14
```

Both sigma panels were informative and both PG5 realized-C tests passed.

---

## 19. Audit outputs

Located under:

```text
scr_iii\output\v002\audit\
```

Important files include:

```text
AUDIT_RESULT_v002.json
```

and, after freezing:

```text
AUDIT_FREEZE_v002.json
```

There may also be pass / checkpoint / provenance files depending on the engine package.

---

# STAGE D — FREEZE AUDIT

## 20. Freeze only a passing audit

Run:

```text
RUN_SCR_III_V002_FREEZE_AUDIT.bat
```

Expected reference terminal form:

```text
SCR-III v002 audit frozen: <SHA-256>
Exit code: 0
```

The freeze record binds primary execution to the exact passing audit and design hashes.

Do not edit any audited design file after this point.

Primary should refuse to run if the audit freeze is missing or invalid.

---

# STAGE E — PRIMARY

## 21. Run primary

After the passing audit is frozen:

```text
RUN_SCR_III_V002_PRIMARY.bat
```

Primary depths:

```text
14
16
18
```

Thirty seed families are assigned per depth.

Each accepted family produces:

```text
2 sigma × 5 q = 10 main cells
```

Infeasible families are logged and never replaced.

---

## 22. Expected reference primary accounting

Reference accepted families:

```text
d=14: 24/30
d=16: 21/30
d=18: 21/30
```

Therefore:

```text
accepted families total = 66
generated main cells = 66 × 10 = 660
planned main cells = 900
```

Reference primary cell verdict counts:

```text
PRESERVATION_FAIL: 448
NO_MATERIAL_REDUCTION: 152
REDUCTION_WITHOUT_NET_GAIN: 60
VALID_STRUCTURAL_REDUCTION: 0
```

These are expected historical results, not pass/fail targets to tune toward.

---

## 23. Primary outputs

Located under:

```text
scr_iii\output\v002\primary\
```

Typical important files:

```text
PRIMARY_RESULT_v002.json
PRIMARY_COMPLETE_v002.json
PRIMARY_CHECKPOINT_v002.json
```

plus per-cell instance/result and solution-loss-ledger files.

No `reports` directory is expected yet.

That directory is created only during the final summary stage.

---

# STAGE F — NULLS / CONTROLS

## 24. Run nulls

After primary completes:

```text
RUN_SCR_III_V002_NULLS.bat
```

Reference workload:

```text
660 primary cells
```

including the preregistered N1 matched-random replicates and the other frozen controls.

The terminal periodically prints progress:

```text
v002 nulls 25 / 660
...
v002 nulls 650 / 660
```

Reference completion:

```text
v002 NULLS COMPLETE H5=True
Exit code: 0
```

---

## 25. Reference null/control findings

Reference values include:

```text
C1_pass = true
Z0_pass = true
H5_pass = true
N1 mean EI ≈ 0
N4 median EI < 0
```

The completed reference run had an N1 mean EI effectively centered on zero and a negative N4 median EI, as required.

---

## 26. Null output

Located under:

```text
scr_iii\output\v002\nulls\
```

Primary result file:

```text
NULL_RESULT_v002.json
```

Do not alter controls after observing their result.

---

# STAGE G — APPLICABILITY ESTIMATORS

## 27. Run estimators

After nulls complete:

```text
RUN_SCR_III_V002_ESTIMATORS.bat
```

The stage evaluates the two frozen applicability estimators.

### E1

Family/regime calibration estimator.

Frozen pass criteria:

```text
MAE <= 0.10
Spearman >= 0.80
```

### E2

Charged instance-level subtree estimator.

Frozen pass criteria:

```text
MAE <= 0.10
Spearman >= 0.80
```

E2 compute cost is explicitly recorded.

---

## 28. Reference estimator result

Reference E1:

```text
MAE ≈ 0.15661
Spearman ≈ 0.59911
PASS = false
```

Reference E2:

```text
MAE ≈ 0.07372
Spearman ≈ 0.89962
PASS = true
```

Therefore:

```text
H4 = false
```

because H4 requires both estimators to pass.

This is a valid scientific outcome.

Do not retune or rerun E1 to rescue H4.

---

## 29. Estimator output

Located under:

```text
scr_iii\output\v002\estimators\
```

Main file:

```text
ESTIMATOR_RESULT_v002.json
```

---

# STAGE H — SUMMARY / FINAL ANALYSIS

## 30. Run summary

Only after both of these exist:

```text
NULL_RESULT_v002.json
ESTIMATOR_RESULT_v002.json
```

run:

```text
RUN_SCR_III_V002_SUMMARY.bat
```

This stage creates:

```text
scr_iii\output\v002\reports\
```

Reference terminal result:

```text
SCR-III-A v002 SUMMARY: COUPLING_MAP_ONLY
Exit code: 0
```

---

## 31. Final report files

The completed v002 reports folder contains:

```text
FINAL_ANALYSIS_v002.json
SUMMARY_v002.md
SCR_III_A_RESULT_v002.md
SCR_III_A_FREEZE_v002.json
```

The first two are produced by the pipeline summary.

The last two are the final scientific result/freeze records added after the completed pipeline.

---

## 32. Final reference scientific outcome

The frozen result is:

```text
study verdict: COUPLING_MAP_ONLY
H1: PASS
H3a: PASS
H3b: PASS
H4: FAIL
H5: PASS
TRANSFER_CONFIRMED: false
COUPLING_LAW_CANDIDATE: false
```

All six realized-C primary panels were informative and passed the preregistered dose-response test.

No condition reached:

```text
VALID_STRUCTURAL_REDUCTION
```

and no condition reached:

```text
HIGH_RELIABILITY_REDUCTION
```

The strongest preserved condition improved exact retention substantially but still did not satisfy exact equivalence and did not produce net end-to-end computational gain.

---

# REPRODUCTION INTERPRETATION

## 33. Reproducing numbers versus reproducing logic

A successful reproduction has two levels.

### Level 1 — pipeline reproduction

Required:

- validation passes;
- source/design hashes match;
- frozen seeds are loaded correctly;
- stage ordering is enforced;
- audit gating works;
- audit freeze gates primary;
- primary/null/estimator/summary outputs are produced;
- final result is derived by the frozen code.

### Level 2 — numerical reproduction

If using the exact frozen code, exact seed files, same Python/runtime dependencies, and deterministic implementations, the numerical results should match the frozen records.

Timing fields may vary across machines.

Do not treat wall-clock differences alone as reproduction failure.

---

## 34. What may legitimately differ across machines

The following may vary:

```text
wall time
CPU utilization
console refresh timing
filesystem timestamps
```

The following should not vary under a correct deterministic reproduction:

```text
seed identities
accepted/infeasible family identities
accepted attempt indices
instance hashes
solution sets
recall / EI
realized C
gate outcomes
hypothesis pass/fail
study verdict
```

If these scientific outputs differ, stop and inspect provenance before continuing.

---

# LONG-RUN NOTES

## 35. Why d=18 is slow

The route space scales as:

```text
N = 2^d
```

so:

```text
d=14 → 16,384
d=16 → 65,536
d=18 → 262,144
```

d=18 therefore has:

```text
4×
```

the route space of d=16 and:

```text
16×
```

the route space of d=14.

Some families also use many common-attempt trials before acceptance or infeasibility.

Therefore d=18 can take substantially longer than d=16.

This is expected.

---

## 36. When not to stop a long run

If the console continues to print progress or `python.exe` is consuming CPU, let the run continue.

Do not stop merely because d=18 appears much slower.

A family that ultimately becomes:

```text
INFEASIBLE_FAMILY
```

may consume the full frozen attempt budget.

---

## 37. When to investigate a possible stall

Investigate if:

- there is no console progress for an unusually long period;
- CPU usage remains near zero;
- the same family/step never completes;
- no checkpoint/output timestamp changes;
- Python has exited but the batch wrapper is still waiting unexpectedly.

Before terminating, preserve:

```text
terminal screenshot
current checkpoint file
last output timestamp
Task Manager CPU state
```

---

# ERROR / STOP RULES

## 38. If VALIDATE fails

Stop immediately.

Do not continue to acceptance, audit, or primary.

Check:

```text
source hashes
design hashes
seed separation
schema/config
installed engine version
duplicate/stale files
Python environment
```

---

## 39. If ACCEPTANCE PREFLIGHT looks weak

Do not tune anything.

The v002 acceptance preflight is diagnostic.

Record the flags exactly as produced.

The real audit and primary accepted-family counts determine later underpowered/infeasible statuses.

---

## 40. If AUDIT closes

Stop that version.

Do not:

- run primary anyway;
- edit thresholds;
- add q levels;
- add sigma levels;
- replace audit seeds;
- rerun after changing the engine.

A scientific repair requires a new version.

This is exactly what happened from v001 to v002.

---

## 41. If PRIMARY contains infeasible families

This is expected.

Do not replace them.

The preregistration explicitly treats family infeasibility as part of the benchmark.

---

## 42. If H4 fails

Do not reinterpret the failure as an engine error unless the estimator stage itself reports an implementation failure.

In v002:

```text
E1 failed
E2 passed
H4 failed
```

That is the frozen scientific result.

---

# STATUS DICTIONARY

## 43. Important statuses

```text
PASS
```

Stage completed its frozen gate.

```text
INVALID_RUN
```

Implementation/provenance problem. Scientific interpretation is not valid.

```text
INFEASIBLE_FAMILY
```

No common accepted attempt was found within the frozen attempt cap.

```text
CLOSED_PRE_PRIMARY — DOSE_NOT_RESOLVED
```

The intended coupling manipulation was not sufficiently delivered.

```text
CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED
```

Dose was delivered but the frozen coupling-response gate failed.

```text
PRESERVATION_FAIL
```

SCR target differs from baseline target.

```text
NO_MATERIAL_REDUCTION
```

Preservation may pass at cell level, but reduction is below the frozen minimum.

```text
REDUCTION_WITHOUT_NET_GAIN
```

Preservation/reduction conditions are insufficient to yield the frozen net-gain threshold.

```text
VALID_STRUCTURAL_REDUCTION
```

Strict preservation + material reduction + net gain.

```text
TRANSFER_CONFIRMED
```

The same frozen valid-reduction mechanism transfers across the preregistered scales.

```text
COUPLING_LAW_CANDIDATE
```

The full frozen coupling-law criteria pass.

```text
COUPLING_MAP_ONLY
```

The controlled coupling map is scientifically valid, but the stronger law/transfer criteria do not all pass.

---

# FINAL FREEZE

## 44. Completed v002 final-freeze files

After `SUMMARY_v002.md` and `FINAL_ANALYSIS_v002.json` were produced, SCR-III-A v002 was formally closed with:

```text
SCR_III_A_RESULT_v002.md
SCR_III_A_FREEZE_v002.json
```

stored under:

```text
scr_iii\output\v002\reports\
```

The project-root handoff context for the next phase is:

```text
CTX_SCR_III_B.md
```

---

## 45. Do not rerun frozen v002 to improve the result

The final v002 result is:

```text
COUPLING_MAP_ONLY
```

Do not modify or rerun the completed v002 pipeline to seek:

```text
VALID_STRUCTURAL_REDUCTION
TRANSFER_CONFIRMED
COUPLING_LAW_CANDIDATE
```

A new scientific question belongs in a new phase/version.

---

# QUICK REPRODUCTION CHECKLIST

## 46. v002 checklist

Run in this exact order:

```text
[ ] RUN_SCR_III_V002_VALIDATE.bat
[ ] confirm validation PASS

[ ] RUN_SCR_III_V002_ACCEPTANCE.bat
[ ] archive ACCEPTANCE_PREFLIGHT_v002.json

[ ] RUN_SCR_III_V002_AUDIT.bat
[ ] confirm audit PASS

[ ] RUN_SCR_III_V002_FREEZE_AUDIT.bat
[ ] confirm audit freeze hash exists

[ ] RUN_SCR_III_V002_PRIMARY.bat
[ ] confirm PRIMARY_COMPLETE_v002.json

[ ] RUN_SCR_III_V002_NULLS.bat
[ ] confirm NULL_RESULT_v002.json

[ ] RUN_SCR_III_V002_ESTIMATORS.bat
[ ] confirm ESTIMATOR_RESULT_v002.json

[ ] RUN_SCR_III_V002_SUMMARY.bat
[ ] confirm FINAL_ANALYSIS_v002.json
[ ] confirm SUMMARY_v002.md

[ ] retain SCR_III_A_RESULT_v002.md
[ ] retain SCR_III_A_FREEZE_v002.json
```

Reference final verdict:

```text
COUPLING_MAP_ONLY
```

---

## 47. Recommended location of this guide

Place this file at the project root:

```text
structural_complexity_reduction\
└─ SCR_III_PIPELINE_GUIDE.md
```

This keeps the reproduction instructions beside the canonical SCR-III specifications and Windows runners while leaving the frozen `scr_iii` execution/output tree untouched.

---

## 48. Reproduction principle

The governing rule for SCR-III is:

\[
\boxed{
\text{freeze first}
\rightarrow
\text{validate}
\rightarrow
\text{audit}
\rightarrow
\text{freeze audit}
\rightarrow
\text{primary}
\rightarrow
\text{controls}
\rightarrow
\text{estimators}
\rightarrow
\text{final verdict}
}
\]

No downstream computational gain is allowed to override a failed preservation or provenance gate.

That rule is part of the scientific result of the SCR program itself.
