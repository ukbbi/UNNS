# UNNS-SCALE-I v009 — Constant-Ratio Covering and Excursion Geometry

Evidence labels: PROVED / CERTIFIED (exact computation, re-verified) / EXPERIMENTAL / OPEN. Finite maxima are lower bounds, not suprema.

## 0. Corrections to v008 (ERRATUM_v008.md)
E1 (PROVED, CERTIFIED): a constant-ratio shape (v′,w′,c,d,P,Q) routes n iff v′|n, w′|n+1, **P | cn/v′+1 and P | d(n+1)/w′+1**, q,r≥2. Both congruences are required; together (CRT, gcd(v′,w′)=1) they give one residue class mod lcm(v′P,w′P)=P·v′·w′ for n ≥ n0. Example: (1,2,1,1) at n=3 fails the second congruence.
E2 (PROVED): converse of Theorem L′ needs B | Q²aN. Counterexample N=M=1,(P,Q)=(2,3),(P′,Q′)=(1,2),a=600000,a′=1600000: S1, S2 hold, n=27/5.

## 1. Covering problem
Each corrected shape is (for n≥n0) one residue class. A finite family F therefore covers all n ≥ max n0 iff its classes form a covering system; otherwise the complement is periodic with positive density. `classes.py` implements shape→class (CERTIFIED equal to the route test: 0 mismatches on 2≤n<6000 for K=8, plus random shape tests).
`cover.py` is an exact best-first refinement of the residue tree: a node is closed when contained in a class; otherwise it is split by a prime of m/gcd(m,M). The uncovered measure after any budget is a rigorous upper bound on the density of integers outside the union; a finished run with no dead node would be a covering certificate.
Result (CERTIFIED computation, no certificate): K=4 (1372 classes): uncovered ≤ 2.0×10⁻³; K=8 (4369): ≤ 3.0×10⁻⁴; K=12 (8114, n0≤450): ≤ 8.1×10⁻⁶. Every run stopped at the 1.5M-node frontier cap; no run finished and no provably uncovered class (dead node) was found. So: the density of n **not** covered by constant-ratio shapes of size ≤K shrinks fast with K, but **no finite covering is established and none is refuted**. OPEN: whether finitely many shapes cover all n; D_{10^6}∈{4,5,6} remains OPEN (D≥4 window theorem of v005 covers n<10^6 only).
Honest consequence: this is not a further large coverage table; it is a density-bound pipeline whose output is a rigorous but non-terminating certificate attempt. A real proof must either use infinite parameter families (growing P,Q) or show an obstruction class; neither is provided here.

## 2. Arithmetic wormhole geometry (precise definitions)
Graph G_B: vertices ℕ>0, edges {kN,k(N+1)²}; "Arithmetic Wormhole" is an evocative name for a property of this graph, not a physical wormhole. Precise subject: **height-constrained geodesics / excursion necessity**.
- Route (path) π=(x₀,…,x_ℓ): simple path; length ℓ; height h(π)=max xᵢ.
- Domain L=max(x₀,x_ℓ) (e.g. endpoints Bn, B(n+1), L=B(n+1)); excursion ratio ρ(π)=h(π)/L; π is *inside* if h(π)≤L.
- Route cost: (ℓ, h). Minimal height with length budget ℓ₀: h*(x,y;ℓ₀)=min{h(π): length ≤ ℓ₀}; h_geo = min over shortest paths only.
- Wormhole candidate: endpoints ≤L, d(x,y)≤4, a short path has h ≫ L (we report ρ). Necessary wormhole at (L,ℓ₀): **every** route of length ≤ ℓ₀ has height > L, i.e. h*(x,y;ℓ₀) > L.
- Important distinction (EXPERIMENTAL, CERTIFIED data): h_geo ≠ h*(·;4). For 90 of 268 tested n a longer-than-shortest route (length 4 while d=3, or 3 while d=2) has strictly lower height than every shortest route.

### Data (B=10⁶, exact, complete neighbourhoods; paths re-verified independently)
- Shortest paths, n=2..269 and 700..768: distances d∈{2,3,4}; the minimal geodesic height exceeds B(n+1) for most n.
- All simple routes of length ≤4, n=2..279: 197 of the 278 n tested (n=2..279) are **necessary wormholes at (L=B(n+1), ℓ₀=4)**; 81 are not (a route of height exactly B(n+1) exists). Maximal observed excursion ratio 524 (n=262).
- Many primes ≥200 (e.g. 211, 223, 227, 229, 233, 241, 257, 263, 269, 701…) show geodesic min-height exactly B(n+1)² (ρ=n+1): consistent with the Absorption Lemma (a prime ℓ∥n must be absorbed by a label ≥ℓ−1, forcing a vertex ≳Bp² when absorbed in the first forward label). Counter-evidence to a uniform law: n=79 and 239 are inside/low (ρ=1, 7.2), n=727,739,751 have ρ≈2n.
- Reviewer's family (PROVED by explicit path, CERTIFIED legal for k≤40): n=3k, 4|B: Bn → 3B(k+1)² → (3B/4)(2k+1) → B(3k+2)² → B(n+1); height B(n+2)², ρ=(n+2)²/(n+1)→∞. This is an **upper bound** on h*, hence it proves only that wormhole *candidates* of unbounded ratio exist, not necessity.
- Partial necessity lemma (PROVED, for (+-|+-) routes, prime n=p∤B): if p|N then x₁=Bp(N+1)²/N>Bp·N≥Bp²; if p|M+1 then y₁≥B(p+1)p. The remaining case p|r−1 is not controlled, and non-(+-|+-) route types are not covered, so **necessity for primes is OPEN** (EXPERIMENTAL support only).

## 3. What v009 does not claim
No covering certificate; no proof that D_{10^6}=4; no proof of excursion necessity as n→∞; no statement about trillion-scale computational benefit (Gate 4 remains deferred). v001–v008 are untouched (hash-checked).
