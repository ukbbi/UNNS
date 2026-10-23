# FIELD-I v004 — Theorems (proofs)

## T22  Reduction to the square-root part — proved, checked (J1.1)
Let a = s²t with s maximal (t squarefree). Then d²|a ⇔ d | s (compare p-adic valuations: 2v_p(d) ≤ v_p(a) ⇔ v_p(d) ≤ ⌊v_p(a)/2⌋). Hence
 D(a/b) = { d | s : d ≥ 2, d ≡ 1 (mod b) }, gcd(s,b)=gcd(t,b)=1, and (s,t) ↔ a is a bijection (t squarefree, arbitrary).
The fibre depends only on (s,b). Pair indices: h_ij = x·g/L² = t·H0, H0 = s²g/(bL²) ∈ Z_{>0} (L | s since L = lcm of divisors of s; b | g). Rigidity depends only on D (the ratios g/L²).
Corollary (squarefree scaling; observation of the v003 review, now formal): for squarefree m with gcd(m,ab)=1, D(ma/b) = D(a/b) and all indices are multiplied by m. In particular x=20736/5 (s=144, t=1) yields 145152/5, 228096/5, 269568/5, … (t = 7, 11, 13, …), all with D = {6,16,36} and indices (1,9,16)·t.
Primitive reduction: if D=D(s,b) and λ = lcm(D), then D(λ,b) = D (divisors of λ are divisors of s and contain D). So every fibre has a primitive representative (λ,b).

## T23  Closure lemmas — proved, checked (J1.4)
D = {d | s, d≥2, d≡1 mod b}. (Q) d | e in D ⇒ e/d is 1 or in D (e/d | s and e/d ≡ e·d⁻¹ ≡ 1). (G) d,e ∈ D with c = gcd(d,e) ≡ 1 (mod b) ⇒ lcm(d,e) = de/c ≡ 1 is in D, and c is 1 or in D. Conversely c ≢ 1 ⇒ lcm ≢ 1 and c ∉ D.

## T24  Shape theorem for three-route fibres (b ≥ 2) — proved, checked (J1.5, J1.6, J1.8)
Let D = {d1,d2,d3}. Up to relabelling exactly one of:
1. **Chain** d1|d2|d3: then D = {q,q²,q³}; non-rigid.
2. **Lambda** (d1|d3, d2|d3, d1∤d2, d2∤d1): then d3 = d1d2; non-rigid.
3. **V** (d1|d2, d1|d3, d2,d3 incomparable): impossible.
4. **One comparable pair**: D = {q,q²,e} with e incomparable to q and q² (e∤q², q∤e); **always rigid**.
5. **Antichain**: no divisibility; every pair has gcd ≥ 2 and ≢ 1 (mod b); rigid or non-rigid according to whether the three weights are distinct (both occur).
Proof. Poset on 3 elements has 0,1,2 or 3 comparable pairs; with 2 comparable pairs it is V or Lambda.
(1) Q: d3/d1, d2/d1, d3/d2 ∈ {1}∪D. d2/d1 < d2 ⇒ d2/d1 = d1 ⇒ d2 = d1². d3/d2 < d3, in D ⇒ ∈ {d1,d2}; d3/d2 = d2 ⇒ d3/d1 = d1³ ∉ D, so d3 = d1³. Weights: g = q−1 for all three pairs (gcd(q^a−1,q^c−1) = q^{gcd(a,c)}−1), L = q², q³, q³ ⇒ w13 = w23.
(2) Q: d3/d1 and d3/d2 lie in D and are smaller than d3, and d1,d2 are not divisors of each other, so both lie in {d1,d2}. If d3/d1 = d1 then d3 = d1² and d3/d2 ∈ {d1,d2} gives d2 = d1 or d2² = d1², both excluded; hence d3/d1 = d2, i.e. d3 = d1d2. Weights: L13 = L23 = d3, g13 = gcd(d1−1, d1d2−1) = gcd(d1−1,d2−1) (d1d2−1 = d2(d1−1)+(d2−1)) and likewise g23 = gcd(d2−1,d1−1). So w13 = w23.
(3) d2 = d1m2, d3 = d1m3 with m2,m3 ≥ 2; m_i ≡ 1 (mod b) by Q and divides s, so m_i ∈ D; m2 | d2 and m2 < d2 ⇒ m2 = d1 (m2 = d3 would make d3 | d2), likewise m3 = d1, so d2 = d3 = d1², contradiction.
(4) Comparable pair d_i | d_j, third e. Q gives d_j/d_i ∈ D, smaller than d_j, not e (else e | d_j): so d_j = d_i² = q². Weights: w12 = (q−1)/q⁴ (pair q,q²), w1e = g1/lcm(q,e)², w2e = g2/lcm(q²,e)², g1 = gcd(q−1,e−1), g2 = gcd(q²−1,e−1).
 – w12 = w1e: put lcm(q,e) = qm, then g1 = (q−1)m²/q²; gcd(q²,q−1)=1 ⇒ q | m, m = qm″, g1 = (q−1)m″² ≤ q−1 ⇒ m″ = 1 ⇒ lcm(q,e) = q² ⇒ e | q², contradiction.
 – w12 = w2e: put lcm(q²,e) = q²m′ (m′ = e/gcd(q²,e)); then g2 = (q−1)m′²; g2 | q²−1 ⇒ m′² | q+1; m′ | g2 | e−1 and m′ | e ⇒ m′ = 1 ⇒ e | q², contradiction.
 – w1e = w2e: lcm(q²,e) = r·lcm(q,e) with r | q; equality gives g2 = g1r² ⇒ r² | q²−1, r | q ⇒ r = 1 ⇒ q² | … ⇒ v_p(e) ≥ 2v_p(q) for every p | q ⇒ q | e, contradiction.
(5) Lemma G: a pair with gcd ≡ 1 would force lcm ∈ D, hence equal to the third element, giving divisibility; a coprime pair has gcd = 1 ≡ 1. ∎
(b = 1: Lemma G applies to every pair, so antichain and one-pair shapes cannot occur; this is v003 T20, checked J1.9.)

## T25  Infinite rigid families — proved
(a) Scaled: for any rigid primitive (s,b) and any squarefree t with gcd(t,b)=1, x = s²t/b has the same D and is rigid: infinitely many values per configuration (T22).
(b) Primitive (distinct s): b = 3, s = 22r, r prime, r ≡ 23 (mod 63). Divisors of s that are ≥ 2 reduce mod 3 to 2 (2, 11, r, 22r) or 1 (22, 2r, 11r) since r ≡ 2 (mod 3); so D = {22, 2r, 11r}. All pair lcm's equal 22r. gcd(21,2r−1) = 3 (r ≡ 2 mod 21 ⇒ 2r−1 ≡ 3), gcd(21,11r−1) = 21 (11r−1 ≡ 21 ≡ 0), gcd(2r−1,11r−1) = gcd(2r−1,9) = 9 (2(11r−1) = 11(2r−1)+9; r ≡ 5 mod 9). The weights 3,21,9 over (22r)² are distinct, so the fibre is rigid (an antichain). Infinitely many such primes r by Dirichlet (gcd(23,63) = 1). First: r = 23, x = 506²/3 type value with s = 506. ∎
(c) Statement for v003: the infinite family asked for is T25(a); T25(b) shows rigidity is not only a scaling effect.

## T26  Exact global minimum of the growth-time bound — proved, checked (J3.1)
For d ∉ D(x), K_d ≥ 1 and T(x) ≤ K_d (v003 T18) hence T(x) ≤ min over all such d. With k0 = K_{d_min}, a d improving k0 needs v d² ≤ vd²·⌈γ/(vd²)⌉ < γ + k0, i.e. d² < (γ+k0)/v. So the minimum over all d ∉ D is computed by finite search d ≤ ⌊√((γ+k0)/v)⌋ (+1 for safety in the code).

## T27  Provable lower bound for the growth of R — proved, checked (J2.1)
(a) G(x_n) = gcd(N_i over D(x_n)) is non-increasing along C-orbits (D grows ⇒ gcd over a larger set divides gcd over a smaller set). (b) d_min ≤ R+2 (R+1 consecutive integers 2..R+2 cannot all lie in a set of size R). Hence with v0 = G(x_0), T(x) ≤ v0 (R(x)+2)² − 1 whenever R(x) = R. Let n(r) be the first step with R(x_n) ≥ r: if R(x_{n(r)}) = r exactly, n(r+1) ≤ n(r) + v0(r+2)² − 1; otherwise n(r+1) = n(r). So n(R0+m) ≤ Σ_{r=R0}^{R0+m−1} (v0 (r+2)² − 1), i.e. R(x_n) ≳ (3n/v0)^{1/3}. This is a proved but weak bound; sampled orbits grow much faster (open).

## T28  Monotone fibre growth is specific to the collective branch — proved (example), checked (J4.1, J4.2)
Along C-orbits D(x_n) ⊆ D(x_{n+1}). Along a route-aware orbit x + kΔ_rs this fails: x = 36, pair (2,3), Δ = 36: R(36(k+1)) = 3,3,3,5,3,3,3,5 (R drops 5 → 3 at x = 180). In the corpus R decreases somewhere along the first 10 steps in 118 of 118 pair orbits tested (data).

## Open
Arithmetic criterion for antichain rigidity (weights g_ij/L_ij²); full list of primitive configurations; true growth rate of R(x_n); whether every d ≥ 2 enters D(x_n); finer structural comparison of branches (J4).
