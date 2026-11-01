# HD-1D v002 -- threshold theory of route admissibility and swap classes (continues THEOREMS.md of v001, all preserved)

Origin: the threshold law and the {2,3,14} classification were proposed in the review note of 2026-11-01; here they are re-proved, independently re-verified (src/verify_v002.py) and extended.
Scope: all statements concern histories from a FIXED source m (any positive integer). *Complete* histories additionally require a squarefree source; e.g. for {2,3,14} the sources 14q with 2|q or 3|q are not squarefree, so only q coprime to 6 (and squarefree) give complete histories - there the class count is 2, as in v001.
Same-author caveat; C3 not claimed; novelty not assessed.

## D-T7  Threshold law (PROVED)
For an ordering w = (N_1..N_l) put S_j(p) = sum_{i<=j} Delta_p(N_i), Delta_p(N) = 2v_p(N+1) - v_p(N), b_p(w) = max(0, max_{1<=j<=l} -S_j(p)), K(w) = prod_p p^{b_p(w)}. Then
  w is admissible from m  <=>  K(w) | m.
Moreover K(w) is the smallest admissible source, and the admissible sources are exactly the multiples of K(w).
*Proof.* Admissibility of step j means N_j | m_{j-1}, i.e. v_p(m_{j-1}) >= v_p(N_j) for all p. If p | N_j then v_p(N_j+1) = 0 and v_p(m_j) = v_p(m_{j-1}) - v_p(N_j), so the condition is v_p(m_j) >= 0; if p does not divide N_j the condition is vacuous and v_p(m_j) = v_p(m_{j-1}) + 2v_p(N_j+1) >= 0 automatically once v_p(m_{j-1}) >= 0. By induction w is admissible iff v_p(m) + S_j(p) >= 0 for all p, j, i.e. iff v_p(m) >= -S_j(p) for all j, i.e. iff v_p(m) >= b_p(w) for all p. QED
*Corollaries.* K((A,B)) = AB/gcd(B,(A+1)^2) (D-T1(a)); K of all arrangements of a multiset in the "all arrangements" statement is prod N_i (D-T1(c)).

## D-T7'  The swap graph is an induced subgraph (PROVED)
For a label multiset C let G(C) be the graph whose vertices are the distinct arrangements of C and whose edges join arrangements differing by an adjacent exchange of two distinct labels. At source m the swap graph of the histories (m; w) with content C is the subgraph of G(C) induced on A(m) = {w : K(w) | m}. *Proof.* An edge between two admissible words is a legal swap (the exchanged word is admissible; the endpoint is unchanged by D-T1); conversely a legal swap joins two admissible words. QED

## D-T8  Connectivity thresholds and the divisibility filtration (PROVED)
(a) w, w' lie in one swap class at source m iff some path gamma in G(C) from w to w' has M_gamma := lcm_{v in gamma} K(v) dividing m. The minimal such M_gamma form an antichain under divisibility (the *connection thresholds* of the pair); src/thresholds.py:connect_thresholds computes it.
(b) The induced graph at m depends only on A(m). If m' = lcm{K(w): w in A(m)} then m' | m and A(m') = A(m). Hence every swap-graph shape that ever occurs for the content C occurs at a source in the lcm-closure L(C) of {K(w)}, a finite set; the classification of C is a finite computation.
(c) *Monotonicity.* If m | m* then A(m) is contained in A(m*) and every swap connection persists: classes at m* are unions of classes at m, plus possibly new classes made of newly admissible arrangements. A class never splits, but the number of classes is not monotone: {2,3,14} has 2 classes at 14 and 1 at 28; {2,3,8} has 1 class at 2 and 2 at 8.
*Proof.* (a) a path with all vertices admissible exists iff every vertex threshold divides m iff the lcm does. (b) A(m') contains A(m) (thresholds divide m') and is contained in A(m) (m' | m). (c) K(w) | m | m*. QED

## D-T9  The family {2,3,N} (a PROVED; converse FINITE-EXACT)
Let N >= 4 and N != 2, 3 (distinct labels). Write x = 2, y = 3, z = N; a = v_2(N), b = v_3(N), c_2 = v_2(N+1), c_3 = v_3(N+1), R = prod_{q>=5} q^{v_q(N)}. Displacements: x: (p=2: -1, p=3: +2), y: (+4, -1), z: (2c_2 - a, 2c_3 - b); primes q >= 5 only matter through the consumption v_q(N) at label N, so K(w) = R * 2^{d_2(w)} * 3^{d_3(w)}. G is the 6-cycle xyz - xzy - zxy - zyx - yzx - yxz - xyz.
(a) If N = 2 (mod 6) then (a >= 1, b = 0, c_2 = 0, c_3 >= 1) and the thresholds are
 K(2,3,N) = 2^{max(1,a-3)} R,  K(2,N,3) = K(N,2,3) = 2^{a+1} R = 2N,  K(N,3,2) = 2^a R = N,  K(3,N,2) = K(3,2,N) = 3 * 2^{max(0,a-3)} R.
If N = 3 (mod 6) then (a = 0, b >= 1, c_2 >= 1, c_3 = 0) and
 K(2,3,N) = 2 * 3^{b-1} R = K(2,N,3),  K(N,2,3) = N,  K(N,3,2) = K(3,N,2) = 3N,  K(3,2,N) = 3^{max(1,b-1)} R.
In both cases at source m = N exactly two arrangements are admissible, the reverse of each other - (2,3,N) and (N,3,2) for N = 2 mod 6; (N,2,3) and (3,2,N) for N = 3 mod 6 - and they are opposite vertices of the hexagon. So the content has two swap classes at m = N. (The first is the v001 case N = 14: thresholds 14,28,21,21,28,14.)
*Proof.* The threshold formulas follow from D-T7 by listing the prefix sums of the three displacement vectors in each order (deficits at p = 2, 3; R from the consumption of primes q >= 5 by N). At m = N, T(N,3,2) = N and K(2,3,N) | N (N=2 case), the other four thresholds contain the factor 3 or 2N and do not divide N; the N = 3 case is symmetric. QED
(b) *Converse (FINITE-EXACT).* For 4 <= N <= 400, the content {2,3,N} has a split source iff N = 2 or 3 (mod 6) and N >= 8 (132 values; the minimal split source is N itself in every case). The structure depends on N only through (a, b, c_2, c_3); the splitting criterion "(a >= 1 and c_3 >= 1) or (b >= 1 and c_2 >= 1)" was checked for all realisable exponent tuples in [0,12]^4 (600 cases). A formal proof for all N (a regime argument for the max(0,.)-expressions) is not given.
*Reading.* N = 2 (mod 6) means N consumes 2 while N+1 feeds 3; N = 3 (mod 6) means N consumes 3 while N+1 feeds 2: the label N joins the 2<->3 production cycle of the labels 2 and 3 and contests the same initial capacity.

## D-T10  Complete classification for {2,3,14} (PROVED)
Thresholds: K = 14 for (14,3,2) and (2,3,14); 28 for (14,2,3) and (2,14,3); 21 for (3,14,2) and (3,2,14). All admissible arrangements from m end at 5400 (m/14). Number of swap classes of the histories from source m:
  0 if neither 14 nor 21 divides m;  2 if 14 | m and gcd(m/14, 6) = 1;  1 otherwise.
In particular from 14q: 2 classes iff gcd(q,6) = 1. The two original histories are connected iff 28 | m or 42 | m (connection thresholds 28, 42).
*Proof.* A(m) is {the two 14-vertices} if 14|m, plus {the two 28-vertices} if 28|m, plus {the two 21-vertices} if 21|m, and 7 | m is necessary. On the hexagon (14,3,2)-(3,14,2)-(3,2,14)-(2,3,14)-(2,14,3)-(14,2,3)-back: the 14-vertices are opposite; adding the 28-pair joins them by the path through (14,2,3),(2,14,3); adding the 21-pair by the path through (3,14,2),(3,2,14); the 21-pair alone is an edge. Hence the count is 2 exactly for 14 | m, 28 and 21 not dividing m. QED
v001's family (squarefree q coprime to 210) is the part q coprime to 6 of this classification, and the squarefreeness / prime-5,7 restrictions there were unnecessary for the split statement for fixed-source histories.

## Census (FINITE-EXACT, results/THRESHOLD_CENSUS.json)
Distinct three-label contents with labels <= 30: 127 of 4060 have a split source (each has a unique minimal split source in the sample); four distinct labels <= 14: 103 of 1001; multisets with a repeated label (sizes 3-5, labels <= 10): 121 of 2355. Largest component count seen: 2 (three labels), 3 (four labels, e.g. {2,3,8,9} at source 8: classes {(2,3,8,9)}, {(2,9,8,3)} and a class of four arrangements starting with 8).

## Open (D-Q1 refined)
(i) A proof of the D-T9 converse for all N and a classification of all split three-label contents (the {2,3,N} family is one pattern among 127 contents; others such as {2,8,15}, {2,9,15} split at sources 40, 45). (ii) For k labels, the structure of the lcm-closure L(C) and the maximum number of components. (iii) How independent prime obstructions combine (components appearing/merging as the source gains prime factors: the "divisibility filtration" of the history geometry). (iv) Relation of the swap classes to the orthant-walk picture (D-W) - a geometric description of the hexagon holes.
