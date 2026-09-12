README — DATASET C ALPHA APPLICATION V2
Cosmological Boundary Routing
Planck-Anchored Lambda-CDM

PURPOSE

This folder records the accepted version 2 alpha-deformation analysis for Dataset C.

The analysis applies the established 21-point alpha grid to the validated Planck-anchored Lambda-CDM trajectory while keeping the provisional boundary-margin channel diagnostic-only.

SCRIPT

canonical/alpha/tools/
c_planck_lcdm_alpha_apply_v2.py

INPUT

generated_trajectory/validated/
planck_lcdm_trajectory_validated.csv

ALPHA GRID

alpha minimum: 0.50
alpha maximum: 1.50
alpha points: 21
alpha radius: |alpha - 1|

Trajectory rows: 4001
Base intervals: 4000
Grid rows: 84,000

ACTIVE RESPONSE CHANNELS

ln(E) gap response          weight 0.35
total-density response      weight 0.30
curvature response          weight 0.20
composition response        weight 0.15

The provisional margin response is retained in the grid for inspection only.

It does not contribute to:

- structural_response
- phase_persistence_score
- instability_flag
- collapse_onset_radius

OUTPUTS

canonical/alpha/grids/
C_PLANCK_LCDM_alpha_grid_v2.csv

canonical/alpha/vectors/
C_PLANCK_LCDM_5d_vector_v2.csv

canonical/alpha/summaries/
C_ALPHA_APPLICATION_SUMMARY_v2.csv

canonical/alpha/normalization_review/
C_ALPHA_NORMALIZATION_REVIEW_v2.csv

NORMALIZATION STATUS

Active-channel scale review: PASS
Margin diagnostic warning: YES
Review status: comparable_active_channels

Mean normalized responses:

gap response          0.244475
density response      0.244475
curvature response    0.248765
composition response  0.993713

The provisional margin channel remains strongly scale-unstable, but it no longer contaminates the accepted vector.

ACCEPTED 5D VECTOR

mean_GR                    0.244475
var_GR                     0.022290
anisotropic_persistence    0.172874
admissibility_persistence  0.992619
collapse_onset_radius      0.45
collapse_observed          yes

GRID OUTCOME

Valid rows:       83,380
Instability rows:    620
Total rows:       84,000

Admissibility persistence:

0.992619

Stable alpha basin:

0.60 <= alpha <= 1.40

First instability:

|alpha - 1| = 0.45

Instability occurs only at:

alpha = 0.50
alpha = 0.55
alpha = 1.45
alpha = 1.50

INTERPRETATION

The Planck-anchored Lambda-CDM trajectory remains structurally persistent across nearly the entire tested alpha range.

The accepted result indicates:

- a broad stable deformation basin around alpha = 1;
- no early loss of admissibility near the canonical state;
- strong persistence through radiation-dominated evolution;
- localized sensitivity in matter- and Lambda-dominated transition intervals;
- instability only under extreme deformation.

The remaining instability is driven mainly by the composition-shift channel, especially where matter and Lambda fractions redistribute rapidly.

Therefore:

collapse_onset_radius = 0.45

must presently be interpreted as:

composition-driven alpha instability onset

and not as a literal physical collapse of the cosmological trajectory.

RELATION TO DIRECT DATASET C RESULTS

The direct preliminary ladder q_C(a) = ln(E(a)) previously showed:

- FULL_PERCOLATION in STRUC-PERC-I;
- Geometric Persistence in STRUC-I;
- Stable Structure;
- A_kappa = 1 throughout;
- maximum structural pressure rho approximately 0.291.

The alpha analysis strengthens that result by showing that the same trajectory remains admissible over 99.26 percent of the tested deformation grid.

STATUS

Alpha application v2: COMPLETE
Active-channel normalization: PASS
Margin channel: DIAGNOSTIC-ONLY
5D vector: ACCEPTED, PRELIMINARY
Dataset C alpha stage: COMPLETE

INTERPRETIVE LIMIT

This is still a Dataset C result.

It does not yet establish:

- the final shared A/B/C canonical margin;
- cosmological boundary routing;
- singularity removal;
- equivalence between classical, corrected, and observed-compatible trajectories.

Those conclusions require matched Dataset A and Dataset B construction and the final ABC bridge.

NEXT STEP

Proceed to Dataset A:

A_classical_friedmann

using the same Planck parameter anchor, sampling range, interval construction, alpha grid, response channels, and structural-vector conventions.
