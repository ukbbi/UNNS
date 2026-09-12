Charge Boundary Routing I
Phase 1 Verified Corpus Builder
README.txt

Purpose
-------

This folder/script regenerates the verified canonical Phase 1 corpus for the
Charge Boundary Routing I project.

The Phase 1 corpus is the curated empirical foundation for testing the UNNS
charge-boundary hypothesis:

    External charge observability appears only as integer or neutral closure,
    while fractional charge appears as a confined internal coordinate or as a
    non-externalized boundary case.

The builder does not attempt to infer the charge law directly. It produces the
controlled A-D classification corpus needed before ladder construction,
STRUC-PERC-I analysis, STRUC-I analysis, bridge comparison, or manuscript
synthesis.


Expected Location
-----------------

Place the script here:

    charge_boundary_routing_i/
    └── scripts/
        └── build_phase1_verified_corpus.py

Run it from the project root:

    cd "path\to\charge_boundary_routing_i"
    python scripts\build_phase1_verified_corpus.py


Required Project Folders
------------------------

The script creates missing output folders automatically, but the project should
normally have this structure:

    charge_boundary_routing_i/
    │
    ├── README.txt
    ├── PROJECT_SCOPE.txt
    ├── CITATION.txt
    │
    ├── data/
    │   ├── raw/
    │   │   └── pdg/
    │   ├── canonical/
    │   └── derived/
    │
    ├── scripts/
    │   └── build_phase1_verified_corpus.py
    │
    └── outputs/
        └── reports/


Required Source PDFs
--------------------

Keep the PDG source PDFs here:

    charge_boundary_routing_i/
    └── data/
        └── raw/
            └── pdg/
                ├── rpp2026-sum-leptons.pdf
                ├── rpp2026-sum-gauge-higgs-bosons.pdf
                ├── rpp2026-sum-quarks.pdf
                ├── rpp2026-sum-mesons.pdf
                ├── rpp2026-sum-baryons.pdf
                └── rpp2026-sum-searches.pdf

These PDFs are the provenance basis for the curated canonical tables.

Important: the builder does not parse the PDFs automatically. That is deliberate.
PDF extraction is brittle and can silently corrupt notation such as ±, fractions,
bars, antiparticles, and charge-conjugation symbols. The script is a curated
canonical builder: the PDG PDFs remain the evidence, and the script regenerates
the verified CSV tables from explicitly encoded source-backed rows.


Generated Files
---------------

After running the script, it writes:

    data/canonical/
        phase1_layerA_external_closures.csv
        phase1_layerB_confined_fractional.csv
        phase1_layerC_composite_closures.csv
        phase1_layerD_boundary_absences.csv

    data/derived/
        charge_boundary_phase1_combined.csv
        charge_boundary_phase1_verified_summary.json

    outputs/reports/
        phase1_verified_canonical_report.txt


Layer Definitions
-----------------

Layer A: Primitive External Closures

    Externally observable, non-confined particles with integer or neutral
    electric charge.

    Includes:
        electron / positron
        muon / antimuon
        tau / antitau
        electron, muon, tau neutrinos
        photon
        W- / W+
        Z
        Higgs

    Main role:
        establish the primitive external integer-neutral baseline.

Layer B: Confined Fractional Coordinates

    Quarks and antiquarks with fractional electric charge.

    Includes:
        u, d, s, c, b, t
        anti-u, anti-d, anti-s, anti-c, anti-b, anti-t

    Main role:
        establish fractional charge as locally valid but not externally free.

Layer C: Composite Closures

    Hadronic composite states whose internal fractional charges close to
    integer or neutral external charge.

    Seed verified set includes:
        proton
        neutron
        pi+
        pi0
        pi-
        K+
        K0
        K-
        Delta++
        Omega-

    Main role:
        test whether fractional internal coordinates route into integer or
        neutral external closure.

Layer D: Boundary Absences / Boundary Constraints

    Negative or constraint cases marking the externalization boundary.

    Includes:
        free quark searches
        magnetic monopole searches
        proton-electron charge-balance constraint
        neutron charge-violating decay constraint

    Main role:
        capture what fails to externalize or is tightly constrained at the
        charge boundary.


Canonical Schema
----------------

All CSV files use the same schema:

    object_id
    phase
    layer
    pdg_section
    pdg_name
    symbol
    category
    generation
    components
    component_charges
    Q_over_e
    anti_symbol
    anti_Q_over_e
    free_external
    confined
    fractional_internal
    integer_external
    neutral_external
    closure_error
    closure_class
    route_class
    source_file
    source_note
    notes

This unified schema keeps Layers A-D compatible for later merging, ladder
construction, validation, and route classification.


Classification Vocabulary
-------------------------

Primary closure classes:

    FREE_INTEGER_CLOSURE
    FREE_NEUTRAL_CLOSURE
    INTERNAL_FRACTIONAL_COORDINATE
    COMPOSITE_INTEGER_CLOSURE
    COMPOSITE_NEUTRAL_CLOSURE
    TERMINAL_FREE_FRACTIONAL
    UNRESOLVED_DUAL_BOUNDARY
    CONSTRAINED_NEUTRALITY_BOUNDARY
    CONSTRAINED_CHARGE_VIOLATION_BOUNDARY

Primary route classes:

    EXTERNAL_CLOSURE
    CONFINED_ROUTE
    COMPOSITE_CLOSURE
    BOUNDARY_ABSENCE
    DUAL_BOUNDARY_CANDIDATE
    BOUNDARY_CONSTRAINT


Expected Row Counts
-------------------

The current verified Phase 1 corpus contains:

    Layer A: 14 rows
    Layer B: 12 rows
    Layer C: 10 rows
    Layer D: 4 rows
    Total:   40 rows


What This Builder Does
----------------------

The script:

    1. Defines the canonical schema.
    2. Encodes verified Layer A-D rows.
    3. Writes one canonical CSV per layer.
    4. Writes a combined Phase 1 CSV.
    5. Writes a JSON summary.
    6. Writes a short local report.

It is intended to make the project reproducible locally. If the CSV files are
lost, edited incorrectly, or need to be regenerated in a clean clone, rerun this
script.


What This Builder Does Not Do
-----------------------------

The script does not:

    - parse PDG PDFs automatically;
    - run STRUC-PERC-I;
    - run STRUC-I;
    - build numeric ladder files;
    - perform alpha-deformation;
    - perform bridge analysis;
    - claim a final law of electric charge.

The generated CSV files are canonical corpus tables, not chamber-ready ladders.


Next Step After Running
-----------------------

After confirming the generated files, proceed to ladder construction:

    scripts/
        build_charge_ladders.py

Expected future ladder outputs:

    ladders/
        layerA_external_charge_ladder.csv
        layerB_fractional_charge_ladder.csv
        layerC_composite_closure_ladder.csv
        layerD_boundary_absence_ladder.csv
        ABCD_charge_boundary_ladder.csv

Only after that should STRUC-PERC-I and STRUC-I be run.


Recommended Workflow
--------------------

    1. Place PDG PDFs in data/raw/pdg/.
    2. Run scripts/build_phase1_verified_corpus.py.
    3. Check data/canonical/ files.
    4. Check data/derived/charge_boundary_phase1_combined.csv.
    5. Read outputs/reports/phase1_verified_canonical_report.txt.
    6. Build numeric charge ladders.
    7. Run STRUC-PERC-I.
    8. Run STRUC-I.
    9. Compare route classes.
    10. Update manuscript notes and project reports.


Interpretive Status
-------------------

This Phase 1 corpus supports the first controlled empirical framing:

    Primitive external charge states appear as integer or neutral closures.
    Fractional charge appears as a confined internal coordinate.
    Composite hadrons show fractional internal coordinates closing into integer
    or neutral external states.
    Free fractional charge remains a boundary absence in the verified source set.

This is not yet the final UNNS charge law. It is the first reproducible
charge-boundary classification layer from which the law-shape may later be
tested.
