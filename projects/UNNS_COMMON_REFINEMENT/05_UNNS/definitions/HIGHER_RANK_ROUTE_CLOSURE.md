# Higher-Rank Structural Route Closure

## Exact scope

This result concerns positive affine monoids, not arbitrary UNNS structures.

Within that domain, common refinement now has a complete structural criterion.

## Rank-one result

Previously:

\[
\operatorname{RCI}(H)=1
\]

was equivalent to global route closure.

That rank-one result can be understood as complete occupation of the allowed
nonnegative lattice.

## What changes in higher rank

Lattice completion survives as a necessary ingredient, but it no longer determines
route closure by itself.

The new obstruction is an **atomic relation**.

Let

\[
\mathcal A(H)=\{u_1,\ldots,u_s\}
\]

be the atoms and let

\[
r=\operatorname{rank}\operatorname{gp}(H).
\]

Define

\[
\operatorname{ARD}(H)=s-r.
\]

This is the rank of the independent relation space among atomic directions.

Then, for positive affine monoids,

\[
\boxed{
\operatorname{ARD}=0
\iff
\text{global common refinement}.
}
\]

Thus there are now two complementary UNNS diagnostics:

- **RCI** — rank-one lattice/splitting closure.
- **ARD** — higher-rank atomic-relation defect.

## Structural meaning

If \(\operatorname{ARD}>0\), distinct atomic routing histories can reach the same endpoint:

\[
\sum_i n_i u_i
=
\sum_i m_i u_i,
\qquad
(n_i)\ne(m_i).
\]

The endpoint therefore loses information about atomic ancestry.

That is exactly the configuration in which common refinement can fail.

If \(\operatorname{ARD}=0\), every endpoint retains a unique atomic coordinate vector.
The substrate is then free:

\[
H\cong\mathbb N_0^r,
\]

and every equality can be refined coordinatewise.

## Key discovery

Rank one hid a geometric condition.

Every rank-one pointed cone is automatically simplicial and unimodular relative to its
own lattice. Therefore only the saturation defect was visible.

Higher rank exposes the missing condition:

\[
\boxed{
\text{structural route closure requires both occupancy and independence}.
}
\]

- **Occupancy:** the allowed lattice positions needed by the cone are present.
- **Independence:** the primitive structural directions do not satisfy competing atomic relations.

## Bridge toward the omnific problem

The affine theorem makes one feature especially important:

\[
\boxed{
\text{refinement}\Longrightarrow
\text{irreducibles are prime}.
}
\]

And in the finite affine setting the converse, together with atomicity, forces the entire
monoid to be free.

This makes the reported omnific proof step

> irreducible omnific integers are prime

structurally significant rather than incidental.

The next comparison should therefore track three objects in the omnific proof:

1. **irreducible → prime traceability;**
2. **the replacement for finite atomic independence;**
3. **the well-founded support/Archimedean descent that substitutes for finite generation.**

That is now the precise bridge from the affine theorem to Conway's domain.
