# SCR-I v003 Result Record

**Project:** Structural Complexity Reduction (SCR)  
**Benchmark:** SCR-I-A  
**Preregistration:** `SCR_I_PREREG_v003`  
**Engine:** `SCR_I_ENGINE_v003`  
**Optimization layer:** `SCR_I_V003_OPT_v001`  
**Primary seeds:** 2026101001, 2026101002, 2026101003, 2026101004, 2026101005  
**Pool sizes:** 2,500, 10,000, 40,000  
**Run status:** `COMPLETE` — 15/15 primary cells completed  
**Source archive SHA-256:** `5dd600ae2a86b69c9a357399a90c77e15172209e9611b7a8891b3332eeb534fe`

## Frozen primary question

Can a frozen UNNS structural gate chain reduce mechanism-candidate space while preserving the independently identified viable **mechanism-basin structure**?

The preservation unit in v003 is the basin/class, not individual candidate identity.

## Frozen primary preservation criteria

A primary cell qualifies as structurally preserved only when all frozen basin-level criteria pass:

- basin recall = 1.000;
- each baseline target basin retains at least 20 target-positive SCR survivors;
- at least 95% of each baseline basin lies within normalized distance 0.25 of a surviving target-positive representative from that same basin;
- normalized survivor-centroid drift from the baseline basin centroid ≤ 0.125;
- unclustered target fraction ≤ 0.05;
- all adequately populated target phenotype strata `(regime_base, family, composition)` remain represented.

Candidate-level target recall is diagnostic only.

## Primary outcome

The primary run completed all 15 preregistered seed × pool-size cells.

- `STRUCTURAL_COMPRESSION_PRESERVED`: **10/15**
- `REPRESENTATION_LOSS`: **5/15**
- Median candidate-space reduction: **92.03%**
- Reduction range: **91.40%–92.68%**
- Minimum basin recall: **1.000**
- Median end-to-end time gain: **8.39×**
- Median operation-count gain: **6.73×**

| Pool | Preserved | Representation loss | Median reduction | Min basin recall | Median geometric coverage | Median time gain |
|---:|---:|---:|---:|---:|---:|---:|
| 2,500 | 0/5 | 5/5 | 92.36% | 1.000 | 86.98% | 9.22× |
| 10,000 | 5/5 | 0/5 | 92.03% | 1.000 | 98.13% | 8.39× |
| 40,000 | 5/5 | 0/5 | 92.02% | 1.000 | 99.83% | 7.88× |

## Scale transition

The result is scale-dependent.

At **N = 2,500**, all five cells retain basin identity (`basin_recall = 1.0`) but fail one or more frozen representation criteria. Median geometric coverage is only 86.98%; the worst cell falls to 65.38%. One seed produces two baseline basins and leaves only 2 target-positive survivors in the smaller basin. Accordingly, all five N=2,500 cells receive `REPRESENTATION_LOSS`.

At **N = 10,000** and **N = 40,000**, all ten cells pass the complete frozen preservation criteria while retaining only about 8% of the original candidates. These ten cells receive `STRUCTURAL_COMPRESSION_PRESERVED`.

## Selective enrichment

The independent target oracle marks a median **52.52%** of the unfiltered population as viable.

After G1→G4 filtering, a median **99.15%** of surviving candidates are target-positive.

The median candidate-level target recall is only **15.04%**, as expected for an aggressive ~92% contraction, but this recall is **1.889×** the median rate-matched random-pruning recall.

In all 15 primary cells, SCR target recall exceeds the maximum target recall observed among that cell's matched random-null replicates.

## Gate contraction profile

For the 40,000-candidate gate audit, the mean first-rejection shares are:

- G1: **60.83%**
- G2: **22.34%**
- G3: **13.60%**
- G4: **3.23%**

Short-circuit evaluation requires only **1.785** gate evaluations per candidate on average at N=40,000.

## Cell-level record

| Seed | Pool | Survivors | Reduction | Basin recall | Coverage | Drift | Target recall | Time gain | Verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2026101001 | 2,500 | 215 | 91.40% | 1.000 | 90.65% | 0.0893 | 15.97% | 8.80× | `REPRESENTATION_LOSS` |
| 2026101001 | 10,000 | 797 | 92.03% | 1.000 | 98.13% | 0.1055 | 15.07% | 8.51× | `STRUCTURAL_COMPRESSION_PRESERVED` |
| 2026101001 | 40,000 | 3,173 | 92.07% | 1.000 | 99.88% | 0.0940 | 14.97% | 7.88× | `STRUCTURAL_COMPRESSION_PRESERVED` |
| 2026101002 | 2,500 | 184 | 92.64% | 1.000 | 84.04% | 0.1059 | 13.73% | 9.86× | `REPRESENTATION_LOSS` |
| 2026101002 | 10,000 | 732 | 92.68% | 1.000 | 97.33% | 0.0996 | 13.92% | 8.80× | `STRUCTURAL_COMPRESSION_PRESERVED` |
| 2026101002 | 40,000 | 3,181 | 92.05% | 1.000 | 99.83% | 0.0942 | 14.95% | 7.80× | `STRUCTURAL_COMPRESSION_PRESERVED` |
| 2026101003 | 2,500 | 187 | 92.52% | 1.000 | 65.38% | 0.1418 | 14.52% | 9.22× | `REPRESENTATION_LOSS` |
| 2026101003 | 10,000 | 816 | 91.84% | 1.000 | 98.14% | 0.0876 | 15.48% | 7.79× | `STRUCTURAL_COMPRESSION_PRESERVED` |
| 2026101003 | 40,000 | 3,207 | 91.98% | 1.000 | 99.80% | 0.0930 | 15.16% | 7.73× | `STRUCTURAL_COMPRESSION_PRESERVED` |
| 2026101004 | 2,500 | 203 | 91.88% | 1.000 | 86.98% | 0.0907 | 15.14% | 9.14× | `REPRESENTATION_LOSS` |
| 2026101004 | 10,000 | 754 | 92.46% | 1.000 | 97.73% | 0.1082 | 14.32% | 8.39× | `STRUCTURAL_COMPRESSION_PRESERVED` |
| 2026101004 | 40,000 | 3,194 | 92.02% | 1.000 | 99.84% | 0.0999 | 15.04% | 7.98× | `STRUCTURAL_COMPRESSION_PRESERVED` |
| 2026101005 | 2,500 | 191 | 92.36% | 1.000 | 89.73% | 0.0651 | 14.47% | 9.58× | `REPRESENTATION_LOSS` |
| 2026101005 | 10,000 | 824 | 91.76% | 1.000 | 98.29% | 0.0927 | 15.52% | 8.03× | `STRUCTURAL_COMPRESSION_PRESERVED` |
| 2026101005 | 40,000 | 3,232 | 91.92% | 1.000 | 99.78% | 0.0944 | 15.24% | 7.90× | `STRUCTURAL_COMPRESSION_PRESERVED` |

## Frozen interpretation

**Established by this benchmark:**  
At sufficiently large sampling density (N≥10,000 in the frozen v003 design), the UNNS G1→G4 gate chain reduces candidate space by about 92% while preserving the independently identified viable basin/class representation under the frozen criteria, and does so with a strong enrichment of independently viable targets relative to rate-matched random pruning.

**Not established:**  
This benchmark does not establish a computational-complexity-class result, universal asymptotic speedup, or unique basin-preservation advantage over random subsampling. At large N, rate-matched random nulls also preserve the broad basin geometry well.

## Run integrity note

The machine-readable progress record states `COMPLETE` with 15/15 cells. The terminal wrapper later returned exit code 1 after printing the completed records; this does not alter the completed primary outputs and is treated as a launcher return-code defect rather than a scientific-run failure.
