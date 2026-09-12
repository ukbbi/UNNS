README_b_alpha_apply.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase B — Alpha Application / Deformation-Grid Script

SCRIPT:
tools/b_alpha_apply.py

PURPOSE:
Apply α-deformation to Phase B STRUC_PERC_I canonical inputs and generate:

1. object-level α deformation grids
2. object-level 5D vectors
3. Phase B alpha summary files

INPUT:
struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN1993J_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN1999em_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN2011dh_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN2012aw_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN2013ej_struc_perc_input.csv

OUTPUT:
alpha_application/grids/*.csv
alpha_application/vectors/*.csv
alpha_application/summaries/B_ALPHA_APPLICATION_SUMMARY.csv
alpha_application/summaries/B_5D_VECTOR_SUMMARY.csv

RECOMMENDED RUN
Open PowerShell in:

B_supernova_light_curves/

Then run:

python tools/b_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application

OPTIONAL ALPHA GRID
Default:
alpha_min = 0.50
alpha_max = 1.50
alpha_points = 21

Custom example:

python tools/b_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application --alpha-min 0.5 --alpha-max 1.5 --alpha-points 21

SINGLE OBJECT RUN
From B_supernova_light_curves/:

python tools/b_alpha_apply.py struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv alpha_application/grids/B_SN1987A_alpha_grid.csv alpha_application/vectors/B_SN1987A_5d_vector.csv

DEFORMATION FEATURES
The script deforms:

gap
duration_days
mean_slope
mean_curvature

For each α value, it computes:

gap_alpha
duration_alpha
slope_alpha
curvature_alpha
gap_response_norm
duration_response_norm
slope_response_norm
curvature_response_norm
structural_response
phase_persistence_score
alpha_status
instability_flag

5D VECTOR DEFINITIONS

mean_GR:
Mean normalized gap response over all α-grid rows.

var_GR:
Variance of normalized gap response over all α-grid rows.

anisotropic_persistence:
Variance of mean structural response across band × phase groups.

admissibility_persistence:
Fraction of α-grid rows that remain valid.

collapse_onset_radius:
First |α − 1| at which instability is detected.
If no instability is detected, this records the maximum tested radius.

NOTES:
This is a first-pass Phase B deformation layer. It does not claim a final
astrophysical mechanism. It tests whether the compact light-curve ladder
representation remains structurally coherent under controlled deformation.

SPECIAL OBJECT:
SN2012aw should be inspected carefully because the STRUC-PERC-I run returned
FULL_PERCOLATION but with high κ_connect and high tail dominance.
