# Regime Lens — Canonical Notes

This document accompanies the live visualization:

**`regime_lens_v1.2.0_CANONICAL.html`**

It explains *what the Regime Lens is*, *why it exists*, and *how it should be interpreted* within the UNNS τ-Filtered Observability Foundations.

This file is intentionally scoped.
For the full chamber overview, theory, and datasets, see `README.md` in this folder.

---

## What the Regime Lens Is

The **Regime Lens** is a standalone, executable visualization that renders **dynamic regimes** produced by τ-filtered recursion:

- **τ-admissible (stable)**
- **transitional / critical**
- **collapse-dominated (Operator XII)**

It does **not** introduce a new model.
It exposes, in real time, the *same regime logic already defined and computed* by the Foundations Chamber.

In short:

> The Regime Lens is a *view*, not a generator.

---

## What It Visualizes

The lens renders the relationship between:

- **κ (curvature / instability measure)**
- **Λ (τ-admissibility threshold)**
- **regime classification**

Conceptually:

- κ ≤ Λ → τ-admissible evolution  
- κ ≈ Λ → transitional / critical regime  
- κ > Λ → collapse-selected dynamics (XII)

These regimes correspond directly to those described in:

- *UNNS as an ∞-Operadic Substrate* (formal definition)
- τ-Filtered Observability — Foundations Chamber (operational implementation)

---

## Why This Exists as a Separate Module

The Regime Lens is intentionally **decoupled** from:

- the generator
- the JSON import/export logic
- the chamber UI state machine

This separation serves three purposes:

1. **Conceptual clarity**  
   Regimes are presented as first-class observable objects, not as UI side-effects.

2. **Article integration**  
   The lens can be embedded as a *live figure* in public articles via `<iframe>`.

3. **Canonical stability**  
   The file is versioned and frozen (`v1.2.0_CANONICAL`) to ensure reproducibility and long-term reference.

---

## Relationship to the Foundations Chamber

| Foundations Chamber | Regime Lens |
|---------------------|------------|
| Computes κ, Λ, admissibility | Visualizes regime geometry |
| Produces JSON outputs | Requires no data input |
| Multi-tab instrument | Single conceptual lens |
| Analysis & comparison | Interpretive surface |

The Regime Lens **does not replace** any chamber functionality.
It isolates and clarifies one idea:

> *Consistency as a measurable regime, not a binary property.*

---

## Intended Use

The Regime Lens is designed to be used as:

- a **live figure** in unns.tech articles
- a **conceptual bridge** between formal definitions and intuition
- a **didactic tool** for readers unfamiliar with τ-filtering mechanics

It is especially suited for:
- public explanations
- presentations
- theory → visualization transitions

---

## What This File Is Not

- Not a simulator
- Not a data validator
- Not a replacement for the chamber
- Not a source of new metrics

All numerical authority remains with:
- exported JSON runs
- comparison cards
- the Foundations Chamber itself

---

## Canonical Status

- File: `regime_lens_v1.2.0_CANONICAL.html`
- Status: **Frozen**
- Changes require:
  - version bump
  - explicit rationale
  - separate review

This document exists to **anchor interpretation**, not to evolve independently.

---

## See Also

- `README.md` — full Foundations pack overview  
- `COMPARISON_RESULT_CARD.md` — formalized multi-run comparison  
- `UNNS as an ∞-Operadic Substrate.pdf` — theoretical foundation  
- `tau_filtered_observability_lab.html` — operational chamber

---

**UNNS Canonical Materials**  
Dynamic consistency • τ-filtering • collapse-selected recursion
