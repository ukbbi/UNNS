README_a_inlists_to_stage_ladder.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase A — MESA Inlist Stage Scaffold Converter

SCRIPT:
tools/a_inlists_to_stage_ladder.py

PURPOSE:
Create first-pass Phase A structural-stage scaffold ladders from the archived
MESA pre-MS to core-collapse test-suite folders.

INPUT:
A1_12M_pre_ms_to_core_collapse/
A2_20M_pre_ms_to_core_collapse/

OUTPUT:
ladders/A1_12M_stage_ladder.csv
ladders/A2_20M_stage_ladder.csv

IMPORTANT:
This script does not parse MESA history.data or profile*.data.
It creates a stage scaffold from the MESA inlist chain.

The result is useful for pipeline alignment and scaffold testing, but it is not
a full physical stellar-evolution output.

RECOMMENDED RUN:
Open PowerShell in:

A_mesa_precollapse_tracks/

Then run:

python tools/a_inlists_to_stage_ladder.py --batch .

SINGLE-FOLDER RUN:
python tools/a_inlists_to_stage_ladder.py A1_12M_pre_ms_to_core_collapse ladders/A1_12M_stage_ladder.csv

STAGE CHAIN:
1 late_pre_zams
2 zams
3 end_core_he_burn
4 end_core_c_burn
5 lgTmax_silicon_approach
6 core_collapse

NEXT STEP:
Convert the stage ladders into A STRUC-PERC-I canonical inputs and numeric
ladders.
