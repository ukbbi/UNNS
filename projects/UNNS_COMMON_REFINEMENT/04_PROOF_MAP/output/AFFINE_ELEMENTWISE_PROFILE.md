# Exact Higher-Rank Affine Elementwise Route Profile

## Status

This note continues the established elementwise correspondence

\[
x\text{ primal}
\iff
\text{every endpoint equality containing }x\text{ admits a }2\times2\text{ refinement}.
\]

The immediate question was whether the rank-one phenomenon

\[
\text{finite non-primal core}\; +\; \text{cofinal all-primal tail}
\]

survives in the retained higher-rank positive-affine controls.

It does not.

For every retained affine failure control (`ARD>0`), the non-primal locus is infinite and
unbounded.  The exact geometry of that locus depends on the source of the atomic relation.

No bounded search is used as proof below.  The script
`scripts/BUILD_AFFINE_ELEMENTWISE.py` records the proved classifications and performs finite
regression checks of the explicit certificate families.

---

# 1. Main result

For the seven retained affine controls, the exact primal loci are:

| System | Exact primal locus | Non-primal locus unbounded? |
|---|---|---:|
| `FREE_N2` | all elements | no |
| `FREE_SKEW` | all elements | no |
| `NORMAL_PARITY` | \(\{0\}\cup\{(2m,2n):m,n\ge1\}\) | yes |
| `NORMAL_CONE2` | \(\{0\}\cup\{(x,y):y\text{ even},\ y\ge2,\ 2x-y\ge2\}\) | yes |
| `NONNORMAL_2D` | \(\{0\}\cup\{(2m,n):m\ge1,\ n\ge2\}\) | yes |
| `NORMAL_SQUARE3` | \(\{k(1,1,2):k\ge0\}\) | yes |
| `FREE_N3` | all elements | no |

Thus the retained higher-rank failure controls have **no analogue of the rank-one cofinal
all-primal tail**.

More strongly, three distinct unbounded defect geometries occur:

1. **congruence-channel persistence** — a full-dimensional bad congruence class survives
   arbitrarily far from the origin;
2. **hole-channel persistence** — nonnormality leaves an unbounded bad class and boundary strips;
3. **relation-dominated persistence** — in the non-simplicial square cone, primality survives only
   on a one-dimensional central ray.

---

# 2. General lemma: primal elements form a submonoid

Let \(H\) be a commutative cancellative monoid.  If \(p\) and \(q\) are primal, then \(p+q\)
is primal.

Indeed, suppose

\[
p+q+t=y+z.
\]

Primality of \(p\) gives

\[
p=p_1+p_2,\qquad p_1\le_H y,\qquad p_2\le_H z.
\]

Write \(y=p_1+y'\) and \(z=p_2+z'\).  Cancellation gives

\[
q+t=y'+z'.
\]

Primality of \(q\) gives \(q=q_1+q_2\) with \(q_1\le_H y'\) and \(q_2\le_H z'\).
Therefore

\[
p+q=(p_1+q_1)+(p_2+q_2)
\]

is a valid split below \(y,z\).

Hence the primal locus

\[
P(H)=\{x\in H:x\text{ is primal}\}
\]

is itself a submonoid.

This will be useful for `NORMAL_SQUARE3`.

---

# 3. `NORMAL_PARITY`

## 3.1 Monoid

Let

\[
H_P=\langle(2,0),(1,1),(0,2)\rangle
=\{(x,y)\in\mathbb N_0^2:x+y\equiv0\pmod2\}.
\]

Set

\[
A=(2,0),\qquad B=(0,2),\qquad C=(1,1).
\]

Then

\[
2C=A+B.
\]

Every element has a unique canonical form

\[
mA+nB+\varepsilon C,
\qquad m,n\in\mathbb N_0,
\quad\varepsilon\in\{0,1\}.
\]

Equivalently,

\[
(m,n,\varepsilon)\longmapsto(2m+\varepsilon,2n+\varepsilon).
\]

The only carry is

\[
(m,n,1)+(r,s,1)
=(m+r+1,n+s+1,0).
\]

## 3.2 Exact primal locus

\[
\boxed{
P(H_P)=\{0\}\cup\{(2m,2n):m,n\ge1\}.
}
\]

### Why the even-even interior is primal

Take

\[
X=(m,n,0),\qquad m,n\ge1,
\]

in canonical coordinates and suppose

\[
X+T=Y+Z.
\]

If \(Y\) and \(Z\) are not both in the odd class, no carry occurs on the right.  The free
coefficients of \(X\) can therefore be split coordinatewise between the free coefficients of
\(Y\) and \(Z\), giving an even-class divisor of each branch.

If \(Y\) and \(Z\) are both odd, their addition contributes exactly one carry \(A+B\).  The
equality implies that the residual free coefficients satisfy

\[
m-1\le A_Y+A_Z,
\qquad
n-1\le B_Y+B_Z.
\]

Because \(m,n\ge1\), write \(X\) as the sum of two odd-class elements.  Split the residual
coefficients \(m-1,n-1\) coordinatewise between the two branches.  Each odd summand then divides
the corresponding odd branch, and their sum is exactly \(X\).

Thus every even-even point with both coordinates positive is primal.

### Why every odd-odd point is non-primal

For

\[
X=(2m+1,2n+1),
\]

use

\[
X+(1,1)=(2m+2,0)+(0,2n+2).
\]

Any refinement across the two axis terms would have to split \(X\) into

\[
(2m+1,0)+(0,2n+1),
\]

but neither odd axis term belongs to \(H_P\).  Hence the equality is non-refinable at \(X\).

### Why the even boundary rays are non-primal

For \(k\ge1\),

\[
(2k,0)+(0,2)=(1,1)+(2k-1,1)
\]

is non-refinable at \((2k,0)\).  The vertical case is symmetric.

Therefore non-primality survives arbitrarily far both in the interior odd-odd congruence class and
along the two boundary rays.

---

# 4. `NORMAL_CONE2`

## 4.1 Monoid and exact isomorphism

Let

\[
H_C=\langle(1,0),(1,1),(1,2)\rangle
=\{(x,y)\in\mathbb N_0^2:0\le y\le2x\}.
\]

Define

\[
\Theta(x,y)=(2x-y,y).
\]

Then \(\Theta\) is a monoid isomorphism

\[
H_C\cong H_P.
\]

Indeed, \(2x-y\ge0\), \(y\ge0\), and

\[
(2x-y)+y=2x
\]

is even.  Conversely, for \((u,v)\in H_P\),

\[
\Theta^{-1}(u,v)=\left(\frac{u+v}{2},v\right).
\]

Primality is preserved by monoid isomorphism.

## 4.2 Exact primal locus

Transporting the `NORMAL_PARITY` classification gives

\[
\boxed{
P(H_C)
=
\{0\}\cup
\{(x,y):y\text{ even},\ y\ge2,\ 2x-y\ge2\}.
}
\]

Equivalently, with extreme rays

\[
A=(1,0),\qquad C=(1,2),
\]

\[
P(H_C)\setminus\{0\}
=\{mA+nC:m,n\ge1\}.
\]

The non-primal locus contains every odd-\(y\) interior point and both cone facets, so it is
unbounded and not boundary-confined.

---

# 5. `NONNORMAL_2D`

## 5.1 Monoid

Let

\[
H_N=\langle A,B,C\rangle,
\qquad
A=(2,0),\ B=(1,1),\ C=(0,1).
\]

The relation is

\[
2B=A+2C.
\]

The monoid has the exact description

\[
H_N
=
\{(x,y)\in\mathbb N_0^2:x\text{ even or }y\ge1\}.
\]

Thus the missing lattice points are precisely

\[
(2k+1,0).
\]

Every element has a unique canonical form

\[
mA+nC+\varepsilon B,
\qquad \varepsilon\in\{0,1\},
\]

or in coordinates

\[
(m,n,\varepsilon)\longmapsto(2m+\varepsilon,n+\varepsilon).
\]

Adding two odd-class terms produces the carry

\[
2B=A+2C.
\]

## 5.2 Exact primal locus

\[
\boxed{
P(H_N)
=
\{0\}\cup\{(2m,n):m\ge1,\ n\ge2\}.
}
\]

### Proof of primality

Let

\[
X=(m,n,0)
\]

in canonical coordinates, where \(m\ge1\) and \(n\ge2\), and suppose

\[
X+T=Y+Z.
\]

If \(Y,Z\) are not both odd-class elements, there is no carry between them.  The free \(A\)- and
\(C\)-coefficients of \(X\) can be divided coordinatewise between the two branches, using
only even-class divisors.

If \(Y,Z\) are both odd, their sum contributes the carry

\[
A+2C.
\]

The endpoint equality therefore leaves enough branch capacity to split

\[
m-1
\]

copies of \(A\) and

\[
n-2
\]

copies of \(C\).  Since \(m\ge1,n\ge2\), write \(X\) as the sum of two odd-class elements and
split those residual free coefficients coordinatewise.  Each odd summand divides its corresponding
odd branch.

Hence \(X\) is primal.

### Exact non-primal families

All remaining nonzero elements belong to one of four unbounded families.

For every odd-\(x\) point \(X=(2m+1,n)\), \(n\ge1\),

\[
X+(1,1)=(2m+2,0)+(0,n+1)
\]

is non-refinable: a split across the two axes would require the missing point \((2m+1,0)\).

For the vertical axis,

\[
(0,n)+(2,1)=(1,1)+(1,n),\qquad n\ge1,
\]

and the missing difference \((1,0)\) blocks refinement.

For \(m\ge1\),

\[
(2m,0)+(0,2)=(1,1)+(2m-1,1),
\]

and

\[
(2m,1)+(0,1)=(1,1)+(2m-1,1)
\]

are likewise non-refinable.

Thus the lattice-hole defect is not localized near the origin.  It propagates through an entire
odd-\(x\) bulk class and two low boundary strata.

---

# 6. `NORMAL_SQUARE3`

## 6.1 Monoid

Let

\[
A=(0,0,1),\quad
B=(1,0,1),\quad
C=(0,1,1),\quad
D=(1,1,1).
\]

Then

\[
A+D=B+C.
\]

The monoid is exactly

\[
H_S
=
\{(x,y,n)\in\mathbb N_0^3:0\le x\le n,\ 0\le y\le n\}.
\]

It is normal and saturated, but its cone is non-simplicial.

## 6.2 Exact primal locus

Define

\[
R=(1,1,2)=A+D=B+C.
\]

Then

\[
\boxed{
P(H_S)=\{kR:k\ge0\}.
}
\]

So the entire three-dimensional affine monoid has only a one-dimensional primal spine.

### Step 1: \(R\) is primal

Use the isomorphism

\[
\Phi(x,y,n)=(x,n-x,y,n-y)
\]

from \(H_S\) onto

\[
K=\{(p,q,r,s)\in\mathbb N_0^4:p+q=r+s\}.
\]

Under \(\Phi\),

\[
R\longmapsto Q=(1,1,1,1).
\]

Suppose

\[
Q+T=Y+Z
\]

in \(K\).  Coordinatewise, every position of \(Q\) is covered by \(Y\) or \(Z\).

If \(Y\ge Q\), take the entire \(Q\) from \(Y\).  If \(Z\ge Q\), take none from \(Y\).
Otherwise, because each element of \(K\) has equal left-pair and right-pair sums, every nonzero
branch has support in both pairs.  In each two-coordinate pair, choose one coordinate supplied by
\(Y\) whose complementary coordinate is supplied by \(Z\).  The two chosen coordinates form one
of the four binary atoms of \(K\), and its complement in \(Q\) is supported by \(Z\).

Therefore \(Q\), hence \(R\), is primal.

Since primal elements are closed under addition, every \(kR\) is primal.

### Step 2: every point off the central ray is non-primal

Take

\[
X=(x,y,n)\in H_S
\]

not of the form \(kR\), and set

\[
M=\max\{x,y,n-x,n-y\}.
\]

Then

\[
T=(M-x,M-y,2M-n)\in H_S
\]

and

\[
X+T=(M,M,2M).
\]

There are two cases.

#### Case A: \(n\ne x+y\)

Use

\[
(M,M,2M)=(M,0,M)+(0,M,M)=MB+MC.
\]

Every divisor of \(MB\) lies on the \(B\)-ray, and every divisor of \(MC\) lies on the
\(C\)-ray.  Therefore any refinement of \(X\) across these two branches would force

\[
X=rB+sC=(r,s,r+s),
\]

hence \(n=x+y\), contradiction.

#### Case B: \(n=x+y\) but \(x\ne y\)

Use instead

\[
(M,M,2M)=(0,0,M)+(M,M,M)=MA+MD.
\]

Every divisor of \(MA\) lies on the \(A\)-ray and every divisor of \(MD\) lies on the
\(D\)-ray.  A refinement would force

\[
X=rA+sD=(s,s,r+s),
\]

hence \(x=y\), contradiction.

The only remaining possibility is

\[
x=y,\qquad n=x+y=2x,
\]

which is exactly the ray \(kR\).

Thus the classification is complete.

---

# 7. Free controls

`FREE_N2`, `FREE_SKEW`, and `FREE_N3` are free commutative monoids on their atoms.
Therefore every element is primal and every endpoint equality refines.

They remain the exact all-primal controls.

---

# 8. Rank-one versus higher-rank obstruction topology

The contrast is now exact for the retained controls.

## Rank one

For a non-refinable numerical monoid:

\[
\text{finite gap set}
\Longrightarrow
\text{finite non-primal core}
\Longrightarrow
\text{cofinal all-primal tail}.
\]

The obstruction is eventually exhausted.

## Higher rank

For every retained nonfree affine control:

\[
\boxed{
\text{non-primality persists along unbounded structural directions.}
}
\]

There is no scalar threshold beyond which every element becomes primal.

The profiles are qualitatively different:

- `NORMAL_PARITY`: bad congruence class + bad boundary rays;
- `NORMAL_CONE2`: the same phenomenon transported into cone coordinates;
- `NONNORMAL_2D`: lattice-hole channel + low strips;
- `NORMAL_SQUARE3`: only a one-dimensional central primal spine survives.

Under natural exhaustions, the relative primal densities are:

\[
\begin{array}{c|c}
\text{system} & \text{limiting relative primal density}\\
\hline
\text{NORMAL_PARITY} & 1/2\\
\text{NORMAL_CONE2} & 1/2\\
\text{NONNORMAL_2D} & 1/2\\
\text{NORMAL_SQUARE3} & 0
\end{array}
\]

These density statements describe the proved exact loci under the stated natural exhaustions; they
are not being proposed as new invariants.

---

# 9. Consequence for the Conway / UNNS comparison

The finite analogy to the omnific proof is now sharper.

Rank one can become locally safe merely by passing beyond a finite gap region.  Higher rank shows
that this mechanism is not enough in general: independent atomic relations can produce defect
channels that remain present at arbitrarily large scale.

Therefore the omnific architecture should not be read as a transfinite version of
"eventually get past the bad finite part."

Its stronger structural role is:

\[
\boxed{
\text{descent must land in a primal base and transport must preserve primality,}
}
\]

so that no unbounded relation channel survives at any support class.

This distinguishes two mechanisms:

\[
\text{rank-one conductor saturation}
\quad\neq\quad
\text{global elimination of relation defects}.
\]

The successful omnific route requires the latter.

---

# 10. What is proved, and what is not

## Proved within this project

For all seven retained affine controls, the primal loci above are exact.
For all four retained affine failure controls, the non-primal locus is infinite and unbounded.
Hence the rank-one finite-core/cofinal-tail phenomenon fails in this higher-rank control corpus.

## Not yet proved

The project has **not yet proved** the universal statement

> every nonfree positive affine monoid of rank at least two has an unbounded non-primal locus.

That is now the natural theorem candidate suggested by the exact control results, but it requires a
separate general proof or a counterexample search.

---

# 11. Immediate next theorem question

The next mathematically substantive question is:

\[
\boxed{
\operatorname{rank}H\ge2,\ \operatorname{ARD}(H)>0
\quad\stackrel{?}{\Longrightarrow}\quad
H\setminus P(H)\text{ is unbounded}.
}
\]

If true, this would identify a genuine dimension-sensitive transition:

\[
\text{rank one: finite obstruction core}
\quad\longrightarrow\quad
\text{higher rank: persistent obstruction channels}.
\]

That is the correct next target before promoting the pattern to a general UNNS law.
