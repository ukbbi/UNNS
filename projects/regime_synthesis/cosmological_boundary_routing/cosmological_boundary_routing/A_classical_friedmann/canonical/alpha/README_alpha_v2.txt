README — DATASET A ALPHA APPLICATION V2
Cosmological Boundary Routing
Classical Friedmann Singular Approach

PURPOSE

This step applies the same version-2 alpha deformation convention used for Dataset C to the validated Dataset A contraction trajectory.

The analysis preserves the original path order from a = 1 toward a = 1e-8 and retains signed H < 0 as trajectory metadata.

SCRIPT

canonical/alpha/tools/
a_classical_friedmann_alpha_apply_v2.py

INPUT

generated_trajectory/validated/
classical_friedmann_approach_validated.csv

ALPHA GRID

alpha minimum: 0.50
alpha maximum: 1.50
alpha points: 21
alpha radius: |alpha - 1|

ACTIVE RESPONSE CHANNELS

ln(E) gap response          weight 0.35
total-density response      weight 0.30
curvature response          weight 0.20
composition response        weight 0.15

The provisional margin response remains diagnostic-only and does not affect structural response, persistence, instability, or collapse onset.

OUTPUTS

canonical/alpha/grids/
A_CLASSICAL_FRIEDMANN_alpha_grid_v2.csv

canonical/alpha/vectors/
A_CLASSICAL_FRIEDMANN_5d_vector_v2.csv

canonical/alpha/summaries/
A_ALPHA_APPLICATION_SUMMARY_v2.csv

canonical/alpha/normalization_review/
A_ALPHA_NORMALIZATION_REVIEW_v2.csv

RUN

Open a terminal in:

A_classical_friedmann/canonical/alpha/tools/

Run:

python a_classical_friedmann_alpha_apply_v2.py

EXPECTED RELATION TO DATASET C

The direct sorted A and C ladders are identical because both use the same set of ln(E) values.

The alpha stage retains Dataset A's contraction path, negative signed H, increasing density, increasing curvature, and approach toward the numerical cutoff.

INTERPRETIVE LIMIT

The endpoint a = 1e-8 is a numerical cutoff, not a sampled singularity.

Any reported instability onset is an alpha-deformation threshold in the selected representation, not a direct observation of a cosmological singularity.
