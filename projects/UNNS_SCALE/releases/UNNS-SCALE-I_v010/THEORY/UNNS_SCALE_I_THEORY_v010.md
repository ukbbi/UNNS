# UNNS-SCALE-I v010 — Height-Constrained Arithmetic Geometry

Labels: PROVED / CERTIFIED (exact finite computation, independently re-verified) / EXPERIMENTAL / OPEN. B = 10⁶, graph = SELECT-II (edges {kN, k(N+1)²}), window W = [1, 10¹²].
Central question (from the v009 review): does the four-step theorem of v005 (max_{1≤n≤999999} d(10⁶n, 10⁶(n+1)) = 4, ambient graph) survive when **every vertex of the route must stay in [1,10¹²]**?

## 1. Definitions
- Ceiling-C graph G_C: induced subgraph of SELECT-II on [1,C]. d_C(x,y) = distance in G_C (∞ if disconnected).
- H_ℓ(x,y) = min over routes of length ≤ ℓ of the maximum vertex (minimal required ceiling; ∞ if none). H_ℓ ≤ C ⇔ d_C ≤ ℓ.
- Window pair P_n = (10⁶n, 10⁶(n+1)), 1 ≤ n ≤ 999999 (both endpoints in W). Three quantities: numerical separation 10⁶; ambient distance d(P_n) ≤ 4 (v005); required height H₄(P_n) and window distance d_W(P_n)=d_{10¹²}(P_n).
- **Test lemma (PROVED).** d_C(x,y) ≤ 4 ⇔ the radius-2 balls of x and y *inside G_C* intersect (a path of length ≤4 has a vertex within 2 steps of both ends along the path, all inside [1,C]). So disjoint restricted balls certify d_C > 4.
- **Label bound (PROVED).** Every edge label met in G_C satisfies N ≤ √C (a forward label N | y with y(N+1)²/N ≤ C has N ≤ y and N ≤ C/y; a backward step has q ≤ √y). For C=10¹² all labels are ≤ 10⁶, so a sieve to √C+2 factors every needed N, N+1, q, q−1 and the restricted balls are exactly computable.

## 2. Main theorem (CERTIFIED)
**Theorem W.** For B = 10⁶ and C = 10¹²: of the 999,999 pairs P_n,
- **2,997** have d_W ≤ 4 (a route of ≤4 steps with all vertices ≤ 10¹²; includes every n ≤ 682);
- **997,002 (99.70 %)** have d_W ≥ 5 — their restricted radius-2 balls are disjoint — i.e. **every route of at most four steps must leave the trillion window**. The first such pair is n = 683.
Per block of 10⁴ values of n the number of in-window four-step pairs is 2609, 105, 39, 27, 18, 18, 7, 8, 11, 5, … (decreasing). Method: `ball.cpp` (exact C++), verified by an independent Python implementation (`rball.py`, Pollard-rho/Miller-Rabin `exact_lib`) on 609 pairs (full mode; 119 in quick mode) including exhaustive n<400, by a fresh g++ rebuild on blocks, and edge-checked routes for every sampled passing pair.
**Consequence.** The v005 four-step theorem is genuinely an *ambient* statement: for 99.70 % of window pairs the four-step connection uses numerical regions beyond 10¹² (largest vertices reach 10¹⁹–10²² in v005 data). The induced trillion-window metric is **not** the ambient metric. This sharpens the v005 caveat from a remark into a quantified theorem, and answers the v009 question: global-domain excursion necessity is established (finite, exact).

## 3. Trade-off between route length and height
- **n = 5 (review example, CERTIFIED):** H₄ = 6,230,016 (ceiling 6,230,015 ⇒ disjoint balls of 225 / 292 vertices); the shortest route has 3 steps but height 732,050,000. Longer route, lower height.
- **Window distances (EXACT where stated):** n = 683, 5039: d_W = 5 (radius-3/radius-2 balls meet; radius 2/2 disjoint). Sample of 62 n (stratified, log-spaced + primes), radius 5 per side: d_W = 3–4 for n ≲ 10³ (5 at n=683); 4–6 for 10³ ≲ n < 10⁴; 4–8 for 10⁴ ≲ n < 10⁵; 7–10 for sampled n ≥ 10⁵ where decided, and **> 10** (radius-5 balls disjoint, 14 of 62 sampled n, all ≥ 226103) otherwise. So the window-induced distance of the same pair grows from 4 to at least 11 while the ambient distance stays ≤ 4. Whether G_W is connected between these endpoints is OPEN.
- **Minimal ceilings (EXPERIMENTAL, 2005-n sample, every 499th n; ceiling search capped at 10¹⁵):** H₄ ≤ 10¹² for only 6 sampled n; for n in [10⁴,10⁵) 61 % have H₄ ≤ 10¹⁵ (0 ≤ 10¹²); for n in [10⁵,10⁶) only 2.7 % have H₄ ≤ 10¹⁵ and the rest satisfy H₄ > 10¹⁵ (certified lower bound). Among sampled n ≥ 1000 with H₄ ≤ 10¹⁵, log(H₄/(10⁶(n+1)))/log n has median 0.75 and maximum 1.08 — consistent with excursion ratio growing like a power of n, but the sample is right-censored, so this is **not** a theorem. Unbounded growth of the minimal excursion ratio: OPEN (v009 gave the family B(n+2)² as upper bound only).
- **Endpoint-domain data of v009 (197/278 forced outside [1,B(n+1)]) is a different domain from this window result; both are finite exact statements.**

## 4. What v010 does not claim
No value of d_W above 10; no proof that G_W is connected or of its diameter; no proof of H₄ growth; D_{10⁶} = sup over all n remains {4,5,6}. Only pairs (10⁶n, 10⁶(n+1)) with B = 10⁶ and C = 10¹² were studied. Gate 4 (computational benefit) stays deferred: Theorem W implies that replacing the trillion window by its induced graph does *not* preserve four-step routes.
