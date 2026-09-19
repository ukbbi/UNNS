# PDS Global Primality and Route-Closure Theorem

## Theorem

Let \(M\) be a commutative monoid with zero, cancellative away from zero, equipped with a
Primal Descent System satisfying

\[
F,\ Q,\ D,\ T.
\]

Then every element of \(M\) is primal:

\[
\boxed{
\forall x\in M,\ \operatorname{IsPrimal}(x).
}
\]

Consequently \(M\) has the four-factor refinement property:

\[
\boxed{
ab=cd
\Longrightarrow
\exists e,f,g,h,
\quad
a=ef,\ b=gh,\ c=eg,\ d=fh.
}
\]

Thus

\[
\boxed{
F+Q+D+T
\Longrightarrow
\text{Global Primality}
\Longrightarrow
\text{Route Closure}.
}
\]

---

# Proof of global primality

We prove

\[
\operatorname{IsPrimal}(x)
\]

for every \(x\) by well-founded induction on

\[
\rho(x).
\]

Fix \(x\).

## Zero case

If

\[
x=0,
\]

then \(x\) is primal in the usual monoid-with-zero sense.

So assume

\[
x\ne0.
\]

## Base case

If

\[
\operatorname{Base}(x),
\]

axiom \(F\) gives

\[
\operatorname{IsPrimal}(x).
\]

## Non-base case

Assume

\[
\neg\operatorname{Base}(x).
\]

To prove \(x\) primal, take arbitrary \(b,c\in M\) with

\[
x\mid bc.
\]

Choose \(d\in M\) such that

\[
bc=xd.
\]

Equivalently,

\[
xd=bc.
\]

By \(Q\), there exists a local certificate

\[
q\in\mathcal Q(x;b,c,d).
\]

By \(T\), this certificate transports to

\[
t,w,e,f\in M
\]

satisfying

\[
x=tw,
\qquad
t=ef,
\qquad
e\mid b,
\qquad
f\mid c.
\]

By \(D\),

\[
\rho(w)<\rho(x).
\]

Hence the induction hypothesis gives

\[
\operatorname{IsPrimal}(w).
\]

Now use primality of \(w\) to split the residual factor through the remaining cofactors of
\(b\) and \(c\).

Because

\[
e\mid b,
\qquad
f\mid c,
\]

write

\[
b=eg,
\qquad
c=fh.
\]

Using

\[
x=tw=efw
\]

and the original product equation,

\[
xd=bc=(eg)(fh)=ef(gh),
\]

cancellation of the nonzero retained factor \(t=ef\) yields

\[
w\mid gh.
\]

Since \(w\) is primal, there exist

\[
w_1,w_2
\]

such that

\[
w=w_1w_2,
\qquad
w_1\mid g,
\qquad
w_2\mid h.
\]

Therefore

\[
x
=
efw
=
(ew_1)(fw_2),
\]

with

\[
ew_1\mid eg=b
\]

and

\[
fw_2\mid fh=c.
\]

So \(x\) is primal.

This closes the well-founded induction.

Hence

\[
\boxed{
\forall x,\operatorname{IsPrimal}(x).
}
\]

\[
\Box
\]

---

# From global primality to four-factor refinement

Take

\[
ab=cd.
\]

If \(a=0\), the zero-product case is handled directly.

Assume \(a\ne0\).

Since every element is primal, \(a\) is primal.

From

\[
a\mid cd
\]

obtain

\[
a=ef,
\qquad
e\mid c,
\qquad
f\mid d.
\]

Write

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

Cancellation of nonzero \(a\) gives

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

Thus the four-factor refinement property holds.

This is the same generic algebraic equivalence used in the audited Lean development.

---

# What the theorem says structurally

PDS identifies a different route to global refinement from SRS.

SRS says:

\[
\text{locally refinable ranked obligations}
\Longrightarrow
\text{global witnesses}.
\]

PDS says:

\[
\text{local quotient control}
+
\text{strict factor descent}
\Longrightarrow
\text{every element primal}
\Longrightarrow
\text{global refinement}.
\]

The two mechanisms need not be identified.

---

# Status

**THEOREM — proved inside the PDS axioms defined by this project.**

The source-level Conway realization is recorded separately.

No claim is made here that PDS is a novel theorem relative to all existing abstract factorization
theory.  The important project result is that PDS is a faithful abstraction of the audited
transfinite proof spine, unlike the earlier attempted SRS realization.
