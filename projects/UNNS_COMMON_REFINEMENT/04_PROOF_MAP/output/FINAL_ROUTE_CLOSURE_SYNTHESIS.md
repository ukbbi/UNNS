# Final Route-Closure Synthesis

## Common Refinement and Structural Route Closure in the UNNS Substrate

**Project:** `UNNS_COMMON_REFINEMENT`  
**Status:** cross-regime synthesis after integer, rank-one, affine, and Conway source-level analysis  
**Conway source lock:** `gaearon/conway-refinement` commit `264445c93b78554c408e99e4e7f663693b4e91ab`

---

# 1. Original question

The project began with the contrast between

\[
ab=cd
\]

and the stronger existence of a common refinement

\[
a=ef,\qquad b=gh,\qquad c=eg,\qquad d=fh.
\]

The central research question was:

> **What structural property survives the transition from ordinary integers to omnific integers that keeps the refinement square admissible?**

The project now has enough exact material to answer this at two different levels.

---

# 2. Final answer — algebraic level

The surviving algebraic property is

\[
\boxed{\text{every-element primality / pre-Schreier factor traceability}.}
\]

In the relevant cancellative commutative setting,

\[
\boxed{
\text{every element primal}
\iff
\text{four-factor refinement}.
}
\]

Thus factor traceability is not merely correlated with route closure.  It is the exact algebraic
state corresponding to global route closure.

This part does **not** require a specifically UNNS reformulation.

---

# 3. Final answer — mechanism level

The project also found something not contained in the bare equivalence above.

The successful regimes do not obtain primal traceability by the same mechanism.
What they share is a local-to-global pattern:

\[
\boxed{
\text{exact routed local block}
+
\text{strictly simpler unresolved residue}
+
\text{route-closed terminal regime}
+
\text{ambient reconstruction}
\Longrightarrow
\text{global traceability}.
}
\]

This has been isolated as the proved proposition

`05_UNNS/definitions/ROUTE_CLOSURE_INDUCTION.md`.

The proposition is deliberately narrow.  It is not a new generic confluence framework and does not
replace the source-specific Conway hypotheses.

---

# 4. Four-regime comparison

## A. Positive integers — immediate repair

For positive integers,

\[
e=\gcd(a,c)
\]

produces coprime residuals and forces cross-routing.

In divisibility form, if

\[
a\mid bc,
\]

one may take

\[
e=\gcd(a,b),\qquad f=a/e,
\]

and coprimality forces

\[
f\mid c.
\]

The whole factor `a` is therefore routed in one step.
The unresolved residue can be taken to be `1`.

Structural form:

`local split -> residual unit -> done`.

There is no defect core and no persistent defect channel.

---

## B. Rank-one nonfree affine/numerical monoids — finite residual defect core

The exact rank-one theorem gives global refinement only for the free lattice ray.
For nonfree numerical monoids, elementwise analysis proved:

\[
\boxed{H\setminus P(H)\text{ is finite}.}
\]

After the conductor, all sufficiently large elements are primal.

So the failure geometry is:

`finite obstruction core + cofinal primal tail`.

This regime is especially important because it falsifies a simplistic interpretation:

> “If route traceability eventually becomes universal, global route closure follows.”

It does not.
Global refinement requires **every** element primal, including the finite residual core.

Thus conductor saturation provides eventual safety but does not supply a mechanism that repairs the
terminal obstruction core.

---

## C. Higher-rank nonfree positive affine monoids — persistent defect channel

For

\[
\operatorname{rank}H\ge2,
\qquad
\operatorname{ARD}(H)>0,
\]

the project proved the stronger persistent defect-ray result:

\[
\boxed{
\exists a,\rho\ne0\quad
\forall n\ge0:
\quad a+n\rho\notin P(H).
}
\]

The failure is no longer confined to a finite core.
It can be propagated indefinitely along a legitimate monoid direction.

Structural form:

`local relation defect -> rank-preserving propagation -> no terminal repair`.

This is the clearest finite model of a route defect that survives motion through the substrate.

---

## D. Omnific candidate proof — exact repair plus forced descent

The source-locked Conway audit identifies the opposite pattern:

`finite-class primality`

`-> exact common-tail quotient refinement`

`-> occupied support-class selection`

`-> retained-block factorisation`

`-> strict support-class order-type decrease`

`-> ambient transport`

`-> primal lower-rank residual`

`-> splice`

`-> every-element primality`

`-> four-factor refinement`.

The important source-level fact is not “transfinite mathematics” by itself.
It is that the unresolved residual is **forbidden from propagating at unchanged structural rank**.
Each recursive step lowers a well-founded ordinal complexity, while the terminal finite-class regime
is already primal.

Structural form:

`exact repair -> lower-rank residue -> primal base -> reconstruction`.

---

# 5. The decisive contrast

The four regimes can now be arranged by what happens to a potential route defect.

### Positive integers

\[
\text{defect is eliminated immediately}.
\]

### Rank-one failures

\[
\text{defect survives only in a finite residual core}.
\]

### Higher-rank affine failures

\[
\text{defect propagates indefinitely at persistent structural complexity}.
\]

### Omnific candidate proof

\[
\text{every local residual is forced to strictly lower well-founded complexity until it reaches a primal base}.
\]

This is the strongest cross-regime structural distinction established by the project.

---

# 6. Why “well-founded descent” alone is still insufficient

The project originally considered whether the common surviving property might be something like

\[
\text{well-founded structural descent}.
\]

That is now rejected as the invariant.

Descent is a **mechanism**, not the final property.
A system could possess some decreasing complexity measure without every divisibility being locally
repairable, or it could descend into a non-primal terminal core.

The exact sufficient pattern requires all of the following:

1. an exact routed local block;
2. a complementary residual;
3. strict decrease of a well-founded rank on that residual;
4. a terminal/base regime that is already primal;
5. ambient reconstruction of the local routing.

Removing any of these jobs leaves a recognizable failure mode:

- no exact routed block -> immediate non-primality;
- no strict decrease -> persistent defect channel can survive;
- non-primal base -> finite obstruction core survives;
- no ambient reconstruction -> quotient-only repair need not solve the original equality.

---

# 7. What UNNS genuinely adds

UNNS should **not** rename

\[
\text{every element primal}
\]

as though that were a new algebraic theorem.

The useful UNNS contribution is the separation of three levels:

### Endpoint level
Two routes reach the same terminal result.

### Traceability level
Every factor can be routed through a decomposition; algebraically, every element is primal.

### Mechanism level
Traceability is established by an admissible sequence of exact local repairs whose unresolved
residue cannot remain structurally stationary and whose terminal regime is already closed.

The last level is where the comparison with other UNNS work becomes meaningful.  It describes not
only whether a structure exists, but **how structural incompatibility is permitted or forbidden to
persist under transformation**.

---

# 8. Final UNNS route-closure proposition

The project can now state, without overclaiming:

> **Route-Closure Induction Proposition.**  In a commutative cancellative monoid equipped with a
> well-founded structural rank, suppose a designated base regime is primal.  Suppose further that
> every divisibility involving a non-base element admits an exact ambient routed factor block whose
> complementary factor has strictly lower structural rank.  Then every element is primal, and hence
> every product equality admits four-factor refinement.

This proposition is proved in

`05_UNNS/definitions/ROUTE_CLOSURE_INDUCTION.md`.

It adds real content beyond the standard equivalence because it supplies a sufficient **construction
principle** for reaching the pre-Schreier state.

It does not claim necessity, and it does not claim that all refinement structures must organize their
proofs through the same rank/descent architecture.

---

# 9. Final answer to the original research question

The original question was:

> What structural property survives the transition from ordinary integers to omnific integers that keeps the refinement square admissible?

The answer is now two-layered.

## Property

\[
\boxed{\text{global factor traceability: every element is primal}.}
\]

## Successful construction pattern

\[
\boxed{
\text{exact local routing}
+
\text{well-founded reduction of the unresolved residue}
+
\text{primal terminal closure}
+
\text{ambient reconstruction}.
}
\]

The integers realize this pattern degenerately and immediately: the residual can be reduced to the
unit in one gcd-controlled step.

The candidate omnific proof realizes it transfinally: a retained support-class block is repaired,
the residual support-class rank strictly decreases, and the process terminates in the finite-class
primal regime.

The failure systems show exactly why each distinction matters:

- rank one can leave a finite unresolved core;
- higher rank can support an infinite persistent defect ray.

Therefore the strongest justified UNNS conclusion is:

\[
\boxed{
\textbf{global route closure is the absence of any structural defect capable of surviving every admissible exact repair and well-founded reduction.}
}
\]

This final sentence is an UNNS interpretation of the proven comparison, not a replacement definition
of algebraic primality.

---

# 10. Research status after this synthesis

The original Conway/UNNS structural-comparison objective is now substantially complete at the
current source state.

What remains would be a **new research branch**, not an unfinished step in this comparison:

- formalize the route-closure induction proposition in Lean;
- seek non-affine algebraic systems that separate the sufficiency mechanism from other proofs of
  pre-Schreier structure;
- investigate whether analogous “persistent defect channel vs rank-lowering repair” diagnostics are
  useful outside factor-refinement algebra.

Those should not be started automatically inside this project without a deliberate decision to
extend its scope.
