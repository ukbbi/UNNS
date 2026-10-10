# FREEZE_v008 — SCR-III-B Solver Implementation Gate

**Project:** UNNS Structural Complexity Reduction (SCR)  
**Branch:** SCR-III-B — Generative Admissibility / Physical Sufficiency  
**Freeze record date:** 2026-10-10  
**Canonical status:** `SCR-III-B / PREFLIGHT_v008 / SOLVER_IMPLEMENTATION_GATE_PASS / LOCALLY_REPRODUCED`  
**Classification:** Implementation-only preflight; not a primary G/P/T/C result.

## 1. Reproduction and evidence

The uploaded `PREFLIGHT_v008.zip` reports `SOLVER_IMPLEMENTATION_GATE_PASS` with no mandatory failures. The user additionally executed the following commands from the established Windows D: project via Ubuntu/WSL:

```bash
python3 scr_iii_b/solvers/validate_v008.py
python3 scr_iii_b/solvers/test_v008.py
```

The user-supplied terminal screenshot shows:
- `SOLVER_IMPLEMENTATION_GATE_PASS`;
- `mandatory_failures: []`;
- **10/10 named validation checks PASS** (`F1`, `G0`, `S1`–`S4`, `K1`, `S6`–`S8`);
- **7/7 unit tests PASS**;
- clean return to the shell prompt.

An earlier attempted path, `scr_iii_b/solver_gate/`, failed with `No such file or directory`; that was an instruction/path error, **not** a failed scientific test. The correct package path is `scr_iii_b/solvers/`.

The local reproduction is screenshot-confirmed. This document does not claim direct access to or independent checksum measurement of the Windows D: drive.

## 2. Implemented solver definitions and verified behaviour

- **B0:** optimized full nominal-space Gray-code energy scan, returning the complete physical target set.
- **B1:** exact Hamiltonian-aware branch-and-bound. Its lower bound was tested as admissible on **530** partial assignments and matched a separately written Python expression.
- **G1:** nominal-space grammar filtering; outputs exactly `S_T ∩ S_G` (subject to the solver's documented ground-energy handling).
- **G2:** constructive grammar enumeration with incremental physical pair-energy updates; outputs the same grammar-restricted target set as G1.
- **Checks:** B0=B1 and G1=G2 on public 1×1 and 2×2 patches at reference and near-threshold windows, plus synthetic mixed-sign, ferro-, antiferro- and all-degenerate instances. Known false-exclusion counts match v006.

The package also records conservative proposed tie handling on synthetic near-tie cases. **The tie policy was tested, not frozen.**

### Frozen reference integrity

The package-reported F1 hash check covered **33 frozen code/output files across v005–v007**, with **zero mismatches**. No historical code, original Dryad source, validation output or GitHub mutation is authorized by this record.

## 3. Outcome-blind 3×3 acceptance run

At the **already-public W=0 anchor**, all four implementations returned the same two complementary grammar-admissible ground states and the physical reference E₀ matched v007. Output and operation counts were deterministic across five repeats.

The v008 guard refused 3×3 W>0 calls without `--unblind-after-freeze`. Its invocation audit records no successful 3×3 W>0 run and no excited-state spectrum or primary target outcomes. The guard-refusal test does not constitute scientific unblinding.

**The 3×3 spectrum is only low-energy-window outcome-blinded, not completely spectrum-blind:** v007's published drift and `V4.relative_to_scale` already permit an approximate upper-spectrum inference. This disclosure remains part of the v007 record.

## 4. Cost ledger — 3×3, W=0 only

Packaged builder medians of five single-thread repetitions (not identical to a future primary run):

| Architecture | Median wall time | Nodes or states |
|---|---:|---:|
| B0 Gray-code | 0.326 s | 16,777,216 |
| G1 grammar scan | 0.1116 s | 16,777,216 |
| G2 constructive grammar | 0.0003277 s | 25,786 |
| B1 exact branch-and-bound | 0.00009402 s | 4,232 |

The package records operations and peak RSS separately. These timings are **acceptance-only W=0 measurements**, not a charged W>0 speedup claim. At W=0 the Hamiltonian-aware B1 is faster than G2; that ordering cannot be extrapolated to broader physical windows.

## 5. Public gap diagnostics and epistemic limits

At `W = k_B T_ref`, with `T_ref = 792 K`, public patches show:

| Patch | Δ_nonG / k_BT | W/Δ_nonG | Exact preservation |
|---|---:|---:|---|
| 1×1 | 0.871 | ≈1.15 | FAIL |
| 2×2 | 0.952 | ≈1.05 | FAIL |

For the frozen grammar and a fully specified exact finite energy target, preservation is equivalent to `W < Δ_nonG`, subject to the separately specified conservative numerical tie rule. These public results warn that a 3×3 preservation failure is possible; **they do not reveal its W>0 outcome**.

H-T's old beyond-gap requirement was logically unsatisfiable. Transfer is **NOT_TESTED** pending a separately specified independent physical target-family study. G contraction is supported by previous finite-patch enumeration; P at 3×3 W>0 and charged C remain untested.

## 6. Outstanding preregistration decisions

The following are deliberately **not frozen** by v008:

1. Primary window constant and rule.
2. Tie-policy constant, energy-tolerance and endpoint policy.
3. Numerical decision thresholds and uncertainty method for G/P/C.
4. Null seeds, sample sizes, invalid-null handling and candidate ordering.
5. Charged E2 exact local-energy comparator design and certification.
6. Runtime, memory, warmup and repeat limits.
7. Global reversal `Z₂` symmetry policy (not used by the v008 solvers).
8. Common independently certified E₀ policy for all primary solvers; avoid contamination from grammar-restricted `Ê₀`.

The included `scr_iii_b/drafts/` SPEC and PREREG amendments remain **UNFROZEN working documents**. No primary run may be authorized merely from this implementation gate.

## 7. Archive provenance

- Upload: `PREFLIGHT_v008.zip`
- Archive SHA-256: `6840460165cac08f58108d257f5fbc96bfb83a4427bb5e48bca5dd9d705ab991`
- Verified against the archive's own `MANIFEST_v008.json`: **12/12 listed code/output files match their SHA-256 digests**.
- Scientific report: `scr_iii_b/output/validation/v008/REPORT_v008.md`
- Machine-readable results: `REPORT_v008.json`, `TESTS_v008.json`
- Cost records: `COST_LEDGER_v008.json` and `.csv`
- Draft change log: `scr_iii_b/drafts/DRAFT_AMENDMENTS_v008.md`

The package's per-run timing-file hashes do not need to remain identical after local re-execution. The package hash above identifies the uploaded v008 artifact, not every extracted local file.

## 8. Freeze action and next milestone

Place this independent record at:

`structural_complexity_reduction/FREEZE_v008.md`

Keep v005–v008 code and outputs **unchanged by research policy**. This document is an additive scientific freeze record, not an operating-system read-only permission change. Future corrections must be explicit, versioned and cross-referenced; GitHub remains untouched.

**Next milestone:** `PREFLIGHT_v009` — preregistration closure gate, resolving E2, tie policy, seeds, null budgets, target-independent thresholds and certified common E₀ without revealing 3×3 W>0 results.

**Final status:** `SOLVER_IMPLEMENTATION_GATE_PASS / LOCALLY_REPRODUCED / PRIMARY_NOT_AUTHORIZED`.
