# Primal Descent System (PDS)

## Why PDS exists

The source-level audit of the candidate Conway proof showed that the transfinite machinery is
organized around **primality of every element**, not around direct recursive construction of
four-factor witnesses.

The generic algebraic endpoint is:

\[
\forall x,\ \operatorname{IsPrimal}(x)
\iff
\text{four-factor refinement}.
\]

A **Primal Descent System (PDS)** abstracts the recursive mechanism used to prove the left-hand side.

This is a different abstraction from SRS.  SRS remains valid in its own category.

---

# 1. Ambient algebra

A PDS is built over a commutative monoid with zero \(M\) satisfying cancellation away from zero.

For \(x,b,c\in M\),

\[
\operatorname{IsPrimal}(x)
\]

means:

\[
x\mid bc
\Longrightarrow
\exists x_1,x_2,\quad
x=x_1x_2,\quad
x_1\mid b,\quad
x_2\mid c.
\]

This is the pre-Schreier / decomposition-monoid notion used in the candidate proof.

---

# 2. Structural rank

The system has an ordinal-valued rank

\[
\rho:M\to\mathrm{Ord}.
\]

It also has a base predicate

\[
\operatorname{Base}(x).
\]

The intended interpretation is:

- base objects are handled by a finite/local theorem;
- non-base objects are reduced to a complementary factor of strictly smaller rank.

---

# 3. Local certificates

For every nonzero, non-base \(x\), and every product equation

\[
xd=bc,
\]

the PDS has a type/set of **local quotient certificates**

\[
\mathcal Q(x;b,c,d).
\]

The certificate itself may live in a quotient, germ, graded, local, or otherwise simplified
structural domain.

Crucially, a local certificate is **not** yet an ambient primality witness.

---

# 4. Transport data

Every local certificate \(q\in\mathcal Q(x;b,c,d)\) can be transported back to ambient data

\[
t,w,e,f\in M
\]

such that

\[
x=tw,
\]

\[
t=ef,
\]

\[
e\mid b,
\qquad
f\mid c.
\]

Here:

- \(t\) is the retained/local block;
- \(w\) is the residual factor;
- \(e,f\) are the ambient factors supplied by transport of the local refinement.

This is the exact algebraic configuration needed for the generic splicing lemma.

---

# The four PDS axioms

## F — Base Primality

\[
\boxed{
\operatorname{Base}(x)
\Longrightarrow
\operatorname{IsPrimal}(x).
}
\]

This is the finite-class theorem in the Conway realization.

---

## Q — Local Quotient Refinement

For every

\[
x\ne0,
\qquad
\neg\operatorname{Base}(x),
\qquad
xd=bc,
\]

there exists at least one local certificate

\[
q\in\mathcal Q(x;b,c,d).
\]

`Q` says that the difficult global product equation can always be resolved at some appropriate
local/quotient structural site.

Any completeness, fraction-field, cofinality, or local polynomial hypotheses belong to the
**realization of Q**, not to the abstract PDS theorem.

---

## D — Strict Residual Descent

For the residual \(w\) produced from every transported local certificate,

\[
\boxed{
\rho(w)<\rho(x).
}
\]

This is the well-founded engine of the transfinite recursion.

---

## T — Ambient Transport

Every local certificate transports to ambient factors

\[
t,w,e,f
\]

with

\[
x=tw,
\qquad
t=ef,
\qquad
e\mid b,
\qquad
f\mid c.
\]

The subsequent splice with primality of \(w\) is a generic algebraic lemma of cancellative
commutative monoids with zero; it does not need to be an extra PDS axiom.

---

# Why there is no separate L axiom

The Conway audit showed that Cauchy completeness is not used as an inverse-limit theorem on
witness sets.

Instead, completeness is one of the concrete hypotheses that makes `Q` true:

\[
\text{common-tail completeness}
\Longrightarrow
\text{exact local quotient refinement}.
\]

Therefore PDS places the limit-stage analytic/topological work inside the local-certificate
existence mechanism `Q`.

This is faithful to the audited proof architecture.

---

# Why there is no irreducible-to-prime axiom

The target of the recursion is already stronger:

\[
\forall x,\operatorname{IsPrimal}(x).
\]

Once every element is primal, four-factor refinement follows generically.

Irreducible \(\Rightarrow\) prime is then an important consequence in suitable atomic settings,
but it is not required as the load-bearing premise of PDS.

---

# Minimal PDS data summary

A PDS therefore consists of:

\[
(M,\rho,\operatorname{Base},\mathcal Q)
\]

together with the four axioms

\[
\boxed{F,Q,D,T}.
\]

The theorem file proves:

\[
F+Q+D+T
\Longrightarrow
\forall x,\operatorname{IsPrimal}(x)
\Longrightarrow
\text{four-factor refinement}.
\]
