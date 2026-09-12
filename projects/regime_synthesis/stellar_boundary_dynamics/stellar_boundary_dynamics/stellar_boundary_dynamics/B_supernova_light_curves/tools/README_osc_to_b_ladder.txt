README.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase B — Running osc_to_b_ladder.py

PURPOSE
This file explains how to run osc_to_b_ladder.py correctly for converting
Open Supernova Catalog / AstroCats JSON files into Phase B STRUC_PERC_I
light-curve ladder CSV files.

SCRIPT
tools/osc_to_b_ladder.py

INPUT
One raw OSC / AstroCats JSON file for a single supernova object.

OUTPUT
One canonical Phase B light-curve ladder CSV file written into:

ladders/

EXPECTED PROJECT STRUCTURE

B_supernova_light_curves/
  tools/
    osc_to_b_ladder.py

  raw/
    SN1987A/
      SN1987A_OSC_raw.json
      SOURCE_SN1987A.txt

    SN1993J/
      SN1993J_OSC_raw.json
      SOURCE_SN1993J.txt

    SN1999em/
      SN1999em_OSC_raw.json
      SOURCE_SN1999em.txt

    SN2011dh/
      SN2011dh_OSC_raw.json
      SOURCE_SN2011dh.txt

    SN2012aw/
      SN2012aw_OSC_raw.json
      SOURCE_SN2012aw.txt

    SN2013ej/
      SN2013ej_OSC_raw.json
      SOURCE_SN2013ej.txt

  ladders/
    B_SN1987A_light_curve_ladder.csv
    B_SN1993J_light_curve_ladder.csv
    B_SN1999em_light_curve_ladder.csv
    B_SN2011dh_light_curve_ladder.csv
    B_SN2012aw_light_curve_ladder.csv
    B_SN2013ej_light_curve_ladder.csv

IMPORTANT PATH RULE
The command depends on where PowerShell is currently located.

If PowerShell is inside:

B_supernova_light_curves/tools/

then input and output paths must begin with ../ because raw/ and ladders/
are one level above tools/.

Correct pattern from tools/:

python osc_to_b_ladder.py ../raw/<OBJECT_FOLDER>/<RAW_JSON_FILE> ../ladders/<OUTPUT_LADDER_FILE>

Example:

python osc_to_b_ladder.py ../raw/SN1993J/SN1993J_OSC_raw.json ../ladders/B_SN1993J_light_curve_ladder.csv

If PowerShell is inside the parent folder:

B_supernova_light_curves/

then call the script through tools/ and do not use ../

Correct pattern from B_supernova_light_curves/:

python tools/osc_to_b_ladder.py raw/<OBJECT_FOLDER>/<RAW_JSON_FILE> ladders/<OUTPUT_LADDER_FILE>

Example:

python tools/osc_to_b_ladder.py raw/SN1993J/SN1993J_OSC_raw.json ladders/B_SN1993J_light_curve_ladder.csv

RECOMMENDED METHOD
Use the parent folder method because it is clearer.

Open PowerShell in:

B_supernova_light_curves/

Then run:

python tools/osc_to_b_ladder.py raw/SN1987A/SN1987A_OSC_raw.json ladders/B_SN1987A_light_curve_ladder.csv

python tools/osc_to_b_ladder.py raw/SN1993J/SN1993J_OSC_raw.json ladders/B_SN1993J_light_curve_ladder.csv

python tools/osc_to_b_ladder.py raw/SN1999em/SN1999em_OSC_raw.json ladders/B_SN1999em_light_curve_ladder.csv

python tools/osc_to_b_ladder.py raw/SN2011dh/SN2011dh_OSC_raw.json ladders/B_SN2011dh_light_curve_ladder.csv

python tools/osc_to_b_ladder.py raw/SN2012aw/SN2012aw_OSC_raw.json ladders/B_SN2012aw_light_curve_ladder.csv

python tools/osc_to_b_ladder.py raw/SN2013ej/SN2013ej_OSC_raw.json ladders/B_SN2013ej_light_curve_ladder.csv

ALTERNATIVE METHOD FROM tools/
If PowerShell is already inside:

B_supernova_light_curves/tools/

then run:

python osc_to_b_ladder.py ../raw/SN1987A/SN1987A_OSC_raw.json ../ladders/B_SN1987A_light_curve_ladder.csv

python osc_to_b_ladder.py ../raw/SN1993J/SN1993J_OSC_raw.json ../ladders/B_SN1993J_light_curve_ladder.csv

python osc_to_b_ladder.py ../raw/SN1999em/SN1999em_OSC_raw.json ../ladders/B_SN1999em_light_curve_ladder.csv

python osc_to_b_ladder.py ../raw/SN2011dh/SN2011dh_OSC_raw.json ../ladders/B_SN2011dh_light_curve_ladder.csv

python osc_to_b_ladder.py ../raw/SN2012aw/SN2012aw_OSC_raw.json ../ladders/B_SN2012aw_light_curve_ladder.csv

python osc_to_b_ladder.py ../raw/SN2013ej/SN2013ej_OSC_raw.json ../ladders/B_SN2013ej_light_curve_ladder.csv

RAW FILE NAMING CONVENTION
Raw files should use the aligned names:

SN1987A_OSC_raw.json
SN1993J_OSC_raw.json
SN1999em_OSC_raw.json
SN2011dh_OSC_raw.json
SN2012aw_OSC_raw.json
SN2013ej_OSC_raw.json

Output ladder files should use:

B_SN1987A_light_curve_ladder.csv
B_SN1993J_light_curve_ladder.csv
B_SN1999em_light_curve_ladder.csv
B_SN2011dh_light_curve_ladder.csv
B_SN2012aw_light_curve_ladder.csv
B_SN2013ej_light_curve_ladder.csv

COMMON ERROR
If you see:

FileNotFoundError: [Errno 2] No such file or directory

then one of these is wrong:

1. PowerShell is in the wrong folder.
2. The path does not use ../ when running from tools/.
3. The raw JSON file has not been renamed to the aligned *_OSC_raw.json name.
4. The object folder name does not match the command.

CHECKING FILES BEFORE RUNNING
From tools/, check a raw folder with:

dir ../raw/SN2011dh

From B_supernova_light_curves/, check a raw folder with:

dir raw/SN2011dh

SUCCESS MESSAGE
A successful run prints something like:

Object: SN1999em
Rows written: 1207
Skipped non-magnitude photometry records: 0
Output: ../ladders/B_SN1999em_light_curve_ladder.csv

WHAT THE SCRIPT DOES
The script reads the OSC JSON object, extracts magnitude-based photometry, and
writes rows in the Phase B ladder schema.

It maps:

OSC photometry.time       -> time_mjd
OSC photometry.band       -> band
OSC photometry.magnitude  -> brightness_value
OSC photometry.source     -> raw_reference/source trace

It also adds preliminary ladder fields:

stage_index
phase_name
time_since_peak_days
slope_local
curvature_local
transition_marker
boundary_role
support_regime_proxy
struc_perc_role
unns_interpretation

IMPORTANT SCIENTIFIC NOTE
The generated phase labels are preliminary data-prep labels based on time since
minimum magnitude per band. They are not final astrophysical claims. They are
sufficient for the first STRUC_PERC_I ladder scaffold and should be refined
after visual inspection and later CLE/alpha-application steps.

CURRENT PHASE B STATUS
The six pilot ladder files have been generated:

B_SN1987A_light_curve_ladder.csv
B_SN1993J_light_curve_ladder.csv
B_SN1999em_light_curve_ladder.csv
B_SN2011dh_light_curve_ladder.csv
B_SN2012aw_light_curve_ladder.csv
B_SN2013ej_light_curve_ladder.csv

NEXT PIPELINE STEP
Inspect the six ladder CSV files, summarize row counts and band coverage, then
prepare Phase B for STRUC_PERC_I conversion and alpha-application.
