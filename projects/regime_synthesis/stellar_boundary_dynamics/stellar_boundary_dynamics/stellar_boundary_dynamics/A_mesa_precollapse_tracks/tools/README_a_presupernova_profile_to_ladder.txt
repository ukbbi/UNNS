README_a_presupernova_profile_to_ladder.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase A — Real Pre-Supernova Profile Converter

SCRIPT:
tools/a_presupernova_profile_to_ladder.py

PURPOSE:
Convert real processed pre-supernova MESA profile .data files from Zenodo
5556959 into Phase A numerical radial-structure ladders.

This replaces the scaffold route for scientific Phase A processing.

INPUT FILES:
precomputed_tracks/selected_tracks/ZENODO_5556959/profile_single_M12.09_128net.data
precomputed_tracks/selected_tracks/ZENODO_5556959/profile_single_M19.98_128net.data

OUTPUT FILES:
ladders/A1_12M_presupernova_profile_ladder.csv
ladders/A2_20M_presupernova_profile_ladder.csv

SUMMARY OUTPUT:
summaries/A_PRESUPERNOVA_PROFILE_LADDER_SUMMARY.csv

DATA STRUCTURE INSPECTED:
Each .data file is a MESA profile-style file.

Observed structure:
line 1: global column numbers
line 2: global column names
line 3: global values
line 4: blank
line 5: profile column numbers
line 6: profile column names
line 7+: zone rows

The global header includes:
model_number
num_zones
star_age
time_seconds
star_mass
he_core_mass
c_core_mass
o_core_mass
si_core_mass
fe_core_mass

The profile rows include:
zone
logT
logRho
logP
logR
luminosity
entropy
q
radius
mass
ye
abar
mu
h1
he4
c12
o16
ne20
mg24
si28
fe56
eps_nuc
non_nuc_neu

DIRECTION:
The first profile row is the surface/envelope side.
The last profile row is the central core side:
q near 0, high logT, high logRho.

RECOMMENDED RUN:
Open PowerShell in:

A_mesa_precollapse_tracks/

Then run:

python tools/a_presupernova_profile_to_ladder.py --batch precomputed_tracks/selected_tracks/ZENODO_5556959 ladders summaries/A_PRESUPERNOVA_PROFILE_LADDER_SUMMARY.csv

SINGLE FILE RUN:
python tools/a_presupernova_profile_to_ladder.py precomputed_tracks/selected_tracks/ZENODO_5556959/profile_single_M12.09_128net.data ladders/A1_12M_presupernova_profile_ladder.csv

OUTPUT LADDER MEANING:
Each row is one radial zone in the pre-supernova model profile.
This is a real pre-supernova radial-structure ladder, not a time-series history
track and not an inlist scaffold.

SCIENTIFIC CAUTION:
These files are final/pre-supernova profile structures. They are suitable for
radial support/composition/boundary analysis. They do not by themselves provide
a time-resolved stellar evolution history.

NEXT STEP:
Convert these Phase A profile ladders into STRUC-PERC-I canonical inputs and
numeric ladders.
