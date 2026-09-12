# JHTDB Pilot A — STITCH-MECH Summary

**Project:** `UNNS_TURB_JHTDB_v0_1`  
**Pilot:** `jhtdb_pilot_a`  
**Mechanism instrument:** `STITCH-MECH v0.1.1`  
**Mechanistic verdict:** `SURVIVES_LOCAL_GEOMETRY_CONTROL`

## 1. Research question

The purpose of this phase was to test whether the very low real scale–time stitching defect,

\[
D_{\square},
\]

is merely a consequence of local route geometry, or whether it reflects a deeper organization of turbulent structural evolution.

The operative question was:

> **Does the low real \(D_{\square}\) remain exceptional after the route graph is randomized under progressively stronger local geometric constraints?**

This phase therefore moved beyond the original degree-preserving ROUTE-I null and introduced a hierarchy of harder controls.

---

## 2. Frozen baseline

The analysis uses the frozen STRUC-ROUTE-I Pilot-A run:

`outputs/exports/struc_route_i/jhtdb_pilot_a/jhtdb_pilot_a_20260904_235409.zip`

SHA-256:

`cc2c2caadca37d8f9cea7415bad37929da4e3a11d069a1414d18fba42126b788`

The frozen route graph contains:

- 12,484 structural objects;
- 17,560 supplied route candidates;
- 17,459 eligible relations;
- 5 scale layers;
- 10 time layers.

STITCH-MECH independently recomputed the stored edge geometry and reproduced the real ROUTE-I mean stitching defect exactly:

\[
D_{\square}^{real}=0.026627534107437796.
\]

The geometry consistency check passed with effectively machine-precision agreement:

- maximum `distance_norm` recomputation error:
  \(5.55\times10^{-17}\);
- maximum `feature_similarity` recomputation error:
  \(0\).

---

## 3. Null hierarchy

Three controls define the mechanism test.

### N0 — frozen ROUTE-I null

Degree-preserving endpoint rewiring from the original STRUC-ROUTE-I analysis.

\[
D_{\square}^{N0}=0.9967862679967401
\]

with:

\[
z_{fav}\approx1022.66,
\qquad
p_{fav}=0.00990099.
\]

### N1 — distance-stratified degree-preserving null

N1 preserves:

- route axis and layer transition;
- source out-degree;
- destination in-degree;
- source-row confidence weight;
- within-transition `distance_norm` stratum.

Result:

\[
D_{\square}^{N1}=0.3290907646784556.
\]

The real graph is still far below the constrained null:

\[
\frac{D_{\square}^{real}}{D_{\square}^{N1}}
\approx0.0809.
\]

Equivalently, the real defect is about 91.9% lower than the N1 mean.

Inference:

\[
z_{fav}\approx106.40,
\qquad
p_{fav}=0.00990099.
\]

Null quality:

- 100/100 unique null graphs;
- mean mobility fraction:
  \(0.04548\);
- real-graph match fraction:
  \(0\);
- no quality flags.

### N2 — distance + feature-stratified degree-preserving null

N2 preserves all N1 constraints and additionally preserves the within-transition `feature_similarity` stratum.

Result:

\[
D_{\square}^{N2}=0.2236493646833274.
\]

The real graph remains:

\[
\frac{D_{\square}^{real}}{D_{\square}^{N2}}
\approx0.1191,
\]

so the real defect is about 88.1% lower than the N2 mean.

Inference:

\[
z_{fav}\approx44.69,
\qquad
p_{fav}=0.00990099.
\]

Null quality:

- 100/100 unique null graphs;
- mean mobility fraction:
  \(0.01546\);
- real-graph match fraction:
  \(0\);
- no quality flags.

---

## 4. Primary result

The null hierarchy behaves in the physically expected direction:

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

As progressively more local geometry is preserved, the nulls become more similar to the real graph. This shows that local geometry explains part of the original ROUTE-I contrast.

However, even the hardest N2 control remains far from the real value.

Therefore the primary mechanistic result is:

\[
\boxed{\texttt{SURVIVES\_LOCAL\_GEOMETRY\_CONTROL}}
\]

The low real scale–time stitching defect cannot be explained by:

- degree structure alone;
- route-layer structure alone;
- centroid/radius distance locality alone;
- or the combined distance + local feature-similarity structure preserved by N2.

This establishes a residual scale–time organization beyond the tested graph-local geometric constraints.

---

## 5. Object-level mechanism

STITCH-MECH analyzed all:

\[
4957
\]

stitching-eligible source objects.

The ordinary rank associations are:

\[
\rho(D_{\square},\text{enstrophy})
=0.16675,
\]

\[
\rho(D_{\square},\epsilon_{proxy})
=0.18983.
\]

After conditioning on:

- scale;
- time;
- outgoing overlap statistics;
- IoU;
- normalized distance;
- feature similarity;
- scale branch state;
- time branch state;
- scale merge state;
- time merge state,

the physical-intensity association remains positive:

\[
\rho_{partial}(D_{\square},\text{enstrophy})
=0.17902,
\]

\[
\rho_{partial}(D_{\square},\epsilon_{proxy})
=0.12005.
\]

Thus the association between stitching failure and physical intensity is not removed by the available route-geometry controls.

---

## 6. High-\(D_{\square}\) tail

The upper 10% of the \(D_{\square}\) population contains 496 objects.

Within that tail:

### Enstrophy

124 of the 496 high-\(D_{\square}\) objects also belong to the top 10% of enstrophy.

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

with stratified permutation:

\[
p\approx1.9996\times10^{-4}.
\]

### Dissipation proxy

93 of the 496 high-\(D_{\square}\) objects also belong to the top 10% of the dissipation proxy.

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

This confirms that large departures from scale–time commutation preferentially occur in physically intense structures.

---

## 7. Branching and merging

The defect is also associated with structural reorganization.

Median-\(D_{\square}\) contrasts are significant for:

- scale branching;
- time branching;
- time merging;
- any branch/merge restructuring.

For example:

### Scale branching

- flagged:
  422 objects;
- median \(D_{\square}\):
  \(9.61\times10^{-4}\);
- unflagged median:
  \(0\);
- permutation:
  \(p\approx1.9996\times10^{-4}\).

### Time branching

- flagged:
  174 objects;
- median \(D_{\square}\):
  \(3.35\times10^{-4}\);
- unflagged median:
  \(0\);
- permutation:
  \(p\approx1.9996\times10^{-4}\).

### Time merging

- flagged:
  127 objects;
- median \(D_{\square}\):
  \(7.56\times10^{-4}\);
- unflagged median:
  \(0\);
- permutation:
  \(p\approx1.9996\times10^{-4}\).

### Any restructuring

- flagged:
  680 objects;
- median \(D_{\square}\):
  \(9.57\times10^{-5}\);
- unflagged median:
  \(0\);
- permutation:
  \(p\approx1.9996\times10^{-4}\).

Scale merging alone does not show the same contrast.

---

## 8. Structural interpretation

The mechanism-stage result now supports a more specific picture than the original constrained-routing statement.

Most turbulent structural evolution is close to scale–time commuting:

\[
ST\approx TS.
\]

The scale-first and time-first routes usually lead to nearly the same descendant distribution.

The failures of that compatibility are localized rather than global.

They preferentially occur where structures are:

- branching;
- merging;
- undergoing route restructuring;
- high in enstrophy;
- or high in dissipation proxy.

This suggests a candidate structural regime:

> **A largely commuting scale–time organization with localized noncommuting breakdowns associated with intense turbulent restructuring.**

This is now the leading mechanistic interpretation of Pilot A.

---

## 9. Relation to the previous cross-chamber result

The earlier Pilot-A synthesis established that `D_STITCH` is the strongest primary structural coordinate because it survives three independent chamber views:

1. STRUC-ROUTE-I:
   constrained relative to matched route nulls;
2. STRUC-I:
   Geometric Persistence / Weak Persistence;
3. STRUC-PERC-I:
   Giant Component Percolation.

STITCH-MECH adds a fourth layer of evidence:

4. the low real \(D_{\square}\) survives harder graph-local geometry controls.

The evidence hierarchy is therefore now:

\[
\boxed{
\text{Constrained routing}
\rightarrow
\text{Persistent }D_{\square}\text{ geometry}
\rightarrow
\text{Connected }D_{\square}\text{ gap structure}
\rightarrow
\text{Survival under local-geometry nulls}
}
\]

---

## 10. Claim boundary

The positive result must remain within the actual capabilities of the frozen Pilot-A graph.

N1 and N2 preserve increasingly local graph geometry available from the ROUTE-I object and edge tables.

They do **not** preserve exact newly evaluated voxel overlap or IoU for rewired object pairs, because the original object masks are not contained in the frozen ROUTE-I run.

Therefore this result establishes:

> **The scale–time stitching signal survives the tested graph-local geometric explanations.**

It does **not yet establish** survival against every possible field-level geometric or dynamical surrogate.

---

## 11. Resulting hypothesis

The strongest current Pilot-A hypothesis is:

\[
\boxed{
\text{Turbulent structural evolution occupies a largely commuting scale–time route regime,}
}
\]

with:

\[
\boxed{
\text{localized noncommutation associated with intense restructuring events.}
}
\]

A plausible physical interpretation is that ordinary turbulent evolution preserves a common structural ancestry across scale and time, while intermittent or strongly reorganizing events locally break that compatibility.

The intermittency interpretation remains a hypothesis until tested against independent cutouts and standard intermittency observables.

---

## 12. Next experiment

The next scientific step is **independent JHTDB replication under frozen settings**.

The Pilot-A protocol should now be frozen before replication:

- physical adapter settings;
- scale factors;
- segmentation;
- ROUTE-I thresholds;
- ROUTE-I null settings;
- `D_STITCH` extraction;
- STRUC-I / STRUC-PERC-I interpretation rules;
- STITCH-MECH N1/N2 definitions;
- null-quality thresholds;
- physical-tail definitions.

The next replication should use an independent spatial cutout and/or independent time window.

The central replication question is:

> **Does the same commuting scale–time regime, including its localized physically intense breakdowns, reappear independently?**

---

## 13. Phase conclusion

Pilot A has now progressed from a first positive route result to a mechanistic structural finding.

The current evidence supports:

\[
\boxed{
\textbf{Scale–time structural compatibility is a real, nontrivial organizing feature of this turbulent flow sample.}
}
\]

Within the tested graph-local controls, it is not reducible to degree structure, local spatial proximity, or local feature similarity.

The remaining task is no longer to establish that Pilot A contains structure.

It is to determine whether this scale–time structural regime is **reproducible and generalizable**.
