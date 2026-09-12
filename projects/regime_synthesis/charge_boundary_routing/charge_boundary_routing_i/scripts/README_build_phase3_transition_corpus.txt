Charge Boundary Routing I
Phase 3 — Closure-Preserving Transitions
README_build_phase3_transition_corpus.txt

Generated: 2026-06-15


Purpose
-------
This README documents:

    scripts/build_phase3_transition_corpus.py

The script starts Phase 3 of Charge Boundary Routing I by building the seed
transition corpus for closure-preserving particle transitions.

Phase 3 moves the project from:

    Phase 1 — static boundary classification
    Phase 2 — cross-layer bridge geometry

to:

    Phase 3 — dynamic closure-preserving transitions


Core Question
-------------
Do allowed particle transitions preserve the charge-boundary invariant while
routing identity between different structural regimes?

This is stronger than ordinary charge conservation.

Ordinary projection:

    sum(Q_initial) = sum(Q_final)

Phase 3 structural question:

    Is the transition an admissible route between closure regimes?


Input Status
------------
The script is self-contained.

It does not require raw PDG parsing at runtime.

Instead, it uses a small canonical seed registry of transition objects and
allowed seed transitions. Source PDFs are referenced in metadata fields so the
corpus remains provenance-aware.


Where to Place the Script
-------------------------
Place the script here:

    charge_boundary_routing_i/
    └── scripts/
        └── build_phase3_transition_corpus.py


How to Run
----------
Run from the project root:

    python scripts\build_phase3_transition_corpus.py

Expected project root:

    charge_boundary_routing_i/


Files Written
-------------
The script writes:

    charge_boundary_routing_i/
    └── data/
        ├── canonical/
        │   └── phase3_closure_preserving_transitions.csv
        └── derived/
            └── phase3_transition_summary.json


Folders Prepared
----------------
The script also prepares the Phase 3 working folders:

    charge_boundary_routing_i/
    ├── ladders/
    │   └── phase3_transitions/
    │       ├── one_column/
    │       └── diagnostics/
    │
    ├── results/
    │   ├── struc_perc_i/
    │   │   └── phase3_transitions/
    │   └── struc_i/
    │       └── phase3_transitions/
    │
    └── outputs/
        └── reports/
            └── phase3_transitions/


Seed Transitions
----------------
The initial Phase 3 seed corpus contains seven controlled transitions:

    T001 — neutron_beta_decay
           n -> p + e- + anti_nu_e

    T002 — positive_pion_muonic_decay
           pi+ -> mu+ + nu_mu

    T003 — negative_muon_decay
           mu- -> e- + anti_nu_e + nu_mu

    T004 — w_minus_leptonic_decay
           W- -> e- + anti_nu_e

    T005 — w_plus_leptonic_decay
           W+ -> e+ + nu_e

    T006 — neutral_pion_two_photon_decay
           pi0 -> gamma + gamma

    T007 — positive_kaon_muonic_decay
           K+ -> mu+ + nu_mu


Why These Transitions
---------------------
The seed is intentionally small.

It is designed to test several transition forms:

    composite -> composite + external + neutral
    composite -> external + neutral
    external -> external + neutral
    neutral composite -> neutral radiation closure

This lets Phase 3 test dynamic routing without immediately becoming a full
particle-decay database.


Phase 1 Layer Codes Used
------------------------
The script preserves the Phase 1 layer language:

    A = primitive external integer / neutral charge closures
    B = confined fractional internal charge coordinates
    C = composite integer / neutral charge closures
    D = boundary absences / empirical constraints

Phase 3 seed transitions mostly use A and C because they are allowed external
or composite transitions. Layer B and D remain structurally relevant through
the already-completed Phase 2 bridge interpretation and later control sets.


Important Fields in the CSV
---------------------------
The canonical CSV contains the following main field groups:

Identity:

    transition_id
    transition_name
    initial_objects
    final_objects
    initial_symbols
    final_symbols

Charge closure:

    initial_Q_sum
    final_Q_sum
    charge_balance_error
    charge_conserved

Layer routing:

    initial_layers
    final_layers
    layer_transition

Route and closure classes:

    initial_route_classes
    final_route_classes
    route_transition
    initial_closure_classes
    final_closure_classes
    closure_transition

Multiplicity and structural deltas:

    initial_multiplicity
    final_multiplicity
    charged_initial_count
    charged_final_count
    neutral_initial_count
    neutral_final_count
    charged_multiplicity_delta
    neutral_multiplicity_delta
    composite_initial_count
    composite_final_count
    external_initial_count
    external_final_count
    composite_count_delta
    externalization_delta

Boundary preservation:

    boundary_preservation_code
    boundary_route_preserved

Classification and provenance:

    transition_class
    source_file
    source_note
    notes


Transition Classes
------------------
Initial transition_class values include:

    COMPOSITE_TO_COMPOSITE_PLUS_EXTERNALS
    COMPOSITE_TO_EXTERNALS
    LEPTONIC_EXTERNAL_DECAY
    EXTERNAL_TO_EXTERNALS
    NEUTRAL_COMPOSITE_TO_RADIATION


Expected Output Logic
---------------------
All seed transitions are allowed charge-conserving transitions.

Therefore:

    charge_balance_error = 0
    charge_conserved = TRUE
    boundary_preservation_code = 1
    boundary_route_preserved = TRUE

Later Phase 3 expansions may include forbidden or constrained transitions with:

    boundary_preservation_code = 0

or another explicit code, if needed.


What This Script Does Not Do
----------------------------
This script does not:

    parse PDG PDFs
    build chamber ladders
    run STRUC-PERC-I
    run STRUC-I
    produce figures
    produce the final Phase 3 report

It only builds the canonical Phase 3 seed corpus and summary.


Next Script
-----------
After this script runs successfully, the next script should be:

    scripts/build_phase3_transition_ladders.py

That next script should read:

    data/canonical/phase3_closure_preserving_transitions.csv

and write numeric chamber-ready ladders into:

    ladders/phase3_transitions/
    ladders/phase3_transitions/one_column/
    ladders/phase3_transitions/diagnostics/


Recommended Phase 3 Chamber Encodings
-------------------------------------
The next ladder builder should probably create numeric ladders such as:

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

The most important first-pass encodings are:

    charge_balance_error
    layer_transition_code
    route_transition_code
    closure_transition_code
    boundary_preservation_code


Relation to Phase 2C
--------------------
Do not mix the +1 same-charge route control into this Phase 3 seed corpus.

Keep it separate as:

    Phase 2C — Same-Charge Different-Route Control

Reserved control objects:

    positron
    proton
    pi+
    K+
    W+

Expected Phase 2C result:

    same Q = +1 does not imply same structural route.


Operational Rule
----------------
Phase 3 begins only after the canonical transition corpus exists.

Correct order:

    1. Run build_phase3_transition_corpus.py
    2. Confirm data/canonical/phase3_closure_preserving_transitions.csv exists
    3. Confirm data/derived/phase3_transition_summary.json exists
    4. Build Phase 3 transition ladders
    5. Run STRUC-PERC-I
    6. Run STRUC-I
    7. Produce Phase 3 transition chamber comparison report


Canonical Interpretation
------------------------
The canonical interpretation of Phase 3 is:

    Charge conservation is the visible projection.
    Boundary-route preservation is the structural invariant.

This is the dynamic continuation of the Phase 1 and Phase 2 result:

    equal charge value does not imply equal structural route.
