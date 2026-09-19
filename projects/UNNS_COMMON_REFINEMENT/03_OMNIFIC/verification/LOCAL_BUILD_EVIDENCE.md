# Independent Local Conway Build Evidence

## Date
2026-09-19

## Environment

```text
Platform: Windows
Checkout: C:\leancheck\conway
Pinned commit: 264445c93b78554c408e99e4e7f663693b4e91ab
lean-toolchain: leanprover/lean4:v4.31.0
Lake reported Lean: 4.31.0
```

The checkout was cleaned before the build. Two untracked local experimental items were moved out of
the repository, after which `git status --short` returned no output.

## Dependency preparation

The first long-path attempt failed during Mathlib cache extraction with repeated Windows path errors.
Using the short checkout path `C:\leancheck\conway`, a fresh:

```text
rmdir /s /q .lake
lake update
```

completed successfully.

## Targeted theorem build

Command:

```text
lake build ConwayRefinement.Surreal.OmnificInteger.Refinement.ConwayRefinement
```

Result:

```text
Build completed successfully (2649 jobs).
```

Therefore:

\[
\boxed{\text{Independent local targeted final-theorem build: PASS}}
\]

This is a build of the final Conway refinement theorem module and all dependencies required by that
module. It is not a build of every auxiliary repository target.

## Axiom-audit note

`lake exe axioms` was attempted after the targeted build and reported that the umbrella
`ConwayRefinement.olean` did not exist. That executable is designed for the full project build.

This does not invalidate the targeted theorem build. The project-wide axiom audit remains PASS from
the exact pinned-commit CI run.

## Clean-state confirmation

`lake update` modified `lake-manifest.json`; it was restored with:

```text
git restore lake-manifest.json
```

and the final:

```text
git status --short
```

returned no output.
