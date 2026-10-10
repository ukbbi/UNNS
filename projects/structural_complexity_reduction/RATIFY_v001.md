# SCR-III-B Primary Design Ratification — 2026-10-10

**Status:** DESIGN CHOICES RATIFIED; PRIMARY DOCUMENTS NOT YET FROZEN; PRIMARY RUN NOT AUTHORIZED.
**Basis:** `PREFLIGHT_v009.zip`, particularly `DECISION_REGISTER_v009.md`, `REPORT_v009.md`, and v009 synthetic uncertainty simulations.
**Scope:** Outcome-blind 3×3 Generative Admissibility / Physical Sufficiency primary study.

## Ratified decision register

| ID | Decision | Ratified selection |
|---|---|---|
| 1 | Patch | Fixed 3×3 free-boundary square ice, 24 spins, 16,777,216 nominal configurations |
| 2 | Primary window | `W = k_B × 792 K = 1.093474008e-20 J`, using exact SI Boltzmann constant |
| 3 | Sensitivity windows | `W=0.5 k_B T` and `W=2 k_B T`, reported separately; neither rescues primary failure |
| 4 | Numerical policy | `tau = 1e-9 × sum(abs(K_ij))`; operational membership `E <= E0 + W + tau`; distinct from ideal exact-arithmetic membership; all ambiguous threshold cases included conservatively and flagged |
| 5 | Null master seed | `20261010`, deterministic domain-separated family/index sub-seeds |
| 6 | Null counts | 1,000 valid N1 degree-preserving and 1,000 valid N2 free-incidence nulls; 5,000 draw cap each; report shortfalls, rejection reasons, and hashes |
| 7 | E2 | Retain strongest 75% of pair interactions by absolute coupling, tie by pair index; certified omitted-term bound and full fallback; cost sensitivity reported, exactness independently tested |
| 8 | Global Z2 symmetry | Off for primary; separate equal-opportunity sensitivity only |
| 9 | B0 | Optimized single-thread Gray-code exhaustive complete-target solver with exact resynchronization |
| 10 | B1 | Exact Hamiltonian-aware branch-and-bound, bound proof retained; required sensitivity arm, not H-C denominator |
| 11 | H-G | Exact constructive/brute-force membership agreement, no energy/target leakage, ≥99% nominal candidate contraction; known v007 count is historical replication |
| 12 | H-P | Complete global physical-target certification and zero false exclusions; separately report delta_nonG and W/delta_nonG after unblinding |
| 13 | H-T | NOT_TESTED; future independent target-family protocol required |
| 14 | H-C | See revised deterministic paired-round rule below, conditional on P and complete output |
| 15 | Timing | Single thread, 3 warmups, 15 timed paired rounds, deterministic balanced interleaving and logged environment |
| 16 | Budgets | 30 minutes per algorithm arm and 2 GiB RSS; timeouts/shortfalls reported, no silent substitution |
| 17 | Global E0 | Frozen v007 physical anchor `-0.091840413960727757` A units, `-9.2719947518037269e-20 J`; same input for all solvers |
| 18 | Primary unblinding | Forbidden until a separately dated freeze and explicit authorization; v009 PASS itself is insufficient |

## Revised H-C uncertainty rule

The v009 proposed moving-block percentile bootstrap was labeled a nominal 95% interval, but synthetic coverage was only about 78–87%. **REJECT that interval as a 95% inferential decision procedure.**

Instead use a **deterministic, conservative operational success rule**, with no population confidence level implied:

1. Require H-P PASS and independently certified complete, identical target sets; otherwise C=`NOT_ELIGIBLE`.
2. Each of 15 predeclared paired timed rounds measures end-to-end B0 and G2 wall-clock cost under balanced order. Charge preprocessing, generation, downstream work, and relevant deployment certification according to the predeclared cost ledger; describe amortization separately.
3. Define `r_i = C_B0,i / C_G2,i`. Require positive, finite denominators and all 15 planned valid pairs; failures/timeouts are disclosed, not omitted.
4. Require both `median(r_i) >= 1.20` **and** `min_i(r_i) >= 1.20` for H-C `PASS`.
5. If all required outputs are correct and any pair falls below 1.20, classify `THRESHOLD_NOT_MET` (not a claim of zero speedup); if measurement completeness fails, classify `INCONCLUSIVE` or `EXECUTION_LIMIT`.
6. Report all 15 paired ratios, paired medians, full cost ledger, CPU/wall times, and B1/E2 sensitivities. Exploratory bootstrap intervals may be included **only** as explicitly uncalibrated descriptive diagnostics, never as a formal 95% bound.

This is a demanding finite-sample decision rule, **not** a statistically calibrated test of future-machine performance. It can fail due to runtime variation and therefore controls the positive operational claim rather than proving statistical absence of benefit.

## Null interpretation

Compute full real-versus-null survivor-count and delta_nonG distributions and observed ranks. **No confirmatory p-value, significance threshold, or 'distinctive grammar' PASS is authorized**, because v009 included no prospective calibration or power analysis for that hypothesis. Nulls are controlled descriptive/adversarial comparisons; any separate null-superiority claim needs its own preregistered protocol.

## Numerical safeguards

The `tau` expansion defines an *operational* target, not an exact mathematical equality claim about the unexpanded window. Preserve inclusive equality. Report both `W` and `W+tau`, the threshold proximity diagnostic, exact direct energy uncertainties, and flagged ambiguous configurations. Any unresolved numerical case prevents an unqualified P PASS; conservative inclusion alone cannot be used to hide an unresolved certificate.

## Prior knowledge and leakage

The window was selected knowing public 1×1 and 2×2 results: delta_nonG = 0.871 and 0.952 `k_B T` respectively, so both fail at `W=k_B T`. The 3×3 low-energy W>0 outcomes remain withheld. v007 V4 statistics disclosed some upper-spectrum scale, not the low-energy target outcomes. Describe verifiers as separately implemented and cross-validated under shared authorship.

## Freeze and execution separation

This file **ratifies prospective scientific choices** but is not itself the signed/hash-locked primary preregistration. Assemble final SPEC and PREREG, inspect cross-document consistency, hash exact versions and frozen dependencies, then create a distinct dated primary freeze record. **Do not execute or unblind any real 3×3 W>0 task until a subsequent, explicit primary authorization.** Frozen v005–v009 preflights and GitHub remain unchanged.
