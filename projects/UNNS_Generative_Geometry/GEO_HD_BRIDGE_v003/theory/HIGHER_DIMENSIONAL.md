# R3-E  Higher-dimensional history geometry

## What is established here
**Restricted R3-T4 (arithmetic obstruction ⇒ topological property) — PROVED.**  
*Blocked-pair lemma.* Let a complex of admissible words (fixed source and content) contain two single labels `a,b` such that no word has `a,b` adjacent with both orders admissible. Then `[a before b]` is constant on components, and if both values occur the complex is disconnected. The arithmetic input is Lemma J (`HISTORY_INVARIANTS.md`); for source 4 and `{2,4} ∪ A` the obstruction is a *resource deficit*: no `A`-label can fire at the source (`N ∤ 4`) and `v_2(4)=2 < 3`.  
This gives a family of arbitrarily high history-cube dimension (content size `n` ⇒ dimension `n-1`) with `pi_0 >= 2`, proved by arithmetic, not by assigning component numbers.

**Not achieved (R3-T4 in full generality): OPEN.** No theorem predicts the number of components, produces a family with proven non-trivial `H_1`/`H_2`, or classifies obstructions to filling recombination cycles. The loop complexes (source 32, labels 2,3,4,5,8 and the four-prime analogue) are connected; their homology is v001's, not re-derived here.

## Four quantities kept apart (as in v002)
| quantity | meaning | 3-prime example | 4-prime example |
|---|---|---|---|
| V | valuation coordinates | 4 | 5 |
| A | active constraint primes | 3 | 4 |
| R | history-cube dimension | 4 | 5 |
| G | peak realised state-geometry dimension | 3 | 4 |
State geometry of every state on these routes is contractible (B2-T1), so the disconnectedness is a property of the *relations between histories*, never of a snapshot. The first-event bit `I` is a geometric observable of the history (the first occurrence event), which no snapshot of the endpoint or budget sees.

## Distinctions (6.1)
Components (R3-T3/T4-restricted), loops and voids (v001/HD-1D, not re-proved), failure of local completion (swap-square failure: Lemma J fails), resource obstruction (feeding deficit), algebraic obstruction between contents (rewrite law, v002) are listed separately; only the first and fourth are connected by a theorem here.
