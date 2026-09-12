CHARGE BOUNDARY ROUTING I
Fractional Charge as Confined Route, Integer Charge as External Closure

UNNS Substrate Research Program
Project code: CBR-I
Working folder: charge_boundary_routing_i

1. PROJECT THESIS

Charge Boundary Routing I tests whether the empirical distinction between externally observable electric charge and confined fractional charge can be expressed as a UNNS boundary-routing phenomenon.

The guiding hypothesis is:

    External charge observability requires charge-boundary closure.
    Fractional charge is permitted as an internal confined route coordinate,
    but does not appear as a freely externalized state unless it closes into
    an integer or neutral boundary charge.

This project does not attempt to reproduce the full Particle Data Group database. It builds a small, controlled corpus for testing a structural UNNS question:

    Does external charge observability coincide with integer or neutral closure,
    while fractional charge appears only as confined internal structure or as
    a non-externalized boundary case?

2. CURRENT PROJECT STAGE

Current stage:

    Phase 1 — Charge Boundary Classification
    Layer A — Primitive External Charge Closures

Layer A establishes the baseline of externally observable, non-confined Standard Model particles whose electric charge is integer or neutral.

Layer A source files:

    data/raw/pdg/rpp2026-sum-leptons.pdf
    data/raw/pdg/rpp2026-sum-gauge-higgs-bosons.pdf

Layer A canonical output:

    data/canonical/phase1_layerA_external_closures.csv

3. FOLDER STRUCTURE

Recommended project layout:

    charge_boundary_routing_i/
    |
    |-- README.txt
    |-- PROJECT_SCOPE.txt
    |-- CITATION.txt
    |
    |-- data/
    |   |-- raw/
    |   |   |-- pdg/
    |   |   |   |-- rpp2026-sum-leptons.pdf
    |   |   |   |-- rpp2026-sum-gauge-higgs-bosons.pdf
    |   |   |
    |   |   |-- notes/
    |   |
    |   |-- canonical/
    |   |   |-- phase1_layerA_external_closures.csv
    |   |   |-- phase1_layerB_confined_fractional.csv
    |   |   |-- phase1_layerC_composite_closures.csv
    |   |   |-- phase1_layerD_boundary_absences.csv
    |   |
    |   |-- derived/
    |       |-- charge_closure_classified.csv
    |       |-- charge_boundary_summary.json
    |
    |-- schemas/
    |   |-- phase1_charge_boundary_schema.json
    |   |-- layerA_schema.json
    |   |-- layerB_schema.json
    |   |-- layerC_schema.json
    |   |-- layerD_schema.json
    |
    |-- scripts/
    |   |-- validate_layerA.py
    |   |-- build_charge_ladders.py
    |   |-- classify_charge_routes.py
    |   |-- summarize_phase1.py
    |
    |-- notebooks/
    |   |-- phase1_exploration.ipynb
    |
    |-- ladders/
    |   |-- layerA_external_charge_ladder.csv
    |   |-- layerB_fractional_charge_ladder.csv
    |   |-- layerC_composite_closure_ladder.csv
    |   |-- ABC_charge_boundary_ladder.csv
    |
    |-- results/
    |   |-- struc_perc_i/
    |   |-- struc_i/
    |
    |-- outputs/
    |   |-- tables/
    |   |-- figures/
    |   |-- reports/
    |
    |-- manuscript/
        |-- outline.txt
        |-- notes.txt
        |-- charge_boundary_routing_i_draft.txt

4. PHASE 1 LAYERS

Layer A — Primitive External Charge Closures

    Purpose:
        Establish the external integer-neutral charge baseline.

    Examples:
        electron, positron, muon, antimuon, tau, antitau,
        electron neutrino, muon neutrino, tau neutrino,
        photon, W-, W+, Z, Higgs.

    Expected classes:
        FREE_INTEGER_CLOSURE
        FREE_NEUTRAL_CLOSURE

Layer B — Confined Fractional Coordinates

    Purpose:
        Establish quark fractional charges as locally valid but externally non-free.

    Examples:
        up, down, strange, charm, bottom, top,
        anti-up, anti-down, anti-strange, anti-charm, anti-bottom, anti-top.

    Expected classes:
        INTERNAL_FRACTIONAL_COORDINATE
        CONFINED_FRACTIONAL_ROUTE

Layer C — Composite Closures

    Purpose:
        Test whether fractional internal components route into integer or neutral external closures.

    Examples:
        proton, neutron, pi+, pi0, pi-, K+, K0, K-, Delta++, Omega-.

    Expected classes:
        COMPOSITE_INTEGER_CLOSURE
        COMPOSITE_NEUTRAL_CLOSURE

Layer D — Boundary Absences and Non-Observed Cases

    Purpose:
        Mark the empirical externalization boundary.

    Examples:
        isolated quark searches, free fractional charge searches,
        magnetic monopole searches, millicharged particle constraints.

    Expected classes:
        TERMINAL_FREE_FRACTIONAL
        UNRESOLVED_DUAL_BOUNDARY
        CONSTRAINED_EXOTIC_BOUNDARY

5. RELATION TO STRUC-PERC-I AND STRUC-I

The raw canonical CSV files are classification corpora, not chamber ladders.

Before using STRUC-PERC-I v2.5.0 or STRUC-I v1.0.4, the corpus rows must be converted into ordered numeric ladder encodings.

STRUC-PERC-I role:

    First connectivity and percolation screen.
    It evaluates whether a charge-route ladder forms a connected structural regime
    or fragments into Tail/Hard behavior.

STRUC-I role:

    Second admissibility-pressure check.
    It tests ordered ladder response under the Universal Structural Law form:

        inv(P_epsilon ; L) <= nu(V_epsilon(L))

    and reports admissibility profiles, pressure regimes, and stability indicators.

Layer A alone will likely be structurally simple because its values are only -1, 0, +1.
The chambers become more meaningful after Layers A, B, and C are compared.

6. CURRENT LAYER A RESULT STATEMENT

Provisional Layer A result:

    Among primitive externally observable, non-confined Standard Model particles
    in the Layer A mini-corpus, electric charge appears only as integer or neutral
    external closure: Q/e in {-1, 0, +1}.

This is not the final law of electric charge. It is the first empirical boundary anchor.

7. NEXT STEP

Proceed to:

    Phase 1 — Layer B: Confined Fractional Coordinates

Download and archive the PDG 2026 Quarks summary table into:

    data/raw/pdg/rpp2026-sum-quarks.pdf

Then create:

    data/canonical/phase1_layerB_confined_fractional.csv

Layer B will test the boundary contrast against Layer A:

    Layer A: external integer-neutral closures
    Layer B: confined fractional coordinates
