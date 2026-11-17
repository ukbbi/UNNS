# UNNS-SCALE-I v005 — Specification
Release: Trillion-Window Metric Closure (Part A, closed) and Infinite-Scale Investigation (Part B, exploratory). v001–v004 frozen; no GitHub changes; Gate 4 deferred.
Part A target: M_{10^6} = max_{1<=n<=999999} d_G(10^6 n, 10^6 (n+1)) exactly. Acceptance: explicit bound <=4 for every n (identity replay, n=1, 614 exact paths), partition of 1..999999 checked by enumeration, one certified distance-4 pair.
Part B target: D_{10^6} in {4,5,6}. Acceptance for closure: universal length-4 (or 5) coverage, or an exact distance-5/6 witness with disjoint-ball certificate. Neither is achieved; exploratory data only.
Results: results/A_* (Part A), results/B_* (Part B), results/raw. Verifier: code/verify_all_v005.py [--quick]. Baselines read from ../SHA256SUMS.txt and ../UNNS-SCALE-I_v00{2,3,4}/SHA256SUMS_v00{2,3,4}.txt.
