# UNNS-SCALE-I v006 — Arithmetic Intersection and Universal Metric Closure (exploratory)

Status labels: PROVED / CERTIFIED (finite exact computation, independently re-checkable) / EXPERIMENTAL / OPEN.
v005 Part A (M_{10^6} = 4 on the window 1 <= n <= 999999) is frozen and untouched. v006 does **not** close D_{10^6}.

## 1. Setting
SELECT-II graph on positive integers, edges {kN, k(N+1)^2}.
Forward move x -> x(N+1)^2/N (N | x); backward move x -> x(q-1)/q^2 (q >= 2, q^2 | x), label N = q-1.
d_B(n) = d(Bn, B(n+1)); D_B = sup_n d_B(n); D_B <= 6 for every B (v003).
Pointwise divisor law (v003): A | B => d_B(n) <= d_A(n), hence D_B <= D_A.

## 2. Proposition 1 (four-step criterion) — PROVED
d(x,y) <= 4  <=>  B_2(x) ∩ B_2(y) != ∅, where B_2 is the radius-2 ball.
Proof. If d(x,y) <= 4 take a shortest path and its vertex at distance min(2,d) from x; it lies in both balls (the remaining distance is <= 2). Conversely a common vertex z gives a path of length <= d(x,z)+d(z,y) <= 4. ∎
Consequences: D_B >= 5 is equivalent to the existence of n with B_2(Bn) ∩ B_2(B(n+1)) = ∅. A certificate of that is a pair of complete radius-2 balls. For d = 5 radius (2,3) suffices, for d = 6 radius (3,3).
Word types of a radius-2 neighbour of x are ++, +-, -+, -- (and the shorter words). A four-step route is a pair (word_x | word_y) of such words reaching the same vertex; there are 16 pairs of length-2 words. `code/b2_types.py` enumerates the typed balls exactly.

## 3. Scale-divisibility experiment (E1, E3) — CERTIFIED
10^6 = 2^6 5^6 has 49 divisors A = 2^a 5^b. Because D_{10^6} <= D_A, a divisor with D_A = 4 would prove D_{10^6} = 4 ("sufficient scale").
Result (explicit edge-checked paths for every upper bound, complete-ball certificates for the lower bounds):
- D_A = 6 for A in {1, 2, 4, 5, 8, 10}.
- D_A >= 5 for A in {16, 20, 25, 32, 40, 50, 64, 80, 100, 125, 160, 200, 250, 320, 400, 500, 625, 1000, 1250, 2000, 2500, 3125, 5000, 6250, 10000, 12500, 15625, 25000, 31250, 50000} and A = 800 (witness n = 551339, found in E3 and audited in `E3_scale800.json`) — 37 divisors including the six above.
- Therefore none of these 37 divisors can serve as a sufficient scale.
- Not determined (12): 1600, 4000, 8000, 20000, 40000, 62500, 100000, 125000, 200000, 250000, 500000, 10^6. Time-boxed exact search over the 614 exceptional v005 values, n <= 200 (E1) and a further 40-300 values per scale (E3) found only distances <= 4. These are lower-bound searches and are NOT upper bounds. Some scales had a few n skipped by a memory guard (counted as 'memory' in the E3 files).
Reading: the divisor route can only succeed at one of the 12 remaining scales, and the experiment gives no evidence either way for D_{10^6}.

## 4. Primality audit of the lower-bound certificates — CERTIFIED
The exploratory engine uses fixed-base Miller–Rabin and is not authoritative. The independent complete-ball checker `audit_cert.py` verifies every factorisation by product equality, trial division below 10^6 and a 13-base deterministic Miller–Rabin (a proof below 3.317e24, Sorenson–Webster). For the six key certificates (D_10 = 6 at n = 365759 and 351359; D_4 = 6 at 62459; D_8 = 6 at 122939; D_1 = 6 at 365759; d_12(25199) = 5) the largest prime factor that occurs is 6.69e11, far below the bound, so every ball is complete and every lower bound is a proof. Records: `results/AUDIT_key_certificates.json`.

## 5. The (+-|+-) route — EXPERIMENTAL
Targeted exact test `pm_meet.py`: does there exist N | Bn, q^2 | Bn(N+1)^2/N and M | B(n+1), r^2 | B(n+1)(M+1)^2/M with equal results z = x(N+1)^2(q-1)/(Nq^2) = y(M+1)^2(r-1)/(Mr^2)?
Witness search at B = 10^6 for 12,862 values of n (the 614 v005 exceptional values, n <= 400, a random window sample, the v005 outside-window values, 6,000 random window values, 3,000 random values up to 10^9, 1,063 values with 720 | n+1 up to 10^10): **every n had a (+-|+-) witness**, each re-verified by integer arithmetic. A census with complete radius-2 balls on 14 values found every n meeting at total length exactly 4, with (+-|+-) present in 14/14.
This suggests the conjecture "for B = 10^6 every n admits a (+-|+-) four-step route, hence D_{10^6} = 4", but it is evidence, not a proof; a sample, even a large one, cannot rule out a sparse set of obstructions, and the known D_A = 5, 6 behaviour at smaller scales shows obstructions exist at those scales (the exceptional n there are what makes D_A > 4). We have no symbolic construction of the (N, q, M, r) parameters and no obstruction certificate for 10^6.

## 6. Honest state
- D_{10^6} in {4, 5, 6} remains OPEN (v005 Part B unchanged).
- Proved: Proposition 1; the divisor-lattice law; 37 of 49 divisors are not sufficient scales.
- Open: whether one of the 12 remaining scales is sufficient; a symbolic proof of (+-|+-) universality; an n with disjoint radius-2 balls at 10^6.
- Gate 4 deferred. v001–v005 unchanged (hash-checked). No GitHub changes.
