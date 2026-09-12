Charge Boundary Routing I
Phase 2C-P — Pairwise Same-Charge Route Control
README_build_phase2C_pairwise_route_control.txt

This v2 package fixes the diagnostics-folder write error by explicitly creating
every output folder before writing any CSV, JSON, or TXT file.

Why this script is needed
-------------------------
The original Phase 2C control has only five objects:

    positron
    proton
    pi+
    K+
    W+

All have Q/e = +1.

The five-row object ladders are correct conceptually, but STRUC-I can reject
them as too small / too low-cardinality. This script converts the five objects
into unordered pairwise comparisons:

    5 choose 2 = 10 pair rows

Control question:

    When charge_difference = 0 for every pair, do structural route differences
    remain nonzero?

Expected result:

    Same Q = +1 does not imply same structural route.

Required input
--------------
Run this first:

    python scripts\build_phase2C_same_charge_route_control.py

This creates:

    data/canonical/phase2C_same_charge_route_control.csv

Then run:

    python scripts\build_phase2C_pairwise_route_control.py

Files written
-------------
    data/derived/phase2C_pairwise_same_charge_route_control.csv
    data/derived/phase2C_pairwise_same_charge_route_control_summary.json
    ladders/phase2C_pairwise_same_charge_control/
    ladders/phase2C_pairwise_same_charge_control/one_column/
    ladders/phase2C_pairwise_same_charge_control/diagnostics/

Primary chamber files
---------------------
Use these one-column files first:

    phase2C_pairwise_ladder_structural_distance.csv
    phase2C_pairwise_ladder_route_distance.csv
    phase2C_pairwise_ladder_type_distance.csv
    phase2C_pairwise_ladder_structural_route_pair_code.csv
    phase2C_pairwise_ladder_category_pair_code.csv
    phase2C_pairwise_ladder_sub_category_pair_code.csv
    phase2C_pairwise_ladder_pair_class_code.csv
    phase2C_pairwise_ladder_layer_pair_code.csv

Do not upload first
-------------------
    phase2C_pairwise_ladder_charge_difference.csv
    phase2C_pairwise_ladder_same_charge_pair.csv

They are constant because every pair compares Q/e = +1 objects.
