# D4-T6 / D4-T7 — resource-saturated connectivity and classified obstructions

Setting: fixed alphabet A, fixed source m, fixed endpoint; the set H of all admissible histories with that endpoint; the contents of H form (part of) a toric fibre {c >= 0 : V c = d}.

## Operational dichotomy (the resource-sensitive completeness statement)
For a move set M of kernel vectors:
1. **Above the resource condition** (every content satisfies P(c) | m): H is one rewrite class iff the content fibre is connected by M.  With M ⊇ Graver basis, always.  [T6a, PROVED]
2. **Below it** the history space may be disconnected for exactly three kinds of reasons, which are separately observable:
   (a) *algebraic*: the content fibre is disconnected under M (D-B4); holds at every source;
   (b) *exposure*: contents are linked by a move in M but no history has a contiguous redex because the block's context labels cannot be moved out of it (D-B3/D4-T7);
   (c) *emptiness*: some content has no admissible history from m (sources outside the support of the fibre).

**T6a Saturation theorem (PROVED).** Let the contents of a fibre be connected by Graver moves staying inside the fibre.  If P(c) | m for all contents c, then all histories form one rewrite class.
Proof: by the v001 theorem all arrangements of each content are admissible, so each content is one swap class (adjacent swaps between arrangements stay admissible).  For a Graver move c -> c+z, take any history of c, swap it into the form u·r (u an arrangement of z-, r the rest), replace u by v: u·r and v·r are admissible by the same theorem.  Hence adjacent contents' classes merge.  Graver bases are Markov bases (Sturmfels), so the content fibre is connected.  Verified on random fibres with Graver moves: 44 fibre-source pairs, 0 violations (Y4).

**Quotient description (PROVED).** Rewrite classes are exactly the connected components of the graph whose nodes are swap classes and whose edges are exposed redexes (a redex u or v occurring as a contiguous block in some word of the class, whose replacement is admissible).  Immediate from the definitions.

## The test family   F_j :  2^4 3^j  <->  1·8^2 3^j     (move z=(1,-4,0,2) on {1,2,3,8})
* Each content has exactly ONE swap class at every source (checked j<=8).
* **D4-T7 dichotomy.** Over every source (divisors of P*), the two contents are rewrite-connected iff **3 | m or 16 | m**; otherwise (sources with v3(m)=0, v2(m) in {1,2,3}; where both contents are nonempty) the history space has exactly two rewrite classes.  FINITE-EXACT for j = 1..8 over all sources (0 violations, 135 table entries up to j=5 in the verifier, full table to j=8 in results/DICHOTOMY.json).
* **Exposure obstruction (PROVED for all j).** Suppose 3 ∤ m and v2(m) <= 3.  Labels 3 can only be applied after a state gains 3-valuation; R(2)=9/2 and R(8)=81/8 are the only labels that do (R(1)=4, R(3)=16/3 lose it or are neutral).  In content 2^4 3^j all 2s lie in the block 2222, so before it no 3 can occur and v2 stays <= 3 < 4: the block 2222 is never executable.  In content 1·8^2 3^j all 8s lie in the block, so again no 3 precedes it, the block starts at position 0, and each order of {1,8,8} fails (needs v2 >= 4 or 6).  So no redex is exposed and the two classes cannot be joined.
* Sufficiency for general j is OPEN: when 16 | m the redex 2222 occurs at position 0 followed by 3^j, but 3^j needs v3 >= j and the block gives only 8, so for j > 8 an interleaved arrangement is needed.  The verified range is j <= 8 (builder) and j <= 5 (independent verifier, +j<=8 in --full).

## {1,2,3}: positive completeness (FINITE-EXACT)
For the three-label alphabet the single relation 1^7 <-> 2^2 3^4 plus swaps connects every pair of equal-endpoint histories at every source, in the box a<=1, b<=4, c<=8, fibre length >= 2: 30 fibres, 840 fibre-source pairs, 0 disconnected (builder), 16 fibres / 364 pairs re-checked independently (Y5).  No general proof; recorded as OPEN (the fibres are rank-1 chains c + t(7,-2,-4), so connectivity is a statement about consecutive contents; a proof would need exposure of a redex for each consecutive pair).
