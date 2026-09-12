README.txt
UNNS-H Mode Project
Component: edge_event_model_validator.py

============================================================
PURPOSE
============================================================

edge_event_model_validator.py validates the first event-level UNNS-H Mode
edge-admissibility model.

It does NOT run STRUC-I.
It does NOT run STRUC-PERC-I.
It does NOT create a new chamber result.

Instead, it tests the already computed event-level model scores:

    m_edge_event = C_edge_capacity - F_route_fragmentation

The goal is to check whether the formal model genuinely separates the reviewed
TCV suspect shots into meaningful edge-admissibility corridors.

This component belongs after:

    edge_admissibility_event_model.py

and after the model report:

    docs/12_EVENT_LEVEL_EDGE_ADMISSIBILITY_MODEL_REPORT.md


============================================================
WHERE THIS FILE BELONGS
============================================================

Place the validator here:

    unns_hmode_project/
      components/
        edge_event_model_validator.py

This README may be placed beside it as:

    unns_hmode_project/
      components/
        README_edge_event_model_validator.txt

or, if each component folder uses one local README, merge this content into:

    unns_hmode_project/
      components/
        README.txt


============================================================
INPUT FILES
============================================================

Required input:

    outputs/reports/tcv_edge_event_model_scores.csv

This file is produced by:

    components/edge_admissibility_event_model.py

Optional but recommended inputs:

    data/processed/tcv_lh_events_canonical.csv
    outputs/reports/tcv_suspect_shot_review.csv

The validator can run with the score file alone, but the canonical and
shot-review files provide useful context and help preserve traceability.


============================================================
OUTPUT FILES
============================================================

The validator writes:

    outputs/reports/tcv_edge_event_model_validation.csv
    outputs/reports/tcv_edge_event_model_validation.md
    outputs/reports/tcv_edge_event_model_validation_summary.json

Recommended documentation copy:

    docs/13_EDGE_EVENT_MODEL_VALIDATION.md

Copy or rename:

    outputs/reports/tcv_edge_event_model_validation.md

to:

    docs/13_EDGE_EVENT_MODEL_VALIDATION.md


============================================================
RUN COMMAND
============================================================

Run from the project root:

PowerShell:

    python components\edge_event_model_validator.py --scores outputs\reports\tcv_edge_event_model_scores.csv --canonical data\processed\tcv_lh_events_canonical.csv --shot-review outputs\reports\tcv_suspect_shot_review.csv --out-dir outputs\reports

macOS / Linux:

    python components/edge_event_model_validator.py --scores outputs/reports/tcv_edge_event_model_scores.csv --canonical data/processed/tcv_lh_events_canonical.csv --shot-review outputs/reports/tcv_suspect_shot_review.csv --out-dir outputs/reports


============================================================
WHAT THE VALIDATOR TESTS
============================================================

The validator answers five questions:

1. Does m_edge_event separate the reviewed shots into ordered corridors?

2. Do the four observed branch families produce distinct score patterns?

3. Does the model distinguish ILH = 1 from ILH = 0, or is it branch-specific?

4. Which term dominates each event:
       S_power_balance
       S_transport
       S_timing
       S_edge_response
       density support
       species support
       geometry support

5. Which shots remain ambiguous or near the boundary?


============================================================
MODEL TERMS
============================================================

The model being validated is:

    m_edge_event = C_edge_capacity - F_route_fragmentation

where:

    F_route_fragmentation =
        S_power_balance
      + S_transport
      + S_timing

and:

    C_edge_capacity =
        S_edge_response
      + density_support_percentile
      + species_position_percentile
      + geometry_stability

Interpretation:

    If m_edge_event < 0:
        route-fragmentation pressure dominates.
        The event is leakage-like or structurally stressed.

    If m_edge_event is close to 0:
        the event is boundary-ambiguous.
        It may sit near a transition corridor.

    If m_edge_event > 0:
        edge-capacity evidence dominates.
        The event is edge-response / boundary-preserving-like.


============================================================
EXPECTED MODEL STATES
============================================================

The validator expects these model states:

    negative_leakage_margin
    boundary_ambiguous_margin
    positive_boundary_margin

A strong validation result should show ordered separation:

    negative leakage margins < boundary ambiguous margins < positive boundary margins

The validator records this as:

    PASS_STRICT_ORDERING
    PASS_COARSE_ORDERING
    FAIL_OVERLAP
    PARTIAL
    INSUFFICIENT


============================================================
IMPORTANT OUTPUT COLUMNS
============================================================

The CSV output includes:

    SHOT
    TIME
    ILH
    ILH_category
    fragment_tags
    formal_corridor
    m_edge_state
    m_edge_event
    C_edge_capacity
    F_route_fragmentation
    S_power_balance
    S_transport
    S_edge_response
    S_timing
    dominant_fragmentation_term
    dominant_fragmentation_value
    dominant_capacity_term
    dominant_capacity_value
    margin_support_level
    is_boundary_ambiguous
    is_mixed_ilh
    validation_note


============================================================
HOW TO READ THE RESULT
============================================================

The Markdown report is the easiest output to read first:

    outputs/reports/tcv_edge_event_model_validation.md

Look first at:

    Validation status
    Main validation table
    State-level margin summary
    Branch-family score patterns
    Ambiguous shots
    Mixed-ILH shots

The JSON summary is useful for automated downstream reporting:

    outputs/reports/tcv_edge_event_model_validation_summary.json

The CSV is useful for manual sorting, plots, and later figures:

    outputs/reports/tcv_edge_event_model_validation.csv


============================================================
WHAT THIS VALIDATION CAN CLAIM
============================================================

If validation succeeds, we may claim:

    The first event-level UNNS-H Mode margin separates the reviewed TCV
    suspect shots into leakage-like, boundary-ambiguous, and edge-response
    corridors.

We may also claim:

    The four observed branch families can be represented as formal score
    components contributing to route fragmentation and edge capacity.


============================================================
WHAT THIS VALIDATION CANNOT CLAIM
============================================================

Do NOT claim that this proves the physical origin of H-mode.

Do NOT claim that UNNS predicts fusion confinement yet.

Do NOT claim that the reviewed shots are faulty, anomalous, or causal.

Do NOT claim that m_edge_event is the final time-dependent edge margin.

This is an event-level pilot validator only.

The full project still requires:

    time-series data
    edge turbulence diagnostics
    radial electric field / E x B shear information
    pedestal evolution
    confinement-time response
    ELM or boundary-relaxation timing
    cross-machine validation


============================================================
NEXT STEP AFTER RUNNING
============================================================

After running the validator:

1. Open:

       outputs/reports/tcv_edge_event_model_validation.md

2. Copy it to:

       docs/13_EDGE_EVENT_MODEL_VALIDATION.md

3. Inspect whether the model passes strict or coarse ordering.

4. If the result is strong:
       proceed to figures and a first technical note.

5. If the result is weak:
       revise the score weights or component definitions before publication
       writing.


============================================================
PROJECT STATUS AFTER THIS COMPONENT
============================================================

At this point the project has:

    project structure
    TCV ingestion
    STRUC-I baseline
    STRUC-PERC-I fragmentation test
    fragment-isolate mapping
    suspect-shot review
    event-level edge-admissibility model
    model report
    model validation

The next major phase, after validation, is either:

    A. figure generation and technical-note writing

or:

    B. model revision and a second validation pass.
