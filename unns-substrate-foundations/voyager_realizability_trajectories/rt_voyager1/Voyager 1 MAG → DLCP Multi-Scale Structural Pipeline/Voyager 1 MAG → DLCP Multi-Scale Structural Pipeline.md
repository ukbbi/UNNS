

Voyager 1 MAG → DLCP Multi-Scale Structural Pipeline
1. Overview

This repository implements a DLCP-based structural ladder generation pipeline for Voyager 1 magnetic field (48s cadence) data, designed to support:

STRUC-PERC-I batch analysis
Structural regime identification
Robustness validation of boundary detection

The pipeline converts raw physical measurements into UNNS-valid structural ladders, enabling analysis in the admissibility manifold M
adm
	​

.

2. Scientific Objective

The core goal is to test:

Is t* = 2012 (κ_conn minimum) invariant under window-scale variation?

This corresponds to validating that the heliopause boundary detection is:

not an artifact of segmentation
not dependent on window size
structurally intrinsic
3. Data Source

Voyager 1 MAG high-resolution dataset (48s cadence):

https://cdaweb.gsfc.nasa.gov/pub/data/voyager/voyager1/magnetic_fields_cdaweb/hires1991_2030/primary/mag_48s/

Why this dataset
Direct measurement of heliospheric → interstellar transition
High temporal resolution (48s)
Physically meaningful observable: magnetic field magnitude
Suitable for DLCP windowing
4. Pipeline Concept

The pipeline performs:

CDF → |B| reconstruction → cleaning → sliding windows → sorting → ladders (.txt)
Key transformation
time series → structural object (ladder)

This is not signal processing — it is structural re-encoding.

5. Multi-Scale Validation Design

The pipeline performs a controlled parameter sweep:

WINDOW_CONFIGS = [
    (512, 128),
    (1024, 256),
    (2048, 512),
]
Interpretation
Window	Duration	Purpose
512	~6.8 h	fine-scale structure
1024	~13.6 h	baseline
2048	~27.3 h	coarse-scale validation
6. Invariant Parameters (Critical)

These must NOT change across runs:

✔ B components: ["B1", "B2", "B3"]
✔ |B| = sqrt(B1² + B2² + B3²)
✔ MIN_VALID_RATIO = 0.95
✔ Physical filter: 0 < |B| < 10 nT
✔ Fill-value removal
✔ Zero plateau rejection
✔ Extreme value rejection (>10 nT)
✔ Ladder construction: sorted ascending
✔ Output format: .txt (one value per line)

This ensures:

only window scale varies — nothing else

7. Generator: voyager1_mag_multiscale_pipeline.py

The generator performs:

7.1 File ingestion
Reads .cdf files from working directory
Extracts B1, B2, B3
7.2 Reconstruction
|B| = sqrt(B1² + B2² + B3²)
7.3 Cleaning
removes NaN / Inf
removes fill values
filters:
B ≤ 0 (zero plateau)
B ≥ 10 nT (artifacts)
7.4 Windowing

Sliding window:

WINDOW_SIZE = W
STEP_SIZE   = S
7.5 Ladder construction
ladder = sort(cleaned_segment)
7.6 Output
one value per line

Compatible with STRUC-PERC-I.

8. Output Structure
outputs_multi_scale/
    W512_S128/
    W1024_S256/
    W2048_S512/

Each contains:

run_config.txt
v1_<file>_W..._win_XXXX_..._L_B.txt
run_config.txt

Includes:

window parameters
invariant settings
number of ladders
execution metadata
9. STRUC-PERC-I Integration

Each scale directory is processed independently:

W*/ → batch analysis → CSV

Example outputs:

struc_perc_batch_results.csv
struc_perc_batch_results.json
10. Required Analysis

For each scale:

Compute:

year → mean κ_conn
year → excursion density
year → class distribution
11. Robustness Criterion

The result is valid if:

argmin_t κ_conn(t) = 2012

for all:

W = 512, 1024, 2048

Additionally:

excursions localized near 2011–2012
post-2012 κ plateau
FULL dominance after crossing
12. Dataset Scope
Minimum
2011–2013
Full validation
2011–2017
Why full range
confirms global minimum
verifies post-boundary stability
rules out transient artifacts
13. Interpretation

If robustness holds:

t* = 2012 is a structural invariant

not:

artifact of segmentation
14. Pipeline Classification

This pipeline is:

✔ deterministic
✔ parameter-controlled
✔ reproducible
✔ structurally invariant (except window scale)

15. What This Is NOT
✗ Not time-series analysis
✗ Not signal filtering
✗ Not statistical smoothing

It is:

✔ structural transformation into ℳ_adm
16. Next Steps
Run all scales
Batch through STRUC-PERC-I
Export CSV
Compare:
t*_512
t*_1024
t*_2048

Expected:

t*_512 = t*_1024 = t*_2048 = 2012
17. Summary

This pipeline establishes:

a mapping from physical data → structural ladders
a controlled multi-scale experiment
a robustness test of boundary detection
18. Key Insight

The pipeline does not analyze data —
it converts it into a form where structure becomes observable.