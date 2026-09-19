# Affine Route-Closure Criterion

## Domain

Let \(H\) be a **positive affine monoid**: a finitely generated additive submonoid of
\(\mathbb Z^d\) with

\[
H\cap(-H)=\{0\}.
\]

Thus \(H\) is commutative, cancellative, torsion-free, conical, and finitely generated.

For

\[
a+b=c+d
\]

in \(H\), a common refinement is a matrix

\[
\begin{matrix}
e & f\\
g & h
\end{matrix}
\]

with

\[
a=e+f,\qquad b=g+h,\qquad c=e+g,\qquad d=f+h.
\]

Let \(\mathcal A(H)\) denote the finite set of atoms of \(H\), and let

\[
r=\operatorname{rank}\operatorname{gp}(H),\qquad
s=|\mathcal A(H)|.
\]

Define the **Atom-Relation Defect**

\[
\operatorname{ARD}(H)=s-r.
\]

Because the atoms generate \(H\), \(s\ge r\).

---

# Theorem

For a positive affine monoid \(H\), the following are equivalent:

1. \(H\) has the Riesz \(2\times2\) refinement property.
2. Every atom of \(H\) is prime in the algebraic preorder.
3. Factorization into atoms is unique.
4. \(H\) is a free commutative monoid on its atoms.
5. \(H\cong\mathbb N_0^r\).
6. \(|\mathcal A(H)|=r\).
7. \(\operatorname{ARD}(H)=0\).

Hence

\[
\boxed{
H\text{ has global structural route closure}
\iff
\operatorname{ARD}(H)=0.
}
\]

If

\[
\operatorname{ARD}(H)>0,
\]

then \(H\) necessarily contains a nontrivial atomic relation, and global common refinement fails.

---

## Proof

### 1. Refinement forces atoms to be prime

Let \(p\) be an atom and suppose

\[
p+z=x+y.
\]

A refinement gives

\[
p=e+f,\qquad
z=g+h,\qquad
x=e+g,\qquad
y=f+h.
\]

Since \(p\) is an atom, either \(e=0\) or \(f=0\).

If \(e=0\), then \(p=f\) and \(p\le_H y\).

If \(f=0\), then \(p=e\) and \(p\le_H x\).

Thus \(p\) is prime.

Therefore

\[
\text{refinement}\Longrightarrow
\text{every atom is prime}.
\]

### 2. Prime atoms force unique factorization

A positive affine monoid is atomic: every nonzero element is a finite sum of atoms.

Assume every atom is prime and suppose

\[
p_1+\cdots+p_m=q_1+\cdots+q_n
\]

are two atomic factorizations.

Because \(p_1\) is prime, it lies below one \(q_j\). Since \(q_j\) is itself an atom,
this forces \(p_1=q_j\). Cancellation removes that atom from both sides.

Induction gives equality of the two multisets of atoms.

Thus factorization is unique.

### 3. Unique atomic factorization is freeness

Let the distinct atoms be \(u_1,\ldots,u_s\).

Unique factorization makes

\[
\mathbb N_0^s\to H,\qquad
(n_1,\ldots,n_s)\mapsto\sum_i n_i u_i
\]

bijective.

Hence

\[
H\cong\mathbb N_0^s.
\]

The Grothendieck group is therefore

\[
\operatorname{gp}(H)\cong\mathbb Z^s,
\]

so \(s=r\).

### 4. Atom count equal to rank forces freeness

Conversely, the atoms generate \(\operatorname{gp}(H)\).

If \(s=r\), then \(s\) group generators span a rank-\(s\) free abelian group, so they
are \(\mathbb Z\)-linearly independent. Therefore there is no nontrivial relation between
two different nonnegative combinations of atoms.

Hence atomic factorization is unique and \(H\cong\mathbb N_0^r\).

### 5. Free monoids have refinement

In \(\mathbb N_0^r\), refinement is coordinatewise.

For

\[
a+b=c+d,
\]

set

\[
e_i=\min(a_i,c_i),\qquad
f_i=a_i-e_i,\qquad
g_i=c_i-e_i.
\]

The endpoint equality yields a nonnegative \(h_i\) satisfying

\[
b_i=g_i+h_i,\qquad
d_i=f_i+h_i.
\]

Thus \(\mathbb N_0^r\), and every monoid isomorphic to it, has refinement.

This closes the equivalence.

---

# Geometric corollary

Let

\[
L=\operatorname{gp}(H),\qquad
C=\mathbb R_{\ge0}H.
\]

Then refinement is equivalent to the existence of a lattice basis
\(u_1,\ldots,u_r\) of \(L\) such that

\[
C=\sum_{i=1}^r\mathbb R_{\ge0}u_i
\]

and

\[
H=\sum_{i=1}^r\mathbb N_0u_i.
\]

Equivalently:

\[
\boxed{
H=C\cap L
\quad\text{and}\quad
C\text{ is unimodular simplicial with respect to }L.
}
\]

This is the exact higher-rank replacement for the rank-one lattice-saturation criterion.

---

# What survives from rank one?

The previous rank-one theorem was

\[
H\subseteq\mathbb N_0,\qquad
\text{refinement}\iff H=\operatorname{Sat}_{lat}(H).
\]

In rank one every pointed rational cone has one ray, so the cone is automatically simplicial.
Relative to its generated rank-one lattice, the primitive ray generator is automatically a
lattice basis.

Therefore **unimodular simpliciality is invisible in rank one**.

Once rank \(>1\), lattice saturation remains necessary but is no longer sufficient.

Higher rank adds a second requirement:

\[
\boxed{\text{no independent atomic relations}.}
\]

That requirement is measured exactly by

\[
\operatorname{ARD}(H)=|\mathcal A(H)|-\operatorname{rank}\operatorname{gp}(H).
\]

---

# Exact counterexamples

## Saturated but non-unimodular

\[
H=\langle(2,0),(1,1),(0,2)\rangle.
\]

This equals the nonnegative points of its parity lattice:

\[
H=\{(x,y)\in\mathbb N_0^2:x\equiv y\pmod2\}.
\]

So it is lattice-saturated relative to its own generated group.

But

\[
(2,0)+(0,2)=(1,1)+(1,1),
\]

and the three displayed generators are atoms.

Thus

\[
\operatorname{ARD}=3-2=1
\]

and refinement fails.

This proves that **saturation alone ceases to be sufficient beyond rank one**.

## Saturated and simplicial, but non-unimodular

\[
H=\langle(1,0),(1,1),(1,2)\rangle.
\]

It is the full lattice-point monoid of the cone

\[
0\le y\le2x,
\]

yet

\[
(1,0)+(1,2)=2(1,1).
\]

Again

\[
\operatorname{ARD}=1.
\]

So even **normality + simpliciality** is insufficient: unimodularity is the missing ingredient.

## Saturated but non-simplicial

Let

\[
H=\langle
(0,0,1),(1,0,1),(0,1,1),(1,1,1)
\rangle.
\]

This is the lattice-point monoid of

\[
0\le x\le z,\qquad
0\le y\le z.
\]

Its cone has four extreme rays in rank three.

The atomic relation

\[
(0,0,1)+(1,1,1)
=
(1,0,1)+(0,1,1)
\]

gives an exact refinement failure.

Here

\[
\operatorname{ARD}=4-3=1.
\]

---

# Structural conclusion

The rank-one picture

\[
\text{route closure}=\text{lattice closure}
\]

does not survive unchanged.

The affine higher-rank picture is

\[
\boxed{
\text{route closure}
=
\text{lattice closure}
+
\text{atomic independence}
}
\]

or geometrically

\[
\boxed{
\text{route closure}
=
\text{normality}
+
\text{unimodular simpliciality}.
}
\]

The algebraic form is even sharper:

\[
\boxed{
\text{route closure}
\iff
\text{every irreducible is prime}
\iff
\text{free atomic architecture}.
}
\]
