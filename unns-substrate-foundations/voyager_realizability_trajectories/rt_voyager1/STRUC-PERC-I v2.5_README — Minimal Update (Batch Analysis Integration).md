# STRUC-PERC-I v2.5.0

**README — Minimal Update (Batch Analysis Integration)**

---

## Overview

Version **v2.5.0** introduces a **single functional upgrade**:

> **Batch analysis capability**

No changes were made to:

* mathematical definitions
* graph construction
* percolation logic
* verdict system
* theoretical interpretation

The engine remains **identical in behaviour per ladder** to v2.4.0.

---

## 🔒 What is Fully Preserved

All core components from v2.4.0 remain unchanged:

---

### 1. Full Pairwise Vulnerability Graph

* Exact PRP definition preserved
* No approximation changes
* Same edge condition:

ε = κ · IQR(Δ) (fallback: median)

---

### 2. Percolation Logic

* Strict no-reset continuity
* Same chain construction
* Same κ* detection
* Same spanning requirement

---

### 3. 4-Tier Verdict System

* FULL
* GIANT
* TAIL
* HARD

No thresholds or criteria modified.

---

### 4. Domain Adapters

* Same adapters
* Same preprocessing rules
* No transformation changes

---

### 5. Outlier Analysis

* Same detection rules
* Same thresholds
* Same influence metrics

---

### 6. Adaptive κ Extension

* Same logic
* Same stopping conditions
* Same interpretation

---

### 7. Theoretical Status

Unchanged:

* Theorem 1 (necessary direction): **established**
* Sufficient direction: **open**

---

## 🚀 What Was Added

### Batch Analysis Mode

v2.5.0 allows:

* running **multiple ladders in sequence**
* processing datasets without manual re-entry
* automating repeated structural evaluation

---

### What This Means Practically

You can now:

* analyze entire datasets (e.g. Voyager, spectral series)
* compare ladders consistently
* scale experiments without modifying the engine

---

### What It Does NOT Change

Batch mode:

* does **not alter computation**
* does **not merge ladders**
* does **not affect results**

Each ladder is still:

> processed independently using the exact v2.4.0 pipeline

---

## 🧠 Conceptual Position

v2.5.0 is:

> **an execution-layer extension, not a theoretical or algorithmic change**

---

## 📊 Version Difference (Precise)

| Aspect            | v2.4.0        | v2.5.0             |
| ----------------- | ------------- | ------------------ |
| Core algorithm    | unchanged     | unchanged          |
| Graph model       | unchanged     | unchanged          |
| Percolation logic | unchanged     | unchanged          |
| Verdict system    | unchanged     | unchanged          |
| Input mode        | single ladder | single + batch     |
| Output            | per run       | per run (repeated) |

---

## ✔ Compatibility

* Fully backward compatible
* Identical results for identical input
* No recalibration required

---

## Final Statement

v2.5.0 introduces **only one capability**:

> **the ability to run the same validated engine repeatedly over multiple ladders**

Nothing else has changed.

---

## Interpretation

This version marks a shift from:

> **manual analysis**

to

> **systematic experimentation**

— without altering the underlying theory or computation.

---
