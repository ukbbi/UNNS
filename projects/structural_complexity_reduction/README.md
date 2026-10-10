# Structural Complexity Reduction (SCR)

**UNNS Substrate research project**  
**Current canonical benchmark:** `SCR-I-A v003`  
**Current status:** `STRUCTURAL_COMPRESSION_CONFIRMED_ABOVE_REPRESENTATION_FLOOR`

## Core question

> Can a frozen UNNS structural filter reduce an effective candidate/search space before downstream computation while preserving the independently defined structural object that matters?

For SCR-I-A v003, the preservation unit is the independently identified viable **mechanism basin/class**, not individual candidate identity.

## Canonical result

The completed primary run contains **15/15 preregistered cells** across five independent primary seeds and three pool sizes (`2,500`, `10,000`, `40,000`).

- median candidate reduction: **92.03%**;
- minimum basin recall: **1.000**;
- median end-to-end time gain: **8.39×**;
- median operation-count gain: **6.73×**;
- median viable-target fraction in the nominal pool: **52.52%**;
- median viable-target fraction among SCR survivors: **99.15%**;
- median target-recall enrichment over rate-matched random pruning: **1.889×**.

Scale outcome:

| Pool size | Frozen verdict pattern | Median geometric coverage |
|---:|---|---:|
| 2,500 | 5/5 `REPRESENTATION_LOSS` | 86.98% |
| 10,000 | 5/5 `STRUCTURAL_COMPRESSION_PRESERVED` | 98.13% |
| 40,000 | 5/5 `STRUCTURAL_COMPRESSION_PRESERVED` | 99.83% |

The result therefore supports structural compression **above a finite representation floor**. Basin preservation by itself is not unique to SCR at large N; the stronger distinctive result is basin preservation combined with strong enrichment of independently viable mechanisms.

## Canonical records

Human-readable consolidation:

```text
output/reports/v003/SCR_I_V003_RESULT_RECORD.md
output/reports/v003/SCR_I_V003_ANALYSIS.md
output/reports/v003/SCR_I_V003_NULL_ANALYSIS.md
```

Machine-readable final record:

```text
output/exports/v003/SCR_I_V003_FINAL.json
```

Raw primary outputs remain in `output/` for reproducibility.

## Frozen preregistration

The active preregistration is:

```text
SCR_I_PREREG_v003/
```

Earlier v001/v002 preregistrations are preserved read-only under `archive/prereg/`; they are not active code. v001 exposed an impossible target-oracle guard, and v002 exposed candidate identity as the wrong preservation unit for this calibration.

## Active commands

```text
RUN_DASHBOARD.bat       local read-only dashboard / provenance view
RUN_VALIDATE_V003.bat   validate preregistration, implementation and design audit
RUN_SETUP_V003.bat      re-establish source lock + design audit on a fresh copy
RUN_SCR_I_A_v003.bat    canonical primary runner; refuses rerun after completed frozen result
```

## Claim boundary

SCR-I-A v003 does **not** establish a complexity-class result, P=NP, a universal asymptotic speedup, or unique basin preservation over random pruning. It establishes a controlled benchmark result: large structural contraction, preserved basin/class representation above sufficient sampling density, strong viable-target enrichment, and net computational gain under the frozen calibration.
