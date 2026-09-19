# UNNS Admissibility–Percolation

**Folder:** `UNNS_ADMISSIBILITY_PERCOLATION`

**Intended repository path:** `UNNS/projects/UNNS_ADMISSIBILITY_PERCOLATION/`

**Parent corpus source:** `UNNS_COMMON_REFINEMENT`

## Purpose

This project studies the relation between two distinct UNNS structural notions:

1. **perturbative admissibility**, measured by STRUC-I v1.0.4;
2. **gap-space percolative connectivity**, measured by STRUC-PERC-I v2.5.0.

The common-refinement / factor-traceability results are not what these chambers measure.
They provide an independently characterized algebraic corpus that can be used as a controlled
test bed.

The project was therefore renamed from the provisional
`UNNS_TRACEABILITY_PHENOTYPE` framing after the STRUC-I run and a closer functional audit of
both chambers.

The rename changes the **interpretive scope**, not the frozen data, chamber code, adapter,
or completed STRUC-I result.

## Central research question

> How are perturbative structural admissibility and percolative connectivity related for the same ordered ladders, and what additional structure is revealed when those ladders come from algebraically different systems?

A second, explicitly external comparison is:

> Do independently known algebraic route-closure properties correlate with either chamber result, without being confused with the chamber definitions themselves?

## Chamber roles

### STRUC-I v1.0.4 — Universal Ladder Admissibility

STRUC-I asks whether perturbations of an ordered ladder remain inside its allowed inversion budget.

Its core test is:

```text
inv(P_epsilon ; L) <= nu(V_epsilon(L))
```

At each scale, STRUC-I estimates:

```text
A_kappa(L)
=
fraction of perturbations satisfying the admissibility inequality
```

Its native taxonomy is:

```text
Geometric Persistence
Structural Boundary
Structural Instability
```

The chamber also reports structural pressure:

```text
rho = mean inversion load / vulnerability budget
```

but `rho` is explicitly a **secondary analytic** and does not replace the core admissibility
classification.

### STRUC-PERC-I v2.5.0 — Full PRP Percolation Analyzer

STRUC-PERC-I works on the ladder gap vector.

Vertices are gaps `Delta_i`. A full pairwise vulnerability graph is built with edges whenever:

```text
abs(Delta_i - Delta_j) <= epsilon
```

with:

```text
epsilon = kappa * IQR(Delta)
```

and median-gap fallback when IQR is zero.

Its native outcomes are:

```text
FULL_PERCOLATION
GIANT_COMPONENT_PERCOLATION
TAIL_FRAGMENTATION
HARD_FRAGMENTATION
```

The chamber tracks giant-component ratio, isolated vertices, connectivity threshold,
fragmentation, tail dominance, and adaptive large-kappa extension.

Its own logic distinguishes two directions:

```text
HARD_FRAGMENTATION
    -> established necessary-direction USL violation
```

whereas the sufficient direction from percolation to admissibility remains open.

`TAIL_FRAGMENTATION` is explicitly treated as inconclusive rather than as automatic structural
failure.

## Important scale distinction

The chambers do not use the same scale normalization:

```text
STRUC-I:
epsilon = kappa * median(gaps)

STRUC-PERC-I:
epsilon = kappa * IQR(gaps)
with median fallback when IQR = 0
```

Therefore this project does **not** assume point-by-point equality of their kappa axes.

The comparison is primarily structural and verdict-level unless a separately justified scale
alignment is introduced later.

## Frozen corpus

The retained corpus contains 30 systems, six in each class:

```text
INT_FREE
R1_FREE
R1_FAIL
AFF_FREE
AFF_FAIL
```

The corpus still carries the machine labels:

```text
TRACEABLE
NON_TRACEABLE
```

because those labels were assigned before any chamber run and are part of the frozen provenance.

In this renamed project they are interpreted correctly as **independent algebraic annotations**,
not as STRUC-I or STRUC-PERC-I target classes.

## Frozen primary encoding

Each system is represented by one label-blind 128-level `SYSTEM_SPECTRUM`.

The exact construction remains frozen in:

`adapters/ADAPTER_SPEC.md`

That document retains the provisional earlier project name because it is part of the preregistered
hash set and must not be rewritten after the first chamber run.

See:

`PROTOCOL_AMENDMENT_001.md`
`RENAME_RECORD.md`

## Current status

**STRUC-I COMPLETE — STRUC-PERC-I v2.5.0 RAW RETAINED — AUDIT/REPAIR v2.5.1 READY**

STRUC-I was run on the frozen grouped input:

`inputs/struc_i/ALL_SYSTEM_SPECTRA.csv`

Raw output is retained under:

`outputs/struc_i/`

The completed run contains:

- 30 ladders;
- 128 levels per ladder;
- 40 kappa steps;
- 2000 Monte Carlo perturbations per step;
- no subsampling.

### STRUC-I result

All 30 ladders were classified:

```text
Geometric Persistence
Stable Structure
```

with:

```text
mean_Ak = 1.0
min_Ak  = 1.0
```

So, for this frozen corpus and encoding, every system is perturbatively admissible under the
STRUC-I criterion.

This includes both algebraically route-closed and algebraically route-defective systems.

That result is important:

> Algebraic route closure and STRUC-I perturbative admissibility are not the same structural property.

The secondary `rho` diagnostic varies across ladders, but the completed STRUC-I run does not support
interpreting it as a monotone algebraic traceability score.

## What STRUC-PERC-I now tests

Because STRUC-I found universal admissibility in this corpus, the STRUC-PERC-I stage becomes
especially informative.

The next questions are:

- Do all 30 admissible ladders also percolate?
- Are some admissible ladders only giant-component or tail-fragmented?
- Does any original, non-downsampled ladder reach `HARD_FRAGMENTATION`?
- If so, does that create a cross-chamber inconsistency requiring an audit of assumptions,
  representation, or theorem applicability?
- If all ladders percolate, how much variation remains in connectivity thresholds and
  fragmentation signatures?


## Completed percolation audit

STRUC-PERC-I Audit v2.5.1 has now been run in the browser on the same frozen 30 inputs.

All 30 runs completed and all 30 eventually reached full connectivity under the exact-threshold
audit.

That final binary result must be interpreted carefully: explicitly probing the exact connectivity
threshold makes eventual connectivity expected for a finite full-pairwise threshold graph.

The informative output is therefore `kappa_connect_exact`.

Across this corpus it ranges from `0` to `15.073646`.

The cleanest repeated contrast is rank one:

```text
R1_FREE: kappa_connect_exact = 0  for 6/6
R1_FAIL: kappa_connect_exact = 1  for 6/6
```

Both classes remain fully admissible under STRUC-I.

## Pilot conclusion

The first experiment is complete.

The two chambers are compatible but non-identical:

- STRUC-I core admissibility is saturated at full admissibility for all 30 ladders.
- Exact percolation connectivity difficulty varies substantially.
- That connectivity scale is not globally ordered by algebraic route-closure status.

Canonical synthesis:

`outputs/synthesis/ADMISSIBILITY_PERCOLATION_SYNTHESIS.md`

A future experiment should be separately preregistered around a bounded-scale, exact-threshold, or
component-growth percolation observable.
