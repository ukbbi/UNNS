# SPEC v011
code/kruskal.cpp: exact connection ceilings (Kruskal over edges by larger endpoint, queries (Bn,B(n+1))); outputs results/K_k*.txt.gz (B=100,1000,10^4,999).
code/comp.cpp: exhaustive component check of Theorems P/P' on G_C. code/conn.cpp: hub = component of 1 in G_{1e9}; classifies the 10^6 vertices B m (direct / flip gadget / other), kappa matrices; results CN1_*.
code/conn2.cpp: bounded BFS links to the hub (args: todo out RMAX CAP [MULT] [domain=1]); results CN2 (radius 2), CN3b (primes via vertex p, ceiling B m). code/kq.cpp: general pair queries. code/ceilings.py: pair ceilings from certificates (CN4_pair_ceilings.json). code/hubpath.py, explicit_routes.py: explicit Python routes (E1_explicit_routes.json).
code/verify_all_v011.py [--quick]: needs sibling dirs UNNS-SCALE-I_v002..v010, g++, scipy, sympy; full mode also rebuilds conn/conn2 (needs ~4 GB RAM, ~10 min).
