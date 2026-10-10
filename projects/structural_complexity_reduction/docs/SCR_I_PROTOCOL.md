# SCR-I Protocol — Canonical v003 State

**Active frozen preregistration:** `SCR_I_PREREG_v003`  
**Primary run:** complete, 15/15 cells  
**Rerun policy:** prohibited after primary completion except from a separately versioned new preregistration.

## Paired computational design

Baseline evaluates the independent viability oracle over the nominal mechanism population. SCR first applies frozen G1→G4 and then evaluates the same downstream oracle only on survivors. Structural-filter cost is included.

## Preservation unit

The primary preservation unit is viable basin/class geometry. Candidate identity recall is secondary. The frozen requirements are defined only in `SCR_I_PREREG_v003/` and include full basin recall, minimum target survivors per basin, geometric coverage, centroid drift, unclustered-target fraction and phenotype-stratum recall.

## Null

Rate-matched random pruning uses exactly the SCR survivor count. It tests whether basin preservation is generic under equal-rate subsampling and whether SCR gives additional target selectivity.

## Cost accounting

Report candidate reduction, downstream-evaluation reduction, wall-time gain and operation-count gain. Gate short-circuit work is counted.

## Scientific integrity

- source lock is pinned;
- design-audit seeds and primary seeds are disjoint;
- v003 primary seeds are now exposed and frozen;
- UPI remains blinded and non-pruning for the primary result;
- implementation-only caching and Windows-safe checkpointing may change runtime overhead, never scientific rules or outcomes.
