# GIG-INFO v006 — Synthesis: self-contained results, independent certificates, minimal observation
UNNS Research Collective. Sibling of v001–v005 (frozen, untouched). No new census, no information-signature search.
1. `THEORY/SELF_CONTAINED_RESULTS.md` — Result I (dead-set nerve theorem) and Result II (pairwise-adjacency theorem + sharpness), with classical inputs named and prior-art review explicitly NOT done.
2. `VERIFY/standalone_verify.py` — stdlib-only verifier (no import from this package): the finite hypotheses of Result II (30/435/4060), the triple counterexample (beta_2=5 from the definition of K_A), and 290 cycle/cocycle certificates for Result I (+ beta_2 by definition for 4 systems; `--full` for all 290). Run: `python VERIFY/standalone_verify.py`.
3. Minimal observation (C20/D21/G20): exhaustive over all 219,145 distinct dead-set patterns of the census. No count-level statistic of the nerve decides beta_2>0; the strong-collapse core does, and positive cores are small (105 of 151 positive patterns are the bare 3-vertex hollow triangle).
4. `ERRATUM_v005.md` — parent-hash defect in v005 (V004 pointed at GIG_I_v005), impact assessed, fixed here.
Run all: `python run_all.py` (~12 min, 2 cores). Tests: `python TESTS/test_v006.py`.
