# STRUC-PERC Batch Runner (α, μ)

## Overview

This folder contains a complete pipeline for running **operator-driven structural analysis** using the STRUC-PERC engine.

The system performs batch evaluation of ladders under joint deformation by:

* α (alpha operator)
* μ (mu operator)

and maps resulting **structural regimes**, **commutator behavior**, and **connectivity metrics**.

---

## What This System Does

For each input ladder:

1. Applies α–μ transformations
2. Runs STRUC-PERC engine
3. Computes:

   * regime verdicts
   * connectivity metrics
   * forward vs reverse differences (commutator)
4. Saves:

   * JSON results (full grid)
   * TXT ladders (inspection-ready)
   * optional CSV exports

---

## Folder Structure

```
.
├── data/
│   └── base_ladders/        # input ladders (.txt / .csv)
│
├── output/
│   ├── ladders/             # generated ladders (TXT)
│   └── *.json               # batch results
│
├── Docs/
│   ├── Methods.md
│   └── Phase Mapping Protocol.md
│
├── runner.py                # main batch executor
├── config.py                # grids, paths, dataset config
├── operators.py             # α and μ implementations
├── analysis.py              # commutator + transition logic
├── engine_bridge.py         # Python → Node → STRUC-PERC bridge
│
├── run_struc_perc.js        # Node runner for engine
├── engine_server.js         # optional server layer
│
├── struc_perc_i_v2_4_0.html # STRUC-PERC engine (UI + core)
│
├── test.txt / test.csv      # sample input files
└── package.json             # Node dependencies
```

---

## How It Works

### Pipeline

```
ladder → α/μ transforms → STRUC-PERC → metrics → aggregation
```

### Execution Layers

* **Python**

  * orchestration
  * batching
  * data handling

* **Node.js**

  * executes engine script
  * extracts JSON from browser-like environment

* **HTML Engine**

  * performs structural computation

---

## How to Run

### 1. Install Node dependencies

```bash
npm install
```

### 2. Run batch

```bash
python runner.py
```

---

## Input Formats

Supported:

* `.txt`

  ```
  0 1 2 3 10 11 12
  ```

* `.csv`

  ```
  0,1,2,3,10,11,12
  ```

All inputs are automatically parsed into numeric arrays.

---

## Output

### JSON (main result)

```
output/<dataset>_results.json
```

Contains:

* forward results
* reverse results
* commutator

---

### TXT ladders

```
output/ladders/
```

Each file:

* one ladder
* STRUC-PERC compatible
* ready for manual inspection

---

### CSV (optional)

Structured export of ladders or results.

---

## Manual Inspection (Important)

To inspect any case:

1. Open:

   ```
   struc_perc_i_v2_4_0.html
   ```
2. Paste ladder from:

   ```
   output/ladders/*.txt
   ```
3. Click **RUN FULL PRP**
4. Observe structure

---

## Key Concepts

### Forward vs Reverse

* Forward: μ(α(L))
* Reverse: α(μ(L))

---

### Commutator

Measures operator interaction:

* Δ_giant
* Δ_kappa
* verdict difference

---

### Regimes

STRUC-PERC classifies into:

* FULL
* CRITICAL
* SOFT
* HARD_FRAGMENTATION

---

## Current Status

✅ Engine working
✅ Python pipeline working
✅ Node bridge working
✅ Batch execution stable
✅ Output generation complete

---

## Important Notes

* Synthetic datasets are used for **testing only**
* No physical conclusions should be drawn from them
* Real datasets are required for research results

---

## Next Steps

* Run real datasets:

  * HD
  * D₂
  * CO₂
  * geoid / cosmological ladders

* Analyze:

  * phase transitions
  * commutator structure
  * regime boundaries

---

## Purpose

This system is designed to:

> Map structural behavior under operator deformation and detect regime dynamics across domains.

---

## Version

STRUC-PERC Engine: v2.4.0
UNNS Substrate Research Program — 2026

---

## Author Context

Part of the **UNNS Substrate project**
Focused on **operator-driven structural regime theory**

---
