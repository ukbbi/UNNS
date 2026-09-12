README_b_struc_input_to_numeric_ladders.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase B — Convert Canonical Inputs to STRUC-PERC-I Numeric Ladders

PURPOSE
b_struc_input_to_numeric_ladders.py converts Phase B STRUC_PERC_I canonical
input CSV files into plain numeric ladder .txt files that can be loaded into
STRUC-PERC-I v2.5.0 batch mode.

WHY THIS STEP IS NEEDED
STRUC-PERC-I v2.5.0 expects a plain ordered numeric ladder:

x1 <= x2 <= ... <= xn

It does not understand the multi-column Phase B canonical input schema directly.
Therefore the canonical input CSVs must first be reduced to pure numeric ladders.

INPUT
struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN1993J_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN1999em_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN2011dh_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN2012aw_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN2013ej_struc_perc_input.csv

OUTPUT
struc_perc_i/numeric_ladders/B_SN1987A_numeric_ladder.txt
struc_perc_i/numeric_ladders/B_SN1993J_numeric_ladder.txt
struc_perc_i/numeric_ladders/B_SN1999em_numeric_ladder.txt
struc_perc_i/numeric_ladders/B_SN2011dh_numeric_ladder.txt
struc_perc_i/numeric_ladders/B_SN2012aw_numeric_ladder.txt
struc_perc_i/numeric_ladders/B_SN2013ej_numeric_ladder.txt

CONVERSION RULE
The script reads the "gap" column from each canonical input row.

For this Phase B run:

gap = phase-local magnitude range

The script then creates a cumulative monotone ladder:

x0 = 0
x1 = gap1
x2 = gap1 + gap2
x3 = gap1 + gap2 + gap3
...

This turns phase-local structural excursions into a valid ordered numeric ladder.

RECOMMENDED BATCH RUN
Open PowerShell in:

B_supernova_light_curves/

Then run:

python tools/b_struc_input_to_numeric_ladders.py --batch struc_perc_i/canonical_inputs struc_perc_i/numeric_ladders struc_perc_i/summaries/B_NUMERIC_LADDER_SUMMARY.csv

SINGLE-FILE RUN
From B_supernova_light_curves/:

python tools/b_struc_input_to_numeric_ladders.py struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv struc_perc_i/numeric_ladders/B_SN1987A_numeric_ladder.txt

FROM tools/
If PowerShell is inside:

B_supernova_light_curves/tools/

then use ../ paths:

python b_struc_input_to_numeric_ladders.py ../struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv ../struc_perc_i/numeric_ladders/B_SN1987A_numeric_ladder.txt

EXPECTED SUMMARY OUTPUT
struc_perc_i/summaries/B_NUMERIC_LADDER_SUMMARY.csv

The summary records:

input_file
output_file
object_name
rows_in
numeric_points_out
gap_source
gap_min
gap_max
gap_sum
status

NEXT STEP
Load the generated .txt files into STRUC-PERC-I v2.5.0 Batch Mode:

struc_perc_i/numeric_ladders/*.txt

Then export:

struc_perc_batch_results.csv
struc_perc_batch_results.json

SCIENTIFIC NOTE
These numeric ladders are first-pass structural reductions of observed
supernova light-curve phase behavior. They are designed for STRUC-PERC-I
percolation testing. They are not raw photometry and should not be interpreted
as physical light curves directly.
