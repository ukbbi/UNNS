# Conway Verification Protocol

## Scope

This protocol verifies the candidate Lean proof of Conway's four-factor refinement conjecture for
omnific integers at the pinned repository state:

```text
Repository: gaearon/conway-refinement
Commit: 264445c93b78554c408e99e4e7f663693b4e91ab
Lean: v4.31.0
Mathlib: fabf563a7c95a166b8d7b6efca11c8b4dc9d911f
CombinatorialGames: 3c6dcdbc1ce9e4a16f9b6aa16ee485a744568404
```

The verification target is not merely "does Lean compile?"

It is the stronger question:

> Does the checked theorem encode Conway's intended four-factor statement, use only an acceptable
> logical foundation, follow the claimed proof spine, and survive reproducible / independent
> verification?

---

# Status vocabulary

- **PASS** — the specified verification was executed and the criterion was met.
- **PARTIAL** — substantial evidence was obtained, but the strongest version of the criterion was
  not executed independently.
- **FAIL** — the criterion was executed and failed.
- **OPEN** — this verification layer requires outside work not available in the current execution.

---

# V1 — Statement fidelity audit

## Criterion

Verify all of the following:

1. the formal target quantifies over omnific integers;
2. it assumes only
   \[
   ab=cd;
   \]
3. it concludes the existence of \(e,f,g,h\) in the same domain with
   \[
   a=ef,\quad b=gh,\quad c=eg,\quad d=fh;
   \]
4. no nonzero, reducedness, finite-support, or other extra hypothesis has entered the final theorem;
5. the omnific-integer predicate corresponds to Conway's cut definition;
6. the standalone first-principles statement and proved statement have the same declaration closure.

## Evidence to inspect

- `ConwayRefinement/Surreal/OmnificInteger/RefinementConjecture.lean`
- `ConwayRefinement/Surreal/OmnificInteger/Refinement/ConwayRefinement.lean`
- `Challenge.lean`
- `Solution.lean`
- `scripts/PalomarCompatibility.lean`
- L'Innocente–Mantova 2024, Conjecture 1.1.1(2)

## Pass condition

The Lean statement is the same four-factor formula as the published conjecture, with no
strengthening or weakening material to the theorem.

---

# V2 — Proof-trust / axiom audit

## Criterion

Verify:

1. no project theorem depends transitively on `sorryAx`;
2. no custom/domain-specific axiom enters the proof;
3. only the standard allowed axioms
   `propext`, `Classical.choice`, `Quot.sound`
   occur in the audited project declarations;
4. any intentional `sorry` used for a challenge statement is isolated from the proved project and
   is paired with an exact proved counterpart.

## Evidence to inspect

- `scripts/Axioms.lean`
- `.github/workflows/ci.yml`
- CI axiom-audit output
- `Challenge.lean`
- `Solution.lean`
- isolated-claim proof audit

---

# V3 — Reproducible build audit

## Criterion

At the pinned commit:

1. obtain the pinned Lean and dependency revisions;
2. build the full authoritative project module glob;
3. build the standalone Challenge and Solution surfaces;
4. run the statement-compatibility audit;
5. run the axiom audit;
6. run the standalone and proof-link audits.

## Strong version

Repeat from a fresh checkout on a machine/environment not controlled by the proof author.

## Project runner

Use:

```text
scripts\RUN_CONWAY_VERIFY.bat
```

This runner clones the exact pinned commit into a disposable directory and invokes the full build
and core audits.

---

# V4 — Dependency-spine audit

## Criterion

Verify directly from Lean source that the transfinite proof really has the claimed logical form:

```text
finite-class primality
→ exact local quotient refinement
→ retained-block factorisation
→ strictly smaller support-class rank
→ induction gives primal residual
→ ambient transport
→ primal splice
→ current element primal
→ every element primal
→ four-factor refinement
→ transport to omnific integers
```

## Critical declarations

```text
isPrimal_of_finite_classes_and_limit_tail_conditions
exists_closed_class_refinement_at_support_class
exists_factor_with_smaller_support_class_orderType
exists_factor_refinement_of_closed_class_refinement
exists_primalRefinement_of_factor_refinement
signedSmallSupportIntegerPart_isPrimal
signedSmallSupportIntegerPart_decompositionMonoid
hasFourFactorRefinement_of_decompositionMonoid
conwayRefinement
```

## Pass condition

The proof body actually invokes these steps in the claimed direction and the rank inequality is
strict.

---

# V5 — Independent endgame reconstruction

## Criterion

Independently reconstruct:

\[
\forall a,\operatorname{IsPrimal}(a)
\Longrightarrow
\operatorname{HasFourFactorRefinement}.
\]

The reconstruction must explicitly handle:

- \(a=0\);
- \(a\neq0\);
- cancellation away from zero;
- extraction of \(e,f\) from primality;
- construction of \(g,h\);
- derivation of \(b=gh\).

A Lean version is supplied in this project as `IndependentEndgame.lean`.

## Strong pass condition

Compile that file independently against a minimal trusted algebra environment.

---

# V6 — Independent critical transfinite-step reconstruction

## Criterion

Reconstruct, independently of the proof-guide prose, the central induction step:

1. start with \(x\mid bc\), write \(xd=bc\);
2. obtain an exact local closed-class refinement;
3. factor
   \[
   x=t\,w
   \]
   with
   \[
   \rho(w)<\rho(x);
   \]
4. transport the local split of \(t\) back to the ambient integer part;
5. apply the induction hypothesis to make \(w\) primal;
6. splice the two pieces to prove \(x\) primal.

## Strong pass condition

Re-formalize this step in a separate Lean mini-project using only the public theorem interfaces.

---

# V7 — External mathematical review

## Criterion

At least one mathematically qualified independent reviewer should inspect:

- statement fidelity;
- the Hahn-series / surreal identification;
- the common-tail completeness use;
- strict support-class descent;
- the local-to-ambient transport;
- the final pre-Schreier/refinement endgame.

## Pass condition

A review independent of the proof author and the AI systems that generated the proof reports no
substantive gap.

Lean kernel checking is not a substitute for this semantic review.

---

# Final classification

The candidate theorem is considered:

### Mechanically verified

when V1–V4 pass.

### Independently formally confirmed

when V1–V6 pass, including fresh independent Lean compilation.

### Mathematically independently confirmed

when V1–V7 pass.

The project must report the strongest status actually achieved, not the strongest status suggested
by the existence of a `.olean` file or a successful CI badge.
