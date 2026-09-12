STITCH-MECH v0.1.1
==================

PURPOSE
-------
Answer the next JHTDB Pilot-A question:

    Is the very low real D_square genuinely dynamical organization,
    or is it already implied by local route geometry?

The instrument does NOT modify STRUC-ROUTE-I, STRUC-I, STRUC-PERC-I, or
the frozen Pilot-A run.

PLACEMENT
---------
Put this folder at:

    UNNS_TURB_JHTDB_v0_1\
        tools\
            analyze\
                STITCH_MECH_v0_1_0\

The tool automatically locates the frozen run:

    outputs\exports\struc_route_i\jhtdb_pilot_a\
        jhtdb_pilot_a_20260904_235409.zip

The frozen run is SHA-256 locked.

RUN
---
Double-click:

    RUN_WINDOWS.bat

The existing STRUC-ROUTE-I Python environment is reused.

The run is RESUMABLE. N1/N2 null rows are checkpointed after every null.

CONTROL HIERARCHY
-----------------
REAL
    Frozen JHTDB Pilot-A route graph.

N0
    Existing frozen ROUTE-I degree-preserving endpoint null.
    Imported from the original run; not recomputed.

N1
    Distance-stratified degree-preserving null.

    Swaps remain within the same scale/time transition group.
    In/out degree is preserved exactly.
    A rewired pair is accepted only when both new edges remain in the
    same within-group distance_norm quantile bins as the edges replaced.

N2
    Distance + feature-stratified degree-preserving null.

    All N1 constraints plus preservation of the within-group
    enstrophy-based feature_similarity stratum.

Null mobility and graph diversity are measured. A constrained null that is
too immobile is declared UNDERRESOLVED rather than interpreted.

IMPORTANT LIMIT
---------------
The frozen ROUTE-I run contains object centroids, radii and edge geometry but
not the original voxel masks.

Therefore N1/N2 preserve increasingly local graph geometry available from
the frozen tables, but they do NOT preserve exact voxel overlap or IoU for
newly rewired pairs.

A positive result rejects these graph-local geometric explanations. It does
not replace a future field-level surrogate control.

OBJECT-LEVEL MECHANISM TABLE
----------------------------
The instrument also builds:

    STITCH_MECH_OBJECTS.csv

For every source with finite D_square it combines:

- D_square
- scale/time persistence
- scale/time branch/merge flags
- outgoing overlap statistics
- outgoing IoU
- distance_norm
- feature_similarity
- physical volume / equivalent radius
- enstrophy
- Q
- strain proxy
- dissipation proxy

It then asks whether physical intensity remains associated with D_square
after conditioning on scale, time, route geometry and branch/merge state.

OUTPUTS
-------
Human/machine analysis:

    analysis\mechanism\jhtdb_pilot_a\stitch_mech_v01\
        REPORT.html
        REPORT.json

Tables:

    outputs\tables\stitch_mech\
        STITCH_MECH_OBJECTS.csv
        STITCH_NULL_HIERARCHY.csv
        STITCH_N1_NULLS.csv
        STITCH_N2_NULLS.csv

Bundle:

    outputs\records\STITCH_MECH_RESULT.zip

PRIMARY INTERPRETATION
----------------------
If N2 is statistically valid and real D_square remains significantly lower
than N2:

    SURVIVES_LOCAL_GEOMETRY_CONTROL

If N2 is valid but real D_square is no longer distinguishable:

    NOT_DISTINGUISHABLE_FROM_LOCAL_GEOMETRY_CONTROL

If N2 lacks mobility/diversity:

    N2_UNDERRESOLVED


V0.1.1 BUG FIX
--------------
v0.1.0 correctly loaded and validated the frozen ROUTE-I run and reproduced
the real D_square, but then failed while building the mechanism table.

Cause:
    the outgoing-edge aggregate table renamed `src_id` to `node_id`, while
    its edge-count companion table did not. The subsequent merge requested
    `node_id` from both tables.

v0.1.1 fixes only this dataframe-key mismatch. The scientific protocol,
N0/N1/N2 definitions, seeds, binning, thresholds and frozen source are
unchanged.

Because the v0.1.0 failure occurred before N1 started, there are no partial
null results that need to be preserved from that failed run.
