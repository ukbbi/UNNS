# JHTDB Pilot A — Cross-Chamber Synthesis

**Project:** `UNNS_TURB_JHTDB_v0_1`  
**Pilot:** `jhtdb_pilot_a`  
**Record:** `JHTDB_CROSS_CHAMBER_SYNTHESIS v0.1`  
**Status:** Pilot-A synthesis complete

## 1. Purpose

This record freezes the first cross-chamber interpretation of the JHTDB forced-isotropic turbulence pilot after independent interrogation by:

- **STRUC-ROUTE-I v0.1.2** — route persistence, branching/merging, null comparison, and scale-time stitching;
- **STRUC-I v1.0.4** — perturbational admissibility geometry;
- **STRUC-PERC-I v2.5.0** — connectivity/percolation of ladder-gap structure.

The three chambers are not chained numerically. STRUC-I and STRUC-PERC-I independently interrogate frozen scalar descendants extracted from the same STRUC-ROUTE-I run.

## 2. Frozen provenance

Primary physical source:

`data/raw/jhtdb/isotropic1024coarse/cutouts/isotropic1024-coarse-velocity.h5`

Public source reference:

[ArielLubonja/johns-hopkins-turbulence-database — Hugging Face dataset repository](https://huggingface.co/datasets/ArielLubonja/johns-hopkins-turbulence-database/tree/main)

This public repository is the external source used to obtain the local frozen JHTDB-derived HDF5 corpus preserved by this project.

SHA-256:

`e32c9225af656a2f0fa0a704be7dcd78fa12efc1a01b880af23eb45e02108a46`

Frozen STRUC-ROUTE-I run:

`outputs/exports/struc_route_i/jhtdb_pilot_a/jhtdb_pilot_a_20260904_235409.zip`

SHA-256:

`cc2c2caadca37d8f9cea7415bad37929da4e3a11d069a1414d18fba42126b788`

STRUC-I exports:

- `outputs/exports/struc_i/jhtdb_pilot_a/mc2000/`
- `outputs/exports/struc_i/jhtdb_pilot_a/mc10000/`

STRUC-PERC-I export:

- `outputs/exports/struc_perc_i/jhtdb_pilot_a/batch_01/`

Primary route-derived ladders:

- `D_STITCH`
- `P_TIME`
- `P_SCALE`

## 3. STRUC-ROUTE-I result

The physical route graph contains:

- 12,484 structural objects;
- 17,560 supplied route candidates;
- 17,459 eligible relations;
- 5 scale layers;
- 10 time layers.

The primary verdict is:

**CONSTRAINED_ROUTING**

The null ensemble is well mobile and diverse:

- 100/100 unique null graphs;
- mean mobility ≈ 0.9986;
- real-graph match fraction = 0.

The inferential pattern is:

| Metric | Real | Null mean | Result |
|---|---:|---:|---|
| Scale persistence | 0.3508 | 0.3498 | positive, not significant (`p≈0.0792`) |
| Time persistence | 0.5072 | 0.4956 | supported (`z≈11.01`, `p≈0.0099`) |
| Stitching defect `D□` | 0.0266 | 0.9968 | strongly supported (`z_fav≈1022.66`, `p≈0.0099`) |

Route entropy is descriptive only under the current endpoint-rewiring null.

The `[1,2,4,8]` sensitivity analysis retains `CONSTRAINED_ROUTING`, so the sparse factor-16 layer does not drive the primary route result.

## 4. STRUC-I result

The 10,000-MC precision run reproduces the same qualitative partition as the 2,000-MC primary run.

| Ladder | mean Aκ | min Aκ | Aκ at κmax | Regime | State |
|---|---:|---:|---:|---|---|
| `D_STITCH` | 0.971708 | 0.9181 | 0.9989 | **Geometric Persistence** | Weak Persistence |
| `P_TIME` | 0.598378 | 0.5813 | 0.6340 | Structural Instability | Random Structure |
| `P_SCALE` | 0.535600 | 0.5228 | 0.5541 | Structural Instability | Random Structure |

`P_TIME` is **boundary-adjacent**: its mean `Aκ` lies only `0.001622` below the chamber's `0.60` regime boundary. This does not change the formal verdict, but it should be retained in interpretation.

`D_STITCH` is not boundary-adjacent. Its high `Aκ` is reproduced under the larger Monte Carlo count and is the robust STRUC-I positive.

## 5. STRUC-PERC-I result

| Ladder | Verdict | Gap vertices | Giant ratio | Isolated | Interpretation |
|---|---|---:|---:|---:|---|
| `D_STITCH` | **GIANT_COMPONENT_PERCOLATION** | 652 | 0.996933 | 0 | substantive |
| `P_TIME` | FULL_PERCOLATION | 9 | 1.000000 | 0 | low-dimensional / quantized |
| `P_SCALE` | FULL_PERCOLATION | 3 | 1.000000 | 0 | low-dimensional / quantized |

The `P_TIME` and `P_SCALE` percolation results must not be read as evidence from thousands of independent gap vertices. The generic adapter sorts and deduplicates exact duplicate ladder values before constructing the gap graph. Because persistence is highly quantized, the resulting graphs have only 9 and 3 gap vertices respectively.

`D_STITCH`, by contrast, retains 652 gap vertices and reaches a giant ratio of ≈99.693% with no isolated vertices. This is the substantive percolation result.

## 6. Cross-chamber signature

### D_STITCH — primary organization coordinate

**ROUTE-I:** very low real scale-time stitching defect relative to rewired route nulls.  
**STRUC-I:** Geometric Persistence / Weak Persistence.  
**STRUC-PERC-I:** Giant Component Percolation.

**Synthesis:** `D_STITCH` is the only primary Pilot-A descendant that remains structurally organized under all three independent chamber views.

### P_TIME — network organization without scalar admissibility

**ROUTE-I:** temporal persistence is significantly enhanced relative to the route null.  
**STRUC-I:** boundary-adjacent Structural Instability.  
**STRUC-PERC-I:** full percolation only after collapse to a 9-gap quantized support.

**Synthesis:** temporal persistence is meaningful as a property of the route network, but its scalar value population is not itself a robust admissible ladder.

### P_SCALE — weak route signal

**ROUTE-I:** scale persistence is positive but not significant at the primary inference threshold.  
**STRUC-I:** Structural Instability.  
**STRUC-PERC-I:** full percolation only on a 3-gap quantized support.

**Synthesis:** no strong cross-chamber organization is established for the scale-persistence coordinate.

## 7. Principal finding

The strongest structural result of Pilot A is **not merely that turbulent objects persist**.

It is:

> **The compatibility of structural evolution across scale and time is more strongly organized than the persistence magnitudes themselves.**

Scale-time stitching survives three distinct interrogations:

1. it is extraordinarily different from matched route-null organization;
2. its scalar population has persistent admissibility geometry;
3. its gap structure is almost globally connected.

This makes scale-time compatibility the leading structural coordinate of the current UNNS turbulence branch.

## 8. Physical tail

Rare high-`D_STITCH` events preferentially coincide with physically intense structures:

- top-decile enstrophy enrichment ≈ 2.50×;
- top-decile dissipation-proxy enrichment ≈ 1.87×.

The association remains after scale control in the completed follow-up analysis.

This supports a specific hypothesis:

> Local failures of scale-time stitching may be associated with turbulent intermittency.

This is **not yet an identification of `D_STITCH` with intermittency**. It is a testable next-stage hypothesis.

## 9. Claim boundary

### Established within Pilot A

- Constrained route organization relative to the frozen degree-preserving route-null ensemble.
- Enhanced temporal route persistence.
- Strongly reduced real scale-time stitching defect.
- Robust STRUC-I Geometric Persistence of `D_STITCH`.
- STRUC-PERC-I Giant Component Percolation of `D_STITCH`.
- Survival of the route verdict after removal of factor 16.

### Supported but not generalized

- Scale-time compatibility appears structurally privileged relative to persistence magnitudes.
- High-stitch-defect events are enriched in intense turbulent structures.

### Open

- Generality across independent JHTDB cutouts and time windows.
- Generality across Reynolds numbers and turbulence classes.
- Survival under harder geometry-constrained or field-level nulls.
- Direct relationship between high-`D_STITCH` events and standard intermittency observables.

## 10. Next research question

**Why is scale-time stitching organized when the persistence coordinates themselves are not?**

The next validation stage should replicate the frozen Pilot-A protocol on an independent JHTDB cutout/time window before any threshold retuning or broader turbulence claim.
