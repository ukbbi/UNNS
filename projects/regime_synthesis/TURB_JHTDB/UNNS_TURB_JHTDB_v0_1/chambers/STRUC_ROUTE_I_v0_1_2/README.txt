STRUC-ROUTE-I v0.1.2
Multiscale Structural Routing & Persistence Chamber
UNNS Substrate Program

STATUS
------
Functional first implementation.

PURPOSE
-------
STRUC-ROUTE-I tests whether identified structures in a layered dynamical
system persist, branch, merge, and route through SCALE and/or TIME in a
reproducibly constrained manner relative to matched null routing.

It is deliberately domain-agnostic.

It does NOT:
- detect vortices;
- read a raw turbulence HDF5 as its scientific input;
- define coherent structures;
- replace STRUC-I or STRUC-PERC-I;
- invent a universal composite routing score.

Those boundaries are intentional.

THE THREE-CHAMBER ARRAY
-----------------------
STRUC-I       : ordered-ladder admissibility under perturbation.
STRUC-PERC-I  : gap-structure connectivity/percolation.
STRUC-ROUTE-I : identity, persistence, branching, merging and routing
                through scale/time.

WINDOWS QUICK START
-------------------
1. Extract this folder.
2. Double-click:

       RUN_WINDOWS.bat

3. On first launch the chamber creates a local .venv and installs its Python
   dependencies.
4. Your browser opens to a LOCAL address (127.0.0.1). No scientific input is
   sent to a remote service.
5. Either:
   - run one of the built-in exact synthetic fixtures, or
   - upload manifest.json + objects.csv/parquet + relations.csv/parquet,
     optionally families.csv.

The Python engine performs the analysis. JavaScript is display/control only.

COMMAND LINE
------------
A project folder must contain:

    manifest.json
    objects.csv OR objects.parquet
    relations.csv OR relations.parquet
    optional families.csv OR families.parquet

Run:

    .venv\Scripts\python.exe cli.py samples\perfect_chain

or after activation:

    python cli.py samples\perfect_chain

OUTPUT
------
Each run is written beneath:

    outputs\<run_id>\

Canonical files:
    RESULT.json
    RUN.json
    SUMMARY.csv
    NODES.parquet
    EDGES.parquet
    SQUARES.parquet
    NULLS.csv
    LADDERS.zip

The browser exposes a ZIP download of the same run folder.

IMPORTANT SCIENTIFIC RULES
--------------------------
1. Route edges must move exactly one adjacent layer forward:
   - scale edge: scale_idx + 1, same time_idx
   - time edge : time_idx + 1, same scale_idx

2. Display sampling never alters the Python analysis.

3. Null graphs preserve the directed source out-degree and target in-degree
   within each scale/time transition layer by degree-preserving endpoint swaps.

4. Evidence verdicts are based on transparent empirical null tests, not a
   weighted composite score.

5. Relation eligibility is declared in manifest.json and exported with every
   result.

6. STRUC-ROUTE-I does not decide what physical quantity is conserved. An
   optional object weight column is declared by the adapter/project manifest.

See SPEC.md for the frozen v0.1.2 model.

V0.1.1 NULL-MOBILITY PATCH
--------------------------
Null runs now expose attempted/accepted swaps, mobility, graph diversity and real-graph clone fraction. Failed null-quality gates force UNDERRESOLVED rather than NULL_LIKE_ROUTING.


V0.1.2 UPDATE
-------------
- Real-graph Layers 1–6 render immediately before the null ensemble finishes.
- Layer 7 shows live null index, accepted swaps, mobility, elapsed time and ETA.
- Route entropy remains displayed but is explicitly NON-INFERENTIAL under the
  current endpoint-rewiring null, because outgoing source edge-weight multisets
  are preserved exactly.
- Optional manifest.analysis_filter supports sensitivity analyses without
  rebuilding the physical source corpus.
- Every run attempts a high-D_square physical association export:
    STITCH_PHYSICS.json
    STITCH_TAIL.csv
    STITCH_BY_TIME.csv
    STITCH_BY_SCALE.csv
- ANALYZE_RUN_WINDOWS.bat performs the same tail analysis on an existing v0.1.1
  run ZIP without re-running its 100 nulls.
