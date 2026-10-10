# SCR Reuse Map

Earlier UNNS projects are source references. SCR does not rewrite their canonical results.

## 1. Direct structural-complexity ancestors

### `canonical/chamber_lii_phase_P₃/`
**Use:** mechanism-space contraction.

Reusable ideas:
- pre-gate vs post-gate mechanism counts;
- explicit gate set;
- quantified reduction;
- structural selection without external fitness.

### `canonical/chamber_liii_phase_P₄/`
**Use:** adversarial relaxation / hidden-class search.

Reusable ideas:
- relax gates after contraction;
- search rejected/residual space;
- distinguish selective pruning from over-restriction;
- local completeness rather than global claims.

### `canonical/chambers_li-lv-structural-arc/`
**Use:** factorization → selection → contraction → closure → persistence architecture.

## 2. Gate methodology

### `canonical/axis_v_admissibility_gate/`
**Use:** invariant/falsifier/signature discipline.

Reusable:
- orthogonality tests;
- deterministic gates;
- preregistration;
- no solution-dependent invariant;
- gate-specific complexity/cost accounting.

## 3. Canonicalization and adversaries

### `projects/regime_synthesis/predictive_admissibility_search/`
**Use:** CLE / PAS methods.

Reusable:
- domain adapters;
- canonical structural representation;
- persistence metrics;
- adversarial ladders;
- shuffled-real controls;
- failed-falsification preservation.

## 4. Core structural instruments

### STRUC-I
Use where an ordered ladder representation is legitimate.

Measures perturbative admissibility; do not reinterpret it as a generic solver heuristic.

### STRUC-PERC-I
Use where gap-space connectivity is relevant.

Keep its percolative meanings distinct from STRUC-I admissibility.

## 5. Zero-contraction / distinction control

### `projects/UNNS_COMMON_REFINEMENT/UNNS_ADMISSIBILITY_PERCOLATION/`

Useful because the preserved corpus contains systems with different independent algebraic annotations while STRUC-I saturates at full admissibility.

SCR can use such a corpus to test whether its machinery invents pruning where the chosen admissibility instrument does not distinguish candidates.

## 6. Representation sensitivity

### `projects/regime_synthesis/non-crossability/`

Reusable:
- raw vs Delta representation comparisons;
- representation-induced fragmentation;
- recovery tests;
- boundary monitoring.

SCR lesson:
apparent exclusion may be representational and must be tested under alternate admissible charts.

## 7. Search-state instrumentation

### `canonical/least-divergence_selection_universality/`

Reusable:
- explicit `statesExplored`;
- stable endpoint counts under changing exploration volume;
- search-topology measurement.

SCR lesson:
candidate-space contraction and actual states explored are separate endpoints.

## 8. Correlation vs generativity

### `canonical/chamber_xlix/`

Reusable:
- Discovery Mode;
- Conditioned Sampling Mode.

SCR lesson:
correlation with rejected states is not sufficient to justify a pruning gate.

## 9. Failure preservation

### `standards/UNNS-ADM/`

Reusable:
- immutable admissibility records;
- negative-space preservation;
- auditable failure reasons.

SCR should preserve every rejected candidate with its gate and reason code.

## 10. Instability diagnostic

### `docs/unns_paradox_index/`
### Chamber XXIII

Reusable:
- scalar/fuller UPI diagnostics;
- instability profiles;
- fold/closure/collapse diagnostics.

SCR-I role:
secondary diagnostic only.

## 11. Refinement and falsification model

### `projects/UNNS_YM_STRUCTURAL_SPECTRAL/`

Reusable:
- preregistered refinement axes;
- matched physical/adversarial processing;
- explicit failure conditions;
- preserving negative outcomes;
- separating structural observations from stronger physical claims.

## 12. Older complexity material

### `docs/UNNS_Operational_Grammar/UNNS_on_NP_Hardness/`

Historical relevance:
- early idea of effective state-space collapse;
- Repair / Normalization as equivalence-class reduction.

SCR policy:
do **not** inherit unvalidated claims that exponential search is converted to polynomial complexity.
SCR replaces those statements with measurable paired benchmarks and full cost accounting.

## 13. Old performance benchmark

### `unns-benchmark-suite.html`

Historical/demo value only.

Do not use as SCR evidence without redesign because several comparisons relabel conventional or altered algorithms as “UNNS” and do not isolate structural filtering as the only experimental variable.

SCR requires the same downstream solver in both arms.
