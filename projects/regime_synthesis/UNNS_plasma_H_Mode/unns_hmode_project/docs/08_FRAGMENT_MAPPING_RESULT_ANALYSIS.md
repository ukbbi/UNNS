# UNNS-H Mode Project — Fragment-Isolate Mapping Result Analysis

**Recommended location:** `unns_hmode_project/docs/08_FRAGMENT_MAPPING_RESULT_ANALYSIS.md`  
**Source artifact analyzed:** `outputs/reports/tcv_suspect_transition_families.csv`  
**Context:** TCV L-H transition database, after STRUC-I and STRUC-PERC-I two-chamber screening.

---

## 1. Executive conclusion

The fragment-isolate mapping step converted the previous chamber-level statement — “some TCV L-H variables fragment” — into a **row/shot-localized branch inventory**.

The new result does not merely repeat that certain variables hard-fragmented. It identifies the **candidate shots and small branch components** that sit at the edges of those fragmenting variables. The strongest gain is that the fragmentation is now localized into a small set of recurrent shots, rather than being spread uniformly across the corpus.

The central result is:

> The TCV L-H transition corpus remains globally coherent, but the fragmentation localizes around small, recurrent branch families in power balance, transport response, divertor/edge response, and event timing.

This strengthens the UNNS interpretation that H-mode access is unlikely to be explained by total heating power alone. The mapped branches point instead toward a multi-coordinate transition condition involving **power balance + transport response + edge/divertor response + timing corridor**.

---

## 2. Dataset basis

The original ingested TCV event table contains:

| Quantity | Value |
| --- | --- |
| Rows | 92 |
| Columns | 79 |
| Unique shots | 66 |
| Shot range | 66444–73917 |
| Years | 2020, 2021, 2022 |
| ILH=1 entries | 84 |
| ILH=0 entries | 8 |

This is the same basis used for the earlier two-chamber run.

---

## 3. Prior chamber context

### 3.1 STRUC-I baseline

STRUC-I established that the scalar TCV ladders are broadly admissible under perturbation. The run was dominated by **Geometric Persistence** with mostly **Stable Structure** states. The weak-persistence signals were concentrated around variables such as `event_time`, `helium_fraction_candidate`, and in the L-H-only subset also `n_Ryter`.

| STRUC-I category | Count |
| --- | --- |
| Weak Persistence | 6 |
| Stable Structure | 42 |

This means the mapped fragmentation should not be read as wholesale collapse. The corpus first passed an admissibility baseline.

### 3.2 STRUC-PERC-I branch context

STRUC-PERC-I then revealed selective fragmentation:

| Subset | FULL_PERCOLATION | HARD_FRAGMENTATION | Hard-fragmenting variables |
| --- | --- | --- | --- |
| All events | 20 | 4 | chi_eff_candidate, divertor_signal_candidate, P_total_aux_candidate_MW, P_total_candidate_MW |
| L-H-only | 19 | 5 | chi_eff_candidate, event_time, P_loss_candidate_MW, P_total_aux_candidate_MW, P_total_candidate_MW |

This is the reason the mapper was needed: STRUC-PERC-I showed which scalar variables fragmented, but not yet which shots or branch rows were responsible.

---

## 4. What the new mapper result contains

The mapper produced **21 suspect branch records**.

| Subset | Mapped branch records |
| --- | --- |
| all_events | 13 |
| lh_only | 8 |

The mapped records separate into two structural roles:

| Component role | Count |
| --- | --- |
| singleton_isolate | 13 |
| minor_component | 8 |

Interpretation:

- **singleton_isolate** means a one-gap branch detached from the giant component under the mapper reconstruction;
- **minor_component** means a small but multi-gap branch detached from the giant component;
- both are useful because they identify the local places where the scalar ladder ceases to behave as one connected family.

The mapped variables are:

| Subset | Variable | Mapped records |
| --- | --- | --- |
| all_events | P_loss_candidate_MW | 2 |
| all_events | P_total_aux_candidate_MW | 1 |
| all_events | P_total_candidate_MW | 1 |
| all_events | chi_eff_candidate | 2 |
| all_events | divertor_signal_candidate | 4 |
| all_events | event_time | 3 |
| lh_only | P_loss_candidate_MW | 2 |
| lh_only | divertor_signal_candidate | 4 |
| lh_only | event_time | 2 |

---

## 5. Most recurrent suspect shots

The most important new information is the recurrence of particular shots across mapped branch records.

| SHOT | Branch mentions | Variables involved | Subsets |
| --- | --- | --- | --- |
| 69807 | 5 | event_time(2); P_loss_candidate_MW(1); P_total_aux_candidate_MW(1); chi_eff_candidate(1) | all_events(5) |
| 68001 | 4 | P_loss_candidate_MW(1); P_total_aux_candidate_MW(1); P_total_candidate_MW(1); chi_eff_candidate(1) | all_events(4) |
| 69668 | 4 | chi_eff_candidate(2); event_time(2) | all_events(4) |
| 69892 | 4 | divertor_signal_candidate(4) | all_events(2); lh_only(2) |
| 66445 | 4 | divertor_signal_candidate(4) | all_events(2); lh_only(2) |
| 68719 | 4 | divertor_signal_candidate(4) | all_events(2); lh_only(2) |
| 69913 | 4 | event_time(4) | all_events(2); lh_only(2) |
| 67992 | 3 | P_loss_candidate_MW(2); chi_eff_candidate(1) | all_events(2); lh_only(1) |
| 68206 | 3 | P_loss_candidate_MW(3) | all_events(2); lh_only(1) |
| 68207 | 2 | P_loss_candidate_MW(1); divertor_signal_candidate(1) | all_events(2) |
| 68000 | 2 | divertor_signal_candidate(2) | all_events(1); lh_only(1) |
| 68003 | 2 | divertor_signal_candidate(2) | all_events(1); lh_only(1) |
| 67990 | 2 | divertor_signal_candidate(2) | all_events(1); lh_only(1) |
| 68632 | 2 | divertor_signal_candidate(2) | all_events(1); lh_only(1) |
| 68006 | 2 | divertor_signal_candidate(2) | all_events(1); lh_only(1) |

These recurrent shots are now candidate **transition-family shots**. They are not automatically “bad data” or failed events. They are the rows most repeatedly adjacent to isolated branches in the variables that matter for H-mode access.

The strongest recurrence pattern is:

- `69807` appears in five branch records, primarily around power loss, auxiliary total power, transport proxy, and event-time branches.
- `68001` appears in four all-events branch records, around power balance and transport proxy variables.
- `69668` appears in four all-events branch records, concentrated in transport and timing branches.
- `69892`, `66445`, and `68719` appear repeatedly in divertor/edge-response branches.
- `69913` appears repeatedly in event-time branches.

This is the first localization of the H-mode branch problem from “variable-level fragmentation” to **specific shot families**.

---

## 6. Branch-family interpretation

| Branch family | Variables | Main recurrent shots | UNNS reading |
| --- | --- | --- | --- |
| Power-balance / loss | P_total_candidate_MW, P_total_aux_candidate_MW, P_loss_candidate_MW | 68001, 69807, 67992, 68206, 68207, 68002, 68200, 68422 | Separates heating/loss pathways rather than the clean L-H threshold scalar alone. |
| Transport proxy | chi_eff_candidate | 67992, 68001, 69668, 69807 | Points to transport-response branching, not only input-power branching. |
| Divertor / edge response | divertor_signal_candidate | 69892, 66445, 68719, 68000, 68003, 68632, 68006, 67990, 68728 | Localizes the edge/divertor-response branch; this is directly relevant to boundary-route preservation. |
| Transition timing | event_time | 69807, 69668, 69913, 67986, 66452 | Shows that L-H access timing is not a single smooth corridor in the mapped branches. |

### 6.1 Power-balance / loss family

The power-family branches are important because the earlier chamber result showed a contrast between `P_LH_candidate_MW` and broader total-power variables. The L-H threshold candidate percolated, while total and auxiliary power variables fragmented in STRUC-PERC-I.

The mapper now localizes parts of this split to shots such as `68001`, `69807`, `67992`, and `68206`.

UNNS reading:

> H-mode access is not encoded by raw total power alone. The transition appears to depend on how power enters the admissible boundary configuration.

### 6.2 Transport-response family

`chi_eff_candidate` maps to recurrent branches involving `67992`, `68001`, `69668`, and `69807`.

UNNS reading:

> The fragmentation is partly transport-structural. H-mode origin should be sought in transport-route reorganization, not only in scalar heating level.

### 6.3 Divertor / edge-response family

The divertor branch is one of the most physically interesting because H-mode is an edge transition. Recurrent shots include `69892`, `66445`, `68719`, `68000`, `68003`, `68632`, and `68006`.

UNNS reading:

> The edge/divertor signal behaves like a boundary-response family. This is directly aligned with the hypothesis that H-mode is a boundary-route preservation transition.

### 6.4 Timing family

The timing branch involves `69807`, `69668`, `69913`, `67986`, and `66452`.

UNNS reading:

> L-H transition timing is not a single smooth corridor. It may separate into multiple temporal access branches.

This matters because STRUC-I had already marked `event_time` as one of the weaker persistence variables, and STRUC-PERC-I later showed L-H-only timing fragmentation.

---

## 7. What the new result adds to the research program

Before this step, the project had:

1. an ingested TCV event dataset;
2. an admissibility baseline from STRUC-I;
3. a percolation/fragmentation screen from STRUC-PERC-I.

After this step, the project now has:

1. a **branch inventory**;
2. a **shot recurrence list**;
3. a first set of **candidate transition families**;
4. a concrete path toward physical interpretation.

The new result therefore moves the project from:

> “Which variables fragment?”

into:

> “Which actual TCV shots sit on those fragmenting branches, and what physical regime do they represent?”

That is the necessary bridge from chamber diagnostics to plasma interpretation.

---

## 8. Scientific interpretation

The mapped fragments concentrate in variables associated with:

- power balance;
- power loss;
- transport response;
- event timing;
- divertor / edge response.

They do not primarily concentrate in static geometry variables such as `R_geo_m`, `minor_radius_m`, `q95`, `kappa`, or `B_t_T`.

This supports a restrained but meaningful claim:

> The H-mode transition signal in this TCV subset appears branch-sensitive in the dynamical and boundary-response variables, rather than simply in static machine geometry.

This is precisely where the physical origin of H-mode should be searched: in the edge transport and power-balance reorganization that turns a turbulent leakage regime into a high-confinement boundary regime.

---

## 9. Important limitations and technical cautions

### 9.1 The mapper output is a localization tool, not a final verdict engine

The mapper identifies isolated and minor gap components from the canonical event table. It should not be treated as a replacement for STRUC-I or STRUC-PERC-I.

### 9.2 Chamber verdict metadata was not fully attached inside the mapping CSV

The column `chamber_verdict` appears as `NOT_PROVIDED`, and chamber-level fields such as `chamber_giantRatio`, `chamber_isolated`, and `chamber_isolatedFraction` are empty in this mapping output. This likely means the mapper did not successfully join the STRUC-PERC JSON metadata by filename/variable name.

This does not invalidate the branch localization, but it means the next version of the mapper should patch metadata joining so each mapped record carries the original STRUC-PERC verdict.

### 9.3 All records are marked LOW priority

Every mapped record currently has `mapping_priority = LOW`. This appears to be conservative scoring, not evidence that the result is unimportant. Since STRUC-PERC-I already identified HARD_FRAGMENTATION in the relevant variables, the priority score should be revised after shot-level review.

### 9.4 Candidate variables still need field-glossary locking

Several fields use `_candidate` names. Their units and exact physical meanings should be finalized from the TCV README/notebook before manuscript-level claims are made.

### 9.5 Gap-component mapping is not yet causal physics

A mapped branch says that a shot or shot pair sits near a structural discontinuity in a scalar ladder. It does not by itself prove the physical cause of H-mode. It tells us where to inspect next.

---

## 10. Working conclusion

The new mapping result gives the UNNS-H Mode project its first shot-localized branch structure.

The most meaningful conclusion is:

> The TCV L-H transition data is not merely admissible and not merely fragmented. It is selectively branched. The branches localize around a small set of shots and around variables tied to power balance, transport, timing, and edge/divertor response.

This is a stronger position than the two-chamber result alone. It gives us actual discharge candidates to inspect for physical transition families.

---

## 11. Recommended next analytical step

The next step should be a focused suspect-shot reviewer:

`components/tcv_suspect_shot_reviewer.py`

It should read:

- `data/processed/tcv_lh_events_canonical.csv`
- `outputs/reports/tcv_suspect_transition_families.csv`

and export:

- `outputs/reports/tcv_suspect_shot_review.csv`
- `outputs/reports/tcv_suspect_shot_review.md`

The reviewer should aggregate one row per suspect shot and list the physical variables, fragment variables, branch counts, and possible subfamily interpretation.

This is the correct next move because the work has now reached the point where abstract chamber branches must be converted into physically interpretable discharge families.
