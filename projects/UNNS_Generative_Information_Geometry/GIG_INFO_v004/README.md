# GIG-INFO v004 — Information Recoverability and Grammar Transfer
Sibling of GIG_INFO_v001–v003 and GIG_I_v001–v007 (all frozen, read-only; no remote GitHub changes).

Three questions, three answers (details and tags in THEORY/THEOREMS.md, tables in RESULTS/report.md):
1. Why can second-neighbourhood information recover topology? PROVED: beta2 of the history complex equals dim H_1 of the *forbidden-history complex* (Alexander duality, verified on 700 systems). That locates the topology; it does not explain the success of S2. The conjectured sufficiency of (Q,S2) is FALSIFIED as a general principle (certified counterexample among prefix-defined systems; equal N, h1, Q, S2, even Sum|B2|^2) but holds on all 609,983 arithmetic regimes tested (the seven hard positives are resolved by S2 with margins as small as 16).
2. How many bits? Balanced ensemble, exact: 1 bit uncertainty; in-sample exact signatures leave 0.455 (N), 0.013 (N,h1), 0 ((N,h1,Q,S2)); but out-of-sample (train census -> test held-out) an observer recovers only about 0.3-0.7 bit; exact-signature lookup is worse than ignorance.
3. Symbolic transfer? No H2 ever occurs in transition-grammar systems (783 S/R/N systems, 563,976 random six-symbol digraph systems): the beta2 hierarchy is untestable there. For beta1 the hierarchy N -> radius 1 -> radius 2 reproduces in symbolic and arithmetic domains.

Run: `python3 run_all.py` (about 40 min, 2 processes; needs numpy, scikit-learn); tests `python3 TESTS/test_v004.py`.
