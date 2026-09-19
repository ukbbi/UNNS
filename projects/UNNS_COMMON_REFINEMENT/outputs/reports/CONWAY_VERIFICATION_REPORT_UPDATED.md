# Conway Verification Report

## Target

Repository: `gaearon/conway-refinement`

Pinned commit:

`264445c93b78554c408e99e4e7f663693b4e91ab`

Current repository comparison during this execution showed `main` to be identical to the pinned
commit.

---

# Executive result

The protocol separates three levels of confirmation.

## 1. Mechanically verified at the pinned commit — YES

The following were executed and passed:

- statement fidelity audit;
- exact theorem-shape audit;
- project-wide axiom audit;
- repository CI build at the exact commit;
- Palomar statement compatibility audit;
- standalone/proof-link audits;
- dependency-spine audit;
- independent mathematical reconstruction of the primality-to-refinement endgame;
- independent source-level reconstruction of the critical transfinite step.

## 2. Independently formally confirmed — NOT YET

Two stronger checks remain incomplete:

- a fresh Lean/Lake rebuild outside the proof author's CI infrastructure;
- an independent Lean re-formalization of the critical transfinite step.

The current container has neither Lean nor Lake, and outbound Git access is unavailable there.
A reproducible Windows runner has been added to the project for execution on an independent machine.

## 3. Independently mathematically confirmed — NOT YET

The repository itself records that no independent specialist or peer review has been completed.

Therefore the strongest defensible status after this execution is:

\[
oxed{
	ext{mechanically verified candidate proof with strong statement/source audit;}
\quad
	ext{independent formal and specialist confirmation remain incomplete.}
}
\]

---

# V1 — Statement fidelity: PASS

The internal project target is:

```text
def ConwayRefinementConjecture : Prop :=
  HasFourFactorRefinement Surreal.OmnificInteger
```

and unfolds to:

\[
ab=cd
\Longrightarrow
\exists e,f,g,h,\quad
a=ef,\ b=gh,\ c=eg,\ d=fh.
\]

No nonzero or nondegeneracy assumptions occur.

The standalone Challenge states the theorem from first-principles Conway-game data:

- numeric well-founded games;
- Conway equivalence as equality;
- omnific membership by the cut equation
  \[
  x=\{x-1\mid x+1}\];
- the same four-factor conclusion.

The external 2024 L'Innocente–Mantova statement records Conway's refinement conjecture in the same
four-factor form.

The CI compatibility audit reports:

```text
palomar-compatibility: checked 51 declarations;
the statement closure is portable between the Challenge and Solution modules.
```

### Verdict

`PASS`

The formal theorem has the intended algebraic shape.

A final semantic caveat remains normal for any formalization: specialist review of the chosen model
of omnific integers is still valuable, but no material strengthening of the four-factor statement
was found.

---

# V2 — Axiom / trust audit: PASS

The repository's `scripts/Axioms.lean` enumerates project modules and checks transitive declaration
dependencies.

Its allowlist is exactly:

```text
propext
Classical.choice
Quot.sound
```

The exact-commit CI reports:

```text
axioms: audited 13114 ConwayRefinement declarations;
every declaration reduces to [propext, Classical.choice, Quot.sound].
```

The root `Challenge.lean` intentionally contains one `sorry`, because it is the challenge surface.
That hole is not part of the proved `ConwayRefinement` library. `Solution.lean` proves the same
first-principles statement, and the compatibility/proof-link audits pass.

### Verdict

`PASS`

No hidden domain-specific axiom or transitive `sorry` appears in the audited proof library.

---

# V3 — Build reproducibility

## Exact-commit CI: PASS

GitHub Actions run:

`33806052174`

for the pinned commit completed successfully.

The verify job records:

```text
lake build
Build completed successfully (3145 jobs).
```

and then successfully ran:

- Palomar compatibility;
- axiom audit;
- module-system audit;
- standalone Mathlib audit;
- standalone CombinatorialGames audit;
- isolated-claim proof audit;
- style/documentation/layering audits;
- environment lint.

The toolchain/dependencies are pinned:

```text
Lean 4.31.0
Mathlib fabf563a7c95a166b8d7b6efca11c8b4dc9d911f
CombinatorialGames 3c6dcdbc1ce9e4a16f9b6aa16ee485a744568404
```

## Independent fresh local rebuild: PARTIAL

The current execution container does not have `lean` or `lake`, and its shell cannot resolve
`github.com`, so a second independent kernel build could not be executed here.

This is not counted as a failure of the theorem.

It is counted as an unfinished **independence** check.

A runner has been supplied:

```text
scripts\RUN_CONWAY_VERIFY.bat
```

---

# V4 — Dependency-spine audit: PASS

The source audit confirms the exact critical chain.

In `LimitTailPrimality.lean`, the theorem

```text
isPrimal_of_finite_classes_and_limit_tail_conditions
```

defines the rank as the order type of nonzero support Archimedean classes and performs well-founded
ordinal induction.

At infinite rank it invokes:

```text
exists_closed_class_refinement_at_support_class
```

to obtain exact quotient-class refinement.

Then:

```text
exists_factor_with_smaller_support_class_orderType
```

produces

\[
x=t\,w
\]

with the literal strict inequality

\[

ho(w)<
ho(x).
\]

Then:

```text
exists_factor_refinement_of_closed_class_refinement
```

transports the retained-block split back to ambient divisibility data.

The induction hypothesis establishes:

\[
\operatorname{IsPrimal}(w).
\]

Finally:

```text
exists_primalRefinement_of_factor_refinement
```

splices the local split with residual primality.

The final omnific file then proves:

```text
signedSmallSupportIntegerPart_isPrimal
signedSmallSupportIntegerPart_decompositionMonoid
conwayRefinement
```

and transports four-factor refinement through the signed Hahn/omnific ring equivalence.

### Verdict

`PASS`

The source proof has the claimed transfinite structure.

---

# V5 — Independent endgame reconstruction

The generic implication

\[
orall a,\operatorname{IsPrimal}(a)
\Longrightarrow
	ext{four-factor refinement}
\]

was reconstructed independently in:

```text
03_OMNIFIC/verification/INDEPENDENT_ENDGAME_PROOF.md
```

including the zero case and the nonzero cancellation case.

A compact Lean source was also created:

```text
03_OMNIFIC/verification/IndependentEndgame.lean
```

### Verdict

Mathematical reconstruction: `PASS`

Independent Lean compilation in this environment: `PARTIAL / NOT EXECUTED`

---

# V6 — Critical transfinite-step reconstruction

The central induction step was reconstructed directly from theorem interfaces and the proof body,
without relying on the blueprint prose.

The independently reconstructed chain is:

\[
x\mid bc
\]

\[
\Downarrow
\]

\[
xd=bc
\]

\[
\Downarrow
\]

\[
	ext{exact local closed-class refinement}
\]

\[
\Downarrow
\]

\[
x=t\,w,\qquad 
ho(w)<
ho(x)
\]

\[
\Downarrow
\]

\[
t=e_Af_A,\quad e_A\mid b,\quad f_A\mid c
\]

\[
\Downarrow
\]

\[
w	ext{ primal by induction}
\]

\[
\Downarrow
\]

\[
x	ext{ primal}.
\]

### Verdict

Independent source-level reconstruction: `PASS`

Independent Lean re-formalization: `OPEN`

---

# V7 — Independent specialist review: OPEN

The repository's own formalization record states:

```text
No independent specialist or peer review is recorded.
```

This execution performed a source and formal-architecture audit, but it does not substitute for a
specialist review of surreal/Hahn-series mathematics.

### Verdict

`OPEN`

---

# Final verification classification

| Level | Status |
|---|---|
| Statement fidelity | PASS |
| Project axiom audit | PASS |
| Exact-commit CI build | PASS |
| Dependency-spine audit | PASS |
| Independent mathematical endgame | PASS |
| Independent local Lean rebuild | PARTIAL |
| Independent Lean critical-step reconstruction | OPEN |
| Independent specialist review | OPEN |

## Strongest justified statement

\[
oxed{
	ext{The pinned candidate proof is mechanically verified and passes a strong source-level}
top
	ext{statement, axiom, dependency, and reconstruction audit.}
}
\]

But:

\[
oxed{
	ext{full independent confirmation has not yet been achieved.}
}
\]

The remaining work is narrowly defined rather than vague:

1. execute the supplied fresh-build runner on an independent Lean-capable machine;
2. re-formalize the critical transfinite induction step independently;
3. obtain specialist mathematical review.


---

# Independent local build update — 2026-09-19

The previously incomplete local-build item has now been executed successfully on an independent
Windows machine.

```text
Checkout: C:\leancheck\conway
Commit: 264445c93b78554c408e99e4e7f663693b4e91ab
Lean: 4.31.0
```

The command

```text
lake build ConwayRefinement.Surreal.OmnificInteger.Refinement.ConwayRefinement
```

completed with:

```text
Build completed successfully (2649 jobs).
```

Therefore:

\[
\boxed{\text{Independent local targeted final-theorem build: PASS}}
\]

The local `lake exe axioms` command was not applicable after a targeted module build because it
expects the umbrella `ConwayRefinement.olean`, which is generated by the full project build. The
exact-commit CI project-wide axiom audit remains PASS and is unaffected.

The checkout was returned to a clean Git state afterward.

## Updated strongest status

The candidate proof is now:
- mechanically verified at the pinned commit;
- independently rebuilt locally at the final-theorem-module level;
- source-audited for statement, dependency spine, and transfinite descent.

Remaining higher confirmation layers:
1. independent Lean re-formalization of the critical transfinite step;
2. independent specialist mathematical review.
