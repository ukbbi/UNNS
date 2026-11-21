# FUG-I v004 — Structural Activation and Ancestry Growth Laws

**Project:** `UNNS_INDUCED_STRUCTURES/investigations/FIBONACCI`  
**Date:** 2026-11-20  
**State:** exact run + independent verification completed; prepared for local user validation  
**Execution:** Python 3 standard library, no third-party packages, no `.bat`, no network.  
**Remote policy:** local-only. No GitHub writes.

## Question

**When does a new UNNS nesting history first become admissible inside the Fibonacci overlay, and how does ancestry complexity grow as the Fibonacci index grows?**

The fixed UNNS substrate is `M ⟂ N = M(N+1)^2/N`. This investigation declares the already studied SELECT-II continuation grammar `T_N(x) = x(N+1)^2/N` where `N|x`; it does not redefine the substrate.

## Phase 4 results at a glance

1. **Activation law (PROVED):** a labelled history word `w` appears in the ancestry of `F_n` iff the Fibonacci rank of its minimum endpoint `z(E(w))` divides `n`.
2. **First-appearance classification (VERIFIED-EXACT):** 83 distinct nonempty words appear among the first 84 Fibonacci layers. Every one of the 208 recorded nonempty history instances is reconstructed from its first-appearance index.
3. **Merger gate (PROVED):** the two different-content words `(3,8,3)` and `(1,1,1,2)` merge from a common source at a Fibonacci target exactly for indices `n` divisible by `72`; the minimal merger endpoint is `864`.
4. **Infinite delayed activation (PROVED, alphabet-restricted):** for every odd `r`, between `F_(12r)` and `F_(24r)` the immediate labels within `A={1,2,3,5,7,11}` stay equal, while word `(7,2)` appears newly at depth two.
5. **Unbounded ancestry (PROVED):** at `F_(6*4^t)`, the longest all-label-1 history has length exactly `t+1`; hence complete ancestry depth is not uniformly bounded across Fibonacci targets.
6. **Controls (VERIFIED-EXACT, descriptive):** Lucas and shifted Fibonacci violate some of the index-divisibility activation correspondences; these controls are not matched null models.

## Local installation

Extract the ZIP to a sibling of the earlier releases:

```text
UNNS_INDUCED_STRUCTURES/
  investigations/
    FIBONACCI/
      FUG_I_v001/       (unchanged)
      FUG_I_v002/       (unchanged)
      FUG_I_v003/       (unchanged)
      FUG_I_v004/       (this release)
```

Open **PowerShell** in `FUG_I_v004` and run exactly:

```powershell
py -3 scripts\run_p4.py
py -3 scripts\verify_p4.py
```

If the `py` launcher is unavailable, substitute `python` for `py -3`. Neither script needs administrator permissions. The first script writes only to `FUG_I_v004/results`; the verifier reads the same results and the **embedded copy** of v003 reference records.

## Package contents

```text
FUG_I_v004/
  README.md
  README.txt
  RELEASE_NOTES.md
  SOURCE_PROVENANCE.md
  MANIFEST.json
  theory/
    SPEC.md
    THEOREMS.md
    LIMITS.md
  scripts/
    arith.py              inherited exact integer arithmetic from v003
    run_p4.py             computes activation ranks, families and controls
    verify_p4.py          separate checks; does not import run_p4
  baseline_v003/          self-contained copies of selected frozen v003 outputs
  results/
    RESULTS.md
    summary.json
    word_activation_84.csv
    index_activation_84.csv
    transport_activation_84.csv
    merger_gate.json
    delayed_family_witnesses.csv
    unbounded_depth_spine.csv
    control_activation_84.json
  controls/
    CONTROL_PROTOCOL.md
  docs/
    REGISTER_PATCH.md
    NEXT_RESEARCH.md
  figures/
    rank_activation.svg
```

## Read the results

- Start with `results/RESULTS.md` for the finite census and exact families.
- Read `theory/THEOREMS.md` for complete theorem statements and proofs.
- Read `theory/LIMITS.md` to avoid over-interpreting the finite controls and the restricted-alphabet theorem.
- Inspect `results/word_activation_84.csv` to see the minimum endpoint and first Fibonacci index of each observed history word.
- To reproduce the research, run both commands from the project root; successful verification ends with `FUG-I v004 VERIFY PASS`.

## Scope and provenance

The minimal-source endpoint threshold is inherited from FUG3-T1 and existing UNNS SELECT-II / GEO-HD work. The Fibonacci rank-of-apparition law is classical number theory. Phase 4 adds an explicit synthesis, a reproducible activation register, a first-appearance merger gate, and two mathematically proved infinite family statements. Results of a finite search are never generalized without proof.
