# GIG-INFO v005 — Forbidden-History Topology and Information Recovery: report

## 1. Mathematics

**Arithmetic.** For prefix-defined systems (all arithmetic regimes) the forbidden complex Y_A is homotopy equivalent to the dead-set nerve N[D_A] (T-NERVE, from the star-intersection lemma L1), so beta_2(K_A) = dim H_1(N[D_A]).
- Nerve model vs direct Y: 1290/1290 agree (158 census positives, 132 held-out positives, 1000 sampled negatives); all 1290 prefix-defined.
- L1 numerical check: 5953 sets T, 4281 nonempty and all acyclic, 141 in the hard case (cap T empty, cup T full); failures 0.
- Non-bounding hollow triangle in N[D]: 288/290 positives, 0/1000 negatives (707 negatives have hollow triangles, all bounding).
- The other 2 positives carry a non-bounding 4-cycle formed by two complementary dead-set pairs.
- Cycle + cocycle certificates verified for 290/290 positives.
- 'No cone point' is not equivalent to non-bounding: 6 (positives) and 105 (negatives) uncone hollow triangles bound.

**Sharp pairs.**
- INFO v002 pair, content [2, 3, 4, 5, 8, 15], sources 480/800: |D| = [11, 7], H1(N[D]) ranks [1, 0], dead sets only in the positive ['{2,3,5,15}', '{2,3,5,8,15}', '{2,5,15}', '{2,5,8,15}', '{3,5,15}', '{3,5,8,15}', '{5,15}', '{5,8,15}'], only in the negative ['{15}', '{3,4}', '{3}', '{4,15}']; non-bounding hollow triangles [14, 0].
- INFO v003 witness, content [2, 4, 5, 9, 14, 15], sources 2520/3780: |D| = [5, 5], H1(N[D]) ranks [1, 0], dead sets only in the positive ['{4,9,15}', '{9,15}'], only in the negative ['{2,4}', '{4,14}']; non-bounding hollow triangles [4, 0].

**S2.** In the 4 census classes with equal (N,h1,Q,Sds) and mixed sign, S2 differences (positive minus negative): {'pos>neg': 0, 'pos<neg': 4, 'equal': 0}. No derivation from the nerve is offered.

**Symbolic transition grammar.** Theorem T-ADJ: for every digraph G on six events, beta_2 of the Hamiltonian-path complex is 0.
- Finite hypotheses: single Z_p acyclic for all 30 pairs ([[0, 0, 0]]); all 435 Z_pq nonempty and connected; all 4060 Z_pqr nonempty (120 disconnected, harmless).
- All 665 distinct S/R/N masks: beta_2 max 0; (beta1,beta2,beta3) distribution {'(0, 0, 0)': 616, '(2, 0, 0)': 42, '(6, 0, 0)': 6, '(8, 0, 0)': 1}.
- Random pair-adjacency systems: {'tested': 300, 'Y_H1_positive': 0, 'beta2_K_positive': 0, 'duality_mismatch': 0}.
- Sharpness: forbidding the consecutive triples [[1, 2, 0], [5, 4, 3]] gives Betti numbers [1, 2, 5, 0, 0, 0] (beta_2 = 5); mechanism: Z1 and Z2 have trivial reduced H0,H1, their intersection has 6 components (reduced b0 = 5), union has reduced b1 = 5.
- Exploratory: 905 of 19993 random 3-adjacency systems have beta_2 > 0.
