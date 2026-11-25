# FUG-I v003 — Fibonacci Generative Ancestry Geometry and History Invariants

**UNNS_INDUCED_STRUCTURES / investigations / FIBONACCI**

This is **Phase 3** of the local Fibonacci-UNNS induced geometry investigation. It is a sibling release: preserve `FUG_I_v001` and `FUG_I_v002` unchanged.

## Mathematical question

What geometrical relationships arise from complete ordered histories, rather than only immediate occurrence fibres, when Fibonacci values are placed against the fixed UNNS nesting arithmetic? Which histories persist, activate at deeper levels, or converge from the same source by different label compositions?

Original UNNS substrate: `M ⟂ N=M(N+1)^2/N`, `M,N>=1`, rational outputs allowed.

Selected continuation in this release: `T_N(x)=(x/N)(N+1)^2` when `N|x`, applied to positive integer states. Do not confuse the selected continuation graph with the entire substrate.

## Install locally (Windows)

Extract alongside the earlier releases:

```text
UNNS_INDUCED_STRUCTURES\
  investigations\
    FIBONACCI\
      FUG_I_v001\   (unchanged)
      FUG_I_v002\   (unchanged)
      FUG_I_v003\   (new)
```

In File Explorer open `FUG_I_v003`, click the address bar, type `powershell`, press Enter. Execute:

```powershell
py -3 scripts\run_p3.py
py -3 scripts\verify_p3.py
```

Both scripts use **only the Python standard library**. You do not need to run a batch file or change Windows security settings. They work wherever the folder is placed on your D: drive. Outputs regenerate under `results\`.

## What Phase 3 establishes

- A theorem classifying complete history words by a **minimal admissible endpoint**.
- A full-history **gcd intersection law** and its Fibonacci specialization, checked on all 7,056 ordered index pairs through 84.
- **Delayed activation** of new generative histories at depth two despite unchanged one-step nesting labels; observed in six proper index-divisibility transports.
- **122 exact same-source merger pairs** in the finite Fibonacci window, comprising 119 permutation and 3 different-content pairs.
- At `F72`, four admissible words from one source yield the same target with two distinct label contents. This produces a **theorem for infinitely many Fibonacci target indices `72k`**, by exact scaling and Fibonacci divisibility.
- Arithmetic controls with Lucas and shifted Fibonacci; no unjustified exceptionality or physics claim.

For exact details and proofs, read `theory/THEOREMS.md` and `results/RESULTS.md`.

## Folder guide

```text
FUG_I_v003/
  README.md
  README.txt
  MANIFEST.json
  RELEASE_NOTES.md
  SOURCE_PROVENANCE.md
  baseline_v002/            6 locked previous results
  controls/                 control scope and caution
  docs/                     research-register patch proposal
  theory/                   formal specification + theorem proofs
  scripts/                  arithmetic, generator, independent verifier
  results/                  generated CSV, JSON and summary
  figures/                  F72 merger and depth-2 activation SVG
```

## Main mathematical result

With `r_N=(N+1)^2/N`, the exact equality

`r_3^2*r_8 = r_1^3*r_2 = 288`

is realized from the same positive integer source `1730743096803` at Fibonacci target `F72=498454011879264`. Every `F_(72k)` contains scaled copies of the corresponding legal source-locked histories. Thus the selected UNNS nesting operation induces an unbounded, explicitly proved family of different-content generative mergers in the Fibonacci observation layers.

The multiplier-kernel arithmetic is already studied in GEO-HD; the Fibonacci realization and infinite target family are established in this release.

## Reproducibility and scope

All computations are exact integers/rationals. The full census is bounded to index 84 and uses the deterministic 64-bit factorization regime of FUG-I v002. The independent verifier checks prime-valuation source thresholds, dynamic-program route counts, exhaustive intersection/transport assertions, witness legality, and controls. The release includes the source-locked v002 files so its outputs can be audited without GitHub access.


