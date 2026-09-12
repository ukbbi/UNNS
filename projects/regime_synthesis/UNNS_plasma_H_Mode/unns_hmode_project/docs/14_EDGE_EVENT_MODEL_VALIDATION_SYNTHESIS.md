# UNNS-H Mode Project — Edge-Event Model Validation Synthesis

## 1. Purpose

This synthesis records what was gained from validating the first event-level UNNS-H Mode edge-admissibility model.

It should be placed after the validation report:

```
docs/
  13_EDGE_EVENT_MODEL_VALIDATION.md
  14_EDGE_EVENT_MODEL_VALIDATION_SYNTHESIS.md
```

The validation report gives the direct output of the validator.  
This synthesis explains what that result means for the research program.

---

## 2. Model being validated

The validated model is the first event-level precursor of the eventual time-dependent edge margin:

```
m_edge_event = C_edge_capacity - F_route_fragmentation
```

where:

```
F_route_fragmentation =
  S_power_balance
  + S_transport
  + S_timing
```

and:

```
C_edge_capacity =
  S_edge_response
  + density_support_percentile
  + species_position_percentile
  + geometry_stability
```

The model was designed to convert the four empirical branch families observed in the TCV pilot into formal score components:

```
power_balance_branch          → S_power_balance
transport_branch              → S_transport
edge_divertor_response_branch → S_edge_response
timing_branch                 → S_timing
```

The validation question was simple:

> Does this formal model actually separate the reviewed shots into meaningful leakage-like, ambiguous, and edge-response corridors?

---

## 3. Validation result

The validator returned:

```
state_separation: PASS_STRICT_ORDERING
reviewed_shots: 9
ambiguous_shots: 2
mixed_ILH_shots: 1
```

This is the strongest internal validation outcome available in the current validator.

The strict ordering condition means:

```
max(negative leakage margin) < min(boundary ambiguous margin)

and

max(boundary ambiguous margin) < min(positive boundary margin)
```

The measured ranges were:

```
negative_leakage_margin:
  min  = -0.793663
  max  = -0.227105
  mean = -0.457666

boundary_ambiguous_margin:
  min  = -0.073868
  max  =  0.052241
  mean = -0.010813

positive_boundary_margin:
  min  =  0.527590
  max  =  0.793112
  mean =  0.659667
```

The three model states are therefore cleanly separated.

---

## 4. Validated shot corridors

The nine reviewed TCV shots separated as follows.

### 4.1 Negative leakage margin

```
69807
69668
67992
68001
```

These events sit in the negative-margin region.  
Their route-fragmentation pressure exceeds their edge-capacity evidence.

They are dominated by transport, timing, or power-balance fragmentation.

### 4.2 Boundary ambiguous margin

```
69913
68206
```

These events sit close to zero margin.

They are not cleanly leakage-like and not cleanly edge-response-like.  
They are therefore useful boundary cases.

### 4.3 Positive boundary margin

```
66445
69892
68719
```

These events sit in the positive-margin region.

They all belong to the edge-divertor response corridor and are dominated by edge-response capacity.

---

## 5. Main validation table

| SHOT | ILH | m_edge_event | m_edge_state | Formal corridor | Dominant fragmentation | Dominant capacity |
|---:|:---|---:|:---|:---|:---|:---|
| 69807 | 0 | -0.793663 | negative_leakage_margin | mixed_power_transport_timing_leakage_corridor | S_transport | geometry_stability |
| 69668 | 0 | -0.551591 | negative_leakage_margin | transport_timing_corridor | S_transport | geometry_stability |
| 67992 | 1 | -0.258305 | negative_leakage_margin | power_transport_corridor | S_power_balance | geometry_stability |
| 68001 | 1;0 | -0.227105 | negative_leakage_margin | power_transport_corridor | S_power_balance | geometry_stability |
| 69913 | 1 | -0.073868 | boundary_ambiguous_margin | timing_only_or_timing_dominant_corridor | S_timing | geometry_stability |
| 68206 | 1 | 0.052241 | boundary_ambiguous_margin | power_balance_corridor | S_power_balance | density_support_percentile |
| 66445 | 1 | 0.527590 | positive_boundary_margin | edge_divertor_response_corridor | S_timing | S_edge_response |
| 69892 | 1 | 0.658299 | positive_boundary_margin | edge_divertor_response_corridor | S_power_balance | S_edge_response |
| 68719 | 1 | 0.793112 | positive_boundary_margin | edge_divertor_response_corridor | S_power_balance | S_edge_response |

---

## 6. Branch-family result

The branch-family means show the main discovery:

```
timing_branch:
  mean m_edge_event = -0.473041

transport_branch:
  mean m_edge_event = -0.457666

power_balance_branch:
  mean m_edge_event = -0.306708

edge_divertor_response_branch:
  mean m_edge_event = 0.659667
```

This is the decisive validation pattern.

The timing, transport, and power-balance branches occupy the negative side of the margin.  
The edge-divertor response branch occupies the positive side.

Therefore, the edge-divertor branch is not merely another fragment type.  
It behaves as a distinct positive boundary-response corridor in the model.

---

## 7. What the validation establishes

The validation establishes four things inside the current TCV event-level pilot.

### 7.1 The model is not arbitrary

The event-level margin does not collapse into an unordered scatter.  
It separates the nine reviewed shots into three non-overlapping margin classes.

### 7.2 The branch families are meaningful

The four empirical branch families are not only descriptive labels.  
They become formal score components with distinct effects on the event margin.

### 7.3 Edge response is structurally different from leakage pressure

The edge-divertor response corridor separates positively from the power-balance, transport, and timing branches.

This supports the UNNS-H Mode interpretation that boundary response is not simply another instability indicator.  
It may represent the event-level signature of edge-capacity formation.

### 7.4 H-mode access is not reducible to total power alone

The negative and ambiguous corridors include power-balance fragmentation, but the positive corridor is defined by edge-response dominance.

This supports the working view:

> Heating power may push the plasma toward transition, but edge-route organization determines whether the transition becomes structurally admissible.

---

## 8. Physical interpretation

The validated model suggests the following event-level structure.

### 8.1 Leakage-like corridor

Shots in this corridor show high route-fragmentation pressure.

This pressure may arise through:

```
power-balance fragmentation
transport fragmentation
timing-corridor fragmentation
```

In UNNS terms, these events are not simply low-power or failed events.  
They are events where the route structure around transition remains fragmented.

### 8.2 Boundary-ambiguous corridor

Shots in this corridor lie near zero margin.

They are valuable because they may represent the neighborhood of the L-H boundary.  
They should be examined carefully before any stronger claim is made.

### 8.3 Edge-response corridor

Shots in this corridor show strong edge-capacity evidence.

The model associates them with:

```
edge/divertor response dominance
positive m_edge_event
low route-fragmentation pressure
```

This is the closest current event-level analogue of a boundary-preserving H-mode access route.

---

## 9. Relation to the central UNNS-H Mode thesis

The project thesis is:

> H-mode is a boundary-admissibility transition in which the plasma edge reorganizes from a turbulent leakage layer into a route-preserving confinement layer.

The validation does not prove the full thesis.

However, it supports the event-level precursor of that thesis:

> The TCV suspect-shot set separates into leakage-like, boundary-ambiguous, and edge-response corridors when power-balance, transport, timing, and edge/divertor-response structures are modeled as opposing route-fragmentation and edge-capacity terms.

That is a real formal gain.

---

## 10. What this validation does not establish

This validation does not yet prove the physical origin of H-mode.

It does not yet establish the full time-dependent object:

```
m_edge(t)
```

It does not yet include direct time-series diagnostics of:

```
edge turbulence
radial electric field
E×B shear
pedestal gradient evolution
temperature evolution
confinement-time response
ELM timing
H-L back-transition behavior
```

It does not show cross-machine generality.

It does not prove that the same structure will appear in MAST, AUG, DIII-D, JET, WEST, ASDEX Upgrade, or future reactor-scale regimes.

The result is an internally validated TCV event-level pilot model.

---

## 11. Why the result matters

The validation matters because it changes the project status.

Before validation, the model was a plausible construction.

After validation, the model becomes a testable internal result:

```text
The event-level edge-admissibility margin cleanly separates the reviewed TCV shots into three ordered structural states.
```

This justifies moving forward to figure generation and a first technical note, provided the claims remain properly bounded.

---

## 12. Recommended figures

The next presentation layer should include four figures.

### Figure 1 — Margin separation by shot

A bar chart of `m_edge_event` for the nine reviewed shots, ordered from most negative to most positive.

Purpose:

```
show strict ordering visually
```

### Figure 2 — Branch-family mean margins

A bar chart of mean `m_edge_event` by branch family:

```
timing_branch
transport_branch
power_balance_branch
edge_divertor_response_branch
```

Purpose:

```
show that edge-divertor response separates from leakage branches
```

### Figure 3 — Capacity vs fragmentation plane

A scatter plot:

```
x-axis: F_route_fragmentation
y-axis: C_edge_capacity
color/group: m_edge_state
```

Purpose:

```
show the geometric separation of the event-level margin
```

### Figure 4 — Shot corridor taxonomy

A schematic diagram:

```
negative leakage corridor → boundary ambiguous corridor → positive edge-response corridor
```

Purpose:

```
summarize the UNNS interpretation for manuscript or unns.tech
```

---

## 13. Recommended next document

The next technical document should be:

```
15_EVENT_LEVEL_EDGE_MODEL_FIGURE_PLAN.md
```

or, if figures are generated immediately:

```
15_EVENT_LEVEL_EDGE_MODEL_FIGURES.md
```

After figures, the project can move to a first technical note:

```
manuscript/
  hmode_boundary_route_preservation_tcv_pilot.md
```

---

## 14. Current project state

```
project structure                         complete
TCV ingestion                              complete
STRUC-I baseline                           complete
STRUC-PERC-I fragmentation test            complete
fragment-isolate mapping                   complete
suspect-shot review                        complete
event-level edge-admissibility model       complete
model report                               complete
model validation                           complete
validation synthesis                       current document
figures                                    next


---

## 15. Final synthesis statement

The first UNNS-H Mode event-level model has passed internal validation on the reviewed TCV suspect-shot set.

The result is not a proof of H-mode origin, but it is a strong pilot finding:

> The reviewed TCV transition-related shots separate into strictly ordered leakage-like, boundary-ambiguous, and edge-response corridors under the event-level edge-admissibility margin `m_edge_event`.

The most important structural result is:

> power-balance, transport, and timing branches load the negative side of the margin, while the edge-divertor response branch occupies the positive side.

This is the first validated event-level form of the UNNS-H Mode boundary-admissibility hypothesis.
