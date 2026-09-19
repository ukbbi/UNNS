# Primality–Refinement Correspondence

## Elementwise localization of structural route closure

**Project:** `UNNS_COMMON_REFINEMENT`  
**Status:** derived algebraic result / project synthesis  
**Scope:** commutative cancellative monoids; additive notation is used for the non-refinement controls and multiplicative notation for the Conway form.

---

# 1. Why this note exists

The Conway Structural Spine identified

\[
\text{every element primal}
\]

as the algebraic state shared by the successful positive-integer regime and the audited omnific candidate proof, and absent globally in the exact failure systems.

The next question is whether this statement can be localized to a single element and a single failed equality.

It can.

The key result is:

\[
\boxed{
 x\text{ is primal}
 \iff
 \text{every endpoint equality having }x\text{ as a corner admits a }2\times2\text{ refinement}.
}
\]

This turns primality from a background factorization property into an exact **local route-closure criterion**.

---

# 2. Multiplicative statement

Let \(M\) be a commutative cancellative monoid and let \(x\in M\).

Recall that \(x\) is **primal** if for every divisibility relation

\[
x\mid yz
\]

there are \(e,f\in M\) such that

\[
x=ef,\qquad e\mid y,\qquad f\mid z.
\]

Define the **corner refinement property for \(x\)**:

> For every equality
> \[
> xb=cd,
> \]
> there exist \(e,f,g,h\in M\) such that
> \[
> x=ef,\qquad b=gh,\qquad c=eg,\qquad d=fh.
> \]

Then:

## Theorem — Elementwise Primality–Refinement Correspondence

\[
\boxed{
 x\text{ is primal}
 \iff
 x\text{ has the corner refinement property}.
}
\]

---

# 3. Proof: primality implies corner refinement

Assume \(x\) is primal and

\[
xb=cd.
\]

Then \(x\mid cd\). By primality, there exist \(e,f\) such that

\[
x=ef,
\]

with

\[
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

Substituting into the endpoint equality gives

\[
(ef)b=(eg)(fh)=efgh.
\]

By cancellation,

\[
b=gh.
\]

Therefore

\[
\boxed{
 x=ef,
 \quad b=gh,
 \quad c=eg,
 \quad d=fh.
}
\]

So every endpoint equality containing a primal corner is structurally refinable.

---

# 4. Proof: corner refinement implies primality

Assume every equality

\[
xb=cd
\]

has a common refinement.

Suppose

\[
x\mid cd.
\]

Choose \(b\) such that

\[
xb=cd.
\]

By the corner refinement property, there are \(e,f,g,h\) with

\[
x=ef,
\qquad
c=eg,
\qquad
d=fh.
\]

Hence

\[
e\mid c,
\qquad
f\mid d.
\]

Therefore \(x\) is primal.

This direction needs only the existence of the endpoint equality produced by divisibility; cancellation is needed in the first direction to recover the complementary corner.

---

# 5. Global corollary

Applying the elementwise theorem to every \(x\in M\) gives

\[
\boxed{
\text{every element primal}
\iff
\text{every endpoint equality admits common refinement}.
}
\]

Equivalently, in the present cancellative setting,

\[
\boxed{
\text{decomposition / pre-Schreier factor traceability}
\iff
\text{global }2\times2\text{ route closure}.
}
\]

This is the exact algebraic backbone of the cross-regime comparison.

---

# 6. Four-corner obstruction localization

Now suppose

\[
ab=cd
\]

has **no** common refinement.

If \(a\) were primal, the theorem above would construct the missing square. Therefore \(a\) is non-primal.

But the equality is symmetric under exchanging the four corner roles. The same argument can be repeated with \(b\), \(c\), or \(d\) as the distinguished corner.

Hence:

## Corollary — Four-Corner Obstruction

For a non-refinable equality in a commutative cancellative monoid,

\[
\boxed{
ab=cd\text{ with }D_R=1
\Longrightarrow
 a,b,c,d\text{ are all non-primal}.
}
\]

The statement concerns the four **positions**. Some positions can of course contain the same element.

This is stronger than saying merely that the ambient monoid is not a decomposition monoid.

A single failed square localizes the obstruction to every structural block participating in that equality.

---

# 7. Converse certificate: non-primality manufactures a failed square

Suppose \(x\) is non-primal.

Then there exist \(y,z\) such that

\[
x\mid yz
\]

but no factorization

\[
x=ef
\]

can simultaneously satisfy

\[
e\mid y,
\qquad
f\mid z.
\]

Choose \(t\) with

\[
xt=yz.
\]

If this equality admitted a four-factor refinement, its \(x\)-row would provide exactly the forbidden split of \(x\).

Therefore

\[
\boxed{
 x\text{ non-primal}
 \Longrightarrow
 \exists\,t,y,z:\ xt=yz\text{ is a }D_R=1\text{ equality}.
}
\]

Combining both directions:

\[
\boxed{
 x\text{ non-primal}
 \iff
 x\text{ occurs as a corner of some non-refinable endpoint equality}.
}
\]

This is the most useful local form of the project result.

---

# 8. Additive form used by the project controls

For the additive monoids in `02_NONREF`, replace multiplication by addition.

An element \(x\) is primal when

\[
x\le_H y+z
\]

implies a decomposition

\[
x=e+f,
\qquad
e\le_H y,
\qquad f\le_H z,
\]

where \(u\le_H v\) means \(u\) divides \(v\) in the algebraic preorder, i.e. \(v=u+w\) for some \(w\in H\).

The elementwise theorem becomes

\[
\boxed{
 x\text{ primal}
 \iff
 \text{every equality }x+b=c+d\text{ admits additive }2\times2\text{ refinement}.
}
\]

And a failure

\[
a+b=c+d
\]

with no refinement certifies all four corner positions as non-primal.

---

# 9. Direct check against the flagship rank-one control

For

\[
H=\langle2,3\rangle
\]

the project has

\[
2+4=3+3
\]

with no refinement in \(H\).

Therefore the same equality is simultaneously a non-primality certificate for the four positions

\[
2,
\quad 4,
\quad 3,
\quad 3.
\]

For example, from the corner \(2\),

\[
2\le_H3+3
\]

because

\[
3+3=2+4.
\]

If \(2\) were primal, it would split across the two copies of \(3\), producing a refinement of the equality. The project has already established that no such refinement exists.

Thus the route defect and the primality defect are not merely correlated; they are the same obstruction viewed from two directions.

---

# 10. Direct check against the affine controls

The affine failure

\[
(2,0)+(0,2)=(1,1)+(1,1)
\]

in `NORMAL_PARITY` has no common refinement.

Therefore every corner position is non-primal:

\[
(2,0),
\quad(0,2),
\quad(1,1),
\quad(1,1).
\]

The same conclusion applies to each explicit `D_R=1` equality retained in the affine corpus.

The generated file

```text
04_PROOF_MAP/output/FAILURE_CERTIFICATES.csv
```

records this consequence for all 513 canonical rank-one failure systems and all 4 explicit affine failure systems currently retained in the project.

---

# 11. UNNS interpretation

The result sharpens the earlier phrase **factor traceability under decomposition**.

A primal element is a structural block whose identity can always be decomposed and traced through any two-branch recombination in which it participates.

A non-primal element is therefore not merely "hard to factor". It admits at least one endpoint coincidence for which its identity cannot be routed through the opposite branches.

So the local UNNS statement is:

\[
\boxed{
\text{primal structural block}
\iff
\text{locally route-closed structural block}.
}
\]

And the failure statement is:

\[
\boxed{
D_R=1
\Longrightarrow
\text{four-corner loss of decomposable route traceability}.
}
\]

This is more precise than calling non-refinement a generic stitching defect. The defect is localized in divisibility structure.

---

# 12. What this changes in the project

The next exact object should not be another global abstraction.

The mathematically natural next object is an **elementwise route-closure profile**:

\[
\operatorname{RC}(x)=
\begin{cases}
1,&x\text{ is primal},\\
0,&x\text{ is non-primal}.
\end{cases}
\]

This is not proposed as a new theorem or a new invariant name for publication. It is a computational/project diagnostic that asks:

> Where inside a non-refinement system does traceability fail, and where does it survive?

That question is directly relevant to the Conway comparison because the omnific candidate proof attempts to drive this profile to

\[
\operatorname{RC}(x)=1
\quad\text{for every }x
\]

by support-class descent and transport.

A bounded numerical scan may be useful for exploration, but a bounded search must never be mislabeled as a proof of primality. Exact classifications should be derived only when the algebra of the chosen system supports them.

---

# 13. Status discipline

- **Standard algebraic notion:** primal element; decomposition monoid / pre-Schreier terminology.
- **Derived project theorem:** elementwise corner-refinement equivalence in the commutative cancellative setting.
- **Derived project corollary:** every `D_R=1` equality certifies all four corner positions as non-primal.
- **Generated project evidence:** 517 retained failure equalities converted into four-corner certificates.
- **UNNS interpretation:** primality is local decomposable route traceability.
- **Not claimed:** novelty of the primal/decomposition concepts or of their generic algebraic relationship to refinement theory.
- **Not claimed:** that a bounded computational primality scan establishes exact primality.

---

# 14. Standard terminology check

The terminology used here agrees with standard factorization theory and Mathlib: a decomposition monoid is one in which every element is primal; for domains this is the multiplicative condition underlying the pre-Schreier property.

This note uses that standard algebra only as the exact mathematical carrier of the UNNS route-traceability interpretation.
