# GEO_HD_1D_v004 — theorem register

Status vocabulary: PROVED (argument in theory/), FINITE-EXACT (exhaustive over the stated finite range, not a proof beyond it), OPEN.
All statements are for the fixed-source SELECT-II multiplier R(N)=(N+1)^2/N.  Same-author work: not independent review.  C3 not claimed; novelty not assessed.

| id | statement | status |
|---|---|---|
| D4-T1 | same source: equal endpoint <=> V_A(c-c')=0 | PROVED (+ box 8,110,682 pairs, 0 violations) |
| D4-T2 | every kernel vector is realised from m=prod N^{|z|}; minimal sources = antichain of lcm(K(u),K(v)) | PROVED; minimal-source lists for 6 relations FINITE-EXACT |
| D4-T3 | block replacement p·u·s <-> p·v·s legal iff lcm(K,K') | m iff v admissible from state after p | PROVED (+ 11,000 randomized tests) |
| D4-T4 | ker V_{1,2,3} = Z(7,-2,-4); R(1)^7=R(2)^2R(3)^4=4^7 | PROVED |
| D4-T5 | 2^r histories 4 -> 4^(7r+1), r+1 contents, cube complex contractible | PROVED (histories, contents); Betti FINITE-EXACT r<=4 (cube homology is classical) |
| D4-T6a | saturation: P(c)|m for all contents + Graver-connected fibre => one rewrite class | PROVED |
| D4-T6b | quotient-graph description of rewrite classes | PROVED |
| D4-T6c | {1,2,3}: swaps + 1^7<->2^2 3^4 connect all equal-endpoint histories at every source | FINITE-EXACT (box a<=1,b<=4,c<=8) ; general OPEN |
| D4-T7a | exposure obstruction in F_j (3∤m, v2(m)<=3 => two classes) | PROVED for all j |
| D4-T7b | F_j connected iff 3|m or 16|m | FINITE-EXACT j<=8 (all sources); general j OPEN |
| D4-T7c | insufficient generators: {z1,z2} cannot connect fibre {3^2 8,1^3 2}; Graver z3 can | PROVED (explicit) ; 498/816 deficient fibres FINITE-EXACT |
| D4-T8a | join example m=280,840: swap space 4 points, rewrite space circle (Betti (1,1)) | PROVED/explicit |
| D4-T8b | homotopy type of extended complexes; coherence cells | OPEN |
| D4-T9 | births-losses is a rewrite invariant; fibre sequences distinguish cube histories (r<=4); (births,losses) pairs injective only r<=3 | PROVED (invariant) / FINITE-EXACT |

## Reading for the project
Algebraic equivalence (equal endpoint) becomes operational equivalence (one rewrite class) under an explicit sufficient resource condition (T6a: P(c)|m for every content, with a Graver-complete move set).  Below the condition three separately detectable obstruction types exist (algebraic / exposure / emptiness), and the exposure type has a sharp, much weaker, threshold in the test family (3|m or 16|m versus the saturation bound 2^6 3^j).
