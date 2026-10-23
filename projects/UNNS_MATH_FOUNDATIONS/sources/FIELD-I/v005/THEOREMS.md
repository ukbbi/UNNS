# FIELD-I v005 — Theorems (T29–T34). Continues v004 numbering (T22–T28).

Notation as in SPEC.md. x = a/b lowest terms; a = s^2 t, t squarefree; u(D) = lcm{d^2}.

## T29 (Signature criterion for three-route rigidity; closes J1)
For d, e >= 2 put L = lcm(d,e), g = gcd(d-1,e-1). Then gcd(g, L) = 1, so w(d,e) = g/L^2 is in lowest terms and
w(d,e) = w(d',e')  <=>  (L,g) = (L',g').
Hence a three-route fibre is rigid (three edge weights pairwise distinct) iff its three signatures (L_ij, g_ij) are pairwise distinct.
*Proof.* A prime p | g divides d-1 and e-1, so p divides neither d nor e, hence not L. Thus gcd(g, L^2) = 1 and g/L^2 is reduced. Reduced fractions are equal iff numerators and denominators agree, and L^2 = L'^2 iff L = L'. QED
*Consequences (antichain, verified K1.4–K1.5).* Three distinct LCMs: always rigid. Two distinct LCMs: rigid iff the two edges sharing the LCM have different g. One LCM: rigid iff the three g differ. Applies to every three-route fibre, integer or rational (K1.7).

## T30 (Arithmetic of G)
For D(x) nonempty: (a) b | G(x); (b) gcd(u(D), G) = 1, so Delta_coll = u/G is reduced with denominator G; (c) G(x) = 1 <=> 2 in D(x) <=> x is an integer divisible by 4.
*Proof.* (a) every d = 1 mod b. (b) every d = 1 mod G is coprime to G, so d^2 and lcm are. (c) 2 in D means 4 | a and 1 = 1 mod b, i.e. b = 1 hence x integer, 4|x; conversely then s is even (v2(x) = 2 v2(s) + v2(t) >= 2 with v2(t) <= 1 forces v2(s) >= 1), so 2 in D, G | 1. If G = 1 and x not an integer 4|x, then either b >= 2 (contradicting b | G) or x integer with s odd, all d odd, d-1 even, G even: contradiction. QED

## T31 (Monotone orbits)
D(x_n) is contained in D(x_{n+1}), and G_{n+1} | G_n.
*Proof.* Write x_n = a/b, Delta = u/G. Over denominator G the sum has numerator aG/b + u, divisible by d^2 for d in D (d^2 | a, d^2 | u). Since d = 1 mod G it is coprime to G, so d^2 divides the reduced numerator, and d = 1 mod G is 1 mod the reduced denominator. Hence D grows and G, a gcd over a larger set, divides the old G. QED

## T32 (Regime I: closed dynamics, G = 1)
Let x be an integer divisible by 4, x = s^2 t. Then s is even, D(x) = {d | s : d>=2}, G = 1, Delta_coll = s^2, and
C(x) = s^2 (t+1) = s'^2 t', with s' = s * sigma, sigma^2 || t+1 (largest square divisor), t' = sqf(t+1).
s' is even, so regime I persists. The map t -> sqf(t+1) absorbs every t into the cycle 1 -> 2 -> 3 -> 1 (sigma = 1, 1, 2). After absorption s multiplies by 2 every three steps and nothing else.
*Proof.* Everything but absorption follows from T30 and s in D (u = lcm of squares of divisors of s = s^2). Absorption: for t >= 4, if t+1 is not squarefree then t' <= (t+1)/4; one of t+1, t+2, t+3, t+4 is divisible by 4, so within <=4 steps the value drops to <= (t+4)/4 < t. Values <=3 are in the cycle. QED
*Corollary R.* With N the entry time and s_N the value of s then, R(x_n) = tau(s_n) - 1, which is non-decreasing and grows linearly (the exponent of 2 rises by 1 per three steps).

## T33 (Non-universality) — answers the v005 primary question
For every collective orbit, the reach set U = union D(x_n) omits infinitely many d >= 2 (it has counting function O(log X); density 0). Precisely:
 (A) if G_inf > 1 then U contains only d = 1 mod G_inf; in particular 2 is never reached;
 (B) if G_inf = 1 then the orbit is eventually in regime I and U = {d >= 2 : d | s_N 2^k, some k}; every d with an odd prime factor not dividing s_N is never reached.
*Proof.* By T31, G_n | G_{n-1} stabilises at G_inf, and every d in D(x_n) has d = 1 mod G_n, hence mod G_inf. (A) is immediate. (B): G_{n0} = 1, so x_{n0} is an integer 4|x (T30), T32 applies; by T31 D(x_n) for n < n0 is inside D(x_{n0}). Counting: tau(odd(s_N)) (1 + log_2 X). QED
*Reading.* The v004-review outcome (i) is false for every orbit. Outcome (ii) is the case G_inf > 1, not excluded by T33 alone (see T34, Open). Outcome (iii) is realised by every orbit that reaches G = 1; so "G -> 1" is necessary for nothing here and sufficient for nothing: the obstruction is the arithmetic of odd primes, not only G. Explicit: the orbit of 4 is 4, 8, 12, 16, 32, 48, 64, 128, ... and reaches only powers of 2.

## T34 (G = 2 cannot persist)
If G(x) = 2 then G collapses to 1 in at most 7 further steps (<= 8 steps in total).
*Proof.* G = 2 forces all d odd, so u = lcm(d^2) = 1 mod 8 and Delta_coll = u/2. With y = 2x, y_{n+1} = y_n + u_n = y_n + 1 mod 8 while G stays 2. Within 8 steps y = 0 mod 8 at an even y, i.e. x integer, 4 | x, which is G = 1 by T30. QED
**Open (K3.6).** G-collapse for every orbit. Obstruction to the same proof for G >= 3: u is a unit square mod 4G but not forced to be 1 mod 4G. Numerically all 290 orbits collapse (median 22 steps, max 239); G-unchanged growth events occur but only at G = 2 (153/2 -> 81).
