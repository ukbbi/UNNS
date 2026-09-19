# AFFINE ROUTE-CLOSURE REPORT

## Main result

For a positive affine monoid \(H\),

\[
H\text{ has global common refinement}
\iff
H\cong\mathbb N_0^r.
\]

Equivalently, with \(\mathcal A(H)\) the atoms and
\(r=\operatorname{rank}\operatorname{gp}(H)\),

\[
\boxed{
\operatorname{ARD}(H)
=
|\mathcal A(H)|-r
=
0.
}
\]

## What survived from rank one?

**Lattice saturation survives as a necessary condition.**

But it is no longer sufficient.

The exact counterexample

\[
H=\langle(2,0),(1,1),(0,2)\rangle
\]

is already saturated in its own parity lattice, yet

\[
(2,0)+(0,2)=(1,1)+(1,1)
\]

is a nontrivial relation between atoms.

Thus endpoint equivalence survives while structural ancestry is ambiguous.

## What new ingredient appears?

Higher rank exposes **atomic independence**.

Geometrically the correct condition is not merely

\[
H=C\cap L,
\]

but

\[
H=C\cap L
\]

together with \(C\) being **unimodular simplicial** relative to \(L\).

So the rank-one law

\[
\text{route closure}=\text{lattice closure}
\]

generalizes to

\[
\boxed{
\text{route closure}
=
\text{lattice closure}
+
\text{independent primitive directions}.
}
\]

## Exact examples

| System | rank | atoms | ARD | saturated? | refinement |
|---|---:|---:|---:|---|---|
| \(N_0^2\) | 2 | 2 | 0 | yes | yes |
| \(\langle(2,0),(1,1)\rangle\) | 2 | 2 | 0 | yes (relative lattice) | yes |
| parity monoid \(\langle(2,0),(1,1),(0,2)\rangle\) | 2 | 3 | 1 | yes | no |
| \(\langle(1,0),(1,1),(1,2)\rangle\) | 2 | 3 | 1 | yes | no |
| \(\langle(2,0),(1,1),(0,1)\rangle\) | 2 | 3 | 1 | no | no |
| normal square cone in rank 3 | 3 | 4 | 1 | yes | no |
| \(N_0^3\) | 3 | 3 | 0 | yes | yes |

## Why this matters for Conway

The finite affine theorem gives the chain

\[
\text{refinement}
\iff
\text{irreducibles prime}
\iff
\text{free atomic routing}.
\]

The candidate omnific proof reportedly contains the intermediate result that irreducible
omnific integers are prime.

That is now a mathematically precise point of contact.

The next comparison should ask what replaces the affine ingredients that no longer exist
in the omnific setting:

1. finite generation;
2. a finite atom basis;
3. finite-dimensional relation rank.

The proof's support ranks, Archimedean classes and transfinite descent are the natural
candidates for the replacement mechanism.
