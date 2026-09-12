UNNS Protein MSM Admissibility Pipeline
=======================================

PROJECT CONTEXT
----------------
This directory extends the UNNS Substrate framework into
protein folding and metastable-state traversal systems.

The objective is NOT biological classification.

The objective is to reinterpret protein folding dynamics as:

    admissibility geometry
    over constrained realizability manifolds.

The data originates from:

    Folding@home Markov State Models (MSMs)

hosted through the OSF COVID-19 simulation corpus.


CORE THEORETICAL MOTIVATION
----------------------------
Protein folding naturally contains structures closely aligned with UNNS:

    - admissibility corridors
    - metastable basins
    - constrained traversal
    - localized rupture
    - recoverable pathways
    - merge-boundary transitions

The MSM representation therefore provides an empirical testbed for:

    continuity preservation
    under complex state-space traversal.


SOURCE FILES
-------------
Input files:

    tprobs.npy
    populations.npy

Origin:

    Folding@home MSM model directory (https://osf.io/fs2yv/files/osfstorage)

Interpretation:

    tprobs.npy
        transition probability matrix
        between metastable protein states

    populations.npy
        equilibrium basin occupancies
        for MSM states


STRUCTURAL INTERPRETATION
--------------------------
The MSM is interpreted as:

    a weighted admissibility transition graph.

Meaning:

    state_i → state_j

represents:

    continuity traversal
    through realizability space.

The protein is therefore treated NOT as a sequence object,
but as:

    a constrained continuity manifold.


protein_msm_ladder_generator.py
--------------------------------
Purpose:

    Convert MSM transition geometry into
    STRUC_PERC_I-compatible admissibility ladders.

Generated output folder:

    protein_ladders/

Generated ladders:

    msm_out_strength.txt
    msm_in_strength.txt
    msm_population.txt
    msm_stitching_strength.txt
    msm_bottleneck_risk.txt


LADDER DEFINITIONS
-------------------

1. msm_out_strength.txt
------------------------
Meaning:

    outgoing continuity strength
    from each metastable state.

Interpretation:

    how strongly a state propagates
    admissible traversal.


2. msm_in_strength.txt
-----------------------
Meaning:

    incoming transition accessibility.

Interpretation:

    how reachable each state is
    from the global continuity manifold.


3. msm_population.txt
----------------------
Meaning:

    basin occupancy strength.

Interpretation:

    metastable persistence
    and admissibility basin depth.


4. msm_stitching_strength.txt
------------------------------
Meaning:

    local admissibility-gluing proxy.

Computed from:

    - outgoing continuity
    - incoming continuity
    - graph degree
    - basin population

Interpretation:

    local merge-boundary stitching strength.


5. msm_bottleneck_risk.txt
---------------------------
Meaning:

    localized rupture / traversal bottleneck risk.

Interpretation:

    states with significant occupancy
    but weak admissibility stitching.


STRUC_PERC_I PROCESSING
------------------------
The generated ladders were batch-processed through:

    STRUC_PERC_I

Output folder:

    STRUC_PERC_I_output/

Generated files:

    struc_perc_batch_results.json
    struc_perc_batch_results (1).csv


BATCH RESULTS SUMMARY
----------------------

FULL_PERCOLATION
-----------------
    msm_bottleneck_risk.txt
    msm_in_strength.txt
    msm_population.txt
    msm_stitching_strength.txt

GIANT_COMPONENT_PERCOLATION
----------------------------
    msm_out_strength.txt


KEY OBSERVATION
----------------
The protein MSM landscape exhibits:

    near-perfect global coherence

across approximately:

    5000 metastable states.

The only partially fragmented ladder:

    msm_out_strength.txt

still retained:

    giantRatio ≈ 0.9984

with only:

    3 isolated states
    out of ~5000.

This is extremely important.


THEORETICAL INTERPRETATION
---------------------------
The protein folding manifold behaves as:

    a strongly stitched admissibility system.

Observed geometry:

    - preserved giant continuity
    - extremely localized rupture
    - metastable traversal persistence
    - recoverable admissibility structure

This aligns remarkably well with earlier UNNS domains:

    - chemistry ladders
    - FCC continuity systems
    - Voyager trajectories
    - neutrino admissibility recovery
    - Higgs interaction ladders


EMERGING UNIVERSAL PATTERN
---------------------------
Across radically different domains,
the same structural geometry repeatedly appears:

    global coherence persists
    while rupture localizes sharply.

The protein MSM results strongly support:

    localized admissibility defects
    without global manifold collapse.


MERGE-BOUNDARY INTERPRETATION
------------------------------
The MSM state graph appears to encode:

    admissibility corridor traversal.

Localized bottlenecks may correspond to:

    merge-boundary rupture regions.

Strong stitching continuity suggests proteins
naturally evolve within:

    highly constrained admissible manifolds.


IMPORTANT CONCEPTUAL SHIFT
---------------------------
This framework does NOT interpret protein folding as:

    brute-force state search.

Instead:

    proteins traverse admissible continuity corridors
    through constrained realizability space.


PIPELINE SUMMARY
-----------------

tprobs.npy
populations.npy
        ↓
protein_msm_ladder_generator.py
        ↓
protein_ladders/
        ↓
STRUC_PERC_I
        ↓
protein admissibility geometry
        ↓
continuity / rupture analysis


DIRECTORY STRUCTURE
--------------------

protein/
│
├── tprobs.npy
├── populations.npy
├── protein_msm_ladder_generator.py
│
└── protein_ladders/
    │
    ├── msm_out_strength.txt
    ├── msm_in_strength.txt
    ├── msm_population.txt
    ├── msm_stitching_strength.txt
    ├── msm_bottleneck_risk.txt
    ├── MSM_LADDER_REPORT.txt
    │
    └── STRUC_PERC_I_output/
        │
        ├── struc_perc_batch_results.json
        └── struc_perc_batch_results (1).csv