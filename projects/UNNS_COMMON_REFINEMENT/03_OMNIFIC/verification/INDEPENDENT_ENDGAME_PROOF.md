# Independent Endgame Reconstruction

## Claim

Let \(R\) be a commutative monoid with zero, cancellative away from zero.

Assume:

\[
\forall a\in R,\quad \operatorname{IsPrimal}(a).
\]

Then \(R\) has four-factor refinement.

## Proof

Take

\[
ab=cd.
\]

### Zero case

If \(a=0\), then

\[
cd=0.
\]

With no zero divisors, either \(c=0\) or \(d=0\).

If \(c=0\), choose

\[
e=0,\qquad f=d,\qquad g=b,\qquad h=1.
\]

Then

\[
a=ef=0,\qquad
b=gh=b,\qquad
c=eg=0,\qquad
d=fh=d.
\]

The case \(d=0\) is symmetric.

### Nonzero case

Assume

\[
a\neq0.
\]

From

\[
ab=cd
\]

we have

\[
a\mid cd.
\]

Since \(a\) is primal, there exist \(e,f\) such that

\[
a=ef,
\qquad
e\mid c,
\qquad
f\mid d.
\]

Choose \(g,h\) with

\[
c=eg,
\qquad
d=fh.
\]

Then

\[
ab
=
cd
=
(eg)(fh)
=
(ef)(gh)
=
a(gh).
\]

Since \(a\neq0\), cancellation gives

\[
b=gh.
\]

Therefore

\[
a=ef,\qquad
b=gh,\qquad
c=eg,\qquad
d=fh.
\]

So \(R\) has four-factor refinement.

\[
\Box
\]

## Comparison with the audited repository

This reconstruction matches the generic theorem

```text
hasFourFactorRefinement_of_decompositionMonoid
```

and its equivalence

```text
hasFourFactorRefinement_iff_forall_isPrimal
```

in `ConwayRefinement/Algebra/Divisibility/Refinement.lean`.

The reconstruction was done independently at the mathematical level.

A separate local Lean compilation was not possible in the current execution environment because
Lean/Lake are not installed there.
