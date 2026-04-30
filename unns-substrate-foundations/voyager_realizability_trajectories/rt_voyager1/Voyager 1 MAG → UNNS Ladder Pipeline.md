Voyager 1 MAG → UNNS Ladder Pipeline

STRUC-PERC-I v2.5.0 Integration

Overview

This repository implements a complete structural pipeline:

Voyager 1 MAG (CDF) → Sliding windows → Sorted ladders → STRUC-PERC-I → Regime classification

It converts raw heliophysics time-series into UNNS-valid structural objects (ladders) and evaluates them using the STRUC-PERC-I v2.5.0 chamber.

Components
1. voyager1_mag_ladder_pipeline.py

Role: Generator

Reads Voyager 1 MAG .cdf files
Extracts magnetic field magnitude
Applies sliding window segmentation
Produces sorted ladders (UNNS-compliant)
Outputs .txt files for STRUC-PERC-I
2. struc_perc_i_v2_5_0.html

Role: Structural analysis engine

Accepts ladder input (single or batch)
Computes:
κ (connectivity delay)
Giant ratio
Connectivity margin proxy
Classifies regimes:
FULL
GIANT
TAIL
HARD
3. Raw Data (NASA CDAWeb)

Source (direct):

https://cdaweb.gsfc.nasa.gov/pub/data/voyager/voyager1/magnetic_fields_cdaweb/hires1991_2030/primary/mag_48s/

Why Voyager 1 MAG (48s)?

We deliberately use:

mag_48s (48-second cadence)
primary/
hires1991_2030/
Rationale
1. Physical relevance
Magnetic field is the most stable structural observable
Unlike plasma density, it is not dominated by instrument artifacts
2. Structural continuity
Provides long continuous trajectory (1991–2030)
Critical for UNNS trajectory analysis
3. Resolution balance
48s cadence:
high enough to capture structure
low enough to avoid noise-driven fragmentation
4. CDAWeb canonical dataset
Already cleaned and standardized
Compatible with reproducible workflows
Pipeline Design (UNNS-Compliant)
Step 1 — Data Extraction

From CDF:

Load magnetic field magnitude (|B| or equivalent variable)
Remove fill values / NaNs
Step 2 — Sliding Window Segmentation
WINDOW_SIZE = 1024
STEP_SIZE   = 256

Why:

Ladders represent local structural states
Not global signals
Step 3 — Ladder Construction

Each segment is transformed:

ladder = sorted(segment)

Important:

❌ NOT time series
❌ NOT signal processing
✔ Ordered structural object
Step 4 — Output Format

Each ladder is saved as:

one value per line
.txt format

Example:

0.1821
0.1830
0.1837
...

This is strictly required by STRUC-PERC-I.

Step 5 — Output Structure
output/
  voyager1_YYYYMMDD_WIN_XXXX/
    ..._L_B.txt

Each window is:

independent
reproducible
analyzable in isolation
STRUC-PERC-I v2.5.0

The chamber implements:

Ladder → κ → GR → regime
Core Outputs
κ — connectivity delay
giantRatio
kappa_connect
verdict
Regime Interpretation
Regime	Meaning
FULL	stable connected structure
GIANT	near-boundary connectivity
TAIL	fragmentation onset
HARD	structural collapse
Batch Mode

v2.5.0 introduces:

multi-file ingestion
sequential processing
export:
CSV
JSON
Example Workflow
1. Generate ladders
python voyager1_mag_ladder_pipeline.py
2. Open chamber

Open:

struc_perc_i_v2_5_0.html
3. Run batch
drag all .txt ladders
click RUN BATCH
4. Export results
batch_results.csv
What This Pipeline Produces

This is NOT data processing.

It is:

Structural transformation of physical observables into UNNS regime objects

Scientific Role

This pipeline enables:

1. Trajectory reconstruction
Voyager → path in ℳₐdm
2. Boundary detection
heliopause as realizability boundary
3. Cross-domain comparison
atoms / cosmology / heliophysics
Relation to UNNS Framework

This pipeline directly implements:

connectivity margin concept
regime classification
structural ladders as primary objects
Known Constraints
density datasets → unreliable (instrumental HARD)
requires proper cleaning
window size must remain fixed for comparability
Key Insight

Voyager data is not just time-series.

It is:

a continuous structural trajectory approaching a realizability boundary

Status
✔ Generator implemented
✔ Batch analysis operational
✔ 2011 validated
⏳ Full decade analysis in progress
Reference Visualization

See structural ordering principle:




Usage

Research use within UNNS Substrate project.

Next Steps
Extend to 2012–2017
Compare with Voyager 2 trajectory
Detect boundary crossing (heliopause)
Final Note

This system is not a data pipeline.

It is:

a structural measurement instrument for physical reality