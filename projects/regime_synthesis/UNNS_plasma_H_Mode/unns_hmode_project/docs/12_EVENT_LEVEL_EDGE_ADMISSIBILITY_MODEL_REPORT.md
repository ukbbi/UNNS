# UNNS-H Mode Project — Event-Level Edge-Admissibility Model Report

## 1. Purpose

This report records the first formal conversion of the observed TCV branch families into a computable UNNS-H Mode event-level model.





---

## 2. Background

The first TCV pilot produced three layers of evidence:

1. STRUC-I showed that the TCV scalar ladders are broadly admissible.
2. STRUC-PERC-I showed that selected variables fragment into minor or isolated structural branches.
3. The fragment-isolate and suspect-shot reviews localized those branches to a small recurrent shot set.

The key recurrent fragment variables were:

```
P_loss_candidate_MW
chi_eff_candidate
divertor_signal_candidate
event_time
P_total_aux_candidate_MW
P_total_candidate_MW
```

The branch tags condensed into four families:

```
power_balance_branch
transport_branch
edge_divertor_response_branch
timing_branch
```

This report converts those empirical families into a first formal model.

---

## 3. Core empirical branch families

The four observed families are interpreted as follows.

| Empirical branch | Physical reading | UNNS model score |
|---|---|---|
| `power_balance_branch` | fragmentation in loss / total / auxiliary power structure | `S_power_balance` |
| `transport_branch` | fragmentation in effective transport / chi-like response | `S_transport` |
| `edge_divertor_response_branch` | isolated edge/divertor response behavior | `S_edge_response` |
| `timing_branch` | transition-time corridor separation | `S_timing` |

This creates the first bridge from observed chamber output to a formal event-level UNNS-H Mode state variable.

---

## 4. First formal event-level object

The project ultimately aims at a time-dependent edge margin:

```
m_edge(t)
```

However, the current TCV dataset is event-level rather than full time-trace data. Therefore the correct first object is an event-level precursor:

```
m_edge_event
```

The first formal definition is:

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
  + S_density_support
  + S_geometry_support
  + S_species_support
```

This definition intentionally separates two opposing roles.

`F_route_fragmentation` measures leakage pressure, route instability, or fragmented transition access.

`C_edge_capacity` measures evidence that the plasma edge is capable of organizing and sustaining a boundary-response corridor.

---

## 5. Component definitions

### 5.1 Power-balance score

```
S_power_balance
```

This score represents structural pressure arising from fragmentation in:

```
P_loss_candidate_MW
P_total_candidate_MW
P_total_aux_candidate_MW
```

Interpretation:

High `S_power_balance` indicates that the event lies in a fragmented power-balance corridor. This does not mean the shot is wrong or unusable. It means the event does not sit inside a single smooth power-threshold ladder.

### 5.2 Transport score

```
S_transport
```

This score represents structural pressure associated with:

```
chi_eff_candidate
```

Interpretation:

High `S_transport` indicates that the shot belongs to a transport-fragmented branch. In the UNNS-H Mode reading, this is one of the strongest indicators that the transition is not reducible to total heating power alone.

### 5.3 Edge-response score

```
S_edge_response
```

This score represents branch membership associated with:

```
divertor_signal_candidate
```

Interpretation:

High `S_edge_response` is treated as edge-response evidence, not merely as another failure. It may indicate that the event participates in a distinct edge/divertor response corridor.

### 5.4 Timing score

```
S_timing
```

This score represents structural separation in:

```
event_time
```

Interpretation:

High `S_timing` indicates that transition access may occur through separated temporal corridors rather than one universal timing pathway.

---

## 6. Event-level states

The first model assigns three qualitative states:

```
negative leakage margin
boundary ambiguous margin
positive boundary margin
```

These are not final physical classes. They are first-pass UNNS event-level states.

| State | Meaning |
|---|---|
| negative leakage margin | route-fragmentation pressure exceeds edge-capacity evidence |
| boundary ambiguous margin | neither leakage nor edge response dominates strongly |
| positive boundary margin | edge-response / support evidence exceeds fragmentation pressure |

The purpose of these states is not to replace plasma-physics labels, but to introduce a structural layer that can later be compared against L-mode, L-H, H-mode, H-L, and ELM-related windows.

---

## 7. First shot-level separation

The initial event model separates the nine reviewed shots into three provisional corridors:

```
negative leakage margin:
  69807
  69668
  67992
  68001

boundary ambiguous margin:
  69913
  68206

positive boundary margin:
  66445
  69892
  68719
```

This is the first formal outcome of the UNNS-H Mode project.

The separation is physically suggestive because the positive-margin group corresponds to the edge/divertor-response trio, while the negative-margin group contains mixed power-balance, transport, and timing fragmentation.

---

## 8. Core gain

Before this step, the project had a descriptive result:

> There are fragments.

After this step, the project has a computable event-level model:

> There is an event-level edge-admissibility margin separating leakage-like, ambiguous, and edge-response corridors.

The core conversion is:

```
power_balance_branch          → S_power_balance
transport_branch              → S_transport
edge_divertor_response_branch → S_edge_response
timing_branch                 → S_timing
```

and these produce:

```
m_edge_event
formal_corridor
m_edge_state
```

This is the first formal UNNS-H Mode model derived from TCV event data.

---

## 9. What this does not yet prove

This report does not prove the physical origin of H-mode.

It does not prove that any reviewed shot is anomalous, faulty, causal, or uniquely important.

It does not yet establish a time-dependent edge margin.

It does not yet show that the same model works on another machine, such as MAST, AUG, DIII-D, JET, or ITER-relevant projections.

The current model is an event-level formalization of the first TCV pilot signal.

---

## 10. Required next step

The next stage is validation.

The validation question is:

> Does `m_edge_event` genuinely separate the observed shot families in a physically meaningful way, or is it merely re-labeling the same branch tags?

Therefore the next document should be:

```
docs/
  13_EDGE_EVENT_MODEL_VALIDATION.md
```

and the next script should be:

```
components/
  edge_event_model_validator.py
```

The validator should test:

1. whether `m_edge_event` separates the nine reviewed shots into stable ranges;
2. whether power-balance, transport, timing, and edge-divertor branches occupy different score patterns;
3. whether `m_edge_event` distinguishes ILH states or instead identifies branch-specific structure;
4. which score components dominate each corridor;
5. which shots remain ambiguous or inconsistent.

---

## 11. Project status after this report

The project has now moved from empirical reconnaissance to first formal modeling.

Current status:

```
project structure                    done
TCV ingestion                         done
STRUC-I baseline                      done
STRUC-PERC-I fragmentation test       done
fragment-isolate mapping              done
suspect-shot review                   done
event-level edge model                done
model validation                      next
time-series m_edge(t)                 not yet

```

This report should be treated as the formal bridge between the pilot analysis and the validation phase.
