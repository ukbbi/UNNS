# SCR-I v003 Null Analysis

## Purpose

The frozen N1 control retains exactly the same number of candidates as G1→G4 but selects them randomly. The purpose is to determine which parts of the v003 result are generic consequences of subsampling and which are structurally selective.

The primary SCR result does not require beating N1. N1 determines whether an additional Level-B claim of structural selectivity is warranted.

## 1. Target-recall enrichment

| Pool | SCR target recall (median) | Null target recall (median) | Enrichment | SCR geom. coverage | Null geom. coverage |
|---:|---:|---:|---:|---:|---:|
| 2,500 | 14.52% | 7.62% | 1.899× | 86.98% | 73.36% |
| 10,000 | 15.07% | 7.99% | 1.899× | 98.13% | 98.00% |
| 40,000 | 15.04% | 8.03% | 1.888× | 99.83% | 100.00% |

Across the 15 primary cells:

- median enrichment of SCR candidate-level target recall over the matched-null median: **1.889×**
- enrichment range: **1.836×–2.000×**
- SCR target recall exceeds the **maximum** null target recall in **15/15 cells**.

With 30 null replicates, the conservative one-sided empirical bound is `(0+1)/(30+1) = 0.0323`.  
With 100 null replicates, the corresponding bound is `(0+1)/(100+1) = 0.00990`.

Thus, every cell places the observed SCR target enrichment beyond the sampled matched-random null distribution.

## 2. Basin recall

Basin recall is 1.0 for SCR in every primary cell.

Matched random subsampling also commonly preserves the single broad basin. Basin recall therefore does not by itself distinguish SCR from random pruning in this benchmark.

This is an important limitation: the positive claim should not be phrased as “random pruning destroys the basin while UNNS preserves it.”

## 3. Geometric coverage

At N=2,500, SCR generally retains more of the basin geometry than the rate-matched null median, but both are below the frozen 95% preservation threshold.

At N=10,000, SCR and the random nulls have nearly identical median geometric coverage:

- SCR median: **98.13%**
- matched-null median: **98.00%**

At N=40,000, random pruning slightly exceeds SCR in raw geometric coverage:

- SCR median: **99.83%**
- matched-null median: **100.00%**

This shows that the broad basin is highly redundant at large N.

## 4. Centroid drift

Random matched pruning generally yields smaller centroid drift than SCR at N=10,000 and N=40,000.

This does not invalidate the v003 structural-compression verdict because SCR remains within the frozen centroid-drift bound. It does, however, prevent the claim that SCR gives the best geometric approximation of the basin.

The most defensible interpretation is that SCR is **selective** rather than geometrically neutral: it concentrates independently viable candidates in particular regions of the viable basin while preserving the basin/class representation.

## 5. Null-supported conclusion

The nulls separate two effects:

### Generic redundancy effect
At sufficiently large N, an ~8% subsample can preserve the global geometry of the single broad target basin even when selected randomly.

### Structural-selection effect
G1→G4 selects target-positive mechanisms at roughly **1.89×** the target-recall rate of matched random pruning, and this enrichment exceeds every sampled null replicate in all 15 cells.

Therefore the strongest null-supported SCR-I-A v003 claim is:

> Basin preservation at large N is not unique to structural filtering, but the combination of strong compression, preserved basin/class representation, and strong enrichment of independently viable targets is structurally selective relative to rate-matched random pruning.

## 6. Claim boundary

N1 supports a **Level-B selective-enrichment claim**, not a universal optimality claim. The benchmark contains one dominant viable basin and does not test whether the same selectivity persists in domains containing multiple well-separated viable classes.
