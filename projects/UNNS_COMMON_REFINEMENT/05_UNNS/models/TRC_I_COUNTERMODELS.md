# TRC-I Falsification — Five Explicit Countermodels

## Aim

The provisional schema was

\[
I+P+D+L+R
\stackrel{?}{\Longrightarrow}
\text{Transfinite Route Closure}.
\]

The next question was not whether the five labels could be made to look plausible.
It was whether each role can be removed while the other four remain present and route closure fails.

The project now contains five explicit countermodels.

A critical distinction is retained:

- `CM_I` and `CM_P` are algebraic/stratified constructions.
- `CM_D`, `CM_L`, and `CM_R` are abstract refinement-system countermodels because
  \(D,L,R\) describe recursion, limit handling, and local-to-global reconstruction rather
  than ordinary monoid identities.

The countermodels therefore establish **logical independence inside the TRC test framework**,
not a claim that every condition is necessary in every conceivable algebraic category.

---

# CM-I — Remove Local Independence

Let

\[
B=\langle
u=(1,0),\,
v=(1,1),\,
w=(1,2)
\rangle\subseteq\mathbb N_0^2.
\]

There is an atomic relation

\[
u+w=2v.
\]

This equality has no common refinement in \(B\).

Now densify the construction:

\[
H_I=\{0\}\cup(\mathbb Q_{>0}\times B).
\]

Every nonzero element is reducible:

\[
(q,b)
=
(q/2,0)
+
(q/2,b).
\]

So \(H_I\) has **no irreducibles at all**.

Therefore condition \(P\),

> every irreducible is prime,

holds vacuously.

But the endpoint equality

\[
(1,u)+(1,w)=(1,v)+(1,v)
\]

cannot refine: projecting any hypothetical refinement to the \(B\)-coordinate would
give a refinement of \(u+w=2v\), which does not exist.

Thus:

\[
\boxed{\neg I,\ P,\ D,\ L,\ R,\ \neg\text{RouteClosure}.}
\]

This is important because it separates independence failure from prime traceability:
prime traceability alone says nothing when the domain is atomless.

---

# CM-P — Remove Prime Traceability

Take

\[
H=\langle2,3\rangle.
\]

Stratify the two atoms into separate one-generator local strata:

\[
S_2=\langle2\rangle,
\qquad
S_3=\langle3\rangle.
\]

Each local stratum is rank-one free, so the local independence requirement \(I\) holds.

But \(2\) is not prime in \(H\):

\[
2\le_H 3+3
\]

because

\[
6-2=4\in H,
\]

while

\[
2\not\le_H3
\]

because

\[
3-2=1\notin H.
\]

The exact endpoint equality

\[
2+4=3+3
\]

has no refinement witness.

Hence:

\[
\boxed{I,\ \neg P,\ D,\ L,\ R,\ \neg\text{RouteClosure}.}
\]

This shows why graded/local independence cannot replace factor traceability across strata.

---

# CM-D — Remove Well-Founded Descent

Define a deterministic refinement-obligation machine

\[
X\to Y\to X.
\]

The initial endpoint equality produces obligation \(X\).
A route-closure witness would require reaching terminal state \(W\).

But

\[
W
\]

is unreachable.

There is no branching, no local relation, no limit stage, and reconstruction is identity.
So \(I,P,L,R\) hold in the operational model.

The sole obstruction is the directed cycle:

\[
X\to Y\to X\to\cdots.
\]

No well-founded rank can strictly decrease along every obligation step.

Thus:

\[
\boxed{I,\ P,\ \neg D,\ L,\ R,\ \neg\text{RouteClosure}.}
\]

This countermodel applies to the **recursive proof architecture**. It should not be read as
claiming that every algebraic refinement monoid must possess a distinguished descending rank.

---

# CM-L — Remove Limit Closure

For each finite stage \(n<\omega\), let the unique local refinement witness be

\[
w_n=1^n.
\]

The witnesses are perfectly compatible:

\[
w_n
=
w_{n+1}\restriction n.
\]

Every predecessor stage is solved.

The structural rank is the ordinal stage index, so transfinite induction is well founded.
Local independence and prime traceability are trivial, and finite reconstruction works.

Now define an endpoint equality at stage \(\omega\).

Its only possible global witness is

\[
1^\omega.
\]

But the witness universe contains **finite strings only**.

So the compatible family

\[
(w_n)_{n<\omega}
\]

has no represented limit.

Hence:

\[
\boxed{I,\ P,\ D,\ \neg L,\ R,\ \neg\text{RouteClosure}.}
\]

This is the cleanest justification yet for keeping `L` separate from `D`.

Well-founded transfinite descent does not itself supply the limit object.

---

# CM-R — Remove Reconstruction

Take three independent local patches

\[
P_1,P_2,P_3.
\]

Each has local witness

\[
1.
\]

So the local witness family is

\[
(1,1,1).
\]

Impose the global reconstruction law

\[
x_1+x_2+x_3\equiv0\pmod2.
\]

Every local problem is solved.
There is no recursive or limit obstruction.

But

\[
1+1+1\equiv1\pmod2.
\]

Thus the local witnesses cannot be reconstructed into a global witness.

Therefore:

\[
\boxed{I,\ P,\ D,\ L,\ \neg R,\ \neg\text{RouteClosure}.}
\]

This is a pure local-to-global obstruction.

---

# Falsification matrix

| Model | I | P | D | L | R | Route closure |
|---|---:|---:|---:|---:|---:|---:|
| CM-I | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ |
| CM-P | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ |
| CM-D | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ |
| CM-L | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ |
| CM-R | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

Within the formal TRC test framework, all five roles are therefore independently load-bearing.

---

# What this does and does not prove

It **does prove** that the five roles are not redundant in the abstract schema as currently formalized.

It **does not yet prove**

\[
I+P+D+L+R
\Longrightarrow
\text{global common refinement}
\]

for an interesting broad mathematical category.

Necessity-style falsification has succeeded.
Sufficiency remains the next theorem problem.

The next step is therefore no longer to invent more examples.

It is to define an abstract category of **stratified refinement systems** in which the five
conditions have precise axioms, and then determine the weakest additional compatibility
assumptions under which their conjunction is sufficient.
