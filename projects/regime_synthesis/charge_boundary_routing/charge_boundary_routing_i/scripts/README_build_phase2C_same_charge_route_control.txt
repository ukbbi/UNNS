Charge Boundary Routing I
Phase 2C — Same-Charge Different-Route Control
README_build_phase2C_same_charge_route_control.txt

Generated: 2026-06-15


Purpose
-------
This README documents:

    scripts/build_phase2C_same_charge_route_control.py

Phase 2C is the reserved validation/control test for Charge Boundary Routing I.

It tests whether objects with the same external charge Q = +1 occupy the same
structural route.


Control Question
----------------
Does same external charge Q = +1 imply same structural route?

Expected UNNS result:

    Same Q = +1 does not imply same structural route.

Canonical statement:

    Charge value is a projection.
    Structural route is a separate coordinate.


Control Objects
---------------
The Phase 2C control corpus contains five Q = +1 objects:

    positron
    proton
    pi+
    K+
    W+

All have:

    Q_over_e = +1

But they differ by:

    layer
    category
    sub_category
    route class
    closure class
    structural route label
    composite / external status
    boson / fermion status
    hadron / lepton / gauge-boson status


Where to Place the Script
-------------------------
Place the script here:

    charge_boundary_routing_i/
    └── scripts/
        └── build_phase2C_same_charge_route_control.py


How to Run
----------
Run from the project root:

    python scripts\build_phase2C_same_charge_route_control.py


Files Written
-------------
Canonical corpus:

    data/canonical/phase2C_same_charge_route_control.csv

Summary:

    data/derived/phase2C_same_charge_route_control_summary.json

Ladders:

    ladders/phase2C_same_charge_control/

One-column chamber ladders:

    ladders/phase2C_same_charge_control/one_column/

Diagnostics:

    ladders/phase2C_same_charge_control/diagnostics/
        phase2C_same_charge_route_control_summary.json
        README_phase2C_same_charge_route_control_diagnostics.txt

Prepared result folders:

    results/struc_perc_i/phase2C_same_charge_control/
    results/struc_i/phase2C_same_charge_control/

Prepared report folder:

    outputs/reports/phase2C_same_charge_control/


Encodings Built
---------------
The script builds these encodings:

    Q_over_e
    same_charge_constant
    layer_code
    route_class_code
    closure_class_code
    category_code
    sub_category_code
    structural_route_code
    composite
    external
    boson
    fermion
    hadron
    meson
    baryon
    lepton
    gauge_boson


Expected Constant Encodings
---------------------------
These encodings are intentionally constant:

    Q_over_e
    same_charge_constant

Reason:

    every object in the control has Q/e = +1.

Do not upload these first. They are invariant diagnostics.


Primary Chamber Inputs
----------------------
Use these one-column files first:

    ladders/phase2C_same_charge_control/one_column/
        phase2C_same_charge_ladder_structural_route_code.csv
        phase2C_same_charge_ladder_category_code.csv
        phase2C_same_charge_ladder_sub_category_code.csv
        phase2C_same_charge_ladder_layer_code.csv
        phase2C_same_charge_ladder_composite.csv
        phase2C_same_charge_ladder_external.csv
        phase2C_same_charge_ladder_boson.csv
        phase2C_same_charge_ladder_fermion.csv
        phase2C_same_charge_ladder_hadron.csv

Optional secondary files:

    phase2C_same_charge_ladder_meson.csv
    phase2C_same_charge_ladder_baryon.csv
    phase2C_same_charge_ladder_lepton.csv
    phase2C_same_charge_ladder_gauge_boson.csv
    phase2C_same_charge_ladder_route_class_code.csv
    phase2C_same_charge_ladder_closure_class_code.csv


Do Not Upload First
-------------------
Skip these in the first chamber pass:

    phase2C_same_charge_ladder_Q_over_e.csv
    phase2C_same_charge_ladder_same_charge_constant.csv


Recommended STRUC-PERC-I Output Placement
-----------------------------------------
After STRUC-PERC-I, save as:

    results/struc_perc_i/phase2C_same_charge_control/
        PHASE2C_SAME_CHARGE_STRUC_PERC_I_v2_5_0_batch_results.csv
        PHASE2C_SAME_CHARGE_STRUC_PERC_I_v2_5_0_batch_results.json


Recommended STRUC-I Output Placement
------------------------------------
After STRUC-I, save as:

    results/struc_i/phase2C_same_charge_control/
        PHASE2C_SAME_CHARGE_STRUC_I_v1_0_4_profiles.csv
        PHASE2C_SAME_CHARGE_STRUC_I_v1_0_4_results.json


Interpretation Rule
-------------------
If Q_over_e is constant but structural_route_code, category_code, layer_code,
and object flags separate, then the control supports:

    same Q = +1 does not imply same structural route.

This should be used as the clean validation/control result for the manuscript
or public article.
