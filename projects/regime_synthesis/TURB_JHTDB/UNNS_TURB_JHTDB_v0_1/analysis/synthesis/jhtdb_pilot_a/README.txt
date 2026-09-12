JHTDB PILOT A — SYNTHESIS RECORDS
=================================

This folder preserves successive Pilot-A synthesis stages.

VERSION 0.1 — CROSS-CHAMBER BASELINE
------------------------------------
SYNTHESIS.md
SYNTHESIS.json

These files preserve the first synthesis after:

    STRUC-ROUTE-I
        +
    STRUC-I
        +
    STRUC-PERC-I

They remain historical records and should not be overwritten.

VERSION 0.2 — CURRENT CROSS-STAGE SYNTHESIS
-------------------------------------------
SYNTHESIS_v02.md
SYNTHESIS_v02.json

Version 0.2 incorporates the completed STITCH-MECH v0.1.1 mechanism stage.

The principal v0.2 addition is:

    SURVIVES_LOCAL_GEOMETRY_CONTROL

The current Pilot-A interpretation is therefore the v0.2 pair.

CURRENT WORKING PICTURE
-----------------------
Pilot A supports a largely commuting scale-time structural route regime with
localized noncommuting breakdowns preferentially associated with structural
reorganization and physically intense events.

CLAIM BOUNDARY
--------------
The N1/N2 mechanism controls are graph-local controls. They do not preserve
exact newly evaluated voxel overlap or IoU for rewired object pairs.

The result therefore establishes survival under the tested graph-local
geometric explanations, not every possible field-level surrogate.

NEXT SCIENTIFIC STAGE
---------------------
Independent JHTDB replication under the frozen Pilot-A protocol.

CHECKSUMS
---------
SHA256SUMS.txt should cover:

    README.txt
    SYNTHESIS.md
    SYNTHESIS.json
    SYNTHESIS_v02.md
    SYNTHESIS_v02.json

Do not include SHA256SUMS.txt itself in the checksum ledger.

Use UPDATE_SHA256SUMS.bat after copying the v0.2 files into this folder.
It calculates the hashes from the exact local files, including the preserved
v0.1 SYNTHESIS.json.
