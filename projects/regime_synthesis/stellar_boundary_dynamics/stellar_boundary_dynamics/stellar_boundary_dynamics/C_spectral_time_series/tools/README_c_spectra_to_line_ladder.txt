README_c_spectra_to_line_ladder.txt
STELLAR_BOUNDARY_DYNAMICS_I
Phase C — WISeREP Spectra to Line Ladder Converter

SCRIPT:
tools/c_spectra_to_line_ladder.py

PURPOSE:
Convert raw WISeREP spectral files into Phase C spectral line ladders.

INPUT:
raw/C1_SN1993J/
raw/C2_SN2012aw/

Each raw object folder should contain:
wiserep_spectra.csv
SOURCE_<object>_WISeREP.txt
raw spectra files with extensions:
.dat
.flm
.txt
.ascii
.asc

OUTPUT:
ladders/C1_SN1993J_spectral_line_ladder.csv
ladders/C2_SN2012aw_spectral_line_ladder.csv

SUMMARY:
summaries/C_SPECTRAL_LINE_LADDER_SUMMARY.csv

RECOMMENDED RUN:
Open PowerShell in:

C_spectral_time_series/

Then run:

python tools/c_spectra_to_line_ladder.py --batch raw ladders summaries/C_SPECTRAL_LINE_LADDER_SUMMARY.csv

WHAT IT EXTRACTS:
For each spectrum and each target line window, the script computes structural
line-window proxies:

continuum_level
line_flux_proxy
line_depth_proxy
equivalent_width_proxy
velocity_proxy_km_s
width_proxy_angstrom
signal_quality_proxy

TARGET LINE WINDOWS:
H_alpha
H_beta
He_I_5876
O_I_7774
Ca_II_NIR
Si_II_6355
Fe_II_5169
Ni_Co_decay_proxy

IMPORTANT:
These are spectral structural proxies, not abundance measurements.
They should be used for STRUC-PERC-I and α-application as feature ladders, not
as direct nucleosynthesis yields.

NEXT STEP:
After creating the two spectral line ladders, create:

tools/c_line_ladder_to_struc_perc_i.py
