# SRS Route-Closure Theorem

## Theorem

Let

\[
\mathfrak S
\]

be a Stratified Refinement System satisfying the five axioms

\[
I,\ P,\ D,\ L,\ R.
\]

Then \(\mathfrak S\) has global route closure:

\[
\boxed{
I+P+D+L+R
\Longrightarrow
W(q)\neq\varnothing
\quad
\text{for every }q\in\mathcal Q.
}
\]

Equivalently:

\[
\boxed{
I+P+D+L+R
\Longrightarrow
\text{global common refinement}
}
\]

**inside the category of Stratified Refinement Systems.**

---

# Proof

We prove, by transfinite induction on \(\alpha<\Theta\), the statement

\[
P(\alpha):
\qquad
W(q)\neq\varnothing
\quad
\text{for every }q\in\mathcal Q_\alpha.
\]

Assume that

\[
P(\beta)
\]

holds for every

\[
\beta<\alpha,
\]

and fix

\[
q\in\mathcal Q_\alpha.
\]

There are two cases.

---

## Case 1 — \(q\) is local/successor type

By **I** and **P**, the Local Refinement Lemma applies to the leading shadow

\[
\sigma(q)
\]

in

\[
G_q.
\]

Hence there exists

\[
\bar w\in\overline W(q).
\]

By **R1**, this shadow witness determines a finite residual set

\[
\operatorname{Res}(q,\bar w)
\]

and a sound assembly map

\[
\operatorname{Asm}_{q,\bar w}.
\]

By **D**, every residual obligation

\[
r\in\operatorname{Res}(q,\bar w)
\]

has strictly lower rank:

\[
\rho(r)<\alpha.
\]

Therefore the induction hypothesis gives

\[
W(r)\neq\varnothing
\]

for every residual \(r\).

Choose one exact witness

\[
w_r\in W(r)
\]

for each residual.

Because the residual set is finite, this requires only finite choice.

Apply the sound assembly map:

\[
w
=
\operatorname{Asm}_{q,\bar w}\big((w_r)_r\big).
\]

By **R1**,

\[
w\in W(q).
\]

Thus

\[
W(q)\neq\varnothing.
\]

---

## Case 2 — \(q\) is limit type

For every

\[
\beta\in B_q
\]

we have

\[
\beta<\alpha.
\]

Therefore the induction hypothesis gives

\[
W(q_\beta)\neq\varnothing.
\]

By **L**, pointwise solvability of all approximants implies coherent solvability:

\[
\varprojlim_{\beta\in B_q}W(q_\beta)\neq\varnothing.
\]

Choose a coherent family

\[
(w_\beta)_{\beta\in B_q}
\in
\varprojlim_{\beta\in B_q}W(q_\beta).
\]

By **R2**,

\[
w
=
\operatorname{Rec}_q((w_\beta)_\beta)
\]

is an exact witness for \(q\).

Hence

\[
W(q)\neq\varnothing.
\]

---

Both cases establish \(P(\alpha)\).

By transfinite induction,

\[
W(q)\neq\varnothing
\]

for every obligation in the SRS.

Therefore the system has global route closure.

\[
\boxed{\Box}
\]

---

# Why the theorem is not tautological

None of the five axioms individually asserts

\[
W(q)\neq\varnothing
\]

for every global obligation.

Their jobs are separated:

- **I** removes cross-coordinate relations at the active stratum.
- **P** turns local irreducibles into traceable prime factors.
- **D** guarantees that residual problems lie below the current rank.
- **L** supplies coherence at genuine limit stages.
- **R** transfers solved local/residual data back to the original obligation.

The conclusion appears only after transfinite induction combines the five roles.

The five previously constructed countermodels show that none of the roles can simply be
deleted from this architecture.

---

# Relation to the finite affine theorem

A positive affine refinement problem becomes a finite-rank SRS with no genuine limit nodes.

Then:

- \(I\) is atomic-coordinate independence;
- \(P\) is irreducible \(\to\) prime;
- \(D\) is ordinary finite descent;
- \(L\) is vacuous;
- \(R\) is coordinate reconstruction.

The SRS theorem therefore collapses to the previously established affine criterion.

---

# Relation to the candidate Conway architecture

The public candidate proof has structural components matching the five SRS roles:

- **I** — associated-graded algebraic independence and polynomial presentations;
- **P** — primality results and irreducible omnific integers being prime;
- **D** — strict decrease of support-class order type and transfinite extension;
- **L** — common-tail cofinality / quotient completeness;
- **R** — normal-form reconstruction and transfer to the omnific integer part.

This does **not** constitute an independent proof of Conway's theorem.

It says something different:

> If the Conway development really realizes an SRS satisfying the five axioms, then its global
> refinement conclusion fits a general transfinite route-closure theorem rather than being an
> isolated phenomenon.

Verifying that realization axiom-by-axiom is the next bridge-validation task.

---

# Status

**THEOREM — proved from the SRS axioms as defined in this project.**

What remains open is not the internal implication.

What remains open is the **realization problem**:

> Which naturally occurring mathematical systems satisfy the SRS axioms, and can the candidate
> omnific proof be mapped to them without strengthening or reinterpreting its actual lemmas?


---

# Conway realization audit — correction

A source-level audit of the candidate Conway repository at commit
`264445c93b78554c408e99e4e7f663693b4e91ab` found that the proof does **not** instantiate the
current SRS axioms literally.

The SRS theorem above remains valid as an abstract theorem.

However:

- `D` has an exact realization;
- `R1` has a strong realization after re-encoding obligations as primality/divisibility problems;
- `I` and `L` are only analogical/partial matches;
- `P` is not the load-bearing premise of the final proof;
- `R2` is not used in the SRS inverse-limit sense.

The candidate proof is more faithfully described as a transfinite proof that **every element is
primal**, followed by the generic equivalence between global primality and four-factor refinement.

See:
`03_OMNIFIC/output/SRS_CONWAY_AUDIT.md`.
