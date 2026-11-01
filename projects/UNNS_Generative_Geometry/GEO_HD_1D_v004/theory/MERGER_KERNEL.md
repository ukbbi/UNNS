# D4-T1 / D4-T2 / D4-T4 — the integer-kernel merger theory   (GEO_HD_1D_v004)

Notation. R(N) = (N+1)^2/N.  A history h from source m ends at m * prod R(N_i).  c(h) = label-content vector over an alphabet A.
Delta_p(N) = v_p(R(N)) = 2 v_p(N+1) - v_p(N);  V_A = (Delta_p(N_j))_{p,j} over the primes of the labels and successors.

**D4-T1 (PROVED).** Two histories from the same source have the same endpoint iff V_A (c - c') = 0.
Proof: R(N) is a positive rational whose p-adic valuation is Delta_p(N); a positive rational is determined by its valuations, and primes outside the rows have valuation 0 for every R(N).  Checked exhaustively over all words of length <= 6 from four sources, 118+ content pairs per source, and on a box of 8,110,682 content pairs (results/MERGER_KERNEL.json): 0 violations.

**D4-T2 (PROVED).** Every nonzero z in ker_Z V_A is realised: with m = prod N_i^{|z_i|} both sides of z = z+ - z-  admit EVERY arrangement (v001 all-arrangements theorem, P(C) | m) and have one endpoint, with different contents.
Exact source condition: the pair (L-side word u, R-side word v) is simultaneously admissible from m iff lcm(K(u),K(v)) | m, so the minimal sources for a relation form the antichain of minimal lcm(K(u),K(v)) (K = v002/v003 threshold).  Examples (results/MERGER_KERNEL.json, verified by Y1 for all m < 400):
{1,2,3} z=(7,-2,-4): [2,3];  {1,2,8} z=(1,-4,2): [16];  {1,2,3,8}: (3,1,-2,-1): [3,8]; (4,-3,-2,1): [2,3]; (2,5,-2,-3): [6,8].
Note the realisation source prod N^{|z|} is sufficient, not minimal: for 1^7 <-> 2^2 3^4 the antichain [2,3] means that some arrangement pair is simultaneously admissible iff 2 | m or 3 | m; the fixed order (2,2,3,3,3,3) alone has K=4 (benchmark source 4).

**D4-T4 (PROVED).** ker V_{1,2,3} = Z (7,-2,-4): rows p=2,3 have rank 2 on 3 columns and (7,-2,-4) is primitive.  Box check |z_i|<=40 finds only its multiples.
Corollary: R(1)^7 = R(2)^2 R(3)^4 = 4^7 = 16384.

Rank 2 kernels: {1,2,3,8} has kernel rank 2 with Graver candidates (box 8) (1,-4,0,2), (2,5,-2,-3), (3,1,-2,-1), (4,-3,-2,1), (7,-2,-4,0) (FINITE-EXACT as a Graver list; the box is not a proof of completeness of the Graver basis).
