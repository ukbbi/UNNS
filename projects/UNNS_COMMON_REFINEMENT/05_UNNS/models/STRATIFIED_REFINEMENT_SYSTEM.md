# Stratified Refinement System (SRS)

## Purpose

This definition is the formal setting in which the provisional TRC-I roles

\[
I,\ P,\ D,\ L,\ R
\]

become actual mathematical axioms.

It is deliberately abstract enough to include:
- the finite affine control as a degenerate finite-rank case;
- filtered / graded factorization systems;
- transfinite support constructions of the kind visible in the candidate Conway proof.

It is not asserted that every mathematical refinement problem naturally forms an SRS.

---

# 1. Refinement obligations

An **endpoint obligation** is an object \(q\) representing an equality of two routes.

The system has a class

\[
\mathcal Q=\bigcup_{\alpha<\Theta}\mathcal Q_\alpha
\]

indexed by an ordinal \(\Theta\).

For

\[
q\in\mathcal Q_\alpha
\]

write

\[
\rho(q)=\alpha
\]

for its structural rank.

Each obligation has a set

\[
W(q)
\]

of exact common-refinement witnesses.

The system has **global route closure** when

\[
W(q)\neq\varnothing
\qquad
\text{for every }q\in\mathcal Q.
\]

---

# 2. Two kinds of obligations

Every obligation is declared either:

1. **local/successor type**, or
2. **limit type**.

This distinction is structural, not merely whether the ordinal \(\rho(q)\) happens to be
a successor or a limit ordinal.

A local obligation is solved by refining its leading stratum and pushing any remaining
defect to lower rank.

A limit obligation is solved from a coherent family of lower-rank approximants.

---

# 3. Local shadows

For every local obligation \(q\), the SRS supplies a **leading shadow**

\[
\sigma(q)
\]

which is itself an endpoint equality in a commutative conical cancellative monoid

\[
G_q.
\]

The shadow monoid has a specified decomposition

\[
G_q
=
\bigoplus_{j\in J_q} C_{q,j},
\]

where elements have finite support.

The \(C_{q,j}\) are called **local coefficient monoids**.

A shadow refinement witness is an ordinary \(2\times2\) refinement matrix in \(G_q\).

Write

\[
\overline W(q)
\]

for the set of shadow refinement witnesses.

---

# 4. Residual obligations and assembly

Given a local obligation \(q\) and a shadow witness

\[
\bar w\in\overline W(q),
\]

the SRS supplies a finite set

\[
\operatorname{Res}(q,\bar w)\subseteq\mathcal Q
\]

of residual obligations and an assembly operation

\[
\operatorname{Asm}_{q,\bar w}:
\prod_{r\in\operatorname{Res}(q,\bar w)} W(r)
\longrightarrow
W(q).
\]

If the residual set is empty, the empty product is a singleton, so assembly directly
produces a witness for \(q\).

This is the exact place where a leading/graded refinement is lifted back into the original
system.

---

# 5. Limit approximants

For every limit-type obligation \(q\in\mathcal Q_\alpha\), the SRS supplies:

- a cofinal directed set \(B_q\subseteq\alpha\);
- approximating obligations \(q_\beta\in\mathcal Q_\beta\) for \(\beta\in B_q\);
- restriction maps

\[
r_{\gamma\beta}:W(q_\gamma)\to W(q_\beta)
\qquad
(\beta\le\gamma,\ \beta,\gamma\in B_q)
\]

satisfying the inverse-system identities.

The coherent witness space is

\[
\varprojlim_{\beta\in B_q} W(q_\beta).
\]

The SRS also supplies a reconstruction map

\[
\operatorname{Rec}_q:
\varprojlim_{\beta\in B_q}W(q_\beta)
\longrightarrow
W(q).
\]

---

# The five axioms

## I — Independent Local Structure

For every local \(q\),

\[
G_q=\bigoplus_{j\in J_q}C_{q,j}
\]

is an **internal independent decomposition**: there are no cross-coordinate relations.

Equivalently, equality in \(G_q\) is coordinatewise equality in the coefficient monoids.

This is the abstract form of:
- `ARD=0` in the finite affine case;
- associated-graded algebraic independence / polynomial-coordinate separation in the
  Conway bridge.

---

## P — Prime Traceability

Every coefficient monoid \(C_{q,j}\) is atomic, and every irreducible element of
\(C_{q,j}\) is prime.

Therefore factor identity is traceable inside every active local coordinate.

This is the exact local form of the earlier phrase **irreducible -> prime**.

---

## D — Well-Founded Descent

For every local obligation \(q\), every shadow witness
\(\bar w\in\overline W(q)\), and every residual

\[
r\in\operatorname{Res}(q,\bar w),
\]

we have

\[
\rho(r)<\rho(q).
\]

Thus residual refinement cannot recurse at equal or increasing structural rank.

---

## L — Coherent Limit Closure

For every limit obligation \(q\), if

\[
W(q_\beta)\neq\varnothing
\qquad
\text{for all }\beta\in B_q,
\]

then

\[
\varprojlim_{\beta\in B_q}W(q_\beta)\neq\varnothing.
\]

So individually solvable lower stages possess at least one **coherent** witness family.

This is stronger than ordinary pointwise completeness and is exactly what the earlier
`CM_L` countermodel lacked.

---

## R — Sound Reconstruction

Two reconstruction statements are required.

### R1 — local lift/assembly

For every local \(q\) and every shadow witness
\(\bar w\in\overline W(q)\),

\[
\operatorname{Res}(q,\bar w)
\]

and

\[
\operatorname{Asm}_{q,\bar w}
\]

are defined, finite, and sound: exact witnesses for all residual obligations assemble to
an exact witness of \(q\).

### R2 — limit reconstruction

For every limit \(q\),

\[
\operatorname{Rec}_q
\]

is defined and sound: every coherent lower-rank witness family reconstructs to an exact
witness in \(W(q)\).

This precision matters.

`R` is not merely "the representation is faithful." It is the actual local-to-global
lifting/reassembly principle required by the theorem.

---

# Local Refinement Lemma

Under \(I+P\),

\[
\overline W(q)\neq\varnothing
\]

for every local obligation \(q\).

## Proof

Fix one coefficient monoid \(C=C_{q,j}\).

Because \(C\) is atomic and every irreducible is prime, factorization into irreducibles is
unique up to order.

Indeed, given

\[
p_1+\cdots+p_m=q_1+\cdots+q_n,
\]

primality of \(p_1\) routes it into one of the \(q_k\); since \(q_k\) is irreducible this
forces equality, and cancellation plus induction finishes the argument.

Therefore \(C\) is a free commutative monoid on its irreducibles and has the Riesz
refinement property.

A direct sum of refinement monoids has coordinatewise refinement.

Hence

\[
G_q=\bigoplus_j C_{q,j}
\]

has refinement, and every endpoint equality \(\sigma(q)\) possesses a shadow witness.

\[
\Box
\]

This lemma is the exact point where `I` and `P` cooperate.

Neither is silently identified with global route closure.

---

# Scope note

The SRS definition is operational by design.

The theorem to follow does **not** claim that `irreducible -> prime` alone implies
transfinite refinement in arbitrary algebraic structures.

It says that once a problem admits this specific stratified architecture, the five explicit
axioms are sufficient.
