# Route-Closure Lean Kernel Verification Record

## Status

**LEAN KERNEL VERIFIED**

The formal module `04_PROOF_MAP/lean/RouteClosureInduction.lean` was compiled successfully in a local Windows checkout of the audited Conway refinement repository.

## Locked source state

- Repository: `gaearon/conway-refinement`
- Commit: `264445c93b78554c408e99e4e7f663693b4e91ab`
- Lean toolchain selected by the repository: `leanprover/lean4:v4.31.0`

The checkout was verified locally with:

```text
git rev-parse HEAD
264445c93b78554c408e99e4e7f663693b4e91ab
```

## Build placement

The test module was copied into the repository library tree as:

```text
ConwayRefinement/UNNS/RouteClosureInduction.lean
```

This made it part of the repository's declared `ConwayRefinement.*` Lake library.

## Kernel build

Command:

```text
lake build ConwayRefinement.UNNS.RouteClosureInduction
```

Observed result:

```text
[837/837] Built ConwayRefinement.UNNS.RouteClosureInduction
Build completed successfully (837 jobs).
```

A second logged run reused the verified cache and again ended with:

```text
[829/829] Replayed ConwayRefinement.UNNS.RouteClosureInduction
Build completed successfully (829 jobs).
```

The local session also copied the saved build log into the working project as:

```text
outputs/records/ROUTE_CLOSURE_KERNEL_CHECK.txt
```

That exact text log remained on the user's local project and was not uploaded into this archive. This archive preserves the supplied terminal evidence image instead.

## Linter notices

The build emitted informational `linter.hashCommand` notices for diagnostic `#check` commands at the end of the test module. These were not compilation failures; the module built successfully.

## Formal conclusion verified

Lean accepted the formal chain:

```text
HasWellFoundedRouteClosure + well-founded structural rank
    -> forall a, IsPrimal a
    -> HasFourFactorRefinement
```

using the exact Conway algebraic interface and the repository theorem
`exists_primalRefinement_of_factor_refinement` for the splice step.

## Evidence

Terminal screenshot:

`outputs/records/ROUTE_CLOSURE_KERNEL_EVIDENCE.png`
