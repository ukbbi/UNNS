# GEO-HD-1D v001 report (D0-D2 with D3/D4 first results)

**What changed in direction.** The object studied is no longer one static fibre inside another but the *histories* of generation: SELECT-II routes, their endpoint projection, their interchanges.

## Answer to "what distinguishes histories that merge?"
1. **Walk model (D-W).** A history is a walk of valuation vectors in the nonnegative orthant, with step Delta(N) = (2v_p(N+1) - v_p(N))_p. The endpoint is where the walk stops; total displacement telescopes, so only the route carries the history.
2. **Commutation is arithmetic and state dependent (D-T1).** Labels A, B can be exchanged at state m iff A*B | m. More generally all arrangements of a multiset of labels are admissible iff the product of the labels divides m. The ordered route A,B exists iff A*B/gcd(B,(A+1)^2) | m.
3. **Occurrence fibres see the route (D-T4).** Distinct labels from one state always give distinct fibres (Lemma L); consequently the fibre sequence is a *faithful* encoding of a history for fixed source, while the endpoint keeps only its last entry. Every legal swap changes exactly one fibre, so occurrence signatures are not swap invariants. The only occurrence data a swap preserves: source, content (label multiset), endpoint and all but one fibre.
4. **Interchange does not capture all route equivalence (D-T5).** Same source, same content, same endpoint but no chain of legal swaps: (14; 14,3,2) and (14; 2,3,14) both reach 5400, each is isolated; infinite family 14q. Cause: resource contention at the prime 2 (capacity 1, consumers 2 and 14, producer 3).

## Higher-dimensional route structure
* Many histories, one endpoint: H(72)=4, H(72^2)=100, H(72^3)=3601, H(72^4)=194,864, H(72^5)=14,177,856, H(72^6)=1,258,011,667 (recurrence; r<=3 independently by forward DP). Lower bound C(2r,r) proved; far from sharp.
* Route cubes of every dimension: prefix 1^r then r blocks 12/21 (proved via the Independence Lemma). The maximal disjoint-swap cube dimension in 72^r is not r: 1, 2, 4, 5 for r=1..4 (explicit 4-cube in 72^3 from source 3).
* Local legality does not give higher cells at overlaps: (2; 1,2,4) has both adjacent swaps but only 3 of 6 arrangements; at 60 the labels 2,6,10 are pairwise swappable with no triple cell.

## Benchmarks
D-B1 state 6: successors 24,27,32,49; pair classification of labels {1,2,3,6} at 6: (1,2),(1,3),(1,6),(2,3) diamonds, (2,6),(3,6) both admissible but neither order. D-B2 72: four histories, classes {h1,h2}|{h3}|{h4}, fibres and birth/loss (D(16)={2,4} -> D(72)={2,3,6}: loss 4, births 3,6). D-B3 powers of 72 as above. D-B4 pair classification counts (m<=120, A<B<=40): 739 diamonds, 1662 one-way (AB), 682 one-way (BA), 494 both-labels-but-no-order. D-B5 bounded common futures: regression only.

## Proved / finite-exact / open
Proved: D-T0, D-W, D-T1, D-T2(lower bound), D-T3, D-T4, D-T5 (family). Finite-exact: H values, class counts, cube dimensions, census [4,6000]. Open: D-Q1 (swap-class classification), D-Q2 (growth of H(72^r) and cube dimension), D-Q3 (common futures, unbounded), D-Q4..Q6.
Not claimed: C3, novelty. Neighbouring literature (concurrency / directed topology) noted, not read in depth. Same-author caveat applies.
