# Elementwise Route-Closure Report

## Status

**Exact rank-one classification completed.**

This report follows `PRIMAL_REFINEMENT_CORRESPONDENCE.md`, which established:

```text
x primal
iff
every endpoint equality containing x is 2x2-refinable.
```

## New proved results

For a primitive numerical monoid `S` with conductor `c`:

1. **Gap localization**
   - a non-refinable equality `x+t=y+z` can occur only when `|x-y|` and `|x-z|` are gaps of `S`;
   - therefore every possible failure around a fixed `x` lies in a finite gap window.

2. **Cofinal primal tail**
   - every `x >= 4c` is primal;
   - after restoring the gcd scale `gamma`, every original element `x >= 4*gamma*c` is primal.

3. **Finite obstruction core**
   - all non-primal elements occur below the proved `4c` threshold;
   - therefore the full elementwise profile is exactly computable.

## Corpus

Source: `02_NONREF/output/rank1_generator_scan.csv`

```text
793 total systems
280 globally refinable
513 globally non-refinable
```

All 513 non-refinement systems were classified exactly below the proved tail bound.

Key results:

```text
414 / 513 (80.70%) failure systems contain early primal elements
median non-primal core size = 18
maximum non-primal core size = 130
exact tail onset / conductor:
    minimum = 2.1
    median  = 2.6666666667
    maximum = 3.5
proved universal tail bound = 4c
```

The ratio values are corpus observations. Only the `4c` bound is claimed as proved here.

## Flagship

For `H=<2,3>`:

```text
conductor c = 2
non-primal elements = 2,3,4,5
exact all-primal tail begins at 6
proved generic bound = 8
```

Thus a monoid can remain globally non-refinable even though every sufficiently large element is locally route-closed.

## Conway/UNNS significance

The comparison now separates three notions:

```text
elementwise primality
cofinal/effective prevalence of primality
global every-element primality
```

The rank-one failure systems can satisfy the second very strongly while failing the third because a finite obstruction core survives.

This sharpens the comparison with the audited omnific candidate proof. Support-class descent should not be interpreted merely as making "large" objects simple. Its decisive role is paired with base primality and transport so that no unresolved non-primal residual core remains.

## Reproducibility

Run:

```text
python scripts/BUILD_ELEMENTWISE_PROFILE.py
```

Generated:

```text
04_PROOF_MAP/output/RANK1_ELEMENTWISE_SUMMARY.csv
04_PROOF_MAP/output/RANK1_ELEMENTWISE_PROFILE.csv
outputs/records/RANK1_ELEMENTWISE_RESULT.json
```

Mathematical derivation and interpretation:

```text
04_PROOF_MAP/output/ELEMENTWISE_ROUTE_PROFILE.md
```

## Next

Apply the same elementwise question to the retained affine controls and determine whether higher-rank atomic relations produce an unbounded non-primal set rather than a finite obstruction core.
