# Crystallography → UNNS Ladder & Transition Analysis

This folder contains the full pipeline and outputs for converting crystallographic CIF data into UNNS-compatible structural ladders and analyzing their dimensional behavior under deformation.

---

# 📁 Folder Structure

crystallogrphy_cif_to_ladders_strict/
│
├── crystallography_cifs_input/ # Raw CIF files (input)
├── crystal_ladders_expanded/ # Generated distance ladders (expanded structures)
├── crystal_ladders_fixed/ # Strict-filter ladders (high-quality subset)
├── crystal_transition_data/ # Transition outputs (α, m, dim vs B)
│
├── crystal_ladders_expanded.zip # Zipped expanded ladders
├── crystal_ladders_fixed.zip # Zipped filtered ladders
├── crystal_transition_data.zip # Zipped transition datasets
│
└── crystallography_transition_generator.py # Main generator


---

# 🧠 Purpose

This pipeline converts **crystallographic structures** into:

1. **Distance ladders** (structural spectra)
2. **Deformation responses** under controlled operator \( B \)
3. **Dimensional regime classification**

Goal:

> Extract **dimensional structure (dim)**, **scaling (α)**, and **margin (m)** from real crystal systems and compare them to atomic and cosmological domains.

---

# ⚙️ Pipeline Overview

## Step 1 — Input (CIF files)

Located in:

crystallography_cifs_input/


Each `.cif` file contains:
- minimal asymmetric unit
- symmetry-compressed structure

---

## Step 2 — Structure Expansion

Using `pymatgen`:

```python
structure.make_supercell([3,3,3])

This reconstructs a full atomic environment, resolving the key issue:

CIF ≠ full structure
Step 3 — Ladder Construction

From expanded atomic positions:

3D coordinates → pairwise distances → sorted spectrum

Output:

crystal_ladders_expanded/*.csv

Each file:

value
d₁
d₂
d₃
...
Step 4 — Deformation Sweep

Apply structural deformation:

B ∈ [0, 1]

For each B:

deform ladder
compute gaps
extract:
alpha (α) → scaling exponent
m         → margin (order)
gamma     → energy scaling
dim       → effective dimension

Output:

crystal_transition_data/*.csv
📊 Output Meaning

Each transition file contains:

file, B, alpha, gamma, m, dim

Interpretation:

Quantity	Meaning
dim	Number of active structural degrees of freedom
α	scaling behavior of gaps
m	structural order (uniformity of gaps)
γ	spectral growth exponent
🔍 Observed Results (This Run)
1. Dominant Regime

Most crystallographic systems:

dim = 3 (stable)

→ fully activated structural regime

2. Rare Transition

Observed:

Fe_mp-150 — dim 1 → 3 at low B

→ discrete structural activation

3. Universal Drift

Across rigid systems:

α → ~1.3–1.45
m → ~0.57–0.60
γ → ~0.31–0.34

→ convergence toward a common structural corridor

🧠 Interpretation

Crystallography shows:

A) Structural rigidity

Most crystals are already in a maximal dimensional regime

B) Hidden activation (rare)

Some structures (e.g., Fe variant) start in reduced dimension and activate

C) Cross-domain alignment

Behavior differs from:

Domain	Behavior
Atomic (Zeeman)	strong transitions
Cosmology	low-dim rigid
Crystallography	high-dim rigid

⚠️ Important Notes
CIF limitations

CIF files contain:

minimal atomic sets
symmetry encoding

Without expansion:

→ degenerate ladders
→ dim collapse
→ m = NaN

This pipeline fixes that.

Ladder validity conditions

A structure is accepted only if:

sufficient atoms AND sufficient pairwise distances

Rejected cases indicate:

under-specified CIF
too small unit cell
insufficient structural richness
🚀 How to Run
pip install pymatgen
python crystallography_transition_generator.py
📌 What This Folder Represents

This is the crystallographic branch of the UNNS dimensional program:

Structure → Ladder → Deformation → Dimension

It provides:

real-world condensed matter validation
comparison with atomic and cosmological datasets
evidence for dimension as a structural invariant