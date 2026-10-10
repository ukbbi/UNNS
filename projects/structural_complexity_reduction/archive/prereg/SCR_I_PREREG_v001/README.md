# SCR-I Preregistration v0.0.1

**Package:** `SCR_I_PREREG_v001`  
**Project:** Structural Complexity Reduction (SCR)  
**Program:** SCR-I  
**Benchmark:** SCR-I-A — Mechanism-Space Reduction Calibration  
**Status:** FROZEN BEFORE SCR-I-A EXECUTION  
**Date:** 2026-10-06

## Purpose

This package freezes the first executable scientific protocol for Structural Complexity Reduction before outcome-bearing SCR-I-A runs are performed.

SCR-I asks whether a structural filter can reduce a candidate/search space **before** a conventional downstream evaluation, while preserving the target result and producing a net reduction in computational work after the filter cost is counted.

SCR-I-A is deliberately a **calibration benchmark** derived from the existing UNNS Phase P3/P4 mechanism-space program. It is intended to validate the accounting, falsification, null-control, and preservation machinery. It is not, by itself, evidence that SCR generalizes to unrelated NP-hard, physical, or spectral problems.

## Frozen primary question

> Can the pinned P3/P4 structural gate set reduce the number of mechanism candidates that require downstream Mode-C evaluation while preserving every independently defined Mode-C positive target in the frozen benchmark corpus and outperforming rate-matched non-structural pruning after filter cost is included?

## Package contents

- `PREREG.md` — complete preregistration.
- `BENCH_A.md` — benchmark construction and paired-arm design.
- `GATES.md` — frozen G1–G4 predicates and use restrictions.
- `METRICS.md` — primary and secondary metrics.
- `NULLS.md` — matched null and adversarial controls.
- `DECISION_RULES.md` — positive, negative, invalid, and indeterminate outcomes.
- `UPI_BLIND.md` — UPI is diagnostic-only in SCR-I-A.
- `SOURCE_LOCK.md` — pinned upstream repository sources and blob SHAs.
- `RUN_PLAN.md` — exact execution order and freeze discipline.
- `config/scr_i_prereg_v001.json` — machine-readable frozen configuration.
- `schema/result_schema.json` — required result-record schema.
- `scripts/validate_prereg.py` — internal consistency validator.
- `scripts/prereg_hash.py` — SHA-256 manifest generator.
- `scripts/RUN_VALIDATE.bat` — Windows validation entry point.
- `MANIFEST.md` and `SHA256SUMS.txt` — package inventory and hashes.

## Placement

Place this directory at:

```text
structural_complexity_reduction/docs/SCR_I_PREREG_v001/
```

Do not overwrite the existing project-level SCR-I documents. This preregistration specializes them for Benchmark A.
