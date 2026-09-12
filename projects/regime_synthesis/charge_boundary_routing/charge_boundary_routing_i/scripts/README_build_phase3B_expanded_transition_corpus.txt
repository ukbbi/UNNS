Charge Boundary Routing I
Phase 3B — Expanded Allowed Transition Corpus
README_build_phase3B_expanded_transition_corpus.txt

Generated: 2026-06-15

Purpose
-------
This README documents:

    scripts/build_phase3B_expanded_transition_corpus.py

The script builds a larger allowed-transition corpus for Phase 3B.

Phase 3B question:

    Do route_transition_code and closure_transition_code remain weakly
    persistent when the transition corpus grows beyond the 7-transition seed?

Place
-----
Place the script here:

    charge_boundary_routing_i/
    └── scripts/
        └── build_phase3B_expanded_transition_corpus.py

Run
---
Run from project root:

    python scripts\build_phase3B_expanded_transition_corpus.py

Writes
------
Canonical corpus:

    data/canonical/phase3B_expanded_allowed_transition_corpus.csv

Summary:

    data/derived/phase3B_expanded_allowed_transition_summary.json

Prepared folders:

    ladders/phase3B_expanded_transitions/
    ladders/phase3B_expanded_transitions/one_column/
    ladders/phase3B_expanded_transitions/diagnostics/
    results/struc_perc_i/phase3B_expanded_transitions/
    results/struc_i/phase3B_expanded_transitions/
    outputs/reports/phase3B_expanded_transitions/

Corpus Scope
------------
The expanded corpus contains 38 allowed transitions:

    7 original Phase 3 seed-continuity transitions
    31 new expansion transitions

Expansion families:

    charged_meson_decay
    neutral_meson_decay
    baryon_decay
    baryon_resonance_decay
    w_z_mediated_channel
    radiative_decay

Important
---------
This is a controlled robustness corpus, not a complete particle-decay database.

All rows are intended as allowed charge-preserving transitions.

Phase 2C remains separate:

    Phase 2C — Same-Charge Different-Route Control
