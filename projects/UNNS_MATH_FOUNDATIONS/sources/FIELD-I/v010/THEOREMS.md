# FIELD-I v010 — THEOREMS (T59–T63): Multi-Prime Carry Coexistence

Status tags: **PROVED** (hand proof from earlier theorems; the tests are consistency checks, not the proof), **DATA**, **OPEN**.
Notation as in v009: persistent orbit with G = g, x = γL²/g, exponent state E = (e_p), o_p = ord_g(p), w = γ + 1, and T49–T58 of v009 (unchanged).

Question of v010 (O9.2): can two distinct primes p ≠ q both carry infinitely often in the eventual regime of a persistent orbit?
**Answer: no. At most one prime carries infinitely often (T60), for every g and every seed.**

---------------------------------------------------------------------------------------------------------------------------------

## T59 — The carry scheduler (PROVED; T53–T56 restated as a dynamical system)

**Eventual regime.** By T51 the orbit is eventually class-periodic. Call a prime *active* if its exponent is unbounded and *inert* otherwise. After a finite time only active primes change their exponent,
every active prime is saturated (e_p ≥ o_p − 1), and (T54, T55) every carry is complete and a prime power p^j with γ = 1 immediately before it and w = p^{2j}.
**Pending carry.** For a state E and a prime p ∤ g put e = e_p (0 if p ∤ L) and
 j_p(E) = min{ j ≥ 1 : p^{e+j}·a ≡ 1 (mod g) for some a ∈ 𝒜_{−p}(E) },  c_p(E) = p^{j_p(E)},
where 𝒜_{−p}(E) is the set of residues of divisors of ∏_{q≠p} q^{e_q} (j_p = ∞ if no j ≤ o_p works).
**Statement.** At a reset state (γ = 1) of the eventual regime the next carry is **the prime p with the smallest pending carry c_p(E)** (ties are impossible: p^a = q^b has no solution with a, b ≥ 1 for p ≠ q).
Its exponent increases by j_p, no other exponent changes, the γ-cycle is 1, 2, …, c_p² − 1 and the next reset occurs after c_p² − 1 steps. The orbit stays persistent iff c_p² < g (g odd; c_p² < 4g for g even), T52(c).
Three immediate consequences, used in T60:
 (a) c_p depends on E only through e_p and the residue sets of the other primes. For a saturated prime these sets are the subgroup ⟨q⟩ whatever e_q is; for an inert prime they are constant.
     Hence for an active p, c_p is a function of **e_p mod o_p alone**: c_p = p^{gap_p(e_p)}, gap_p(e) = min{ j ≥ 1 : (e + j) mod o_p ∈ Abs_p } (T56).
 (b) For an inert prime c_p is **constant** ("frozen").
 (c) After p fires, e_p mod o_p ∈ Abs_p; each further firing of p moves e_p mod o_p to the next element of Abs_p in the cyclic order of Z/o_p (so p visits every element of Abs_p cyclically).
*Proof.* By T54 the next carry from γ = 1 is the smallest M that is available at w = M². By T53 a new part M(d) is available iff M(d)² | w. In the eventual regime a composite M(d) involves ≥ 2 primes whose exponents change,
hence active (so saturated); by the argument of T55 such an M is not minimal. So the minimal available M is a prime power p^j, and p^j is available iff p^{e+j}·a ≡ 1 for some a ∈ 𝒜_{−p}, i.e. iff j ≥ j_p;
the smallest available M is therefore min_p p^{j_p}. (a)–(c) follow from the definitions and T56. QED
*Test S1:* the scheduler (min over all primes p ≤ 2√g of p^{j_p}) reproduces the residue machine's carry at every reset state of every collected eventual cycle.

---------------------------------------------------------------------------------------------------------------------------------

## T60 — Single-prime dominance (PROVED): at most one prime carries infinitely often

**Theorem.** In the eventual regime of every persistent orbit (every g, every seed) exactly one prime is active. Equivalently: **no x₀ and no p ≠ q exist with p and q both carrying infinitely often.**
The same holds for every abstract system of cyclic odometers (Z/s_i, C_i, p_i), s_i ≥ 1, C_i ≠ ∅, with the minimum-pending-carry rule (T59): at most one odometer fires infinitely often.

**Proof.** Some prime is active (otherwise L is eventually constant and γ_n ≤ 2M eventually (v008 T47) would make x_n bounded, but x_{n+1} > x_n). Suppose p ≠ q are both active. For an active prime r let
 m_r = max{ r^{gap_r(k)} : k ∈ Abs_r }
be its **worst-case pending carry** (largest value of c_r once r has fired at least once); at that time e_r mod o_r ∈ Abs_r so c_r ≤ m_r always (T59(c)). Distinct primes never have equal powers, so m_p ≠ m_q;
let p be the active prime with the larger m (among two or more active primes take p to be the one with the largest m_r, q any other active prime). Then m_q < m_p.
Choose k* ∈ Abs_p with p^{gap_p(k*)} = m_p. Since p fires infinitely often and by T59(c) its residue runs cyclically through all of Abs_p, there is a reset time t after both p and q have fired at least once with e_p mod o_p = k*, so c_p = m_p.
From then on p's exponent can change only when p fires, and p fires only when c_p < c_r for every other prime r (T59). But c_q ≤ m_q < m_p = c_p at **every** later reset (q is past its first firing, and c_q ≤ m_q is a bound valid at all times).
So p never fires after t, contradicting that p is active. Hence at most one prime is active; by the first sentence exactly one. The argument used only (a)–(c) of T59, so it applies verbatim to abstract odometer systems. QED

**Corollary 1 (starvation rule).** The unique active prime r satisfies m_r < c_p for every inert prime p with a finite pending carry (apply the proof to r's worst-case state: r fires from it only if m_r < c_p, and c_p is frozen).
In particular, among *saturated* primes with nonempty Abs the survivor is the one with the **smallest worst-case pending carry** m. This is the structural rule governing coexistence: the prime with the largest worst-case carry is always the one that starves.
(Test X1: in all abstract pairs and all start states the survivor is the smaller-m prime; tests R3, R4: on real cycles the survivor's m is smaller than every competitor's frozen pending carry.)
**Corollary 2 (the "threshold-overlap" necessary condition is vacuous).** For two primes to coexist one would need B_p⁺ > B_q⁻ and B_q⁺ > B_p⁻ (maxima/minima of the candidate sets). The proof above shows more: coexistence would need m_q > m_p *and* m_p > m_q.
So the pair filter proposed for v010 never leaves a survivor; the product-automaton criterion reduces to "never".
**Corollary 3 (one rule for every regime).** Regime I (G_∞ = 1, x_{n+3} = 4x_n) is the single-prime system p = 2 with γ-cycle 1,2,3; the eight-step (p = 3), 24-step (p = 5), 48-step (p = 7) and mixed-power cycles are single-prime systems with other (p, Abs_p).

---------------------------------------------------------------------------------------------------------------------------------

## T61 — The eventual scaling factor is a prime power (PROVED)

Let p be the active prime (T60), Abs_p ⊂ Z/o_p with minimal translation period s (the least s | o_p with Abs_p + s = Abs_p), and j_1, …, j_m the gaps of Abs_p inside one period (Σ j_i = s).
Then the eventual orbit has **γ-period P_γ = Σ_{i=1}^m (p^{2j_i} − 1)** and **L_{n+P_γ} = p^s L_n**, hence
 **x_{n+P_γ} = p^{2s} x_n**,
i.e. the scaling factor ρ is a **prime power p^s**. (For G_∞ = 1: p = 2, s = 1, P_γ = 3, ρ = 2.) Every orbit of the collective map therefore eventually satisfies x_{n+P} = p^{2s} x_n with p prime.
*Proof.* One active prime: the carries are the successive gaps of Abs_p around Z/o_p (T56) with cycle lengths p^{2j}−1 (T54). The carry word is periodic with the minimal rotation period equal to the minimal translation period s of Abs_p,
and over it e_p increases by Σ j_i = s while all other exponents are constant. QED
*Tests R2, C1:* ρ = p^s on every collected single-prime cycle and every control (g = 31: Abs = {0,2,4} mod 5, s = 5, ρ = 32, P_γ = 15+15+3 = 33; g = 17: s = 8, ρ = 256; g = 11, 31, 367: Abs = Z/o_p, s = 1, ρ = q).

---------------------------------------------------------------------------------------------------------------------------------

## T62 — Two saturated clocks have coprime periods (PROVED for prime g; arithmetic structure of Abs)

Let g be an odd prime, p ≠ q active (or merely saturated) with orders o_p, o_q, background F (residues of the frozen part). Then 𝒜_{−p} = ⟨q⟩·F is a union of cosets of ⟨q⟩, and Abs_p = {k : p^{−k} ∈ ⟨q⟩F} is invariant under k ↦ k + τ_p, τ_p = o_p / gcd(o_p, o_q);
likewise Abs_q is τ_q-periodic with τ_q = o_q / gcd(o_p, o_q). **τ_p and τ_q are coprime.**
*Proof.* (Z/g)* is cyclic, so |⟨p⟩ ∩ ⟨q⟩| = gcd(o_p, o_q) and p^τ ∈ ⟨q⟩ iff τ is a multiple of o_p/gcd(o_p,o_q). Then p^{−(k+τ)} ∈ ⟨q⟩F ⇔ p^{−k} ∈ ⟨q⟩F. The numbers x/gcd(x,y) and y/gcd(x,y) are coprime. QED
Meaning: the two clocks can only be coupled through the common background F, and their natural periods share no factor, so phase locking is impossible by the arithmetic as well; T60 shows that the lack of coupling is not even needed — the scheduler rule alone excludes coexistence. (Test X3.)

---------------------------------------------------------------------------------------------------------------------------------

## T63 — Corrections to the v010 problem statement (registered)

(E1) The lemma "if p, q both occur infinitely often then B_p⁺ > B_q⁻ and B_q⁺ > B_p⁻" is **true but far from sharp**; its sharp form is T60 (m_q > m_p and m_p > m_q), which is contradictory.
(E2) "Two counter-rotating admissibility odometers with alternating carry thresholds" cannot exist, even abstractly: with the min-rule scheduler, the odometer whose worst-case pending carry is larger is always the one that stops (test X1 is exhaustive for small moduli).
(E3) The classification tags used in the search: ABSTRACT_COEXISTENCE = none; ARITHMETIC_REALIZABLE = none; COLLECTIVE_CERTIFIED = none; EXCLUDED = every candidate pair, by proof (not by search).

---------------------------------------------------------------------------------------------------------------------------------

## Status after v010

PROVED: T59 (scheduler), T60 (single-prime dominance + starvation rule), T61 (ρ = p^s), T62 (coprime clocks), T63 (registered corrections). v009's O9.2 is **resolved negatively** (it is a theorem, not a search result).
OPEN: **O10.1** a closed decision rule from the seed for *which* prime survives (T60 gives the necessary rule m_r < frozen pending carries; the full rule requires running the scheduler);
**O10.2** (=O9.1) whether (Q1)–(Q4) of T57 are solvable for every odd prime q (see RESULTS for the extended data q = 11: g = 6689);
**O10.3** which triples (g, p, Abs_p) are realizable by seeds (the classification of eventual types) — T62 and the window c² < g restrict them, but a complete characterisation is not given;
**O10.4** the same single-dominance question for orbits with composite or even g is covered by T59–T60 (the proof does not use primality of g), but the numerical sample is almost entirely prime g.
