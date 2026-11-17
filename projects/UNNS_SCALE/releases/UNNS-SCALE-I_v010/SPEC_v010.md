# SPEC v010
`code/ball.cpp` (g++ -O2): ball B nlo nhi C out.bin → 32-byte records (n, min meeting vertex or 0, |Ball2(Bn)|, |Ball2(B(n+1))|) with all vertices ≤ C. Window scan: B=10^6, C=10^12, n=1..999999 in two halves (results/W_a.bin.gz, W_b.bin.gz; summary W1_window_summary.json).
`code/prof.cpp`: prof B Cmax W RMAX out n… → per n: H4 (min over ≤4-step routes of max vertex, 0 if > Cmax=10^15) and d_W (bidirectional BFS in G_W, radius ≤ RMAX each side, −1 if > 2·RMAX). results/P1 (d_W, 62 n), P2 (H4, 2005 n).
`code/rball.py`: independent Python restricted balls. `code/verify_all_v010.py [--quick]`: layout = sibling dirs UNNS-SCALE-I_v00{2..9}, SHA256SUMS.txt at parent; needs g++ for the rebuild check (skipped otherwise).
