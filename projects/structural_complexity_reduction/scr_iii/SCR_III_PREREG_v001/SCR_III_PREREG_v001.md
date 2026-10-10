# SCR_III_PREREG_v001

**Project:** Structural Complexity Reduction  
**Phase:** SCR-III-A — Coupling Threshold and Valid Reduction  
**Benchmark:** `ROUTE_CSP_C v001`  
**Status:** `FROZEN_BEFORE_AUDIT`  
**Frozen:** 2026-10-08  
**Basis:** `SCR_III_COUPLING_SPEC_v001` (`RATIFIED_SPEC`) and `SCR_III_STRUCTURE_v001` (`FROZEN_STRUCTURE`)

No audit or primary result was used to choose any rule below.

## 1. Research question

> When a frozen structural grammar and an independently solved target share a controlled generative cause, how does target preservation change as that coupling increases, and where does state-space contraction become preservation-valid and computationally useful?

SCR-III-A is a ruler experiment. It does not test whether any real physical target is coupled to UNNS.

## 2. Frozen source lock

The following SCR-II v002 artifacts are imported byte-identically and are read-only:

| File under `scr_ii/` | SHA-256 |
|---|---|
| `grammar/route_grammar.py` | `f0b855b8201a23ba6abb175b8b342627fd4e389fc41608fe7b3b27958946c1a0` |
| `filter/structural_filter.py` | `162d91a9e75af7c7569069ec8049c5089c555a003a04e8a718dc84776c5f5be6` |
| `solver/exact_solver.py` | `f981bc237e99e605ea66b93a5175e0145110a9cff02236c11cdc39ee486539b0` |
| `nulls/controls.py` | `83451edaa2c1da0657cf7a21394944541be7d6f7929e5aae50bcc677f7f0caf1` |
| `generator/route_csp_i_v002.py` | `9f7e38c95e00f930af437a92fca3981344acb888d6a8fdb754ee1d2bc4f88d98` |
| `engine_common.py` | `4bd542d52e236248d8453bf00e8871335eadf9df6def44ee312c258a56a40bfe` |
| `analysis/metrics.py` | `58ddf67184cd53794174d69aaf52c88777cdc9c5d2b6cbceec3c54b3836b9cfd` |

Preflight must recompute and match all seven hashes.

`structural_filter.py` continues to consume the same structural field names: `symbol`, `phase`, `discontinuity`, `branch_id`.

## 3. Frozen benchmark constants

```text
checksum modulus: 5
density band on free subspace: [0.02, 0.04]
M_min: 4
attempt budget per seed family: 64
COST_MAX: 1000 (v002 draw law)
PENALTY: 2 * d * COST_MAX
cost-window half-width: round(0.025 * d * 1000)
grammar: Γ_route v001
gate order: G1 → G2 → G3 → G4
```

No constant above may be changed inside v001 after audit begins.

## 4. Coupling construction

For each depth-family seed:

1. Generate one structural skeleton stream with unconditional per-layer mirror variates \(u_i\).
2. Generate one coupling permutation π, independent of structure.
3. For σ, mirror a layer when \(u_i<σ\).
4. For q, use nested mask \(M_q=\pi[:\mathrm{round}(qd)]\).
5. Generate the v002-style sequence of base arithmetic attempts once.
6. Search attempts 0–63 in order for the first **common attempt** satisfying the frozen multiplicity/density rule at every active q for that depth.
7. Use that same accepted attempt across every q and both σ levels in the family.
8. At masked layers, anchor to the structural good option and penalize the decoy.
9. Compute the target predicate exactly as frozen in the coupling specification.

If no common attempt exists, record `INFEASIBLE_FAMILY`; do not substitute another seed.

Acceptance may not inspect target survival under the structural filter.

## 5. Frozen grid

### Audit

```text
depth 10:
  sigma = {0.8, 0.9}
  q     = {0.0, 0.1, 0.2, 0.3}
  12 seed families

depth 12:
  sigma = {0.8, 0.9}
  q     = {0.0, 0.1, 0.2, 0.3, 0.4}
  12 seed families
```

A0 and Z0 anchors are run at both audit depths.

### Primary

```text
depth = {14, 16, 18}
sigma = {0.8, 0.9}
q     = {0.0, 0.1, 0.2, 0.3, 0.4}
20 seed families per depth
```

Planned main cells: 600.  
A0 anchor cells: 60.  
Z0 anchor cells: 60.  
Total planned cells: 720.

No grid expansion is permitted in v001.

## 6. Frozen seeds

The canonical seed file is `SEEDS_v001.json`.

### Audit

```text
d=10:
2026111101 2026111102 2026111103 2026111104
2026111105 2026111106 2026111107 2026111108
2026111109 2026111110 2026111111 2026111112

d=12:
2026111201 2026111202 2026111203 2026111204
2026111205 2026111206 2026111207 2026111208
2026111209 2026111210 2026111211 2026111212
```

### Primary

```text
d=14:
2026112101–2026112120

d=16:
2026112201–2026112220

d=18:
2026112301–2026112320
```

Within each primary depth:
- families 1–5 are E1 calibration families;
- families 6–20 are estimator-holdout families.

All siblings of a family remain on the same side of this split.

The seed file also freezes null/analysis RNG bases. Burned smoke-test seeds 9100000–9100029 are forbidden.

## 7. Metrics

For every non-invalid cell record:

### Preservation

\[
r=\frac{|S_T\cap S_G|}{|S_T|}
\]

\[
\ell=|S_T\setminus S_G|
\]

\[
a_0=\frac{|S_G\setminus S_T|}{N-|S_T|}
\]

\[
EI=\frac{r-a_0}{1-a_0}
\]

plus:
- exact-set equality indicator;
- extra solutions, which must be zero.

### Reduction and cost

- \(R_{leaf}\)
- \(R_{node}\)
- \(G_{time}=T_{baseline}/T_{SCR,total}\)
- \(T_{encode}\), reported separately
- baseline and SCR node counts
- baseline/SCR/C1 wall time

### Structure-only

- \(L=|S_G|\)
- \(m=|S_T|\)
- \(|D|\)
- C
- \(N_{rej,free}\)
- q, σ, depth, free-layer count f
- accepted attempt index

### Provenance

- seed family
- instance SHA-256
- source-hash preflight
- RNG stream identifiers
- benchmark/schema versions

## 8. Analysis populations

**Population A:** every successfully generated non-invalid cell. Used for the coupling ruler and all graded preservation/reduction analyses.

**Population V:** cells satisfying:

\[
L\ge m
\]

and

\[
R_{leaf}\ge0.25.
\]

Population V is only the exact-validity-eligible stratum.

No exact-infeasible or low-reduction cell is deleted from Population A.

## 9. Controls and nulls

### C0
Baseline exact solver. Defines \(S_T\).

### SCR
Frozen structural filter + unchanged SCR solver.

### C1
Frozen solver-native arithmetic pruning. Must match C0 exactly in 100 % of cells.

### A0
Unmodified v002 generator on the same depth-family seeds. Used as the independent-target anchor.

### Z0
σ = 1, q = 0. Must give \(L=N\) and exact preservation.

### N1 — rate-matched random prefix pruning
50 replicates per cell.

For each cell:

\[
p_{acc}=(L/N)^{1/d}.
\]

This parameter is derived from the cell's structure-only leaf fraction and is not tuned using target labels.

### N2 — symbol shuffle
Use the frozen SCR-II v001 null implementation.

### N3 — degree-preserving grammar transition permutation
Use the frozen SCR-II v001 null implementation.

N2 and N3 each use 12 fixed permutations on the first five primary seed families at each main condition.

### N4 — anti-coupled sign control
Use the same base arithmetic draw and mask as C-MASK, but:
1. set the anti-anchor to the decoy option at masked layers;
2. penalize the good option at masked layers;
3. only then compute anti-anchor cost, checksum target, terminal seal and window.

Expected sign: median EI ≤ 0.

## 10. Solution-loss ledger

For each baseline solution absent from SCR, walk the solution prefix through G1→G4 and record the first failing gate.

This ledger is descriptive/attributional only.

Single-gate causal coupling arms are out of scope and reserved for:

```text
SCR_III_A2_GATE_ABLATION
```

## 11. SCR applicability estimators

### E1 — family/regime calibration

At each primary depth and condition:
- use the first five preregistered families to compute calibration mean recall and EI;
- predict the mean recall/EI of the remaining fifteen families by those calibration means.

Evaluate across the 30 main primary conditions.

Pass criterion:
- recall MAE ≤ 0.10;
- Spearman correlation of predicted versus held-out condition-mean recall ≥ 0.80.

### E2 — charged instance-level estimator

For every estimator-holdout primary cell:
- prefix depth h = 6;
- choose 8 of 64 prefix subtrees without replacement using the deterministic estimator RNG;
- exhaustively enumerate C0 and SCR only inside those subtrees;
- estimate recall and EI from the sample;
- predict whole-cell recall/EI.

Pass criterion:
- cell-level recall MAE ≤ 0.10;
- Spearman predicted versus observed recall ≥ 0.80.

Record \(C_{E2}/T_{baseline}\). E2 cost does not disappear from any computational claim.

## 12. Confirmatory hypotheses

### H0 — anchors
A0 must reproduce the qualitative v002 independent-target regime. Z0 must preserve exactly with \(L=N\).

### H1 — paired monotone dose response
For each primary \((σ,d)\) panel use the one-sided seed-blocked permutation statistic:

\[
T=\sum_i\sum_j(q_{ij}-\bar q_i)(r_{ij}-\bar r_i).
\]

Permute q labels only within family, preserving missingness.

Use:
```text
100000 Monte Carlo permutations
trend_permutation_seed = 2026119901
one-sided alternative: T > 0
Holm correction across 6 primary panels
familywise alpha = 0.05
```

H1 passes only if all feasible panels remain significant after Holm correction.

### H3a — construction anchor
Any Population-V cell with C = 1 must preserve exactly.

### H3b — free rejecting layers
For cells with \(N_{rej,free}\ge3\), pooled \(P_{exact}\le0.20\).

### H4 — applicability estimator
E1 and E2 meet their frozen §11 thresholds.

### H5 — controls
- N1 mean EI within ±0.01;
- N4 median EI ≤ 0;
- C1 exact in 100 %;
- Z0 exact with \(L=N\) in 100 % of valid cells.

N2/N3 are reported but not verdict-bearing.

## 13. Audit gates

| Gate | Requirement | Failure |
|---|---|---|
| PG1 | source hashes, determinism, RNG separation, firewall, family attempt reuse | `INVALID_RUN` |
| PG2 | σ=0, q=0 C-MASK generator equivalent in law to A0/v002 | `CLOSED_PRE_PRIMARY — GENERATOR_NOT_V002_EQUIVALENT` |
| PG3 | common-attempt family acceptance ≥0.5 at each audit depth | failing entries `INFEASIBLE_CONDITION`; no replacement grid |
| PG4 | each σ has ≥1 q with audit \(P(L\ge m)\ge0.9\) | σ labelled `EXACT_TIER_INFEASIBLE`; map analysis retained |
| PG5 | positive blocked dose trend at nominal p<0.10 in every audit panel | `CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED` |
| PG6 | N4 median EI ≤0 | `CLOSED_PRE_PRIMARY — KNOB_SIGN_ERROR` |
| PG7 | Z0 exact, \(L=N\) | `INVALID_RUN` |
| PG8 | C1 = C0 exactly | `INVALID_RUN` |
| PG9 | ≥1 audit condition mean recall in (0.1,0.9) | `CLOSED_PRE_PRIMARY — STEP_FUNCTION_KNOB` |

Audit may not modify the design.

## 14. Cell verdict order

```text
INVALID_RUN
→ PRESERVATION_FAIL
→ NO_MATERIAL_REDUCTION
→ REDUCTION_WITHOUT_NET_GAIN
→ VALID_STRUCTURAL_REDUCTION
```

Thresholds:
```text
NO_MATERIAL_REDUCTION: R_node < 0.25
REDUCTION_WITHOUT_NET_GAIN: G_time < 1.10
```

## 15. Condition verdicts

A condition is `VALID_STRUCTURAL_REDUCTION` only when all are true:

1. 20/20 preregistered cells generated successfully;
2. 20/20 are Population V;
3. 20/20 preserve the exact target set;
4. median \(R_{node}\ge0.25\);
5. median \(G_{time}\ge1.10\).

Report the exact Clopper–Pearson interval.

`HIGH_RELIABILITY_REDUCTION` may be reported when at least 18/20 exact-preserve and the reduction/gain thresholds pass. It is not an exact-equivalence result.

## 16. Study verdicts

### `TRANSFER_CONFIRMED`
The same preregistered q/σ condition is `VALID_STRUCTURAL_REDUCTION` independently at d = 14, 16 and 18.

### `COUPLING_LAW_CANDIDATE`
All of:
- H1 passes in every feasible primary panel after Holm correction;
- H4 passes;
- H5 verdict-bearing controls pass;
- C1 exact in 100 %;
- recall moves in the preregistered direction with realized C.

### `COUPLING_MAP_ONLY`
Primary executes validly and yields the frozen map, but not every law-candidate criterion passes.

### `CLOSED_PRE_PRIMARY — <reason>`
A closure audit gate fails.

No complexity-class conclusion is permitted.

## 17. Schema freeze requirement

SCR-III must create:

```text
scr_iii/SCR_III_PREREG_v001/schema/route_csp_c_v001.schema.json
```

The reason is benchmark/version/interface separation and new coupling metadata (`sigma`, q, mask/coverage provenance, family attempt index, RNG stream IDs), **not** an option-cost maximum in the old SCR-II schema.

The schema must validate before audit.

## 18. Preflight requirements

Before `RUN_AUDIT.bat` may execute:

1. all seven frozen hashes match;
2. `SEEDS_v001.json` validates and is disjoint from known frozen/burned blocks;
3. new instance/result schemas validate;
4. determinism test passes;
5. stream-separation test passes;
6. family-pairing/common-attempt test passes;
7. extended structural-filter firewall test passes;
8. C1/C0 exactness unit tests pass on test fixtures;
9. Z0 and N4 construction tests pass;
10. preregistration manifest and SHA-256 freeze are generated.

If any preflight item fails, audit is not authorized.

## 19. Execution order

```text
PREFLIGHT
→ AUDIT
→ AUDIT_REPORT
→ AUDIT_FREEZE
→ PRIMARY
→ NULLS
→ ESTIMATORS
→ CONSOLIDATE
→ FINAL_FREEZE
```

Primary execution is forbidden until the audit is accepted without changing the preregistration.

## 20. Anti-tuning / map-only lock

Within v001, after audit begins:

- q = 0.5 may not be added;
- σ = 0.95 may not be added;
- \(M_{min}\) may not be lowered;
- the density band may not be widened;
- failed/infeasible seeds may not be replaced;
- validity may not be weakened;
- C-LABEL may not replace C-MASK;
- UPI may not enter the primary filter or verdict.

If an expanded high-coupling study is scientifically warranted, create a new version.

## 21. UPI

UPI/H-UPI is out of scope for SCR-III-A.

It may return in SCR-III-B as a blinded secondary diagnostic after the physical grammar and target protocol are frozen.

## 22. Authorized next step

After the preregistration files, schemas, config and hash freeze are assembled and `RUN_VALIDATE.bat` passes, build:

```text
SCR_III_ENGINE_v001
```

No primary run is authorized by this document alone.
