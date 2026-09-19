# Rank-One Common Refinement Criterion

## Scope

Let \(H\subseteq\mathbb N_0\) be a nonzero additive submonoid.

For \(a,b,c,d\in H\), call

\[
a+b=c+d
\]

**commonly refinable in \(H\)** if there exist \(e,f,g,h\in H\) such that

\[
a=e+f,\qquad b=g+h,\qquad c=e+g,\qquad d=f+h.
\]

This is exactly the \(2\times2\) Riesz refinement property.

Let

\[
m=\min(H\setminus\{0\})
\]

and let

\[
\gamma=\gcd(H),
\]

equivalently the positive generator of the group \(\operatorname{gp}(H)=\gamma\mathbb Z\).

---

# Theorem — Rank-One Route-Closure Criterion

For every nonzero additive submonoid \(H\subseteq\mathbb N_0\), the following are equivalent:

1. \(H\) has the \(2\times2\) refinement property.
2. The least positive element \(m\) is prime with respect to the algebraic preorder of \(H\).
3. \(H=m\mathbb N_0\).
4. \(H=(\mathbb R_{\ge0}H)\cap\operatorname{gp}(H)=\gamma\mathbb N_0\); i.e. \(H\) equals its rank-one lattice saturation.
5. \(m=\gamma\).

Thus the exact rank-one criterion is

\[
\boxed{\text{common refinement for all endpoint equalities}\iff m=\gcd(H).}
\]

Define the rank-one route-closure index

\[
\operatorname{RCI}(H)=\frac{m}{\gamma}.
\]

Then

\[
\boxed{\operatorname{RCI}(H)=1\iff H\text{ has common refinement}.}
\]

If \(\operatorname{RCI}(H)>1\), common refinement fails.

---

## Proof

### Lemma 1 — the least positive element is an atom

Because \(m\) is the least positive member of \(H\), a decomposition

\[
m=u+v,\qquad u,v\in H
\]

cannot have both \(u,v>0\). Hence \(m\) is an atom.

### Lemma 2 — atoms are prime in a conical refinement monoid

Assume \(p\) is an atom and

\[
p+z=x+y.
\]

Refinement gives

\[
p=r+s,\qquad z=t+u,\qquad x=r+t,\qquad y=s+u.
\]

Since \(p\) is an atom, either \(r=0\) or \(s=0\).

If \(r=0\), then \(p=s\) and \(p\le_H y\).
If \(s=0\), then \(p=r\) and \(p\le_H x\).

Therefore \(p\) is prime.

Hence refinement implies that the least positive element \(m\) is prime.

### Lemma 3 — if \(m\) is prime, then every element is a multiple of \(m\)

Take any \(x\in H\), \(x>0\).

The ordinary integers \(m\) and \(x\) are commensurable, so there exist positive integers \(r,s\) with

\[
rm=sx.
\]

Then

\[
sx=m+(r-1)m,
\]

so \(m\le_H sx\).

Because \(m\) is prime, repeated application to

\[
sx=x+\cdots+x
\]

gives \(m\le_H x\). Hence

\[
x=m+y
\]

for some \(y\in H\).

If \(y>0\), repeat. Since the ordinary integer value strictly decreases, the process terminates. Thus

\[
x=qm
\]

for some \(q\in\mathbb N_0\).

Therefore \(H\subseteq m\mathbb N_0\). The reverse inclusion holds because \(m\in H\) and \(H\) is closed under addition. Hence

\[
H=m\mathbb N_0.
\]

### Lemma 4 — \(m\mathbb N_0\) has refinement

Scaling by \(m\) identifies \(m\mathbb N_0\) with \(\mathbb N_0\).

For

\[
a+b=c+d
\]

in \(\mathbb N_0\), set

\[
e=\min(a,c),\qquad
f=a-e,\qquad
g=c-e.
\]

Then the endpoint equality forces a nonnegative \(h\) with

\[
b=g+h,\qquad d=f+h.
\]

So \(\mathbb N_0\), and therefore \(m\mathbb N_0\), has refinement.

This closes the equivalence.

### Lattice form

For a nonzero submonoid of \(\mathbb N_0\),

\[
\operatorname{gp}(H)=\gamma\mathbb Z
\]

and

\[
(\mathbb R_{\ge0}H)\cap\operatorname{gp}(H)=\gamma\mathbb N_0.
\]

Therefore

\[
H=m\mathbb N_0
\]

is equivalent to

\[
m=\gamma,
\]

and to equality with the rank-one lattice saturation.

---

# Constructive failure theorem

The negative direction can be made explicit.

Suppose

\[
m>\gamma.
\]

Choose the smallest \(x\in H\) that is not a multiple of \(m\).

Choose the least integer \(k\ge2\) such that

\[
kx-m\in H.
\]

Such a \(k\) exists: a common multiple of \(m\) and \(x\) eventually gives one.

Then

\[
m+(kx-m)=x+(k-1)x
\]

is an endpoint equality in \(H\), but it has no common refinement.

Why?

Any refinement would split the atom \(m\) as

\[
m=e+f.
\]

Hence either \(e=m,f=0\) or \(e=0,f=m\).

The first case forces

\[
x-m\in H,
\]

contradicting the choice of \(x\).

The second forces

\[
(k-1)x-m\in H,
\]

contradicting the minimality of \(k\).

Therefore the displayed equality is a canonical \(D_R=1\) witness.

---

# Immediate classification of the project controls

\[
\mathbb N_0:\quad m=1,\ \gamma=1,\ \operatorname{RCI}=1.
\]

\[
2\mathbb N_0:\quad m=2,\ \gamma=2,\ \operatorname{RCI}=1.
\]

\[
3\mathbb N_0:\quad m=3,\ \gamma=3,\ \operatorname{RCI}=1.
\]

By contrast,

\[
\langle2,3\rangle:\quad m=2,\ \gamma=1,\ \operatorname{RCI}=2,
\]

\[
\langle2,5\rangle:\quad m=2,\ \gamma=1,\ \operatorname{RCI}=2,
\]

\[
\langle3,4\rangle:\quad m=3,\ \gamma=1,\ \operatorname{RCI}=3.
\]

So the distinction is no longer empirical:

> In rank one, route closure is exactly the condition that the monoid already contains every nonnegative lattice point allowed by its generated group.

The missing ingredient is not merely "connectivity" and not merely the existence of ordinary-number gaps. It is failure of full rank-one lattice closure, equivalently failure of the least positive atom to be prime.
