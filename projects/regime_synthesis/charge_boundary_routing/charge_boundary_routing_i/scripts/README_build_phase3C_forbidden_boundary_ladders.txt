Charge Boundary Routing I
Phase 3C Forbidden Boundary Ladder Generator
README_build_phase3C_forbidden_boundary_ladders.txt

Place this script here:

    charge_boundary_routing_i/
    └── scripts/
        └── build_phase3C_forbidden_boundary_ladders.py

Required input:

    charge_boundary_routing_i/
    └── data/
        └── canonical/
            └── phase3C_forbidden_constrained_transition_corpus.csv

Run from project root:

    python scripts\build_phase3C_forbidden_boundary_ladders.py

It writes:

    data/derived/
        phase3C_forbidden_constrained_transition_summary.json

    ladders/phase3C_forbidden_boundary/
        phase3C_ladder_<encoding>.csv

    ladders/phase3C_forbidden_boundary/one_column/
        phase3C_ladder_<encoding>.csv

    ladders/phase3C_forbidden_boundary/diagnostics/
        phase3C_encoding_manifest.csv
        phase3C_category_codebook.json
        phase3C_transition_audit.csv
        phase3C_balance_check.csv
        phase3C_group_counts.json
        phase3C_expected_behavior_summary.json

It also creates:

    results/struc_perc_i/phase3C_forbidden_boundary/
    results/struc_i/phase3C_forbidden_boundary/
    outputs/reports/phase3C_forbidden_boundary/

First STRUC-PERC-I uploads should come from:

    ladders/phase3C_forbidden_boundary/one_column/

Primary files:

    phase3C_ladder_route_charge_consistency_code.csv
    phase3C_ladder_closure_charge_consistency_code.csv
    phase3C_ladder_allowed_vs_forbidden_code.csv
    phase3C_ladder_boundary_pressure_index.csv
    phase3C_ladder_boundary_response_code.csv
    phase3C_ladder_route_transition_code.csv
    phase3C_ladder_closure_transition_code.csv
    phase3C_ladder_transition_class_code.csv
    phase3C_ladder_transition_status_code.csv
    phase3C_ladder_charge_balance_abs_error.csv
    phase3C_ladder_electric_charge_violation_flag.csv
    phase3C_ladder_free_fractional_externalization_flag.csv
    phase3C_ladder_selection_violation_flag.csv
    phase3C_ladder_route_incoherence_flag.csv
    phase3C_ladder_forbidden_flag.csv

Do not upload constant or n_unique < 2 encodings first.
Check:

    ladders/phase3C_forbidden_boundary/diagnostics/phase3C_encoding_manifest.csv
