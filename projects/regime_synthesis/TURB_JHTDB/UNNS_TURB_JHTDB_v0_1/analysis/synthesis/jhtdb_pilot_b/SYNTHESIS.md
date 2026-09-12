# JHTDB Pilot B — Final Replication Synthesis

**Project:** `UNNS_TURB_JHTDB_v0_1`  
**Pilot:** `jhtdb_pilot_b`  
**Record:** `JHTDB_PILOT_B_SYNTHESIS v0.1`  
**Status:** `FINAL_REPLICATION_SYNTHESIS`  
**Created UTC:** `2026-09-07T22:11:59+00:00`

## 1. Final outcome

The preregistered Pilot-B replication is complete.

**Final classification: `STRUCTURAL PARTIAL REPLICATION`.**

Pilot B independently reproduces the central route-mechanism result of Pilot A:

- `CONSTRAINED_ROUTING` under the frozen ROUTE-I null;
- an exceptionally low real scale–time stitching defect D□;
- survival of that low defect under the distance-controlled N1 null;
- survival under the harder distance + feature-controlled N2 null;
- substantive `D_STITCH` connectivity in STRUC-PERC-I;
- restructuring localization through significant scale and time branching contrasts.

It does **not** reproduce the complete Pilot-A cross-chamber/localization signature:

- STRUC-I `D_STITCH` falls from Pilot A's `Geometric Persistence` to Pilot B's `Structural Boundary` (**R3 fail**);
- the preregistered upper-decile physical-intensity localization does not replicate (**R7 fail**).

The result must therefore remain a partial replication rather than be promoted to core replication.

## 2. Independent physical sample

Pilot B uses the same broad `isotropic1024coarse` forced-isotropic setting but a disjoint physical sample:

| Property | Pilot A | Pilot B |
|---|---|---|
| spatial cube, 1-based | x/y/z `1:256` | x/y/z `513:768` |
| stored frames | `1:10` | `501:510` |
| physical time | `0.000–0.018` | `1.000–1.018` |
| spatial overlap | — | `0` grid points with Pilot A |
| frame overlap | — | `0` frames with Pilot A |
| source SHA-256 | `e32c9225...08a46` | `977e6ab3...b969f` |

Pilot B source size is `2,015,302,728` bytes and its frozen selection hash is `385cca0a...a40875e`.

The same frozen physical adapter and analysis grammar were used. Pilot B produced `10,515` objects and `14,169` relation candidates.

## 3. Primary ROUTE-I result

Pilot B returns:

**`CONSTRAINED_ROUTING`**

with:

- 100/100 nulls accepted;
- mean null mobility `0.998859`;
- 100 unique null graphs;
- real-graph match fraction `0`;
- supportive tests `2/3`;
- opposing tests `0`.

Primary metrics:

| Metric | Real | Null mean | p_favorable | Interpretation |
|---|---:|---:|---:|---|
| scale persistence | `0.346636` | `0.346954` | `0.742574` | not significant |
| time persistence | `0.500681` | `0.488256` | `0.00990099` | supported |
| D□ | `0.0141716` | `0.996336` | `0.00990099` | strongly supported |

The `[1,2,4,8]` sensitivity run also returns `CONSTRAINED_ROUTING`; factor 16 is therefore not required for the qualitative route result.

## 4. Cross-chamber result

### STRUC-I

| Ladder | Final mean Aκ | Regime | Replication role |
|---|---:|---|---|
| `D_STITCH` | `0.851863` | **Structural Boundary** | R3 **FAIL** |
| `P_TIME` | `0.598235` | Structural Instability | descriptive |
| `P_SCALE` | `0.564837` | Structural Instability | descriptive |

`D_STITCH` is `0.078137` below the 0.93 Geometric-Persistence boundary, so the frozen boundary-adjacent precision rule does not call for a 10,000-MC D_STITCH rerun. The completed 10,000-MC precision check was appropriately applied only to boundary-adjacent `P_TIME`.

### STRUC-PERC-I

| Ladder | Verdict | Gap vertices | Giant ratio | Isolated |
|---|---|---:|---:|---:|
| `D_STITCH` | **FULL_PERCOLATION** | `336` | `1.000000` | `0` |
| `P_TIME` | FULL_PERCOLATION | `9` | `1.000000` | `0` |
| `P_SCALE` | FULL_PERCOLATION | `3` | `1.000000` | `0` |

`D_STITCH` therefore passes the substantive R4 condition decisively.

## 5. Harder mechanism null hierarchy

STITCH-MECH independently reproduces real D□ = `0.014171635400793336` and returns:

**`SURVIVES_LOCAL_GEOMETRY_CONTROL`**

| Level | Mean D□ | real/null ratio | z_fav | p_fav | Quality |
|---|---:|---:|---:|---:|---|
| N0 | `0.9963363977` | `0.014224` | `868.885` | `0.00990099` | frozen ROUTE-I control |
| N1 | `0.3262040048` | `0.043444` | `98.8741` | `0.00990099` | PASS |
| N2 | `0.2114516957` | `0.067021` | `35.9661` | `0.00990099` | PASS |
| REAL | `0.0141716354` | — | — | — | — |

N1 quality:

- 100 unique graphs;
- mean mobility `0.044413`;
- real-graph match fraction `0`;
- no quality flags.

N2 quality:

- 100 unique graphs;
- mean mobility `0.014257`;
- real-graph match fraction `0`;
- no quality flags.

Thus R5 and the principal mechanism target R6 both pass.

## 6. Frozen R1–R8 outcome

| ID | Pilot B | Key basis |
|---|---|---|
| R1 | **PASS** | `CONSTRAINED_ROUTING`, usable primary nulls |
| R2 | **PASS** | real D□ << N0, p_fav `0.00990099` |
| R3 | **FAIL** | `D_STITCH` = Structural Boundary, mean Aκ `0.851863` |
| R4 | **PASS** | giant ratio `1.0`, `336` gap vertices, `0` isolated |
| R5 | **PASS** | N1 usable; real << N1, p_fav `0.00990099` |
| R6 | **PASS** | N2 usable; real << N2, p_fav `0.00990099` |
| R7 | **FAIL** | both frozen tail enrichments `1.0`, p `1.0` |
| R8 | **PASS** | scale and time branching significant |

Formal classification:

**`STRUCTURAL PARTIAL REPLICATION`**

## 7. Direct Pilot A ↔ Pilot B comparison

The Pilot-A column below maps the frozen Pilot-A baseline onto the later preregistered R1–R8 definitions for direct comparison; it is not a claim that Pilot A itself was prospectively preregistered under those labels.

| ID | Pilot A baseline | Pilot B replication | Comparison |
|---|---|---|---|
| R1 | **PASS** — `CONSTRAINED_ROUTING` | **PASS** — `CONSTRAINED_ROUTING` | route verdict replicates |
| R2 | **PASS** — real `0.0266275` vs N0 `0.996786`, p `0.00990099` | **PASS** — real `0.0141716` vs N0 `0.996336`, p `0.00990099` | primary stitching contrast replicates |
| R3 | **PASS** — Aκ `0.971708`, Geometric Persistence | **FAIL** — Aκ `0.851863`, Structural Boundary | cross-chamber admissibility does not replicate |
| R4 | **PASS** — giant `0.996933`, gaps `652`, isolated `0` | **PASS** — giant `1.0`, gaps `336`, isolated `0` | substantive connectivity replicates |
| R5 | **PASS** — N1 `0.329091`, p `0.00990099` | **PASS** — N1 `0.326204`, p `0.00990099` | distance-controlled survival replicates |
| R6 | **PASS** — N2 `0.223649`, p `0.00990099` | **PASS** — N2 `0.211452`, p `0.00990099` | harder mechanism target replicates |
| R7 | **PASS** — enstrophy `2.50×`, dissipation `1.87×`, both p≈`0.000200` | **FAIL** — both `1.0×`, p=`1.0` | tail localization does not replicate |
| R8 | **PASS** — branching + time merging + any restructure | **PASS** — scale + time branching | restructuring localization replicates in narrower form |

## 8. Quantitative comparison of the stitching hierarchy

| Quantity | Pilot A | Pilot B | B relative to A |
|---|---:|---:|---:|
| REAL D□ | `0.0266275` | `0.0141716` | **46.8% lower** |
| N0 mean | `0.996786` | `0.996336` | `0.045%` lower |
| N1 mean | `0.329091` | `0.326204` | `0.88%` lower |
| N2 mean | `0.223649` | `0.211452` | `5.45%` lower |
| N1 / REAL | `12.36×` | `23.02×` | larger separation in B |
| N2 / REAL | `8.40×` | `14.92×` | larger separation in B |

This descriptive comparison is notable: the independent null hierarchy remains numerically close between pilots while the real Pilot-B stitching defect is substantially smaller. The strongest replicated feature is therefore not a fragile threshold effect; it is the persistence of an exceptionally low real D□ relative to similarly placed constrained null ensembles.

## 9. Physical localization: replicated and non-replicated parts

Pilot A's high-D□ tail was strongly enriched in both physical-intensity measures. Pilot B does not reproduce that frozen tail result.

Pilot B has:

- D□ 90th percentile = `0`;
- `3962` eligible objects;
- frozen nominal top-D selection = all `3962` objects;
- enstrophy enrichment `1.0`, p `1.0`;
- dissipation enrichment `1.0`, p `1.0`.

This is a genuine R7 failure under the preregistration. It also exposes a tie-resolution limitation of the frozen quantile selector in a sample whose D□ distribution has a very large atom at zero. No alternative tail definition is introduced after seeing the result.

At the same time, continuous geometry-conditioned associations remain positive:

| Partial rank | Pilot A | Pilot B |
|---|---:|---:|
| ρ(D□, enstrophy | controls) | `0.17902` | `0.102725` |
| ρ(D□, dissipation | controls) | `0.12005` | `0.049360` |

These are weaker in Pilot B and remain descriptive rather than substitutes for R7.

## 10. Restructuring localization

Pilot A showed significant elevated D□ for scale branching, time branching, time merging, and any restructuring. Pilot B retains significant localization specifically at branching:

- scale branching: p `0.00019996`;
- time branching: p `0.00019996`;
- scale merging: p `1.0`;
- time merging: p `1.0`;
- any restructuring: p `1.0`.

The replicated statement should therefore be narrower than the Pilot-A statement:

> **Scale–time noncommutation remains preferentially localized around branching events, but Pilot B does not reproduce Pilot A's broader merging/aggregate restructuring localization.**

## 11. Scientific interpretation

The independent sample establishes a strong reproducible core of the Pilot-A route mechanism:

> **A very low scale–time stitching defect reappears in a spatially and temporally disjoint turbulent sample and survives both distance-constrained and distance-plus-feature-constrained graph-local nulls.**

The replication is not complete. Two components are sample-sensitive under the frozen protocol:

1. the scalar `D_STITCH` ladder does not cross the STRUC-I Geometric-Persistence threshold in Pilot B;
2. the frozen upper-decile physical-intensity localization does not survive the zero-heavy Pilot-B D□ distribution.

This separates two questions that Pilot A alone could not distinguish:

- **route-mechanism reproducibility:** strongly supported;
- **full cross-chamber/localization signature reproducibility:** not established.

The strongest current two-pilot picture is therefore:

> **A reproducible largely commuting scale–time route regime, with sample-dependent scalar admissibility strength and sample-dependent localization details of the rare noncommuting population.**

## 12. Claim boundary

Established across the two independent forced-isotropic samples:

- `CONSTRAINED_ROUTING` reappears;
- the real D□ is far below N0 in both;
- low real D□ survives N1 in both;
- low real D□ survives N2 in both;
- N1/N2 pass frozen quality gates in both;
- substantive `D_STITCH` gap connectivity appears in both;
- branching-associated elevated D□ appears in both.

Not established across both pilots:

- STRUC-I Geometric Persistence of `D_STITCH`;
- upper-decile physical-intensity enrichment under the frozen selector;
- time-merging or aggregate restructuring localization;
- Reynolds-number generality;
- generality beyond forced isotropic turbulence;
- survival under a field-level surrogate that preserves newly evaluated exact voxel overlap/IoU;
- equivalence of D□ breakdowns with a standard intermittency observable.

N1/N2 remain graph-local controls, not exact field-level overlap-preserving surrogates.

## 13. Frozen conclusion and next decision

Pilot B is now frozen as observed. It must not be replaced by another cutout under the same label.

The protocol's next decision point is whether the R3 and R7 divergences justify a separately preregistered **Pilot C**. That decision should be made from this frozen two-pilot comparison, not by altering Pilot B or retuning the existing thresholds.
