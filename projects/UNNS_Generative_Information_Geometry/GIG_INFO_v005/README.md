# GIG-INFO v005 — Forbidden-History Topology and Information Recovery
UNNS Research Collective · sibling package; v001–v004 and all GIG-I parents are frozen, read-only, and untouched.

Question: which constraints on *forbidden* histories force a two-dimensional hole in the admissible history complex (beta_2(K_A) > 0), and does the answer depend on arithmetic divisibility?
Tool: Alexander duality (v004, T-AD): beta_2(K_A) = dim H_1(Y_A). No new census, no new information signature.

Findings (see THEORY/THEOREMS.md for status tags, RESULTS/report.md for numbers):
1. [PROVED] Star-intersection lemma and nerve theorem: for prefix-defined systems Y_A is homotopy equivalent to the dead-set nerve N[D_A]; beta_2(K_A) = dim H_1(N[D_A]).
2. [FINITE-EXACT] 288/290 known positives have a non-bounding hollow triangle in N[D]; the other 2 have a non-bounding 4-cycle (two complementary dead pairs); 0/1000 sampled negatives have either. Explicit cycle+cocycle certificates for all 290.
3. [FINITE-EXACT] The two certified sharp pairs are explained by which dead sets are present (the 2520/3780 pair: |D| = 5 vs 5, one hollow triangle).
4. [PROVED, computer-assisted] For every digraph on six events, the Hamiltonian-path complex has beta_2 = 0: the symbolic S/R/N grammar can never show beta_2 > 0.
5. [FINITE-EXACT] Sharpness: two forbidden consecutive triples give beta_2 = 5.
6. [OPEN] No derivation of S_2; no purely local criterion for hollow cycles.

Run: `python run_all.py` (about 10 minutes on 2 cores) or `RUN_INFO_V005.bat`; tests: `python TESTS/test_v005.py`. Standard library + numpy.
