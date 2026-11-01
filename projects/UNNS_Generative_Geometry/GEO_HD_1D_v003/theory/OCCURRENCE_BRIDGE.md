# OCCURRENCE_BRIDGE -- Stage D (D9, D-Q3): occurrence fibres and persistence-restricted swap connectivity

Statuses as in THRESHOLDS.md. Same-author caveat; C3 NOT claimed. Fixed-source scope. The benchmark histories are the complete histories ending at 72^r (squarefree source), r <= 3 (H = 4, 100, 3601); r = 4 (194,864 histories) was NOT run.

## Orthant form of the fibre (PROVED; = v001 Lemma V restated)
d in D(m) (d >= 2) iff v_p(m) >= 2 v_p(d) for every prime p | d. So the indicator rho_d of the history is the indicator of the walk lying in the shifted orthant O_d = {v : v_p >= 2 nu_p(d)}; for a prime power p^k it is the single half-space v_p >= 2k. Persistence of an index = sidedness with respect to an orthant of the valuation-walk geometry.

## Local discrepancy (PROVED)
For a legal swap at position i with intermediate states a = T_A x, b = T_B x (A != B), only the entry D(m_{i+1}) of the fibre sequence changes (v001 locality). The discrepancy Delta = D(a) symmetric-difference D(b) is nonempty (Lemma L) and
   |Delta| = prod_p (e_p(a)+1) + prod_p (e_p(b)+1) - 2 prod_p (min(e_p(a), e_p(b)) + 1),  e = half-valuation vector,
because D(a) intersect D(b) = D(min(e(a), e(b))). A swap preserves rho_d iff d is not in Delta, i.e. iff a and b lie on the same side of O_d. (Verifier X5: all 194 legal swaps of the benchmark r <= 2 [r <= 3 in --full] satisfy the formula, with |Delta| > 0.)

## Persistence-restricted swap graphs
For an index d >= 2 keep a legal swap (h, i) in the mode
* **preserve**: iff d is not in Delta (rho_d unchanged);
* **after birth**: iff d is not in Delta, or d does not occur in any of D(m_0..m_i) (the shared part of the fibre sequence before the changed entry).
Both delete edges, so classes(unrestricted) <= classes(after birth) <= classes(preserve) (PROVED; checked).
Using ALL indices at once leaves no edge (Lemma L): the fibre sequence determines the history. A single index d is the reduced, informative property: it records only on which side of one orthant boundary the changed node lies, not the full label or fibre sequence.

## Results (FINITE-EXACT; complete histories ending at 72^r, all swap classes counted over all sources)
| r | histories | classes | preserve d=2 | preserve d=3 | preserve d=4 | preserve d=8 | after d=2 | after d=3 |
|---|---|---|---|---|---|---|---|---|
| 1 | 4 | 3 | 4 | 4 | 4 | 3 | 4 | 3 |
| 2 | 100 | 22 | 36 | 51 | 62 | 54 | 32 | 24 |
| 3 | 3601 | 142 | 413 | 551 | 864 | 1009 | 355 | 239 |
Full tables for d in {2,3,4,6,8,9,12,18,24,36}: results/OCCURRENCE_BRIDGE.json.
Reading. (1) New components arise in both modes: restricted connectivity is strictly finer, already at r=1 for d=2: the two histories h1, h2 of the 72 benchmark (same source, content and endpoint, swap-equivalent) have rho_2 = (0,1,1,1) and (0,1,0,1), so the 2-preserving graph separates them (4 classes instead of 3). (2) The number of classes is *not monotone along divisibility of d*: for r=3, d=12 gives 678 and d=36 gives 493 (12 | 36); same for r=2 (43 vs 33). (3) "After birth" is consistently coarser than "preserve", and for composite d such as 12, 18, 24, 36 it does not refine at all at r=2 (still 22 classes), i.e. composite indices are born late in these histories and early swaps do not see them.

## What is and is not established
Established: the orthant reformulation, the closed form for the discrepancy, the refinement chain, and the finite tables. NOT established (OPEN): a structural classification of the restricted classes, a counting law in r, any statement beyond r = 3 or beyond the 72 family, and whether some d gives a restricted graph with an obstruction not already forced by prime-power indices.
