# UNNS_U4_GEN_v001 — Intrinsic Branching and Autonomous Generative Dynamics

Author: UNNS Research Collective. Inherits unchanged (hashes in inherited/): UNNS_U4_STAGE2_v001, UNNS_U4_M2_ENT_v001. Frozen imports: G is triangle-free; edge set {kN, k(N+1)²}. "Proved" = complete written proof, author-level, external review pending. Classical results cited are prior art, not claimed.

**Setting.** Forward move with parameter N | x: x → x(N+1)²/N =: F_N(x) (edge {x/N·N, x/N·(N+1)²}). A forward move strictly increases the value (F_N(x)/x = N+2+1/N ≥ 4.5 for N ≥ 2... for N≥1 it is ≥ 4), so a forward-only trajectory never revisits a vertex, and since x_{n+2} ≠ x_n and G is triangle-free, it is a legal Y_NB history (U4-M2 item 1). *Branch capacity* at x: b(x) = τ(x) − 1 (choices N ≥ 2).

## GEN-1 — Finite return-state obstruction

**Selector.** Σ = (Q, q₀, K, δ, μ) with Q finite; configuration c_n = (q_n; x_n, x_{n−1}, …, x_{n−K}); x_{n+1} = μ(c_n) ∈ N_G(x_n); q_{n+1} = δ(c_n). μ, δ are time-independent and may be arbitrary (exactly computable or not). The initial K preceding vertices are arbitrary.

**Theorem GEN-1.** Let G be locally finite and h a vertex with x_n = h for infinitely many n = n₁ < n₂ < …. Then (i) the configurations c_{n_i}, (ii) the choices x_{n_i+1}, (iii) the return times n_{i+1} − n_i, and in fact (iv) the entire trajectory (x_n)_{n ≥ n₁}, are eventually periodic. Preperiod plus period of the visit-configuration sequence is at most |Q|·|B_K(h)|^K.

**Proof.** For i > K, the K vertices preceding visit n_i are joined to h by a walk of length ≤ K, so they lie in B_K(h), finite by local finiteness. Hence c_{n_i} ∈ 𝒞_h = Q × {h} × B_K(h)^K, a set of at most |Q||B_K(h)|^K elements. Since c_{n+1} is a function of c_n (μ, δ time-independent), the whole future from time n is a function of c_n; in particular c_{n_{i+1}} = Φ(c_{n_i}) for a fixed map Φ on 𝒞_h. An orbit of a map on a finite set is eventually periodic: there are i < j with c_{n_i} = c_{n_j}, hence c_{n_{i+t}} = c_{n_{j+t}} for all t ≥ 0 and x_{n_i+s} = x_{n_j+s} for all s ≥ 0. All four claims follow. ∎

**Corollary GEN-1c.** A K-history finite-control selector on a locally finite graph either has an eventually periodic trajectory, or visits every vertex only finitely often. In particular, a non-eventually-periodic itinerary requires the trajectory to leave every finite set (a *moving hub*), and requires unbounded state: the current vertex's value is such a state.

**Falsification.** A locally finite graph, a finite-control K-history deterministic selector, and a vertex visited infinitely often with a non-eventually-periodic trajectory. **Does not establish:** anything for selectors with unbounded counters (they can code any sequence; e.g. a counter n and the Thue–Morse digit t_n choosing among E1 blocks gives non-periodic returns at a fixed hub — coded, input = the sequence t); anything about moving hubs.

**Corroboration (bounded).** 162 random time-independent selectors (K ∈ {0,1,2}, |Q| ∈ {1,2,3}, hubs 12, 60, 16, window = ball of radius 3): 0 violations; in the 14 runs with a repeated configuration, configurations and return gaps repeat exactly thereafter; in the 13 runs where the pigeonhole bound is exceeded a repeat was always found. (Most random selectors wander off and return too rarely to test — the evidence is weak and the proof is the proof.) Independent replay of the 133 stored Stage-2 CYCLE rows (x ≤ 10¹⁰) reproduces outcome, preperiod and period in all cases, including the 13 period-21 rows (histogram of periods 2:88, 4:1, 6:1, 19:17, 21:13, 30:8, 65:5); 5 larger rows skipped. These selectors are K ≤ 1, |Q| = 1, so the theorem applies and is consistent: each is eventually periodic.

## GEN-2 — Prime-fire collapse

**Definition.** A *prime-fire* step from x ≥ 2 chooses a prime p | x (N = p) and moves to x(p+1)²/p. A prime-fire selector is any rule (of any kind) choosing p at each step.

**Theorem GEN-2.** For every prime-fire selector and every start x₀ ≥ 2, primes ≥ 5 are fired only finitely often. Hence after a finite transient the itinerary lies in {2,3}^ℕ and evolves through the exponents (α, β) = (v₂, v₃) by the two moves A: (α,β) → (α−1, β+2) (fire 2) and B: (α,β) → (α+4, β−1) (fire 3).

**Proof.** Let q | p+1 be prime. For p = 2: p+1 = 3; for p = 3: p+1 = 4; for odd p: p+1 is even and q ≤ (p+1)/2 < p. So firing p ≥ 5 lowers e_p by 1 and raises exponents only at primes < p (including 2, 3); firing 2 or 3 changes only e₂, e₃. Primes ≥ 5 that can ever occur are ≤ P = max(largest prime of x₀, 3), a finite set. Order the vector (e_p)_{p ≥ 5, p ≤ P} lexicographically from the largest prime down; every fire of a prime ≥ 5 strictly lowers it, fires of 2, 3 leave it unchanged. Lexicographic order on ℕ^m is a well-order, so only finitely many fires of primes ≥ 5 occur. ∎

**Does not establish:** the length of the transient (only finiteness; it can be astronomically long, Hydra-like), anything about composite N (N+1 may introduce new primes ≥ 5, so the collapse does not apply; observation only).

## GEN-3 — The smallest-prime-factor rule is eventually periodic of period 5

**Theorem GEN-3.** Rule SPF (fire the smallest prime factor). For every x₀ ≥ 2 the itinerary is eventually the periodic word (3,2,2,2,2)^∞ (up to phase).
**Proof.** If x₀ is coprime to 6, spf = p ≥ 5, and (p+1)² carries a factor 4, so x₁ has α ≥ 2. Whenever α+β > 0, SPF fires 2 if α ≥ 1 (→ (α−1, β+2), β ≥ 2 afterwards) else 3 (→ (4, β−1)); (0,0) is never reached. From (α,β) it fires 2 exactly α times, reaching (0, β+2α); from (0,β′) the five steps 3,2,2,2,2 lead to (0, β′+7), so the itinerary is (3,2,2,2,2)^∞. ∎ (Registered check: period 5 for all 171 starts.) This is a retained negative result: the simplest autonomous rule is periodic.

## GEN-4 — Moving-hub rule with proved aperiodic branch itinerary

**Rule MAXPP (K = 0, |Q| = 1, vertex-only).** At x ≥ 2, fire the prime p whose prime-power part p^{v_p(x)} is largest. (Ties between distinct primes are impossible.) The comparison is of integers; no constant, target sequence or branch list enters. Each fired N = p divides x, so the step is a legal forward edge; x_{n+1} > 4x_n, so the trajectory never returns and is a legal Y_NB history.

**Theorem GEN-4.** For every x₀ ≥ 2 the itinerary (p_n) of MAXPP satisfies:
(a) after a finite transient p_n ∈ {2,3};
(b) it is **not eventually periodic**;
(c) its tail factor complexity is p(n) = n+1 for all n (a Sturmian word), hence zero topological entropy of its orbit closure.
*Proof of (a).* GEN-2. *Proof of (b).* Let T be after the last fire of a prime ≥ 5; then (α,β) ≠ (0,0) for n ≥ T (otherwise a prime ≥ 5 would fire) and the fired prime is 2 iff 2^α > 3^β. Put f = α ln 2 − β ln 3 (never 0 for (α,β) ≠ (0,0), since 2^α ≠ 3^β). Firing 2 (f > 0) gives f′ = f − ln 18; firing 3 (f < 0) gives f′ = f + ln 48. Hence f stays in [min(f_T, −ln 18), max(f_T, ln 48)] for n ≥ T. Suppose the itinerary is periodic from n₀ ≥ T with period q, containing a fires of 2 and b fires of 3 (a+b = q ≥ 1). Then (α,β) advances by the constant (Δα,Δβ) = (−a+4b, 2a−b) per period, so f advances by Δα ln 2 − Δβ ln 3 per period; boundedness forces this to be 0. By unique factorisation ln 2 / ln 3 is irrational, so Δα = Δβ = 0, i.e. a = 4b and b = 2a, giving a = b = 0, a contradiction. ∎(b)
*Proof of (c).* In the regime n ≥ T the map f ↦ f′ is the rotation by ln 48 (≡ −ln 18) of the circle of length ln 18 + ln 48 = ln 864, and the fired prime is the code of the arc [−ln 18, 0) (length ln 18, equal to the rotation angle) versus [0, ln 48). The rotation angle ln 18 / ln 864 is irrational (18^a = 864^b is impossible), and the coding of an irrational rotation by an arc whose length equals the angle is a Sturmian word with complexity n+1 (Morse–Hedlund 1940; Coven–Hedlund 1973; Lothaire, *Algebraic Combinatorics on Words*, ch. 2 — **imported prior art**). Zero entropy follows from subexponential complexity. ∎(c, modulo the cited theorem)

**Registered check:** all 171 starts: tail has no period ≤ 400, complexity n+1 for n ∈ {1,2,3,5,8,13,21,34}; an independent big-integer implementation (no shared code) reproduces itineraries for 1500 steps on 69 runs with every edge verified legal (864 edges checked with the independent graph layer for x < 10¹¹).

**Information accounting (GEN-G6).** State: the integer x_n, with log₂ x_n ≥ 2n bits (observed ≈ 13,650 bits after 6000 steps). External input: 0 bits per step. Controller description: one line (27 characters). Contrast with a coded branch word: n bits of external input for n binary branches. **Classification (GEN-G4):** unbounded state, K = 0, |Q| = 1; the aperiodicity is carried by the growing counters (α, β). **What this is and is not:** it is an autonomous rule whose branching is non-eventually-periodic, with declared knowledge = the rule's one-line definition; but its itinerary is a *rotation coding* with zero entropy, a low-complexity sequence, not a universal one. It does not show positive entropy, universality, or that any sequence of interest is generated.

## Limits of the prime-fire class (answers to GEN-G5)

By GEN-2 every prime-fire selector is, after a transient, a deterministic guard g(α,β) ∈ {2,3} on a two-counter system. Aperiodicity (GEN-4) and positive entropy are distinct: MAXPP is aperiodic with entropy 0. Positive entropy within the class would need an extremely complicated guard (e.g. one encoding a positive-entropy sequence), which is declared knowledge, not intrinsic; **no intrinsic positive-entropy prime-fire rule is known or excluded.**

## Observations (registered, not theorems)

Prime-fire rules (171 starts, horizon 6000): MINPP tail period 3 (86 starts) or 5 (85); SPF 5; LPF 3; MAXEXP_SMALL 8; ODDEXP_SMALL 10; ROTATE_NEXT 2; MAXPP aperiodic. Prediction P3 (finitely many fires ≥ 5) held for all 1,197 runs. Divisor-fire (cap 64, composite N allowed, 60 starts, horizon 3000): MAXDIV eventual period 164 for all starts (10 distinct tail symbols, primes up to 61 appear — support is not collapsed); MINDIV4 period 2; RANKCYCLE5 period 5 (this one has control state |Q| = 5 and K = 1 itinerary history). All are eventually periodic within the horizon; periodic behaviour of composite rules is an observation only, no theorem. Nothing here shows composite branching cannot do better.

## Status table

| Item | Status |
|---|---|
| GEN-1 (+ Corollary) | Proved (author-level); corroborated; external review pending |
| GEN-2 | Proved (author-level) |
| GEN-3 | Proved (author-level); registered check passes |
| GEN-4 (a),(b) | Proved (author-level); (c) proved modulo classical Sturmian theorem |
| Positive-entropy autonomous rule | Open |
| Universality of any autonomous rule | Open |
| Composite-N dynamics | Observations only |
| SELECT/FIELD/GIG preservation | Open |
| Originality / prior-art review of GEN-2..4 | Not done (Fractran/Conway-type counter dynamics and Sturmian rotation codings are the obvious prior-art neighbours) |
