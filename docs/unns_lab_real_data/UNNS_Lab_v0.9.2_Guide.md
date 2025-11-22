UNNS Laboratory v0.9.2 — Research Preview Guide

File: unns_lab_v0_9_2.html
Status: Research Preview (τ-Field Structural Validation Layer)
Updated: v0.9.2 — November 2025

🌐 Overview

unns_lab_v0_9_2.html is the official τ-Field Real Data Assimilation Laboratory for the UNNS Substrate.

It provides a complete workflow for evaluating the τ-Microstructure Hypothesis using real molecular spectral data (CaF, SrF, BaF, YbF, RaF, etc.).
This version integrates:

✔ v0.9.1 nonlinear τ-projection

✔ v0.9 manifold-aware hyperfine engine

✔ v0.9.2 Quality Metrics Layer

✔ ΔC & g<sub>ω</sub> multi-manifold τ-coupling solver

✔ Modernized Laboratory Guide (Research Preview)

🧩 Features in v0.9.2
1. Nonlinear τ-Projection Engine (v0.9.1)

Aligns synthetic τ-field spectral predictions with real hyperfine transitions using a 6-term nonlinear projection model:

f_real ≈ a₀ + a₁ f_syn + a₂ C + a₃ |C·τ| + a₄ τ + a₅ f_syn²

2. Hyperfine Manifold Engine (v0.9)

Groups lines by manifold_id and computes per-manifold statistics:

Mean residual

RMSE

χ²/dof

Curvature statistics

Centroid frequency

3. τ-Hyperfine Coupling Solver (v0.9.2)

Fits manifold centroids to obtain:

ΔC — curvature offset

g<sub>ω</sub> — τ-spin coupling coefficient

4. NEW Quality Metrics Layer (v0.9.2)

Independent structural & experimental evaluation:

Raw χ²/dof

Normalized χ²/dof (structural)

σ-Weighted χ²/dof (uncertainty-sensitive)

κ — curvature–residual coherence

R — manifold reliability

τ<sub>R</sub> — unified τ-reliability

ΣP — expected outliers

📊 Workflow

Load real dataset (CaF, SrF, BaF, YbF, RaF, etc.)

Run nonlinear τ-projection

Inspect manifolds and residual structure

Compute quality metrics (χ², κ, R, τ<sub>R</sub>)

Evaluate τ-hyperfine coupling (ΔC & g<sub>ω</sub>)

Export results (JSON)

📁 File Structure (for GitHub)
/UNNS/
 ├─ unns_lab_v0_9_2.html          ← main lab interface
 ├─ engine/
 │    ├─ projection_v091.js
 │    ├─ manifolds_v09.js
 │    ├─ quality_v092.js          ← NEW v0.9.2 logic
 │    └─ coupling_v092.js
 ├─ data/
 │    ├─ CaF.json
 │    ├─ SrF.json
 │    ├─ BaF.json
 │    └─ comparison_templates/
 └─ docs/
      └─ UNNS_Lab_v0.9.2_Guide.md ← this file

## 🧩 Key Concepts Introduced in v0.9.2

### Structural vs Experimental Metrics

- **χ²<sub>norm</sub>** — evaluates **τ-structure adequacy**  
- **χ²<sub>σ-weighted</sub>** — evaluates **dataset precision**

> These two must never be mixed.

---

### Manifold Reliability

R = exp(−κ · (χ²<sub>norm</sub> / 20))

---

### Unified τ-Reliability v2

τ<sub>R</sub> = mean(R<sub>manifold</sub>)

---

### Expected Outliers

P<sub>i</sub> = 1 − exp(−(|Δf<sub>i</sub>| / 20)²)


🧪 Validation Notes

v0.9.2 does not modify matching, calibration, the τ-projection polynomial, or ΔC/g<sub>ω</sub> computation.

All new metrics run in parallel (additive, non-destructive).

Hyperfine parameters must remain identical to v0.9.1 for identical datasets.

Weighted χ² may be large for high-precision molecules — this is expected.

📝 Change Log (v0.9.2 Research Preview)

Added Quality Metrics Layer (σ-weights, κ, R, τ<sub>R</sub>, ΣP)

Replaced legacy τ-MSC with the modern τ-MSA framework

Updated workflow to reflect v0.9.2 pipeline

Consolidated 6-term nonlinear projection model

Updated hyperfine engine documentation

Reorganized Guide to match real engine architecture

Labeled v0.9.2 as Research Preview pending multi-molecule validation

📄 Licensing

This file is part of the UNNS Substrate Research Project.
Refer to the root repository for license terms.