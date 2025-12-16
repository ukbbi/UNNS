# UNNS Canonical Repository

This folder contains **canonical UNNS artifacts**: authoritative, theory-anchored, and regression-stable reference materials that define *what counts* as a validated UNNS construction at a given stage of the project.

The `canonical/` directory does **not** replace existing Labs, Chambers, or Explorers.  
Instead, it introduces an **orthogonal reference layer** that designates long-lived, citation-grade instances across the UNNS ecosystem.

---

## Purpose

The UNNS project contains a large and growing collection of experimental Chambers, visualization tools, and exploratory engines distributed across the repository.

The role of `canonical/` is to:

- Preserve **reference-grade executions** of UNNS theory
- Store **validated datasets** used for comparison and regression
- Anchor **interactive Chambers** to their formal mathematical sources
- Provide stable artifacts for citation, teaching, and external review

In short:

> **Labs explore. Canonical instances define.**

---

## What Belongs Here

An artifact may be placed in `canonical/` if it satisfies **all** of the following:

1. **Theory-Anchored**  
   Explicitly tied to a formal UNNS paper or definition (e.g. operadic substrate, τ-filtering, structural recursion).

2. **Operationally Realized**  
   Implemented as an executable Chamber, engine, or computational surface.

3. **Validated**  
   Includes known-good JSON runs, comparison datasets, or reproducibility tests.

4. **Stable by Intent**  
   Not a transient experiment; changes are deliberate, versioned, and documented.

5. **Publicly Referenced**  
   Intended to be linked from unns.tech articles, documentation, or research notes.

---

## What Does *Not* Belong Here

- One-off experiments
- Prototypes without validation
- Early drafts of Chambers
- Historical artifacts kept for archival reasons
- Local or temporary test files

Those remain in their original locations.

---

## Folder Structure Convention

Each canonical item should live in its own subfolder:

```text
canonical/
├── <canonical-name>/
│   ├── README.md        # What this instance is and why it is canonical
│   ├── chamber.html     # Canonical build OR link/wrapper to live chamber
│   ├── data/            # Validated JSON runs and comparison sets
│   ├── theory/          # Referenced papers (PDF or links)
│   └── notes.md         # Optional: interpretation or usage notes
