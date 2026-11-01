# D4-T8 — topology of the extended (swap + rewrite) complex

Construction (cubical). Vertices: admissible histories with a fixed source and endpoint.  Edges: adjacent swaps and block replacements.  Cells: sets of mutually independent moves acting on pairwise disjoint intervals, identified with their vertex sets (a d-cell has 2^d vertices).  GF(2) homology.  There are **no coherence cells**: braid hexagons and relations between overlapping moves are not filled.  Betti numbers are therefore invariants of this specific complex only.

* **D4-T5 cube family (PROVED + FINITE-EXACT counts).** r independent choices of block A=1^7 / B=2^2 3^4 from 4: 2^r histories to 4^(7r+1), r+1 contents, cell counts C(r,d) 2^(r-d), Betti (1,0,...,0) (contractible) for r=1..4 (r<=5 in the full verifier).
* Benchmark source 4 (the 4 words of 1^7, 2^2 3^4 and neighbours): cells {0:4, 1:5}, Betti (1,2) in the builder's maximal-word complex.
* **Join example (loop created by a content-changing relation).** R(2)R(8)R(63) = R(5)R(9)R(35) = 20736/7 on labels (2,5,8,9,35,63); at m = 280 and 840 there are 4 histories, 4 swap classes, one rewrite class, cells {0:4, 1:4}, Betti (1,1): swap-only space is 4 points, the rewrite space is a circle.  So content-changing rewrites can create a loop out of a disconnected swap space — this is the extended analogue of the v003 loops (V=4, E=4, b1=1 verified independently in Y5).
* Kunneth / join behaviour with v003 loop sides: OPEN (examples not computed past the join above).
