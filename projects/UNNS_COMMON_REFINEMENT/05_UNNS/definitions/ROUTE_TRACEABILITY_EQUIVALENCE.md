# Route-Traceability Equivalence

## Purpose

The decisive comparative synthesis of the integer, non-refinement, affine, and omnific branches
identifies the same algebraic property behind every successful refinement regime.

The property is **primality of elements**, equivalently the pre-Schreier / decomposition-monoid
condition when it holds globally.

In UNNS language this is **factor traceability**.

This is not a new algebraic equivalence; it is the exact structural identification needed by this
project.

---

# 1. Local factor traceability

Let \(M\) be a commutative cancellative monoid.  For \(a\in M\), define:

\[
\operatorname{Trace}(a)
\]

to mean that whenever

\[
a\mid cd,
\]

there exist \(e,f\in M\) such that

\[
a=ef,\qquad e\mid c,\qquad f\mid d.
\]

This is exactly the standard definition that \(a\) is **primal**.

Thus:

\[
\boxed{
\operatorname{Trace}(a)
\iff
\operatorname{IsPrimal}(a).
}
\]

The term "traceability" is therefore not an analogy: it is a structural reading of a standard
divisibility property.

---

# 2. Equality-local form

Fix a nonzero \(a\).

Then the following are equivalent:

1. \(a\) is primal.
2. Every equality
   \[
   ab=cd
   \]
   with \(a\) as the distinguished first factor admits a four-factor refinement
   \[
   a=ef,\qquad b=gh,\qquad c=eg,\qquad d=fh.
   \]

## Proof: primality -> local refinement

From

\[
ab=cd
\]

we have

\[
a\mid cd.
\]

If \(a\) is primal, write

\[
a=ef,\qquad e\mid c,\qquad f\mid d.
\]

Choose

\[
c=eg,\qquad d=fh.
\]

Then

\[
ab=(ef)b=(eg)(fh)=efgh.
\]

Cancellation of nonzero \(a=ef\) gives

\[
b=gh.
\]

Hence the exact refinement square exists.

## Proof: local refinement -> primality

Suppose

\[
a\mid cd.
\]

Choose \(b\) with

\[
ab=cd.
\]

By the assumed local refinement property,

\[
a=ef,\qquad c=eg,\qquad d=fh.
\]

Therefore

\[
e\mid c,\qquad f\mid d,
\]

so \(a\) is primal.

Thus:

\[
\boxed{
a\text{ primal}
\iff
\text{every route equality through }a\text{ is refinable}.
}
\]

This is the exact local meaning of **route traceability**.

---

# 3. Global form

A commutative cancellative monoid has global four-factor refinement exactly when every element is
primal.

For a commutative monoid with zero, the same equivalence holds under cancellation away from zero,
with the zero case handled separately.

Therefore:

\[
\boxed{
\text{Global Route Closure}
\iff
\forall a,\operatorname{Trace}(a)
\iff
\forall a,\operatorname{IsPrimal}(a).
}
\]

In ring terminology the global condition is the pre-Schreier / decomposition-monoid property.

This is the surviving algebraic law across the successful regimes studied in this project.

---

# 4. What the law does NOT say

The law does not require:

- a gcd algorithm;
- unique factorization;
- finite atomic structure;
- lattice saturation;
- support-class ranks;
- Archimedean stratification;
- transfinite descent.

Those are **mechanisms that can establish traceability in particular domains**.

The law itself is simply:

\[
\boxed{
\text{factor traceability}
\iff
\text{four-factor route closure}.
}
\]

---

# 5. Domain-specific mechanisms

## Positive integers

Traceability is established by the gcd/coprime argument:

\[
e=\gcd(a,c),\quad a=ef,\quad c=eg,\quad \gcd(f,g)=1,
\]

and the product equality forces

\[
g\mid b,\qquad f\mid d.
\]

So the familiar integer refinement proof is already a proof that every positive integer is primal.

## Rank-one additive monoids

For \(H\subseteq\mathbb N_0\), refinement is equivalent to primality of the least positive atom.

The project criterion

\[
H=m\mathbb N_0
\]

is therefore a rank-one realization of global factor traceability.

## Positive affine monoids

In the finite affine case, atomicity reduces global traceability to primality of atoms.

The project equivalence

\[
\text{refinement}
\iff
\text{every atom prime}
\iff
H\cong\mathbb N_0^r
\]

is an affine realization of the same law.

## Omnific candidate proof

The candidate proof takes the global traceability condition as its actual transfinite target:

\[
\forall a,\operatorname{IsPrimal}(a).
\]

Finite-class primality is extended to arbitrary support-class order type using:

\[
\text{local quotient refinement}
+
\text{retained-block factorization}
+
\text{strict rank descent}
+
\text{ambient transport/splicing}.
\]

Once global primality is established, four-factor refinement follows by the generic algebraic
equivalence.

---

# 6. UNNS conclusion

The structural quantity that survives from ordinary integers to the candidate omnific proof is:

\[
\boxed{\text{factor traceability}.}
\]

The implementation changes radically.

The invariant does not.

The project should therefore distinguish:

\[
\boxed{\text{law}}
\qquad\text{from}\qquad
\boxed{\text{mechanism establishing the law}}.
\]

The law is global primality / traceability.

The integer mechanism is gcd/coprime routing.

The affine mechanism is atomic independence / prime atoms.

The omnific mechanism is transfinite local-refinement descent and transport.
