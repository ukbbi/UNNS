# VERIFICATION, GIG_MANUSCRIPT_v002
All checks below were run for this build with `verify/gigmini.py` and `verify/run_checks*.py`; raw output is in `verify/verify_v002_run.txt` and `verify_v002_run2.txt`. Arithmetic is exact (integers/rationals).

| Check | Result |
|---|---|
| Histories of 72, decomposition, chain rule | pass |
| Counts for 72^r, r=1..6: 4, 100, 3601, 194864, 14177856, 1258011667 | match registered values |
| Lemma F (feasible-family law) | pass |
| Anchor survival laws A and B, injective counts on both windows | pass (8 classes each) |
| Radius-two identity |B2| = 1+d+s-q, 300 random sets | all pass |
| Alexander duality, random systems | 12/12 |
| Nerve theorem instances (beta_2 = H1 of dead-set nerve) | pass, incl. 2520/3780 pair |
| Pairwise locality F1, F2, F3 | 30, 435, 4060 instances pass |
| Triple counterexample N=674, f=(674,1606,1240,320,16), beta=(1,2,5,0,0) | confirmed |
| Pairwise random sample (76) | max beta_2 = 0 |
| Boundary lemma LT0 | 4683 faces, pass |
| Lift checks LT1-LT3, FI1, FI3, J1 | pass |
| Nerve/core random checks | 160, no mismatch |
| Positive patterns, core sizes | 151 patterns; 290 certificates all equal and positive |
| Standalone certificate checker | 290 certificates, ALL PASS (`standalone_verify_v002_run.txt`) |
| Corrupted certificate files | rejected, e.g. "cycle edge not in nerve" (`tamper_v002_run.txt`) |

Not re-run: growth counts for r=8..10 and the three-lift search (NOT_RERUN, inherited). A passing check on the corpus is evidence, not a theorem; the status tag of each statement is in the monograph.
