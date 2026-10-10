# CTX_SCR

## Project

**Structural Complexity Reduction (SCR)**

## Current canonical state

- Active benchmark: `SCR-I-A`
- Active preregistration: `SCR_I_PREREG_v003`
- Engine: `SCR_I_ENGINE_v003`
- Optimization: `SCR_I_V003_OPT_v001` (implementation-only cache/resume)
- Primary status: **COMPLETE — 15/15 cells**
- Frozen outcome label: **`STRUCTURAL_COMPRESSION_CONFIRMED_ABOVE_REPRESENTATION_FLOOR`**

## Central question

> Can UNNS structural admissibility reduce the effective candidate/search space before downstream computation while preserving the independently defined structural object that must remain represented?

For v003 the preservation unit is viable **basin/class geometry**, not individual target identity.

## Primary finding

Across the frozen primary run:

- median candidate contraction ≈ **92.03%**;
- basin recall = **1.0 in every cell**;
- 10/15 cells satisfy all frozen preservation requirements;
- all five failures occur at N=2,500 and are `REPRESENTATION_LOSS`, not basin annihilation;
- all N=10,000 and N=40,000 cells are `STRUCTURAL_COMPRESSION_PRESERVED`;
- median end-to-end time gain ≈ **8.39×**;
- survivor viable-target concentration ≈ **99.15%**, versus ≈ **52.52%** nominally;
- target recall is enriched ≈ **1.889×** over rate-matched random pruning.

Important null result: at large N, rate-matched random pruning also preserves the broad basin geometry well. The supported distinctive claim is therefore **preservation + selective viable-target enrichment**, not preservation alone.

## Version history that must remain understood

- v001 primary was not run: its frozen target oracle was source-level empty under the flat-baseline guard.
- v002 primary was not run: design-only audit showed candidate-level recall ≈0.147–0.153, revealing candidate identity as the wrong preservation unit.
- v003 changed only the preservation unit to basin/class geometry while retaining the frozen generator, G1→G4 and independent viability oracle.

Earlier preregistrations are archived under `archive/prereg/`.

## Canonical output locations

```text
output/                         raw v003 primary outputs
output/v003_phase1/             design-preservation audit
output/checkpoints/             completed primary checkpoint
output/reports/v003/            consolidated scientific record
output/exports/v003/            final machine-readable record
archive/history/                decisive v001/v002 transition evidence
```

## Next research move

Do not tune or rerun SCR-I-A v003. The primary seeds are exposed and the result is frozen. A next experiment should move to a genuinely different benchmark/domain (SCR-II) or perform a preregistered secondary analysis such as the still-blinded UPI association.
