UNNS TURBULENCE — JOHNS HOPKINS TURBULENCE DATABASE
Project root: UNNS_TURB_JHTDB_v0_1
===================================================

PURPOSE
-------
This research branch tests whether real turbulent flow exhibits reproducible
structural organization that can be expressed in UNNS terms without reducing
the experiment to conventional turbulence statistics alone.

The first branch is the JHTDB forced-isotropic pilot based on the
`isotropic1024coarse` Johns Hopkins Turbulence Database dataset.

The operative research question is:

    Does a turbulent flow occupy a restricted structural route space
    across scale and time, relative to matched null organization?

PROJECT BOUNDARY
----------------
This folder is the PROJECT ROOT.

Project-level files belong here:
    MANIFEST.json
    QUESTIONS.md
    README.txt
    RUN_INSPECT_H5.bat
    SCHEMA.md
    SCOPE.md
    TREE.txt
    WORKFLOW.md

Chamber code does NOT belong in the project root.

Chamber implementations belong under:
    chambers\

General scientific utilities belong under:
    tools\

CANONICAL ROOT STRUCTURE
------------------------
UNNS_TURB_JHTDB_v0_1\
├─ analysis\
├─ chambers\
├─ config\
├─ data\
├─ docs\
├─ ladders\
├─ outputs\
├─ tests\
├─ tools\
├─ MANIFEST.json
├─ QUESTIONS.md
├─ README.txt
├─ RUN_INSPECT_H5.bat
├─ SCHEMA.md
├─ SCOPE.md
├─ TREE.txt
└─ WORKFLOW.md

DATA LAYERS
-----------
Official JHTDB reference material:

    data\source\
        README-isotropic.pdf
        ener_Re_time.txt
        spectrum.txt

Third-party extraction provenance:

    data\source\hf\
        README.md
        DEMO_HF_Getdata_local.ipynb

Canonical raw velocity source:

    data\raw\jhtdb\isotropic1024coarse\cutouts\
        isotropic1024-coarse-velocity.h5

The source HDF5 is immutable.

Canonical SHA-256:

    e32c9225af656a2f0fa0a704be7dcd78fa12efc1a01b880af23eb45e02108a46

The source contains ten `Velocity_####` datasets, each 256×256×256×3
float32, with native JHTDB grid spacing.

IMPORTANT PHYSICAL RULE
-----------------------
The original JHTDB simulation is periodic, but this extracted 256³ cube is not
itself a periodic computational domain.

Therefore:
- do not wrap opposite cutout faces together;
- do not use FFT derivatives that assume periodicity on the cutout;
- use boundary-safe physical derivatives;
- reject or explicitly control boundary-truncated structures.


CANONICAL PUBLIC SOURCE ARCHIVE
-------------------------------
The heavy frozen JHTDB-derived source artifacts are publicly archived on Zenodo:

    UNNS Turbulence — JHTDB Analysis Cutouts and High-Re Export v0.1

Exact version DOI:

    10.5281/zenodo.22650769

All-versions concept DOI:

    10.5281/zenodo.22650768

Record:

    https://zenodo.org/records/22650769

Project archive metadata:

    data\source\zenodo\

Zenodo is the canonical public archival/distribution layer.
The immutable local working copies remain under:

    data\raw\jhtdb\

Do not duplicate the multi-gigabyte raw payload inside lightweight project ZIPs.
For exact reproduction of this project state, use/cite the VERSION DOI.
See data\source\zenodo\RESTORE.md for the file-to-local-path restore map.


CURRENT PHYSICAL ADAPTER
------------------------
The JHTDB physical adapter is stored under:

    tools\derive\JHTDB_ROUTE_ADAPTER_v0_1_0\

Its pipeline is:

    velocity HDF5
        ↓
    exact multiscale coarse-graining
        ↓
    boundary-safe physical derivatives
        ↓
    Q / vorticity-derived structural fields
        ↓
    coherent-object segmentation
        ↓
    scale/time overlap relations
        ↓
    STRUC-ROUTE-I project tables

Canonical derived tables:

    data\derived\objects\jhtdb_pilot_a\
        objects.parquet
        relations.parquet

Canonical route project:

    ladders\native\jhtdb_pilot_a\route_project\
        manifest.json
        objects.parquet
        relations.parquet
        ADAPTER_REPORT.json
        PHYS_STATS.csv

Primary adapter bundle:

    outputs\records\JHTDB_PILOT_A_ROUTE.zip

Adapter provenance:

    outputs\records\JHTDB_ADAPTER_REPORT.json

Physical diagnostics:

    outputs\tables\JHTDB_PHYS_STATS.csv

STRUC-ROUTE-I
-------------
Current project chamber:

    chambers\STRUC_ROUTE_I_v0_1_2\

STRUC-ROUTE-I is the routing/persistence chamber.

It tests:
- scale persistence;
- temporal persistence;
- branching;
- merging;
- route conservation;
- scale-time stitching;
- matched route-null behavior.

Its scale-time stitching quantity is:

    D_square = JSD(ST, TS) / ln 2

where ST means scale-then-time routing and TS means time-then-scale routing.

Under the current degree-preserving endpoint-rewiring null, route entropy is
DESCRIPTIVE ONLY because each source node's outgoing edge-weight multiset is
preserved by construction.

STRUC-I and STRUC-PERC-I remain canonical external chambers and must not be
modified by this branch.

CURRENT PILOT STATUS
--------------------
The physical adapter completed successfully on the full 10-frame source.

Pilot A produced:

    objects              12,484
    relation candidates  17,560
    scale relations       6,752
    time relations       10,808

The first STRUC-ROUTE-I physical run returned:

    CONSTRAINED_ROUTING

The strongest current signatures are:
- temporal persistence above the matched route-null ensemble;
- very low real scale-time stitching defect relative to the rewired nulls.

Follow-up checks also showed that:
- removing the sparse factor-16 scale does not drive the result;
- high-D_square events are enriched in physically intense structures.

These are research findings, not project-root configuration values. Preserve
their result files under outputs/ and analysis/ rather than hard-coding them
into upstream source data.

WORKFLOW
--------
1. Preserve and validate source provenance.
2. Keep the HDF5 immutable.
3. Inspect HDF5 structure and hashes.
4. Derive physical fields locally.
5. Build multiscale objects and scale/time relations.
6. Run STRUC-ROUTE-I.
7. Validate against nulls and sensitivity controls.
8. Export route-derived ladders only after route analysis.
9. Run canonical STRUC-I and STRUC-PERC-I downstream.
10. Preserve every frozen configuration and result bundle.

NON-NEGOTIABLE RULES
--------------------
- No fabricated or reconstructed raw JHTDB values.
- No silent retuning of thresholds after seeing outcomes.
- No source modification.
- No chamber code in the project root.
- No periodic treatment of the extracted subcube.
- No replacement or modification of canonical STRUC-I / STRUC-PERC-I.
- Keep provenance, hashes, manifests, and exact run outputs.
- Distinguish source data, derived data, chamber input, chamber output, and
  interpretation.

STATUS
------
Active research branch.

Primary JHTDB forced-isotropic Pilot A is operational and has produced a first
positive constrained-routing result. The branch remains in validation and
cross-chamber synthesis.
