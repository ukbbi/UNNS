# COUNTEREXAMPLES AND EXPLICIT WITNESSES -- GEO_HD_1D_v003 (all recomputed by the verifier)

1. **Strongly connected feeding digraph without split.** (2,4,15), (2,5,9), (2,6,7), (2,6,21), (2,7,27), (2,9,25): the converse of "split => strongly connected" fails (130 of the 257 strongly connected 3-label contents with labels <= 30 never split). The exact reason is T3: no labeling has both b not| L and kappa{a,c} not| L.
2. **Hub not necessary.** 525 three-label contents (labels <= 30) have neither a hub nor a split source.
3. **Connected but not contractible: a loop.** {2,3,8,9} at m = 72: one swap class, 16 admissible arrangements, Betti (1,1,0,0). Infeasible proper subsets: {2,8}, {3,9}.
4. **Connected, simply connected, not contractible: a 2-void.** {2,3,8,9,14} at m = 1008: 96 admissible arrangements, Betti (1,0,1,0,0). Infeasible proper subsets: {2,8,14}, {3,9}.
5. **Cubical complex misses the void.** Same data: cubical Betti (1,19,0,0,0).
6. **Persistence-restricted splitting.** The two swap-equivalent 72-histories have different rho_2: (0,1,1,1) vs (0,1,0,1); the 2-preserving graph separates them. Non-monotone in d: r=3, d=12 gives 678 classes, d=36 gives 493.
7. **Two-label blocks with repeated labels can have 3 arrangements**, so the "block of >= 3 labels" necessary condition is claimed for distinct labels only.
