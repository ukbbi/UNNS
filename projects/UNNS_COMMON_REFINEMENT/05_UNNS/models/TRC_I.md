# TRC-I — Transfinite Route-Closure Schema

## Status

**PROVISIONAL SCHEMA — NOT YET A GENERAL THEOREM**

This schema is extracted from:
1. the proved positive-affine route-closure criterion developed in this project; and
2. the architecture of the public candidate Lean proof of Conway's refinement conjecture.

It is intended to identify the next theorem to formulate.

---

## Five structural conditions

Let a structural domain admit:
- an endpoint composition law;
- a notion of irreducibility;
- a stratification/rank of structural complexity;
- local factor/refinement operations;
- limit objects or completion when the rank is transfinite.

Define:

### I — Local Independence
At each active stratum, the leading structural coordinates admit a presentation with no
hidden relation capable of destroying factor traceability.

### P — Prime Traceability
Every irreducible is prime, or an equivalent divisibility principle holds strongly enough
to route an irreducible factor through a product.

### D — Well-Founded Descent
Every unresolved local factor/refinement step strictly lowers a well-founded structural rank.

### L — Limit Closure
At limit stages, the common tail/quotient/completion remains inside a domain where the local
factor/refinement principle still applies.

### R — Reconstruction
Compatible local refinements can be lifted/reassembled into the original global domain.

---

# Working implication

\[
(I)+(P)+(D)+(L)+(R)
\stackrel{?}{\Longrightarrow}
\text{global common refinement}.
\]

The question mark is essential.

The Conway proof architecture is evidence that these roles can jointly support a transfinite
refinement theorem in one highly nontrivial domain. It does not by itself prove the abstract
schema.

---

# Finite affine reduction

For a positive affine monoid:
- `I` collapses to `ARD=0`;
- `P` is atom -> prime;
- `D` is ordinary finite termination;
- `L` is vacuous;
- `R` is coordinate reconstruction.

Thus TRC-I reduces to the theorem already obtained:

\[
\operatorname{ARD}=0
\iff
H\cong\mathbb N_0^r
\iff
\text{global refinement}.
\]

---

# Omnific realization suggested by the proof map

| TRC-I condition | Candidate Conway realization |
|---|---|
| I | associated-graded algebraic independence; polynomial presentations |
| P | reduced omnific primality; irreducibles prime |
| D | strict decrease of support-class order type; transfinite extension |
| L | common-tail cofinality and Cauchy completeness |
| R | signed normal form; Hahn integer-part primality; Oz refinement |

This table is the current central bridge of the project.

---

# Falsification targets

A future abstract theorem must fail cleanly if any one of the five conditions is removed.

Required adversarial models:

1. `¬I`: atomic/graded relations but otherwise good factorization.
2. `¬P`: irreducibles that divide products without dividing either factor.
3. `¬D`: recursive factor control with a non-well-founded structural rank.
4. `¬L`: correct successor steps but an incomplete limit stage.
5. `¬R`: valid local refinements that cannot be lifted globally.

Only after those five failure classes are constructed should TRC-I be promoted from schema to
theorem candidate.


---

# Falsification update

The five requested omission tests have now been constructed.

See:

`05_UNNS/models/TRC_I_COUNTERMODELS.md`

and

`06_TESTS/output/TRC_I_COUNTERMODELS.json`.

Within the explicit TRC test framework, each of `I`, `P`, `D`, `L`, and `R` can be removed
while the other four are retained, and route closure fails.

This establishes independence/load-bearing status for the schema roles **inside that test
framework**.

It does not settle sufficiency of all five together.


---

# Sufficiency update — promoted to SRS theorem

The provisional implication has now been proved after replacing the informal ambient
"structured domain" by the precise notion of a **Stratified Refinement System (SRS)**.

See:

- `05_UNNS/models/STRATIFIED_REFINEMENT_SYSTEM.md`
- `05_UNNS/models/SRS_ROUTE_CLOSURE_THEOREM.md`

Inside the SRS category:

\[
I+P+D+L+R
\Longrightarrow
\text{global route closure}.
\]

The proof is by transfinite induction.

No sixth axiom was required, but `R` had to be made precise as:
- `R1` local lift/assembly;
- `R2` limit reconstruction.

The remaining open problem is **realization**, not abstract sufficiency.
