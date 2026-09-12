# STITCH-MECH v0.1.1 — Specification

## Scientific question

\[
D_{\square}^{real} \ll D_{\square}^{N0}
\]

is already established. The next test is whether this contrast survives nulls
that retain increasingly local route geometry.

## Null invariants

Every generated N1/N2 graph preserves:

1. directed edge count;
2. axis (`scale` or `time`);
3. physical transition group;
4. source out-degree;
5. destination in-degree;
6. each source-row confidence weight.

N1 additionally preserves each edge-row's within-transition distance stratum.

N2 additionally preserves each edge-row's within-transition
feature-similarity stratum.

Pair-specific `distance_norm` and `feature_similarity` are recomputed after
accepted endpoint swaps.

## Primary endpoint

Mean source-level normalized Jensen-Shannon stitching defect:

\[
D_{\square}
=
JSD(ST,TS)/\ln 2.
\]

The exact STRUC-ROUTE-I v0.1.2 definitions are frozen in
`stitch_mech/route_math.py`.

## Inference

For each valid null ensemble:

\[
p_{fav}
=
\frac{1+\#\{D_{null}\le D_{real}\}}{N+1}.
\]

The frozen ROUTE-I significance level is retained.

## Null quality

A null family is not interpreted if:

- mean accepted-swap fraction < 0.01;
- unique graph fraction < 0.10;
- real-graph clone fraction > 0.90.

No automatic relaxation of N1/N2 constraints is permitted.

## Mechanism decomposition

Primary physical variables:

- enstrophy mean;
- dissipation proxy \(2\nu(\mathrm{enstrophy}-2Q)\).

Primary controls:

- time and scale;
- outgoing overlap fraction;
- IoU;
- centroid/radius distance;
- feature similarity;
- branch/merge state.

The report includes ordinary rank association, time×scale-stratified
high-tail enrichment, and geometry-conditioned partial-rank association.

## Claim boundary

N1/N2 are graph-local controls. They cannot preserve exact new-pair voxel
overlap because the ROUTE-I run does not contain source masks. Field-level
surrogates remain a later control.
