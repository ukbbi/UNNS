# FUG-I v003 — Mathematical proofs and evidence register

## FUG3-T1. Minimal endpoint theorem [PROVED — elementary extension of previous threshold theory]

For any finite word `w=(N_1,...,N_k)` with `Q_{j-1}=a_{j-1}/b_{j-1}` reduced, a positive integer source `x` supports the word if and only if `K(w)|x`, where

`K(w)=lcm_j (b_{j-1}N_j / gcd(a_{j-1}, b_{j-1}N_j))`.

For every admissible source `x`, the endpoint is `x * Q_k`. Consequently the possible endpoints are exactly `E(w)*positive integers`, where `E(w)=K(w)*Q_k` is a positive integer. In particular,

`w in W(y) iff E(w)|y`.

**Proof.** Immediately before the `j`-th move the current state is `x*a_{j-1}/b_{j-1}`. The move with label `N_j` is legal exactly when `x*a_{j-1}/(b_{j-1}N_j)` is an integer. This is equivalent to `(b_{j-1}N_j / gcd(a_{j-1},b_{j-1}N_j)) | x`. Requiring all steps gives the least common multiple `K(w)`. The endpoint of the minimum source is a legal positive integer, `E(w)`, and scaling the source by `q>=1` scales every intermediate state and endpoint by `q`. Conversely every legal source is such a multiple. The empty word has `K=E=1`. QED.

**Provenance note.** GEO-HD-1 already has minimal source-threshold theory for labelled histories. This theorem is a self-contained endpoint formulation used for FUG-I; no priority over earlier arithmetic/history literature is asserted.

## FUG3-T2. Complete-history gcd-meet theorem [PROVED]

For arbitrary positive integers `a,b`,

`W(gcd(a,b))=W(a) intersect W(b)`.

**Proof.** By T1, `w in W(a) intersect W(b)` iff `E(w)` divides both `a` and `b`, iff it divides `gcd(a,b)`, iff `w in W(gcd(a,b))`. QED.

**Fibonacci corollary.** The classical identity `gcd(F_m,F_n)=F_{gcd(m,n)}` gives

`W(F_m) intersect W(F_n)=W(F_{gcd(m,n)})`.

The meet is an *equality of complete ordered word sets*, not just a counting inequality or an equality of incoming label sets. The proof is a combination of the fixed substrate, the chosen self-substitution, and independent Fibonacci divisibility.

**Join caution.** `W(lcm(a,b))` contains `W(a) union W(b)`, but equality may be strict. For `a=4,b=9`, the one-step label `5` belongs to `W(36)` and neither `W(4)` nor `W(9)`. Longer mixed histories also appear.

## FUG3-T3. Coefficientwise transport and delayed activation [PROVED; extends v002 T5]

For any positive integer `B`, the full word inclusion `W(y) subseteq W(By)` holds, so `P_{By}(t)-P_y(t)` has nonnegative integer coefficients.

More precisely, the new words are exactly

`{w: E(w)|By and E(w) does not divide y}`.

The first activation depth is the least length of such a word, if one exists. In particular, no new length-one label need appear even when extra longer histories occur.

**Proof.** From T1, `E(w)|y` implies `E(w)|By`. The set difference is exactly the displayed set and decomposes by word length, proving the coefficientwise claim and the depth criterion. QED.

For Fibonacci `m|n`, `B=F_n/F_m` is integral, so the theorem applies to `P_{F_n}-P_{F_m}`. It is the same label-word injection as v002 T5, refined by first-activation depth.

**Exact witness [VERIFIED-EXACT]:**

`P_{F12}(t)=1+5t+7t^2+3t^3`;

`P_{F24}(t)=1+5t+8t^2+8t^3+3t^4`.

Their difference is `t^2+5t^3+3t^4`; no new immediate labels, yet additional depth-two and deeper histories appear.

## FUG3-T4. Source-locked content-kernel test [PROVED — consequence of multiplication]

If words `w,v` are both admissible from the **same source** `x`, then `T_w(x)=T_v(x)` iff

`prod_{N in w} [(N+1)^2/N] = prod_{N in v} [(N+1)^2/N]`.

**Proof.** Each path evaluates to the source times its product of rational multipliers. Since `x>0`, equality of endpoints is equivalent to equality of products. QED.

This classifies a merger as permutation-equivalent if its label multisets agree, or different-content otherwise. The general multiplicative-kernel machinery is present in GEO-HD-1; the FUG-I task is finding exact Fibonacci realizations.

## FUG3-T5. An infinite family of Fibonacci different-content mergers [PROVED from exact witness]

For every integer `k>=1`, the Fibonacci target `F_{72k}` admits **at least three distinct different-content merger pairs** with a common scaled source.

**Exact witness:** put `s=1,730,743,096,803`, `F72=498,454,011,879,264`. The following four legal label words from `s` all end at `F72`:

`(3,8,3)`, `(1,1,1,2)`, `(1,1,2,1)`, `(1,2,1,1)`.

Their common endpoint multiplier is

`[(4^2/3)]^2 * [(9^2/8)] = 4^3*(3^2/2)=288`, and `288*s=F72`.

The first word has content `{3,3,8}` whereas each of the last three has `{1,1,1,2}`. Hence there are at least three different-content pairs. All intermediate states and divisibility checks are recorded in `results/cross_content_witnesses.csv`.

**Proof of infinitude.** Fibonacci strong divisibility yields `F72 | F_(72k)` for every `k>=1`. Put `B_k=F_(72k)/F72` (a positive integer). Each of the four legal histories from `s` lifts under the exact scale covariance to the same ordered label word from `B_k*s`, ending at `B_k*F72=F_(72k)`. Their content difference persists, supplying the same three distinct pairs for every `k`. As `F_(72k)` is strictly increasing in `k`, there are infinitely many distinct target values. QED.

**Relationship to GEO-HD.** The identity has signed content vector `(3,1,-2,-1)` over ordered label alphabet `(1,2,3,8)`, a kernel witness documented in GEO_HD_1D_v004. What FUG-I v003 specifically establishes is an explicit occurrence at Fibonacci index 72 and its infinite index-multiple family.

## FUG3-C1. Census of first 84 indices [VERIFIED-EXACT FINITE]

- All 84 target layers, all depths: 292 history records counting 84 empty words and 208 nonempty words.
- 7,056 ordered Fibonacci index pairs satisfy the complete-history gcd-meet identity (including index-duplicates of value 1).
- 307 proper index-divisibility transports: activation depth `0` in 193 cases (no additional histories), depth `1` in 108, depth `2` in 6.
- 122 repeated-source merger pairs: 119 permutation-equivalent and 3 different-content, the latter confined to `F72` within this window.
- The frozen v002 Fibonacci-to-Fibonacci endpoint census (4 pairs, 8 paths) is unchanged and rechecked.

**Numerical verification.** `scripts/run_p3.py` produces the complete word/merger/transport CSV. `scripts/verify_p3.py` independently checks threshold exponents using prime valuations, route actions, full dynamic-program counts, the complete pairwise intersections, transport differences, the witness words, independent naive square-divisor inverses on `y<=120`, and Lucas/shifted-Fibonacci controls. All tests pass in the packaged run.

## FUG3-O1. Beyond the first 84 Fibonacci indices [OPEN]

Determine all first appearances of distinct-content kernel relations within Fibonacci ancestry; quantify how many relations accumulate as index magnitude increases. The infinite family from T5 settles *existence of infinitely many such Fibonacci targets*, not their complete classification.

## FUG3-O2. Discrimination and conditional controls [OPEN]

The shifted Fibonacci `F_n+1` control has 15 different-content merger pairs in indices 1..84, while Fibonacci has 3. The controls differ in arithmetic size and divisibility. No statistical exceptionality or physical interpretation follows from these raw counts; stronger size-, factorization-, and valuation-matched null designs remain necessary.

## FUG3-O3. Beyond selected integer self-substitution [OPEN]

Whether related ancestry and meet theorems can be defined for rational non-anchor occurrences or independently chosen multilevel UNNS operators is outside the present result. Such work requires explicit grammars and cannot be inferred from T1–T5 alone.
