# Chamber XXX — Conservation Testing

**Discrete Divergence & Structural Flux Analysis**

This chamber implements and validates the conservation test for τ-closure
as defined in:

> *Discrete Divergence, Structural Flux, and the Conservation of τ-Closure*

---

## Purpose

Chamber XXX tests whether **τ-closure implies a conservation principle**
on refinement evolution.

The answer is **no**.

τ-closure is a classification invariant (survival under collapse),
not a conserved quantity.

---

## What This Chamber Does

- Builds refinement graphs from mechanism traces
- Assigns **non-numerical structural flux** (e.g. Z[O,R,P])
- Computes **discrete divergence** at each structural state
- Detects minimal **cycle-with-leak falsifiers**
- Separates closure classification from conservation testing

---

## Validated Mechanisms

| Mechanism | Closure | Conservation | Witness |
|---------|--------|--------------|---------|
| A_pure_cycle | Proto-closed | Holds | None |
| M_leak | Proto-closed | **Falsified** | Cycle-with-leak |
| M_collapse | Collapse | N/A | None |
| C_balanced_leak | Proto-closed | Holds | None |
| B_expansion | Collapse | N/A | None |

---

## Key Result

> **τ-closure survives collapse, but it does not flow.**  
> Conservation is a stricter property that must be earned — not assumed.

This result is empirically validated using a minimal structural falsifier.

---

## Artifacts

Each mechanism includes a complete evidence bundle:

- `*_trace.json` — refinement trace
- `*_graph.json` — refinement graph
- `*_divergence.json` — discrete divergence report
- `*_witnesses.json` — falsifier detection
- `*_complete_bundle.json` — full packaged evidence

---

## Status

- Theory: **Complete**
- Instrument: **Validated**
- Next steps: visualization & carrier exploration

---

UNNS Research Collective
