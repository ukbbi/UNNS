# Elementwise Route-Closure Profile

## Exact rank-one result and its Conway/UNNS significance

**Project:** `UNNS_COMMON_REFINEMENT`  
**Status:** proved rank-one project result + exact corpus classification + UNNS interpretation  
**Primary source corpus:** `02_NONREF/output/rank1_generator_scan.csv`

---

# 1. Question

After establishing

\[
x\text{ primal}
\iff
\text{every endpoint equality containing }x\text{ admits a }2\times2\text{ refinement},
\]

the immediate question was no longer only whether a whole monoid is globally refinable.

It became:

> **How is route traceability distributed element by element inside a monoid that fails global refinement?**

For the project's rank-one monoids, this question has an exact answer.

The answer is unexpectedly strong:

\[
\boxed{
\text{global refinement may fail even though all sufficiently large elements are primal.}
}
\]

Thus global non-refinement does **not** mean that route traceability fails everywhere.

---

# 2. Normalized rank-one setting

Let

\[
H=\langle g_1,\ldots,g_k\rangle\subseteq\mathbb N_0
\]

be a nonzero finitely generated additive submonoid, and let

\[
\gamma=\gcd(g_1,\ldots,g_k).
\]

Normalize by

\[
S=H/\gamma.
\]

Then \(S\) is a primitive numerical monoid. If \(S=\mathbb N_0\), the established rank-one theorem already gives global refinement and every element is primal.

Otherwise let \(c\) be the conductor of \(S\):

\[
c=\min\{n:\ n+\mathbb N_0\subseteq S\}.
\]

All gaps of \(S\) therefore lie in

\[
\{1,\ldots,c-1\}.
\]

---

# 3. Gap-Localization Lemma

Consider an endpoint equality in additive notation

\[
x+t=y+z,
\]

with distinguished corner \(x\in S\).

## Lemma

If this equality has no \(2\times2\) refinement, then

\[
\boxed{
|x-y|\notin S,
\qquad
|x-z|\notin S.
}
\]

Hence

\[
\boxed{
|x-y|<c,
\qquad
|x-z|<c.
}
\]

### Proof

If \(y\ge x\) and \(y-x\in S\), then

\[
x=x+0,
\]

and the equality refines immediately with the complementary pieces \(y-x\) and \(z\).

If \(x\ge y\) and \(x-y\in S\), then

\[
x=y+(x-y),
\]

and the equality again refines immediately, with the remaining corner equal to \(t\).

The same argument applies to \(z\).

Therefore a failed square can only occur when both distances from \(x\) are gaps of the normalized numerical monoid. Since every integer at least \(c\) lies in \(S\), both distances are strictly below \(c\). ∎

## Consequence

For a fixed \(x\), non-primality is an **exactly finite** question. One does not need to search arbitrary \(y,z\); only the finite gap window

\[
x\pm(\mathbb N_0\setminus S)
\]

can contain a counterexample.

This is what makes the elementwise corpus classification exact rather than merely a bounded scan.

---

# 4. Cofinal Primal-Tail Theorem

The gap localization yields a stronger theorem.

## Theorem

Let \(S\) be a primitive numerical monoid with conductor \(c>0\). Then

\[
\boxed{
x\in S,\quad x\ge4c\quad\Longrightarrow\quad x\text{ is primal}.}
\]

Equivalently, in the original unnormalized monoid \(H\),

\[
\boxed{
x\ge4\gamma c\quad\Longrightarrow\quad x\text{ is primal}.}
\]

### Proof

Assume for contradiction that

\[
x+t=y+z
\]

is non-refinable with \(x\ge4c\).

By the gap-localization lemma, any failed square must have \(y\) and \(z\) within a gap-distance of \(x\).

If \(y\ge x\), use

\[
x=(x-c)+c.
\]

Because \(x-c\ge3c\), both pieces lie in \(S\). Moreover,

\[
y-(x-c)=y-x+c\ge c
\]

and, since \(z>x-c\ge3c\),

\[
z-c\ge2c.
\]

All complementary pieces are therefore in \(S\), producing a refinement. The same argument applies if \(z\ge x\).

Hence a failed square would require

\[
y<x,
\qquad
z<x.
\]

Write

\[
y=x-r,
\qquad
z=x-s,
\]

where the gap-localization lemma gives

\[
0<r,s<c.
\]

Then

\[
t=x-r-s\ge4c-2(c-1)>2c.
\]

Now split

\[
x=(y-c)+(r+c).
\]

Both pieces belong to \(S\): \(y-c\ge2c\) and \(r+c\ge c\). The complementary pieces are

\[
c
\]

and

\[
t-c\ge c.
\]

Thus all four entries lie in \(S\), giving a refinement and contradicting the assumed failure.

Therefore every \(x\ge4c\) is primal. ∎

---

# 5. Finite non-primal obstruction core

Define descriptively

\[
\mathcal O(S)=\{x\in S:\ x\text{ is non-primal}\}.
\]

The theorem gives

\[
\boxed{
\mathcal O(S)\subseteq[1,4c).
}
\]

So every finitely generated rank-one monoid has only a **finite non-primal obstruction core** after gcd normalization.

Combining this with the project's established rank-one theorem gives:

\[
\boxed{
H\text{ globally refinable}
\iff
\mathcal O(H)=\varnothing.
}
\]

For the non-refinable rank-one systems, the failure is therefore not an everywhere failure. It is caused by a finite set of structurally non-traceable elements.

Above that core, elementwise route closure is restored even though the monoid remains globally non-refinable.

---

# 6. Exact corpus classification

The reproducible script

```text
scripts/BUILD_ELEMENTWISE_PROFILE.py
```

applies the two proved lemmas to the existing 793-system rank-one corpus.

The result is exact:

```text
793 total rank-one systems
280 globally refinable
513 globally non-refinable
```

For the 280 globally refinable systems, normalization contains generator \(1\), so the monoid is \(\mathbb N_0\) after scaling and every element is primal.

For all 513 globally non-refinable systems, the entire non-primal set is classified by checking the finite interval below \(4c\) and using gap localization for each candidate element.

## Corpus-level result

Among the 513 globally non-refinable systems:

- **414 / 513 = 80.70%** already contain primal elements **below** the onset of their final all-primal tail;
- the median non-primal obstruction-core size is **18** elements;
- the largest obstruction core in this corpus contains **130** elements;
- the exact tail onset divided by the conductor ranges from **2.1** to **3.5**, with median **2.6667**;
- the proved universal bound is \(4c\); the smaller corpus ratios are observations, not promoted to a theorem.

This means that in most failure systems the elementwise profile is not a single clean transition

```text
non-primal -> primal.
```

Instead it can interlace:

```text
non-primal / primal / non-primal / ... / final primal tail.
```

Only the last tail is guaranteed to remain primal forever.

---

# 7. Flagship examples

## \(H=\langle2,3\rangle\)

Here

\[
c=2.
\]

The exact non-primal elements are

\[
2,3,4,5.
\]

Every element

\[
x\ge6
\]

is primal.

Thus the flagship equality

\[
2+4=3+3
\]

comes entirely from the finite obstruction core, while the same monoid is elementwise route-closed at every sufficiently large corner.

## \(H=\langle2,5\rangle\)

Here

\[
c=4.
\]

The final primal tail begins at

\[
12,
\]

but \(10\) is already primal before that tail. This is the simplest corpus example showing that primality can reappear locally before the last non-primal obstruction has disappeared.

## \(H=\langle4,7\rangle\)

Here

\[
c=18.
\]

The exact final primal tail begins at

\[
42,
\]

while the earlier elements

\[
28,32,35,36,39,40
\]

are already primal.

This gives a visibly interlaced route-closure profile inside a globally non-refinable monoid.

## \(H=\langle11,12\rangle\)

Here

\[
c=110.
\]

The exact final tail begins at

\[
231,
\]

and the finite obstruction core contains 130 non-primal elements. Yet 45 primal elements already occur below the final tail onset; the first is \(132\).

---

# 8. What this changes in the Conway comparison

The previous comparison correctly identified

\[
\text{every element primal}
\]

as the surviving algebraic property behind global refinement.

The elementwise result now adds an important qualification:

\[
\boxed{
\text{a system can fail globally while primal traceability survives on a large, even cofinal, subset.}
}
\]

So the distinction is no longer merely

```text
refinable system / non-refinable system.
```

There is an internal profile.

For rank one:

```text
finite obstruction core
        +
cofinal primal tail.
```

The conductor supplies the finite structural threshold beyond which missing additive splittings can no longer sustain a corner-level refinement defect.

---

# 9. Finite analogue of the omnific descent mechanism

This gives a substantially cleaner comparison with the audited Conway proof architecture.

## Rank one

```text
gaps below conductor
        ↓
possible local obstruction
        ↓
finite non-primal core
        ↓
conductor saturation
        ↓
cofinal primal tail
```

The mechanism **does not** establish global refinement, because the finite core still contains non-primal elements.

## Omnific candidate proof

The audited source architecture instead has the form

```text
finite/base primality
        +
local quotient refinement
        +
strict support-class descent
        +
ambient transport
        ↓
every element primal
        ↓
four-factor refinement.
```

The analogy should not be overstated: conductor order and support-class order are different mathematical objects.

But the structural comparison is now precise enough to be useful:

> **Both mechanisms reduce route-closure difficulty by moving into a region/level where local factor routing is controlled. The decisive difference is what happens at the residual base.**

In the non-refinable rank-one systems, a finite obstruction core survives.

In the omnific candidate architecture, the base-primality component is exactly what is intended to prevent such an unresolved residual core.

Thus the most informative finite analogue of the transfinite mechanism is not simply “descent.” It is:

\[
\boxed{
\text{controlled reduction}
+
\text{closure of the residual base}
\Longrightarrow
\text{global primal traceability}.
}
\]

That statement is an interpretation of the comparison, not a new general theorem.

---

# 10. Immediate next test

Rank one has now revealed something very specific: global failure is compatible with a finite non-primal core and a cofinal all-primal tail.

The next exact question should move to the retained affine controls:

> **Does higher rank preserve a finite obstruction core, or can independent atomic relations generate non-primality along unbounded directions?**

That test directly connects the elementwise result to the established higher-rank finding that lattice saturation alone is insufficient and atomic relations become an independent obstruction.

No new generic confluence framework is needed.
