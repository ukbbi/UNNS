README_c_line_ladder_to_struc_perc_i.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase C — Spectral Line Ladder to STRUC-PERC-I Converter

SCRIPT:
tools/c_line_ladder_to_struc_perc_i.py

PURPOSE:
Convert Phase C spectral line ladders into STRUC-PERC-I canonical inputs and
numeric ladders.

INPUT:
ladders/C1_SN1993J_spectral_line_ladder.csv
ladders/C2_SN2012aw_spectral_line_ladder.csv

OUTPUT:
struc_perc_i/canonical_inputs/C1_SN1993J_struc_perc_input.csv
struc_perc_i/canonical_inputs/C2_SN2012aw_struc_perc_input.csv

struc_perc_i/numeric_ladders/C1_SN1993J_numeric_ladder.txt
struc_perc_i/numeric_ladders/C2_SN2012aw_numeric_ladder.txt

struc_perc_i/summaries/C_STRUC_PERC_I_INPUT_SUMMARY.csv

RECOMMENDED RUN:
Open PowerShell in:

C_spectral_time_series/

Then run:

python tools/c_line_ladder_to_struc_perc_i.py --batch ladders struc_perc_i

NUMERIC LADDER:
The numeric ladder is a cumulative date-ordered spectral gap sequence.

Gap is based on changes in:

line_flux_proxy
line_depth_proxy
equivalent_width_proxy
velocity_proxy_km_s
width_proxy_angstrom
signal_quality_proxy
line transitions
element transitions

NOTE:
Because phase_days is currently unavailable, ordering is based on spectrum_date
and spectrum_id. This is acceptable for the pilot but should be refined if
phase metadata becomes available.

NEXT STEP:
Run the generated numeric ladders through STRUC-PERC-I batch mode.
