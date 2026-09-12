Charge Boundary Routing I
Phase 3B — Expanded Allowed Transition Corpus
README_build_phase3B_expanded_transition_ladders.txt

Generated: 2026-06-15


Purpose
-------
This README documents:

    scripts/build_phase3B_expanded_transition_ladders.py

The script reads the Phase 3B expanded allowed-transition corpus and builds
numeric chamber-ready ladders for STRUC-PERC-I and STRUC-I.

It is the second Phase 3B build step.

The first Phase 3B script is:

    scripts/build_phase3B_expanded_transition_corpus.py

That script writes:

    data/canonical/phase3B_expanded_allowed_transition_corpus.csv

This ladder script reads that CSV and creates:

    full provenance ladders
    one-column chamber upload ladders
    diagnostics and codebooks


Where to Place the Script
-------------------------
Place the script here:

    charge_boundary_routing_i/
    └── scripts/
        └── build_phase3B_expanded_transition_ladders.py


Required Input
--------------
Before running this script, this file must exist:

    charge_boundary_routing_i/
    └── data/
        └── canonical/
            └── phase3B_expanded_allowed_transition_corpus.csv

Create it by running:

    python scripts\build_phase3B_expanded_transition_corpus.py


How to Run
----------
Run from the project root:

    python scripts\build_phase3B_expanded_transition_ladders.py

Expected project root:

    charge_boundary_routing_i/


Files Written
-------------
The script writes full provenance ladders to:

    charge_boundary_routing_i/
    └── ladders/
        └── phase3B_expanded_transitions/
            ├── phase3B_expanded_transition_ladder_charge_balance_error.csv
            ├── phase3B_expanded_transition_ladder_initial_total_charge.csv
            ├── phase3B_expanded_transition_ladder_final_total_charge.csv
            ├── phase3B_expanded_transition_ladder_charged_multiplicity_delta.csv
            ├── phase3B_expanded_transition_ladder_neutral_multiplicity_delta.csv
            ├── phase3B_expanded_transition_ladder_layer_transition_code.csv
            ├── phase3B_expanded_transition_ladder_route_transition_code.csv
            ├── phase3B_expanded_transition_ladder_closure_transition_code.csv
            ├── phase3B_expanded_transition_ladder_category_transition_code.csv
            ├── phase3B_expanded_transition_ladder_boundary_preservation_code.csv
            ├── phase3B_expanded_transition_ladder_externalization_delta.csv
            ├── phase3B_expanded_transition_ladder_composite_count_delta.csv
            ├── phase3B_expanded_transition_ladder_transition_class_code.csv
            ├── phase3B_expanded_transition_ladder_transition_family_code.csv
            ├── phase3B_expanded_transition_ladder_initial_multiplicity.csv
            ├── phase3B_expanded_transition_ladder_final_multiplicity.csv
            ├── phase3B_expanded_transition_ladder_charged_initial_count.csv
            ├── phase3B_expanded_transition_ladder_charged_final_count.csv
            ├── phase3B_expanded_transition_ladder_neutral_initial_count.csv
            ├── phase3B_expanded_transition_ladder_neutral_final_count.csv
            ├── phase3B_expanded_transition_ladder_composite_initial_count.csv
            ├── phase3B_expanded_transition_ladder_composite_final_count.csv
            ├── phase3B_expanded_transition_ladder_external_initial_count.csv
            └── phase3B_expanded_transition_ladder_external_final_count.csv

It writes one-column chamber upload versions to:

    charge_boundary_routing_i/
    └── ladders/
        └── phase3B_expanded_transitions/
            └── one_column/

It writes diagnostics to:

    charge_boundary_routing_i/
    └── ladders/
        └── phase3B_expanded_transitions/
            └── diagnostics/
                ├── phase3B_expanded_transition_ladder_summary.json
                └── README_phase3B_expanded_transition_ladder_diagnostics.txt


Full Provenance vs One-Column Files
-----------------------------------
Full provenance ladder files preserve:

    value
    transition_id
    transition_name
    phase
    batch
    transition_family
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
    category_transition
    transition_class
    source_file
    source_note
    notes

Use full provenance files for audit and interpretation.

Use one-column files for chamber upload.

One-column files contain only:

    value


Encodings Built
---------------
This script builds 24 encodings:

    charge_balance_error
    initial_total_charge
    final_total_charge
    charged_multiplicity_delta
    neutral_multiplicity_delta
    layer_transition_code
    route_transition_code
    closure_transition_code
    category_transition_code
    boundary_preservation_code
    externalization_delta
    composite_count_delta
    transition_class_code
    transition_family_code
    initial_multiplicity
    final_multiplicity
    charged_initial_count
    charged_final_count
    neutral_initial_count
    neutral_final_count
    composite_initial_count
    composite_final_count
    external_initial_count
    external_final_count


Primary Phase 3B Robustness Targets
-----------------------------------
Phase 3 seed found weak persistence in:

    route_transition_code
    closure_transition_code
    transition_class_code
    initial_total_charge
    final_total_charge

Phase 3B should first check whether this remains true in the expanded corpus.

Primary one-column files to test first:

    phase3B_expanded_transition_ladder_route_transition_code.csv
    phase3B_expanded_transition_ladder_closure_transition_code.csv
    phase3B_expanded_transition_ladder_transition_class_code.csv
    phase3B_expanded_transition_ladder_transition_family_code.csv
    phase3B_expanded_transition_ladder_category_transition_code.csv
    phase3B_expanded_transition_ladder_initial_total_charge.csv
    phase3B_expanded_transition_ladder_final_total_charge.csv


Expected Constant Encodings
---------------------------
For the expanded allowed-transition corpus, these may be constant:

    charge_balance_error
    boundary_preservation_code

Reason:

    Phase 3B contains allowed charge-preserving transitions only.

Therefore:

    charge_balance_error = 0
    boundary_preservation_code = 1

Keep these as invariant diagnostics, but do not upload them first if the
diagnostics confirms they are constant.


Categorical Code Warning
------------------------
Do not interpret categorical code values as physical magnitudes.

For example:

    route_transition_code = 5

does not mean it is physically greater than:

    route_transition_code = 2

The code is only a deterministic numeric label so the chamber can process the
category. Interpretation must return to the diagnostics codebook.


Recommended STRUC-PERC-I Output Placement
-----------------------------------------
After STRUC-PERC-I, save exports here:

    charge_boundary_routing_i/
    └── results/
        └── struc_perc_i/
            └── phase3B_expanded_transitions/
                ├── PHASE3B_EXPANDED_STRUC_PERC_I_v2_5_0_batch_results.csv
                └── PHASE3B_EXPANDED_STRUC_PERC_I_v2_5_0_batch_results.json


Recommended STRUC-I Output Placement
------------------------------------
After STRUC-I, save exports here:

    charge_boundary_routing_i/
    └── results/
        └── struc_i/
            └── phase3B_expanded_transitions/
                ├── PHASE3B_EXPANDED_STRUC_I_v1_0_4_profiles.csv
                └── PHASE3B_EXPANDED_STRUC_I_v1_0_4_results.json

If exported in multiple batches, label them:

    PHASE3B_EXPANDED_STRUC_I_v1_0_4_profiles_part1.csv
    PHASE3B_EXPANDED_STRUC_I_v1_0_4_results_part1.json
    PHASE3B_EXPANDED_STRUC_I_v1_0_4_profiles_part2.csv
    PHASE3B_EXPANDED_STRUC_I_v1_0_4_results_part2.json


Correct Phase 3B Order
----------------------
Use this order:

    1. python scripts\build_phase3B_expanded_transition_corpus.py
    2. python scripts\build_phase3B_expanded_transition_ladders.py
    3. Inspect ladders/phase3B_expanded_transitions/diagnostics/
    4. Upload selected non-constant one-column ladders to STRUC-PERC-I
    5. Save STRUC-PERC-I results
    6. Upload same selected one-column ladders to STRUC-I
    7. Save STRUC-I results
    8. Produce Phase 3B expanded transition comparison report


What This Script Does Not Do
----------------------------
This script does not:

    create the expanded corpus
    parse PDG PDFs
    run STRUC-PERC-I
    run STRUC-I
    decide physical correctness of reactions
    produce the final Phase 3B comparison report

It only transforms the canonical Phase 3B corpus into chamber-ready numeric
ladders.


Relation to Phase 2C
--------------------
Do not mix Phase 2C into this script.

Phase 2C remains separate:

    Phase 2C — Same-Charge Different-Route Control

Expected control result:

    same Q = +1 does not imply same structural route.
