README_c_alpha_normalization_review.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase C — Alpha Normalization Review Script

SCRIPT:
tools/c_alpha_normalization_review.py

PURPOSE:
Review first-pass Phase C spectral alpha grids and 5D vectors before B–C or
A–B–C bridge comparison.

INPUTS:
alpha_application/grids/*.csv
alpha_application/summaries/C_5D_VECTOR_SUMMARY.csv

OUTPUTS:
alpha_application/normalization_review/C_ALPHA_NORMALIZATION_REVIEW.csv
alpha_application/normalization_review/C_5D_VECTOR_SUMMARY_v2.csv
alpha_application/normalization_review/C_NORMALIZATION_REVIEW_INTERPRETATION.txt

RECOMMENDED RUN:
Open PowerShell in:

C_spectral_time_series/

Then run:

python tools/c_alpha_normalization_review.py alpha_application/grids alpha_application/summaries/C_5D_VECTOR_SUMMARY.csv alpha_application/normalization_review

WHAT IT CHECKS:
gap_response_norm
flux_response_norm
depth_response_norm
equivalent_width_response_norm
velocity_response_norm
width_response_norm
quality_response_norm
transition_response_norm
tail_pressure_proxy

BOUNDING RULE:
anisotropic_persistence_bounded = anisotropic_persistence / (1 + anisotropic_persistence)

SPECIAL FLAGS:
scale_review_needed
high_tail_attention
high_kappa_attention

INTERPRETATION:
The original v1 vectors remain diagnostic.
The v2 vectors are the safe layer for bridge work.
