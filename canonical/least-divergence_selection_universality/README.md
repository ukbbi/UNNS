# Least-Divergence Selection — Universality (L4)

This folder contains the **canonical L4 materials** demonstrating the universality and inevitability of **least-divergence selection** in the UNNS Substrate.

It finalizes the transition from *robustness* to *necessity* by showing that least-divergence outcomes persist under both **decision perturbations** and **ordering (history) perturbations**, including the discrete-cost regime.

---

## Folder Contents

### Interactive Chamber

- **`chamber_xxxi_v1_0_6.html`**  
  **Chamber XXXI — Refinement Geodesic Computer**

  The primary experimental instrument used in L4 validation.  
  Supports:
  - σ = 0 exact determinism
  - σ-sweeps under ordering noise (Mode B)
  - discrete cost quantum detection
  - reproducible seeded runs
  - JSON export for aggregation

  This chamber explicitly attempts to falsify least-divergence selection by perturbing exploration history rather than evaluation.

---

### Public Showcase Articles (unns.tech)

- **`chamber_xxxi_showcase_unns_tech.html`**  
- **`chamber_xxxi_showcase_unns_tech_2.html`**

  Public-facing UNNS.tech articles presenting Chamber XXXI and its findings using:
  - static SVGs
  - animated SVGs (no JavaScript)
  - user.css–compatible layout

  These articles translate the technical results into a readable narrative without relying on internal layer terminology.

---

### Core Validation Artifact

- **`mode_b_validation_results.png`**

  Central empirical result of L4:

  - sharp exploration phase transition at **σ ≈ 1.0**
  - discrete cost quantum revealed as a structural scale
  - least-divergence geodesics remain stable across the transition

  This figure captures the key invariance: exploration volume changes, outcomes do not.

---

### Canonical Papers (PDF)

- **`The Dynamic Completion of the UNNS Substrate.pdf`**  
  Establishes refinement completion, physical geodesics, and robustness under **decision-level perturbations**.

- **`Ordering Noise and the Universality of Least-Divergence Selection in the UNNS Substrate.pdf`**  
  Introduces **ordering noise (Mode B)** and demonstrates that least-divergence selection is invariant under exploration-history perturbation, including the discrete-cost regime.

  Together, these papers form the formal theoretical backbone of L4.

---

### Summary Document

- **`CHAMBER XXXI v1.0.6 — SUMMARY.md`**

  Concise technical summary of:
  - chamber purpose
  - perturbation axes
  - validation results
  - interpretation scope

  Serves as a quick-reference companion to the full papers.

---

## Scientific Status

This folder establishes that:

- least-divergence selection is **not heuristic**
- it is **not dependent on cost evaluation**
- it is **not dependent on exploration order**
- it persists under controlled attempts at falsification

At this stage, least-divergence selection functions as a **substrate-level necessity**, not a contingent algorithmic outcome.

---

## Position in the UNNS Program

L4 completes the validation arc:

- τ-invariants → dynamic refinement → geodesic selection → inevitability

The UNNS Substrate is now characterized as a **pre-geometric mechanism** that:
- generates constants,
- governs refinement flow,
- and constrains admissible projections (mathematical, geometric, physical).

Subsequent work moves beyond validation toward **mechanism coupling and extension**.

---

## Reproducibility

All results in this folder are:
- deterministic at σ = 0
- seed-controlled for σ > 0
- statistically aggregated
- failure-mode explicit

No narrative assumptions are required to reproduce or audit the findings.

---

## Status

**L4 — Complete**  
This folder is final and canonical.
