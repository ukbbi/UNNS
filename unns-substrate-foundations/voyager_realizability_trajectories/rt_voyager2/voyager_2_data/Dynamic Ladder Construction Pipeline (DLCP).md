# ⚙️ Dynamic Ladder Construction Pipeline (DLCP)  
### Voyager 2 Plasma → UNNS / STRUC-PERC-I Ready Ladders

---

## 🧭 Overview

The **Dynamic Ladder Construction Protocol (DLCP)** transforms raw **Voyager 2 plasma CDF data** into **STRUC-PERC-I compatible structural ladders**.

It converts time-series plasma measurements into **sorted realizability structures** across sliding windows, enabling **dynamic trajectory analysis** within the UNNS Substrate.

---

## 📦 Output

For each `.cdf` file, the pipeline produces:


output/
voyager_<file>WIN<index><start><end>/
L_V.txt
L_dens.txt
L_T.txt
L_w.txt


Each file is:

- ✅ **STRUC-PERC-I ready**
- ❌ **No further preprocessing required**

---

## 🔬 Observables Extracted

- **V** — velocity  
- **dens** — density  
- **T** — temperature  
- **w** — thermal speed  

---

## ⚙️ Processing Steps

### 1. Data Cleaning
- Remove NaN values  
- Remove CDF fill values  
- Ensure synchronized variables  

### 2. Window Segmentation
- Sliding windows over time-series  
- High-integrity filtering  

### 3. Ladder Construction
- Sorted values per observable  

---

## 🧱 DLCP Structure (UNNS-Aligned)

### Stage 1 — Primary Ladder

L_V = sorted(V)


### Stage 2 — Parallel Ladders

L_dens = sorted(dens)
L_T = sorted(T)
L_w = sorted(w)


### Stage 3 — Embedded State

Each window produces:


(L_V, L_dens, L_T, L_w)


👉 This defines a **local point in realizability space**

---

## 📏 Window Parameters

| Parameter | Value | Description |
|----------|------|------------|
| WINDOW_SIZE | 1024 | samples per window |
| STEP_SIZE | 256 | sliding stride |
| MIN_VALID_RATIO | 0.95 | minimum valid data |

---

## 🧼 Data Integrity

Ensures:

- high-quality windows  
- synchronized multi-variable structure  
- no artificial smoothing  

---

## ⚖️ Normalization Mode


NORMALIZE = False


- **False** → raw physical structure (**recommended**)  
- **True** → normalized ladders (comparative analysis)

---

## ▶️ How to Run

### Install dependency
```bash
python -m pip install cdflib
Execute pipeline
python voyager_ladder_pipeline.py
🧠 Interpretation Layer

Each window represents:

a time-local structural snapshot

Across all windows:

a trajectory in realizability space

🔗 Next Step (Critical)

DLCP outputs are not final results.

They must be processed through:

⚙️ STRUC-PERC-I Chamber

Per ladder:

regime classification
connectivity κ
margin m(L)
tail dominance
🌌 Role in UNNS Framework

DLCP enables:

transition from static ladders → dynamic trajectories
testing of:
temporal stability
regime confinement
boundary approach
⚠️ Limitations
Requires correct CDF variable names (V, dens, T, w)
Assumes uniform sampling cadence
Does not perform STRUC analysis
📌 Summary

DLCP is:

the entry point from real astrophysical data into the UNNS Substrate

It performs:

time-series plasma data
        ↓
structural ladders
        ↓
STRUC-ready realizability input

---

# 🧠 What this fixes

Compared to your version:

- ✔ consistent headers  
- ✔ real tables (not text blocks)  
- ✔ proper code blocks (safe ones)  
- ✔ visual hierarchy  
- ✔ aligned with your main README style  
- ✔ looks like a **pipeline spec, not notes**

---

# 🚀 Where this belongs

Put this as:

``` id="c1n6yj"
rt_voyager2/protocol/README.md