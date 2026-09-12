NEUTRINO RISC Δ-LIFTING + STRUC-PERC-I PIPELINE
================================================

Project:
UNNS Substrate — Non-Crossability / RISC Regime Analysis

Corpus:
Neutrino detector reconstruction ladders

Purpose
-------
This pipeline evaluates whether Δ-lifting:

    ΔL = |x(i+1) - x(i)|

systematically:

- restores admissibility,
- suppresses representation-induced fragmentation,
- stabilizes FCC-like regimes,
- increases margin m(L),
- preserves GR,
- or recovers latent structural continuity.

The pipeline operationally tests:

    RISC
    Margin-Confinement
    FCC persistence
    admissibility transport
    local continuity extraction

------------------------------------------------------------
CURRENT ALIGNED FOLDER STRUCTURE
------------------------------------------------------------

neutrinos_roots/

    raw/
        *.txt
        delta_txt_ladder.py

        delta_outputs/
            *_delta.txt

            struc_perc_delta_results/

    struc_perc_raw_results/

    extract_neutrino_ladders.py

    inspect_root_structure.py
    inspect_branch_structure.py

    *.root

------------------------------------------------------------
PIPELINE OVERVIEW
------------------------------------------------------------

ROOT detector files
    ↓
extract_neutrino_ladders.py
    ↓
raw realizability ladders (*.txt)
    ↓
STRUC-PERC-I RAW ANALYSIS
    ↓
struc_perc_raw_results/
    ↓
Δ-lifting
    ↓
delta_outputs/*_delta.txt
    ↓
STRUC-PERC-I Δ ANALYSIS
    ↓
struc_perc_delta_results/
    ↓
raw vs Δ comparison
    ↓
RISC / FCC / margin interpretation

------------------------------------------------------------
STAGE 1 — ROOT STRUCTURE INSPECTION
------------------------------------------------------------

Purpose:
    inspect ROOT files and identify usable branches.

Files:

    inspect_root_structure.py
    inspect_branch_structure.py

ROOT sources:

    deepL_performance.root
    TMVA_performance.root
    EnerySpectrum.root
    evt.root
    variable.root
    Fib_CDPMT.root

Goal:
    identify:
        - classifier outputs
        - energy observables
        - angular observables
        - hit-time variables
        - embedding coordinates

------------------------------------------------------------
STAGE 2 — LADDER EXTRACTION
------------------------------------------------------------

Script:

    extract_neutrino_ladders.py

Purpose:
    convert ROOT observables into normalized scalar ladders.

Operations:

    - extract arrays
    - remove invalid values
    - normalize
    - sort
    - export TXT ladders

Output:

    raw/*.txt

Examples:

    L_TMVA_*.txt
    L_deepL_*.txt
    L_bkg_*.txt
    L_sig_*.txt

These are:
    normalized realizability ladders.

------------------------------------------------------------
STAGE 3 — STRUC-PERC-I RAW ANALYSIS
------------------------------------------------------------

Input:

    raw/*.txt

Output folder:

    struc_perc_raw_results/

Purpose:
    establish baseline admissibility structure.

Required metrics:

    GR
    TD
    κconn
    verdict class
    isolated-node count
    margin proxy
    theorem activation

Key targets:

    FULL
    GIANT
    TAIL
    HARD
    FCC-like

------------------------------------------------------------
STAGE 4 — Δ-LIFTING
------------------------------------------------------------

Script:

    raw/delta_txt_ladder.py

Purpose:
    generate Δ-lifted realizability ladders.

Definition:

    ΔL = |x(i+1) - x(i)|

Operational meaning:

    local continuity extraction.

------------------------------------------------------------
CORRECT USAGE
------------------------------------------------------------

IMPORTANT:
The script REQUIRES an argument.

------------------------------------------------------------
PROCESS ALL TXT FILES IN CURRENT FOLDER
------------------------------------------------------------

Go to:

    neutrinos_roots/raw/

Then run:

    python delta_txt_ladder.py .

The dot means:

    process all TXT ladders in current directory.

THIS IS THE STANDARD USAGE.

------------------------------------------------------------
PROCESS A SPECIFIC FOLDER
------------------------------------------------------------

Example:

    python delta_txt_ladder.py raw

------------------------------------------------------------
PROCESS A SINGLE FILE
------------------------------------------------------------

Example:

    python delta_txt_ladder.py L_TMVA_hSigSB.txt

------------------------------------------------------------
WRONG USAGE
------------------------------------------------------------

THIS:

    python delta_txt_ladder.py

is invalid.

The script will:
    display usage instructions
    and terminate.

No files will be processed.

------------------------------------------------------------
EXPECTED TERMINAL OUTPUT
------------------------------------------------------------

Example:

    [INFO] Found 67 files

    [PROCESSING] L_TMVA_hSigSB.txt
    [OK] L_TMVA_hSigSB_delta.txt
    [SIZE] 91

    ...

    [DONE]
    [SUCCESS] 67
    [FAILED ] 0

------------------------------------------------------------
Δ OUTPUT LOCATION
------------------------------------------------------------

Generated Δ-ladders are saved to:

    raw/delta_outputs/

Examples:

    L_TMVA_hSigSB_delta.txt
    L_deepL_hSigSB_delta.txt
    ...

These files are:

    normalized
    sorted
    STRUC-PERC-I compatible

------------------------------------------------------------
STAGE 5 — STRUC-PERC-I Δ ANALYSIS
------------------------------------------------------------

Input:

    raw/delta_outputs/*_delta.txt

Output folder:

    raw/delta_outputs/struc_perc_delta_results/

Purpose:
    evaluate admissibility after Δ-lifting.

Required metrics:

    GR
    TD
    κconn
    verdict class
    isolated-node count
    margin proxy
    theorem activation

------------------------------------------------------------
STAGE 6 — RAW vs Δ COMPARISON
------------------------------------------------------------

Match:

    raw ladder
        ↔
    corresponding Δ-ladder

Example:

    L_TMVA_hSigSB.txt
        ↔
    L_TMVA_hSigSB_delta.txt

------------------------------------------------------------
REQUIRED COMPARISON TABLE
------------------------------------------------------------

Target file:

    delta_margin_comparison.csv

Required columns:

    ladder
    raw_verdict
    delta_verdict
    raw_GR
    delta_GR
    raw_TD
    delta_TD
    raw_margin
    delta_margin
    margin_shift
    result
    interpretation

------------------------------------------------------------
INTERPRETATION RULES
------------------------------------------------------------

margin_shift = delta_margin - raw_margin

If:

    margin_shift > 0

then:

    Δ-lifting improved margin.

If:

    margin_shift = 0

then:

    Δ-lifting preserved margin.

If:

    margin_shift < 0

then:

    Δ-lifting degraded margin.

------------------------------------------------------------
MOST IMPORTANT DETECTION CASES
------------------------------------------------------------

RISC recovery:

    HARD → FULL
    HARD → GIANT
    TAIL → FULL
    TAIL → GIANT

FCC stabilization:

    TD remains high
    while GR increases
    and fragmentation decreases

These indicate:

    latent admissibility recovery.

------------------------------------------------------------
PRIMARY SCIENTIFIC QUESTIONS
------------------------------------------------------------

1. Does Δ-lifting suppress HARD fragmentation?

2. Does Δ-space restore FULL or GIANT structure?

3. Does GR increase?

4. Does margin increase?

5. Are FCC-like regimes stabilized?

6. Does Δ-space suppress RISC artifacts?

7. Does local continuity survive beneath
   observational fragmentation?

------------------------------------------------------------
THEORETICAL INTERPRETATION
------------------------------------------------------------

If repeatedly validated:

Δ-lifting may behave as:

    - local continuity extraction
    - admissibility restoration
    - latent manifold recovery
    - representation correction
    - structural denoising
    - observational gauge reduction

This strongly aligns with:

    - RISC
    - Margin-Confinement
    - FCC persistence
    - admissibility transport
    - representation-sensitive realizability

------------------------------------------------------------
CURRENT STATUS
------------------------------------------------------------

ROOT inspection:
    COMPLETE

Ladder extraction:
    COMPLETE

Generated raw ladders:
    COMPLETE

Generated Δ-ladders:
    COMPLETE

Δ-ladders generated:
    67

Δ generation success:
    67 / 67

STRUC-PERC RAW analysis:
    COMPLETE

STRUC-PERC Δ analysis:
    RUNNING / NEXT STAGE

Remaining task:
    raw vs Δ comparative analysis