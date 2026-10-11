# Structural Complexity Reduction (SCR)

**UNNS Substrate research program**  
**Repository:** [ukbbi/UNNS — SCR](https://github.com/ukbbi/UNNS/tree/4e759d38/projects/structural_complexity_reduction)  
**Published reference commit:** [`4e759d38`](https://github.com/ukbbi/UNNS/commit/4e759d38) (abbreviated)  
**Research status:** SCR-I-A v003 frozen; SCR-IV formally closed; SCR-III held-out/physical-transfer work remains open.  
**SCR-IV closure verdict:** `SCR_IV_COMPLETE / FINITE_GAP_CERTIFIED / PREDICTIONS_PROVEN`

## Purpose

Structural Complexity Reduction investigates whether **generative structural admissibility** can restrict a nominal candidate or configuration space *before* downstream computation; whether that restriction preserves the mathematical or physical targets of interest; and when it produces a measurable computational benefit.

The UNNS (Unbounded Nested Number Sequences) motivation is that generation, routes, constraints, boundaries, and persistence may distinguish nominal possibilities from effectively admissible ones. SCR turns that motivation into separately testable criteria. A small admissible set is not automatically a physically sufficient or computationally advantageous one.

The program treats three questions as distinct:

1. **Contraction:** How much of the nominal space can a frozen grammar exclude or avoid constructing?
2. **Preservation:** Does it retain the specified target—mechanism basins, exact solutions, or physical low-energy configurations, as appropriate to the benchmark?
3. **Computational consequence:** Does the same downstream task run more efficiently after including filtering and verification costs?

For the physical SCR-III branch these are operationalized as **G** (generative contraction), **P** (physical sufficiency), **T** (external physical transfer), and **C** (costed computational consequence). The benchmark-specific preservation unit is always stated explicitly: SCR-I-A's basin/class recall must not be equated with SCR-III's all-state low-energy preservation.

## Research progression and outcomes

| Stage | Scientific question and system | Evidence-supported outcome | Record status |
|---|---|---|---|
| **SCR-I-A v003** | Can frozen structural gates reduce mechanism candidate pools while preserving viable **mechanism basins/classes**? | Strong contraction and viable-target enrichment; measured benchmark-specific end-to-end gains above a representation floor | **Frozen primary benchmark** |
| **SCR-II / `ROUTE_CSP_I`** | Can structural gates transfer to unseen layered binary route/CSP instances while preserving the **complete exact solution set** and reducing downstream cost? | Repository documentation establishes the benchmark architecture and intended exact-solution/controls design; no single terminal numerical verdict is asserted here | **Separate branch; consult its records** |
| **SCR-III-A** | Can the prior structural approach be coupled to a new problem family under a frozen coupling specification? | Frozen stage includes `COUPLING_MAP_ONLY` in the physical-transfer predecessor record | **Frozen predecessor** |
| **SCR-III-B (3×3 spin ice)** | Can a 2-in/2-out grammar retain all states within an energy window of a frozen square-spin-ice Hamiltonian? | 2,604 of 16,777,216 states admitted; at the preregistered 1 kBT window, **10/26** target states retained and **16** excluded: **G passes, P fails** | **Audited SCR-III numerical evidence, not Lean-certified** |
| **SCR-III-GAP4 (4×4)** | Does the finite excluded-state energy gap match a prospective prediction on a 40-spin instance? | Frozen numerical result supports δ₄ below 1 and inside the predeclared interval; original excluded-state minimum later corrected by exact certification | **Frozen numerical history plus additive correction** |
| **SCR-IV (IV-1 through IV-5)** | Can the exact encoded 4×4 global ground and grammar-excluded minima, gap, and predictions be certified by Lean? | Both minima, positive finite gap, and two frozen inequalities proved in recorded Lean execution; exact non-grammar witness/value corrected | **Closed** |

The stages address different standards of success. In particular, **the 8.39× SCR-I-A benchmark gain is not a speedup claim for the SCR-III/IV spin-ice calculation**.

## SCR-I-A v003 — canonical mechanism-space benchmark

The completed primary run reports **15/15 preregistered cells**: five primary seeds across pool sizes 2,500, 10,000, and 40,000.

| Measure | Frozen reported result |
|---|---:|
| Median candidate reduction | **92.03%** |
| Minimum mechanism-basin recall | **1.000** |
| Median end-to-end time gain | **8.39×** |
| Median operation-count gain | **6.73×** |
| Median viable-target fraction in the nominal pool | **52.52%** |
| Median viable-target fraction among survivors | **99.15%** |
| Median target-recall enrichment versus rate-matched random pruning | **1.889×** |

| Pool | Frozen verdict pattern | Median geometric coverage |
|---:|---|---:|
| 2,500 | 5/5 `REPRESENTATION_LOSS` | 86.98% |
| 10,000 | 5/5 `STRUCTURAL_COMPRESSION_PRESERVED` | 98.13% |
| 40,000 | 5/5 `STRUCTURAL_COMPRESSION_PRESERVED` | 99.83% |

**Canonical result:** `STRUCTURAL_COMPRESSION_CONFIRMED_ABOVE_REPRESENTATION_FLOOR`. Basin preservation alone is not unique to SCR under the larger-pool controls; the stronger joint observation is basin preservation **with strong enrichment of viable mechanisms** and benchmark-specific computational gains.

Records: [`output/reports/v003/SCR_I_V003_RESULT_RECORD.md`](output/reports/v003/SCR_I_V003_RESULT_RECORD.md), [`SCR_I_V003_ANALYSIS.md`](output/reports/v003/SCR_I_V003_ANALYSIS.md), [`SCR_I_V003_NULL_ANALYSIS.md`](output/reports/v003/SCR_I_V003_NULL_ANALYSIS.md), and [`output/exports/v003/SCR_I_V003_FINAL.json`](output/exports/v003/SCR_I_V003_FINAL.json). Frozen preregistration: [`SCR_I_PREREG_v003/`](SCR_I_PREREG_v003/). Earlier v001/v002 material remains archived; the earlier target-oracle guard and candidate-identity preservation-unit failures are retained as historical design corrections.

## SCR-II — cross-domain discrete transfer

The [`scr_ii/`](scr_ii/) branch introduces `ROUTE_CSP_I`: unseen layered binary route/constraint-satisfaction instances, a frozen route grammar, arithmetic solution constraints, exact downstream ground truth, matched nulls, and separate calibration/design/primary seeds. Its intended criterion is **complete exact-solution preservation**, not just basin recall.

This root summary does **not** assign SCR-II a final success or failure verdict without a consolidated terminal record. The branch's own sources and results remain authoritative for its execution status.

## SCR-III — physical admissibility and the exclusion gap

The physical branch studies finite **free-boundary square artificial spin ice**, with a frozen simulator-derived model Hamiltonian and a local **two-in/two-out vertex grammar**. Grammar membership and Hamiltonian energies are different calculations, but the Hamiltonian is **not claimed to have independent provenance** from the common frozen source.

For the full nominal space \(S_0\), grammar set \(S_G\), Hamiltonian \(H\), and whole-space ground energy \(E_0=\min_{s\in S_0}H(s)\), define

\[
S_T(W)=\{s\in S_0:H(s)\le E_0+W\},\qquad
\Delta_{\neg G}=\min_{s\notin S_G}H(s)-E_0.
\]

For a finite nonempty excluded set, **all** states in the inclusive energy window are preserved exactly when

\[
S_T(W)\subseteq S_G\quad\Longleftrightarrow\quad W<\Delta_{\neg G}.
\]

The strict inequality matters: when \(W=\Delta_{\neg G}\), the lowest excluded state is inside the inclusive target window.

### 3×3 primary study

- **24 binary spins:** 16,777,216 nominal configurations.
- **Frozen ice-rule grammar:** 2,604 admitted configurations (approximately **99.98448% contraction**).
- **Primary 1 kBT target:** 26 energy-window states; 10 admitted and **16 false exclusions**.
- **Outcome:** strong generative contraction (**G PASS**), but failure of the preregistered physical-sufficiency requirement (**P FAIL**).
- **T:** independent physical transfer not tested; **C:** not eligible for the primary physical benchmark after the P failure.

These figures are **SCR-III audited numerical results**, not SCR-IV Lean theorems. They do not imply that excluded states are physically nonexistent.

### 4×4 prospective finite-gap investigation

The 4×4 patch has **40 binary spins**, 16 constrained vertices, 780 pair couplings, and **2⁴⁰ = 1,099,511,627,776** nominal configurations. Before the real 4×4 evaluation, the program froze

\[
\delta_4<1,
\qquad 0.790439676056526\le\delta_4\le1.0333534753990623,
\]

where \(\delta_4\) is the exclusion gap normalized by the frozen \(k_BT\) convention. The prediction was prospectively frozen, but the deviation history remains integral to its interpretation: the planned synthetic feasibility campaign was incomplete, the certification audit followed the numerical run, and the earlier exploratory verdict was `GAP_INCONCLUSIVE`.

A 4×4 grammar count was **not recorded in the frozen investigation**. Any later combinatorial count must be separately cross-checked against the frozen incidence masks and documented before being promoted to an audited project result; it is not silently inserted into the frozen series here.

## SCR-IV — machine-certified finite optimization

**Closure verdict:** `SCR_IV_COMPLETE / FINITE_GAP_CERTIFIED / PREDICTIONS_PROVEN` for the **exact dyadic encoding of the frozen 4×4 model** in the recorded Lean 4.34.1 execution.

- `ground_exact_min` certifies the whole-space ground-energy value, with witness id **711243241830**.
- `nongT_exact_min` certifies the grammar-excluded minimum, with corrected witness id **711243241766**.
- `frozen_nonG_not_min` proves that the original excluded-state candidate is **not** the exact excluded-state minimum.
- `gap_exact`, `gap_pos`, `pred_lt1_true`, `pred_r2_true`, and `iv5_final` establish the exact positive gap and both registered prediction inequalities.

The certified gap is

\[
\boxed{\Delta_{\neg G}=\frac{12095447728404694790}{2^{70}}\,A>0},
\qquad \delta_4\approx0.9459172223430826.
\]

The frozen numerical excluded-state value exceeds the exact minimum by **928/2⁷⁰ A** (approximately \(7.86\times10^{-19}\,A\)). The two prediction verdicts remain unchanged. The correction is below the original solver's reported numerical resolution; its exact causal path through the solver's pruning trace was not established.

The Lean certification used **344 ground** and **804 non-grammar** proof-certificate batches (1,148 in total), exact arithmetic, proof-tree frontier coverage, and a proved-sound checker. The accepted certificates establish minimum **values**, not uniqueness or the full minimizer sets. The normalized-gap conventions use frozen constants, including the frozen binary64 value of \(A(792\,\mathrm K)\); the physical derivation of that value is not formalized in Lean. The grammar/geometric-ice-rule correspondence was differential-tested, not formally proved.

The recorded Lean runs occurred in a cloud container. **Independent WSL re-verification was explicitly waived** as a closure condition. SCR-IV's closure does **not** close the outstanding SCR-III held-out discrimination study, the synthetic feasibility campaign, or the six defaults in the SCR-III held-out freeze.

Canonical records:

- [`scr_iii_b/SCR_IV_CLOSURE_v001.md`](scr_iii_b/SCR_IV_CLOSURE_v001.md) — authoritative additive closure;
- [`scr_iii_b/GAP4_EXACT_ADDENDUM_v001.md`](scr_iii_b/GAP4_EXACT_ADDENDUM_v001.md) — exact correction, source hashes and theorem register;
- [`scr_iii_b/GAP4_RESULT_FREEZE_v001.md`](scr_iii_b/GAP4_RESULT_FREEZE_v001.md) — unmodified original numerical freeze;
- [`scr_iii_b/SCR_IV_LEAN_v005/`](scr_iii_b/SCR_IV_LEAN_v005/) — Lean theorem sources, manifests, proof certificates and recorded logs;
- [`scr_iii_b/SCR_IV_LEAN_v004/`](scr_iii_b/SCR_IV_LEAN_v004/) — certified global-optimum proof batches;
- [`scr_iii_b/GAP4_v010/`](scr_iii_b/GAP4_v010/) — frozen 4×4 numerical instance and prediction source material.

The original v001–v005 delivered ZIP archives are preserved in the separate research archive, but the published Git tree at commit `4e759d38` uses **extracted Lean package directories** and omits duplicate ZIP files. SHA-256 checksums quoted by closure records refer to the original frozen delivery files, **not** to hashes of the GitHub folders.

## Evidence hierarchy and interpretation

| Layer | Proper reading |
|---|---|
| Frozen protocols, nulls and numerical audits (SCR-I / SCR-III) | Controlled benchmark or model-specific empirical/computational findings |
| Accepted Lean theorems (SCR-IV) | Exact mathematical results for the specified encoded finite Hamiltonian |
| UNNS substrate interpretation | Research interpretation connecting generation, boundaries, admissibility and physical preservation; not itself a theorem established by these tests |

The program's central lesson is positive and discriminating: **generative structural restrictions can be made quantitatively testable, their candidate-space contraction measured, their target-preservation boundaries located, and selected finite results machine-certified**. In different benchmarks they yield different outcomes: a benchmark-specific computational gain in SCR-I-A and a measured low-energy preservation failure in SCR-III. Both are part of the scientific record.

## Repository map and usage

```text
structural_complexity_reduction/
├── README.md                       # this research overview
├── SCR_I_PREREG_v003/               # frozen SCR-I-A preregistration
├── archive/                         # historical protocols and transition evidence
├── adapters/, dashboard/, src/, scripts/, tests/
├── output/                          # SCR-I canonical results and evidence
├── scr_ii/                          # route/CSP transfer program
├── scr_iii/                         # SCR-III-A coupling/engine branch
└── scr_iii_b/                       # physical transfer, GAP4 and SCR-IV
    ├── GAP4_v010/
    ├── GAP4_RESULT_FREEZE_v001.md
    ├── GAP4_EXACT_ADDENDUM_v001.md
    ├── SCR_IV_CLOSURE_v001.md
    ├── SCR_IV_LEAN_v004/
    └── SCR_IV_LEAN_v005/
```

For the frozen SCR-I-A v003 workflow, the original commands remain available:

```text
RUN_DASHBOARD.bat       read-only dashboard / provenance view
RUN_VALIDATE_V003.bat   validate preregistration, implementation and design audit
RUN_SETUP_V003.bat      restore source lock and audit on a fresh copy
RUN_SCR_I_A_v003.bat    canonical primary runner (protects completed frozen result)
```

Do not rerun a frozen primary experiment merely to populate missing prose or charts. Preserve existing hashes, result files and historical deviations. Any new computation or interpretive correction belongs in an **additive, separately versioned** record.

## Manuscript and citation

Working manuscript: **_Structural Complexity Reduction: Generative Admissibility, Physical Exclusion Gaps, and Machine-Certified Optimization_**.

For reproducibility, link to the **fixed project commit** rather than only the moving `main` branch:

```text
https://github.com/ukbbi/UNNS/tree/4e759d38/projects/structural_complexity_reduction
```

The source archive and the scientific manuscript serve complementary purposes. For exact statements consult the corresponding frozen numerical record or Lean theorem, not a higher-level README paraphrase.

## Status boundaries

- **SCR-I-A v003:** calibrated mechanism-basin compression, enrichment and measured benchmark-specific computational gains, with representation loss at the smallest pool size.
- **SCR-III-B:** 3×3 grammar contraction confirmed; low-energy physical sufficiency fails at the primary 1 kBT window.
- **SCR-IV:** formally closed with certified exact finite minima, gap and prediction inequalities.
- **SCR-III held-out study:** open; authorization/defaults unresolved and not implied by SCR-IV closure.

This is a project-wide overview. Its purpose is to make the **whole research sequence visible without conflating the different target definitions, verification standards or verdicts**.
