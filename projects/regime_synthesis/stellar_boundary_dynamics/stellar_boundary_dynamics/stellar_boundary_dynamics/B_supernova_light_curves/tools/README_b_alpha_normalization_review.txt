README_b_alpha_normalization_review.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase B — Alpha Normalization Review Script

SCRIPT:
tools/b_alpha_normalization_review.py

PURPOSE:
Review the first-pass Phase B alpha grids and 5D vectors before using them for
A–B comparison.

The script detects slope/curvature dominance, bounds anisotropic_persistence,
and writes a safer v2 vector summary.

INPUTS:
alpha_application/grids/*.csv
alpha_application/summaries/B_5D_VECTOR_SUMMARY.csv

OUTPUTS:
alpha_application/normalization_review/B_ALPHA_NORMALIZATION_REVIEW.csv
alpha_application/normalization_review/B_5D_VECTOR_SUMMARY_v2.csv
alpha_application/normalization_review/B_NORMALIZATION_REVIEW_INTERPRETATION.txt

RECOMMENDED RUN:
Open PowerShell in:

B_supernova_light_curves/

Then run:

python tools/b_alpha_normalization_review.py alpha_application/grids alpha_application/summaries/B_5D_VECTOR_SUMMARY.csv alpha_application/normalization_review

WHAT IT CHECKS:
mean_gap_response
mean_duration_response
mean_slope_response
mean_curvature_response
slope_to_gap_ratio
curvature_to_gap_ratio
max_channel_to_gap_ratio
original_anisotropic_persistence
bounded_anisotropic_persistence
scale_review_needed
high_tail_attention

BOUNDING RULE:
anisotropic_persistence_bounded = anisotropic_persistence / (1 + anisotropic_persistence)

INTERPRETATION:
The original v1 vectors are preserved.
The v2 vectors should be used for cross-object comparison and A–B bridge work.
