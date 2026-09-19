# Route Closure Criterion — UNNS Form

## Exact mathematical domain

This statement is proved here only for nonzero additive submonoids

\[
H\subseteq\mathbb N_0.
\]

It is not asserted as a universal theorem for arbitrary UNNS ladders.

## Endpoint relation

\[
R_1=(a,b),\qquad R_2=(c,d),\qquad I(R)=\sum R.
\]

Endpoint equivalence is

\[
I(R_1)=I(R_2).
\]

Structural route closure means that a common refinement matrix exists:

\[
\begin{matrix}
e & f\\
g & h
\end{matrix}
\]

with

\[
a=e+f,\quad b=g+h,\quad c=e+g,\quad d=f+h.
\]

## Exact rank-one criterion

Let

\[
m=\min(H\setminus\{0\}),\qquad
\gamma=\gcd(H).
\]

Define

\[
\operatorname{RCI}(H)=m/\gamma.
\]

Then

\[
\boxed{\operatorname{RCI}=1\iff\text{every endpoint equality has structural route closure}.}
\]

And

\[
\boxed{\operatorname{RCI}>1\iff\text{there exists an exact }D_R=1\text{ endpoint equality}.}
\]

## Structural meaning

The generated group permits lattice positions

\[
\gamma\mathbb N_0.
\]

The actual monoid supplies only

\[
H.
\]

When

\[
H=\gamma\mathbb N_0,
\]

all permitted rank-one lattice positions needed for splitting are present.

When

\[
H\subsetneq\gamma\mathbb N_0,
\]

some permitted internal positions are absent. Those omissions can block the cross-routing required by a common refinement.

Therefore the rank-one result makes the earlier UNNS statement precise:

\[
\text{same endpoint}
\not\Rightarrow
\text{common ancestry}
\]

unless the substrate is closed under the internal splitting positions required by its own lattice.

## Relation to the earlier "blocking-hole" observation

The `<2,3>` flagship case had the missing value `1`.

The theorem now shows that `1` was not an accidental bad value. It was evidence that

\[
H\neq \operatorname{Sat}_{lat}(H).
\]

Thus the former empirical phrase **splitting hole** becomes the exact rank-one obstruction:

\[
\operatorname{Sat}_{lat}(H)\setminus H\neq\varnothing.
\]

The theorem also explains why `2N` and `3N` remain fully refinable even though they omit many ordinary integers: those omitted integers are not lattice positions in their own generated groups.

This is the first theorem-level realization of **structural route closure** in the project.
