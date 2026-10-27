# GEO-I v008 — Report

**Scope.** Programmes A (small-box geometry), B (hollow-box topology), C (minimal binary obstructions), D (certification), from the v007 baseline, which is preserved as a frozen record (`docs_v007/`).

## Outcome in plain terms

| Programme | Target | Result |
|---|---|---|
| A | G8-C1: `U = conv(F)` on all small boxes | **Not proved, not refuted.** New: G8-S (staircase = squareless zone; explains 29,890), G8-R1 (reduction to the cap, conditional on G8-T2), exhaustive exact sweep of **26,636** small boxes (`3 ≤ d ≤ 20`, all units): all covered, 0 failures. Local lemmas G8-L1…L4 are PROPOSED only. |
| B | G8-C2/G8-T2: exact hollow topology | **Not proved.** G8-T2 CHECKED `3 ≤ d ≤ 72`. New and proved: **G8-T1 filling lemma** (both holes filled by explicit Graver parallelograms in every enlarged box), G8-K1; β₁ along `Q=(d,h)`: 0 for every `h ≥ d+1` on 40 unit classes `d ≤ 11`, never increasing (CHECKED). |
| C | G8-C3/G8-T3: `r_min ≤ 3` | **Not proved in general.** New and proved: B-LOW (`r_min ≥ 3` always), B-COMMON, B-NULL′, B-BASIS, B-SERIES; complete classification of minimal boxes of nullity 3 and 4 with `r_min = 3` for **all** `n`; the `RM(1,k−1)` infinite family; complete censuses `n ≤ 9` (1, 3, 11, 50, 273, 1757 minimal representatives, all rank 3, all collisions full-support, all with a common-base rank-3 collision). |
| D | certificates | `checker8.py` with COVER, GAP, HOMOLOGY, RANK; 40 new certificates (plus the 20 v007 ones) accepted, tampered ones rejected. |

**Gate G2 (Programme A) — honest statement.** G2 asks for a proof, a decisive counterexample, or a substantial new infinite-family theorem rather than an extended search. v008 has *no* proof and *no* counterexample for G8-C1. Its claim to G2 rests on G8-T1 (all `d`, all units, all enlarged boxes) and G8-S/G8-R1; whether that is "substantial" for G8-C1 is for the reader to judge — the cap beyond the square remains unproved. The search range extension (26,636 boxes) is recorded as evidence only.

## Gates

* **G1 preservation:** v001–v007, SELECT-I/II, FIELD-I, Foundations unchanged; inherited files hash-checked (`PROVENANCE.json`); GitHub untouched.
* **G3–G6:** statements, proofs and certificates as in the registry (MATHEMATICS.md); proofs live in SMALL_BOX/HOLLOW/MINIMAL_RANK.
* **G7 reproducibility:** deterministic code; `verify.py` regenerates the cheap results and checks shipped records for the expensive ones (named SHIPPED); nothing is PASS when not run (UNAVAILABLE).
* **G8 documentation:** eight documents, seven exact-data figures, registry statuses restricted to the allowed vocabulary.

## Mandatory regressions

Re-run (inherited, not counted as v008): 3600 and `210^4` benchmarks, 44100, `2304/5`, `82944/5`, `2^{10+2t}3^4/5`, `2^{10}7^{10}/15`, `s = ±1` theorems, `d ≤ 30` archived window, G7-T1 and G7-T3, HYP-LL FALSE, 4D/5D parity benchmarks, v007 binary census qualifications (kept as historically stated; superseded for `n ≤ 9` as explained in MATHEMATICS.md §4).

## Honest limits

* Counts of v008's census ("representatives") are not comparable with v007's raw multiset counts.
* HOMOLOGY certificates certify the Betti numbers of the supplied planar complex, not that it equals the arrangement of `U`.
* Nullity ≥ 5 minimal boxes are not classified (orbit enumeration in `F_2^5` was not feasible here); the census `n ≤ 9` covers some of them.
* Reference review is record-level only (PRIOR_ART.md); no priority claim.
* Time: exhaustive sweeps were run to `d = 20` (v006/v007 ranges `d ≤ 30` and squareless `d ≤ 32` inherited).

## Suggested next steps

1. G8-T2 by a continued-fraction induction on `(d,s)` (would close the hull of the square; with G8-R1 leaves only the cap).
2. The cap: prove G8-L1…L4 or find the obstruction.
3. G8-C3′ (common base) as the structural route to `r_min ≤ 3`; classify nullity 5.
