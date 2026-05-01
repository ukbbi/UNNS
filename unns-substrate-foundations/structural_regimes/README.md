# ⚙️ Parameterized Structural Response Scanner (α, μ)

### Transition Detection in Operator-Deformed UNNS Ladders

---

## 🧭 Overview

This module implements a parameterized system for scanning structural response of ladders under  
operator deformation:

(α, μ)

It evaluates how structural regimes evolve when a base ladder is transformed by:

μ ∘ α

using the **STRUC-PERC-I v2.4.0 chamber**.

---

## 🔑 Core Idea

Each input ladder L is transformed over a parameter grid:

(α, μ) ∈ [0.80, 1.20] × [0.80, 1.20]

For each pair:

L′ = μ(α(L))

The transformed ladder is evaluated structurally to determine:

- regime (verdict)  
- connectivity threshold (κ)  
- dominant component ratio  

---

## 🎯 What This System Does

This module performs a directed scan of operator space to:

- detect structural regime transitions  
- identify first boundary crossings  
- track stability under deformation  

---

## ⚠️ Important Clarification

This system:

- ✔ uses forward operator composition only (μ ∘ α)  
- ✔ performs early-stop transition detection  
- ✔ extracts core structural metrics  

This system does NOT:

- ✖ compute reverse operator order (α ∘ μ)  
- ✖ compute commutators  
- ✖ generate full phase fields  

---

## 🧱 System Architecture

runner.py  
├── config.py           (parameter grids and constants)  
├── operators.py        (α and μ transformations)  
├── engine_bridge.py    (STRUC-PERC interface)  
├── engine_server.js    (Puppeteer execution layer)  
└── analysis.py         (metric helpers, partial use)  

---

## 📂 Folder Structure

data/  
&nbsp;&nbsp;└── base_ladders/          (input datasets)

output/  
&nbsp;&nbsp;├── *_results.json         (raw structural outputs)  
&nbsp;&nbsp;└── *_metrics.csv          (extracted metrics)

core scripts:  
&nbsp;&nbsp;runner.py  
&nbsp;&nbsp;config.py  
&nbsp;&nbsp;operators.py  
&nbsp;&nbsp;engine_bridge.py  
&nbsp;&nbsp;analysis.py  

STRUC-PERC chamber:  
&nbsp;&nbsp;struc_perc_i_v2_4_0.html  

---

## ⚙️ Configuration

Defined in `config.py`:

Parameter grid:

ALPHA_GRID = np.linspace(0.80, 1.20, 17)  
MU_GRID    = np.linspace(0.80, 1.20, 17)  

STRUC parameters:

K_POINTS = 17  
K_MIN    = 0.01  
K_MAX    = 1.0  

---

## ▶️ Execution

Run from project root:

python runner.py

---

## 🔄 Pipeline Logic

For each ladder:

1. Load ladder from file  
2. Normalize (sort and deduplicate)  
3. Reduce size if necessary  
4. Auto-sparsify to target connectivity (κ ≈ 1)

Then perform parameter scan:

for α in ALPHA_GRID:  
&nbsp;&nbsp;for μ in MU_GRID:  
&nbsp;&nbsp;&nbsp;&nbsp;L′ = μ(α(L))  
&nbsp;&nbsp;&nbsp;&nbsp;R  = STRUC(L′)  

---

## 🚨 Transition Detection

The system tracks structural regime changes:

- the first verdict is stored  
- scanning continues across (α, μ)  
- execution stops at first regime change  

This identifies:

→ the first structural boundary in operator space  

---

## 📊 Output Structure

### Results JSON

output/<name>_results.json  

Contains:

- structural outputs per (α, μ)  
- detected transition (if present)  

---

### Metrics CSV

output/<name>_metrics.csv  

Fields:

- ladder → dataset name  
- alpha, mu → operator parameters  
- verdict → structural regime  
- kappa → connectivity threshold  
- giant_ratio → dominant component size  

---

## 🔬 Preprocessing

### Normalization

- removes duplicate values  
- sorts ladder  

---

### Auto-Sparsification

Function: auto_sparsify_to_kappa()

Purpose:

- reduces ladder size  
- adjusts sampling to target κ ≈ 1.0  
- preserves structural behavior  

---

## 🧠 Interpretation

Each ladder produces:

→ a trajectory in operator space until structural transition  

This reveals:

- structural robustness  
- deformation sensitivity  
- location of admissibility boundary  

---

## 🔗 Role in UNNS Framework

This module provides:

- empirical detection of regime boundaries  
- operator-based stress testing  
- input for Phase Mapping Protocol  

It acts as:

→ a practical boundary detector in realizability space  

---

## ⚠️ Limitations

- forward operator order only (μ ∘ α)  
- no commutator computation  
- partial exploration (early stop)  
- limited metric extraction  

---

## 📌 Status

- ✔ operational  
- ✔ stable execution  
- ✔ transition detection validated  
- ⚠ full phase mapping not implemented  

---

## 🧠 Conceptual Summary

Realizability is probed by deformation.

This system identifies where a structure:

→ ceases to remain admissible under operator action  

That point defines:

→ the boundary of realizability in operator space  