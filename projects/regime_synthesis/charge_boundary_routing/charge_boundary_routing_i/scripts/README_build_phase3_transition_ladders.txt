Charge Boundary Routing I
Phase 3 — Closure-Preserving Transitions
README_build_phase3_transition_ladders.txt

Generated: 2026-06-15


Purpose
-------
This README documents:

    scripts/build_phase3_transition_ladders.py

The script builds numeric, chamber-ready ladders for Phase 3 transition testing.

It is the second Phase 3 build step.

The first script:

    scripts/build_phase3_transition_corpus.py

creates the canonical transition corpus.

This script:

    scripts/build_phase3_transition_ladders.py

reads that corpus and produces the ladder files used by STRUC-PERC-I and STRUC-I.


Project Position
----------------
Current project sequence:

    Phase 1 — Boundary Classification              COMPLETE
    Phase 2 — Bridge Geometry                       COMPLETE
    Phase 2C — +1 Same-Charge Route Control          RESERVED / VALIDATION
    Phase 3 — Closure-Preserving Transitions         ACTIVE

Phase 3 asks:

    Do allowed particle transitions preserve the charge-boundary invariant
    while routing identity between different structural regimes?


Where to Place the Script
-------------------------
Place the script here:

    charge_boundary_routing_i/
    └── scripts/
        └── build_phase3_transition_ladders.py


Required Input
--------------
Before running this script, this file must already exist:

    charge_boundary_routing_i/
    └── data/
        └── canonical/
            └── phase3_closure_preserving_transitions.csv

That file is produced by:

    python scripts\build_phase3_transition_corpus.py


How to Run
----------
Run from the project root:

    python scripts\build_phase3_transition_ladders.py

Expected project root:

    charge_boundary_routing_i/


Files Written
-------------
The script writes full provenance ladders to:

    charge_boundary_routing_i/
    └── ladders/
        └── phase3_transitions/
            ├── phase3_transition_ladder_charge_balance_error.csv
            ├── phase3_transition_ladder_initial_total_charge.csv
            ├── phase3_transition_ladder_final_total_charge.csv
            ├── phase3_transition_ladder_charged_multiplicity_delta.csv
            ├── phase3_transition_ladder_neutral_multiplicity_delta.csv
            ├── phase3_transition_ladder_layer_transition_code.csv
            ├── phase3_transition_ladder_route_transition_code.csv
            ├── phase3_transition_ladder_closure_transition_code.csv
            ├── phase3_transition_ladder_boundary_preservation_code.csv
            ├── phase3_transition_ladder_externalization_delta.csv
            ├── phase3_transition_ladder_composite_count_delta.csv
            └── phase3_transition_ladder_transition_class_code.csv

It writes chamber-upload one-column versions to:

    charge_boundary_routing_i/
    └── ladders/
        └── phase3_transitions/
            └── one_column/
                ├── phase3_transition_ladder_charge_balance_error.csv
                ├── phase3_transition_ladder_initial_total_charge.csv
                ├── phase3_transition_ladder_final_total_charge.csv
                ├── phase3_transition_ladder_charged_multiplicity_delta.csv
                ├── phase3_transition_ladder_neutral_multiplicity_delta.csv
                ├── phase3_transition_ladder_layer_transition_code.csv
                ├── phase3_transition_ladder_route_transition_code.csv
                ├── phase3_transition_ladder_closure_transition_code.csv
                ├── phase3_transition_ladder_boundary_preservation_code.csv
                ├── phase3_transition_ladder_externalization_delta.csv
                ├── phase3_transition_ladder_composite_count_delta.csv
                └── phase3_transition_ladder_transition_class_code.csv

It writes diagnostics to:

    charge_boundary_routing_i/
    └── ladders/
        └── phase3_transitions/
            └── diagnostics/
                ├── phase3_transition_ladder_summary.json
                └── README_phase3_transition_ladder_diagnostics.txt


Full Provenance vs One-Column Files
-----------------------------------
The files in:

    ladders/phase3_transitions/

preserve transition metadata.

They include:

    value
    transition_id
    transition_name
    encoding
    initial_objects
    final_objects
    initial_symbols
    final_symbols
    initial_Q_sum
    final_Q_sum
    charge_balance_error
    charge_conserved
    initial_layers
    final_layers
    layer_transition
    route_transition
    closure_transition
    transition_class
    source_file
    source_note
    notes

These files are for audit, documentation, and later analysis.

The files in:

    ladders/phase3_transitions/one_column/

contain only:

    value

These are the files to upload to STRUC-PERC-I and STRUC-I.


Encodings Built
---------------
The script builds twelve encodings:

    charge_balance_error
    initial_total_charge
    final_total_charge
    charged_multiplicity_delta
    neutral_multiplicity_delta
    layer_transition_code
    route_transition_code
    closure_transition_code
    boundary_preservation_code
    externalization_delta
    composite_count_delta
    transition_class_code


Encoding Meaning
----------------

charge_balance_error
    Absolute charge-balance error for each transition.
    For the current allowed seed corpus this should be 0 for every row.

initial_total_charge
    Total external charge before the transition.

final_total_charge
    Total external charge after the transition.

charged_multiplicity_delta
    Number of charged final objects minus number of charged initial objects.

neutral_multiplicity_delta
    Number of neutral final objects minus number of neutral initial objects.

layer_transition_code
    Numeric code assigned to the full layer transition pattern, for example:
        C -> C;A;A
        C -> A;A
        A -> A;A

route_transition_code
    Numeric code assigned to the full route-class transition pattern.

closure_transition_code
    Numeric code assigned to the full closure-class transition pattern.

boundary_preservation_code
    1 for allowed charge-boundary-preserving seed transitions.
    Later constrained or forbidden transitions may use another value.

externalization_delta
    Number of external final objects minus number of external initial objects.

composite_count_delta
    Number of composite final objects minus number of composite initial objects.

transition_class_code
    Numeric code assigned to the transition_class field.


Expected Constant Encodings
---------------------------
For the current Phase 3 seed corpus, two encodings are expected to be constant:

    charge_balance_error
    boundary_preservation_code

This is correct.

Reason:

    the seed corpus contains allowed charge-conserving transitions only.

Therefore:

    charge_balance_error = 0
    boundary_preservation_code = 1

These two files are useful as diagnostics, but they are not good first chamber
inputs because STRUC-PERC-I or STRUC-I may reject constant ladders or return
uninformative output.


Recommended First Chamber Inputs
--------------------------------
Use these one-column files first:

    ladders/phase3_transitions/one_column/
        phase3_transition_ladder_initial_total_charge.csv
        phase3_transition_ladder_final_total_charge.csv
        phase3_transition_ladder_charged_multiplicity_delta.csv
        phase3_transition_ladder_neutral_multiplicity_delta.csv
        phase3_transition_ladder_layer_transition_code.csv
        phase3_transition_ladder_route_transition_code.csv
        phase3_transition_ladder_closure_transition_code.csv
        phase3_transition_ladder_externalization_delta.csv
        phase3_transition_ladder_composite_count_delta.csv
        phase3_transition_ladder_transition_class_code.csv

Skip these in the first chamber run:

    phase3_transition_ladder_charge_balance_error.csv
    phase3_transition_ladder_boundary_preservation_code.csv

They can be retained as invariant diagnostics.


Recommended STRUC-PERC-I Output Placement
-----------------------------------------
After running STRUC-PERC-I, save the exported results here:

    charge_boundary_routing_i/
    └── results/
        └── struc_perc_i/
            └── phase3_transitions/
                ├── PHASE3_TRANSITIONS_STRUC_PERC_I_v2_5_0_batch_results.csv
                └── PHASE3_TRANSITIONS_STRUC_PERC_I_v2_5_0_batch_results.json


Recommended STRUC-I Output Placement
------------------------------------
After running STRUC-I on the same selected one-column files, save exports here:

    charge_boundary_routing_i/
    └── results/
        └── struc_i/
            └── phase3_transitions/
                ├── PHASE3_TRANSITIONS_STRUC_I_v1_0_4_profiles.csv
                └── PHASE3_TRANSITIONS_STRUC_I_v1_0_4_results.json


Diagnostics
-----------
The diagnostics folder contains:

    phase3_transition_ladder_summary.json
    README_phase3_transition_ladder_diagnostics.txt

Use the diagnostics to verify:

    number of rows
    number of unique values per encoding
    which encodings are constant
    categorical codebooks
    full list of written files

The codebooks are important because categorical encodings such as:

    layer_transition_code
    route_transition_code
    closure_transition_code
    transition_class_code

are numeric only after deterministic category-to-code assignment.


Important Operational Note
--------------------------
Do not interpret categorical code values as physical magnitudes.

For example:

    layer_transition_code = 1
    layer_transition_code = 2

does not mean transition 2 is twice transition 1.

It only means distinct layer-transition patterns have been mapped into
stable numeric codes so the chambers can process them.

The interpretation must return to the diagnostics/codebook.


What This Script Does Not Do
----------------------------
This script does not:

    create the canonical transition corpus
    parse PDG PDFs
    run STRUC-PERC-I
    run STRUC-I
    decide physical correctness of reactions
    produce the final Phase 3 comparison report

It only transforms the canonical Phase 3 transition corpus into chamber-ready
numeric ladders.


Correct Phase 3 Order
---------------------
Use this order:

    1. python scripts\build_phase3_transition_corpus.py
    2. python scripts\build_phase3_transition_ladders.py
    3. Inspect ladders/phase3_transitions/diagnostics/
    4. Upload selected non-constant one-column ladders to STRUC-PERC-I
    5. Save STRUC-PERC-I results
    6. Upload same selected one-column ladders to STRUC-I
    7. Save STRUC-I results
    8. Produce Phase 3 transition chamber comparison report


Relation to Phase 2C
--------------------
Do not mix Phase 2C into this script.

Phase 2C remains the reserved validation/control:

    Same-Charge Different-Route Control

Reserved objects:

    positron
    proton
    pi+
    K+
    W+

Expected control result:

    same Q = +1 does not imply same structural route.

Phase 2C should have its own corpus, ladders, results, and report folders.


Canonical Interpretation
------------------------
The canonical Phase 3 interpretation is:

    Charge conservation is the visible projection.
    Boundary-route preservation is the structural invariant.

This script creates the ladder objects needed to test that statement
empirically with STRUC-PERC-I and STRUC-I.
