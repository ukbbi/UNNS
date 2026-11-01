# R3-C/D  Information carried by complete histories

## 1. Setting and what is *not* claimed
`H(m,t)` = admissible SELECT-II words from source `m` with a given label multiset (content); admissible = every label divides the current state. Relations kept apart: same endpoint ⊃ same content ⊃ swap equivalence (adjacent transposition, both orders admissible; the two orders then have equal products, hence equal intermediate state afterwards) ; content-changing rewrites (v002 R3-law) are not used here.  
Renaming the full state sequence an "invariant" is not done. The candidate quantity below is a **single bit**.

## 2. Lemma J (junction) — PROVED
For labels `N,M` and state `s`, both `N M` and `M N` are admissible from `s` iff for every prime `p`:  
`v_p(s) >= v_p(N)`, `v_p(s)+2v_p(N+1)-v_p(N) >= v_p(M)`, `v_p(s) >= v_p(M)`, `v_p(s)+2v_p(M+1)-v_p(M) >= v_p(N)`  
(direct from `v_p -> v_p + 2v_p(N+1) - v_p(N)`). For `(N,M)=(2,4)` the condition is `v_2(s) >= 3`. Verified on 2 000 random `(s,N,M)` (builder and verifier Z5).

## 3. Theorem R3-T3 (component-separating invariant, infinite family) — PROVED
Source `m=4`. Content `Sigma = {2,4} ∪ A`, with `A` a finite multiset of labels, each `>= 3` (so `A ∩ {1,2,4} = ∅`), the labels 2 and 4 occurring once.  
**(a)** In every admissible word the first label is 2 or 4, and 2 and 4 are never adjacent.  
*Proof.* A label `N >= 3` does not divide the source `4` (divisors of 4: 1,2,4), so it cannot be first. If 2,4 were adjacent they would be at positions `(1,2)`: `4 -2-> 18`, `4 ∤ 18`; `4 -4-> 25`, `2 ∤ 25`. ∎ (This is the resource-deficit form of Lemma J: the junction state is the source, `v_2=2<3`.)  
**(b)** The relative order of two labels that occur once can change only under a swap of those two labels when adjacent. Hence `I(w) = [2 precedes 4]` is invariant on every swap component; and since the first label is 2 or 4, `I(w) = [w_1 = 2]` = which occurrence event comes first: `D: {2} -> {3}` (state 18) or `{2} -> {5}` (state 25). So `I` is a function of the occurrence inventory `D(m_1)` of the first intermediate state: a geometric observable of the history, not a function of source, endpoint or content.  
**(c)** If both orders occur in `H`, the swap complex is disconnected and `I` separates two unions of components. Exact: 121 contents with `A ⊆ {3,5,6,7,8,9,10,11,12,14,15}`, `|A| <= 4`: `I` is constant on every component in all, 2 and 4 never adjacent, 46 contents have both orders (disconnected), component counts `1:69, 2:44, 3:8`.  
**(d) Infinite family.** If `w_1` (2 first) and `w_2` (4 first) are admissible for `Sigma` with common endpoint `E` and `L | E`, `L >= 3`, then `w_1 L`, `w_2 L` are admissible for `Sigma ∪ {L}` (endpoints are equal because the content is). Start from `A_0={5,9}` (words `(2,9,4,5)` and `(4,5,2,9)`, endpoint 9000) and set `L_j = E_j`, `E_{j+1}=(E_j+1)²`: contents of every size, all disconnected, with `I` separating. (Exact enumeration: appending smallest unused divisors of the endpoint, contents of size 4–7, all disconnected; the `L=E` chain, contents of size 4, 5, 6 with labels `5,9,9000,9001²`, has exactly two components of 2 words each, separated by `I`.)  
**Answers to 5.2.** (1) defined; (2) computable from the first label alone; (3) proved invariant under every legal swap; (4) distinguishes components of an infinite family of increasing dimension; (5) not fixed by source, endpoint or label multiset.  
**Applied to B3-3 and B3-4.** `disconnected_3_primes` = `A={3,5,6}`, `disconnected_4_primes` = `A={3,5,6,7}`; the two components (4+6, 12+12 words) are exactly `I=1`, `I=0`. The v001 loss budget `Lambda` was constant on the complex; `I` is not a budget but a first-event datum.

## 4. Limitation theorems (finite-exact + proof sketch)
* `I` is **not complete**: for `A={3,5,9}` there are 3 components (sizes 1, 3, 4) but `I` takes two values; further pair-order bits (e.g. the order of 3 and 5, of 4 and 9) separate the rest. The exact component count is not given by a formula (O3-3).
* `I` says nothing about connected complexes: `loop_3_primes` (source 32, labels 2,3,4,5,8; 30 words) and `loop_4_primes` (source 24; 87 words) each form a **single** swap component, so no component-separating invariant exists there; their loops belong to higher homology (v001).
* Pair-order bits detect only `pi_0`; first/second homology (the loops/voids of HD-1D) need different invariants.
