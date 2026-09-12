Charge Boundary Routing I
Phase 1 — Layer D Non-Applicability Report
README_phase1_layerD_boundary_absence_note.txt

Generated: 2026-06-15

Purpose
-------
This note records the outcome of the attempted Phase 1 — Layer D isolated
chamber tests.

Layer D is the boundary-absence / non-observed-case layer of the Charge
Boundary Routing I corpus. It contains empirical absence and constraint
records rather than ordinary charge-state objects.

Layer D examples include:

    free quark absence
    magnetic monopole absence
    neutron charge-violation constraint
    proton-electron charge mismatch bound

Layer D role in Phase 1:

    Layer A — Primitive External Charge Closures
    Layer B — Confined Fractional Coordinates
    Layer C — Composite Closures
    Layer D — Boundary Absences and Non-observed Cases

Layer D is therefore not an ordinary charge ladder. It is a boundary-marker
layer.


Observed Chamber Behavior
-------------------------
When the six Layer D one-column ladder files were uploaded to STRUC-I v1.0.4,
the chamber rejected all of them with the message:

    No valid numeric ladder found in csv.

The rejected files were:

    layerD_boundary_absence_ladder_absolute_charge.csv
    layerD_boundary_absence_ladder_boundary_route_coordinate.csv
    layerD_boundary_absence_ladder_closure_class_code.csv
    layerD_boundary_absence_ladder_closure_state_code.csv
    layerD_boundary_absence_ladder_route_class_code.csv
    layerD_boundary_absence_ladder_signed_charge.csv

Manual inspection showed that at least one charge-value file contained only:

    value

with no numeric rows below it.

Manual inspection also showed that at least one boundary-coordinate file
contained only a very small numeric sequence:

    value
    1.25
    1.5
    2

This is still too small / too absence-like for STRUC-I v1.0.4 to construct
a meaningful perturbation ladder, gap structure, vulnerability structure,
or Monte Carlo stability profile.


Conclusion
----------
Phase 1 — Layer D cannot be treated as an isolated STRUC-I ladder in the
same way as Layers A, B, and C.

Correct status:

    Phase 1 — Layer D
    STRUC-I isolated test: NOT APPLICABLE / NOT ADMISSIBLE AS INPUT

Reason:

    Layer D contains boundary absences and empirical constraints, not ordinary
    charge-state ladders. Its isolated one-column encodings are either empty
    or too small for STRUC-I v1.0.4 to construct a valid perturbation ladder.

This should not be interpreted as a failed physical result. It is a domain /
layer mismatch: Layer D is not meant to be a standalone numeric ladder.


Scientific Interpretation
-------------------------
Layer D is a boundary-condition layer.

It marks cases where an externalization is absent, forbidden, unresolved,
or strongly constrained. Its role is not to supply ordinary charge values.
Its role is to mark the empirical boundary of charge externalization.

In the Charge Boundary Routing I interpretation:

    Layer A gives external primitive charge closures.
    Layer B gives confined fractional internal coordinates.
    Layer C gives composite integer / neutral closures.
    Layer D gives boundary absences and non-observed externalizations.

Therefore Layer D is best understood as:

    a boundary-marker layer,
    an absence / obstruction layer,
    a constraint layer,
    not an isolated charge-state ladder.


Operational Decision
--------------------
Do not force Layer D through STRUC-I v1.0.4 as a six-file isolated ladder.

For Phase 1, record Layer D isolated STRUC-I status as:

    N/A — not an ordinary numeric ladder.

Do not manually type artificial values into the Layer D CSV files.

Do not patch build_charge_ladders.py yet solely to force Layer D through
STRUC-I.

The present outcome is meaningful and should be preserved:

    Layer D fails as a standalone ladder because it is not a ladder.
    It is a boundary-condition layer.


Relation to STRUC-PERC-I / STRUC-I Workflow
-------------------------------------------
Layers A, B, and C were suitable for isolated chamber testing because they
contain ordinary charge-state or closure-state ladders.

Layer D differs structurally.

Its proper use is likely in the combined ABCD route-space analysis, where it
acts as a boundary condition on the whole charge-routing structure.

Thus the correct Phase 1 interpretation is:

    Layer A — external closure baseline.
    Layer B — internally percolating fractional coordinate layer.
    Layer C — connected composite closure layer.
    Layer D — boundary-marker layer, not STRUC-I-applicable in isolation.

Layer D should therefore appear in the Phase 1 synthesis, but not as a
standalone STRUC-I persistence result.


Recommended Report Language
---------------------------
Use this wording in the Phase 1 synthesis:

    Phase 1 — Layer D was not accepted by STRUC-I v1.0.4 as an isolated
    ladder. The Layer D one-column files were either empty or too small /
    absence-like to support perturbation-ladder construction. This is
    consistent with the design of Layer D: it contains empirical boundary
    absences and constraints, not ordinary charge-state ladders. Layer D is
    therefore treated as a boundary-condition layer whose role is expressed
    in the combined ABCD route-space analysis rather than as an isolated
    STRUC-I persistence result.

Short form:

    Layer D is not a failed ladder. It is the boundary condition of the
    charge-routing ladder.


File Placement
--------------
Save this note as:

    charge_boundary_routing_i/
    └── outputs/
        └── reports/
            └── phase1_layer_resolved/
                └── README_phase1_layerD_boundary_absence_note.txt

Supporting local evidence:

    ladders/one_column/
        layerD_boundary_absence_ladder_absolute_charge.csv
        layerD_boundary_absence_ladder_boundary_route_coordinate.csv
        layerD_boundary_absence_ladder_closure_class_code.csv
        layerD_boundary_absence_ladder_closure_state_code.csv
        layerD_boundary_absence_ladder_route_class_code.csv
        layerD_boundary_absence_ladder_signed_charge.csv

Chamber:

    STRUC-I v1.0.4
    message: No valid numeric ladder found in csv.


Next Step
---------
Proceed to the Phase 1 layer-resolved synthesis.

The synthesis should combine:

    Layer A chamber comparison report
    Layer B chamber comparison report
    Layer C chamber comparison report
    Layer D non-applicability / boundary-condition note

The final Phase 1 synthesis should emphasize:

    Charge-value behavior differs by layer.
    Fractional coordinates percolate internally.
    Composite closures percolate.
    Boundary absences do not form standalone ladders.
    The full charge-boundary structure is cross-layer, not contained in any
    single isolated layer.
