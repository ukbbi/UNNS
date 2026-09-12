# GRAMMAR_FREEZE_v001

## Purpose

This folder is the canonical output record for the **freeze stage** of the
UNNS Multi-Clock Recurrence research program.

It records the point at which the compact multi-clock temporal grammar

\[
D_{2clk} ightarrow [P_{src}; J_{frac} \mid M_{frac}]
\]

was made immutable **before any prospective unseen candidate/control campaign**.

The separate physical extension is:

\[
+\,C_{coll}
\]

No prospective data were used in selecting or freezing this grammar.

C003 remained excluded throughout the freeze.

---

## Frozen status

**Grammar:** `MC_GRAMMAR_v001`  
**Status:** `FROZEN`  
**Stage:** `freeze`  
**Next stage:** `prospective unseen candidate/control`

From this point onward, any change to the representation, thresholds, nulls,
robustness rules, supported domain, or state logic requires a **new grammar version**.

`MC_GRAMMAR_v001` must not be adjusted to accommodate future data.

---

## Frozen temporal grammar

### Domain

`D_2clk`

The chart requires:

- exactly two externally specified incommensurate source clocks;
- a genuine time-domain observable/state trajectory;
- the source-clock ratio obtained from external metadata only;
- no response-derived clock;
- no inverse-FFT or synthetic time-domain reconstruction used as evidence.

### Empirically supported ratio domain

Version `v001` is empirically qualified only on the **golden-ratio branch**.

A legitimate two-clock trajectory with another irrational ratio must therefore be
reported as:

`OUTSIDE_EMPIRICALLY_QUALIFIED_RATIO_DOMAIN`

rather than being treated as a negative temporal result.

---

## Frozen coordinates and gates

### `P_src` — source-torus anchor

Metric:

`JPR_parent_gain`

Null model:

`PHASE_LABEL_PERMUTE`

Frozen gate:

`p_upper <= 0.10`

If this fails:

`SOURCE_UNANCHORED`

No raw parent-magnitude threshold is used.

---

### `J_frac` — fractional joint-phase chart coordinate

Metric:

`JPR_cover_advantage`

Definition:

`max(JPR(d=2,3,4)) - JPR(d=1)`

`J_frac` is always reported but is **not a hard admission gate**.

It describes whether recurrence is organized more strongly on a fractional
joint-phase cover than on the integer parent torus.

---

### `M_frac` — primary temporal decision coordinate

Metric:

`FC_frac_mixed_gain`

Frozen raw gate:

`M_frac >= 0.12`

Frozen hard null:

`FOURIER_PHASE`

Frozen null gate:

`p_upper <= 0.10`

The raw `M_frac >= 0.12` condition must also remain satisfied under every
frozen robustness transformation.

---

## Frozen robustness suite

The following transformations are immutable in `MC_GRAMMAR_v001`:

- temporal-origin shift;
- clock exchange;
- coordinatewise affine state transformation;
- ×5 downsampling;
- first 75% of the trajectory;
- additive noise with sigma = 0.02 × standard deviation.

Failure of the raw `M_frac` gate under any frozen transformation yields:

`MIXED_ORGANIZATION_UNSTABLE`

---

## Frozen temporal states

The grammar evaluates states in this precedence order:

1. `OUTSIDE_CHART_DOMAIN`
2. `OUTSIDE_EMPIRICALLY_QUALIFIED_RATIO_DOMAIN`
3. `SOURCE_UNANCHORED`
4. `MIXED_ORGANIZATION_WEAK`
5. `MIXED_ORGANIZATION_SPECTRAL_NULL`
6. `MIXED_ORGANIZATION_UNSTABLE`
7. `TEMPORAL_CORE_SUPPORTED`

All applicable failure flags are retained in the machine-readable outputs.

---

## Collective / physical extension

`C_coll` remains a separate source-native physical evidence interface.

No universal cross-platform collective scalar was invented.

Permitted annotations are:

- `COLLECTIVE_NOT_ASSESSED`
- `COLLECTIVE_EVIDENCE_UNAVAILABLE`
- `COLLECTIVE_EVIDENCE_AVAILABLE_FOR_DOMAIN_SPECIFIC_REVIEW`

The collective annotation does not alter the frozen temporal state.

---

# Files in this folder

## `FROZEN_GRAMMAR.json`

Complete machine-readable representation of `MC_GRAMMAR_v001`.

Contains:

- domain contract;
- coordinate definitions;
- frozen gates;
- null procedures;
- robustness settings;
- supported ratio domain;
- state vocabulary;
- prospective firewall;
- dependency hashes.

This is the principal machine-readable freeze artifact.

---

## `STATE_LOGIC.json`

Defines the frozen temporal-state evaluation order and conditions.

Use this file to audit how a future candidate/control result is mapped to one of
the frozen temporal states.

---

## `FREEZE_MANIFEST.json`

Dependency and provenance manifest for the freeze.

Records hashes of the method-selection, representation-study, and
grammar-development artifacts on which the frozen grammar depends.

Its purpose is to prove that the prospective campaign is using the same
pre-prospectively frozen method.

---

## `FREEZE_AUDIT.json`

High-level audit of the freeze operation.

Confirms that:

- the compact grammar had already been selected;
- the grammar was frozen at this stage;
- no prospective data were used;
- thresholds were not changed from selection;
- representations were not changed;
- nulls were not changed;
- robustness rules were not changed;
- the supported ratio domain was not changed;
- C003 was not loaded.

---

## `FREEZE_SHA256.txt`

Hash receipt for the freeze-critical files.

Use this file to verify that the frozen grammar, state logic, evaluator
dependencies, and protocol artifacts have not changed.

---

## `DEVELOPMENT_FREEZE_REPLAY.json`

Compact audit summary of the development-corpus replay under the frozen logic.

This is **not validation**.

Its purpose is only to confirm that the frozen implementation reproduces the
selection-stage behavior before prospective testing begins.

---

## `DEVELOPMENT_REPLAY_REFERENCE.csv`

Full development replay reference table inherited from compact-grammar selection.

Contains the candidate clauses and coordinate values for the known development records.

It is preserved as a reference checkpoint and must not be treated as prospective evidence.

---

## `DEVELOPMENT_REPLAY_SUMMARY.csv`

Role-level summary of the development replay.

At freeze, the known development corpus reproduced:

- DTQC positives: `4/4 TEMPORAL_CORE_SUPPORTED`
- Luo LOW controls: `0/2 supported`
- Luo HIGH controls: `0/2 supported`
- Malz-Smith topological non-DTQC controls: `0/6 supported`
- Malz-Smith trivial non-DTQC controls: `0/6 supported`

Again, this is a consistency replay, not external validation.

---

## `DEVELOPMENT_STATE_REPLAY.csv`

Record-by-record replay using the final frozen temporal-state vocabulary.

Shows the exact frozen state assigned to every development record.

This file is useful for auditing *why* a control fails rather than merely whether
it fails.

---

## `DEVELOPMENT_STATE_SUMMARY.csv`

Summary of frozen-state outcomes by development role.

The controls fail through physically meaningful structural states such as:

- `SOURCE_UNANCHORED`
- `MIXED_ORGANIZATION_WEAK`

No additional post-selection rule was introduced to force control rejection.

---

# Interpretation discipline

This folder marks the transition from **development** to **prospective testing**.

Everything before this folder may inform the grammar.

Everything after this folder must test the grammar.

The prospective campaign is therefore forbidden from changing:

- the chart domain;
- the golden-ratio support limitation;
- the JPR definition;
- the FC mixed-gain definition;
- cover depths;
- CV rules;
- null models;
- surrogate counts;
- null gates;
- the `M_frac >= 0.12` boundary;
- robustness transformations;
- temporal-state vocabulary;
- state precedence.

If any of those must change, the result is not a modification of
`MC_GRAMMAR_v001`; it is a new grammar version.

---

# Research-chain position

```text
development corpus                         ✓
initial representation bake-off            ✓
promising fractional/source-torus dev.      ✓
independent specificity challenge           ✓
full cross-representation study             ✓
nulls + robustness + control discrimination ✓
select compact grammar                      ✓
freeze                                      ✓  ← THIS FOLDER
prospective unseen candidate/control        ← NEXT
reveal
finally C003
```

---

## Critical firewall

**C003 must remain untouched until the prospective candidate/control analysis has been
completed, quantitatively locked, and revealed.**

Only after that reveal may C003 be evaluated under the unchanged
`MC_GRAMMAR_v001`.

That final test is what can determine whether a state historically invisible to the
integer-depth grammar becomes visible in the independently developed multi-clock grammar.
