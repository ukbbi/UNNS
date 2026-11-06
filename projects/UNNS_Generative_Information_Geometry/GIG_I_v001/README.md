# GIG_I_v001 — Generative Information Geometry, Phase I

*Generative Information Geometry in the UNNS Substrate: Arithmetic Ancestry, Information Loss, and History Topology.*
UNNS Research Collective · 5 November 2026 · independent, versioned package built on frozen SELECT-II and GEO-HD-1 results. Python standard library only.

## What this release establishes
1. **Exact theory of finite generative ambiguity** `A(t) = log2 |F_t|`, with a source / content / recombination-class / path decomposition (GIG-T1…T6) and the complete numbers for 72 (`2 = 1.5 + 0.5` bits) and the family `72^r` (exact counts to r = 10, `A(72^r) ≥ log2 C(2r,r)` with a self-contained proof).
2. **A recombination information profile** `I_r(t)` with exact properties (GIG-T7): it equals `log2(P_r)/N` for an integer `P_r`, increases strictly until the largest component diameter and then equals `H(W|C,T)`; a first-step law ties `I_1` to the cycle rank of the swap graph; it is additive over pieces.
3. **A radius-2 formula (GIG-T8):** two-swap accessibility sees degrees and *squares*, never hexagonal braid cells.
4. **Sharp counterexamples (GIG-T9, answering GIG-Q2):** six exact pairs of arithmetic pieces with the same `A`, class entropy, within-class entropy and accessibility statistics up to radius 0, 1 or 2, but different homology. The strongest (W5, W6) differ by a single hexagonal cell. The inherited 2-void `{2,3,8,9,14}@1008` has the same one-swap neighbourhood statistics as a contractible piece `{1,2,3,5,7}@105`.
5. **Topology inside complete-history fibres (GIG-T10):** the endpoint 1 382 400 has 15 842 complete histories (13.95 bits) and contains a piece with a genuine loop (`{2,3,14,15}` at the squarefree source 210).
6. **A finite-exact census** (all realizable admissible sets, k ≤ 5) giving the *separating radius*: 1 for k=4, 3 for k=5 (details and numbers in `RESULTS/report.md`), recorded as the falsifiable conjecture GIG-C1.

## Run it
```
python -m unittest discover -s TESTS -v            # 28 tests, ~15 s (1 optional test needs GIG_FROZEN_SRC)
python EXPERIMENTS/run_all.py                       # E1-E4, writes RESULTS/results.json (~75 s)
python EXPERIMENTS/run_all.py --extended            # larger census (k=4 L<=70, k=5 L<=26), RESULTS/results_extended.json (~25 min)
python EXPERIMENTS/E2_growth.py 10                  # long table of |F_{72^r}| (~5 min)
python EXPERIMENTS/make_manifest.py                 # regenerate MANIFEST.json
GIG_FROZEN_SRC=<...>/GEO_HD_1D_v004/src python -m unittest discover -s TESTS   # optional read-only cross-check
```

## Layout
```
THEORY/       DEFINITIONS.md  THEOREMS.md  PROOFS.md  OPEN_PROBLEMS.md
ENGINE/       history_fibres.py  swap_graph.py  information.py   (required)
              history_complex.py  census.py                     (added: inherited complex re-implemented; census)
EXPERIMENTS/  E1_72.py  E2_growth.py  E3_content.py  E4_topology.py  run_all.py  make_manifest.py
TESTS/        test_gig.py
RESULTS/      results.json  results_extended.json  report.md  crosscheck_frozen.json  e2_long_table.json
SPECIFICATION.md   MANIFEST.json
```

## Conventions you must keep in mind
* **Source convention is always stated.** Complete-history fibre `F_t` (squarefree sources) versus fixed-source fibre `F_t(m0)`. The inherited loop `{2,3,8,9}@72` and void `{2,3,8,9,14}@1008` live at *non-squarefree* sources, i.e. in fixed-source fibres; the same loop reappears (up to permutohedron symmetry) at the squarefree source 210.
* **Probability model is always stated** ("uniform on the fibre" unless noted). `A(t)` needs no model.
* **Graph vs. complex.** The swap graph is the 1-skeleton of the permutohedral complex; Betti numbers are claimed only for distinct-label pieces, using the inherited full-subcomplex cell rule — cliques are never filled.
* **Status.** Computed facts are labelled [FINITE-EXACT]; no universal statement is derived from a computation. T1–T8 are proved in `THEORY/PROOFS.md`. GIG-C1/C2 are conjectures.

## Scope boundary
Finite arithmetic history information and recombination topology only. FIELD-I dynamics, thermodynamic or quantum entropy, continuous curvature functionals and non-orientable temporal manifolds are out of scope; the earlier Chronotopos functionals are defined on a different model and are not imported.
