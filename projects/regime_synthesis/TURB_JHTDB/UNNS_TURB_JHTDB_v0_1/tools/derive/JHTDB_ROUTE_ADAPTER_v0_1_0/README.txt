JHTDB ROUTE ADAPTER v0.1.0
UNNS Turbulence — Physical Extraction Layer
============================================

PURPOSE
-------
Transform the canonical local JHTDB-derived velocity source

    data\raw\jhtdb\isotropic1024coarse\cutouts\
        isotropic1024-coarse-velocity.h5

into an analysis-ready structural route project for STRUC-ROUTE-I:

    manifest.json
    objects.parquet
    relations.parquet

The adapter operates locally on the complete HDF5. The 2 GB source file does
not need to be uploaded anywhere.

SCIENTIFIC PIPELINE
-------------------
JHTDB velocity [z,y,x,component]
    ↓
exact block coarse-graining at factors 1,2,4,8,16
    ↓
boundary-safe finite-difference velocity gradients
    ↓
divergence, vorticity, enstrophy, strain², Q, helicity
    ↓
rotation-dominated object segmentation
    ↓
connected structural objects
    ↓
exact voxel-overlap relations across adjacent scale and time layers
    ↓
manifest.json + objects.parquet + relations.parquet
    ↓
STRUC-ROUTE-I v0.1.1

BOUNDARY POLICY
---------------
The 256³ cutout is NOT treated as periodic.

No FFT derivatives are used.
No wrap-around is used.
A fixed physical boundary margin is excluded from object detection.
Objects touching the retained interior boundary are discarded as truncated.

DEFAULT MULTISCALE POLICY
-------------------------
Block factors:

    [1, 2, 4, 8, 16]

A factor f replaces every f×f×f native block by its mean velocity and reduces
the grid resolution accordingly. This is an explicit box coarse-graining, not
an opaque server-side filter.

DEFAULT OBJECT DEFINITION
-------------------------
The default segmentation is:

    Q >= q_rms_multiplier × RMS(Q)

with q_rms_multiplier = 1.5 on the boundary-safe interior.

Q > 0 identifies rotation-dominated local velocity-gradient structure.
The threshold is frozen in config/pilot_a.json and is not silently retuned.

Small components and components touching the retained-interior boundary are
removed.

ROUTING RELATIONS
-----------------
Only positive spatial overlap creates a candidate relation.

For every candidate:
    overlap_src = intersection / source volume
    overlap_dst = intersection / destination volume
    IoU         = intersection / union
    confidence  = overlap_src

Across scale, the coarser label field is expanded exactly onto the finer block
grid before overlap is counted.

Across time, same-scale label fields are compared directly.

The route-project manifest accepts a relation when ANY of:
    overlap_src >= 0.10
    overlap_dst >= 0.10
    IoU         >= 0.05

These thresholds are explicit and exported.

OBJECT WEIGHT
-------------
The ROUTE-I `weight` column is set to integrated enstrophy:

    weight = ∫ (|ω|²/2) dV

This is a positive extensive routing weight. It is NOT asserted to be a
conserved physical quantity.

INSTALLATION
------------
Place the extracted folder at:

    UNNS_TURB_JHTDB_v0_1\
        tools\
            derive\
                JHTDB_ROUTE_ADAPTER_v0_1_0\

Then double-click:

    RUN_ADAPTER_WINDOWS.bat

The launcher uses your existing Python 3 installation and creates its virtual
environment at the short Windows-safe location:

    %LOCALAPPDATA%\UNNS\JHTDB_ROUTE_ADAPTER_v010

OUTPUTS IN THE TURBULENCE PROJECT
---------------------------------
Canonical derived tables:

    data\derived\objects\jhtdb_pilot_a\
        objects.parquet
        relations.parquet

Ready-to-load STRUC-ROUTE-I project:

    ladders\native\jhtdb_pilot_a\route_project\
        manifest.json
        objects.parquet
        relations.parquet
        ADAPTER_REPORT.json
        PHYS_STATS.csv

Convenient bundle:

    outputs\records\JHTDB_PILOT_A_ROUTE.zip

Additional records:

    outputs\records\JHTDB_ADAPTER_REPORT.json
    outputs\tables\JHTDB_PHYS_STATS.csv

STRUC-ROUTE-I
-------------
In STRUC-ROUTE-I v0.1.1 use:

    PROJECT ZIP → JHTDB_PILOT_A_ROUTE.zip

Do not feed the raw HDF5 directly to STRUC-ROUTE-I.

VALIDATION
----------
Run:

    TEST_ADAPTER_WINDOWS.bat

The package contains exact mathematical tests, including solid-body rotation:
Q = Ω², enstrophy = 2Ω², strain² = 0 in the interior.

A small synthetic HDF5 end-to-end adapter run is also tested.

IMPORTANT
---------
The full real JHTDB run can be computationally heavy. It is deliberately
single-process by default to avoid accidental multi-gigabyte RAM multiplication.

For the native 256³ scale, the derivative/segmentation stage can temporarily
use roughly 1 GB of working memory. 8 GB system RAM is a practical minimum;
16 GB or more is preferable while other applications are open.
