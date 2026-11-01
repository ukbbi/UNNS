# D4-T9 — structural information across rewrites

Occurrence fibre D(m) = divisors d >= 2 with d^2 | m  (so the divisor set of the squarefree-root part); a history induces a fibre sequence D(x_0), D(x_1), ...  and event word (births, losses, reappearances).
* births - losses = |D(end)| - |D(start)| depends only on the endpoint: it is a rewrite invariant (D-B1: A has (7,0), B has (14,7), difference 7 each; cube family: 7r for all 2^r histories).
* Fibre sequences are NOT rewrite invariants: A and B have different lengths and different sequences; across the cube family the 2^r histories are pairwise distinguished by their fibre sequences (r<=4), but the (births, losses) pairs are injective only for r <= 3 (distinct pairs 2,4,8,15,24 for r=1..5).  So the event summary is a faithful history-label for r<=3 only.
* Information: rank V = 2 on {1,2,3,8} is what the endpoint remembers; the lost kernel (rank 2) is exactly the information erased by the endpoint and is what rewrites move through.
Scope: complete-root histories (D-B7) are only partly covered — squarefree-root remark 1 -> 4; no general result.
