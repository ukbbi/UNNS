README_a_alpha_apply.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase A — Alpha Application / Deformation-Grid Script

SCRIPT:
tools/a_alpha_apply.py

PURPOSE:
Apply α-deformation to real Phase A STRUC-PERC-I canonical inputs and generate:

1. object-level α deformation grids
2. object-level 5D vectors
3. Phase A alpha summary files

INPUT:
struc_perc_i/canonical_inputs/A1_12M_struc_perc_input.csv
struc_perc_i/canonical_inputs/A2_20M_struc_perc_input.csv

OUTPUT:
alpha_application/grids/A1_12M_alpha_grid.csv
alpha_application/grids/A2_20M_alpha_grid.csv

alpha_application/vectors/A1_12M_5d_vector.csv
alpha_application/vectors/A2_20M_5d_vector.csv

alpha_application/summaries/A_ALPHA_APPLICATION_SUMMARY.csv
alpha_application/summaries/A_5D_VECTOR_SUMMARY.csv

RECOMMENDED RUN:
Open PowerShell in:

A_mesa_precollapse_tracks/

Then run:

python tools/a_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application

OPTIONAL ALPHA GRID:
Default:
alpha_min = 0.50
alpha_max = 1.50
alpha_points = 21

Custom example:

python tools/a_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application --alpha-min 0.5 --alpha-max 1.5 --alpha-points 21

DEFORMATION FEATURES:
The script deforms profile-derived compact structural features:

gap
delta_logT
delta_logRho
delta_ye
delta_support_margin
delta_energy_loss

It computes:

gap_alpha
delta_logT_alpha
delta_logRho_alpha
delta_ye_alpha
delta_support_alpha
delta_energy_loss_alpha
gap_response_norm
thermal_response_norm
density_response_norm
composition_response_norm
support_response_norm
loss_response_norm
structural_response
phase_persistence_score
alpha_status
instability_flag

5D VECTOR DEFINITIONS:

mean_GR:
Mean normalized gap response over all α-grid rows.

var_GR:
Variance of normalized gap response over all α-grid rows.

anisotropic_persistence:
Variance of mean structural response across radial phase groups.

admissibility_persistence:
Fraction of α-grid rows that remain valid.

collapse_onset_radius:
First |α − 1| at which instability is detected.
If no instability is detected, this records the maximum tested radius.

SCIENTIFIC NOTE:
This is a first-pass deformation layer for real pre-supernova radial-profile
data. It does not claim a time-resolved collapse trajectory. It tests
structural stability of the selected terminal/pre-supernova radial profile
representation.
