# 04 — Formal Model Stub

This document defines placeholder notation only. Numerical definitions must be locked after seeing the first real data schema.

## Edge admissibility margin

Let:

- `S(t)` = stabilizing edge-structure term
- `F(t)` = turbulent fragmentation / leakage term
- `G(t)` = pedestal gradient load
- `C(t)` = route coherence / persistence term
- `N(t)` = noise / diagnostic uncertainty term

Initial generic form:

```text
m_edge(t) = normalize[S(t) + C(t) - F(t) - λG(t) - N(t)]
```

Interpretation:

- `m_edge(t) < 0`: L-mode-like leakage / non-admissible boundary.
- `m_edge(t) ≈ 0`: transition/dithering boundary.
- `m_edge(t) > 0`: H-mode-like boundary preservation.
- `m_edge(t) > 0` with high `G(t)`: H-mode but possible ELM overload.

## Boundary overload index

```text
B_overload(t) = normalize[G(t) / max(ε, S(t) + C(t))]
```

Interpretation:

- low overload: stable H-mode
- rising overload: pre-ELM state
- high overload + release marker: ELM event

## Required falsifiability

The model fails if `m_edge(t)` cannot distinguish L-mode from H-mode better than simple raw threshold variables, or if `B_overload(t)` shows no relation to ELM timing.
