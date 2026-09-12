README_a_profile_ladder_to_struc_perc_i.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase A — Profile Ladder to STRUC-PERC-I Converter

SCRIPT:
tools/a_profile_ladder_to_struc_perc_i.py

PURPOSE:
Convert real Phase A pre-supernova radial profile ladders into compact
STRUC-PERC-I canonical input CSV files and plain numeric ladders.

INPUT:
ladders/A1_12M_presupernova_profile_ladder.csv
ladders/A2_20M_presupernova_profile_ladder.csv

OUTPUT:
struc_perc_i/canonical_inputs/A1_12M_struc_perc_input.csv
struc_perc_i/canonical_inputs/A2_20M_struc_perc_input.csv

struc_perc_i/numeric_ladders/A1_12M_numeric_ladder.txt
struc_perc_i/numeric_ladders/A2_20M_numeric_ladder.txt

struc_perc_i/summaries/A_STRUC_PERC_I_INPUT_SUMMARY.csv

RECOMMENDED RUN:
Open PowerShell in:

A_mesa_precollapse_tracks/

Then run:

python tools/a_profile_ladder_to_struc_perc_i.py --batch ladders struc_perc_i

OPTIONAL BIN COUNT:
Default compact radial bins = 64.

Example:

python tools/a_profile_ladder_to_struc_perc_i.py --batch ladders struc_perc_i --bins 64

WHAT THE SCRIPT DOES:
1. Reads the real radial-zone profile ladder.
2. Compresses each profile into compact radial bins.
3. Computes a structural gap from real profile features:
   logT
   logRho
   Ye
   support_margin_proxy
   energy_loss_proxy
   composition-stage transitions
4. Writes a compact STRUC-PERC-I canonical input CSV.
5. Writes a plain monotone cumulative numeric ladder .txt for STRUC-PERC-I.

GAP DEFINITION:
gap_i is a weighted normalized local radial change:

0.25 × ΔlogT
0.25 × ΔlogRho
0.15 × ΔYe
0.15 × Δsupport_margin_proxy
0.10 × Δenergy_loss_proxy
0.10 × composition_transition_fraction

The values are normalized by the robust global range of each profile feature.

SCIENTIFIC MEANING:
This is now a real Phase A structural profile reduction from pre-supernova
model data. It is not an inlist scaffold and not raw MESA source code.

NEXT STEP:
Run the generated numeric ladders in STRUC-PERC-I v2.5.0 batch mode:

struc_perc_i/numeric_ladders/A1_12M_numeric_ladder.txt
struc_perc_i/numeric_ladders/A2_20M_numeric_ladder.txt

Export the results into:

struc_perc_i/struc_perc_batch_results.csv
struc_perc_i/struc_perc_batch_results.json
