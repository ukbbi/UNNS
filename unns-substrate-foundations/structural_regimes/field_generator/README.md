# ⚙️ Structural Field Generator (α, μ)

### Operator-Driven Transition Detection over UNNS Ladders

---

## 🧭 Overview

This module implements a parameterized structural response scanner over operator space:

(α, μ)

It evaluates how ladders evolve under deformation using forward operator composition:

μ ∘ α

The transformed ladders are evaluated through the STRUC-PERC-I v2.4.0 chamber to detect structural regime behavior and boundary transitions.

---

## 🔑 Core Function

For each input ladder L:

L′ = μ(α(L))

The system evaluates L′ and extracts:

- structural regime (verdict)
- connectivity threshold (κ)
- dominant component ratio

---

## 🎯 What This System Does

This system performs a directed scan of operator space to:

- detect structural regime transitions
- identify first admissibility boundary
- measure robustness under deformation

The scan terminates early once a regime change is detected.

---

## ⚠️ Important Limitations

This implementation:

- uses forward operator only (μ ∘ α)
- performs early-stop transition detection
- extracts a minimal set of structural metrics

It does NOT:

- compute reverse operator composition (α ∘ μ)
- compute commutators
- generate full phase fields

---

## 🧱 Folder Structure

field_generator/

├── data/
│   └── base_ladders/          input datasets (CSV or TXT)

├── output/                    results and metrics

├── node_modules/              Puppeteer dependencies (do not commit)

├── analysis.py                metric extraction helpers
├── config.py                  α, μ grids and STRUC parameters
├── config_breakdown.py        alternative configuration definitions
├── convert_csv_to_txt.py      CSV → ladder TXT converter
├── engine_bridge.py           Python ↔ Node interface
├── engine_server.js           Puppeteer execution engine
├── operators.py               α and μ transformations
├── runner.py                  main execution engine
├── run_struc_perc.js          STRUC-PERC runner
├── split_ladder.py            dataset augmentation tools

├── struc_perc_i_v2_4_0.html   STRUC-PERC chamber
└── README.md

---

## ⚙️ Configuration

Defined in config.py:

ALPHA_GRID = np.linspace(0.80, 1.20, 17)  
MU_GRID    = np.linspace(0.80, 1.20, 17)  

K_POINTS = 17  
K_MIN    = 0.01  
K_MAX    = 1.0  

---

## ▶️ Execution

Run from the module directory:

python runner.py

---

## 🔄 Pipeline Logic

For each dataset:

1. Load ladder (CSV or TXT)
2. Normalize:
   - remove duplicates
   - sort values
3. Reduce ladder size if necessary
4. Auto-sparsify to target connectivity (κ ≈ 1.0)
5. Scan parameter space:

for α in ALPHA_GRID:
    for μ in MU_GRID:
        L′ = μ(α(L))
        R  = STRUC(L′)

---

## 🚨 Transition Detection

The system detects the first structural regime change:

- initial verdict is recorded
- scanning continues over (α, μ)
- execution stops when verdict changes

This identifies the first admissibility boundary in operator space.

---

## 📊 Output

Results are stored in:

output/<name>_results.json  
output/<name>_metrics.csv  

Metrics include:

- ladder name
- alpha, mu parameters
- structural verdict
- connectivity threshold (κ)
- giant component ratio

---

## 🔬 Preprocessing Tools

convert_csv_to_txt.py  
Converts CSV datasets into sorted ladder TXT format.

split_ladder.py  
Generates derived ladders:
- lower / upper splits
- stride-based subsets

These expand the dataset space for structural testing.

---

## 🧠 Interpretation

Each ladder produces a trajectory in operator space until structural transition.

This reveals:

- deformation tolerance
- regime stability
- location of structural boundary

---

## 🔗 Role in UNNS Framework

This module functions as:

- a structural stress-testing system
- a boundary detector in realizability space
- an empirical input to Phase Mapping Protocol

It connects operator deformation with structural admissibility.

---

## ⚠️ Practical Notes

node_modules/ should not be committed to GitHub.  
Use a .gitignore entry:

node_modules/

Ensure STRUC-PERC HTML chamber is accessible locally.

---

## 📌 Status

- operational
- stable execution
- transition detection validated


---

## 🧠 Conceptual Summary

This system identifies where a structure ceases to remain admissible under deformation.

That point defines the boundary of realizability in operator space.