# GEO-HD-1B / E2-P3 v001 — Realized Geometric Transport: Coverage, Obstruction, and Higher-Dimensional Persistence

**Organizing principle:** Coverage-Gap Reduction  U ⊆ U′ ⇔ U ∩ (H′ ∖ U′) = ∅.  All verdicts below are exact (rational arithmetic) and every verdict that is stated as a proof-grade fact carries a certificate checked by code that shares nothing with the engine.

## 1. What was learned (short)

1. **Controls reproduce independently.**  A (21⁸/5→21⁸/4): U ⊊ U′, target inherited from G12-T8 and exactly hull-covered.  B (55¹²/27→55¹²/18): U ⊊ U′ although the target is a *hollow box* with a nonempty coverage gap (6 gap pieces, area 6) — every source cell avoids it.  C (2·110⁴/3→110⁴): U ⊄ U′, witness (2/3,2/3,2/3), with a violated inequality for each of the 7 target cells.
2. **Planar audit (9788 FIELD-I rows, k = 2).**  Verdicts: {'CONTAINED': 9788}.  **No planar containment failure** occurs in scope.  Target classes (all relations): {'RESIDUAL_SUBTHRESHOLD_BOX': 2997, 'RESIDUAL_D1_RECTANGULAR': 5515, 'RESIDUAL_EXCEPTIONAL_HOLLOW_BOX': 130, 'INHERITED_G12T8': 1146}.
3. **What is inherited vs residual.**  Of the 266 previously sampled E2-P2 ENLARGE rows, classes: {'INHERITED_G12T8': 40, 'RESIDUAL_D1_RECTANGULAR': 164, 'RESIDUAL_EXCEPTIONAL_HOLLOW_BOX': 14, 'RESIDUAL_SUBTHRESHOLD_BOX': 48}.  Inherited (G12-T8) rows were additionally checked to be *exactly* hull-covered (1146 rows, 0 exceptions).
4. **New elementary theorem (P3-T3).**  For a *rectangular* target lattice the uncovered region is exactly the open corner cube; U ⊆ U′ iff no source cell meets it; Graver edges never do; in k = 2 containment is unconditional (resolves CP3-A for all d′ = 1 targets, 5515 planar rows), in k = 3 any obstruction is carried by a 2-cell.  The even-sum family is classified completely: U ⊄ U′ ⇔ max Q̃ ≥ 2.
5. **Three coordinates.**  S1 scope (2698 rows): 77 failures, all with target Z³ (E2-P1 family); essential in the sense of full coordinate support, 2-dimensional cell and face-irreducibility: 77.  S2 (rectangular nontrivial targets, 3954 candidate rows): predictor failures 459, exact failures 40.  Gate: **3D_WITNESS_PASS**.
5b. **Essential 3D witness, both lattices nontrivial (S2).**  30 exact-certified FIELD-I failures with source and target lattices both nontrivial, full coordinate support, 2-dimensional failing cell, all three coordinate-face restrictions CONTAINED.  Smallest listed: primes [2, 7, 13], box [2, 2, 3], b=9 -> b'=3 (x = 370853389088/9), witness ['4/3', '5/6', '2/3'].  These are *counterexamples to unconditional containment U ⊆ U′* (CP3-A is for planar targets; not a statement about k=2).  The same-author caveat applies; independent verification is by src/certificate_check.py only.
6. **Corrections recorded (append-only):** E2-P2 theorem wording (P2-T1, P2-TF1(v)); GEO-I v012 overlap; and a **new defect found here**: E2-P2's planar sampling window was the square [0,q₁]², incomplete when q₁ < q₂; all 326 E2-P2 geometry verdicts were recomputed — **0 changed**.

## 2. Gates

| Gate | Outcome |
|---|---|
| SOURCE_PASS | True |
| GEOMETRY_PASS | True |
| PLANAR_AUDIT_COMPLETE | True |
| 3D_WITNESS | 3D_WITNESS_PASS |
| CP3_A | OPEN |
| PLANAR_THEOREM_PASS | True |
| 3D_THEOREM_PASS | SCOPED_RECTANGULAR_TARGETS |
| C3 | SCOPED_THEOREM_ONLY |
| EXACT_PASS | True |

`EXACT_PASS` confirms the experiment, not novelty.  `PLANAR_THEOREM_PASS` is claimed **only** for the rectangular-target class (proved, elementary); CP3-A for hollow/sub-threshold d′ ≥ 2 targets is **OPEN**.  `3D_THEOREM_PASS` is scoped to rectangular targets.  `C3` = SCOPED_THEOREM_ONLY (see results/P3_THEOREM_AUDIT.md).

## 3. Controls

| Control | transition | classes | verdict | independent check |
|---|---|---|---|---|
| A | E2-P2/A: 21^8/5 -> 21^8/4 | INHERITED_G12T8 | CONTAINED | {'ok': True, 'reason': 'ok'} |
| B | E2-P2/B: 55^12/27 -> 55^12/18 | RESIDUAL_EXCEPTIONAL_HOLLOW_BOX | CONTAINED | {'ok': True, 'reason': 'ok'} |
| C | E2-P1: 2*110^4/3 -> 110^4 | rectangular Z^3 target | NOT_CONTAINED | {'ok': True, 'reason': 'ok'} |

Control C also verifies the *specified* witness (2/3,2/3,2/3) as its own certificate; the engine's own first witness is ['3/4', '3/4', '3/4'].

## 4. Planar corpus (P3-E2)

Scope: base {'bmax': 130, 'k': 2, 'note': "reproduces the E2-P2 corpus (582 rows with source and target lattices nontrivial) and ADDS target-trivial rows (Lambda' = Z^2), which E2-P2 skipped under 'trivial_lattice'", 'odd': False, 'primes': [2, 3, 5, 7, 11, 13, 17], 'qmax': 4}, expansion {'bmax': 400, 'k': 2, 'odd': False, 'primes': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41], 'qmax': 6}.  Skipped states (explicit): {"base": {"UNAVAILABLE_order_product_large": 266, "UNAVAILABLE_target_denominator_large": 71, "coordinates_change": 6108, "empty_fibre": 18808, "equal_lattices": 1116, "source_trivial_lattice": 320}, "expansion": {"UNAVAILABLE_coordinates_undecided": 494, "UNAVAILABLE_order_product_large": 3379, "UNAVAILABLE_target_denominator_large": 5621, "coordinates_change": 190564, "empty_fibre": 622968, "equal_lattices": 20854, "source_trivial_lattice": 3996}}

| relation | target class | verdict | hull-covered | rows |
|---|---|---|---|---|
| ENLARGE | INHERITED_G12T8 | CONTAINED | True | 6 |
| ENLARGE | INHERITED_G12T8 | CONTAINED | True | 1129 |
| ENLARGE | RESIDUAL_D1_RECTANGULAR | CONTAINED | False | 5515 |
| ENLARGE | RESIDUAL_EXCEPTIONAL_HOLLOW_BOX | CONTAINED | False | 116 |
| ENLARGE | RESIDUAL_SUBTHRESHOLD_BOX | CONTAINED | False | 166 |
| ENLARGE | RESIDUAL_SUBTHRESHOLD_BOX | CONTAINED | True | 218 |
| ENLARGE | RESIDUAL_SUBTHRESHOLD_BOX | CONTAINED | True | 346 |
| INCOMPARABLE | INHERITED_G12T8 | CONTAINED | True | 11 |
| INCOMPARABLE | RESIDUAL_EXCEPTIONAL_HOLLOW_BOX | CONTAINED | False | 14 |
| INCOMPARABLE | RESIDUAL_SUBTHRESHOLD_BOX | CONTAINED | False | 1 |
| INCOMPARABLE | RESIDUAL_SUBTHRESHOLD_BOX | CONTAINED | True | 482 |
| SHRINK | RESIDUAL_SUBTHRESHOLD_BOX | CONTAINED | True | 1784 |

Residual (hollow / sub-threshold, d′ ≥ 2) rows: 3127 total — 297 with a nonempty target gap (containment holds although uncovered hull regions exist), 2830 exactly hull-covered, 0 gap-undecided.

## 5. Three-coordinate search (P3-E3)

S1 table:

| relation | verdict | both nontrivial | essential | rectangular target | rows |
|---|---|---|---|---|---|
| ENLARGE | CONTAINED | False | None | True | 1047 |
| ENLARGE | CONTAINED | True | None | False | 720 |
| ENLARGE | CONTAINED | True | None | True | 180 |
| ENLARGE | NOT_CONTAINED | False | False | True | 77 |
| INCOMPARABLE | CONTAINED | True | None | False | 90 |
| INCOMPARABLE | CONTAINED | True | None | True | 11 |
| SHRINK | CONTAINED | True | None | False | 573 |

S2 (rectangular nontrivial targets, q ∈ [2,4]³): states screened 291168; candidate rows 3954; predictor table {"(False, 'CONTAINED')": 480, "(True, 'CONTAINED')": 3015, "(True, 'NOT_CONTAINED')": 459}; exact engine on 120 rows; predictor/exact agreement {'CONTAINED|CONTAINED': 80, 'NOT_CONTAINED|NOT_CONTAINED': 40}; mismatches [].

Pure-lattice scan (target Z³, index ≤ 8, boxes {1,2}³): 2870 (Λ̃,Q̃) pairs, 22 failures, corner-cube predictor agrees on every pair: True.

**Both-nontrivial failures found:** 30 (see results/P3_COUNTEREXAMPLES.json).

## 6. Independence and shared code

* Builder: `exact_containment.py`, `coverage_gap.py`, `planar_residual.py`, `coupled_3d.py` + the hash-pinned E2-P2 modules in `src/p2/` (FIELD-I step, lattice relation, region Graver set, abstract complex).
* Independent: `certificate_check.py` (imports nothing from the builder) and `audit_p3.py` + `p2/geometry_audit.py` (brute-force arithmetic, own cell enumeration, own maximal-cell reduction).  Certificates are *proposed* by the builder and *accepted only* by the independent verifier against independently derived cells.
* Same author/session wrote both sides; the independence is of code, not of people.  A novelty-grade claim would need a human proof review.
* Not independently re-derived: Graver sets of the large pinned E2-P2 modules are re-derived by `geometry_audit.graver` (brute force) in RUN_VERIFY; GEO-I v012 theorems are cited, not re-proved (P3-L1 is re-proved).

## 7. Resource limits

```json
{
 "arithmetic": "exact rational (fractions.Fraction); no floating point enters any verdict",
 "determinism": "states visited in the fixed order (prime tuple, box, parity, b); rows evaluated in that order; no randomness",
 "global": {
  "3d_node_limit": 30000,
  "containment_node_limit": 20000,
  "gap_node_limit": 50000,
  "order_product_limit": 20000,
  "target_denominator_limit": 2000000,
  "unavailable_rule": "a state exceeding a limit is recorded under its own UNAVAILABLE_* skip reason and never silently dropped"
 },
 "lattice_model_scan": {
  "boxes": "{1,2}^3",
  "index_max": 8,
  "k": 3,
  "note": "pure sublattices of Z^3 (HNF); NOT claimed FIELD-I realizable",
  "target": "Z^3"
 },
 "planar_base": {
  "bmax": 130,
  "k": 2,
  "note": "reproduces the E2-P2 corpus (582 rows with source and target lattices nontrivial) and ADDS target-trivial rows (Lambda' = Z^2), which E2-P2 skipped under 'trivial_lattice'",
  "odd": false,
  "primes": [
   2,
   3,
   5,
   7,
   11,
   13,
   17
  ],
  "qmax": 4
 },
 "planar_expansion": {
  "bmax": 400,
  "k": 2,
  "odd": false,
  "primes": [
   2,
   3,
   5,
   7,
   11,
   13,
   17,
   19,
   23,
   29,
   31,
   37,
   41
  ],
  "qmax": 6
 },
 "three_d_S1": {
  "bmax": 120,
  "k": 3,
  "note": "numerator exponents 2q_i or 2q_i+1 (the E2-P1 control has 2^5)",
  "odd": true,
  "primes": [
   2,
   3,
   5,
   7,
   11,
   13
  ],
  "qmax": 2
 },
 "three_d_S2_rectangular_targets": {
  "bmax": 150,
  "exact_engine_budget": "all predictor NOT_CONTAINED rows + every 10th predictor CONTAINED row (cap 400)",
  "filter": "target lattice rectangular and nontrivial, q_i >= ord_{b'}(p_i) for all i",
  "k": 3,
  "odd": true,
  "primes": [
   2,
   3,
   5,
   7,
   11,
   13
  ],
  "q_range": [
   2,
   4
  ]
 },
 "version": "E2-P3 v001"
}
```

