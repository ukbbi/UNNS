# 🚀 Voyager 1 MAG — Realizability Trajectory (Post-Crossing Corpus)

Structural Phase Transitions Along Physical Trajectories  
UNNS Substrate Research Programme

---

## Overview

This folder contains the **Voyager 1 MAG corpus and its structural analysis** within the UNNS Substrate framework.

The dataset provides the **first post-boundary realization** of a physical trajectory in the admissibility manifold M_adm, enabling:

- detection of a realizability boundary crossing  
- reconstruction of post-crossing basin structure  
- validation of dynamic phase transition theorems  

Unlike Voyager 2 (pre-crossing only), Voyager 1 supplies:

→ crossing + post-crossing stabilization in a single trajectory  

---

## Scientific Role

According to the manuscript :contentReference[oaicite:1]{index=1}:

- Voyager 2 establishes **boundary approach**
- Voyager 1 establishes **boundary crossing and basin separation**

Together they form:

→ a **two-trajectory structural tomography of the heliopause**

---

## Corpus Definition

Source observable:

|B| = √(B₁² + B₂² + B₃²)

Data:

- Voyager 1 MAG (48s resolution)
- Years: 2011–2017
- Windows: 500 per year
- Total runs: 3,500 STRUC-PERC-I evaluations

Pipeline:

DLCP → Ladder construction → STRUC-PERC-I evaluation → Structural trajectory γ(t)

---

## Structural Coordinates

Each epoch is mapped into M_adm via:

- κ_conn (connectivity coordinate)
- tailDom (tail dominance)
- GR (giant ratio)
- E (excursion density)

These define the trajectory:

γ(t) ∈ M_adm

---

## Core Result

The trajectory exhibits a **realizability boundary crossing** at:

t* = 2012

This is obtained purely structurally via:

t* = argmin κ_conn(t)

and matches the physical heliopause crossing.

---

## Boundary Signature Triplet

The Voyager 1 trajectory satisfies the full diagnostic structure:

1. **Critical point**
   - κ_conn has a unique minimum at 2012

2. **Excursion clustering**
   - GIANT / TAIL / HARD regimes concentrate in 2011–2012

3. **Post-boundary basin separation**
   - κ_conn jumps and stabilizes in a disjoint range after 2012

This triplet is the **minimal structural indicator of a phase transition**.

---

## Structural Phases

### Pre-crossing (Heliosheath)

- Years: 2011–2012  
- κ_conn: ~14k–18k  
- Regime: FULL + excursions  
- tailDom: ~0.776–0.781  

Interpretation:

→ boundary approach zone  

---

### Crossing (Transition Layer)

- Centered at: 2012  
- κ_conn minimum  
- Peak excursion density  

Interpretation:

→ finite-thickness transition layer (not a point)  

---

### Post-crossing (ISM Basin)

- Years: 2013–2017  
- κ_conn: ~27k–36k  
- Regime: ~100% FULL  
- tailDom: ~0.93–0.95  
- Excursions: collapse to ~0  

Interpretation:

→ distinct structural basin  

---

## Basin Separation

Pre- and post-crossing coordinate ranges are disjoint:

K_pre ∩ K_post = ∅

This establishes:

→ heliosphere ≠ ISM continuation  
→ they are separate structural basins in M_adm  

---

## Structural Diagnostics (Quantitative)

From the corpus:

- Jump ratio: κ_post / κ_min ≈ 2.1  
- Tail amplification: ≈ +22%  
- Boundary sharpness: +111% in one step  
- Excursion collapse: E(t > t*) = 0  
- Transition thickness: ~1–2 years  

These convert the transition into a **measurable object**.

---

## Geometric Interpretation

The trajectory allows reconstruction of local boundary geometry:

- Curvature proxy: K ≈ 1.163  
- Metric crossing length: ds ≈ 1.42  
- Strong directional asymmetry  

Implication:

→ realizability boundaries are **curved, finite, asymmetric objects** in M_adm  

---

## File Structure

rt_voyager1/

- Voyager 1 MAG → DLCP Multi-Scale Structural Pipeline/  
- Voyager 1 MAG → UNNS Ladder Pipeline.md  
- voyager1_mag_ladder_pipeline.py  

- STRUC-PERC-I v2.5 README  
- struc_perc_i_v2_5_0.html  

- voyager1_struc_perc_analysis.html  
- voyager1_article.html  

- Structural Phase Transitions Along Physical Trajectories.pdf  

- image1p.png  
- image2ap.png  
- image2bp.png  
- image3p.png  

---

## Pipeline

1. Extract |B| from MAG data  
2. Apply DLCP windowing  
3. Construct ladders  
4. Evaluate via STRUC-PERC-I  
5. Aggregate annual structural coordinates  
6. Detect boundary via κ_conn minimum  

---

## Interpretation Within UNNS

This dataset establishes:

- dynamic realizability geometry  
- structural phase transitions along real trajectories  
- basin decomposition inside a single class (FULL)  

It upgrades the framework from:

→ classification  

to:

→ **phase space geometry with detectable transitions**

---

## Cross-Domain Significance

The same boundary signature appears in:

- heliospheric data (this corpus)  
- atomic spectral deformation  
- cosmological κ_conn sweeps  

Implication:

→ realizability boundaries are **cross-domain structural objects**, not domain-specific artifacts  

---

## Constraints and Scope

- Single observable: magnetic field magnitude  
- Single confirmed boundary (heliopause)  
- Coordinate values are chart-dependent  
- Global geometry of M_adm remains open  

---

## Status

- DLCP pipeline: implemented  
- STRUC-PERC analysis: complete  
- Boundary detected: 2012  
- Basin separation: confirmed  
- Manuscript: complete  

---

## Summary

Voyager 1 demonstrates that:

→ a physical boundary crossing manifests as a **structural phase transition**

characterized by:

- connectivity minimum  
- excursion clustering  
- basin separation  

and that:

→ realizability boundaries can be detected **without physical models**, using structure alone