alpha_geoid_earth_moon_mars
===========================

Contents
--------
This pack applies α to Earth, Moon, and Mars geoid/gravity harmonic subsets.

Bodies:
- Earth
- Moon
- Mars

α sweep:
- 0.80
- 0.90
- 1.00
- 1.10
- 1.20

Applied operator
----------------
For each spherical harmonic coefficient row (l, m, C, S), with l >= 2:

    C_alpha(l,m) = C(l,m) * α^l
    S_alpha(l,m) = S(l,m) * α^l

Then:

    mag_alpha = sqrt(C_alpha^2 + S_alpha^2)

Two ladder families are produced.

1. Coefficient-magnitude ladders
--------------------------------
Sorted positive values of mag_alpha.

2. Degree-power ladders
-----------------------
For each degree l:

    power_alpha(l) = sum_m mag_alpha(l,m)^2

Sorted positive degree powers.

Gap ladders
-----------
For each sorted ladder, positive adjacent differences are also produced.

Files
-----
For each body and each α:
- <body>_alpha_<α>_geoid_coeffmag_ladder.csv
- <body>_alpha_<α>_geoid_coeffmag_gaps.csv
- <body>_alpha_<α>_geoid_degreepower_ladder.csv
- <body>_alpha_<α>_geoid_degreepower_gaps.csv

Recommended first chamber run
-----------------------------
Start with:
- earth_alpha_0.80_geoid_degreepower_ladder.csv
- earth_alpha_1.00_geoid_degreepower_ladder.csv
- earth_alpha_1.20_geoid_degreepower_ladder.csv
- moon_alpha_1.00_geoid_degreepower_ladder.csv
- mars_alpha_1.00_geoid_degreepower_ladder.csv

Auxiliary files
---------------
- manifest.csv
- summary.csv
- per-body per-α degreepower tables
