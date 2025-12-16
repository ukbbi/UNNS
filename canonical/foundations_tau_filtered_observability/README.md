# Foundations of τ-Filtered Observability — Canonical Instance

This folder contains the **canonical reference implementation** of the  
**UNNS τ-Filtered Observability Foundations Chamber**.

It anchors an interactive computational surface to its formal mathematical source,
providing validated executions, comparison datasets, and reproducible artifacts
suitable for citation, regression testing, and external analysis.

---

## Canonical Scope

This canonical instance corresponds to the formal paper:

**UNNS as an ∞-Operadic Substrate**  
(`UNNS as an ∞-Operadic Substrate.pdf`)

and its executable realization:

**τ-Filtered Observability — Foundations Chamber**  
(`tau_filtered_observability_lab.html`)

Together, they define a stable reference for:

- τ-coherence as an operadic admissibility criterion
- collapse-selected recursion (Operator XII)
- discrete curvature–based filtering
- observability-restricted dynamics
- multi-run structural comparison

This folder does **not** represent an experiment in progress.
It represents a **validated reference state** of the theory–implementation pair.

---

## Contents

### Formal Reference

- **UNNS as an ∞-Operadic Substrate.pdf**  
  The formal mathematical framework defining UNNS as an ∞-operadic system,
  including τ-filtered sub-categories, collapse selection, and operadic coherence.

### Canonical Chamber

- **tau_filtered_observability_lab.html**  
  A self-contained, browser-executable Foundations Chamber implementing:
  - deterministic state generation
  - Sobtra threshold projection
  - discrete curvature computation
  - τ-admissibility classification
  - collapse labeling (Operator XII)
  - phase-space diagnostics
  - multi-run structural comparison

This file is considered the **canonical executable surface** for the paper.

---

## Validated Test Data

The following JSON files are **schema-conformant** and confirmed to import,
execute, and compare correctly within the Chamber:

- **test_run_valid.json**  
  Single validated run with standard parameters

- **test_run_comparison.json**  
  Baseline multi-run comparison set

- **test_run_high_lambda.json**  
  High-Λ regime emphasizing τ-stability

- **test_run_low_lambda.json**  
  Low-Λ regime emphasizing collapse onset

- **test_run_mixed_operators.json**  
  Operator diversity stress test

- **test_run_varied_params.json**  
  Cross-parameter structural comparison

These files serve three purposes:
1. regression testing
2. example inputs for new users
3. reference datasets for analytical discussion

---

## Reproducibility Guarantees

All runs in this folder satisfy:

- deterministic seeding
- explicit configuration blocks
- complete operator labeling
- explicit admissibility masks
- stable schema versioning

Any future change to the Chamber that breaks compatibility with these files
constitutes a **breaking change** and must be versioned explicitly.

---

## Intended Use

This canonical instance is intended for:

- readers of the paper seeking an executable counterpart
- validation of τ-filtered observability claims
- demonstration of collapse-selected dynamics
- teaching and guided exploration
- regression and comparison against future Chambers

It is **not** intended as:
- a sandbox for experimentation
- a prototype playground
- a mutable development artifact

---

## Relationship to the Broader UNNS Repository

- Other UNNS Chambers remain distributed across the repository
- This folder does not relocate or replace them
- Instead, it designates a **reference anchor** within that ecosystem

The presence of this folder introduces a canonical layer
without imposing structural reorganization elsewhere.

---

## Status

**Canonical — Active**

This instance may be extended by:
- adding new validated comparison datasets
- appending interpretive notes
- referencing follow-up theoretical work

The core artifacts listed above define the reference baseline.
