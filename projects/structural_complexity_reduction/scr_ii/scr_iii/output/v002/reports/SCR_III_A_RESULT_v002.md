# SCR_III_A_RESULT_v002

**Project:** Structural Complexity Reduction (SCR)  
**Phase:** SCR-III-A — Controlled Coupling Gradient  
**Engine:** `SCR_III_ENGINE_v002`  
**Status:** `FROZEN_RESULT`  
**Final study verdict:** `COUPLING_MAP_ONLY`  
**Freeze date:** 2026-10-08

## 1. Final result

SCR-III-A v002 completed the preregistered controlled-coupling study without altering the frozen C-MASK construction, q-grid, σ levels, controls, estimator thresholds, or exact-validity doctrine.

The final study verdict is:

```text
COUPLING_MAP_ONLY
```

This is a completed scientific outcome, not an implementation failure.

The study established a reproducible relationship between **realized structural coverage C** and target preservation, but it did not produce a condition satisfying the full `VALID_STRUCTURAL_REDUCTION` criterion and did not satisfy the full estimator requirement H4.

## 2. Execution accounting

Primary design:

```text
planned main cells: 900
generated main cells: 660
accepted families:
  d=14: 24/30
  d=16: 21/30
  d=18: 21/30
infeasible families: 24
```

No infeasible family was replaced.

Primary cell verdicts:

```text
PRESERVATION_FAIL: 448
NO_MATERIAL_REDUCTION: 152
REDUCTION_WITHOUT_NET_GAIN: 60
VALID_STRUCTURAL_REDUCTION: 0
```

No main cell reached `VALID_STRUCTURAL_REDUCTION`.

## 3. Confirmatory hypothesis record

| Hypothesis / control | Result | Frozen interpretation |
|---|---|---|
| **H1 realized-C dose response** | **PASS** | Recall responds positively to delivered structural coupling across all six informative primary panels. |
| **H3a construction anchor** | **PASS** | All 57 C=1 anchor cells satisfy the construction check. |
| **H3b free-rejecting-layer prediction** | **PASS** | `P_exact = 0.0` when `N_rej,free >= 3`. |
| **H4 applicability estimators** | **FAIL** | E1 fails; E2 passes. The two-estimator conjunction therefore fails. |
| **H5 controls** | **PASS** | Random and anti-coupled controls have the preregistered signs/calibration; C1 and Z0 pass. |
| **TRANSFER_CONFIRMED** | **NO** | No condition is preservation-valid across d=14/16/18. |
| **COUPLING_LAW_CANDIDATE** | **NO** | H4 is a required conjunct and failed. |

Overall cellwise Spearman correlation between C and recall:

```text
0.367148384228
```

This aggregate correlation is descriptive; the preregistered H1 conclusion comes from the paired within-family realized-C tests.

## 4. H1 — the central positive finding

Every primary `(depth, sigma)` panel was dose-informative and every panel passed the one-sided realized-C permutation test after Holm correction:

| depth | σ | dose-delivered families | one-sided p | Holm p | pass |
|---:|---:|---:|---:|---:|---|
| 14 | 0.8 | 20 | 9.9999e-06 | 5.99994e-05 | True |
| 14 | 0.9 | 13 | 9.9999e-06 | 5.99994e-05 | True |
| 16 | 0.8 | 14 | 9.9999e-06 | 5.99994e-05 | True |
| 16 | 0.9 | 8 | 9.9999e-06 | 5.99994e-05 | True |
| 18 | 0.8 | 15 | 9.9999e-06 | 5.99994e-05 | True |
| 18 | 0.9 | 9 | 9.9999e-06 | 5.99994e-05 | True |

Thus v002 resolves the v001 audit problem: when the manipulation is measured by **realized delivered coverage C**, preservation changes reproducibly with coupling across depth and σ.

This establishes a controlled coupling map. It does **not** establish that an unrelated or physical target naturally possesses such coupling.

## 5. Exact preservation and the validity boundary

There are 30 preregistered primary conditions.

```text
VALID_STRUCTURAL_REDUCTION conditions: 0
HIGH_RELIABILITY_REDUCTION conditions: 0
UNDERPOWERED_CONDITION conditions: 0
```

The strongest exact-preservation condition was:

```text
d=14
sigma=0.9
q=0.4
exact=18/24 (75.0%)
Population V=16/24
median R_node=0.312519
median G_time=0.220295
```

This condition improves preservation substantially, but it still fails the strict exact-equivalence requirement and has no net computational gain.

The condition with the largest median `G_time` was:

```text
d=18
sigma=0.8
q=0.0
median R_node=0.868900
median G_time=0.947668
exact=2/21
```

Even there, median `G_time < 1`, so no primary condition produces a net runtime gain under the frozen end-to-end convention.

The main v002 boundary is therefore:

\[
\text{more realized coupling}
\rightarrow
\text{better preservation},
\]

but

\[
\text{better preservation}
\not\Rightarrow
\text{valid structural reduction}.
\]

Preservation, material contraction, and net gain must coexist; they do not coexist on the v002 grid.

## 6. Controls

The completed null/control stage records:

```text
C1 exact control: True
Z0 control: True
H5: True
N1 mean EI: 6.7530821649e-05
N4 median EI: -0.0543545963954
```

N1 is effectively centered on zero, while N4 is negative as required. The problem-aligned C1 control preserves the exact target.

## 7. Applicability estimators

### E1 — family/regime calibration

```text
MAE: 0.156610066660
Spearman: 0.599110122358
PASS: False
```

E1 does not meet the frozen thresholds (`MAE <= 0.10`, `Spearman >= 0.80`).

### E2 — charged instance-level estimator

```text
MAE: 0.073719410352
Spearman: 0.899616491659
PASS: True
median C_E2 / T_baseline: 0.408569
mean C_E2 / T_baseline: 0.483028
evaluated holdout cells: 510
```

E2 meets the frozen predictive thresholds. Its cost is not free and must remain explicitly charged in any transfer experiment.

The frozen interpretation is:

\[
\boxed{\text{family-transfer estimator insufficient; local sampled estimator viable}}
\]

E1 is retained as a negative result/secondary baseline. E2 is the candidate estimator carried into SCR-III-B.

## 8. What SCR-III-A v002 establishes

The defensible positive finding is:

> In a benchmark where grammar–target coupling is created through a declared shared generative channel and measured independently by realized structural coverage C, target preservation responds reproducibly to delivered coupling across multiple depths and two structural-degeneracy regimes.

The equally important boundary is:

> The tested coupling range does not yield preservation-valid, materially reducing, net-faster SCR under the preregistered exact criterion.

Therefore v002 supports a **coupling map**, not a transfer claim and not a complexity-class claim.

## 9. What it does not establish

SCR-III-A v002 does not establish:

- that a real physical target is naturally coupled to a UNNS grammar;
- that C can be directly observed in a real system;
- that structural preprocessing is universally useful;
- that the v002 grid contains a valid reduction regime outside the tested range;
- that E1 is suitable for deployment;
- that E2 is computationally negligible;
- that any complexity class is changed.

No post-hoc q/σ extension, threshold change, estimator rescue, or rerun is authorized inside v002.

## 10. Frozen next scientific question

SCR-III-B asks:

> Does a physical system, whose structural grammar is frozen without target access and whose target is solved or measured independently, naturally occupy a region analogous to the favorable part of the SCR-III-A coupling map?

SCR-III-B carries E2 forward as the preferred applicability estimator, with its compute cost explicitly charged.

SCR-III-A v002 is complete and frozen at `COUPLING_MAP_ONLY`.
