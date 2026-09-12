README_b_ladder_to_struc_perc_i.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase B — Convert Light-Curve Ladders to STRUC_PERC_I Canonical Inputs

PURPOSE
b_ladder_to_struc_perc_i.py compresses full Phase B light-curve ladder CSV files
into compact STRUC_PERC_I-ready canonical input files.

It converts:

ladders/B_SN1987A_light_curve_ladder.csv

into:

struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv

COMPRESSION RULE
The converter compresses each full light-curve ladder into one row per:

object × band × phase_name

This means thousands of photometry rows become a compact structural ladder over
canonical phases such as:

rise
peak
early_decline
plateau_or_shoulder
break
tail_decay
late_relaxation

EXPECTED PROJECT STRUCTURE

B_supernova_light_curves/
  tools/
    osc_to_b_ladder.py
    b_ladder_to_struc_perc_i.py
    README_b_ladder_to_struc_perc_i.txt

  ladders/
    B_SN1987A_light_curve_ladder.csv
    B_SN1993J_light_curve_ladder.csv
    B_SN1999em_light_curve_ladder.csv
    B_SN2011dh_light_curve_ladder.csv
    B_SN2012aw_light_curve_ladder.csv
    B_SN2013ej_light_curve_ladder.csv

  struc_perc_i/
    canonical_inputs/
    summaries/

RECOMMENDED BATCH RUN
Open PowerShell in:

B_supernova_light_curves/

Then run:

python tools/b_ladder_to_struc_perc_i.py --batch ladders struc_perc_i/canonical_inputs struc_perc_i/summaries/B_STRUC_PERC_I_SUMMARY.csv

This will create:

struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN1993J_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN1999em_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN2011dh_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN2012aw_struc_perc_input.csv
struc_perc_i/canonical_inputs/B_SN2013ej_struc_perc_input.csv

and:

struc_perc_i/summaries/B_STRUC_PERC_I_SUMMARY.csv

SINGLE-FILE RUN FROM B_supernova_light_curves/
Example:

python tools/b_ladder_to_struc_perc_i.py ladders/B_SN1987A_light_curve_ladder.csv struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv

SINGLE-FILE RUN FROM tools/
If PowerShell is inside:

B_supernova_light_curves/tools/

then use ../ paths:

python b_ladder_to_struc_perc_i.py ../ladders/B_SN1987A_light_curve_ladder.csv ../struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv

OUTPUT FIELDS
Each compact STRUC_PERC_I row includes:

struc_perc_id
source_ladder_id
object_name
supernova_type
band
phase_name
stage_index
n_points
time_start_mjd
time_end_mjd
duration_days
time_mid_mjd
mag_start
mag_end
mag_min
mag_max
mag_mean
mag_median
mag_range
mean_slope
median_slope
mean_curvature
median_curvature
transition_marker
boundary_role
support_regime_proxy
struc_perc_role
gap
gap_source
alpha_ready
unns_interpretation
raw_reference

GAP DEFINITION
For this first Phase B conversion, the STRUC_PERC_I gap proxy is:

gap = mag_range = mag_max - mag_min

Because the data are in magnitude units, lower magnitude means brighter. This
gap should be understood as a phase-local magnitude excursion, not as final
physical energy output.

ALPHA READINESS
alpha_ready is marked:

yes     when the phase has at least two points and a valid gap
partial when the phase is too sparse or lacks enough valid numeric values

SCIENTIFIC NOTE
These compact files are not yet the final 5D structural vectors. They are the
canonical STRUC_PERC_I input layer. The next steps are alpha-application,
deformation-grid construction, and 5D vector extraction.

PIPELINE POSITION

OSC raw JSON
→ B light-curve ladder CSV
→ compact STRUC_PERC_I canonical input
→ alpha-application
→ deformation grid
→ 5D structural vector
→ comparison
