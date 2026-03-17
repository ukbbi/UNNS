# UNNS — κ₀–κ₁ Chambers  
**Selection, Saturation, and Conditional Symmetry Emergence**

This folder contains the canonical experimental and analytical artifacts for the **κ-layer** of the UNNS (Unbounded Nested Number Sequences) substrate, focusing on **post-τ selection** and **conditional symmetry emergence**.

The κ-layer addresses a precise question:

> Given multiple τ-stable outcomes, *which* stable state becomes selected, and *why*?

Unlike τ (stability) or Ω (observable projection), κ operators are **pure selectors**: they do not modify dynamics, generate structure, or project observables. They operate strictly on already τ-stable ensembles.

---

## Conceptual Overview

The κ pipeline establishes three results:

1. **κ₀ — Selection Saturation**  
   τ-relaxed systems generically admit multiple stable outcomes.  
   Increasing numerical precision does **not** collapse this multiplicity.

2. **κ₁ — Symmetry as a Measured Discriminator**  
   Symmetry is evaluated *after* τ-closure.  
   Some symmetry axes discriminate between stable states; others are empirically null.

3. **κ₁′ — Conditional Symmetry Emergence**  
   Deterministic selection is restored by conditioning κ₁ on **active symmetry axes only**, without altering τ-dynamics.

This demonstrates that symmetry emergence is **conditional**, not automatic.

---

## Folder Contents

### HTML Chambers (Interactive / Canonical)

- **`chamber_kappa_zero.html`**  
  κ₀ chamber: selection saturation in τ-relaxed systems.  
  Demonstrates multiplicity persistence under precision refinement.

- **`chamber_kappa_zero_article_4.html`**  
  Article-form presentation of κ₀ results (unns.tech–ready).

- **`chamber_kappa1_1.html`**  
  κ₁ chamber: symmetry-based selection analysis on τ-stable ensembles.

- **`kappa_series_article.html`**  
  Unified κ-series article (κ₀ → κ₁ → κ₁′), formatted for unns.tech publication.

- **`kappa_series_lab.html`**  
  Lightweight lab / validation view for κ-series experiments.

---

### Papers (PDF)

- **`Selection Saturation in τ-Relaxed Dynamical Systems — Chamber κ₀.pdf`**  
  Formal report on selection saturation and multiplicity persistence.

- **`Conditional Symmetry Emergence in τ-Relaxed Systems.pdf`**  
  Extended paper introducing κ₁ and κ₁′, including methods, data analysis,
  negative controls, and discussion contrasting symmetry-breaking narratives.

---

## Operator Roles (Summary)

| Operator | Role | Acts On | Modifies Dynamics |
|--------|------|--------|------------------|
| Φ | Generability | Rules | No |
| Ψ | Consistency | Structures | No |
| τ | Stability | Dynamics | Yes |
| κ₀ | Multiplicity detection | τ-stable ensemble | No |
| κ₁ | Symmetry diagnostics | τ-stable ensemble | No |
| κ₁′ | Conditional selection | τ-stable ensemble | No |
| Ω | Observable projection | Selected state | Yes |

---

## Reproducibility Notes

- All κ₀–κ₁ results are derived from **deterministic τ-dynamics**.
- Ensembles differ only by initial conditions (seeds).
- κ operators do **not** re-run τ or modify state configurations.
- Symmetry axes are evaluated directly on exported τ-stable configurations.
- κ₁′ performs axis filtering based on measured variance, degeneracy, and gap criteria.

No post hoc filtering or adaptive tuning was applied.

---

## Status

- **κ₀:** Complete, validated, publication-grade  
- **κ₁:** Complete, diagnostic by design  
- **κ₁′:** Complete, conditioned selector (canonical refinement)

This folder represents the **final, stable reference** for κ-layer behavior in the UNNS substrate.

---

## Relation to the UNNS Roadmap

The κ-layer provides the missing link between:

- τ-based stability (Chambers XII, XIV, XXX),
- and Ω-based observable projection (later physics-facing layers).

It establishes selection as a **structural phenomenon**, not a dynamical artifact.

---

*UNNS Project — Canonical Research Artifacts*  
