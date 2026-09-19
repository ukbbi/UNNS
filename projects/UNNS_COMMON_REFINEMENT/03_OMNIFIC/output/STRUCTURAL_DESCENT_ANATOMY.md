# Structural Descent Anatomy

## Purpose

This document completes the original refinement-plan task of extracting the candidate Conway proof
as a structural descent mechanism rather than translating Lean lemmas one by one into UNNS language.

The analysis is tied to the audited public repository state:

```text
gaearon/conway-refinement
commit 264445c93b78554c408e99e4e7f663693b4e91ab
```

The proof remains treated here as a **candidate formal proof architecture**.  This document records
what the audited source actually does structurally.

The governing question is:

> **What structural property survives the transition from ordinary integers to omnific integers
> that keeps the refinement square admissible?**

The comparative synthesis has identified the answer as:

\[
\boxed{
\text{primal factor traceability}
}
\]

that is,

\[
\boxed{
\forall a,\operatorname{IsPrimal}(a).
}
\]

For a nonzero factor \(a\),

\[
a\mid cd
\]

must imply that \(a\) can be split as

\[
a=ef,
\]

with

\[
e\mid c,
\qquad
f\mid d.
\]

Under the cancellative hypotheses used by the project, this is equivalent to the four-factor
refinement property.

The purpose of the present document is narrower and more detailed:

> **How does the candidate omnific proof propagate this traceability through an infinite
> structural hierarchy?**

At every stage we answer four questions:

1. **What quantity becomes simpler?**
2. **What invariant survives?**
3. **What makes the next transition admissible?**
4. **What prevents a non-refinable branch?**

---

# 1. Baseline: the finite integer control

Before entering the omnific proof, recall the successful finite control.

For positive integers,

\[
ab=cd.
\]

Set

\[
e=\gcd(a,c),
\qquad
a=ef,
\qquad
c=eg,
\qquad
\gcd(f,g)=1.
\]

Then

\[
fb=gd.
\]

Coprimality forces

\[
g\mid b,
\qquad
f\mid d,
\]

so

\[
b=gh,
\qquad
d=fh.
\]

The refinement square follows.

The important point is that the **gcd is not the cross-domain invariant**.

It is the finite arithmetic mechanism proving the invariant:

\[
\boxed{
a\text{ is primal / factor-traceable}.
}
\]

This distinction between **law** and **mechanism** is essential throughout what follows.

---

# 2. Failure control: what a non-refinable branch looks like

In the additive monoid

\[
H=\langle2,3\rangle,
\]

the equality

\[
2+4=3+3
\]

has no refinement inside \(H\).

Structurally, the failure is:

\[
2\le_H 3+3,
\]

but

\[
2\nleq_H 3
\]

for either copy of \(3\).

Thus the atom \(2\) is not primal.

This gives the exact obstruction that the omnific proof must avoid:

\[
\boxed{
\text{a factor participates in the combined product but cannot be routed into either branch}.
}
\]

Every successful stage of the omnific proof must prevent this kind of unresolved routing failure.

---

# 3. Global omnific proof spine

The audited candidate proof has the following load-bearing architecture:

```text
finite support-class primality
    ↓
support-class stratification
    ↓
limit initial segment + finite final segment
    ↓
common-tail quotient
    ↓
exact local closed-class refinement
    ↓
retained-block factorization
    ↓
strict decrease of support-class order type
    ↓
primality of the residual by induction
    ↓
ambient transport of the local refinement
    ↓
splice local factor control with residual primality
    ↓
primality of the current element
    ↓
global pre-Schreier / decomposition-monoid structure
    ↓
four-factor refinement
    ↓
transport through signed normal form to omnific integers
```

The central induction theorem is:

```text
isPrimal_of_finite_classes_and_limit_tail_conditions
```

in:

```text
ConwayRefinement/HahnSeries/IntegerPart/LimitTailPrimality.lean
```

The final omnific theorem uses:

```text
signedSmallSupportIntegerPart_isPrimal
signedSmallSupportIntegerPart_decompositionMonoid
conwayRefinement
```

in:

```text
ConwayRefinement/Surreal/OmnificInteger/Refinement/ConwayRefinement.lean
```

---

# 4. Stage A — raw series to support geometry

## Structural move

The full Hahn-series element is not attacked globally.

The proof first reads the element through the geometry of its support and, specifically, through
the Archimedean classes met by its nonzero support.

The structural rank later used by the induction is:

\[
\rho(x)
=
\operatorname{orderType}
\bigl(
\text{nonzero support Archimedean classes of }x
\bigr).
\]

## What quantity becomes simpler?

A highly detailed infinite series is replaced by the ordered set of support classes it meets.

So the description changes from:

\[
\text{coefficients at individual exponents}
\]

to:

\[
\text{ordered support-class geometry}.
\]

The proof has compressed the object without discarding the hierarchy needed for recursion.

## What invariant survives?

The target property remains:

\[
\operatorname{IsPrimal}(x).
\]

The multiplicative/divisibility problem is not replaced by a different endpoint theorem.

Instead, support geometry becomes the organizing coordinate through which primality can be proved.

## What makes the next transition admissible?

The Hahn-series representation is multiplicative and the support-class machinery is compatible with
the underlying ordered exponent group.

This makes it meaningful to use support classes as structural coordinates for factorization.

## What prevents a non-refinable branch?

Nothing has yet been solved at this stage.

What has been gained is a structural measure capable of detecting genuine descent later.

The first protection against unresolved branching is therefore:

\[
\boxed{
\text{the problem has been placed inside a well-founded support hierarchy}.
}
\]

---

# 5. Stage B — support geometry to ordinal rank

## Structural move

The support-class set is assigned its order type:

\[
\rho(x)
=
\operatorname{orderType}
(\text{nonzero support Archimedean classes}).
\]

The proof then performs well-founded induction on this ordinal.

## What quantity becomes simpler?

The complicated support geometry is summarized by one ordinal rank.

The relevant simplification is not numerical smallness but:

\[
\boxed{
\text{strictly lower order type}.
}
\]

## What invariant survives?

Again, the induction statement is:

\[
\operatorname{IsPrimal}(x).
\]

At every ordinal rank the target is the same.

So the invariant propagated through the entire transfinite argument is factor traceability.

## What makes the next transition admissible?

Ordinals are well founded.

Therefore, if a factorization step can replace \(x\) by a residual \(w\) satisfying

\[
\rho(w)<\rho(x),
\]

the induction hypothesis becomes available.

## What prevents a non-refinable branch?

A branch cannot remain forever at equal or increasing structural complexity.

The decisive condition is:

\[
\boxed{
\rho(w)<\rho(x).
}
\]

This is the formal obstruction to uncontrolled infinite descent.

---

# 6. Stage C — finite support-class base regime

## Structural move

If the support meets only finitely many Archimedean classes, the proof does not invoke the full
limit-tail machinery.

It applies the finite-class primality theorem.

Relevant source-level theorem:

```text
isPrimal_of_supportArchimedeanClasses_finite
```

## What quantity becomes simpler?

The structural hierarchy terminates in a finite class configuration.

No transfinite residual step is needed.

## What invariant survives?

The same invariant appears directly:

\[
\operatorname{IsPrimal}(x).
\]

This finite theorem is the base layer from which the arbitrary-order-type result is extended.

## What makes the next transition admissible?

Finite support-class configurations satisfy the local algebraic hypotheses encoded in the finite
Archimedean-class machinery.

The proof can establish primality directly at this level.

## What prevents a non-refinable branch?

There is no unresolved lower-rank branch left.

The factor-routing property is proved outright.

This is the omnific analogue of reaching a regime where routing is already controlled.

---

# 7. Stage D — infinite support to limit initial segment plus finite final segment

## Structural move

At infinite support-class rank, the class set is decomposed into:

\[
T_0\cup T_1,
\]

where:

- \(T_0\) is a nonzero limit initial segment;
- \(T_1\) is finite.

This isolates the genuinely transfinite part of the support.

## What quantity becomes simpler?

The entire infinite support is separated into:

\[
\text{limit core}
+
\text{finite remainder}.
\]

The proof no longer needs to handle every support class symmetrically.

## What invariant survives?

The product equation and primality target remain intact.

The structural split is auxiliary; it does not weaken the required divisibility conclusion.

## What makes the next transition admissible?

The limit initial segment \(T_0\) has no least member in the relevant magnitude order, which is
exactly the setting required for the common-tail quotient construction.

Its cardinality is also controlled by the support bound.

## What prevents a non-refinable branch?

The infinite support is not permitted to remain an unstructured mass.

It is reorganized into a form from which a common tail and quotient can be defined.

Thus the next possible obstruction is localized rather than left globally unresolved.

---

# 8. Stage E — passage to the common-tail quotient

## Structural move

From the limit family of support classes, the proof forms a common tail and the corresponding
quotient of the exponent group.

The crucial hypotheses are:

- Cauchy completeness of the common-tail quotient;
- a fraction-field condition for the bounded Hahn integer part on the tail.

## What quantity becomes simpler?

The original exponent group is replaced by a quotient in which distinctions below the common tail
are collapsed.

This removes structural detail that is irrelevant to the current local refinement step.

## What invariant survives?

The local image of the product equation remains exact enough to support four-factor refinement.

The target is still to recover divisibility information relevant to the original ambient factors.

## What makes the next transition admissible?

This is where completeness matters.

Cauchy completeness is used as part of the mechanism that produces an exact refinement at an
appropriate quotient Archimedean class.

The fraction-field hypothesis ensures the required divisibility algebra in the tail setting.

Thus:

\[
\boxed{
\text{completeness is a local-refinement enabler}.
}
\]

It is not the global invariant.

## What prevents a non-refinable branch?

The quotient theorem does not merely produce an approximate compatibility.

It produces an exact refinement after restriction at a suitable closed Archimedean class.

So the local obstruction is removed before returning to the ambient domain.

---

# 9. Stage F — exact local closed-class refinement

## Structural move

For an equation

\[
xd=bc,
\]

the proof obtains an exact refinement at a quotient class met by the support of \(x\).

Relevant source-level machinery includes:

```text
exists_closed_class_refinement_at_support_class
exists_closed_class_refinement_of_complete_tail_quotient
```

## What quantity becomes simpler?

The global factorization problem is replaced by an exact refinement problem on one controlled
structural block.

## What invariant survives?

The crucial divisibility alignment survives:

the local refinement separates the retained part of \(x\) into pieces aligned with the \(b\) and
\(c\) branches.

This is local factor traceability.

## What makes the next transition admissible?

The selected quotient class is not arbitrary.

It is chosen from a class actually met by the support, so the retained block is nontrivial and
structurally relevant.

## What prevents a non-refinable branch?

The proof prevents the \(\langle2,3\rangle\)-type failure locally:

the retained factor is not merely known to divide the combined product.

It is explicitly split into factors assigned to the two branches.

So at this stage the local routing obstruction is solved.

---

# 10. Stage G — retained-block factorization

## Structural move

The proof factors:

\[
x=t\,w,
\]

where \(t\) is the retained block controlled by the chosen quotient class and \(w\) is the residual
factor.

Relevant theorem:

```text
exists_factor_with_smaller_support_class_orderType
```

## What quantity becomes simpler?

The original element \(x\) is replaced by a residual factor \(w\) with strictly smaller structural
rank:

\[
\rho(w)<\rho(x).
\]

This is the decisive descent step.

## What invariant survives?

The original factor \(x\) has not been discarded.

It is exactly decomposed as:

\[
x=t\,w.
\]

The routing information accumulated for \(t\) therefore remains available when the residual
problem is later solved.

## What makes the next transition admissible?

The support-class factorization theorem proves the strict rank inequality needed by ordinal
induction.

Without this strict inequality, the transfinite argument would not close.

## What prevents a non-refinable branch?

An unresolved residual cannot retain the full structural complexity of \(x\).

It must move to lower rank.

Thus any branch that still needs routing control is forced toward a regime already covered by the
induction hypothesis.

---

# 11. Stage H — induction on the residual factor

## Structural move

Because

\[
\rho(w)<\rho(x),
\]

the induction hypothesis gives:

\[
\operatorname{IsPrimal}(w).
\]

## What quantity becomes simpler?

The entire unresolved part of the current problem has been reduced from \(x\) to \(w\).

## What invariant survives?

Exactly the project’s central invariant:

\[
\boxed{
\text{factor traceability}.
}
\]

The induction hypothesis does not merely say that \(w\) is simpler.

It says that \(w\) already has the divisibility-routing property needed to finish the current
problem.

## What makes the next transition admissible?

The strict rank inequality is the only reason the induction hypothesis can be invoked.

## What prevents a non-refinable branch?

A residual factor cannot become an untraceable dead end.

By induction it is primal.

So any remaining divisibility through that residual can itself be split across the two branches.

---

# 12. Stage I — transport of the local refinement back to the ambient integer part

## Structural move

The quotient/local refinement is transported back to the ambient integer part.

Relevant theorem:

```text
exists_factor_refinement_of_closed_class_refinement
```

The result has the form:

\[
t=ef,
\qquad
e\mid b,
\qquad
f\mid c.
\]

## What quantity becomes simpler?

The local quotient data are replaced by ambient factors that can participate directly in the
original divisibility equation.

## What invariant survives?

The local routing relation survives transport:

\[
e\mid b,
\qquad
f\mid c.
\]

This is the crucial point.

The quotient was only a temporary structural coordinate system.

The divisibility information itself returns to the original domain.

## What makes the next transition admissible?

The transport theorem proves that the quotient-class factorization corresponds to a genuine
ambient factorization of the retained block.

## What prevents a non-refinable branch?

The proof does not permit a local refinement that exists only in the quotient but disappears when
lifted back.

Transport preserves enough exact factor information to continue in the ambient system.

---

# 13. Stage J — splice local control with residual primality

## Structural move

Now we have:

\[
x=t\,w,
\]

\[
t=ef,
\]

\[
e\mid b,
\qquad
f\mid c,
\]

and

\[
\operatorname{IsPrimal}(w).
\]

The generic algebraic splice theorem combines these data.

Relevant theorem:

```text
exists_primalRefinement_of_factor_refinement
```

## What quantity becomes simpler?

There is no further structural simplification.

This is the reconstruction step.

The separately solved local and residual pieces are recombined.

## What invariant survives?

Factor traceability survives both sides of the decomposition:

- \(t\) is locally routed;
- \(w\) is primal and therefore globally routable.

Together they prove:

\[
\operatorname{IsPrimal}(x).
\]

## What makes the next transition admissible?

Cancellation and primality of \(w\) permit the residual factor to be split through the remaining
cofactors of the two branches.

The algebraic splice is exact.

## What prevents a non-refinable branch?

There is nowhere left for unrouted factor content to hide.

The retained block is assigned branchwise, and the residual is itself traceable.

Therefore the current factor \(x\) becomes traceable.

This is the exact negation of the non-refinement obstruction.

---

# 14. Stage K — transfinite completion of primality

## Structural move

The ordinal induction closes:

\[
\forall x,\operatorname{IsPrimal}(x).
\]

## What quantity becomes simpler?

No quantity remains to be simplified.

All support-class ranks have been covered.

## What invariant survives?

The local invariant has become a global property:

\[
\boxed{
\text{every element is primal}.
}
\]

This is the pre-Schreier / decomposition-monoid condition.

## What makes the next transition admissible?

Well-founded induction guarantees that the proof covers every rank once the finite base and strict
descent steps are established.

## What prevents a non-refinable branch?

A non-refinable branch would require some element to fail primality.

But the induction has now established primality at every structural rank.

Thus no such branch remains in the bounded Hahn integer part.

---

# 15. Stage L — global primality to four-factor refinement

## Structural move

The generic algebraic equivalence is invoked:

\[
\boxed{
\forall a,\operatorname{IsPrimal}(a)
\iff
\text{HasFourFactorRefinement}.
}
\]

Relevant source:

```text
ConwayRefinement/Algebra/Divisibility/Refinement.lean
```

with theorems including:

```text
hasFourFactorRefinement_of_decompositionMonoid
hasFourFactorRefinement_iff_forall_isPrimal
```

## What quantity becomes simpler?

The proof no longer needs support geometry, quotient classes, or ordinal ranks.

All of that machinery has done its job.

The final problem is now pure algebra.

## What invariant survives?

The propagated invariant — primality — is converted directly into the target refinement square.

## What makes the next transition admissible?

Cancellation away from zero plus global primality is sufficient to construct:

\[
a=ef,\qquad
b=gh,\qquad
c=eg,\qquad
d=fh.
\]

## What prevents a non-refinable branch?

Global primality and global four-factor refinement are equivalent in this setting.

So once global primality is established, a non-refinable product equality is algebraically
impossible.

---

# 16. Stage M — transport to omnific integers

## Structural move

The signed normal-form equivalence identifies the relevant omnific-integer subring with the bounded
Hahn integer part.

The four-factor refinement property is transported across this equivalence.

Relevant theorem:

```text
conwayRefinement
```

## What quantity becomes simpler?

No structural simplification is performed here.

This is a representation transfer.

## What invariant survives?

The complete four-factor refinement property survives multiplicative equivalence.

## What makes the next transition admissible?

The signed normal-form map is a ring/multiplicative equivalence appropriate for transporting the
refinement property.

## What prevents a non-refinable branch?

Any alleged non-refinable omnific equality would transport to a non-refinable equality in the Hahn
integer-part model, contradicting its established refinement property.

---

# 17. Full four-question matrix

| Stage | What becomes simpler? | What invariant survives? | What makes the transition admissible? | What prevents a non-refinable branch? |
|---|---|---|---|---|
| Raw series → support geometry | coefficients → ordered support classes | primality target | multiplicative Hahn-series representation | places problem in a well-founded hierarchy |
| Support geometry → ordinal rank | support hierarchy → order type | primality target | well-founded ordinal order | unresolved residual must descend |
| Finite support-class regime | finite class structure | primality | finite-class theorem | routing solved directly |
| Infinite support split | whole infinite support → limit core + finite tail | product/divisibility relation | PWO decomposition of class set | infinite complexity localized |
| Common-tail quotient | exponent detail below tail is collapsed | exact local product relation | completeness + fraction-field hypothesis | local exact refinement becomes available |
| Closed-class refinement | global problem → one controlled block | local factor routing | selected class lies in support | retained block splits branchwise |
| Retained-block factorization | \(x\) → \(t\,w\) | exact factor identity | support factorization theorem | \(\rho(w)<\rho(x)\) |
| Residual induction | \(w\) lower rank | primality / traceability | induction hypothesis | residual cannot become an untraceable dead end |
| Ambient transport | quotient factors → ambient factors | branch divisibility | transport theorem | local solution cannot disappear on lifting |
| Splice | local + residual solutions → primality of \(x\) | factor traceability | cancellation + residual primality | no factor content remains unrouted |
| Transfinite completion | all ranks covered | global primality | well-founded induction | no rank escapes the proof |
| Primality → refinement | proof machinery disappears | route closure | pre-Schreier equivalence | non-refinable equality impossible |
| Hahn model → \(\mathbf{Oz}\) | representation changes | four-factor refinement | signed normal-form equivalence | counterexample would transport backward |

---

# 18. The invariant ladder

The original refinement plan asked whether the proof contains an invariant ladder underneath
refinement.

The answer is yes, but it is important to state the ladder correctly.

The **decreasing coordinate** is:

\[
\boxed{
\rho(x)
=
\operatorname{orderType}
(\text{nonzero support Archimedean classes}).
}
\]

The **preserved structural target** is:

\[
\boxed{
\operatorname{IsPrimal}(x).
}
\]

The architecture is therefore:

\[
\text{support geometry}
\]

\[
\downarrow
\]

\[
\text{support-class ordinal rank}
\]

\[
\downarrow
\]

\[
\text{local quotient control}
\]

\[
\downarrow
\]

\[
x=t\,w,
\qquad
\rho(w)<\rho(x)
\]

\[
\downarrow
\]

\[
w\text{ primal}
\]

\[
\downarrow
\]

\[
x\text{ primal}
\]

\[
\downarrow
\]

\[
\text{global route closure}.
\]

The crucial distinction is:

\[
\boxed{
\text{rank decreases, traceability survives}.
}
\]

---

# 19. What the proof is really preserving

It would be inaccurate to say that the candidate proof preserves a particular explicit refinement
witness through every level.

It does not.

What it preserves is the ability to **reconstruct factor routing** after structural simplification.

That is why primality is the correct invariant.

A factor may be:

- represented in a quotient;
- split into a retained block and residual;
- moved through an Archimedean class;
- handled at lower ordinal rank;

yet its divisibility content remains recoverable strongly enough to prove:

\[
a\mid bc
\Longrightarrow
a=a_1a_2,\quad a_1\mid b,\quad a_2\mid c.
\]

This is the precise algebraic meaning of structural route traceability.

---

# 20. What prevents the bad monoid phenomenon

The non-refinement control

\[
H=\langle2,3\rangle
\]

fails because a factor can participate in a combined route without admitting a branchwise split.

The omnific proof architecture repeatedly prevents exactly that situation.

At the controlled block:

\[
\text{exact local refinement}
\]

prevents local routing failure.

For the residual:

\[
\text{strict rank descent}
+
\text{inductive primality}
\]

prevents unresolved routing failure from persisting.

During lifting:

\[
\text{ambient transport}
\]

prevents the local solution from being lost.

During reconstruction:

\[
\text{primal splice}
\]

prevents the retained and residual pieces from becoming incompatible.

So the candidate proof does not avoid non-refinement through one single miraculous lemma.

It excludes it by a coordinated chain of structural safeguards.

---

# 21. Final answer to the four plan questions

## What quantity becomes simpler?

The decisive decreasing quantity is:

\[
\boxed{
\text{order type of the nonzero support Archimedean classes}.
}
\]

Local quotienting and block extraction also simplify the active factorization problem.

## What invariant survives?

\[
\boxed{
\text{primal factor traceability}.
}
\]

This is the structural property ultimately established at every rank.

## What makes the next transition admissible?

A sequence of exact mechanisms:

\[
\boxed{
\text{support stratification}
\rightarrow
\text{common-tail quotient control}
\rightarrow
\text{exact local refinement}
\rightarrow
\text{strict factor descent}
\rightarrow
\text{ambient transport}
\rightarrow
\text{primal splice}.
}
\]

## What prevents a non-refinable branch?

\[
\boxed{
\text{every unresolved residual is forced to lower rank while local factor routing is preserved
and reconstructible}.
}
\]

The residual eventually lies in a regime already known to be primal, and transport/splicing returns
that traceability to the original factor.

---

# 22. Completion of the original refinement plan

The original plan asked us to proceed in this order:

1. establish the ordinary-integer control;
2. construct genuine refinement failures;
3. identify the structural obstruction;
4. dissect the omnific proof by its structural descent;
5. determine the property that survives;
6. ask whether Conway refinement exemplifies a broader UNNS structural law.

Items 1–5 are now complete at the algebraic-structural level.

The resulting synthesis is:

\[
\boxed{
\text{domain-specific mechanism}
\Longrightarrow
\text{factor traceability}
\Longleftrightarrow
\text{common refinement}.
}
\]

The mechanisms differ:

\[
\mathbb N_{>0}:
\quad
\gcd+\text{coprimality}
\]

\[
\text{free affine systems}:
\quad
\text{prime atoms / independent coordinates}
\]

\[
\text{candidate omnific proof}:
\quad
\text{local quotient refinement}
+
\text{strict support-class descent}
+
\text{transport/splicing}.
\]

The invariant does not:

\[
\boxed{
\text{primal factor traceability}.
}
\]

This document therefore marks the formal completion of the structural-descent component of the
original refinement plan.

---

# 23. Status discipline

### Established within this project

- positive-integer refinement mechanism;
- exact non-refinement controls;
- rank-one and finite affine refinement classifications used by the project;
- source-level structural audit of the candidate Conway proof;
- cross-regime identification of primality with route traceability;
- stage-by-stage structural descent anatomy recorded here.

### Classical algebraic fact

The equivalence between global primality/pre-Schreier structure and four-factor refinement is not
claimed as a new theorem.

### Candidate-proof dependence

Statements about omnific integers depend on the audited candidate Lean development and should be
described as such unless and until independent mathematical review establishes the theorem outside
that candidate source.

### UNNS interpretation

The UNNS contribution at this stage is the structural reading:

\[
\boxed{
\text{rank decreases while route traceability survives}.
}
\]

That is the precise mechanism by which the candidate proof turns a highly stratified infinite
factorization problem into global structural route closure.
