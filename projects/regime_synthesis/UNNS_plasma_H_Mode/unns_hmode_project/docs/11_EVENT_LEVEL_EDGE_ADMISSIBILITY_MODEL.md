# 11 — Event-Level Edge-Admissibility Model v0.1

## UNNS-H Mode Project

This document converts the four observed branch families from the TCV L-H pilot into the first formal UNNS-H Mode model.

It defines an event-level precursor:

```text
m_edge_event
```

This is not yet the full time-dependent margin:

```text
m_edge(t)
```

The current dataset is event-level, not full discharge time-series data. Therefore the model below formalizes how the observed branch families can be converted into a computable event-level edge-admissibility score.

---

## 1. Empirical basis

The two-chamber pilot produced three linked findings.

First, STRUC-I showed that the TCV scalar ladders are broadly admissible: their ordered scalar variables preserve structure under perturbation.

Second, STRUC-PERC-I showed selective hard fragmentation in variables tied to power balance, transport, timing, and edge/divertor response.

Third, fragment-isolate mapping and suspect-shot review localized the recurrent branch structure to nine shots:

```text
69807, 68001, 69668, 69892, 66445, 68719, 69913, 67992, 68206
```

The observed fragment families were:

```text
power_balance_branch
transport_branch
edge_divertor_response_branch
timing_branch
```

The event-level model below treats these as the first empirical coordinates of an H-mode edge-admissibility space.

---

## 2. Core interpretation

The working UNNS-H Mode hypothesis is:

> H-mode access is not a single total-power threshold. It is a boundary-admissibility transition in which power input, transport suppression, timing, density, species composition, geometry, and edge response must enter a compatible route-preserving configuration.

The four observed branch families are interpreted as follows.

| Branch family | Physical locus | UNNS interpretation |
|---|---|---|
| `power_balance_branch` | total power, loss power, auxiliary power | route load / power-balance pressure |
| `transport_branch` | effective transport / `chi_eff_candidate` | turbulent leakage or transport fragmentation |
| `edge_divertor_response_branch` | divertor/edge signal | boundary-response capacity |
| `timing_branch` | event-time branch separation | transition corridor timing / route sequencing |

---

## 3. Event branch vector

For each reviewed event or shot aggregate, define the branch vector:

```text
β_event = (B_P, B_χ, B_D, B_τ)
```

where:

```text
B_P = 1 if the event belongs to power_balance_branch, else 0
B_χ = 1 if the event belongs to transport_branch, else 0
B_D = 1 if the event belongs to edge_divertor_response_branch, else 0
B_τ = 1 if the event belongs to timing_branch, else 0
```

The symbols mean:

```text
P  = power balance
χ  = effective transport
D  = divertor / edge response
τ  = event timing
```

---

## 4. Scalar evidence functions

Branch membership is not enough. Each branch also carries scalar intensity.

Let `rank_x(v)` be the percentile rank of value `v` in the full canonical TCV event table.

Then define:

```text
L_P = max(rank(P_loss), rank(P_total), rank(P_total_aux))
L_χ = rank(chi_eff)
L_D = mean(rank(divertor_signal), rank(divertor_signal_150))
L_n = rank(n_e)
L_s = mean(rank(hydrogen_fraction), rank(helium_fraction))
```

For geometry, define a stability factor:

```text
G = 1 - mean(clipped robust deviation of q95, κ, δ, B_t)
```

where:

```text
G ≈ 1  means geometrically ordinary / stable
G ≈ 0  means geometrically displaced / unusual
```

For timing, define:

```text
L_τ = normalized event-time span among reviewed shots
```

This is an event-level proxy. In the later time-series model it should be replaced by a true transition-time functional.

---

## 5. Branch evidence scores

The four branch scores combine chamber-derived branch membership with scalar intensity.

```text
S_P = 0.65 B_P + 0.35 L_P
S_χ = 0.70 B_χ + 0.30 L_χ
S_D = 0.65 B_D + 0.35 L_D
S_τ = 0.70 B_τ + 0.30 L_τ
```

Interpretation:

```text
S_P = power-balance pressure
S_χ = transport fragmentation pressure
S_D = edge-response capacity evidence
S_τ = timing-corridor pressure
```

The branch flags receive more weight than raw scalar rank because the flags were produced by the chamber/fragment mapping pipeline. Scalar ranks refine intensity but do not replace structural evidence.

---

## 6. Route-fragmentation pressure

Define event-level route-fragmentation pressure:

```text
F_route = 0.35 S_P + 0.35 S_χ + 0.30 S_τ
```

This measures the degree to which the event is dominated by power-balance load, transport fragmentation, and timing separation.

A high `F_route` means the event is structurally closer to leakage, fragmented access, or failed boundary-route formation.

---

## 7. Edge-response capacity

Define event-level edge capacity:

```text
C_edge = 0.45 S_D + 0.25 L_n + 0.15 G + 0.15 L_s
```

This measures whether the event has observable boundary-response support.

The terms mean:

```text
S_D = edge/divertor response evidence
L_n = density support
G   = geometry stability
L_s = species-position support
```

A high `C_edge` means the event has stronger signs of edge/boundary organization.

---

## 8. Event-level edge-admissibility margin

The first formal UNNS-H Mode event-level margin is:

```text
m_edge_event = C_edge - F_route
```

Interpretation:

```text
m_edge_event > 0      boundary response exceeds route-fragmentation pressure
m_edge_event ≈ 0      ambiguous boundary state
m_edge_event < 0      route fragmentation exceeds boundary response
```

Classification used in v0.1:

```text
m_edge_event ≥  0.20  positive_boundary_margin
-0.20 < m_edge_event < 0.20  boundary_ambiguous_margin
m_edge_event ≤ -0.20  negative_leakage_margin
```

---

## 9. Formal corridors

The model produces formal corridors from the branch scores.

| Formal corridor | Rule-level meaning |
|---|---|
| `mixed_power_transport_timing_leakage_corridor` | power, transport, and timing all active; likely leakage/failed boundary-route candidate |
| `power_transport_corridor` | power balance and transport active; power-loaded access/departure branch |
| `transport_timing_corridor` | transport and timing active; low-density/non-LH leakage sibling |
| `edge_divertor_response_corridor` | edge/divertor response dominates; candidate boundary-response corridor |
| `timing_only_or_timing_dominant_corridor` | timing branch active without dominant power/transport branch |
| `power_balance_corridor` | power branch active but transport/timing weaker |

---

## 10. v0.1 scored result on the nine reviewed shots

The model produces the following event-level ordering.

| SHOT | Formal corridor | m_edge_event | State |
|---:|---|---:|---|
| 69807 | mixed_power_transport_timing_leakage_corridor | -0.794 | negative_leakage_margin |
| 69668 | transport_timing_corridor | -0.552 | negative_leakage_margin |
| 67992 | power_transport_corridor | -0.258 | negative_leakage_margin |
| 68001 | power_transport_corridor | -0.227 | negative_leakage_margin |
| 69913 | timing_only_or_timing_dominant_corridor | -0.074 | boundary_ambiguous_margin |
| 68206 | power_balance_corridor | 0.052 | boundary_ambiguous_margin |
| 66445 | edge_divertor_response_corridor | 0.528 | positive_boundary_margin |
| 69892 | edge_divertor_response_corridor | 0.658 | positive_boundary_margin |
| 68719 | edge_divertor_response_corridor | 0.793 | positive_boundary_margin |

This gives the first formal separation:

```text
negative margin: power/transport/timing leakage corridors
positive margin: edge-divertor response corridor
ambiguous margin: timing-only or power-only intermediate cases
```

---

## 11. First UNNS-H Mode claim enabled by the model

The formal v0.1 model supports the following restricted claim:

> In the TCV event-level pilot, the branch families separate into route-fragmentation-dominated and edge-response-dominated corridors. The strongest leakage-like cases are not merely high-power cases; they combine transport and timing fragmentation with weak edge response. Conversely, the edge-divertor trio forms a positive-margin boundary-response corridor.

This is not yet the physical origin of H-mode. It is the first formal bridge toward it.

---

## 12. Falsifiable next tests

The model makes several testable predictions.

### Test 1 — Branch separation

The four branch families should occupy separable regions in the score space:

```text
(S_P, S_χ, S_D, S_τ)
```

### Test 2 — Edge-response separation

Events in the edge-divertor response corridor should have higher `m_edge_event` than mixed power/transport/timing leakage events.

### Test 3 — L-H access refinement

For true L-H access events, successful transitions should tend toward higher `C_edge` relative to `F_route`.

### Test 4 — Time-series upgrade

When full time traces are available, `m_edge(t)` should rise before or at L-H transition and should weaken before H-L return or ELM-like boundary relaxation.

---

## 13. What this model is not

This model is not:

```text
a proof of H-mode origin
a fusion power prediction
a replacement for plasma transport theory
a complete pedestal model
a full MHD stability model
```

It is:

```text
a formal event-level UNNS bridge from observed branch families to an edge-admissibility margin.
```

---

## 14. Required next development

The next development is to move from event-level data to time-series data.

The replacement object should be:

```text
m_edge(t)
```

with components such as:

```text
heating power history
density evolution
temperature evolution
edge pressure gradient
turbulence intensity
radial electric field / E×B shear
stored energy response
Dα or divertor signal evolution
ELM timing
H-L back-transition timing
```

Until those are available, `m_edge_event` should be treated as the correct pilot-level formalization, not the final H-mode model.
