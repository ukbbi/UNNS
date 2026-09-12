README — DATASET B ALPHA APPLICATION V2
Cosmological Boundary Routing
Effective LQC Bounce

PURPOSE

This step applies the version-2 alpha deformation analysis to the complete direction-preserving Dataset B path:

contraction
→ exact bounce
→ expansion

The expansion-only ladder is not used for this stage.

SCRIPT

canonical/alpha/tools/
b_lqc_bounce_alpha_apply_v2.py

INPUT

canonical/ladder/
lqc_bounce_response_path_preliminary.csv

BOUNCE-SAFE RESPONSE COORDINATE

q_B = asinh(H_signed / H0)

This coordinate:

- remains finite at H = 0;
- preserves contraction and expansion signs;
- passes continuously through the exact bounce;
- avoids replacing the bounce with an arbitrary epsilon.

ACTIVE CHANNELS

signed-flow gap response   weight 0.35
total-density response    weight 0.30
curvature response        weight 0.20
composition response      weight 0.15

The provisional margin channel is diagnostic-only.

ALPHA GRID

alpha minimum: 0.50
alpha maximum: 1.50
alpha points: 21
alpha radius: |alpha - 1|

OUTPUTS

canonical/alpha/grids/
B_LQC_BOUNCE_alpha_grid_v2.csv

canonical/alpha/vectors/
B_LQC_BOUNCE_5d_vector_v2.csv

canonical/alpha/summaries/
B_ALPHA_APPLICATION_SUMMARY_v2.csv

canonical/alpha/normalization_review/
B_ALPHA_NORMALIZATION_REVIEW_v2.csv

RUN

Open a terminal in:

B_lqc_bounce/canonical/alpha/tools/

Run:

python b_lqc_bounce_alpha_apply_v2.py

INTERPRETIVE NOTE

Because Dataset B contains an exact turning point, its bounce-safe signed-flow coordinate differs from the magnitude-only ln(E) coordinates used in the direct A and C ladders.

The resulting Dataset B vector is suitable for full-path bounce analysis and later orientation-sensitive bridge construction. Direct numerical equality with the A/C magnitude-only vectors is not expected.

The provisional margin remains excluded from structural response and collapse classification.
