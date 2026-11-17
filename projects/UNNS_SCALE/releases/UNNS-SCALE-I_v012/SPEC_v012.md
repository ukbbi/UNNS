# SPEC v012
code/tau_exact.cpp: exact bottleneck DP over all edges of G_Cmax (`tau_exact B Cmax n1 n2 step out [STOPM]`; output `n l:H l:H ... flag`, flag * = floor B(n+1) reached, ~ stalled above floor, # = stopped at STOPM*(n+1), inf = unreachable in Cmax). results F*.txt.
code/ladder.cpp: exact bidirectional BFS inside G_W with node cap (`ladder B RMAX CAP out n W1 W2 ...` -> `n W d` or `n W >r[cap]`); results LAD_*.txt (LAD_E1 = the 12 v011 hub pairs).
code/shortest_routes.py: independent Python shortest routes (SR1.json). code/law_fit.py: ln q(n) fits (FIT_summary.json). code/frontier_io.py: readers, q(n).
code/verify_all_v012.py [--quick]: needs g++ (OpenMP), sympy, numpy; sibling dirs UNNS-SCALE-I_v002..v011; full mode ~15 min, ~3 GB RAM.
