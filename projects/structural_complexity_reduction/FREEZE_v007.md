# FREEZE_v007 — SCR-III-B Exact 3×3 Verifier Feasibility

**Record date:** 2026-10-10  
**Canonical milestone:** `SCR-III-B / PREFLIGHT_v007 / EXACT3_VERIFIER_FEASIBLE / LOCALLY_REPRODUCED`  
**Status:** Historical preflight freeze record; **no primary physical-transfer experiment authorized**  
**Scope:** Frozen Dryad SPMMC v1.00 finite free-boundary Hamiltonian (v005); v006 feasibility results retained as frozen history.

## Evidence and reproduction

The uploaded `PREFLIGHT_v007.zip` includes source, JSON/Markdown reports, and `MANIFEST_v007.json`. Its builder reports a complete direct and Gray-code 3×3 scan and three deterministic repeats. The user separately ran these commands from their D:-hosted project using Ubuntu/WSL:

```bash
python3 scr_iii_b/exact3/validate_v007.py
python3 scr_iii_b/exact3/test_v007.py
```

The supplied terminal screenshot shows `EXACT3_VERIFIER_FEASIBLE`, empty `mandatory_failures`, all **seven named validation checks PASS**, **four of four unit tests PASS**, and return to the shell prompt. This document records screenshot-confirmed reproduction, not independent remote access to the user's D: drive.

The archived F1 report checked **24 frozen v005/v006 code/output files** against their local manifests without mismatches. No edits to those files are authorized.

## Findings

- Exact 3×3 nominal space: **16,777,216** configurations (24 spins); original physical energies evaluated by a direct scan and a Gray-code incremental implementation.
- 1×1 and 2×2 cross-checks at all recorded energy-level thresholds match frozen Python; on 3×3, **2,002 seeded configurations** match frozen physical-energy calculations.
- Grammar survivors on 3×3: **2,604**, consistent among brute-force scanning, frozen Python constructive generation, and C++ constructive generation; constructive traversal uses **25,786 nodes**.
- Only reported 3×3 target anchor: **W=0**, E₀ ≈ **−9.271994751803727 × 10⁻²⁰ J**, **two** ground configurations, **zero** false exclusions. This is **guaranteed alignment**, not independent transfer.
- v007 deliberately withholds the 3×3 excitation spectrum and outcomes for **every W>0 window**, leaving a prospectively specified primary window possible.
- Packaged component costs (single-thread): direct scan **9.56 s**, incremental Gray-code scan **0.2783 s**, grammar scan **0.0893 s**, constructive generator **0.0001638 s**, peak RSS **131 MB**. These are component timings, not end-to-end speedups.
- User-local screenshot: direct scan **5.44 s**, Gray-code scan **0.1450 s**, grammar scan **0.0806 s**, peak RSS approximately **131 MB**. The local machine's timings differ; the scientific verdict agrees.
- 4×4 exact scan estimate ≳**8.45 single-thread hours** under a simple extrapolation; **not measured** or demonstrated. A streaming verifier would be required.

## V4 deviation: post-hoc numerical criterion

The first v007 run failed its imported **1e−12 relative incremental-drift** criterion: measured relative drift was approximately **1.79093e−11**. The builder then adopted **≤1e−10 relative drift**, derived as at least a factor of ten below the **1e−9** energy-level degeneracy grouping tolerance, and reran the preflight.

**This change is post hoc and must remain disclosed.** Direct energies, not Gray-code accumulated values, govern target membership; no change to target sets is reported. The revised criterion passes for this preflight, but does not acquire prospective status for a future preregistered experiment. Independently freeze numerical tolerances before primary execution.

## Limits and nonclaims

- Exact verification is computationally feasible for **3×3**, but exact target preservation for **W>0** has **not** been disclosed or established.
- The 2-in/2-out grammar's 2,604 surviving states are a sharply contracted *grammar* space, **not** a proof that all other physical states are non-generable.
- No independent physical-transfer claim, no conventional-solver comparison, no charged speedup, no primary verdict.
- The solver-selection memo is **advisory and unfrozen**. Two downstream documents remain **drafts**, pending separately prospective design decisions.

## Provenance

- Input package: `PREFLIGHT_v007.zip`
- SHA-256 of uploaded package: `d01896324d73823fadbfc19870d7d35a68d8c976cd3ed2aeb97c234174e86e8c`
- Internal code/output entries verified against `MANIFEST_v007.json`: **9/9 matching**.
- Internal source report: `scr_iii_b/output/validation/v007/REPORT_v007.md`
- Internal test evidence: `scr_iii_b/output/validation/v007/TESTS_v007.json`
- Note: reported timing/output hashes describe the builder's run; local WSL results may legitimately have different timing hashes.

## Freeze policy and next step

Keep this record at `structural_complexity_reduction/FREEZE_v007.md`, outside the frozen `scr_iii_b/output/validation/v007/` directory. Historical v005, v006 and v007 results remain read-only by policy; this Markdown record does **not** set filesystem permissions. Any scientific correction requires an additive versioned amendment. GitHub stays untouched.

**Next authorized action:** revise `SCR_III_B_SPEC_v001.md` and `SCR_III_B_PREREG_v001.md` so *generative-grammar contraction* and *independent physical admissibility* are the principal questions, with measured computational gain a distinct downstream consequence. Both documents remain **unfrozen**, and primary execution remains prohibited until a prospective freeze.
