# UNNS-SCALE-I v008 — Variable-Parameter Midpoint Arithmetic

Labels: PROVED / CERTIFIED (exact finite computation, re-checked by `verify_all_v008.py`) / EXPERIMENTAL / OPEN.
v005 Part A frozen; v006, v007 unchanged (hash-checked); see `ERRATUM_v007.md` for a correction found in this release.
**D_{10^6} is still OPEN (4 <= D <= 6).** v008 produces new exact structure, a correction, and no obstruction.

## 1. The midpoint equation in exact coordinates
Four-step route of type (+-|+-) at scale B: forward labels N | Bn, M | B(n+1), backward labels q, r with q^2 | Bn(N+1)^2/N, r^2 | B(n+1)(M+1)^2/M, q, r >= 2.
Midpoint z = Bn(N+1)^2(q-1)/(Nq^2) = B(n+1)(M+1)^2(r-1)/(Mr^2). Cleared form (reviewer's): nM(N+1)^2r^2(q-1) = (n+1)N(M+1)^2q^2(r-1).

**Theorem L (coordinates) — PROVED, CERTIFIED.** Put v = gcd(N,n), d = N/v (then d | B), v' = n/v, and write rho = (N+1)/q = P/Q in lowest terms.
Then (N,q) is a legal pair iff P | N+1, Q^2 | (B/d)v', gcd(P,Q)=1, q = Q(N+1)/P >= 2; the map (N,q) <-> (d,v,P,Q) is a bijection. Moreover
 z = B n rho (N+1-rho)/N,
 so the route condition is n·rho(N+1-rho)/N = (n+1)·rho'(M+1-rho')/M (rho' = (M+1)/r, the same coordinates at n+1).
Proof. x1 = Bn(N+1)^2/N = (B/d)v'(N+1)^2 and q = Q(N+1)/P, so x1/q^2 = (B/d)v'P^2/Q^2, an integer iff Q^2 | (B/d)v' (gcd(P,Q)=1). z = x1(q-1)/q^2 = Bn rho(N+1-rho)/N after substitution q = (N+1)/rho. ∎
Check: complete divisor enumeration at B = 10^6 for 92 numbers (1,097,012 pairs) gives identical pair sets.

**Theorem L' (integer system) — PROVED, CERTIFIED.** With a = Bn/(NQ^2), a' = B(n+1)/(MQ'^2) (integers):
 (S2) Q'^2 a' M - Q^2 a N = B,  (S1) a·P(Q(N+1)-P) = a'·P'(Q'(M+1)-P').
Conversely any positive integers satisfying S1, S2 with P | N+1, P' | M+1, gcd(P,Q)=gcd(P',Q')=1 and Q(N+1)/P, Q'(M+1)/P' >= 2 define n = Q^2aN/B and a route. So (+-|+-) routes are exactly the integer points of two equations; B enters only as the constant of S2. Verified on all 12,862 stored routes.

## 2. Necessary conditions
**Divisibility Lemma — PROVED, CERTIFIED.** n | N·Q^2·P'^2·(r-1) and n+1 | M·Q'^2·P^2·(q-1).
Proof. Cross-multiplied midpoint law: nP(Q(N+1)-P)Q'^2M = (n+1)P'(Q'(M+1)-P')Q^2N, and Q'(M+1)-P' = P'(r-1) since r = Q'(M+1)/P'. Since gcd(n,n+1)=1, n divides the factor of the right side other than n+1. ∎ (Equivalently v' | d·Q^2P'^2(r-1): the part of n not absorbed by N must be built from the OTHER side's M+1 and r-1.)

**Absorption Lemma — PROVED, CERTIFIED.** Let l be a prime, l not dividing B, l || n. Then l | N or l | M+1 or l | r-1. Likewise l || n+1 implies l | M or l | N+1 or l | q-1.
Proof. l ∤ Q because Q^2 | (B/d)v' and l^2 ∤ v'. Apply the Divisibility Lemma; l | P' implies l | M+1. ∎
Check: 50,345 prime instances over all 12,862 routes: none unabsorbed. Corollary (**large primes force large labels**): T := max(N,M,q,r) >= l-1 for every such prime. Verified for 1,713 exact minimal routes (min T/(l-1) = 1.00, attained).

**Growth Theorem — PROVED, CERTIFIED.** n <= N(M+1)^2 q^2 (r-1) <= T^4(T+1)^2 (n = N(M+1)^2q^2(r-1)/D with D a positive integer). Hence any route needs T >= c n^{1/6}.
Observed (exact minimal route label over all (+-|+-) routes, 1,713 numbers, B = 10^6): log T/log n has minimum 0.513, median ~0.91; the n^{1/6} bound is far from sharp. **OPEN** (conjecture): T >= c n^{1/2}.

## 3. Bounded forward labels (the "square-root regime")
**Theorem S — PROVED (analytic argument, constants not optimised), CORROBORATED.** For fixed N, M, only finitely many n admit a (+-|+-) route with those forward labels (whatever q, r).
Proof. Put c0 = M(N+1)^2/(N(M+1)^2). The cleared equation gives q^2(r-1)/(r^2(q-1)) = c0 n/(n+1), hence q/r = c0 + O(1/r) and mu = beta q - alpha r is a bounded integer (c0 = alpha/beta). With q = c0 r + m0 one finds D := M(N+1)^2r^2(q-1) - N(M+1)^2q^2(r-1) = K1(c0-1-m0) r^2 + ... (the cubic term cancels; K1 = M(N+1)^2). n = N(M+1)^2q^2(r-1)/D. If the r^2 coefficient is nonzero then n = O(r), but q^2 | Bn(N+1)^2/N forces r = O(sqrt n) -> n bounded. If it vanishes (m0 = c0-1, i.e. q+1 = c0(r+1)) then D = K2(c0-1)((c0+1)r+c0-1) and n = (c0 s-1)^2(s-2)/((c0-1)((c0+1)s-2)), s = r+1, whose polynomial division leaves a nonzero constant remainder; integrality for infinitely many s is impossible. (The case c0 = 1, i.e. N = M, gives D = -K1·mu·(rq-q-r), n = O(r) again.) ∎
Symbolic identities for D(r) are checked by the verifier. Computation: all N, M <= 6, q = rho·q0, r = sigma·r0 (q0,r0 <= 6, rho,sigma <= 1000): exactly 126 routes, 25 distinct n (largest 37,179), no growing family. Degeneracy test for every (N, M, P, P') with N, M <= 40: no degenerate tuple.
Consequence: any universal construction needs forward labels that grow with n. In every route found, N or M is of size comparable to n or n+1 (prime scan below) or the route is a constant-ratio shape.

## 4. Primes and adversarial multiples
- **Prime scan (CERTIFIED).** For 560 prime n (400 in [1e3,1e6], 160 in [1e9,1e10]) the exact route set is non-empty; in every route the prime is absorbed by N (never by M+1 or r-1), and the minimal label is p-1 or p (median ratio 1.000). The routes are equal-ratio (rho = rho') with v' = 1 and a small w' | p+1.
- **Adversarial multiples (CERTIFIED).** L_S := lcm of v'P over all constant-ratio shapes with rho > 1 (the v007 shapes), v',w' <= 12, P <= S (L_5 = 831,600; L_30 = 3,693,499,009,200). By construction n = kL_S lies in no class of those shapes. For all 28 tested n = kL_S (S = 5,10,20,30; k = 1..7) an exact (+-|+-) route nevertheless exists: mostly rho = 1/2 or 1/5 (P = 1), occasionally rho with P > S. This is how the erratum was found.

## 5. Constant-ratio shapes revisited (correction of v007)
Shapes (v',w',c,d): c,d | B, gcd(v',w')=1, Delta = c w' - d v' != 0, rho = 1 + cd/Delta = P/Q > 0, gcd(c,P) = gcd(d,P) = 1, Q^2 | (B/c)v', Q^2 | (B/d)w'. Class: v' | n, w' | n+1, P | Q(cn/v'+1). The proof of Theorem A'' of v007 is unchanged for Delta < 0.
- Shapes with P = 1 have no congruence condition. Example (3,1,1,1): rho = 1/2, route for every n divisible by 3. Infinite lines: for (c,d,Q) with Q-1 | cd, all (v',w') with d v' - c w' = Qcd/(Q-1), subject to Q^2 divisibility, e.g. c=d=1, Q=2: v' = w'+2 (w' odd): n has a route whenever (w'+2) | n and w' | n+1 for some odd w'.
- The obstruction of v007 survives only for P > 1 shapes (checked: n = lcm(v'P)·k, K <= 2, is covered by no P > 1 shape).
- Coverage of n <= 2·10^6 (EXPERIMENTAL, exact count; uncovered numbers) — shapes rho>1 only vs with rho<1: K=1: 585,051 / 585,051; K=2: 405,526 / 405,526; K=3: 46,086 / 2,698; K=4: 37,485 / 2,698; K=6: 26,668 / 692; K=8: 18,059 / 387; K=12: 10,497 / 4; K=20: 7,803 / 2; K=40: 6,170 / 1 (see results/C1).
- Residual scan: with shapes v',w' <= 20 only 48 numbers n <= 2·10^7 are uncovered; each has an exact (+-|+-) route (found by complete enumeration; none without).
- Coverage by a finite set F of shapes is periodic in n (period lcm of v'P and w'), so "F covers every n >= n0" is a finite check; whether such an F exists is a covering-system question and is **OPEN**. The mechanism that rescues the multiples of L_S is exactly the P = 1 family; a correct obstruction for the full family would have to defeat the lines of P = 1 shapes simultaneously.

## 6. Status
- PROVED: Theorem L, Theorem L' (integer system), Divisibility and Absorption Lemmas, Growth Theorem (n^{1/6}), Theorem S (bounded forward labels finite), correction of Theorem A'' range (rho<1).
- CERTIFIED: lemma checks on 12,862 routes; prime scan; adversarial multiples; residual scan.
- OPEN: D_{10^6} in {4,5,6}; existence of a finite or parametrised family covering all n; T >= c n^{1/2}; the 12 undetermined divisor scales of v006.
- No obstruction (disjoint radius-two balls) was found: in all tests, including 48 residual numbers, 28 adversarial multiples and 560 primes, a four-step route exists.
- Gate 4 deferred. No GitHub changes.
