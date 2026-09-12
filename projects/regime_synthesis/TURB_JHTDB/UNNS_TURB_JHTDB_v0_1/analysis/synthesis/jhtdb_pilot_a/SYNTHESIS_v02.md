# JHTDB Pilot A — Cross-Stage Structural Synthesis v0.2

**Project:** `UNNS_TURB_JHTDB_v0_1`  
**Pilot:** `jhtdb_pilot_a`  
**Record:** `JHTDB_CROSS_STAGE_SYNTHESIS v0.2`  
**Status:** Pilot-A cross-chamber + mechanism synthesis complete

## 1. Purpose of v0.2

Version 0.1 established the first cross-chamber Pilot-A result:

- STRUC-ROUTE-I found **CONSTRAINED_ROUTING**;
- `D_STITCH` showed **Geometric Persistence** in STRUC-I;
- `D_STITCH` showed **Giant Component Percolation** in STRUC-PERC-I;
- temporal persistence was significant at the route-network level but did not form a robust scalar admissibility ladder;
- scale persistence was weaker and non-significant at the primary ROUTE-I inference threshold.

Version 0.2 adds the completed **STITCH-MECH v0.1.1** mechanism stage.

The central question is no longer only whether scale–time stitching is organized.

It is now:

> **Does the exceptionally low real scale–time stitching defect survive increasingly local geometric route controls, and where does its remaining noncommutation occur?**

The answer within Pilot A is:

\[
\boxed{\texttt{SURVIVES\_LOCAL\_GEOMETRY\_CONTROL}}
\]

This upgrades `D_STITCH` from the leading cross-chamber coordinate to the leading **mechanistically constrained structural coordinate** of the pilot.

---

## 2. Frozen provenance

### Primary physical source

Local frozen source:

`data/raw/jhtdb/isotropic1024coarse/cutouts/isotropic1024-coarse-velocity.h5`

Public source reference:

[ArielLubonja/johns-hopkins-turbulence-database — Hugging Face dataset repository](https://huggingface.co/datasets/ArielLubonja/johns-hopkins-turbulence-database/tree/main)

This public repository is the external source used to obtain the local JHTDB-derived HDF5 corpus preserved by this project.

SHA-256:

`e32c9225af656a2f0fa0a704be7dcd78fa12efc1a01b880af23eb45e02108a46`

### Frozen STRUC-ROUTE-I run

`outputs/exports/struc_route_i/jhtdb_pilot_a/jhtdb_pilot_a_20260904_235409.zip`

SHA-256:

`cc2c2caadca37d8f9cea7415bad37929da4e3a11d069a1414d18fba42126b788`

### Downstream chamber exports

STRUC-I:

- `outputs/exports/struc_i/jhtdb_pilot_a/mc2000/`
- `outputs/exports/struc_i/jhtdb_pilot_a/mc10000/`

STRUC-PERC-I:

- `outputs/exports/struc_perc_i/jhtdb_pilot_a/batch_01/`

### Mechanism-stage outputs

Human/machine analysis:

`analysis/mechanism/jhtdb_pilot_a/stitch_mech_v01/`

Core mechanism report:

- `REPORT.html`
- `REPORT.json`
- `SUMMARY.md`

Mechanism tables:

`outputs/tables/stitch_mech/`

Result bundle:

`outputs/records/STITCH_MECH_RESULT.zip`

---

## 3. Pilot-A structural pipeline

The Pilot-A inference chain is now:

\[
\boxed{
\text{JHTDB velocity field}
\rightarrow
\text{physical objects}
\rightarrow
\text{scale/time route graph}
\rightarrow
D_{\square}
}
\]

followed by four independent interrogation layers:

\[
\boxed{
\text{STRUC-ROUTE-I}
\rightarrow
\{\text{STRUC-I},\text{STRUC-PERC-I}\}
\rightarrow
\text{STITCH-MECH}
}
\]

The chambers are not numerically chained in series.

STRUC-I and STRUC-PERC-I independently interrogate frozen scalar descendants extracted from the same ROUTE-I result.

STITCH-MECH returns to the frozen route graph and asks whether the `D_STITCH` result survives harder route-null constraints.

---

## 4. STRUC-ROUTE-I baseline

The physical route graph contains:

- 12,484 structural objects;
- 17,560 supplied route candidates;
- 17,459 eligible relations;
- 5 scale layers;
- 10 time layers.

Primary verdict:

\[
\boxed{\texttt{CONSTRAINED\_ROUTING}}
\]

Null quality:

- 100/100 unique null graphs;
- mean mobility ≈ 0.9986;
- real-graph match fraction = 0.

Primary inferential pattern:

| Metric | Real | Null mean | Result |
|---|---:|---:|---|
| Scale persistence | 0.3508 | 0.3498 | positive, not significant (`p≈0.0792`) |
| Time persistence | 0.5072 | 0.4956 | supported (`z≈11.01`, `p≈0.0099`) |
| Stitching defect `D□` | 0.02663 | 0.99679 | strongly supported (`z_fav≈1022.66`, `p≈0.0099`) |

Route entropy remains descriptive only under the endpoint-rewiring null because the source outgoing edge-weight multiset is preserved by construction.

The `[1,2,4,8]` scale sensitivity run retains `CONSTRAINED_ROUTING`, establishing that the sparse factor-16 layer does not drive the route verdict.

---

## 5. Cross-chamber result

### 5.1 STRUC-I

The 10,000-MC precision run reproduces the same qualitative partition as the 2,000-MC primary run.

| Ladder | mean Aκ | min Aκ | Aκ at κmax | Regime | State |
|---|---:|---:|---:|---|---|
| `D_STITCH` | 0.971708 | 0.9181 | 0.9989 | **Geometric Persistence** | Weak Persistence |
| `P_TIME` | 0.598378 | 0.5813 | 0.6340 | Structural Instability | Random Structure |
| `P_SCALE` | 0.535600 | 0.5228 | 0.5541 | Structural Instability | Random Structure |

`P_TIME` is boundary-adjacent: its mean \(A_\kappa\) lies only 0.001622 below the 0.60 regime boundary.

`D_STITCH` is not boundary-adjacent. Its Geometric Persistence classification remains the robust STRUC-I positive.

### 5.2 STRUC-PERC-I

| Ladder | Verdict | Gap vertices | Giant ratio | Isolated | Interpretation |
|---|---|---:|---:|---:|---|
| `D_STITCH` | **GIANT_COMPONENT_PERCOLATION** | 652 | 0.996933 | 0 | substantive |
| `P_TIME` | FULL_PERCOLATION | 9 | 1.000000 | 0 | low-dimensional / quantized |
| `P_SCALE` | FULL_PERCOLATION | 3 | 1.000000 | 0 | low-dimensional / quantized |

The persistence ladders are highly quantized. The generic STRUC-PERC-I adapter deduplicates exact duplicate values before gap construction, leaving only 9 and 3 gap vertices for `P_TIME` and `P_SCALE`.

Their percolation verdicts are therefore descriptive of a very low-dimensional support.

`D_STITCH`, by contrast, retains 652 gap vertices and forms a giant component containing ≈99.693% of them, with no isolated vertices.

---

## 6. Cross-chamber signature

### `D_STITCH` — primary organization coordinate

**STRUC-ROUTE-I:** exceptionally low real scale–time stitching defect relative to degree-preserving route nulls.

**STRUC-I:** Geometric Persistence / Weak Persistence.

**STRUC-PERC-I:** Giant Component Percolation.

This was the v0.1 result:

\[
\boxed{
D_{\square}
\text{ survives route, admissibility, and gap-connectivity interrogation}
}
\]

### `P_TIME` — route-network organization without robust scalar admissibility

**STRUC-ROUTE-I:** temporal persistence is significantly enhanced relative to the null.

**STRUC-I:** boundary-adjacent Structural Instability.

**STRUC-PERC-I:** Full Percolation only after reduction to 9 distinct-gap vertices.

The temporal-persistence effect is therefore meaningful primarily as a route-network property rather than as a robust scalar ladder geometry.

### `P_SCALE` — weak route signal

**STRUC-ROUTE-I:** positive but non-significant scale-persistence excess.

**STRUC-I:** Structural Instability.

**STRUC-PERC-I:** Full Percolation on only 3 distinct-gap vertices.

No strong cross-chamber organization is established for scale persistence.

---

## 7. STITCH-MECH mechanism test

The mechanism stage asks whether the low real \(D_{\square}\) is already implied by local geometry.

STITCH-MECH first independently recomputed the stored route geometry and reproduced the ROUTE-I real mean exactly:

\[
D_{\square}^{real}
=
0.026627534107437796.
\]

Geometry consistency:

- `distance_norm` maximum recomputation error:
  \(5.55\times10^{-17}\);
- `feature_similarity` maximum recomputation error:
  \(0\).

This provides an independent implementation check before any new null is applied.

---

## 8. Harder null hierarchy

Three null levels now define the structural mechanism test.

### N0 — degree-preserving endpoint rewiring

Frozen ROUTE-I control:

\[
D_{\square}^{N0}
=
0.9967862679967401.
\]

\[
z_{fav}\approx1022.66,
\qquad
p_{fav}=0.00990099.
\]

### N1 — distance-stratified degree-preserving rewiring

N1 preserves:

- route axis;
- physical transition group;
- source out-degree;
- destination in-degree;
- source-row confidence weight;
- within-transition `distance_norm` stratum.

Result:

\[
D_{\square}^{N1}
=
0.3290907646784556.
\]

Real-to-null ratio:

\[
\frac{D_{\square}^{real}}{D_{\square}^{N1}}
\approx0.0809.
\]

Thus the real defect is about 91.9% lower than the N1 mean.

Inference:

\[
z_{fav}\approx106.40,
\qquad
p_{fav}=0.00990099.
\]

Null quality:

- 100/100 unique null graphs;
- mean mobility = 0.04548;
- real-graph match fraction = 0;
- no quality flags.

### N2 — distance + feature-stratified degree-preserving rewiring

N2 preserves all N1 constraints and additionally preserves the within-transition `feature_similarity` stratum.

Result:

\[
D_{\square}^{N2}
=
0.2236493646833274.
\]

Real-to-null ratio:

\[
\frac{D_{\square}^{real}}{D_{\square}^{N2}}
\approx0.1191.
\]

Thus the real defect is still about 88.1% lower than the N2 mean.

Inference:

\[
z_{fav}\approx44.69,
\qquad
p_{fav}=0.00990099.
\]

Null quality:

- 100/100 unique null graphs;
- mean mobility = 0.01546;
- real-graph match fraction = 0;
- no quality flags.

The N2 ensemble therefore remains sufficiently mobile and diverse to support inference.

---

## 9. Mechanistic result

The null hierarchy moves toward the real graph in the expected direction:

\[
N0
\rightarrow
N1
\rightarrow
N2
\rightarrow
REAL
\]

with:

\[
0.9968
\rightarrow
0.3291
\rightarrow
0.2236
\rightarrow
0.0266.
\]

This is important for two reasons.

First, local geometry clearly explains **part** of the original N0 contrast. The harder the geometric constraints become, the lower the null \(D_{\square}\) becomes.

Second, local geometry does **not** explain the majority of the real organization. Even N2 remains roughly 8.4 times larger than the real mean.

The resulting mechanism verdict is:

\[
\boxed{\texttt{SURVIVES\_LOCAL\_GEOMETRY\_CONTROL}}
\]

Within the tested graph-local controls, the low real scale–time stitching defect is not reducible to:

- route degree structure;
- layer-transition structure;
- centroid/radius locality;
- or the combined distance + local feature-similarity constraints implemented by N2.

This is the main addition of synthesis v0.2.

---

## 10. Object-level localization of noncommutation

STITCH-MECH analyzes all:

\[
4957
\]

stitching-eligible source objects.

The ordinary physical-intensity associations are:

\[
\rho(D_{\square},\text{enstrophy})
=
0.16675,
\]

\[
\rho(D_{\square},\epsilon_{proxy})
=
0.18983.
\]

After conditioning on scale, time, route-overlap statistics, IoU, normalized distance, feature similarity, and branch/merge state, the associations remain positive:

\[
\rho_{partial}(D_{\square},\text{enstrophy})
=
0.17902,
\]

\[
\rho_{partial}(D_{\square},\epsilon_{proxy})
=
0.12005.
\]

The intensity relationship is therefore not removed by the available graph-local geometry controls.

---

## 11. High-defect tail and physical intensity

The upper 10% of \(D_{\square}\) contains 496 source objects.

### Enstrophy

124 of those 496 objects also belong to the top decile of enstrophy.

Observed overlap:

\[
25.0\%.
\]

Random expectation:

\[
\approx10.0\%.
\]

Enrichment:

\[
\boxed{2.50\times}
\]

with time×scale-stratified permutation:

\[
p\approx1.9996\times10^{-4}.
\]

### Dissipation proxy

93 of the 496 high-\(D_{\square}\) objects also lie in the top decile of the dissipation proxy.

Observed overlap:

\[
18.75\%.
\]

Enrichment:

\[
\boxed{1.87\times}
\]

with:

\[
p\approx1.9996\times10^{-4}.
\]

Therefore large departures from scale–time commutation preferentially occur in physically intense structures.

---

## 12. Branching, merging, and restructuring

The stitching defect is also associated with route reorganization.

Significant median-\(D_{\square}\) contrasts occur for:

- scale branching;
- time branching;
- time merging;
- any branch/merge restructuring.

Examples:

### Scale branching

- 422 flagged objects;
- median \(D_{\square}=9.61\times10^{-4}\);
- unflagged median \(=0\);
- permutation \(p\approx1.9996\times10^{-4}\).

### Time branching

- 174 flagged objects;
- median \(D_{\square}=3.35\times10^{-4}\);
- unflagged median \(=0\);
- permutation \(p\approx1.9996\times10^{-4}\).

### Time merging

- 127 flagged objects;
- median \(D_{\square}=7.56\times10^{-4}\);
- unflagged median \(=0\);
- permutation \(p\approx1.9996\times10^{-4}\).

### Any restructuring

- 680 flagged objects;
- median \(D_{\square}=9.57\times10^{-5}\);
- unflagged median \(=0\);
- permutation \(p\approx1.9996\times10^{-4}\).

Scale merging alone does not show a corresponding median contrast.

The emerging picture is therefore not one of diffuse global disorder. Scale–time noncommutation is preferentially associated with structural reorganization.

---

## 13. Integrated Pilot-A interpretation

The evidence hierarchy now contains four distinct levels:

\[
\boxed{
\text{Constrained routing}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{Persistent }D_{\square}\text{ admissibility geometry}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{Nearly globally connected }D_{\square}\text{ gap structure}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{Survival under local-geometry route controls}
}
\]

The strongest Pilot-A interpretation is therefore no longer merely:

> turbulent objects persist.

Nor is it only:

> scale and time are compatible.

The more specific statement supported by the present evidence is:

> **Turbulent structural evolution occupies a strongly organized scale–time route regime in which scale-first and time-first ancestry are usually highly compatible, and this compatibility cannot be reduced to the tested local graph geometry alone.**

The remaining noncommutation is localized preferentially around:

- branching;
- merging/restructuring;
- high enstrophy;
- high dissipation proxy.

This motivates a structural picture of:

\[
\boxed{
\text{a largely commuting scale–time regime with localized noncommuting breakdowns}
}
\]

rather than a uniformly disordered route network.

---

## 14. Relation to intermittency

The high-\(D_{\square}\) tail is enriched in enstrophy and dissipation proxy even after time×scale stratification, and positive physical-intensity associations remain after geometry conditioning.

This supports the hypothesis:

> **Localized failures of scale–time stitching may form a structural signature of intense or intermittent turbulent events.**

This is not yet an identification of \(D_{\square}\) with a standard intermittency observable.

The current result establishes a physically enriched structural-breakdown population.

A direct intermittency claim requires independent comparison with standard intermittency measures or event definitions.

---

## 15. Claim boundary

### Established within Pilot A

- The frozen route graph is `CONSTRAINED_ROUTING` relative to the degree-preserving ROUTE-I null.
- Temporal route persistence is significantly enhanced.
- Real scale–time stitching defect is extraordinarily below the N0 null.
- `D_STITCH` has robust STRUC-I Geometric Persistence.
- `D_STITCH` has substantive STRUC-PERC-I Giant Component Percolation.
- Removing factor 16 does not remove the ROUTE-I result.
- The real \(D_{\square}\) survives the distance-stratified N1 null.
- The real \(D_{\square}\) survives the distance + feature-stratified N2 null.
- N1 and N2 pass the preregistered mobility/diversity quality gates.
- High-\(D_{\square}\) events are enriched in high enstrophy and high dissipation proxy.
- Branching and several restructuring states are associated with elevated \(D_{\square}\).

### Supported but not generalized

- Scale–time compatibility appears structurally privileged relative to persistence magnitudes.
- A largely commuting route regime with localized restructuring-linked breakdowns is a coherent description of Pilot A.
- The high-\(D_{\square}\) population is a plausible structural candidate for an intermittency-related event class.

### Not yet established

- Generality across independent spatial cutouts.
- Generality across independent time windows.
- Generality across Reynolds numbers.
- Generality across other turbulence classes.
- Survival under a field-level surrogate preserving exact newly evaluated voxel overlap or IoU.
- Equivalence between high \(D_{\square}\) and any standard intermittency observable.

---

## 16. Important limitation of N1/N2

N1 and N2 are harder **graph-local** nulls built from information preserved in the frozen ROUTE-I object and edge tables.

They preserve increasingly local route geometry, but newly rewired object pairs do not have original voxel masks available.

Therefore N1/N2 cannot preserve exact newly evaluated voxel overlap or IoU.

The correct interpretation is:

> **The scale–time stitching signal survives the tested graph-local geometric explanations.**

It is not yet:

> the signal survives every possible field-level geometric or dynamical surrogate.

That stronger test belongs to a later phase.

---

## 17. What changed from synthesis v0.1

| Question | v0.1 | v0.2 |
|---|---|---|
| Is route organization non-null? | Yes | Yes |
| Is `D_STITCH` cross-chamber organized? | Yes | Yes |
| Could the huge N0 contrast mainly reflect local route geometry? | Open | **Tested** |
| Does distance locality explain the result? | Open | **No — N1 remains far above real** |
| Does distance + feature locality explain the result? | Open | **No — N2 remains far above real** |
| Where does noncommutation concentrate? | Partly observed | **Localized around intensity and restructuring** |
| Next question | mechanism | **independent replication** |

The principal conceptual advance of v0.2 is therefore:

\[
\boxed{
\text{The leading scale–time organization survives a direct mechanism-oriented null hierarchy.}
}
\]

---

## 18. Frozen Pilot-A baseline for replication

Before replication, the following should now remain frozen:

- JHTDB physical-adapter settings;
- source-boundary treatment;
- multiscale factors;
- object-segmentation rule;
- STRUC-ROUTE-I eligibility thresholds;
- ROUTE-I null settings;
- `D_STITCH`, `P_TIME`, and `P_SCALE` extraction rules;
- STRUC-I chamber settings and interpretation thresholds;
- STRUC-PERC-I chamber settings;
- STITCH-MECH N1 definition;
- STITCH-MECH N2 definition;
- N1/N2 bin counts;
- N1/N2 swap intensity;
- null-quality thresholds;
- high-\(D_{\square}\) tail definition;
- geometry-conditioned mechanism controls.

No threshold should be retuned after seeing the replication data.

---

## 19. Correct next experiment

The next scientific task is an **independent JHTDB replication under this frozen Pilot-A protocol**.

The independent realization should change the physical sample, not the inference machinery.

Suitable replication axes include:

- a different spatial cutout;
- a different time window;
- eventually a different forced-isotropic realization or Reynolds-number regime.

The primary replication questions are:

1. Does the independent sample again produce `CONSTRAINED_ROUTING`?
2. Is real \(D_{\square}\) again extremely low?
3. Does `D_STITCH` again show cross-chamber organization?
4. Does the low \(D_{\square}\) again survive N1?
5. Does it again survive N2?
6. Are high-\(D_{\square}\) events again enriched in physical intensity and restructuring?

The central replication target is therefore not merely a verdict label.

It is the **full structural signature**:

\[
\boxed{
\text{commuting scale–time organization}
+
\text{localized physically intense breakdowns}
}
\]

---

## 20. Synthesis conclusion

Pilot A has progressed through four increasingly demanding stages:

1. real-data structural extraction;
2. route-null discrimination;
3. independent cross-chamber interrogation;
4. mechanism-oriented local-geometry controls.

At every stage, `D_STITCH` has remained the strongest structural coordinate.

The current Pilot-A evidence supports:

\[
\boxed{
\textbf{Scale–time structural compatibility is a nontrivial organizing feature of this turbulent-flow sample.}
}
\]

Within the tested graph-local controls, it is not reducible to route degree structure, centroid/radius locality, or local feature similarity.

The evidence further indicates that noncommutation is not uniformly distributed: it is preferentially associated with route restructuring and physically intense structures.

Accordingly, the leading working picture is:

\[
\boxed{
\textbf{a largely commuting turbulent scale–time route regime with localized noncommuting breakdowns.}
}
\]

The next scientific burden is no longer to show that Pilot A contains such organization.

It is to determine whether this structural regime **reappears independently under a frozen protocol**.
