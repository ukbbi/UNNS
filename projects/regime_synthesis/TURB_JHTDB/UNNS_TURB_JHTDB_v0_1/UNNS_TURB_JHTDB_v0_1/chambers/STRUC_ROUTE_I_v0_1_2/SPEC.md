# STRUC-ROUTE-I v0.1.2 Specification

## 1. Identity

**STRUC-ROUTE-I — Multiscale Structural Routing & Persistence Chamber**

The chamber tests whether structures in a layered dynamical system occupy a
restricted and reproducible route space through scale and/or time.

The primitive object is a directed layered graph:

\[
\mathcal G = (V,E_s,E_t)
\]

where \(E_s\) contains adjacent-scale relations and \(E_t\) contains
adjacent-time relations.

The chamber core is domain-agnostic. Physical feature extraction and object
segmentation occur upstream.

## 2. Input schema

### objects

Required columns:

- `node_id`
- `time_idx`
- `time_value`
- `scale_idx`
- `scale_value`
- `object_id`
- `size`

Optional but recognized:

- `weight`
- `cx`, `cy`, `cz`
- `family_id`
- arbitrary physical feature columns

### relations

Required columns:

- `src_id`
- `dst_id`
- `axis` — `scale` or `time`

Optional:

- `confidence`
- `overlap_src`
- `overlap_dst`
- `iou`
- `distance_norm`
- `feature_similarity`
- `transfer_weight`
- arbitrary relation feature columns

## 3. Relation eligibility

Eligibility is preregistered in `manifest.json`.

Example:

```json
{
  "relation_rule": {
    "mode": "all",
    "conditions": [
      {"column": "confidence", "op": ">=", "value": 0.5}
    ]
  }
}
```

Supported operators:

`>=`, `>`, `<=`, `<`, `==`, `!=`

The empty condition list accepts all supplied relations.

The operative relation weight column is separately declared:

```json
"edge_weight_column": "confidence"
```

Missing edge weights default to 1.0.

## 4. Adjacency rule

By default `strict_adjacent = true`.

A scale edge must satisfy:

\[
\Delta scale\_idx=+1,\qquad \Delta time\_idx=0.
\]

A time edge must satisfy:

\[
\Delta time\_idx=+1,\qquad \Delta scale\_idx=0.
\]

Invalid relations are fatal in strict mode.

## 5. Persistence

For axis \(a\in\{s,t\}\), dynamic programming on the layered DAG gives the
maximum number of forward axis transitions reachable from every object:

\[
D_a(O).
\]

Normalized persistence is

\[
P_a(O)=\frac{D_a(O)}{N_a-1}.
\]

The chamber reports all-node and source-node means plus percentiles.

## 6. Branching and merging

For an axis-specific route graph,

\[
B(O)=\max(d_{\rm out}(O)-1,0)
\]

and

\[
M(O)=\max(d_{\rm in}(O)-1,0).
\]

Branch/merge fractions and multiplicity distributions are reported.

Branching is descriptive. It is not automatically failure.

## 7. Route entropy

Outgoing route weights are normalized:

\[
p_{ij}=\frac{w_{ij}}{\sum_j w_{ij}}.
\]

For \(d_i>1\),

\[
H_i=-\frac{\sum_j p_{ij}\ln p_{ij}}{\ln d_i}.
\]

For one available daughter, \(H_i=0\).

Thus \(0\le H_i\le1\).

Low entropy means strongly preferred routing.

## 8. Route conservation

If `object_weight_column` is declared, destination weight is attributed among
incoming parents proportionally to relation weights.

For parent \(O\),

\[
C_{\rm out}(O)=
\frac{\sum_j W_j^{(\rm attributed)}}{W_O}.
\]

The chamber does not interpret the chosen physical weight.

## 9. Scale-time stitching

For every elementary scale-time cell, compare:

scale then time:

\[
P_{ST}=S_{s,t}T_{s+1,t}
\]

with time then scale:

\[
P_{TS}=T_{s,t}S_{s,t+1}.
\]

For each source object where both two-step distributions exist:

\[
D_\square =
\frac{\operatorname{JSD}(P_{ST},P_{TS})}{\ln2}.
\]

Therefore:

\[
0\le D_\square\le1.
\]

The chamber reports source-level and cell-level stitching defects.

## 10. Null model

The primary internal null preserves:

- axis;
- transition layer;
- number of edges;
- source out-degree;
- destination in-degree;

while rewiring ancestry by repeated directed endpoint swaps.

Field-level controls remain upstream and may be run through the same chamber.

## 11. Null-normalized evidence

The primary evidence metrics are:

- scale source persistence — high direction;
- time source persistence — high direction;
- scale route entropy — low direction;
- time route entropy — low direction;
- scale-time stitching defect — low direction.

For each metric the chamber reports:

- real value;
- null mean;
- null standard deviation;
- favorable-direction z;
- empirical favorable p;
- empirical opposing p.

No weighted composite score is used.

## 12. Evidence verdict v0.1.2

The inference rule is frozen and exported.

`UNDERRESOLVED`
: fewer than two eligible evidence metrics or fewer than `min_nulls` completed
  null graphs.

`CONSTRAINED_ROUTING`
: at least two metrics show favorable empirical p ≤ alpha and no metric shows
  opposing empirical p ≤ alpha.

`NULL_LIKE_ROUTING`
: no favorable or opposing metric reaches alpha.

`MIXED_ROUTING`
: all other sufficiently resolved cases.

Default:
- alpha = 0.05
- min_nulls = 20
- null_count = 100

These are inference settings, not claims of universal physical thresholds.

## 13. Family transitions

If `family_id` is present, family transition counts/probabilities are exported.
Family discovery itself is outside the v0.1.2 chamber core.

## 14. Chamber-array descendants

`LADDERS.zip` exports scalar route-derived sequences suitable for later
adaptation to canonical STRUC-I / STRUC-PERC-I:

- scale persistence
- time persistence
- scale entropy
- time entropy
- scale branching
- time branching
- scale merging
- time merging
- route conservation when available
- stitching defect

## 15. Interface architecture

Python is operative.

HTML/CSS/JavaScript provide:
- input;
- run control;
- progress;
- display;
- sampled route visualization;
- export access.

Browser rendering never changes the analyzed graph.

## 16. Null-mobility diagnostics — v0.1.2

Every generated null graph now records:

- `swap_attempts`
- `swap_accepted`
- `mobility_fraction`
- `mobile_groups`
- `transition_groups`
- `graph_signature`
- `matches_real_graph`

The ensemble-level quality record reports:

\[
f_{\rm mob} =
\frac{N_{\rm accepted}}{N_{\rm attempted}}
\]

together with null-graph diversity and real-graph clone fraction.

Default quality gates:

- mean mobility fraction ≥ 0.01
- unique null-graph fraction ≥ 0.10
- real-graph match fraction ≤ 0.90

These thresholds are configurable under `nulls.mobility` in the manifest.

If the null ensemble fails a quality gate, the chamber emits one or more of:

- `NULL_ENSEMBLE_IMMOBILE`
- `NULL_ENSEMBLE_LOW_DIVERSITY`
- `NULL_ENSEMBLE_REAL_CLONE_DOMINATED`

and the primary evidence verdict is forced to `UNDERRESOLVED`.

This prevents a structurally frozen null ensemble from being misread as evidence
that the real route graph is statistically null-like.



## 17. v0.1.2 inference-role correction

Route entropy is retained as a descriptive structural observable but is removed
from the inferential evidence set under the degree-preserving endpoint-rewiring
null.

Reason: this null preserves every source node's outgoing edge-weight multiset.
Since local route entropy is a function only of those normalized outgoing
weights, it is invariant under the null transformation.

Inferential metrics for this null are therefore:

- scale source persistence — high direction;
- time source persistence — high direction;
- scale–time stitching defect — low direction.

## 18. Incremental rendering

After the real graph is complete but before null generation finishes, the Python
engine publishes the real structure summary to the local FastAPI job state.
Layers 1–6 render immediately and are explicitly marked preliminary until the
null ensemble completes.

Layer 7 additionally displays null progress, accepted swaps, mobility, elapsed
time and ETA.

## 19. Analysis-only structural filters

An optional manifest block:

```json
"analysis_filter": {
  "max_scale_idx": 3,
  "label": "scale_sensitivity_1_2_4_8"
}
```

filters the operative graph after schema validation and before relation
eligibility / metrics / null generation. The source tables are not modified.

## 20. High-D_square physical tail

For source objects with finite `stitch_defect`, v0.1.2 can export exploratory
association statistics between D_square and physical object intensity.

When `enstrophy_mean` and `q_mean` exist:

\[
||S||^2 = \mathrm{enstrophy} - 2Q.
\]

If viscosity is available, a dissipation proxy is

\[
\epsilon_{\rm proxy} = 2\nu ||S||^2.
\]

This analysis is exploratory and never changes the primary chamber verdict.
