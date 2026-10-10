# SCR_III_PREREG_v002

**Project:** Structural Complexity Reduction  
**Phase:** SCR-III-A v002 — Coupling Threshold and Valid Reduction  
**Benchmark:** `ROUTE_CSP_C v001` (unchanged C-MASK generator)  
**Status:** `FROZEN_BEFORE_PREFLIGHT`  
**Frozen:** 2026-10-08  
**Basis:** `SCR_III_COUPLING_SPEC_v002` (`RATIFIED_SPEC`) and `SCR_III_STRUCTURE_v002` (`FROZEN_STRUCTURE`)

No v002 acceptance-preflight, audit, or primary result was used to choose the rules below.

## 1. Scientific question

> Given a frozen structural grammar and a target with controlled shared generative cause, does target recall increase with **realized structural coverage C**, and where does contraction become preservation-valid?

v002 repairs the audit-resolution problem exposed by v001. It does not change C-MASK itself.

## 2. v001 disposition

v001 remains:

```text
CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED
```

No v001 audit is rerun. No v001 primary seed is reused.

## 3. Source lock

`SOURCE_LOCK_v002.md` is normative.

The following remain byte-identical:

- frozen SCR-II v002 grammar/filter/solvers/generator/metrics;
- `scr_iii/compat.py`;
- `scr_iii/engine_common.py`;
- `scr_iii/generator/route_csp_c_v001.py`;
- `scr_iii/nulls/controls_v001.py`;
- `scr_iii/analysis/metrics_v001.py`;
- `scr_iii/analysis/estimators_v001.py`;
- `scr_iii/analysis/structure_stats_v001.py`.

v002 implementation must add versioned runners/analysis rather than overwrite v001 audit/primary executables.

## 4. Frozen benchmark constants

```text
checksum modulus: 5
q: {0.0, 0.1, 0.2, 0.3, 0.4}
sigma: {0.8, 0.9}
M_min: 4
free-subspace density band: [0.02, 0.04]
MAX_ATTEMPTS: 64
PENALTY: 2 * d * COST_MAX
C-MASK: unchanged from v001
C-LABEL: out of scope
```

No audit outcome may alter these.

## 5. Family generation

The family-level common-attempt construction is unchanged from v001.

For a seed/depth family:

1. shared structure stream;
2. shared nested mask permutation;
3. shared base arithmetic attempt sequence;
4. the first attempt 0–63 satisfying the multiplicity/density rule for every active q is accepted;
5. that accepted attempt is used across both σ arms and all q levels.

If no common attempt succeeds:

```text
INFEASIBLE_FAMILY
```

The seed is not replaced.

Family acceptance never reads \(S_T\cap S_G\), recall, EI, exact preservation, or SCR/filter survival.

## 6. Real-engine acceptance-only preflight

### Seeds

Use only the `acceptance_preflight` blocks in `SEEDS_v002.json`:

```text
d=14: 30 families
d=16: 30 families
d=18: 30 families
```

These seeds are burned immediately after this preflight and may not enter audit or primary.

### Permitted observations

- accepted/infeasible;
- attempt index and attempts examined;
- baseline m;
- free-subspace density at each q;
- deterministic instance/provenance hashes.

### Forbidden observations

The preflight must not call or inspect:

- `solve_scr`;
- SCR/filter target survival;
- recall;
- EI;
- exact preservation;
- solution-loss ledger;
- any PG5/H1 statistic.

### Reporting

For each depth report accepted / 30 and median accepted-attempt index.

Flags:

```text
accepted/30 < 15:
    LOW_COMMON_ATTEMPT_ACCEPTANCE

accepted/30 < 21:
    STRICT_VALIDITY_POWER_RISK
```

These flags are diagnostic only. They cannot change the cap, grid, thresholds, or seeds.

## 7. Audit design

```text
depth: 14 only
families: 30
sigma: 0.8, 0.9
q: 0.0, 0.1, 0.2, 0.3, 0.4
MAX_ATTEMPTS: 64
```

Use only the `audit.depth_14` seeds in `SEEDS_v002.json`.

## 8. Dose-delivered families

For accepted family \(i\) and σ:

\[
D_i=\{\ell:u_\ell\ge\sigma\}
\]

\[
C_i(q)=
\begin{cases}
|M_q\cap D_i|/|D_i|,& |D_i|>0\\
0,& |D_i|=0
\end{cases}
\]

A family is:

```text
DOSE_DELIVERED
```

iff:

\[
\max_q C_i(q)>0.
\]

Otherwise:

```text
DOSE_FREE_FAMILY
```

This classification is computed from structure + mask before SCR outcome inspection.

Dose-free cells stay in Population A and all descriptive analyses.

## 9. PG5a — panel informativeness

For each d=14 σ panel, count dose-delivered **accepted** families.

Frozen threshold:

```text
n_dose_min = 6
```

Both σ=0.8 and σ=0.9 audit panels must meet it.

If either fails:

```text
CLOSED_PRE_PRIMARY — DOSE_NOT_RESOLVED
```

This is a closing design-resolution verdict.

## 10. PG5 — realized-C dose response

For each informative panel, restrict the trend statistic to dose-delivered accepted families:

\[
T_C=
\sum_i\sum_j
(C_{ij}-\bar C_i)(r_{ij}-\bar r_i).
\]

Within each family, permute C assignments to observed recall values, preserving tied C values and missingness.

Audit test:

```text
Monte Carlo permutations: 100000
one-sided alternative: T_C > 0
nominal pass threshold: p < 0.10
audit RNG: audit_trend_permutation_seed
```

Both informative σ panels must pass.

If either informative panel has p ≥ 0.10:

```text
CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED
```

## 11. Other audit gates

PG1, PG2, PG4, PG6, PG7, PG8 and PG9 are unchanged from v001.

PG3 remains:

```text
common-attempt acceptance >= 0.50 at audit depth d=14
```

A PG3 miss is recorded as in v001; it does not supersede the explicit closing logic of PG5a/PG5 unless another unchanged closing gate fails.

PG9 is evaluated over d=14 audit conditions.

## 12. Audit authorization rule

Primary is unauthorized unless the v002 audit completes with no closing gate failure.

The audit is then hash-frozen before any primary execution.

## 13. Primary design

```text
depths: 14, 16, 18
families per depth: 30
sigma: 0.8, 0.9
q: 0.0, 0.1, 0.2, 0.3, 0.4
```

Planned:

```text
main: 900 cells
A0: 90 cells
Z0: 90 cells
total: 1080 cells
```

before infeasibility logging.

No infeasible family is replaced.

## 14. Analysis populations

Unchanged from v001.

**Population A:** every successfully generated, non-invalid cell.

**Population V:** exact-validity eligible cells satisfying:

\[
L\ge m
\]

and

\[
R_{leaf}\ge0.25.
\]

Population-A cells are never silently removed from the ruler map.

## 15. Preservation and reduction metrics

Unchanged from v001:

- recall \(r\);
- leak count;
- exact-set equality;
- \(a_0\);
- EI;
- extra solutions;
- \(R_{leaf}\);
- \(R_{node}\);
- \(G_{time}\);
- \(T_{encode}\);
- C;
- \(N_{rej,free}\);
- provenance and hashes.

## 16. Primary H1

For each of the six \((σ,d)\) panels:

1. identify dose-delivered accepted families using §8;
2. if fewer than 6 exist, label:

```text
PANEL_DOSE_UNRESOLVED
```

and report descriptively;
3. otherwise compute the same realized-C \(T_C\) permutation test.

Use:

```text
100000 permutations per informative panel
one-sided T_C > 0
primary_trend_permutation_seed
Holm correction across dose-informative primary panels
familywise alpha = 0.05
```

An unresolved panel does **not** count as evidence for `COUPLING_LAW_CANDIDATE`.

Recall versus nominal q remains descriptive.

## 17. Estimators

E1/E2 algorithms and pass thresholds are unchanged from v001.

Because generation can reject families, within each primary depth:

- order accepted families by frozen seed-list order;
- the first five accepted families are E1 calibration families;
- all remaining accepted families are holdout.

No target-survival result is used to choose the split.

## 18. Condition-level exact validity

For condition \(c\), let \(A_c\) be its accepted family set.

`VALID_STRUCTURAL_REDUCTION` requires:

1. \(|A_c|\ge21\);
2. every accepted cell is Population V;
3. **every** accepted cell exact-preserves;
4. median \(R_{node}\ge0.25\);
5. median \(G_{time}\ge1.10\).

If \(|A_c|<21\):

```text
UNDERPOWERED_CONDITION
```

The condition is still reported in the map.

`HIGH_RELIABILITY_REDUCTION` requires ≥90% of \(A_c\) exact-preserving plus the same reduction/gain thresholds. It is descriptive and is not exact equivalence.

## 19. Study verdicts

### `TRANSFER_CONFIRMED`

Same q/σ condition is `VALID_STRUCTURAL_REDUCTION` independently at d=14,16,18.

### `COUPLING_LAW_CANDIDATE`

Requires:

- every dose-informative primary panel passes H1 after Holm correction;
- no primary panel is `PANEL_DOSE_UNRESOLVED`;
- E1/E2 meet their frozen criteria;
- verdict-bearing controls pass;
- C1 is exact in 100%.

### `COUPLING_MAP_ONLY`

Valid primary map exists but the law-candidate criteria are not all met.

### `CLOSED_PRE_PRIMARY — DOSE_NOT_RESOLVED`

Audit manipulation not sufficiently delivered.

### `CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED`

Dose was delivered in both audit panels but the realized-C recall trend failed in at least one.

Other v001 closing statuses remain available unchanged.

## 20. Controls

C0/SCR/C1/A0/Z0/N1–N4 are unchanged from v001.

N4 retains the frozen anti-coupled construction order.

No control outcome may alter the grid or thresholds.

## 21. Seed discipline

`SEEDS_v002.json` is normative.

It is disjoint from:

- SCR-I v003 explicit blocks;
- SCR-II v001/v002 explicit blocks;
- spent v001 audit blocks;
- reserved unrun v001 primary blocks;
- v001 smoke seeds 9100000–9100029;
- shim-pilot blocks 9212000–9212039, 9214000–9214039, 9216000–9216039, 9218000–9218039.

The engine preflight must re-check collisions programmatically.

## 22. Anti-tuning

After this preregistration is frozen, v002 may not:

- add q=0.5;
- add σ=0.7 or σ=0.95;
- change n_dose_min=6;
- change n_acc_min=21;
- change audit/primary family counts;
- raise MAX_ATTEMPTS above 64;
- widen the density band;
- lower M_min;
- replace rejected families;
- change PG5/H1 thresholds;
- reinterpret a dose-unresolved panel as supportive.

Any scientific change requires v003.

## 23. Execution order

```text
VALIDATE_V002
→ ACCEPTANCE_PREFLIGHT_V002
→ AUDIT_V002
→ AUDIT_FREEZE_V002
→ PRIMARY_V002
→ NULLS_V002
→ ESTIMATORS_V002
→ CONSOLIDATE_V002
→ FINAL_FREEZE_V002
```

No primary run is authorized before the audit freeze exists and validates.
