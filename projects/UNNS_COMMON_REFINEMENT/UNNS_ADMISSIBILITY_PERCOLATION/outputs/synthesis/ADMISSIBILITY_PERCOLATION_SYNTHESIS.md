# Admissibility–Percolation Pilot Synthesis

## Status

**PILOT SYNTHESIS COMPLETE**

This synthesis combines:

- STRUC-I v1.0.4;
- the original STRUC-PERC-I v2.5.0 batch;
- STRUC-PERC-I Audit v2.5.1;
- the unchanged frozen 30-system corpus.

No frozen chamber or preregistered input was altered.

## 1. Corrected question

The project asks:

> How are perturbative structural admissibility and gap-space percolative connectivity related on
> the same ordered ladders?

The algebraic route-closure labels carried by the source corpus are independent annotations, not
definitions of either chamber observable.

## 2. STRUC-I result

All 30 ladders are fully admissible under the tested STRUC-I protocol:

```text
regime  = Geometric Persistence
state   = Stable Structure
mean_Ak = 1.0
min_Ak  = 1.0
```

The STRUC-I core classification is therefore saturated across this corpus.

## 3. Original STRUC-PERC-I v2.5.0 result

The frozen original batch produced:

```text
25 FULL_PERCOLATION
 4 HARD_FRAGMENTATION
 1 TAIL_FRAGMENTATION
```

Those raw verdicts are retained.

The subsequent audit showed that the five non-full outcomes were sensitive to search horizon,
adaptive stopping, or an effective-zero-IQR issue.

## 4. STRUC-PERC-I Audit v2.5.1 result

The browser audit run reports:

```text
30 / 30 COMPLETE
30 / 30 final FULL_PERCOLATION
```

and supplies an exact normalized connectivity threshold for every ladder.

But this final binary result is not itself discriminating.

For a finite set of gap values, the full pairwise threshold graph necessarily connects once the
threshold reaches the maximum adjacent separation in the sorted gap-value set.

Because v2.5.1 explicitly probes that scale, eventual full connectivity is expected by construction.

The informative percolation observable is therefore:

```text
kappa_connect_exact
```

not the eventual yes/no verdict.

## 5. Main cross-chamber result

Across the frozen corpus:

```text
STRUC-I:
    30 / 30 fully admissible

STRUC-PERC-I Audit:
    30 / 30 eventually connected

exact connectivity scale:
    ranges from 0 to 15.073646
```

Therefore perturbative admissibility and percolative connectivity should not be collapsed into a
single binary structural property.

STRUC-I is saturated at full admissibility, while the exact percolation scale retains substantial
variation.

## 6. Rank-one result

The cleanest repeated distinction is rank one.

For all six free rank-one controls:

```text
kappa_connect_exact = 0
```

For all six nonfree rank-one controls:

```text
kappa_connect_exact = 1
```

Both classes nevertheless have:

```text
STRUC-I mean_Ak = 1
STRUC-I min_Ak  = 1
```

Thus the same perturbative admissibility can coexist with a different exact gap-graph connectivity
scale.

In the retained rank-one corpus, the free/nonfree algebraic distinction aligns perfectly with this
connectivity-scale contrast.

That alignment should not be generalized beyond rank one without further evidence.

## 7. Higher-rank result

The affine controls do not preserve the same algebraic ordering.

```text
AFF_FREE:
    median kappa_connect_exact = 3.132993
    mean   kappa_connect_exact = 5.793710

AFF_FAIL:
    median kappa_connect_exact = 2.474745
    mean   kappa_connect_exact = 3.224702
```

The traceable affine class is not uniformly easier to connect than the non-traceable affine class.

So this pilot does not support a global monotone law of the form:

```text
more algebraic route closure
    -> lower percolation threshold
```

The positive-integer controls also span a broad exact-threshold range:

```text
min    = 1.269950
median = 5.138617
max    = 10.412395
```

## 8. Structural interpretation

The strongest justified statement is:

> **Perturbative admissibility and percolative connectivity are compatible but non-identical
> diagnostics.**

In this pilot:

- no ladder violates STRUC-I admissibility;
- every finite gap graph is eventually connectable under the exact-threshold audit;
- the exact connectivity scale varies strongly;
- that scale carries structural information absent from STRUC-I's saturated core classification;
- the connectivity scale does not globally reduce to the algebraic route-closure annotation.

The two chambers are therefore not redundant.

## 9. Limitation revealed by the audit

An unbounded binary question:

```text
Does this finite full-pairwise threshold graph eventually percolate?
```

is weak as a discriminator, because sufficiently large kappa eventually forces connectivity for
finite gap sets with positive scale normalization.

A future experiment should preregister a nontrivial percolation observable such as:

```text
exact connectivity threshold
connectivity within a fixed finite kappa horizon
component-growth profile
tail/outlier structure before connectivity
```

before examining new data.

## 10. Pilot endpoint

The first `UNNS_ADMISSIBILITY_PERCOLATION` experiment is complete.

Its endpoint is:

```text
STRUC-I:
    universal perturbative admissibility

STRUC-PERC-I v2.5.0:
    original bounded/adaptive search record retained

STRUC-PERC-I Audit v2.5.1:
    exact eventual connectivity threshold retained for every case

cross-chamber conclusion:
    admissibility and percolation are compatible but structurally non-identical;
    connectivity scale is the informative percolation variable in this corpus.
```
