# PROTOCOL AMENDMENT 001

## Status

**INTERPRETIVE AMENDMENT AFTER STRUC-I, BEFORE STRUC-PERC-I**

Date: 2026-09-19

This amendment does not replace or alter the frozen `PROTOCOL.md`.

## Reason for amendment

The original preregistered framing asked whether exact algebraic traceability status had a
perturbative/percolative phenotype.

After completing the STRUC-I run and then auditing the actual functional scope of both chambers, the
project framing was corrected.

The chambers do not classify algebraic traceability:

- STRUC-I measures ordered-ladder perturbative admissibility.
- STRUC-PERC-I measures gap-space percolative connectivity.
- traceability/common refinement belongs to the external algebraic provenance of the corpus.

The project is therefore renamed:

`UNNS_ADMISSIBILITY_PERCOLATION`

## What remains frozen

This amendment changes none of the following:

- 30-system corpus;
- case membership;
- algebraic labels;
- `SYSTEM_SPECTRUM` construction;
- 128-point ladder length;
- STRUC-I input;
- STRUC-PERC-I inputs;
- STRUC-I v1.0.4 chamber file;
- STRUC-PERC-I v2.5.0 chamber file;
- completed STRUC-I raw outputs.

The frozen protocol and adapter remain byte-preserved.

## Revised principal question

The principal question for the remainder of the branch is:

> How does full-gap percolative connectivity relate to independently measured perturbative
> admissibility on the same frozen ordered ladders?

The algebraic route-closure labels are retained as secondary explanatory metadata.

## Cross-chamber logic to test

The comparison must respect the chamber's own logical asymmetry.

STRUC-PERC-I treats:

```text
HARD_FRAGMENTATION
    -> established necessary-direction USL violation
```

on original non-downsampled data.

By contrast, the sufficient direction:

```text
percolation
    -> admissibility
```

remains open.

`TAIL_FRAGMENTATION` is inconclusive rather than an automatic violation.

## Consequence of the completed STRUC-I run

STRUC-I found:

```text
30 / 30 ladders:
Geometric Persistence / Stable Structure
mean_Ak = min_Ak = 1.0
```

Therefore the STRUC-PERC-I run now has three particularly important possible outcomes.

### Outcome A — all or nearly all ladders percolate

This is cross-chamber consistent with universal STRUC-I admissibility.

It may support the open sufficient-direction picture on this corpus, but cannot prove it.

### Outcome B — tail fragmentation occurs

This remains compatible with the chamber's own inconclusive tier.

The relation to full admissibility must be analyzed descriptively.

### Outcome C — hard fragmentation occurs on an original ladder

This is the strongest audit case.

Because STRUC-I already found full admissibility for the same frozen ladder, a
`HARD_FRAGMENTATION` verdict would create a substantive cross-chamber tension that must be resolved
before any synthesis claim is made.

Possible audit targets would include:

- scale normalization differences;
- theorem scope;
- ladder representation assumptions;
- gap-graph interpretation;
- admissibility/percolation definitions.

No conclusion should be forced in advance.

## Scale caveat

The chambers use different epsilon normalizations:

```text
STRUC-I:
epsilon = kappa * median(gaps)

STRUC-PERC-I:
epsilon = kappa * IQR(gaps)
with median fallback when IQR = 0
```

Therefore no pointwise equality of kappa values is assumed.

The first synthesis is verdict- and profile-level, not a forced point-by-point scale matching.

## Integrity statement

This amendment was written after observing the STRUC-I result and before executing STRUC-PERC-I.

That timing must remain visible in the project record.
