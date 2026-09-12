# JHTDB Pilot B — Preregistered Replication Protocol

**Project:** `UNNS_TURB_JHTDB_v0_1`  
**Replication:** `jhtdb_pilot_b`  
**Protocol version:** `0.1`  
**Status:** `PREREGISTERED — NO PILOT-B RESULT SEEN`  
**Reference baseline:** JHTDB Pilot A synthesis v0.2

## 1. Purpose

Pilot B is an independent replication test of the structural regime identified in Pilot A.

The Pilot-A working result is:

\[
\boxed{
\text{a largely commuting scale–time route regime with localized noncommuting breakdowns}
}
\]

The purpose of Pilot B is **not** to discover a new configuration that produces the same result.

It is to test whether the Pilot-A signature reappears when the physical sample changes while the analysis protocol remains frozen.

The central replication question is:

> **Does an independent JHTDB sample reproduce the same scale–time structural organization under the frozen Pilot-A pipeline?**

---

## 2. Independence requirement

A sample may be called **Pilot B** only if it is physically independent of the Pilot-A sample to the extent supported by the available source.

Preferred replication:

1. same JHTDB forced-isotropic regime;
2. same cutout dimensions;
3. different spatial cutout;
4. zero spatial overlap with the Pilot-A cube;
5. preferably a non-overlapping time window as well.

If only a new time subset of the same spatial cube is available, label it:

`jhtdb_pilot_a_internal_time`

not Pilot B.

If only a spatial subdivision of the existing Pilot-A cube is used, label it:

`jhtdb_pilot_a_internal_space`

not Pilot B.

The replication record must store the extraction coordinates, time indices, and an explicit independence statement before analysis begins.

---

## 3. Frozen scientific pipeline

Pilot B must use the same scientific pipeline as Pilot A.

### 3.1 Physical adapter

Canonical adapter:

`tools/derive/JHTDB_ROUTE_ADAPTER_v0_1_0/`

Rules frozen from Pilot A:

- same velocity-field interpretation;
- same boundary-safe derivative treatment;
- no periodic wrapping of the extracted subcube;
- same object-definition and segmentation logic;
- same relation-construction logic;
- same source/derived-data separation;
- same physical variables and meanings.

The exact numerical adapter settings must be taken from the preserved Pilot-A adapter configuration/report files. They are **not to be reconstructed from memory** and are not to be retuned after Pilot-B data are inspected.

### 3.2 Multiscale ladder

Frozen scale factors:

\[
[1,2,4,8,16].
\]

No factor may be removed from the primary Pilot-B run because of the Pilot-B result.

The `[1,2,4,8]` analysis remains a predefined sensitivity test only.

### 3.3 STRUC-ROUTE-I

Canonical chamber:

`chambers/STRUC_ROUTE_I_v0_1_2/`

Use the same:

- relation eligibility rules;
- route-weight interpretation;
- persistence definitions;
- scale–time stitching definition;
- 100-null primary ensemble;
- null-quality logic;
- significance threshold;
- export structure.

Route entropy remains descriptive-only under the endpoint-rewiring null.

Primary route endpoint:

\[
D_{\square}
=
JSD(ST,TS)/\ln 2.
\]

### 3.4 Route-derived ladders

Use the same deterministic extraction definitions as Pilot A:

- `D_STITCH`
- `P_TIME`
- `P_SCALE`

Rules:

- duplicates preserved;
- no deduplication;
- no jitter;
- no smoothing;
- no normalization;
- no rescaling;
- full stored numeric precision;
- deterministic ordering only.

### 3.5 STRUC-I

Canonical chamber:

`chambers/STRUC_I_v1_0_4/`

Primary replication run:

- canonical chamber settings;
- 2,000 Monte Carlo perturbations;
- unchanged κ range and κ steps;
- unchanged maximum ladder size;
- deterministic chamber subsampling where required.

Precision rule preregistered before Pilot-B analysis:

> If any ladder's mean \(A_\kappa\) lies within **0.01** of a STRUC-I regime boundary, repeat that ladder at **10,000 MC runs** without changing any other setting.

This rule is a precision check only and does not replace the canonical 2,000-MC result.

### 3.6 STRUC-PERC-I

Canonical chamber:

`chambers/STRUC_PERC_I_v2_5_0/`

Use the canonical chamber unchanged.

Record both:

- formal verdict;
- number of gap vertices after the chamber's generic deduplication.

Percolation of `P_TIME` or `P_SCALE` must again be marked low-dimensional/descriptive if exact-value quantization collapses the gap graph strongly.

### 3.7 STITCH-MECH

Canonical mechanism instrument:

`tools/analyze/STITCH_MECH_v0_1_1/`

Use the frozen N0/N1/N2 definitions.

N0:

- frozen ROUTE-I degree-preserving endpoint-rewiring control.

N1:

- degree/layer-preserving endpoint swaps;
- distance-stratified within physical transition groups.

N2:

- all N1 constraints;
- additional feature-similarity stratification.

Frozen STITCH-MECH quality gates:

- minimum mean mobility fraction: `0.01`;
- minimum unique-graph fraction: `0.10`;
- maximum real-graph match fraction: `0.90`.

Frozen N1/N2 ensemble size:

- 100 nulls each.

Frozen high-\(D_{\square}\) tail:

- upper 10%.

Frozen physical scaling used only for the dissipation proxy:

\[
\nu=0.000185.
\]

No N1/N2 constraint may be relaxed after Pilot-B results are seen.

---

## 4. Primary replication criteria

Pilot B is evaluated criterion-by-criterion. No weighted composite score is used.

### R1 — Route organization

STRUC-ROUTE-I returns a usable primary inference with:

`CONSTRAINED_ROUTING`

and the null ensemble passes its quality checks.

### R2 — Primary stitching contrast

The real mean \(D_{\square}\) is significantly lower than N0 in the preregistered favorable direction.

Required:

\[
p_{fav}<0.05.
\]

The real value, null mean, ratio, z-score, and empirical p-value must all be reported.

### R3 — Cross-chamber admissibility

`D_STITCH` is classified by STRUC-I as:

`Geometric Persistence`

at the canonical 2,000-MC run or at the preregistered 10,000-MC precision check if boundary-adjacent.

A stronger persistence state also counts as replication.

### R4 — Cross-chamber connectivity

`D_STITCH` forms a substantive STRUC-PERC-I connected regime.

Preregistered substantive condition:

- giant-component ratio \(\ge 0.95\);
- at least 100 gap vertices after deduplication;
- zero or negligible isolation must be reported rather than silently ignored.

### R5 — Distance-controlled survival

N1 is usable under the frozen quality gates and:

\[
D_{\square}^{real}<D_{\square}^{N1}
\]

with:

\[
p_{fav}<0.05.
\]

### R6 — Distance + feature-controlled survival

N2 is usable under the frozen quality gates and:

\[
D_{\square}^{real}<D_{\square}^{N2}
\]

with:

\[
p_{fav}<0.05.
\]

R6 is the principal mechanism replication target.

---

## 5. Secondary localization criteria

These are secondary replication tests. They do not override R1–R6.

### R7 — Physical-intensity localization

The upper 10% \(D_{\square}\) tail is tested for enrichment in:

- upper 10% enstrophy;
- upper 10% dissipation proxy.

Report:

- overlap fraction;
- random expected fraction;
- enrichment;
- time×scale-stratified permutation p-value.

A replicated positive localization has:

- enrichment \(>1\);
- \(p<0.05\).

### R8 — Restructuring localization

Repeat the frozen branch/merge contrasts for:

- scale branching;
- time branching;
- scale merging;
- time merging;
- any restructuring.

Report every test, including null results.

A replicated restructuring association requires at least one preregistered flag class to show higher \(D_{\square}\) in the restructuring group with \(p<0.05\).

---

## 6. Replication interpretation

Do not collapse the result into a weighted score.

Report every R1–R8 item independently.

For concise project language:

### Core replication

Use **CORE REPLICATION** only if R1–R6 all pass.

### Structural partial replication

Use **STRUCTURAL PARTIAL REPLICATION** if R2 passes and at least one of R5 or R6 passes, but one or more cross-chamber conditions fail.

### Route-only replication

Use **ROUTE-ONLY REPLICATION** if R1 and R2 pass but both N1/N2 mechanism survival criteria fail or are underresolved.

### No replication

Use **NO REPLICATION** if R2 fails under a usable N0 ensemble.

An underresolved N1 or N2 must be reported as `UNDERRESOLVED`, not converted into failure or success.

---

## 7. Pre-analysis freeze

Before collecting or opening Pilot-B derived results:

1. place this protocol in the project;
2. run `LOCK_PROTOCOL.bat`;
3. preserve `FREEZE_SHA256.txt` and `FREEZE_RECORD.json`;
4. record the Pilot-B source acquisition coordinates/time indices;
5. calculate the source-file SHA-256;
6. write `SOURCE_RECORD.json`;
7. only then run the physical adapter.

The freeze hashes the actual local copies of:

- Pilot-B preregistration files;
- JHTDB physical adapter;
- STRUC-ROUTE-I;
- STRUC-I;
- STRUC-PERC-I;
- STITCH-MECH;
- Pilot-A synthesis v0.2.

If any frozen instrument changes afterward, Pilot B must either:

- use the original frozen copy; or
- increment the replication protocol version and explicitly restart preregistration.

---

## 8. Prohibited post-result changes

After Pilot-B data are inspected, do not:

- retune segmentation thresholds;
- change scale factors in the primary run;
- change relation thresholds;
- alter the number or definition of primary nulls;
- change favorable directions;
- alter STRUC-I regime thresholds;
- change STRUC-PERC-I connectivity rules;
- relax N1/N2 binning or mobility gates;
- redefine the high-\(D_{\square}\) tail;
- change which physical variables count as the primary intensity tests;
- discard an unfavorable run and substitute another extraction under the same Pilot-B label.

Any exploratory modification must be given a new analysis label and kept separate from the preregistered Pilot-B result.

---

## 9. Required outputs

### Source

`data/raw/jhtdb/pilot_b/`

Must contain or reference:

- physical source file;
- `SOURCE_RECORD.json`;
- source checksum;
- extraction-coordinate/time record.

### Derived objects

`data/derived/objects/jhtdb_pilot_b/`

### ROUTE-I

`outputs/exports/struc_route_i/jhtdb_pilot_b/`

### Route ladders

`ladders/route_i/jhtdb_pilot_b/`

### STRUC-I

`outputs/exports/struc_i/jhtdb_pilot_b/`

### STRUC-PERC-I

`outputs/exports/struc_perc_i/jhtdb_pilot_b/`

### STITCH-MECH

`analysis/mechanism/jhtdb_pilot_b/`

and:

`outputs/tables/pilot_b/`

### Final replication synthesis

`analysis/synthesis/jhtdb_pilot_b/`

The final synthesis must include a direct Pilot-A versus Pilot-B comparison table for R1–R8.

---

## 10. Stopping rule

Pilot B is a single preregistered physical replication sample.

Do not keep sampling new cutouts until one reproduces Pilot A.

If Pilot B fails, freeze the failed result first.

Only afterward may Pilot C be defined as a new preregistered replication.

---

## 11. Scientific interpretation boundary

Pilot B tests reproducibility within the same broad JHTDB forced-isotropic setting.

Even a full Pilot-B replication would not by itself establish universality across all turbulent flows.

A successful Pilot B would justify the next step:

- a third independent realization and/or
- a different Reynolds-number regime and/or
- a different turbulence class.

---

## 12. Replication target

The full Pilot-A signature to be tested is:

\[
\boxed{
\text{commuting scale–time organization}
+
\text{localized physically intense / restructuring-linked breakdowns}
}
\]

The decisive question is whether this signature reappears **without changing the inference machinery after seeing the new data**.
