# FIELD-I v003 — Theorems (proofs)

Notation as in v002 (THEOREMS.md T6–T16) and SPEC.md. u/v = Δ_coll(x) in lowest terms, γ = x/Δ_coll ∈ Z_{>0}, G(x) = gcd(N_i).

## T17′  Δ_coll is reduced — proved, checked (H1.4)
Δ_coll = lcm(d_i²)/G with u = lcm(d_i²), v = G. Reduced: a prime p | G divides every N_i = d_i − 1, so p ∤ d_j for all j (else p | 1); hence p ∤ lcm(d_i²). ∎

## T17  Plateau law — proved, checked (H1.4)
D(x_{n+1}) ⊇ D(x_n) (every route continues to C(x_n); v002 G.6). While D is unchanged, Δ_coll is constant, so x_{n0+k} = (γ_0+k)·u/v, with γ_0 = x_{n0}/Δ_coll. ∎

## T18  Growth-time bound — proved, checked (H1.1, H1.2, H1.5)
Let x be realised (R ≥ 1), d ≥ 2 an integer not in D(x), K_d := v d²·⌈γ/(v d²)⌉ − γ. Then 1 ≤ K_d ≤ v d² − 1, and T(x) ≤ K_d. In particular T(x) ≤ G(x)·d_min² − 1, d_min = least integer ≥ 2 not in D(x).
Proof. 0 ≤ K_d < v d² by the ceiling. If K_d = 0 then x = γ u/v = u d² q (q ≥ 1) is an integer divisible by d², so d ∈ D(x), contradiction; hence K_d ≥ 1. Suppose no growth occurs in steps 1..K_d. Then by T17, x_{K_d} = (γ+K_d)u/v = u d² q with q = ⌈γ/(v d²)⌉, an integer divisible by d². By the integer case of v001 T1 (b = 1, d² | a), d ∈ D(x_{K_d}) while D(x_{K_d}) = D(x): contradiction. ∎
(The bound is an upper bound; actual T is smaller in most cases, H1.3.)

## T19  Collective fibre growth (credit: proposed in the v002 review; proof verified here) — proved
For every realised x_0 (R ≥ 1; the review stated R ≥ 2) and x_{n+1} = C(x_n): R(x_n) is non-decreasing, R(x_n) → ∞, and ∪_n D(x_n) is infinite.
Proof. By T18 each growth event happens within finitely many steps, so there are infinitely many events; each adds at least one element and D never shrinks. ∎ (Alternative: if D stabilised at D_*, take d ∉ D_* and use T17 to reach x = u d² q, as in T18.)
Consequence: there is no infinite constant-multiplicity plateau. No growth *rate* is claimed (data: H1.6 shows +1, +2, +3 or +6 per event in the sampled orbits).
Status: conditional on adopting C; the argument is elementary (a fixed-difference progression meets integers divisible by d²).

## T20  Integer R=3 fibres are non-rigid — proved, checked (H2.1–H2.3)
(a) D(m) is closed under divisors ≥ 2 (e | d, e² | d² | m) and under lcm (L² | m).
(b) A 3-element subset of N_{≥2} with these two closures is {p,q,pq} (p ≠ q prime) or {p,p²,p³}. Proof: let P be the primes dividing elements of D. Each p ∈ P lies in D. |P| ≥ 3 gives p,q,r,pq: ≥ 4 elements. |P| = 2 gives {p,q,pq}. |P| = 1 gives powers of p, divisor-closed with 3 elements: {p,p²,p³}.
(c) {p,q,pq}: all L = pq, and gcd(p−1,pq−1) = gcd(p−1,q−1) (pq−1 = p(q−1)+(p−1), gcd(p−1,p)=1), likewise gcd(q−1,pq−1); all three pair indices are equal. {p,p²,p³}: g = p−1 for all three pairs (gcd(p^a−1,p^b−1) = p^{gcd(a,b)}−1), L = p², p³, p³; the pairs (p,p³) and (p²,p³) have equal index.
Hence the weighted triangle has a non-trivial automorphism (a transposition or S₃). ∎

## T21  The restriction is specific to b = 1 — checked example
D(a/b) = D(a) ∩ (1 + bZ) is not divisor-closed. x = 20736/5: D = {6,16,36} (occurrences (576,5),(243,15),(112,35)), L² = 2304, 1296, 20736, g = 5 for all pairs, pair indices H = {1,9,16}: a **rigid** three-route graph. In the searched range (a ≤ 40000, b ≤ 40, 371 rational R=3 fibres) it is the only one. Classification of rational R=3 fibres: open.

## Erratum / clarification (maintenance)
The statement in v002 RESULTS.md that "only γ matters" for label-blind operations is to be read: **γ determines the admissible set** x + Δ_coll Z_{>0}; the *selection* j(x) may depend on any value-level invariant (γ, R, H, x) or none (Y = 2x). The standalone G1–G3 memo (§2) already states this; v002 files are intentionally left unedited.
