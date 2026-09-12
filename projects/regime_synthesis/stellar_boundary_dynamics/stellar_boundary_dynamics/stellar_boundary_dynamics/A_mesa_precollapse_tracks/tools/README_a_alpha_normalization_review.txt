README_a_alpha_normalization_review.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase A — Alpha Normalization Review Script

SCRIPT:
tools/a_alpha_normalization_review.py

PURPOSE:
Review first-pass Phase A alpha grids and 5D vectors before using them for
A–B comparison.

The script detects response-channel dominance, bounds anisotropic_persistence,
and writes a safer v2 vector summary.

INPUTS:
alpha_application/grids/*.csv
alpha_application/summaries/A_5D_VECTOR_SUMMARY.csv

OUTPUTS:
alpha_application/normalization_review/A_ALPHA_NORMALIZATION_REVIEW.csv
alpha_application/normalization_review/A_5D_VECTOR_SUMMARY_v2.csv
alpha_application/normalization_review/A_NORMALIZATION_REVIEW_INTERPRETATION.txt

RECOMMENDED RUN:
Open PowerShell in:

A_mesa_precollapse_tracks/

Then run:

python tools/a_alpha_normalization_review.py alpha_application/grids alpha_application/summaries/A_5D_VECTOR_SUMMARY.csv alpha_application/normalization_review

WHAT IT CHECKS:
mean_gap_response
mean_thermal_response
mean_density_response
mean_composition_response
mean_support_response
mean_loss_response
thermal_to_gap_ratio
density_to_gap_ratio
composition_to_gap_ratio
support_to_gap_ratio
loss_to_gap_ratio
max_channel_to_gap_ratio
original_anisotropic_persistence
bounded_anisotropic_persistence
scale_review_needed
high_kappa_attention

BOUNDING RULE:
anisotropic_persistence_bounded = anisotropic_persistence / (1 + anisotropic_persistence)

INTERPRETATION:
The original v1 vectors are preserved.
The v2 vectors should be used for cross-object comparison and A–B bridge work.
