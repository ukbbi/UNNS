📄 README.md
Parameterized Structural Response Field Generator (α, μ)
🔴 Overview

This directory implements a fully automated structural analysis pipeline built on the STRUC-PERC I v2.4.0 chamber, extended with:

parameterized deformation operators: α (scale) and μ (modulation)
batch execution across structured parameter grids
automated structural classification and metric extraction
reproducible dataset → phase-space mapping
⚡ Core Idea

Each input dataset (ladder) is transformed under:

(α, μ) ∈ [0.80, 1.20] × [0.80, 1.20]

For every pair:

Apply operators:
forward: μ(α(L))
reverse: α(μ(L))
Run through STRUC-PERC chamber
Extract structural response:
connectivity (κ)
fragmentation
component structure
outliers
Store:
raw results (JSON)
structured metrics (CSV)
🧠 System Architecture
runner.py
 ├── config.py           # global parameters, paths, grids
 ├── operators.py        # α and μ transformations
 ├── engine_bridge.py    # Python ↔ Node ↔ STRUC-PERC bridge
 ├── engine_server.js    # Puppeteer interface to chamber
 ├── analysis.py         # commutators, transitions
 └── data/base_ladders   # input datasets (.csv / .txt)
📁 Folder Structure
.
├── data/
│   └── base_ladders/        # input datasets
│
├── output/
│   ├── ladders/             # generated transformed ladders
│   ├── *_results.json       # raw chamber outputs
│   └── *_metrics.csv        # extracted structural metrics
│
├── Docs/                    # optional documentation
├── FULL_OUTPUT/             # archived runs
├── node_modules/            # Puppeteer dependencies
│
├── runner.py                # main execution pipeline
├── config.py               # configuration
├── operators.py            # α, μ operators
├── engine_bridge.py        # engine interface
├── engine_server.js        # chamber automation
├── run_struc_perc.js       # Puppeteer script
├── analysis.py             # derived analysis
│
└── struc_perc_i_v2_4_0.html   # STRUC-PERC chamber
⚙️ Configuration

Defined in config.py:

Parameter grids
ALPHA_GRID = np.linspace(0.80, 1.20, 17)
MU_GRID    = np.linspace(0.80, 1.20, 17)
STRUC-PERC settings
K_POINTS = 17
K_MIN    = 0.01
K_MAX    = 1.0
▶️ Running the System

From root directory:

python runner.py
🔄 Pipeline Execution

For each dataset:

for ladder in BASE_LADDERS:
    for α in ALPHA_GRID:
        for μ in MU_GRID:

Steps:

Load ladder (CSV/TXT)
Normalize (sort + deduplicate)
Apply operators:
forward
reverse
Run STRUC-PERC chamber
Parse output (JSON)
Extract metrics
Save results
📊 Output Files
1. Raw Results
output/<name>_results.json

Contains:

forward / reverse runs
full chamber output
commutator
2. Metrics (Primary Data)
output/<name>_metrics.csv

Columns:

field	meaning
ladder	dataset name
alpha, mu	parameters
verdict	chamber classification
kappa	connectivity threshold
components	final component count
giant_ratio	dominant component size
outliers	anomaly count
depth_type	structural depth class
mechanism	fragmentation mechanism
🧩 Structural Classification

Derived automatically:

Depth Types
Type	Meaning
HARD	no stable connectivity
SHALLOW_FULL	early connectivity
DELAYED_FULL	mid-range connectivity
DEEP_FULL	late connectivity
EXTREME_FULL	extreme threshold
Mechanisms
Type	Meaning
RUPTURE	structural break
TAIL	outlier-driven
NONE	stable
🔬 Interpretation

Each dataset produces a field over (α, μ):

F(α, μ) → structural response

This enables:

detection of invariant regions
identification of rupture zones
operator-induced transitions
domain-dependent structural behavior
🧠 What This System Is

This is not a simple runner.

It is a:

Parameterized Structural Response Field Generator

🚀 Next Step

The generated CSV files are designed for:

phase diagram construction
regime boundary detection
structural law extraction
⚠️ Notes
STRUC-PERC chamber must be present locally
Puppeteer must be installed (node_modules)
Engine returns JSON (string → parsed in pipeline)
Input ladders must contain numeric values only
🔧 Troubleshooting
No output / freeze

→ engine_server.js path or HTML missing

JSON errors

→ engine output malformed (handled with fallback)

No datasets detected

→ check data/base_ladders

📌 Status

✔ Fully operational
✔ Batch execution stable
✔ Metrics extraction integrated
✔ Ready for phase mapping

🧭 Direction

This system is the computational backbone for:

structural regime theory
operator-driven phase transitions
cross-domain admissibility analysis