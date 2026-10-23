# FIELD-I v009 — THEOREMS (T49–T58)

Status tags: **PROVED** (proof given here or in an earlier release, computer checks only confirm), **DATA** (computation, exact but
finite), **OPEN**. A computer certificate is called a *certificate* only when it is a finite-state closure argument that is itself
proved (T51); a bounded enumeration is never called a proof.

Notation (unchanged from v005–v008). For x = a/b reduced, D(x) = {d ≥ 2 : d² | a, d ≡ 1 (mod b)}, R = |D|, G = gcd{d−1}, L = lcm D,
collective map C(x) = x + lcm(d²)/G = x + L²/G. A **persistent** orbit is one with G(x_n) = g constant (g > 1). Then every d ∈ D is ≡ 1
(mod g), so gcd(L,g) = 1, and (v008 T44) x = γ L²/g with γ = g x / L² ∈ ℕ. Write L = ∏ p^{e_p}. v005: D(x_n) ⊆ D(x_{n+1}), G_{n+1} | G_n.
v008 T47: in a persistent orbit γ_n ≤ 2M eventually (M = 4g if L odd, g if L even). A **carry** is a step with L_{n+1} ≠ L_n; r = L_{n+1}/L_n;
a **plateau** is a run of steps with r = 1 (γ → γ+1, L fixed).

---------------------------------------------------------------------------------------------------------------------------------

## T49 — The one-step law (PROVED)

Let x = γL²/g be a persistent state, w = γ+1, h = gcd(g,w), b' = g/h, and
σ' = L · ∏_p p^{⌊v_p(w/h)/2⌋}. Then x' = C(x) = wL²/g and

  **D(x') = { d | σ' : d ≥ 2, d ≡ 1 (mod b') }.**

x' is persistent (G(x') = g) **iff every d in this set is ≡ 1 (mod g)**. In that case L' = lcm D(x') is a multiple of L, r = L'/L is an
integer with r | ∏p^{⌊v_p(w/h)/2⌋}, r² | w, and **γ' = w / r²**.

*Proof.* x' = wL²/g. Since gcd(L,g) = 1 the reduced form has numerator (w/h)L² and denominator b' = g/h. d² | (w/h)L² ⇔ for every p,
2v_p(d) ≤ v_p(w/h) + 2e_p ⇔ v_p(d) ≤ e_p + ⌊v_p(w/h)/2⌋ ⇔ d | σ'. If all d ≡ 1 (mod g) then g | G(x'); G(x') | G(x) = g by
D(x) ⊆ D(x'); so G(x') = g. Conversely persistence needs g | d−1 for all d ∈ D(x'). L | L' from D ⊆ D'; L' | σ' gives r | ∏p^{⌊v_p(w/h)/2⌋};
γ' = g x'/L'² = wL²/L'² = w/r² and is an integer by v008 T44. QED

*Why this is the right object.* The only information about the exponents that enters is the set of residues {p^k mod g}, so the law can
be run on residues (the "machine" of field9.py) and compared with raw iteration of C (tests A1–A3).

## T50 — The eight-step theorem, G = 11 (PROVED)

Let S_k = 2²·3^{3+k}·5⁴ and x = t·S_k²/11. Then for every k ≥ 0:
(i) L(tS_k²/11) = S_k for t = 1,…,8, and L(9S_k²/11) = 3S_k = S_{k+1}; G = 11 throughout;
(ii) the orbit of C from x_0 = 67500²/11 is x_{8k+j} = (j+1)S_k²/11 (j = 0,…,7), hence **x_{n+8} = 9 x_n** (γ-cycle 1→2→…→8→1, one 3-carry per 8 steps);
(iii) R(x_{8k+j}) = 2(4+k)−1 = 7+2k, so **R(x_{n+8}) = R(x_n) + 2**;
(iv) x_{n+3}/x_n takes the eight values 3/2, 8/5, 7/4, 2, 5/2, 18/7, 27/8, 4 — v008 M4a is false (see T58).

*Proof.* g = 11 is prime and w = γ+1 ≤ 9 < 11, so h = 1, b' = 11. Residues mod 11: 3 has order 5, H = ⟨3⟩ = {1,3,4,5,9} (the quadratic
residues); 2 ∉ H, 4 = 3⁴ ∈ H, 8 = 2·4 ∉ H, 5 ≡ 3³, 12 ≡ 1. By T49 the fibre of w S_k²/11 is {d | S_k·sqrtpart(w) : d ≡ 1 (mod 11)}.
*(L is attained.)* Write d = 2^a 3^b 5^c; mod 11 its residue is 2^a·3^{b+3c} (5 ≡ 3³). Since 2 ∉ H, 4 ∈ H (4 ≡ 3⁴), the residue lies in H only for a ∈ {0,2}, and
d ≡ 1 iff 5 | b+3c (a = 0) or 5 | 4+b+3c (a = 2). For b = 3+k, c ≡ −(3+k)·3⁻¹ (mod 5) has a solution c ∈ {0,…,4}, so v₃ = 3+k is attained;
5⁴·3^i = 3^{12+i} ≡ 1 needs i ≡ 3 (mod 5): i = 3 ≤ 3+k, so v₅ = 4 is attained; a = 2 with suitable (b, c) attains v₂ = 2. These equations are periodic in k mod 5
(also checked for k < 400 in N1.1), so L(S_k²/11) = S_k; for t ∈ {1,2,3,5,6,7}, σ' = S_k so L cannot grow.
*(No absorption for t = 1..8.)* For t ∈ {4, 8}, σ' = 2S_k has v₂ = 3; a d with v₂(d) = 3 would need 2³·3^i·5^c ≡ 1, i.e. 8 ∈ H — false.
*(3-carry at t = 9.)* σ' = 3S_k has v₃ = 4+k; d = 3^{4+k}5^c with 5 | 4+k+3c is solvable (c ∈ {0..4}), so v₃(L') = 4+k, L' = 3S_k and γ' = 9/9 = 1.
*(G = 11.)* 12 = 2²·3 | S_k and 12 ≡ 1, 12−1 = 11, so G | 11; every d ≡ 1 (mod 11), so G = 11.
*(Counts.)* d = 2^a 3^b 5^c ≡ 1 forces a ∈ {0,2}; for each a and each c exactly one residue class of b mod 5 works, and the classes for c = 0..4 are distinct,
so Σ_c #{b ≤ B : b ≡ b_c} = B+1 with B = 3+k. Hence R = 2(4+k) − 1 (the −1 removes d = 1). (iv) is exact arithmetic on the closed form. QED
Test: N1.0–N1.7 (160+ direct orbit steps with exact rationals).

## T51 — Finite-state closure; every persistent orbit scales exactly (PROVED)

Fix g. For a prime p ∤ g let o_p = ord_g(p). For e ≥ 0 define the **class** c_p(e) = e if e ≤ o_p−2, and c_p(e) = (o_p−1) + ((e−(o_p−1)) mod o_p) if e ≥ o_p−1.
The class of a persistent state is (γ, (c_p(e_p))_p) (primes with e_p = 0 contribute class 0).

**Class lemma.** The class of C(x), the carry vector Δ_p = e'_p − e_p, and the persistence of C(x) are functions of the class of x.
*Proof.* By T49 the data of the step are w, h, b', s' = ∏p^{⌊v_p(w/h)/2⌋} (functions of γ) and, for each p, the residue set {p^k mod g : 0 ≤ k ≤ e_p + s'_p}.
If e_p ≥ o_p−1 this set is all of ⟨p⟩ whatever e_p is; if e_p < o_p−1 it depends on e_p exactly. The new exponent of p is e_p + Δ_p with
Δ_p = max{ j ∈ [0, s'_p] : p^{e_p+j}·a ≡ 1 (mod b') for some a in the residue set of a divisor of σ'/p-part } (j = 0 is always attained since D ⊆ D'),
and this depends on e_p only through e_p mod o_p (for e_p ≥ o_p−1) or exactly. The persistence test (all d ≡ 1 (mod b') are ≡ 1 (mod g)) is a statement about the same residue sets.
Finally c_p(e+Δ) depends only on c_p(e) and Δ. QED

**Closure principle.** If two states n₁ < n₂ of a persistent orbit have the same class, then for all n ≥ n₁: γ_{n+P} = γ_n (P = n₂ − n₁), the carries repeat, and
**x_{n+P} = ρ² x_n with ρ = L_{n₂}/L_{n₁} ∈ ℕ**, forever. (Induction on n using the class lemma; ρ = ∏p^{(sum of Δ_p over one period)}.)

**Theorem (exact scaling of every persistent orbit).** Every persistent orbit is eventually class-periodic, hence eventually x_{n+P} = ρ²x_n with ρ ≥ 2.
*Proof.* By v008 T47, γ_n ≤ 2M eventually. A prime that is not already in L can enter only through s', i.e. only if p² | w for some w ≤ 2M+1: a finite set F.
So after a finite time the class lies in a finite set; a deterministic map on a finite set is eventually periodic. ρ = 1 is impossible because x_{n+1} > x_n. QED

**Corollary (every orbit).** G_{n+1} | G_n, so G_n is eventually constant = G_∞. If G_∞ = 1, v005 T32 gives x_{n+3} = 4x_n eventually. If G_∞ > 1 the orbit is
eventually persistent and the Theorem applies. **So every orbit of C eventually satisfies an exact law x_{n+P} = ρ²x_n (P ≥ 1, ρ ∈ ℕ, ρ ≥ 2).** This closes the v008 OPEN
"does every orbit enter some exact scaling regime" — what remains open is *which* (P, ρ) occur for a given seed and which g > 1 can occur (see T52, T57).

*Certificates.* run_cycle() in field9.py iterates the residue machine until the class repeats; by the Closure principle that is a proof of eternal periodicity, not an enumeration.
The class period may be much larger than the γ-period (the exponent of a carrying prime must run through o_p residues): for q = 7, g = 367 the class period is 2928 = 61·48.

## T52 — The window theorem: which carries are possible (PROVED)

In a persistent orbit with modulus g:
(a) **g odd ⇒ 2 | L_n for all n.** G = g odd needs some d with d−1 odd, i.e. an even d ∈ D, so 2 | L.
(b) **g odd ⇒ g ∤ γ_n + 1 for all n.** If g | w then h = g, b' = 1 and x' = (w/g)L² is an integer; D(x') = {all divisors ≥ 2 of σ'} ∋ 2 (by (a)), and 2 ≢ 1 (mod g), so x' is not persistent (T49).
   (b') g even (g ≥ 4) ⇒ 4g ∤ γ_n + 1: then 2 | sqrtpart(w/g), so 2 | σ', b' = 1 and again d = 2 ∈ D(x'), 2 ≢ 1 (mod g).
(c) **Every complete carry (below) has M² < g for odd g** (and M² ≤ 4g for even g): a carry from γ = 1 passes through w = 2,…,M², which would contain w = g (or 4g).
   Also gcd(M,g) = 1 because M | d ≡ 1 (mod g).
Consequences: a q-carry needs g > q² (g odd); there are only finitely many carry sizes for a given g (M < √g); 5-carries do not exist for odd g ≤ 25, 7-carries not for odd g ≤ 49. Tests W1, W2, Q4.

## T53 — The absorption criterion (PROVED)

State (g, E) persistent, step with w = γ+1. For d ≥ 2 with d ≡ 1 (mod g) put j_p(d) = max(0, v_p(d) − e_p) and **M(d) = ∏p^{j_p(d)}** (the "new part" of d).
Then d is available at the step ⇔ M(d)² | w (given gcd(M(d), g) = 1). Consequently
 **L' = L·r with r = lcm{ M(d) : d ≡ 1 (mod g), d ≥ 2, M(d)² | w }.**
*Proof.* d | σ' ⇔ for all p: j_p(d) ≤ ⌊v_p(w/h)/2⌋ ⇔ M(d)² | w/h ⇔ M(d)² | w (h | g is coprime to M(d) because gcd(d,g) = 1). Persistence supplies d ≡ 1 (mod b') ⇒ d ≡ 1 (mod g), so
availability does not depend on h. The exponent of p in L' is max(e_p, max_d v_p(d)) = e_p + max_d j_p(d). QED
**Square factors that change L:** p^{2j} | w changes the exponent of p iff there is d ≡ 1 (mod g) with v_p(d) = e_p + j' (1 ≤ j' ≤ j) and other primes at exponents ≤ e_q (or also new, if their squares divide w).
In residue form: ∃ k ∈ (e_p, e_p+j], ∃ a ∈ A_{−p}: p^k a ≡ 1 (mod g), where A_{−p} is the set of residues of divisors of L/p^{e_p} together with the new q-parts allowed by w.
**Types.** *No absorption*: no available d with M(d) > 1 (r = 1, γ' = γ+1). *Partial*: r > 1 and r² < w (γ' = w/r² ≥ 2). *Complete*: r² = w (γ' = 1).
**Complete ⇒ gcd(g,w) = 1:** r² ≤ s'² ≤ w/h, so w = r² ≤ w/h forces h = 1.

## T54 — Carry completeness: partial absorption is a finite transient (PROVED)

Let a carry occur at w from a plateau that started at γ_s (the γ right after the previous carry, or the initial γ). Then
 **γ' ≤ γ_s/4 + 1,** and if γ_s = 1 then **w = M² = r² and γ' = 1 (complete).**
Hence in a persistent orbit γ_s strictly decreases at every carry as long as γ_s ≥ 2, so **after finitely many carries γ = 1, and from then on every carry is complete: w = M², cycle length M² − 1.**
*Proof.* L is constant along the plateau, so by T53 availability of d depends only on M(d)² | w. Let d be available at the carry step. If w − M(d)² ≥ γ_s + 1 then d was already available at
the earlier plateau step w'' = w − M(d)² (M(d)² | w''), i.e. the plateau would have been interrupted — contradiction. Thus w ≤ γ_s + M(d)². Since r is a multiple of M(d) and r ≥ 2:
γ' = w/r² ≤ (γ_s + M(d)²)/r² ≤ γ_s/4 + 1. If γ_s = 1: M² | w and M² ≤ w ≤ 1 + M² give w = M² (as 2M² > M² + 1), so r² | M² and r ≥ M give r = M, γ' = 1. QED
Plateaus are finite and carries infinite in a persistent orbit (T47). Test C1 (many thousand machine steps; bound violated 0 times; no partial carry after γ has been 1).
Partial carries do occur in transients (test C2 prints examples). This is the structural reason why the v008 "cycle 1,2,3" was a special case: the γ-cycle is 1,…,M²−1 with M the **minimal available carry**.

## T55 — Eventual carries are prime powers (PROVED)

In the eventually periodic regime (T51) every carry M is a prime power p^j.
*Proof.* A carry type that recurs infinitely often raises each of its primes' exponents infinitely often, so each prime p | M has e_p ≥ o_p − 1 (saturated) from some time on.
Suppose M has two distinct primes and let d be available with M(d) = M (so w = M², by T54). Take a prime q | M with v_q(M) = j. Choose i ∈ [0, o_q − 1] with i ≡ e_q + j (mod o_q); since e_q ≥ o_q − 1 we have i ≤ e_q.
Then d' = d·q^{i − e_q − j} is an integer, d' ≡ d ≡ 1 (mod g), d' ≥ 2 (it still contains the other prime of M), and M(d') = M/q^j < M with M(d')² | M² = w.
So a smaller carry was already available at w' = M(d')² < M², contradicting that the plateau reached w = M². QED
Test P1: every carry of every eventual cycle found changes exactly one prime exponent.
So the "carry alphabet" is {p^j}; composite carries (e.g. M = 6, w = 36) can occur only in the transient, while some participating prime is unsaturated.

## T56 — The decoupled odometer law (PROVED)

In the eventual regime let A be the set of active primes (unbounded exponent; all saturated); the others are inert (constant exponent). For p ∈ A define
 **Abs_p = { k mod o_p : ∃ a ∈ 𝒜_{−p}, p^k a ≡ 1 (mod g) }**, where 𝒜_{−p} is the set of residues of divisors of ∏_{q ≠ p} q^{e_q} (⟨q⟩ for active q, a fixed finite set for inert q).
𝒜_{−p} does not change in time, hence Abs_p is a fixed subset of Z/o_p. At every state with γ = 1 the next carry is p^{j_p} for the active p minimising p^{j_p}, where
 **j_p = min{ j ≥ 1 : (e_p + j) mod o_p ∈ Abs_p }.**
So the orbit is a system of independent counters e_p mod o_p. In particular, for a single active prime p the carry exponents are the successive gaps of Abs_p around Z/o_p, the γ-cycle lengths are p^{2j}−1,
and P = Σ(p^{2j_i} − 1), ρ = p^{Σ j_i} over one lap. *Proof.* By T54 the next carry is the minimal available M; by T55 it is a prime power; p^j is available iff p^{e_p+j} a ≡ 1 for some a ∈ 𝒜_{−p} (no other prime has a new part). QED
This explains every "nonstandard" cycle found: e.g. g = 31, p = 2 (o = 5): the carries are 2², 2², 2¹ (w = 16, 16, 4), P = 15+15+3 = 33, ρ = 2⁵ = 32; g = 59: mostly 3-carries (w = 9) with occasional 4-carries (w = 16).
There is no *other* kind of cycle in a persistent orbit: every eventual cycle is a word in prime-power carries generated by finitely many independent odometers. Tests O1, P2 (predicted words equal the machine's) exercise **single-active-prime** cycles only; no eventual cycle with two active primes was found, so the multi-prime clause is proved but untested (**OPEN O9.2**: exhibit one).

## T57 — The general q-carry theorem (PROVED, hypotheses finite-checkable)

Let q be an odd prime and g an odd prime with g > q². Put o = ord_g(q), H = ⟨q⟩ ⊂ (Z/g)*. Hypotheses:
(Q1) 2 ∉ H; let e₂ = min{e ≥ 1 : 2^e ∈ H}, and K = ⟨2⟩·H.
(Q2) for every odd M with 3 ≤ M ≤ q−1: M mod g ∉ K; for every even M with 2 ≤ M ≤ q−1: M mod g ∉ H.
(Q3) u is a prime with u ≡ q (mod g), u > q; seed exponents E₀ = {u: o−1, q: ≥1, 2: e₂}.
(Q4) G(x₀) = g for x₀ = L₀²/g, L₀ = u^{o−1} q^{e_q} 2^{e₂} (exact, finite divisor check).
Then the orbit of x₀ is persistent forever and
 (i) γ_n = (n mod (q²−1)) + 1, L_{n+q²−1} = q·L_n, hence **x_{n+q²−1} = q² x_n**;
 (ii) every carry is the q-carry at w = q², every plateau step is r = 1;
 (iii) R(x_n) = 2e_q(n) + 1, so R grows by 2 per carry.
*Proof.* Induction on the carries. State: γ, exponents (e_u, e_q, e₂) = (o−1, e, e₂), e ≥ 1. All w ≤ q² are < g, so h = 1, b' = g, and persistence is automatic from T49 once all d ≡ 1 (mod g).
The residues of the u-part and q-part together are H (u^c ≡ q^c, c ∈ [0, o−1]), independent of e. The only other prime is 2 with exponent e₂ ≥ 1 (and no other prime has p² | w, since the only primes < q have exponent 0 and u > q).
*Available new parts at w < q²:* a new part M(d) = M has M² | w < q², so M ≤ q−1 and M is a product of primes < q. d = M·(old part) ≡ 1.
If M is odd, 2 is not in M, so the 2-part ranges over 2⁰,…,2^{e₂} (which represent all of ⟨2⟩ modulo H) and d ≡ 1 needs M ∈ ⟨2⟩H = K — excluded by (Q2).
If M is even, the 2-exponent is exactly e₂ + j with 2^{e₂} ∈ H, and d ≡ 1 needs M ∈ H — excluded by (Q2). (Also 2 ∉ H by (Q1) covers M = 2.) So r = 1 at every w ≤ q² − 1.
*At w = q²:* σ' = qL; the new part M = q is available iff q^{e+1}·u^c·(2-part with 2^a ∈ H) ≡ 1 for some c ≤ o−1, i.e. q^{e+1+c} ≡ 1: c ≡ −(e+1) (mod o) works. No other new part has M² | q². So r = q, γ' = q²/q² = 1.
Hence the state after the carry is the same shape with e → e+1, which proves (i),(ii). (iii): d = 2^a q^b u^c ≡ 1 forces 2^a ∈ H, i.e. a ∈ {0, e₂} (2 ∉ H and e₂ is the first return); for each (a, b) there is exactly one c mod o, so R + 1 = 2(e+1). QED
*Instances (all verified by direct iteration of C, and by a class-closure certificate T51):*
 q = 3: g = 11, seed (2²·3³·5⁴) [T50; a different saturator, 5 ≡ 3³], and the template seed {47: 4, 3: 1, 2: 2}; P = 8, ρ = 3.
 q = 5: g = 31 (and g = 71 independently, found by random search); P = 24, ρ = 5.
 q = 7: g = 367, seed {3677: 60, 7: 1, 2: 3}; P = 48, ρ = 7; class period 2928, exact G = 367.
*Sharpness.* (Q2) is necessary in the template: for g = 193, q = 7 the orbit is a 3-carry instead (3 ∈ ⟨2⟩H although 3 ∉ H) — this was the failure mode of the first design attempt.
**OPEN (O9.1).** Whether (Q1)–(Q4) can be met for *every* prime q is not proved (the conditions are finitely many "non-membership" conditions on a cyclic quotient of (Z/g)*, so a Chebotarev/Kummer argument is plausible — not carried out). Data: field9.py prints the smallest g found for q up to 23.

## T58 — Corrections to v008 (PROVED / registered erratum)

v008 is unchanged on disk as a historical record. In v009 the following statements of v008 are **withdrawn or corrected**:
(E1) **M4a** ("for every x₀ there is n₀ with x_{n+3} = 4x_n for n ≥ n₀") is **FALSE**: the G = 11 orbit of T50 has x_{n+3}/x_n ∈ {3/2, 8/5, 7/4, 2, 5/2, 18/7, 27/8, 4} forever (T50 (iv)), and the q-carry orbits (T57) have x_{n+q²−1} = q²x_n with other gamma-cycles.
(E2) **M4b** ("every orbit is eventually x = s²t/g with t ∈ {1,2,3}") is **FALSE** (same orbits: t runs through 1,…,q²−1 and the "s" absorbs carries).
(E3) **T48 reformulation.** The v008 equivalence "x_{n+3} = 4x_n iff γ_{n+3} = γ_n and L_{n+3} = 2L_n" is misstated. The correct statement (G unchanged over the three steps, x = γL²/g):
   **x_{n+3} = 4x_n ⇔ γ_{n+3} L_{n+3}² = 4 γ_n L_n² ⇔ γ_{n+3} = 4γ_n / ρ² with ρ = L_{n+3}/L_n ∈ ℕ.**
   The two sufficient special cases are (ρ = 2, γ_{n+3} = γ_n) and (ρ = 1, γ_{n+3} = 4γ_n); other pairs with ρ² | 4γ_n are also allowed by the identity. Separate γ and L conditions are *sufficient, not necessary*.
(E4) The v008 remark "in every known regime the process is the cycle 1,2,3" and "M4.3: cycle 1,2,3 forced" are superseded by T54: the γ-cycle is 1,…,M²−1 with M the minimal available prime-power carry; M = 2 gives 1,2,3.
(E5) v008 T47 is consistent with everything here (γ ≤ 8 ≤ 2M for the G = 11 orbit); it is used (as proved) in T51.
Also from v007/v008 (carried): "K10.6/T39/T41: P needs gcd(g,6)=1" was superseded in v008 (T46) and is not used.

---------------------------------------------------------------------------------------------------------------------------------

## Summary of status after v009

PROVED: T49–T58 (T50 and T57 by explicit hand proof; T51 by finite-state closure; T52–T56 by the one-step law).
DATA: Q-table (smallest g for q ≤ 23), even-g persistent orbit (E1: g = 68), nonstandard cycles (P = 33 ρ = 32 etc.), partial carry transients (C2), random-seed statistics (P1, P2, C1, K1).
OPEN: O9.1 (every q realised?); O9.2 (a cycle with ≥2 active primes); classification of *which* g > 1 admit persistent orbits (even g and odd g with 3|g beyond found instances); how often natural seeds land in each carry word (probabilistic question); whether composite carries can persist when some participating prime has bounded exponent forever (excluded by T55 only for recurring carries — a *non-recurring* composite carry is a transient).
