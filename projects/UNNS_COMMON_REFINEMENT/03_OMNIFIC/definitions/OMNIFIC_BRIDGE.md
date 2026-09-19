# Omnific Bridge — What Replaces the Finite Atom Basis?

## Purpose

The affine part of this project established an exact finite theorem:

\[
\text{refinement}
\iff
\text{every atom is prime}
\iff
\text{unique atomic factorization}
\iff
H\cong\mathbb N_0^r.
\]

For positive affine monoids this could be compressed into

\[
\operatorname{ARD}=0.
\]

That criterion cannot be transferred literally to omnific integers because the Conway
problem is not a finitely generated affine-monoid problem.

The correct next question is therefore:

> Which **roles** played by the finite atom basis reappear in the transfinite proof, and what
> new ingredients are required because the support can be infinite?

This file records only correspondences supported by the public proof map. It does not
claim that the candidate proof has been independently accepted by the mathematical community.

---

# 1. What survives unchanged: prime traceability

The strongest direct correspondence is:

\[
\boxed{\text{irreducible}\Longrightarrow\text{prime}.}
\]

In the affine theorem this was load-bearing: once atoms are prime, competing atomic
factorizations collapse into unique factor coordinates.

The Conway proof map contains:

- **(181) Primality of reduced omnific integers outside \(\mathbb Z\)**;
- **(182) Irreducible omnific integers are prime**.

So prime traceability is not merely analogous. It is an explicit intermediate theorem in
the candidate omnific development.

This is the first exact bridge.

---

# 2. What replaces ARD = 0?

The finite quantity

\[
\operatorname{ARD}
=
|\mathcal A(H)|
-
\operatorname{rank}\operatorname{gp}(H)
\]

measured whether atomic generators carried independent coordinates.

There is no finite atom list to count in the omnific setting.

The proof instead develops:

1. **Cantor–Bendixson ranks of supports**;
2. **algebraic independence in associated graded rings**;
3. **principal RV-elements**;
4. **polynomial presentations**.

The closest structural replacement for finite \(\operatorname{ARD}=0\) is therefore not a
single integer. It is a layered independence statement:

\[
\boxed{
\text{independence of leading/support strata}
\rightarrow
\text{polynomial coordinate control}.
}
\]

This must be described as a structural analogue rather than as a theorem saying
"ARD becomes X". The public proof map does not define such an invariant.

The finite relation space has become a **graded relation problem**.

---

# 3. What replaces a finite atom basis?

In the affine theorem every element could be written using a finite list of independent atoms.

The omnific proof instead uses a hierarchy of support classes and Archimedean structure.

Relevant proof-map components include:

- real structure of surreal Archimedean strata;
- cofinality of surreal Archimedean balls;
- cofinality of common surreal Archimedean tails;
- signed normal-form isomorphism for omnific integers.

Thus the replacement is not another basis in the ordinary linear-algebra sense.

It is better described as

\[
\boxed{
\text{finite atom coordinates}
\rightsquigarrow
\text{normal form + stratified support coordinates}.
}
\]

The object is resolved layer by layer rather than all at once.

---

# 4. What replaces finite termination?

Finite affine factor arguments terminate because there are only finitely many atoms in a
factorization and ordinary size decreases.

The transfinite proof map contains the explicit lemma

**(152) Strict decrease of support-class order type.**

This is the clearest replacement of finite descent.

Instead of a natural-number complexity

\[
n>n_1>n_2>\cdots,
\]

the proof uses a well-founded ordinal/support complexity

\[
\alpha>\alpha_1>\alpha_2>\cdots.
\]

So the finite condition

\[
\text{decomposition terminates}
\]

becomes

\[
\boxed{
\text{support-class descent is well founded}.
}
\]

This is the second exact bridge.

---

# 5. What replaces finite extension?

The proof map contains:

**(158) Transfinite extension of finite-class primality.**

That title is highly informative for the present project.

It says the proof does not discard finite structural control. It proves a finite-class
version and then extends it through the transfinite support hierarchy.

Schematically:

\[
P(\text{finite support classes})
\]

plus

\[
\text{well-founded descent}
\]

gives

\[
P(\text{transfinite support architecture}).
\]

This is very close to the UNNS idea that a global structural law can arise by preserved
constraints propagated through a hierarchy.

---

# 6. A genuinely new ingredient: limit-stage closure

The affine theorem did not need a special limit-stage mechanism.

The omnific proof does.

The proof map contains:

- **(176) Cofinality of common surreal Archimedean tails**;
- **(177) Fraction fields of surreal common-tail integer parts**;
- **(184) A coinitial family of positive elements in surreal common-tail quotients**;
- **(185) Cauchy completeness of surreal common-tail quotients**.

This indicates a new structural requirement:

\[
\boxed{
\text{descent alone is insufficient;
limit/tail stages must also close.}
}
\]

In UNNS language, a transfinite route cannot merely keep descending correctly.
When infinitely many prior stages accumulate, the resulting common tail must remain inside
a structure in which the next factor/refinement step is still realizable.

This has no direct analogue in the finite affine theorem.

---

# 7. The resulting proof spine

The finite affine spine was

\[
\text{independent atoms}
\rightarrow
\text{irreducible = prime}
\rightarrow
\text{unique routing}
\rightarrow
\text{refinement}.
\]

The candidate omnific spine is closer to

\[
\text{support stratification}
\]

\[
\downarrow
\]

\[
\text{graded algebraic independence}
\]

\[
\downarrow
\]

\[
\text{polynomial/local factor control}
\]

\[
\downarrow
\]

\[
\text{finite Archimedean-class primality}
\]

\[
\downarrow
\]

\[
\text{strict support-class descent}
\]

\[
\downarrow
\]

\[
\text{transfinite extension}
\]

\[
\downarrow
\]

\[
\text{common-tail completeness}
\]

\[
\downarrow
\]

\[
\text{surreal Hahn integer-part primality}
\]

\[
\downarrow
\]

\[
\text{Oz refinement}.
\]

The public proof map records the final nodes:

- **(186) Primality of the surreal Hahn integer part**;
- **(187) Refinement property of \(\mathbf{Oz}_u\)**;
- **(188) Conway's refinement theorem for omnific integers**.

---

# 8. The finite-to-transfinite replacement table

| Finite affine role | Transfinite replacement in candidate proof |
|---|---|
| finite atom basis | normal form + support/Archimedean strata |
| ARD = 0 | graded algebraic independence + polynomial presentation |
| atom/irreducible is prime | irreducible omnific integer is prime |
| finite descent | strict decrease of support-class order type |
| finite propagation | transfinite extension of finite-class primality |
| no limit issue | common-tail Cauchy completeness |
| free coordinate routing | Hahn integer-part primality |
| global Riesz refinement | refinement property of Oz |

The important discovery is that **ARD does not disappear** conceptually.

Its finite role splits into two transfinite mechanisms:

\[
\boxed{
\text{independence}
+
\text{well-founded hierarchical propagation}.
}
\]

And because the hierarchy can have limit stages, a third ingredient appears:

\[
\boxed{\text{limit closure}.}
\]

---

# 9. Provisional transfinite route-closure schema

The comparison suggests the following schema.

A transfinite structural system should support global route closure when it has:

1. **Local Independence**  
   leading/graded structural components admit no destructive hidden relations;

2. **Prime Traceability**  
   irreducible structural components cannot disappear into a product;

3. **Well-Founded Descent**  
   every unresolved factor/refinement step lowers a structural rank;

4. **Limit Closure**  
   limit/common-tail stages remain complete enough for the next local step;

5. **Reconstruction**  
   local refined pieces reassemble into the original global structure.

Call these provisionally

\[
(I,P,D,L,R).
\]

Then the working UNNS schema is

\[
\boxed{
I+P+D+L+R
\Longrightarrow
\text{Transfinite Route Closure}.
}
\]

This is **not yet a general theorem** of UNNS.

It is the minimal abstract schema extracted from the finite affine theorem and the architecture
of the candidate Conway proof.

The next mathematical task is to determine whether these five conditions can be stated
independently of Hahn-series/omnific machinery and proved sufficient in an abstract class
of filtered or stratified factorization structures.
