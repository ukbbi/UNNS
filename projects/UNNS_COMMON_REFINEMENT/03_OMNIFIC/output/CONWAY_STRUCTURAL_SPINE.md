# Conway Structural Spine

## Decisive comparative synthesis

The project has now compared four regimes:

1. positive integers;
2. exact rank-one non-refinement controls;
3. higher-rank positive affine monoids;
4. the candidate omnific proof architecture.

The comparison identifies one structural property that exactly separates the successful and failed
refinement regimes:

\[
\boxed{
\text{every element is primal}
}
\]

or, in UNNS language,

\[
\boxed{
\text{every factor is structurally traceable through a competing product route}.
}
\]

This is not merely correlated with refinement.

In the cancellative setting it is equivalent to four-factor refinement.

---

# A. Positive integers

Given

\[
ab=cd,
\]

the gcd construction sets

\[
e=\gcd(a,c),
\qquad
a=ef,
\qquad
c=eg,
\qquad
\gcd(f,g)=1.
\]

The equation becomes

\[
fb=gd,
\]

so

\[
g\mid b,\qquad f\mid d.
\]

Hence

\[
b=gh,\qquad d=fh.
\]

### Structural reading

The gcd is not itself the cross-domain invariant.

It is the finite arithmetic mechanism proving that the distinguished factor \(a\) can always be
split into pieces routed into \(c\) and \(d\).

That is exactly primality.

So:

\[
\boxed{
\text{integer gcd routing}
\Longrightarrow
\text{global primality}
\Longrightarrow
\text{refinement}.
}
\]

---

# B. Rank-one failure controls

Take

\[
H=\langle2,3\rangle.
\]

The equality

\[
2+4=3+3
\]

has no refinement in \(H\).

The reason can be stated exactly as a traceability failure.

The least atom \(2\) lies below \(3+3\):

\[
2\le_H 3+3
\]

because

\[
(3+3)-2=4\in H.
\]

But \(2\) cannot be routed into either branch individually:

\[
2\nleq_H3,
\]

because that would require

\[
3-2=1\in H,
\]

which is false.

Thus the flagship non-refinement equality is simultaneously an explicit witness that \(2\) is not
primal.

The rank-one theorem

\[
H\text{ refinable}
\iff
m\text{ prime}
\iff
H=m\mathbb N_0
\]

is therefore already a traceability theorem.

---

# C. Higher-rank affine controls

For a positive affine monoid \(H\), the project proved:

\[
\text{refinement}
\iff
\text{every atom prime}
\iff
\text{unique atomic factorization}
\iff
H\cong\mathbb N_0^r.
\]

Because these monoids are atomic, prime atoms make every element primal.

So the affine criterion is again the same structural law:

\[
\boxed{
\text{atomic traceability}
\Longleftrightarrow
\text{global route closure}.
}
\]

The invariant is not lattice saturation by itself.

The decisive issue is whether atomic identity remains traceable through competing decompositions.

For the standard relation

\[
u+w=v+v,
\]

an atom such as \(u\) lies below \(v+v\) but not below either \(v\) separately.

That is exactly a primality failure.

---

# D. Omnific candidate proof

The audited candidate proof makes the cross-domain invariant explicit.

Its transfinite target is not gcd structure and not finite atomic freeness.

It proves:

\[
\boxed{
\forall a,\operatorname{IsPrimal}(a).
}
\]

The mechanism is:

\[
\text{finite-class primality}
\]

\[
\downarrow
\]

\[
\text{exact local quotient refinement}
\]

\[
\downarrow
\]

\[
a=t\,w
\quad\text{with}\quad
\rho(w)<\rho(a)
\]

\[
\downarrow
\]

\[
w\text{ primal by induction}
\]

\[
\downarrow
\]

\[
\text{transport + splice}
\]

\[
\downarrow
\]

\[
a\text{ primal}.
\]

After this has been proved for all \(a\),

\[
\forall a,\operatorname{IsPrimal}(a)
\]

is packaged as a decomposition monoid / pre-Schreier condition, and the generic algebraic theorem
produces four-factor refinement.

Thus the omnific proof preserves the **same structural law** as ordinary integers, but establishes
it by a transfinite mechanism instead of gcd arithmetic.

---

# E. The answer to the original refinement-plan question

The plan asked:

> What structural property survives the transition from ordinary integers to omnific integers that
> keeps the refinement square admissible?

The answer supported by the comparison is:

\[
\boxed{
\textbf{primal factor traceability}.
}
\]

More explicitly:

> A factor can be decomposed so that its structural content remains traceable into the two branches
> of any product through which it divides.

Algebraically:

\[
a\mid cd
\Longrightarrow
\exists e,f:
\quad
a=ef,\ e\mid c,\ f\mid d.
\]

Globally:

\[
\boxed{
\forall a,\operatorname{IsPrimal}(a)
\iff
\text{every endpoint product equality admits a common refinement}.
}
\]

---

# F. What becomes of well-founded descent?

Well-founded descent is important, but it is not the surviving law.

Positive integers do not need support-class ordinal descent.

Free affine monoids do not need it either.

The candidate omnific proof needs it because the domain is structurally infinite.

Therefore:

\[
\boxed{
\text{well-founded descent is an omnific proof mechanism, not the common invariant}.
}
\]

The same applies to:

- gcd;
- coprimality;
- atomic freeness;
- Cauchy completeness;
- Archimedean classes.

Each is domain-specific machinery.

The invariant they serve is traceability/primality.

---

# G. Corrected UNNS formulation

The strongest exact statement justified now is:

\[
\boxed{
\text{Global Factor Traceability}
\iff
\text{Global Structural Route Closure}.
}
\]

For an individual nonzero factor \(a\):

\[
\boxed{
a\text{ is primal}
\iff
\text{every product equality passing through }a
\text{ admits a common refinement}.
}
\]

The previously contemplated formula

\[
\text{endpoint equivalence}
+
\text{well-founded descent}
+
\text{local route traceability}
\Rightarrow
\text{common refinement}
\]

should no longer be treated as the fundamental law.

It is better understood as one **sufficient implementation pattern** for proving global
traceability in transfinite domains.

The exact cross-domain law is simpler and stronger:

\[
\boxed{
\text{traceability}
\iff
\text{refinement}.
}
\]

---

# H. Status

### Established in project

- positive-integer witness mechanism;
- exact rank-one failures;
- rank-one route-closure criterion;
- affine route-closure criterion;
- source-level audit of the candidate omnific proof;
- exact identification of the common surviving property.

### Classical algebraic ancestry

The equivalence between all-elements-primal and four-factor refinement is not claimed as a new
algebra theorem.

### UNNS contribution at this stage

The project has identified that its "route traceability" language corresponds exactly to primality,
and that the integer, affine, and candidate omnific mechanisms are different realizations of this
same structural property.

That is the decisive comparative synthesis required by the original refinement plan.
