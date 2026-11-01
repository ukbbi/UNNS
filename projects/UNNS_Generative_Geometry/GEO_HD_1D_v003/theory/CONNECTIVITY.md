# CONNECTIVITY -- Stage B, part 1: the feeding digraph and block factorisation (D7-T1 and beyond)

Statuses as in THRESHOLDS.md. Same-author caveat; C3 NOT claimed.

D7-T1 (connectivity iff some path threshold divides m) is v002 D-T8(a); it is a correct *exact* characterisation but needs a search over paths. The results below are global structure theorems that make the search unnecessary in large cases.

## Definitions
For labels A != B say A *feeds* B if gcd(A+1, B) > 1 (a prime of A+1 divides B: running A makes resource that B consumes). The feeding digraph of a content has the DISTINCT labels as vertices. Its strongly connected components (SCCs) are *blocks*; the condensation is acyclic, so the blocks have a topological order (feeders first).

## Lemma NF (PROVED)
If x does not feed y and (x, y) is admissible from a state s, then (y, x) is admissible from s.
*Proof.* gcd(x+1, y) = 1 gives gcd(y, (x+1)^2) = 1, so K((x,y)) = xy/gcd(y,(x+1)^2) = xy (v001 diamond criterion). K((y,x)) = xy/gcd(x,(y+1)^2) divides xy. So K((y,x)) | K((x,y)) | s. QED (Verifier X1: 12,077 instances and all label pairs below 120.)
In words: a pair that is not "directed" through a shared prime commutes whenever it is legal at all.

## Theorem F2 -- block factorisation (PROVED)
Let C be any content (repeats allowed), B_1, .., B_r the blocks in a topological order of the condensation, C_i the sub-multiset of C on B_i, and m_0 = m, m_i = m_{i-1} * prod_{x in C_i} (x+1)^2/x. Then the number of swap classes of C at source m is
  prod_{i=1..r} (number of swap classes of C_i at source m_{i-1}),
and is 0 as soon as one factor is 0 (some m_{i-1} not an integer counts as 0).
*Proof.* (1) *Sorting.* If w is admissible and (x, y) are adjacent in w with x in a later block than y, then x does not feed y (an edge x->y would force block(x) <= block(y)), so by Lemma NF the swap is legal. Bubble-sorting by block (stable, so the order inside every block is preserved) therefore reaches the block-sorted word u_1...u_r, u_i = the subword of w on C_i, through legal swaps; in particular each u_i is admissible from m_{i-1}.
(2) *Invariant.* For an admissible word w let pi_i(w) = its subword on C_i. A legal swap of two letters of different blocks leaves every pi_i unchanged. A legal swap of two letters of the same block B_i changes pi_i by one adjacent exchange and leaves the others unchanged; sorting w and the swapped word gives two admissible block-sorted words that differ by that exchange inside u_i, so the exchange is a legal swap of C_i from m_{i-1}. Hence the class of pi_i(w) in the swap graph of C_i at m_{i-1} is invariant under legal swaps: w |-> ([pi_1(w)], .., [pi_r(w)]) is constant on swap classes.
(3) *Bijection.* Every tuple of admissible block words concatenates to an admissible word (the entry state of block i is m_{i-1} whatever the choice in earlier blocks), so the map is onto the product of the class sets; two words with equal tuples are connected: sort both, then move inside each block along a path of C_i, each such step being a legal swap of the whole word. QED
(Verifier X2: direct simulation without the threshold machinery; builder census 66,325 content-source pairs including repeated labels, 0 violations.)

## Corollaries
* **F1 (acyclic feeding digraph).** If every block is a single label then at every source there is at most one swap class; moreover for any linear extension tau (the sorted word) K(tau) divides K(w) for every arrangement w, so K(tau) is the universal minimal threshold; the admissible set is a weak-order lower set (see ROUTE_TOPOLOGY.md). *Proof.* sorting step (1) of F2. QED
* **A block with at most two distinct labels (each once) never splits.** It has at most 2 arrangements, which are adjacent. Hence for contents of DISTINCT labels: *a split (>= 2 classes at some source) requires a block with at least 3 labels.* (For repeated labels a two-label block can have three or more arrangements and this is not claimed.)
* **D-T9 converse (PROVED, upgrades the v002 FINITE-EXACT status).** For N >= 4, N != 2,3: the feeding digraph on {2,3,N} is strongly connected iff N = 2 or 3 (mod 6). Indeed 2 and 3 feed each other (gcd(3,3), gcd(4,2)); N feeds 2 iff N is odd; N feeds 3 iff N = 2 (mod 3); 2 feeds N iff 3 | N; 3 feeds N iff N is even. So N joins the block iff (N odd or N = 2 mod 3) and (N even or 3 | N), i.e. N = 3 mod 6 or N = 2 mod 6. Otherwise the blocks are {2,3} and {N}, both with at most 2 arrangements, so there is no split. Combined with v002 D-T9(a) (N = 2,3 mod 6, N >= 8 splits at m = N), {2,3,N} has a split source iff N = 2,3 mod 6 and N >= 8. (Verifier X3: SCC rule for N <= 600/3000, split rule for N <= 120/220 by direct simulation.)

## Hub-descent criterion (PROVED, sufficient, not necessary)
A *hub* is an arrangement h with K(h) | K(w) for all w such that every w has a swap path w = v_0, .., v_s = h with K(v_{i+1}) | K(v_i). If a hub exists the content never splits. *Proof.* If w is admissible at m then K(h) | K(w) | m and every v_i is admissible, so w is connected to h. QED
Finite census (builder): labels <= 30, 3 labels: 3408 contents have a hub and no split, 0 have both, 525 have neither a hub nor a split, 127 split (all without a hub); 4 labels (<= 14): 773 / 0 / 125 / 103. A hub is therefore not necessary.

## Census on three labels (FINITE-EXACT; labels <= 30)
4060 contents; 257 have a strongly connected feeding digraph; 127 split; every split content is strongly connected (this follows from the corollary above) but 130 strongly connected contents never split, e.g. (2,4,15), (2,5,9), (2,6,7). The exact criterion that separates them is the prefix-set criterion of OBSTRUCTIONS.md.
