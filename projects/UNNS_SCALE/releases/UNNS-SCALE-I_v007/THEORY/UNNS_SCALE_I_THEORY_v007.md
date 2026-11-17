# UNNS-SCALE-I v007 — Algebraic Route Construction (constant-ratio families)

Labels: PROVED / CERTIFIED (finite exact check) / EXPERIMENTAL / OPEN. v005 Part A is frozen; v006 untouched. **D_{10^6} remains OPEN (4 <= D <= 6).**

## 1. Setting and notation
B = 10^6 (statements hold for any B with the stated divisibility). Four-step route of type (+-|+-): forward label N | Bn, backward label q (q^2 | x1), meeting a route from B(n+1) of the same type.
Write a label as N = c v with c | B, v | n (every divisor of Bn has this form); put v' = n/v. Likewise M = d w, d | B, w | n+1, w' = (n+1)/w. Let u = cv+1, u' = dw+1.

## 2. The reviewer's divisor-generated proposition — PROVED, CERTIFIED
Let 2h | B, n ≡ 1 (mod 2h+1), n >= 2h+2, s = 2h+1. Then d(Bn, B(n+1)) <= 4 through the midpoint B s (n-1), by
Bn --(N=2hn)--> (B/2h)(2hn+1)^2 --(q=(2hn+1)/s)--> B s (n-1) and B(n+1) --(M=h(n+1))--> (B/h)(h(n+1)+1)^2 --(r=(h(n+1)+1)/s)--> B s (n-1).
(Substitution: q-1 = 2h(n-1)/s, r-1 = h(n-1)/s.) v007 re-verifies it by direct arithmetic and finds that it covers exactly 111 of the 614 exceptional v005 values. It is the case v'=w'=1, c=2h, d=h, rho=2h+1 of Theorem A'' below.

## 3. Theorem A'' (constant-ratio route families) — PROVED
Shape (v', w', c, d), gcd(v',w') = 1, c, d | B, Delta = c w' - d v' > 0. Put rho = 1 + cd/Delta = P/Q in lowest terms (P > Q >= 1). Admissible if gcd(c,P) = gcd(d,P) = 1, Q^2 | (B/c) v' and Q^2 | (B/d) w'.
Class: v' | n, w' | n+1, P | Q u, P | Q u'. For n in the class with q = Qu/P >= 2 and r = Qu'/P >= 2:
 Bn --(N = c n/v')--> (B/c) v' u^2 --(q)--> z,   B(n+1) --(M = d(n+1)/w')--> (B/d) w' u'^2 --(r)--> z',
 z = (B/c)(v'/Q^2) P (Q u - P),  z' = (B/d)(w'/Q^2) P (Q u' - P),  and z = z' . Hence d_B(n) <= 4.
Proof. x1 = (B/c) v' u^2, q^2 = Q^2 u^2/P^2, so x1/q^2 = (B/c) v' P^2/Q^2 is an integer iff Q^2 | (B/c)v'. Then z = x1 (q-1)/q^2 = (B/c)(v'/Q^2) P (Qu-P). Substituting u = c n/v' + 1 gives z = (BP/Q) n + (B/c)(v' P (Q-P)/Q^2); the same computation gives z' = (BP/Q)(n+1) + (B/d)(w' P (Q-P)/Q^2). Equality of the constant terms is (Q-P)(v'/c - w'/d) = Q, i.e. rho - 1 = cd/(c w' - d v'). ∎
Classification (PROVED): in the linear-label regime (labels N = c v, M = d w with v' = n/v and w' = (n+1)/w fixed, backward labels q = Qu/P, r = Q'u'/P'), z and z' are affine in n with slopes BP/Q and BP'/Q'; a shape that works for infinitely many n must have P/Q = P'/Q', and the constant terms then force rho = 1 + cd/Delta. With unequal ratios the shape works for at most one n. So Theorem A'' lists all infinite families of this regime.
Instances for B = 10^6: 108 shapes with v'=w'=1, 7,907 shapes with v',w' <= 12.

## 4. Coverage of the exceptional v005 values — CERTIFIED
Every one of the 614 exceptional n of v005 (the ones not reached by v005's finite-support identities) has an explicit closed-form four-step route from Theorem A'': 481 with v',w' <= 3, 613 with v',w' <= 12, 614 with v',w' <= 40. Each route is re-verified edge by edge by integer arithmetic. (Proposition B, the sub-regime q | u, covers 613 of 614; the single miss, 445499, needs Q > 1.) This explains the 614 by one parametrised principle rather than by 614 separate searches. It does not by itself prove anything about n outside the window.
Window n <= 2·10^6, fraction of n lying in some admissible class with v',w' <= K (EXPERIMENTAL, exact count): K=1 0.7075, K=2 0.7972, K=3 0.9770, K=4 0.9813, K=6 0.9867, K=8 0.9910, K=12 0.9948 (uncovered: 585,051; 405,526; 46,086; 37,485; 26,668; 18,059; 10,497). Among n with 720 | n+1: 0.4544, 0.4544, 0.8776, 0.8776, 0.9413, 0.9647, 0.9993.

## 5. Obstruction to finite covering by these families — PROVED
For any finite set F of admissible shapes put L = lcm over F of v'P. If L | n then n lies in no class of F: n/v' is a multiple of P, so P | Q(c n/v' + 1) would force P | Q, impossible since P > Q >= 1 and gcd(P,Q) = 1. Therefore **no finite set of constant-ratio families covers all n.** (Check: L has 107 digits for the v'=w'=1 shapes; n = L, 2L, 3L are covered by no shape.) The numerical coverage above can therefore approach 1 without ever reaching it.
Consequence for a universal proof: n with n/v' divisible by P for every small shape (very divisible n) must be routed by families whose parameters grow with n, for example N a bounded constant with q absorbing a square factor of n, or labels with v' proportional to n. These regimes are not classified here. We also have not tested n of that size (107 digits is beyond the exact complete-neighbourhood engine).

## 6. Status
- PROVED: Theorem A'' (and the reviewer's proposition as a special case), classification of infinite linear-regime families, non-covering obstruction.
- CERTIFIED: the 614 exceptional n all lie in A'' classes with v',w' <= 40.
- EXPERIMENTAL: window coverage table.
- OPEN: D_{10^6} in {4,5,6}; whether routes exist for the highly divisible residue (n multiple of L); the other 12 divisor scales of 10^6 from v006.
- Stopping rule: the coverage tables are recorded as data only; the new content is the classification and the obstruction, not the tables. Further enlarging K would add nothing mathematically and is not recommended.
- Gate 4 deferred; v001–v006 unchanged (hash-checked); no GitHub changes.
