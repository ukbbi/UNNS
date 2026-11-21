# FUG-I v005 — exact mathematical results

**Date:** 20 November 2026. **Scope:** all-label SELECT-II histories `T_N(x)=x(N+1)^2/N`, `N|x`. The founding UNNS `M ⟂ N` formula remains unchanged.

## Complete 84-layer transport census

| First new history depth | Proper index-divisibility pairs |
|---:|---:|
| 0 — no new words | 193 |
| 1 — immediate new label | 108 |
| 2 — delayed | 6 |
| **Total** | **307** |

All six unrestricted depth-two pairs: (12,24), (12,36), (12,60), (12,72), (24,72), (36,72). Two independent algorithms agree: paired-backward-branch recursion and complete inverse word-set enumeration.

## Exact unrestricted odd-r doubling classification

For every odd r≥1, let A=F_(12r) and B=F_(24r). The first new depth is **2 if L_(12r)/2 is squarefree, otherwise 1**. The two-step history (7,2), with minimal endpoint 288, always appears in B and not A. Thus the problem of whether it is the first activation is entirely the one-step squarefree gate.

Fully factored numerical certificates, all primes checked independently by trial division:

| r | Factorization of L_(12r)/2 | First new depth |
|---:|---|---:|
| 1 | 7·23 | 2 |
| 3 | 7·23·103681 | 2 |
| 5 | 7·23·241·2161·20641 | 2 |
| 7 | 7²·23·167·14503·65740583 | 1 |

At r=7, N=6 is a new immediate label. **For every odd s≥1**, this persists at `(F_(84s),F_(168s))`, giving an infinite first-depth-one obstruction family.

## Matched non-Fibonacci controls

For every prime p≥5, the pair `(144,288p)` has identical full one-step label sets, but the new word (7,2) appears in the second target. First new depth is exactly 2. Ten examples are certified in `matched_integer_controls.csv`.

## Unbounded distinct-content mergers at Fibonacci targets

For each t≥1, the `t+1` distinct words

`1^(7j) 2^(2(t−j)) 3^(4(t−j))`,  j=0,...,t,

are all legal from `2^(2t)3^(4t)` and end at `2^(16t)3^(4t)`. The exact identity `r_1^7=r_2^2 r_3^4=4^7` guarantees equal multipliers; content vectors are different. A Fibonacci target divisible by the common endpoint exists at index `z(2^(16t)3^(4t))`; scaling the common source lifts all t+1 histories to that target. The first eight finite constructions are replayed in the verifier.

## Status and interpretation

**PROVED:** all-label recursion, square-kernel criterion, odd-r Lucas quotient gate, infinite obstruction, matched infinite non-Fibonacci family, unbounded distinct-content mergers at Fibonacci targets.

**VERIFIED-EXACT:** first-84 census; certified r=1,3,5,7 factorizations; exact sampled modular witnesses; small-control oracle.

**OPEN:** infinitude of odd r satisfying the squarefree Lucas quotient condition; complete first-activation distribution at unbounded Fibonacci indices; universal history-kernel classification; physical interpretation.

The finite mathematics establishes a clear boundary between the broad arithmetic capacity of the Substrate and structural behavior special to an imposed sequence. It neither assumes nor refutes any overarching universality proposal.
