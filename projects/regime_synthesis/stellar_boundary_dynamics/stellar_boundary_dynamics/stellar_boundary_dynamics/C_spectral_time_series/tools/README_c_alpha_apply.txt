README_c_alpha_apply.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase C — Alpha Application / Deformation-Grid Script

SCRIPT:
tools/c_alpha_apply.py

PURPOSE:
Apply α-deformation to real Phase C spectral STRUC-PERC-I canonical inputs and
generate object-level α grids and 5D vectors.

INPUT:
struc_perc_i/canonical_inputs/C1_SN1993J_struc_perc_input.csv
struc_perc_i/canonical_inputs/C2_SN2012aw_struc_perc_input.csv

OUTPUT:
alpha_application/grids/C1_SN1993J_alpha_grid.csv
alpha_application/grids/C2_SN2012aw_alpha_grid.csv

alpha_application/vectors/C1_SN1993J_5d_vector.csv
alpha_application/vectors/C2_SN2012aw_5d_vector.csv

alpha_application/summaries/C_ALPHA_APPLICATION_SUMMARY.csv
alpha_application/summaries/C_5D_VECTOR_SUMMARY.csv

RECOMMENDED RUN:
Open PowerShell in:

C_spectral_time_series/

Then run:

python tools/c_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application

OPTIONAL ALPHA GRID:
Default:
alpha_min = 0.50
alpha_max = 1.50
alpha_points = 21

Custom example:

python tools/c_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application --alpha-min 0.5 --alpha-max 1.5 --alpha-points 21

DEFORMATION FEATURES:
gap
delta_line_flux
delta_line_depth
delta_equivalent_width
delta_velocity
delta_width
delta_signal_quality
line/element transition response

5D VECTOR DEFINITIONS:
mean_GR:
Mean normalized gap response over all α-grid rows.

var_GR:
Variance of normalized gap response over all α-grid rows.

anisotropic_persistence:
Variance of mean structural response across element/line groups.

admissibility_persistence:
Fraction of α-grid rows that remain valid.

collapse_onset_radius:
First |α − 1| at which instability is detected.
If no instability is detected, this records the maximum tested radius.

IMPORTANT:
Spectral line-window proxies are structural spectral features, not direct
abundance measurements or radiative-transfer outputs.

NEXT STEP:
After running this script, create:

tools/c_alpha_normalization_review.py
