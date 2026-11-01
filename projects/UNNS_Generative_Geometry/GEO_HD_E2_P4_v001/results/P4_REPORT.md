# GEO-HD-1B / E2-P4 -- P4_REPORT (v001: P4-E0..E2 coupled-target transport preflight)

Scope of this release: spec section 14 (P4-F110 preflight) and the first scoped theorems.  P4-E3 (planar CP3-A) and P4-E4 (coupled 3D census) are **not started**.

## 1. Arithmetic and relation-lattice data

x_m = 2*110^(4m)/9 -> 110^(4m)/3 for every m >= 1 (G = 9, L = 110^(2m)); verified exactly for m = 1..12, by the frozen engine for m = 1,2,3, by independent brute force for m = 1,2,3.  Primes (2,5,11) and the box [0,2m]^3 are preserved.  Source lattice a-b+c = 0 (mod 6) (index 6), target a+b+c even (index 2); Lambda_9 strictly inside Lambda_3.

## 2. Nonrectangularity

Orders mod 9 are (6,6,6) with |H_9| = 6 < 216; mod 3 (2,2,2) with |H_3| = 2 < 8.  **Both lattices are nonrectangular** (contrast: the E2-P3 witness ends at a rectangular target).

## 3. Occurrence fibres and abstract cells (m = 1)

| | source (Lambda_9) | target (Lambda_3) |
|---|---|---|
| occurrence vertices | 5 | 13 |
| oriented Graver vectors in region | 4 | 9 |
| f-vector (vertices, edges, 2-cells, 3-cells) | [5, 7, 2, 0] | [13, 45, 36, 3] |
| abstract Betti numbers | [1, 1, 0, 0] | [1, 6, 6, 0] |

This reproduces the spec 5.4 preflight counts (5 -> 13; edges 7 -> 45; 2-cells 2 -> 36; 3-cells 0 -> 3).  Abstract-cell survival: m = 1 -- all 14 source cells persist as target cells; m = 2 -- only 77 of 246 source cells persist, yet the realized union remains contained (abstract-cell loss does not imply geometric loss; supports P4-F6).

## 4. Realized geometry, m = 1

Forward: U(Lambda_9) is **contained** in U(Lambda_3) (2 source maximal cells, each covered by the 18 target maximal cells; exact subdivision certificates).  Reverse: U(Lambda_3) is **not** contained in U(Lambda_9) (witness ['13/12', '11/12', '13/12']; a violated inequality for each of the 2 source maximal cells).  Classification: **SOURCE_CONTAINED**.  The target is **not hull-covered** at m = 1: its coverage gap has 94 certified pieces, and the source union misses all of them (holes are not obstructions, P4-O1).

## 5. Certificates

results/P4_CERTIFICATES.json holds: m1_forward (containment), m1_reverse (noncontainment), m1_target_hull_cover (gap tree), n4_target_hull_cover (corner lemma, 0 gap nodes), reverse_points (m = 1,2,3) and, if the opt-in stage was run, m2_forward.  All are replayed by RUN_VERIFY.py against cell complexes re-derived from first principles (src/audit_p4.py); a tamper test rejects a perturbed witness.

## 6. Parameter family (general m)

**P4-T1.** For even n >= 4, U(E_3,[0,n]^3) = conv F = { z in [0,n]^3 : sum z >= 2 } (cube tiling by 2-cubes + one exact corner certificate at n = 4 + cell monotonicity).  **P4-T2.** For every m >= 1, U(Lambda_9,Q_m) is strictly inside U(Lambda_3,Q_m): SOURCE_CONTAINED (m = 1 direct; m >= 2 from P4-T1 and the inherited coverage-gap reduction).  Containment does not fail beyond a threshold and does not become more complicated for this family; P4-F5 (failure persisting under box growth) is not exercised because no failure occurs.
  Direct exact run m = 2 (independent of the theorem): forward CONTAINED (21 source / 712 target maximal cells, 223 s).
  Direct m >= 3: UNAVAILABLE_COST.

## 7. Planar CP3-A

**OPEN.**  Only the reclassification was done: the 266 E2-P2 ENLARGE rows split 40 inherited / 164 rectangular / 14 hollow-box / 48 sub-threshold (unchanged); the expanded E2-P3 corpus has 846 ENLARGE rows in the two open classes, all CONTAINED (finite evidence, not a theorem).  No new search was run.

## 8. Essential higher-dimensional findings

None new.  Inherited controls: E2-P1 (parity -> Z^3) and E2-P3 (2,7,13), and the infinite family recorded as E2-P3 Addendum 004 (rectangular target; all 8 tested instances pass).  P4-F110 shows that a transport between two nonrectangular lattices in 3D can be fully contained; it provides no coupled-target obstruction.

## 9. Falsification table (spec 11)

| ID | Result |
|---|---|
| P4-F1 | NOT falsified by P4-F110 (strict enlargement between nonrectangular lattices preserved realized geometry for all m); not a general claim |
| P4-F2 | not tested |
| P4-F3 | not tested |
| P4-F4 | **Supported** at m = 1: the target has certified holes, yet no source cell enters them |
| P4-F5 | not exercised (no failure in the family) |
| P4-F6 | **Supported** at m = 2: abstract cells disappear (77 of 246 persist) while the realized union stays contained |

## 10. Novelty assessment and unresolved obligations

All results are elementary.  P4-T1 is a 3D analogue of the planar GEO-I v012 hull-coverage regime; P4-T2/P4-C1 follow from it with the coverage-gap reduction.  No literature search beyond the frozen project sources; **C3 is not claimed.**  Unresolved: CP3-A, P4-T3 (other coupled families, box-growth classification), P4-T4 (essential 3D coupled obstruction), prior-art audit, direct m >= 3, GEO-I post-v012 commit identification.

## 11. Verification

Shards verified without failure so far (this build): S0, S1, S2, S3, S4, S5, S6, S7.  Builder and audit have the same author.  Shell-limit design: S0-S3, S5 are short; S4 (corner replay) is the heavy shard.
