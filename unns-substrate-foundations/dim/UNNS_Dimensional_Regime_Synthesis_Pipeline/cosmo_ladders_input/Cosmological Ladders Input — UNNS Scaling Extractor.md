# Cosmological Ladders Input — UNNS Scaling Extractor

## Purpose

This folder contains **cosmological datasets already expressed in canonical UNNS ladder form**.

These files are **ready for direct ingestion** by:

unns_scaling_extractor.py


No conversion, reshaping, or preprocessing is required.

---

## What “ladder form” means

Each file represents a **1D ordered sequence of values**:

value_1
value_2
value_3
...
value_N


This sequence is interpreted as a **gap ladder** by the extractor:

- ordering → defines structure
- differences → define gaps
- gaps → define structural invariants

---

## Files in this folder

### Cosmological datasets

- `cw_2mrs_xyz_full_radial_ladder.csv`  
  → 2MRS galaxy distribution (radial ordering)

- `cw_desi_synthetic_xyz_radial_ladder.csv`  
  → DESI synthetic cosmological structure

- `cw_desi_xyz_sample_radial_ladder.csv`  
  → DESI observed sample (XYZ-based radial ordering)

- `desi_sample_ra_dec_z_redshift_ladder.csv`  
  → DESI redshift ladder (cosmic expansion structure)

- `sdss_cw2_generic_ladder.csv`  
  → SDSS-derived cosmic web representation

---

## Important: No conversion needed

These files are **NOT raw cosmology data**.

They are already:

✔ sorted  
✔ reduced to 1D structural representation  
✔ numerically valid (floats)  
✔ suitable for gap extraction  

👉 Therefore:

DO NOT run any converter on these files


---

## How they are used

When passed into the extractor:

python unns_scaling_extractor.py


Each file produces:

- α (gap scaling exponent)
- m (connectivity margin)
- dim (effective dimensionality)
- γ (energy scaling proxy)

---

## Role in the project

These datasets serve as the **cosmological sector** of the UNNS phase space:

(α, m, dim)


They are used to:

- compare against atomic systems (Zeeman ladders)
- compare against materials (DFT / band structures)
- test cross-domain structural invariants
- verify dimensional stability under deformation

---

## Key structural properties (observed)

From current analysis:

- α → tightly clustered (domain-compressed)
- m → overlaps with atomic margin band (~0.577)
- dim → mostly low (1–2)
- deformation response → negligible (structurally stable)

---

## Common failure modes

If extractor reports:

[ERROR] No usable data


Check:

### 1. File format
- Must be **single-column numeric**
- No headers like `value`

### 2. Hidden text contamination
- Remove strings / column labels

### 3. Encoding issues
- Ensure UTF-8 without BOM

---

## DO NOT

- ❌ Convert to Zeeman format  
- ❌ Add artificial B column  
- ❌ Shuffle ordering  
- ❌ Normalize arbitrarily  

These break structural meaning.

---

## Summary

This folder represents:

> Cosmological structures already reduced to their **pure structural form**

They are:

- domain-independent
- directly comparable to atomic and material systems
- essential for mapping the **UNNS structural phase space**

---