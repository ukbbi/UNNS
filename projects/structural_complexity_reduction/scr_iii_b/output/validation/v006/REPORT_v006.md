# REPORT_v006 — Energy-Window Feasibility and Non-Tautology Gate

**Verdict:** `FEASIBILITY_PASS`

This is a feasibility preflight. It is **not** a physical-transfer result, issues no primary SCR verdict, and preregisters nothing. Frozen v005 hashes: test F1 = PASS.

## Combinatorial contraction (not computational gain)

| Patch | Spins | Nominal | Grammar | Contraction | Levels | Δ_nonice (J) | first non-ice level |
|---|---|---|---|---|---|---|---|
| 1x1 | 4 | 16 | 6 | 0.62500 | 4 | 9.529e-21 | 2 |
| 2x2 | 12 | 4096 | 82 | 0.97998 | 275 | 1.041e-20 | 2 |

## 1x1 windows (first levels up to first failure +1)

| k | W (J) | W / A | level size | ice in level | |S_T| | FN | preservation | capacity L/m | class |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 2 | 2 | 2 | 0 | 1.0000 | 3.000 | GROUND_ONLY_TRIVIAL |
| 1 | 6.214e-21 | 0.006155 | 4 | 4 | 6 | 0 | 1.0000 | 1.000 | ICE_EXCITED_PRESERVED_BELOW_FIRST_NONICE (target == S_G: TAUTOLOGY_RISK) |
| 2 | 9.529e-21 | 0.009438 | 8 | 0 | 14 | 8 | 0.4286 | 0.429 | FIRST_NONICE_THRESHOLD_EXPECTED_FAILURE |
| 3 | 2.569e-20 | 0.02544 | 2 | 0 | 16 | 10 | 0.3750 | 0.375 | DEFECT_ACCESSIBLE_FAILURE |

**Regime C (expected-failure control), 1x1:** at level 2 (W = 9.529e-21 J) the target gains 8 non-ice states, all excluded by the grammar (false exclusions = 8). First excluded: id 1 `+---`, E = 0 J, E−E0 = 9.529e-21 J, violated vertices [0].
Target before: 6 states; after: 14; kept by grammar: 6 (ids in `REPORT_v006.json`).

## 2x2 windows (first levels up to first failure +1)

| k | W (J) | W / A | level size | ice in level | |S_T| | FN | preservation | capacity L/m | class |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 2 | 2 | 2 | 0 | 1.0000 | 41.000 | GROUND_ONLY_TRIVIAL |
| 1 | 7.984e-21 | 0.007909 | 8 | 8 | 10 | 0 | 1.0000 | 8.200 | ICE_EXCITED_PRESERVED_BELOW_FIRST_NONICE |
| 2 | 1.041e-20 | 0.01032 | 16 | 0 | 26 | 16 | 0.3846 | 3.154 | FIRST_NONICE_THRESHOLD_EXPECTED_FAILURE |
| 3 | 1.275e-20 | 0.01263 | 8 | 8 | 34 | 16 | 0.5294 | 2.412 | DEFECT_ACCESSIBLE_FAILURE |

**Regime C (expected-failure control), 2x2:** at level 2 (W = 1.041e-20 J) the target gains 16 non-ice states, all excluded by the grammar (false exclusions = 16). First excluded: id 406 `-++-+--++---`, E = -3.048e-20 J, E−E0 = 1.041e-20 J, violated vertices [1].
Target before: 10 states; after: 26; kept by grammar: 10 (ids in `REPORT_v006.json`).

## Non-tautology assessment

- **1x1: NO_NONTRIVIAL_WINDOW.** For W < Delta_nonice every target state is ice-admissible by the definition of Delta_nonice, so preservation is a spectral fact of the frozen Hamiltonian, established here by exhaustive enumeration; no analytic bound for larger patches is derived in v006. Windows beyond ground: none.
- **2x2: NONTRIVIAL_PRESERVATION_CANDIDATE.** For W < Delta_nonice every target state is ice-admissible by the definition of Delta_nonice, so preservation is a spectral fact of the frozen Hamiltonian, established here by exhaustive enumeration; no analytic bound for larger patches is derived in v006. Windows beyond ground: [(1, 10, 82)].

Preservation below Δ_nonice is a *spectral fact of the frozen Hamiltonian* established by enumeration; it is guaranteed-aligned, not an independent proof of transfer. Windows whose target set equals S_G are flagged and excluded from the nontrivial count.

## Structural nulls (2×2, exploratory)

- 2x2|DEGREE_PRESERVING_SWAP: {"valid_nulls": 1000, "capacity_comparable": 1000, "mean_contraction": 0.978291015625, "real_contraction": 0.97998046875, "frac_same_survivor_set": 0.0, "frac_preserve_ground": 0.074, "frac_as_far_as_real": 0.0, "comparable_frac_preserve_ground": 0.074, "comparable_frac_as_far_as_real": 0.0, "frac_preserve_last_ice_window": 0.0, "comparable_frac_preserve_last_ice_window": 0.0}
- 2x2|FREE_RANDOM_4SET: {"valid_nulls": 1000, "capacity_comparable": 981, "mean_contraction": 0.9801552734375, "real_contraction": 0.97998046875, "frac_same_survivor_set": 0.0, "frac_preserve_ground": 0.023, "frac_as_far_as_real": 0.0, "comparable_frac_preserve_ground": 0.023445463812436288, "comparable_frac_as_far_as_real": 0.0, "frac_preserve_last_ice_window": 0.0, "comparable_frac_preserve_last_ice_window": 0.0}

Controls: unchanged-incidence reproduces the real grammar (N1); perturbed-incidence differs (N2); energies and targets unchanged (N3). Seeds are `20261010|family|index`; acceptance rates in `FEASIBILITY_v006.json`.

## Computational cost (separate from contraction)

- 1x1: 16 configs, 6 pair interactions per evaluation; grammar pass 4.36e-05 s vs energy pass 8.11e-05 s (2.73 µs vs 5.07 µs per state); grammar can precede energy: True.
- 2x2: 4096 configs, 66 pair interactions per evaluation; grammar pass 2.82e-03 s vs energy pass 4.88e-02 s (0.69 µs vs 11.93 µs per state); grammar can precede energy: True.
- constructive S_G generation 1x1: 6 grammar states, 30 search nodes vs 16 nominal states.
- constructive S_G generation 2x2: 82 grammar states, 690 search nodes vs 4096 nominal states.
- constructive S_G generation 3x3: 2604 grammar states, 25786 search nodes vs 16777216 nominal states.

## Test summary

| ID | Test | Evidence | Status |
|---|---|---|---|
| F1 | Frozen v005 code and outputs equal the hashes recorded in the local MANIFEST_v005.json (read-only comparison) | STATIC_FILE_HASH | **PASS** |
| C1 | Exhaustive 1x1/2x2 enumeration reproduces frozen v005: ice-state counts, ground ids, ground energy (J), degeneracy; incidence grammar == v005 geometric ice rule on every state | FROZEN_V005_EVALUATOR_PYTHON | **PASS** |
| C2 | Independent vertex typing (source ENWS table re-implemented) agrees with the incidence grammar on every state (Types I,II <=> 2-in/2-out) | SOURCE_DERIVED_INDEPENDENT_PYTHON | **PASS** |
| C3 | Level grouping: degeneracy tolerance (relative 1e-9 of max|E|) is far below the smallest genuine level spacing; no level mixes ice and non-ice states | SOURCE_DERIVED_INDEPENDENT_PYTHON | **PASS** |
| W1 | Every unique energy-level transition evaluated; level-based target sets equal direct threshold H<=E0+W on both sides of every transition | EXHAUSTIVE_ENUMERATION | **PASS** |
| W2 | Window metrics are internally consistent (|S_T∩S_G|+FN=|S_T|, FN non-decreasing with W, ground window preserved) | EXHAUSTIVE_ENUMERATION | **PASS** |
| W3 | Capacity L/m >= 1 for every exactly preserved nonempty window | EXHAUSTIVE_ENUMERATION | **PASS** |
| W4 | Regime C expected-failure control: preservation first fails exactly at the first window admitting a non-ice state (control success, not a preflight failure) | EXHAUSTIVE_ENUMERATION | **PASS** |
| X1 | Constructive (backtracking) generation of S_G equals brute-force S_G (1x1, 2x2) and is order-independent (also 3x3 count; no energies computed for 3x3) | EXHAUSTIVE_ENUMERATION | **PASS** |
| N1 | Unchanged-incidence control reproduces the real grammar exactly (null implementation check) | STRUCTURAL_NULL_MONTE_CARLO | **PASS** |
| N2 | Deliberately perturbed-incidence control changes the surviving set (null implementation check) | STRUCTURAL_NULL_MONTE_CARLO | **PASS** |
| N3 | Hamiltonian energies and physical target sets are bit-identical before and after null generation | STRUCTURAL_NULL_MONTE_CARLO | **PASS** |
| N4 | Valid structural nulls generated for 2x2 in both families with seeds, rejection reasons and acceptance rates logged (1x1 is structurally degenerate: see logs) | STRUCTURAL_NULL_MONTE_CARLO | **PASS** |
| K1 | Computational feasibility measurements recorded separately from structural contraction (runtime, memory, evaluations, pair interactions, environment) | MEASUREMENT | **PASS** |
| T1 | Non-tautology assessment completed for every tested patch (six mandated questions answered with evidence) | ANALYSIS | **PASS** |

## Unresolved / out of scope

- No downstream solver is defined; C_downstream and any net work saving are unmeasured (contraction is not a computational gain).
- E2 charged local estimator not implemented (requirements only): no frozen source defines it.
- Only 1x1 and 2x2 are exhaustively evaluated; 3x3 has a grammar count only (no energy windows).
- Single reference temperature 792 K (energy ordering is T-invariant by v005; windows scale with A(T)).
- Window boundaries here are exploratory, discovered by enumeration; primary windows must be frozen separately before any primary comparison.
- Nothing here extends to the published 24x24 arrays, v1.01 geometry-specific parameters, size disorder or the unmodified simulator.
- Null comparisons are exploratory; 1x1 admits no degree-preserving rewiring.

## Next step

If the verdict is FEASIBILITY_PASS: draft `SCR_III_B_SPEC_v001.md` and a separately frozen primary preregistration (windows frozen *before* any primary comparison). Nothing is frozen by this package.
