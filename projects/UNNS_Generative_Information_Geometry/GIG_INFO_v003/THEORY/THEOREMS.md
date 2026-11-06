# GIG-INFO v003 — theorem and result register
Tags: [PROVED] proof given here; [FINITE-EXACT] exhaustive exact computation on the stated finite domain; [BOUNDED] holds on the domain tested only; [OPEN].
Domain D = six-label census (labels <=16; 346,859 regimes; 158 with beta2>0). Y = 1[beta2>0 over GF(2)].
Local quantities of the legal-swap graph G of a regime: d(w) degree; q(w) number of 4-cycles of G through w (= commuting-swap square faces of K containing w); s(w)=sum_{u~w}(d(u)-1); B2(w) the radius-2 ball; N, E, sq=#squares, Sd2=sum d^2, Ss2=sum s^2, SB2=sum|B2|, SB22=sum|B2|^2.

## Theorem T1 [PROVED] (radius-2 formula; the identity proposed in the v002 assessment)
For every w in G:  |B2(w)| = 1 + d(w) + sum_{u~w}(d(u)-1) - q(w).
Proof. G is an induced subgraph of the permutohedron graph (vertices = permutations, edges = adjacent-position swaps). Swaps change permutation parity, so G is bipartite; hence every endpoint v != w of a non-backtracking 2-walk w-u-v is at distance exactly 2, and every vertex at distance 2 arises. The number of such walks is s(w). In the full permutohedron a vertex v = w.s_i.s_j (s_i != s_j adjacent-position swaps) is reached by exactly two walks if the swaps commute (|i-j|>=2: via w.s_i and via w.s_j) and by exactly one walk if |i-j|=1 (s_i s_{i+1} != s_{i+1} s_i). In G both walks to v survive iff both middle vertices lie in G, i.e. iff w,u1,v,u2 is a 4-cycle of G; and every 4-cycle through w arises this way from a unique v. So |{distance 2}| = s(w) - q(w). Adding w and its d(w) neighbours gives the formula. QED.
Machine check: identical to the pure-python ball histograms on 4,157 regimes (0 mismatches) and at every vertex of the 30 regimes re-checked with definition-level code (tests).

## Corollaries [PROVED]
C1.  SB2 = N + Sd2 - 4 sq.            (sum T1 over w; sum_w s(w) = Sd2 - 2E; sum_w q(w) = 4 sq.)
C2.  Hence for two systems with equal N and equal radius-1 histogram h1 (so equal E, Sd2): SB2 equal  <=>  sq equal. The mean of |B2| carries no information beyond (N,h1) and the square count.
C3.  SB22 = N + Sd2 + Ss2 + Sq2 + 4E + 2Ss - 8 sq + 2Sds - 2Sdq - 2Ssq   with Ss=Sd2-2E, Sds=sum d s, Sdq=sum d q, Ssq=sum s q, Sq2=sum q^2.  (expand (1+d+s-q)^2; verified on all 346,859 regimes.)
C4.  Therefore anything beyond first order in |B2| enters through degree-correlation/walk sums Ss2, Sds, Ssq, Sdq: sums over pairs of two-step walks from a common start.

## Results on D
R1 [FINITE-EXACT] Smallest separating pairs. Of all scalar subsets of size <=4 from the 15-feature pool, no single scalar has zero residual (best: SB22 hides 36 positives in 18 mixed classes). The minimal separating pairs include (N,SB22), (sq,SB22), (SB2,SB22), and, in the second-order pool, (sq,Ss2), (Sd2,Ss2), (Sd3,Ss2), (Sq2,Ss2), (Ss2,Sds), (Ss2,Sdq), (Ss2,Ssq). Every separating pair contains a second-order radius-2 sum (SB22 or Ss2). Zero residual: also for the full h2 histogram and for the f-vector.
R2 [FINITE-EXACT] The 66 positives that (N,h1) leaves in mixed classes (F18): adding ONE scalar to (N,h1) resolves how many of them -- Ss2: 66 (all), SB22: 66 (all), f3: 64, Sds: 59, Ssq: 59, hx: 47, Sq2: 44, Sdq: 44, sq: 42, SB2: 42; nothing first-order (E, Sd2, Sd3, dmax, dmin) resolves any. So for this census a single walk-pair sum, Ss2 = sum_w s(w)^2 (ordered pairs of two-step non-backtracking walks from a common start), added to the radius-1 data carries all the missing information.
R3 [FINITE-EXACT, SHARP WITNESS] Content (2,4,5,9,14,15), sources 2520 (beta2=1) and 3780 (beta2=0): N=540, equal h1, equal hq, equal E=1278, sq=738, Sd2=12212, SB2=9800 (arithmetic and graph data re-derived with definition-level code), but different h2 (SB22 = 180420 vs 180408). Cellular certificate for the positive: 96-face 2-cycle z and 2-cocycle phi with phi(z)=1, verified from the definition; beta2=0 for the negative from two rank routes and the v001 engine. The f-vectors differ in f3 only (291 vs 292); the two arrangement sets share 468 of 540 arrangements (72 swapped), and the 3-face sets differ in 76/77 faces (not "one face").  Consequence [PROVED by witness]: no function of (N,h1,hq) -- hence of (N,E,sq,Sd2,SB2) -- determines Y on D (165 such positive/negative pairs, 22 positives, all with different h2).
R4 [FINITE-EXACT] Non-triviality. The zero residuals are not an artefact of a near-injective signature: for (N,SB22) and the other separating pairs 104 of the 151 positive masks lie in pure classes of size >=2 (largest pure positive class 15); placing the positives at random among regimes of equal N hides 133-149 of 151 (mean 143), real value 0 (no shuffle in 300 gave 0). 47 positives are alone in their class (no negative has their signature -- true but weaker evidence).
R5 [BOUNDED] Pre-registered held-out test H6 (THEORY/PREREGISTRATION.md, sha-256 62b97177...): 6000 sampled six-label contents with maximum label 17..22: 263,124 regimes, 132 positives; pooled with D: 609,983 regimes, 290 positives.
   - S_B=(sq,Ss2): 0 mixed classes in H6 and in D u H6.   CONFIRMED.
   - S_C=(Sd2,Ss2): 0 mixed classes in H6 and in D u H6. CONFIRMED.
   - (N,h1,h2): 0 mixed classes in H6 and pooled. (not a registered prediction; reported.)
   - S_A=(N,SB22): 3 mixed classes in H6 (3 positives), 6 mixed classes (10 positives) in D u H6.  The pre-registered prediction for S_A is FALSIFIED. In 5 of the 6 classes the colliding systems differ in sq and Ss2; in the sixth (N=576) they differ in Ss2 only.
   - P2: (N,h1) leaves 143 of 290 positives in mixed classes (pooled). CONFIRMED.
   Non-triviality on the pooled set: 206 of 290 positives in pure classes of size >=2; the random-placement null hides 267-285 of 290 positives; real value 0.
   So the registered claim "all three pairs separate" is false as stated (P1 fails through S_A); the weaker, more structured statement "(sq,Ss2), (Sd2,Ss2) and the h2 histogram separate" survived out of sample on 263k new regimes. (N,SB22) is a good fingerprint on D but not a law.
R6 [BOUNDED, INCONCLUSIVE] Seven-label exploratory H7 (120 contents of {1..14}, 10,130 regimes, 11 positives): every candidate signature, including (N,h1), has zero mixed classes; N alone does not. The sample is too small and its signatures nearly injective to discriminate; no transfer claim is made at k=7.

## What is NOT claimed
No theorem that radius-2 data determine beta2; no claim beyond six distinct labels (k=7 untested at power) or beyond the sampled label ranges; Ss2 is an empirical separator. The mechanism linking sums over pairs of two-step walks to the presence of a hollow 2-cycle is [OPEN].
Naming correction (v002, unchanged numerically): v002's E_distinct is uniform over distinct rank-indexed masks (219,146), not over distinct labelled arrangement sets (346,859 = every regime). See RESULTS/F17_witness_anatomy.json.
Also noted: the h2 histogram contains N (its counts sum to N), so the zero residual of (N,h2) in v002 equals that of h2 alone.
