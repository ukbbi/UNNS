# UNNS Scaling Extraction — Dimensional Regime Analysis

## Overview

This module is part of the **UNNS Substrate project** and is designed to extract **scaling exponents** from structured physical datasets in order to study:

> **how dimensionality emerges from structural scaling behavior rather than being assumed a priori**

The core idea is that physical systems (atomic spectra, gap structures, Zeeman ladders, etc.) can be classified not by predefined dimensions, but by their **scaling signatures**.

---

## Purpose

The purpose of this pipeline is to:

* Extract measurable scaling exponents from real datasets
* Identify **structural regimes** using these exponents
* Infer **effective dimensionality (dim_eff)** as an emergent property
* Test the UNNS hypothesis:

> **Dimensionality is not fundamental — it is an emergent signature of margin-regulated structural admissibility**

---

## What the Script Does

The script:

```
unns_scaling_extractor.py
```

automatically processes all `.csv` files in its directory and computes:

### 1. Energy Scaling Exponent (γ)

* Derived from ordered energy levels
* Captures how the system expands structurally
* Represents **observable scaling behavior**

---

### 2. Gap Scaling Exponent (α)

* Derived from differences between adjacent levels
* Captures internal structural organization
* Separates regimes:

| α value | Interpretation                  |
| ------- | ------------------------------- |
| α < 0   | Compressed / constrained regime |
| α ≈ 0   | Transitional regime             |
| α > 0   | Expansive / spectral regime     |

---

### 3. Margin Proxy (m)

* Computed from median and dispersion of gaps
* Represents **connectivity stability**
* Observed to remain within a narrow band across systems

> This supports the UNNS claim that margin governs admissibility

---

### 4. Effective Dimension (dim_eff)

* Computed via covariance structure of gap sequences
* Measures number of active structural degrees of freedom

> This is the key output:
>
> **Dimension is inferred — not assumed**

---

## Input Data

The script expects `.csv` files representing structured physical data, such as:

* Atomic spectra (`*_spectrum_*.csv`)
* Gap structures (`*_gap_structure_*.csv`)
* Zeeman ladders (`*_zeeman_ladder.csv`)

Typical columns include:

* `energy_cm-1`
* `gap_cm-1`
* `Level`, `Level0_cm1`, etc.
* `B_T` (for Zeeman datasets)

The script automatically detects relevant columns.

---

## How to Use

### Step 1 — Place Files

Put all `.csv` files in the same folder as:

```
unns_scaling_extractor.py
```

---

### Step 2 — Run

```bash
python unns_scaling_extractor.py
```

---

### Step 3 — Output

The script creates:

```
/output/results.csv
```

Each row contains:

* file name
* scaling exponents (γ, α)
* margin proxy (m)
* effective dimension (dim_eff)

---

## Interpretation Framework

The extracted values define a **structural phase space**:

* **α (alpha)** → internal structure regime
* **γ (gamma)** → observable scaling
* **m (margin)** → stability constraint
* **dim_eff** → emergent dimensionality

---

## Key Insight

Across multiple domains (atomic, spectral, perturbative):

* Scaling behavior is consistent
* Margin remains constrained
* Dimensionality emerges from structure

This supports the central UNNS statement:

> Physical systems are not defined by fixed dimensions, but by their position within a scaling regime governed by connectivity margin.

---

## Current Stage

This pipeline corresponds to:

> **Transition from theoretical framework → testable physics**

We now have:

* measurable exponents
* cross-domain consistency
* reproducible extraction

---

## Next Steps

* Derive explicit mapping:

  ```
  dim_eff = F(α, m)
  ```

* Construct regime phase diagrams

* Compare across domains (atomic, cosmological, geoid, etc.)

* Validate universality of margin constraint

---

## Summary

This tool operationalizes a core UNNS claim:

> **Dimension is not a starting assumption — it is an output of structural scaling.**

The `unns_scaling_extractor.py` script is the first step in turning this claim into a **quantitative, testable framework**.

---
