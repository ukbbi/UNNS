# FREEZE_v009 — SCR-III-B Preregistration Closure Gate

**Project:** UNNS Structural Complexity Reduction (SCR)  
**Branch:** SCR-III-B — Generative Admissibility / Physical Sufficiency  
**Record date:** 2026-10-10  
**Canonical status:** `SCR-III-B / PREFLIGHT_v009 / PREREG_CLOSURE_GATE_PASS / LOCALLY_REPRODUCED`  
**Scope:** Technical readiness and prospective decision-register preparation only.  
**Primary experiment:** **NOT AUTHORIZED**. Neither the primary SPEC nor PREREG is frozen.

## 1. Local Ubuntu/WSL reproduction

After the environment initially stopped at `ModuleNotFoundError: No module named 'numpy'`, NumPy was made available and the user executed, from the existing Windows D:-hosted project root under Ubuntu/WSL:

```bash
python3 scr_iii_b/prereg_gate/validate_v009.py
python3 scr_iii_b/prereg_gate/test_v009.py
```

The user's terminal screenshots confirm:

- Validation verdict: **`PREREG_CLOSURE_GATE_PASS`**.
- `mandatory_failures: []`.
- All **23 named validation checks** shown in the JSON result are `PASS`.
- Validator elapsed time: **143.2 seconds**.
- **8/8 unit tests passed** (`Ran 8 tests in 0.099s`).
- Clean return to the shell prompt.

**Count clarification:** a prior chat reply said 25/25 validation checks. The uploaded `REPORT_v009.json` contains **23 named test statuses**; the uploaded manifest contains **25 separately hashed code, draft and output artifacts**. These counts refer to different things and must not be conflated. This freeze uses the report's verifiable 23 named checks.

The local execution is evidenced by user-supplied screenshots, not by direct inspection of the user's D: drive. This file itself does not claim to have rerun v009 locally.

## 2. Scientific and operational achievements

The uploaded v009 report records successful testing of:

- **E0 reference:** a common, hash-checked v007 physical ground energy for all solvers, with independent Gray-code and branch-and-bound recertification on the disclosed W=0 anchor. E0 ≈ **−9.271994751803727 × 10⁻²⁰ J** at 792 K.
- **E2:** certified truncated pair-interaction remainder bounds, exact public/synthetic target-set comparisons, fallback cases and charged cost accounting.
- **Numerical policy:** proposed tolerance hierarchy and conservative inclusive-endpoint treatment, with synthetic near-boundary tests.
- **Nulls:** deterministic, valid **1,000 N1 + 1,000 N2** grammar-incidence nulls with rejection accounting and outcome-blind feasibility checks.
- **Candidate ordering / Z₂:** deterministic traversal and global-reversal identities; the proposed primary benchmark does not exploit a Z₂ quotient.
- **Cost accounting:** B0, B1, G1, G2 and E2 ledgers, resource feasibility, balanced repeated timing, and separate E0-certification cost.
- **Outcome blindness:** real 3×3 W>0 evaluation and the real exclusion-gap computation were refused; the recorded real 3×3 invocation scope was W=0 anchor or grammar-only work.

The existing v007 `V4.relative_to_scale` disclosure permits inference of an approximate **upper** spectral scale. Accordingly, the preflight is **3×3 low-energy-outcome blinded**, not completely spectrum-blind.

## 3. Proposed values recorded — not ratified

The uploaded decision register contains prospective recommendations, **all awaiting separate ratification**:

| Decision | Proposal |
|---|---|
| Physical patch | 3×3 free boundary, 24 spins |
| Primary window | W = k_B T_ref, T_ref = 792 K |
| Sensitivity windows | W = 0.5 k_B T_ref and 2 k_B T_ref |
| E2 retained interactions | **75%** strongest |K_ij|, tie-broken by index (recommended after synthetic-only cost tests; earlier 25% remains historical proposal) |
| Tolerance | τ = 10⁻⁹ Σ|K_ij|; conservative inclusive threshold |
| Gray-code drift | Relative tolerance 10⁻¹⁰ (to be prospectively approved, not retroactive v007 freeze) |
| Null master seed | 20261010 |
| Nulls | 1,000 each of N1 and N2 |
| Timing | 3 warmups, 15 timed rounds, single thread, balanced interleaving |
| Limits | 30 min per algorithm arm, 2 GiB resident memory |
| Z₂ | Disabled in primary, sensitivity permitted |
| G threshold | 99% contraction plus exact constructive membership |
| P threshold | FN=0 on complete exact physical target |
| T | NOT_TESTED; separate future protocol required |
| C | Conditional on P and complete output; proposed ≥1.20× charged gain against optimized B0, B1/E2 separately reported |

The thermal window has known prior-information sensitivity: at W=k_BT, **1×1 and 2×2 both fail preservation** under the published physical gaps. The 3×3 W>0 physical outcome remains undisclosed. No value may be changed after viewing that outcome.

## 4. Uncertainty procedure — unresolved at freeze-record stage

The v009 synthetic correlated-timing simulations found **only approximately 78–85% empirical coverage** for the proposed nominal 95% moving-block bootstrap interval with 15 rounds. This is **not a calibrated 95% interval**, regardless of the low simulated false-pass rates at selected ratios.

**Do not ratify the H-C uncertainty rule unchanged merely because the technical gate passed.** Final primary preregistration must either:

1. replace or recalibrate the method to meet its stated coverage standard using outcome-blind synthetic/pilot evidence, or
2. adopt an explicitly conservative decision policy and state exactly which uncertainty/false-positive claims it supports, without mislabeling it as 95% coverage.

The decision register also leaves null-separation significance, potential B1/E2 interpretive thresholds, exact boundary status and final freeze authorization open. These require explicit decisions before primary unblinding.

## 5. Scope of the gate verdict

`PREREG_CLOSURE_GATE_PASS` means **the technical implementation and readiness checks passed**. It does **not** mean:

- the primary 3×3 W>0 target was evaluated;
- G, P, T, or C primary hypotheses passed;
- the primary window, E2 setting, seeds or statistical decision rule are ratified;
- the primary SPEC/PREREG has been frozen;
- the W>0 execution guard may be removed;
- UNNS physical transfer or computational acceleration has been established.

The earlier v005–v008 scientific records remain untouched. Frozen-source integrity in the package and local gate is reported as passing; do not change historical files to resolve new concerns.

## 6. Archive provenance and integrity

- Uploaded package: `PREFLIGHT_v009.zip`
- Archive SHA-256: `07a4dcaff69f5390a8e3d5678fc6f7c8bb61dcf63d3791e0375aa49bf65073c7`
- `MANIFEST_v009.json` entries verified against actual uploaded ZIP member bytes: **25/25 match**.
- Scientific report: `scr_iii_b/output/validation/v009/REPORT_v009.md` and `.json`
- Validation outcomes: `scr_iii_b/output/validation/v009/TESTS_v009.json`
- Closure decisions: `scr_iii_b/output/validation/v009/DECISION_REGISTER_v009.md`
- Blindness record: `scr_iii_b/output/validation/v009/BLINDNESS_AUDIT_v009.json`
- Draft amendments: `scr_iii_b/drafts/` (explicitly **UNFROZEN**)

Timing and output hashes are builder-run records; separately reproduced local timing reports can differ without invalidating the scientific verdict. The archive fingerprint above identifies the exact uploaded package examined in this freeze record.

## 7. Freeze placement and next authorized action

Store this **additive standalone record** at:

`structural_complexity_reduction/FREEZE_v009.md`

alongside `FREEZE_v005.md` through `FREEZE_v008.md`, **not inside** the already generated v009 validation directory.

The scientific freeze records the v009 preflight verdict and evidence; it does not set OS read-only permissions. Retain all prior code and outputs as historical records. Corrections require a separately versioned amendment. **GitHub remains unchanged.**

**Next step:** ratify the v009 decision register, explicitly resolve/calibrate the H-C uncertainty rule, prepare the final SPEC/PREREG with their SHA-256 hashes, and create a separate primary-protocol freeze record. Only afterward may a further explicit authorization permit any 3×3 W>0 primary run.

**Final recorded state:**  
`V009_LOCALLY_REPRODUCED / TECHNICAL_GATE_PASS / PRIMARY_DOCUMENTS_UNFROZEN / PRIMARY_NOT_AUTHORIZED`.
