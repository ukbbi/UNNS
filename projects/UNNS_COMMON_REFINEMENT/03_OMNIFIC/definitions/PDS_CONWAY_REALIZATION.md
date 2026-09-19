# PDS–Conway Realization Audit

## Source state

Repository: `gaearon/conway-refinement`

Audited commit:

`264445c93b78554c408e99e4e7f663693b4e91ab`

## Result

At the level of mathematical proof architecture, the candidate Conway development realizes all
four PDS roles without the mismatches found in SRS.

This is a **source-level realization audit**, not a Lean formalization of the abstract PDS record.

---

# F — Base Primality

PDS:

\[
\operatorname{Base}(x)\Rightarrow\operatorname{IsPrimal}(x).
\]

Realization:

`isPrimal_of_supportArchimedeanClasses_finite`

and the `hfinite` hypothesis supplied to

`isPrimal_of_finite_classes_and_limit_tail_conditions`.

The base predicate is:

\[
\operatorname{Base}(x)
\equiv
\text{support of }x\text{ meets finitely many Archimedean classes}.
\]

### Audit

\[
\boxed{\text{PASS}}
\]

---

# Q — Local Quotient Refinement

PDS:

For a nonzero non-base \(x\) and an equation

\[
xd=bc,
\]

there exists a local structural refinement certificate.

Realization:

`exists_closed_class_refinement_at_support_class`.

At infinite support-class rank, the support is split into a limit initial segment and finite final
segment.  Common-tail quotient completeness plus the tail fraction-field hypothesis produce an
exact four-factor refinement at a quotient Archimedean class met by the support.

The deeper local engine is:

`exists_closed_class_refinement_of_complete_tail_quotient`.

### Audit

\[
\boxed{\text{PASS}}
\]

Importantly, this is where Cauchy completeness belongs.

It is not an inverse-limit witness axiom.

---

# D — Strict Residual Descent

PDS:

\[
\rho(w)<\rho(x).
\]

Realization:

`exists_factor_with_smaller_support_class_orderType`.

The rank used in `LimitTailPrimality.lean` is explicitly

\[
\rho(x)
=
\operatorname{orderType}
(\text{nonzero support Archimedean classes of }x).
\]

Factoring at the chosen quotient class gives

\[
x=t\,w
\]

with strictly smaller rank for \(w\).

### Audit

\[
\boxed{\text{PASS}}
\]

---

# T — Ambient Transport

PDS:

The local certificate must become ambient factors

\[
x=tw,\qquad
t=ef,\qquad
e\mid b,\qquad
f\mid c.
\]

Realization occurs in two linked steps.

First:

`exists_factor_with_smaller_support_class_orderType`

produces the retained factor \(t\) and residual \(w\).

Second:

`exists_factor_refinement_of_closed_class_refinement`

transports the quotient-class refinement into the ambient integer part and gives a factorization
of \(t\) whose two factors divide the corresponding ambient right-hand factors.

Then the generic lemma

`exists_primalRefinement_of_factor_refinement`

splices this ambient local refinement with primality of \(w\).

### Audit

\[
\boxed{\text{PASS}}
\]

The splice itself is generic algebra, not a separate PDS axiom.

---

# Global theorem realization

`isPrimal_of_finite_classes_and_limit_tail_conditions`

is the concrete Conway-side realization of the PDS induction theorem.

Its proof:

1. defines the support-class order-type rank;
2. uses well-founded ordinal induction;
3. invokes finite-class primality in the finite case;
4. produces exact local quotient refinement in the infinite case;
5. factors off a retained block;
6. obtains a lower-rank residual;
7. invokes the induction hypothesis on that residual;
8. splices the local refinement and residual primality.

This is PDS nearly clause-for-clause.

The final omnific file then proves:

\[
\forall a,\operatorname{IsPrimal}(a)
\]

for the signed bounded Hahn integer part, installs a `DecompositionMonoid`, invokes the generic
four-factor-refinement theorem, and transports through signed normal form.

---

# Verdict

\[
\boxed{
\text{PDS realization: PASS at source-architecture level}
}
\]

with one qualification:

> The repository does not define a structure literally named `PrimalDescentSystem`, so this is a
> mathematical realization audit, not a machine-checked Lean instance of our abstract definition.

That is substantially stronger and more faithful than the earlier SRS correspondence.
