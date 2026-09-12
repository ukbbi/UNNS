UNNS Metallic Glass Structural Ladder Pipeline
==============================================

PROJECT CONTEXT
----------------
This stage extends the UNNS Substrate trajectory methodology into
experimental chemistry and metallic-glass systems.

The objective is NOT ordinary material classification.

The objective is to transform compositional spectral chemistry data into:

    structural continuity ladders

suitable for:

    STRUC_PERC_I admissibility analysis.

This continues the same trajectory-based methodology previously used for:

    - Voyager trajectories
    - cosmological ladders
    - FCC phase-space systems
    - Higgs interaction ladders
    - corpus phase mapping
    - admissibility regime synthesis

The chemistry domain therefore becomes another realizability-space corpus.


SOURCE DATA
------------
Primary source:

    spectralparam_full.TXT

Origin:

    SciGlass spectral chemistry export

Critical discovery:
The TXT export DOES NOT contain proper named headers.

The file is positional CSV data only.

The first row is NOT a usable schema row.

Therefore all extraction must be performed using:

    positional column indexing

rather than field-name matching.


POSITIONAL COLUMN INTERPRETATION
---------------------------------
The extraction pipeline identified the following stable structure:

    col0  = GlassID
    col1  = RecordID
    col2  = spectral coordinate X
    col3  = source/model
    col4  = oxide/component
    col5  = flag
    col6  = concentration / wt%
    col7  = mode
    col8  = profile
    col9  = spectral coordinate Y
    col10 = source label

Example row:

    2412,33017,1.5140,"Priven-2000","ZnO",0,
    1.2000,2,"Default",2.4640,"Priven-2000"


metallic_glass_ladder_generator.py
-----------------------------------
Purpose:

    Convert raw chemistry spectral records into
    UNNS structural ladders.

Core responsibilities:

    1. Parse positional TXT rows safely
    2. Group rows by:
            (GlassID, Oxide)
    3. Sort records by concentration (wt%)
    4. Emit ordered compositional trajectories

Generated ladder structure:

    index
    wt_pct
    spectral_x
    spectral_y

Interpretation:

    Each ladder represents:

        compositional deformation trajectory
        through realizability space

rather than a static material descriptor.


LADDER INTERPRETATION
----------------------
The emitted ladders are interpreted as:

    admissibility trajectories

under compositional perturbation.

Increasing wt% corresponds to:

    progressive structural deformation.

The spectral coordinates encode:

    evolving structural response geometry.

Thus each ladder becomes:

    a sampled path through realizability space.


trajectory_normalizer.py
-------------------------
A preprocessing stage was introduced before STRUC_PERC_I analysis.

Purpose:

    Remove representational artifacts and stabilize trajectories.

Normalization responsibilities:

    - remove duplicated coordinates
    - smooth discontinuous jumps
    - stabilize scales
    - suppress outlier spikes
    - improve continuity ordering
    - reduce sparse trajectory artifacts

Result:

    normalized_ladders/

ready for STRUC_PERC_I ingestion.


GRID SWEEP VALIDATION
----------------------
Additional validation infrastructure was introduced:

    grid_sweep_runner.py

Purpose:

    test κ-grid invariance.

Motivation:

    demonstrate that admissibility classes are NOT
    numerical artifacts of scan resolution.

Executed sweep families:

    GRID A : 17 layers
    GRID B : 33 layers
    GRID C : 65 layers
    GRID D : 129 layers

Additional perturbation sweeps:

    altered κ_min
    altered κ_max
    expanded κ-range

Observed result:

    near-perfect regime invariance.

This strongly supports:

    structural robustness
    under representational perturbation.


STRUC_PERC_I BATCH RESULTS
---------------------------
The chemistry ladders were batch-processed using STRUC_PERC_I.

High-level outcome:

    FULL_PERCOLATION      : 132
    HARD_FRAGMENTATION    : 368

However the fragmentation geometry revealed
something much deeper.

Most fragmented ladders exhibited:

    - very high giantRatio
    - extremely high tailDominance
    - only 1-2 isolated nodes
    - preserved global coherence

Meaning:

    fragmentation was highly localized.

The structures were usually:

    near-continuous
    but locally ruptured.

This became one of the strongest confirmations of:

    Merge-Boundary-as-Glue

within the chemistry domain.


KEY THEORETICAL RESULT
-----------------------
The chemistry corpus revealed a dual-layer structure:

RAW LADDERS
------------
Expose:

    localized admissibility defects
    boundary-sensitive rupture
    local stitching failure

NORMALIZED LADDERS
-------------------
Expose:

    global manifold continuity
    admissible cluster stability
    recoverable coherence

This distinction became extremely important.

Interpretation:

    chemistry systems preserve large-scale coherence
    while suffering local admissibility rupture near
    merge boundaries.


EMERGING UNIVERSAL PATTERN
---------------------------
The chemistry results aligned strongly with prior UNNS domains:

    - neutrino Δ-lifting
    - FCC confinement
    - Voyager κ-boundaries
    - Higgs interaction ladders
    - corpus admissibility mapping

Common pattern:

    systems preserve global coherence
    while local admissibility rupture appears first.

This may represent:

    a universal structural response law.


IMPORTANT CONCEPTUAL SHIFT
---------------------------
The chemistry ladders should NOT be interpreted as:

    ordinary chemical descriptors

but as:

    experimentally sampled realizability trajectories.

This reframes chemistry as:

    admissibility geometry
    under compositional deformation.


NEXT MAJOR DIRECTION
---------------------
Potential future extension:

    protein folding landscapes

because protein folding naturally contains:

    - admissibility corridors
    - metastable basins
    - recoverable pathways
    - localized rupture
    - constrained manifold traversal

which appear deeply aligned with the chemistry results.


PIPELINE SUMMARY
-----------------

spectralparam_full.TXT
        ↓
metallic_glass_ladder_generator.py
        ↓
metallic_ladders/
        ↓
trajectory_normalizer.py
        ↓
normalized_ladders/
        ↓
STRUC_PERC_I
        ↓
regime_map_analysis
        ↓
admissibility geometry interpretation