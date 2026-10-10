# SCR_III_STRUCTURE_v002

**Project:** Structural Complexity Reduction  
**Phase:** SCR-III-A v002 — Coupling Threshold and Valid Reduction  
**Status:** `FROZEN_STRUCTURE`  
**Frozen:** 2026-10-08  
**Scientific basis:** `SCR_III_COUPLING_SPEC_v002` (`RATIFIED_SPEC`)

## 1. Relationship to v001

SCR-III-A v001 remains frozen at:

```text
CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED
```

No v001 audit cell is rerun or re-gated. Its audit seeds are spent. Its unrun primary seeds remain reserved and excluded from v002.

v002 is a **new preregistered audit-design repair**, not a rescue of v001.

The repair is limited to:

1. PG5 uses realized coverage C rather than nominal q.
2. A structure-only dose-delivery/informativeness gate precedes PG5.
3. Audit depth becomes d=14 only.
4. Audit and primary use 30 families.
5. Strict condition validity uses accepted families with `n_acc_min=21`.
6. Fresh preflight/audit/primary seed blocks are used.

C-MASK itself is unchanged.

## 2. Canonical files

Project-root canonical documents:

```text
SCR_III_COUPLING_SPEC_v001.md      # frozen v001
SCR_III_STRUCTURE_v001.md          # frozen v001
SCR_III_COUPLING_SPEC_v002.md      # ratified v002
SCR_III_STRUCTURE_v002.md          # this file
```

The old non-root file:

```text
scr_iii\SCR_III_COUPLING_SPEC_v001.md
```

is stale and must be deleted locally. It is not part of any v002 hash set.

## 3. Frozen branch discipline

Read-only:

```text
SCR_I_PREREG_v003/
scr_ii/
scr_iii/SCR_III_PREREG_v001/
scr_iii/output/audit/AUDIT_RESULT_v001.json
all v001 preflight/audit freeze records
```

v002 does not overwrite v001 engine scripts or outputs. New executable code is versioned additively.

## 4. v002 layout

```text
structural_complexity_reduction/
│
├─ SCR_III_COUPLING_SPEC_v002.md
├─ SCR_III_STRUCTURE_v002.md
│
└─ scr_iii/
   ├─ compat.py                         # immutable v001 implementation
   ├─ engine_common.py                  # immutable v001 implementation
   ├─ generator/
   │  └─ route_csp_c_v001.py            # unchanged C-MASK generator
   ├─ nulls/
   │  └─ controls_v001.py               # unchanged
   ├─ analysis/
   │  ├─ metrics_v001.py                # unchanged
   │  ├─ estimators_v001.py             # unchanged
   │  ├─ structure_stats_v001.py        # unchanged
   │  └─ trend_test_v002.py             # new realized-C trend
   ├─ scripts/
   │  ├─ validate_engine_v002.py
   │  ├─ run_acceptance_preflight_v002.py
   │  ├─ run_audit_v002.py
   │  ├─ freeze_audit_v002.py
   │  ├─ run_primary_v002.py
   │  └─ summarize_primary_v002.py
   ├─ SCR_III_PREREG_v002/
   │  ├─ SCR_III_PREREG_v002.md
   │  ├─ SEEDS_v002.json
   │  ├─ SOURCE_LOCK_v002.md
   │  ├─ config/
   │  │  └─ prereg_v002.json
   │  ├─ schema/
   │  │  └─ result_v002.schema.json
   │  └─ SHA256SUMS.txt
   └─ output/
      └─ v002/
         ├─ preflight/
         ├─ audit/
         ├─ primary/
         ├─ nulls/
         ├─ estimators/
         └─ reports/
```

Windows runners for v002 must be named distinctly, e.g.:

```text
RUN_SCR_III_V002_VALIDATE.bat
RUN_SCR_III_V002_ACCEPTANCE.bat
RUN_SCR_III_V002_AUDIT.bat
RUN_SCR_III_V002_FREEZE_AUDIT.bat
RUN_SCR_III_V002_PRIMARY.bat
```

## 5. Acceptance-only preflight

Before the audit, v002 remeasures common-attempt acceptance using the real installed engine on dedicated seeds at d=14/16/18.

It may inspect only:

- accepted/infeasible family status;
- accepted attempt index;
- attempts examined;
- baseline solution multiplicity m;
- free-subspace density;
- deterministic provenance.

It must not call the SCR solver, compute recall/EI, inspect exact preservation, or use filter survival.

The preflight is diagnostic and **has no tuning authority**.

## 6. Audit

The v002 audit uses:

```text
depth: 14
sigma: 0.8, 0.9
q: 0.0, 0.1, 0.2, 0.3, 0.4
families: 30
MAX_ATTEMPTS: 64
```

Both σ panels must contain at least six dose-delivered accepted families. Otherwise:

```text
CLOSED_PRE_PRIMARY — DOSE_NOT_RESOLVED
```

If both are informative, both realized-C trend tests must satisfy one-sided p < 0.10. Otherwise:

```text
CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED
```

## 7. Primary

Primary depths:

```text
14, 16, 18
```

Thirty frozen seed families per depth.

Main cells:

```text
2 sigma × 5 q × 3 depths × 30 families = 900
```

plus:

```text
A0 = 90
Z0 = 90
```

for 1,080 planned cells before infeasibility logging.

Infeasible families are never replaced.

## 8. Condition validity

For a condition's accepted family set \(A_c\):

- \(|A_c|\ge21\), otherwise `UNDERPOWERED_CONDITION`;
- every accepted cell is Population V;
- every accepted cell exact-preserves;
- median \(R_{node}\ge0.25\);
- median \(G_{time}\ge1.10\).

This changes only the denominator; exactness itself is not weakened.

## 9. Dose resolution

A family is dose-delivered iff:

\[
\max_q C_i(q)>0.
\]

This is structure + mask only.

Audit panel informativeness:

\[
n_{\mathrm{dose}}\ge6.
\]

Primary H1 uses the same realized-C statistic on dose-delivered families. An unresolved primary panel is explicitly reported and cannot support `COUPLING_LAW_CANDIDATE`.

## 10. Execution order

```text
RATIFIED_SPEC_v002
→ FROZEN_STRUCTURE_v002
→ FROZEN_PREREG_v002
→ BUILD_ENGINE_v002
→ VALIDATE_v002
→ ACCEPTANCE_PREFLIGHT_v002
→ AUDIT_v002
→ AUDIT_FREEZE_v002
→ PRIMARY_v002
→ NULLS / ESTIMATORS
→ CONSOLIDATE
→ FINAL_FREEZE
```

No audit or primary execution is authorized by this structure file alone.
