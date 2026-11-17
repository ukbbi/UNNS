# SPEC v013
code/tau_exact.cpp (v012 engine; v013 adds env NFILE=<list of n> to the range form), code/ladder.cpp (bidirectional exact distance with cap).
code/primeflip.py: composite prime-flip routes (L4). code/capped_routes.py: explicit routes for the seven v012-capped pairs via the 10^6 ladder. code/summarize.py: all headline statistics from stored files (SUMMARY_v013.json). code/verify_all_v013.py [--quick].
results/lattice/F_D.txt: frontiers for the 49 divisors of 10^6 (n=1..99). results/descent/: FB_B/FA_B_sS frontiers + index.txt. results/chain/FC_A.txt: chain-scale frontiers (stop at 10^6(n+1)); FB_1000000.txt = v012 exact frontier.
results/FP_100.txt, FP_1000.txt: exact prime-family frontiers; LAD_pf100/pf1000/primes.txt: ladder distances at (p+1)^2; PF_B6.txt: composite bounds at B=10^6 (every 12th prime in (10^6,10^6+6e4)); FIRSTLEG_B6.json; CHAIN_capped_A.txt, CAPPED_intervals.json, CAPPED_routes.json.
