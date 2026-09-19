# Lean Route-Closure Formalization Report

## Status

The narrow **Well-Founded Route-Closure Induction Proposition** has now been translated into Lean
against the same algebraic interface used by the audited Conway refinement repository.

Formalization file:

`04_PROOF_MAP/lean/RouteClosureInduction.lean`

Source lock:

`gaearon/conway-refinement`

commit:

`264445c93b78554c408e99e4e7f663693b4e91ab`

## What is formalized

The Lean file defines:

`HasWellFoundedRouteClosure`

and proves:

`forall_isPrimal_of_wellFoundedRouteClosure`

followed by:

`hasFourFactorRefinement_of_wellFoundedRouteClosure`.

Thus the formal dependency chain is exactly:

`primal base + local routed block + strict residual-rank descent`

`-> every element IsPrimal`

`-> HasFourFactorRefinement`.

## Reused Conway algebra

The proof deliberately reuses, rather than redefines, the repository's existing results:

- `IsPrimal` from Mathlib divisibility;
- `HasFourFactorRefinement` from `ConwayRefinement.Algebra.Divisibility.Refinement`;
- `exists_primalRefinement_of_factor_refinement` for the splice step;
- `hasFourFactorRefinement_iff_forall_isPrimal` for the final conversion.

This is the main formal test of whether the UNNS synthesis is genuinely compatible with the
source algebra: it is stated directly in the source's own refinement/primality vocabulary.

## Zero/base adaptation

The prose proposition was stated for a cancellative monoid.  The Conway generic refinement file
works in a `CommMonoidWithZero` with `IsCancelMulZero`.  The formal version therefore requires
`Base 0`.  This is not an extra mathematical mechanism; it only assigns the zero case to the
terminal/base branch so the induction uses the same source interface as Conway's theorem.

## Proof structure

For a fixed element `a`, well-founded induction is pulled back along the structural rank map.

- If `a` is in the base regime, primality is immediate.
- Otherwise, for `a ∣ b*c`, local route closure gives
  `a = t*w`, `t = e*f`, `e ∣ b`, `f ∣ c`, and lower rank for `w`.
- The induction hypothesis supplies `IsPrimal w`.
- A witness for `a ∣ b*c` is converted into the product equality required by
  `exists_primalRefinement_of_factor_refinement`.
- The repository splice theorem returns the primal decomposition of `a`.
- Finally `hasFourFactorRefinement_iff_forall_isPrimal` yields four-factor refinement.

## Kernel verification

**Status: LEAN KERNEL VERIFIED.**

The module was compiled in a local Windows checkout of the exact locked repository commit
`264445c93b78554c408e99e4e7f663693b4e91ab`, using the repository-selected Lean 4.31.0 toolchain.
For the build, the file was placed at:

`ConwayRefinement/UNNS/RouteClosureInduction.lean`

and built with:

```text
lake build ConwayRefinement.UNNS.RouteClosureInduction
```

The first full target build ended with:

```text
[837/837] Built ConwayRefinement.UNNS.RouteClosureInduction
Build completed successfully (837 jobs).
```

A second logged run replayed the verified build cache and again completed successfully.
The informational `linter.hashCommand` notices came only from diagnostic `#check` commands at the
end of the test module and were not compilation failures.

Verification evidence is recorded in:

- `outputs/records/ROUTE_CLOSURE_KERNEL_VERIFICATION.md`
- `outputs/records/ROUTE_CLOSURE_KERNEL_EVIDENCE.png`

The user's local working project also contains the text log
`outputs/records/ROUTE_CLOSURE_KERNEL_CHECK.txt`; that exact local log was not uploaded into this
archive.
