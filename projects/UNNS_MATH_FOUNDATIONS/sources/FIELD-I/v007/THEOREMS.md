# FIELD-I v007 — Theorems (T35–T41). Continues v006 numbering (L1–L6) and v005 (T29–T34).

Notation: x = a/b reduced, D = D(x) nonempty, g = G(x) = gcd{d-1 : d in D}, L = lcm D, y = g x in Z (b | g), Y = y + L^2, x' = C(x) = Y/g. Recall (v005 T30–T31): D(x) subset D(x'), G(x') | g, and G(x)=1 iff x is an integer divisible by 4.

## T35 (Transition criterion; reviewer's criterion, proved)
For d >= 2:  d in D(x')  <=>  d^2 | Y  and  (g / gcd(g, d-1)) | (Y / d^2).
*Proof.* d in D(x') iff x' = M d^2/(d-1) with M a positive integer, i.e. M = Y(d-1)/(g d^2) in Z>0 (this is the occurrence form of D; K8.2 checks it against the a',b' form). Since gcd(d^2, d-1)=1, g d^2 | Y(d-1) forces d^2 | Y; then it reads g | (Y/d^2)(d-1), i.e. g/gcd(g,d-1) | Y/d^2. Converse is the same chain. QED
**Corollary T35a (transition identity).** G(x') = gcd(g, {d-1 : d in D(x') \ D(x)}) (gcd with the empty set is g). Hence three event classes: *none* (D'=D); *preserving* (D' strictly larger, every new d = 1 mod g, G'=g); *reducing* (some new d != 1 mod g, G'<g).
**Corollary T35b.** For d = 1 (mod g) the second condition is vacuous: preserving growth <=> a new d = 1 (mod g) with d^2 | y + L^2 and d not in D(x).

## T36 (Anatomy of a preserving event)
Let x -> x' be a preserving event with new set N = D(x') \ D(x). Then
 (a) every d in N is coprime to g;
 (b) no d in N divides L; hence every d in N contains a *fresh prime* (q not dividing L) or a *carried prime power* (v_q(d) > v_q(L) > 0);
 (c) fresh prime q: q does not divide y and q^2 | y + L^2, i.e. -y is a nonzero square modulo q^2; moreover q does not divide g;
 (d) carried prime q, l = v_q(L): v_q(y) = 2l exactly and q | y/q^(2l) + (L/q^l)^2;
 (e) N is closed under divisors: if d in N, e | d, e >= 2, e = 1 mod g, then e in N or e in D(x).
*Proof.* (a) d = 1 mod g. (b) For d0 in D, d0^2 | a and gcd(d0,g)... for every prime q, v_q(y) >= 2 v_q(d0), so v_q(y) >= 2 v_q(L). If d | L and d = 1 mod g then d^2 | y, and since gcd(d,g)=1, d^2 | a; d = 1 mod g gives d = 1 mod b, so d in D(x), contradicting newness. (c) q^2 | Y by T35 and q not| L gives q not| L^2, so q not| y. (d) v_q(Y) > 2l is needed for v_q(d) > l; since v_q(y) >= 2l = v_q(L^2), v_q(Y) > 2l forces v_q(y) = 2l and the q-free parts to cancel mod q. (e) e^2 | d^2 | Y and e = 1 mod g, T35. QED
**Reading.** A preserving event is *never* an internal rearrangement of the current fibre: it must introduce a new prime (an arithmetic coincidence y = -L^2 mod q^2) or push the exponent of an existing prime up (a 'carry', which is automatic for q = 2 in the family of T38).

## T37 (Plateau escape; v006 L1, used below)
If D is unchanged for k steps, y_k = y_0 + k L^2; with L odd the least positive k with y_k = 0 mod 4g is <= 4g, with L even <= g. Hence between two growth events a G>1 orbit spends <= 4g (L odd) or <= g (L even) steps, so a persistent orbit has infinitely many growth events, all preserving after some time.

## T38 (Persistent regime P_g — the counterexample)
Let g >= 5 with gcd(g,6)=1, and s = 2^k m with k >= 1, m odd, gcd(m,g)=1. Assume
 (H1) the residues mod g of the divisors of m contain the subgroup <2> of (Z/g)*;
 (H2) every prime power q^e || m divides some divisor d of 2^k m with d = 1 mod g;
 (H3) gcd{(d-1)/g : d | s, d >= 2, d = 1 mod g} = 1.
Put x_0 = s^2 t/g with t in {1,2,3}. Then for the collective orbit x_{n+1}=C(x_n), with (s_0,t_0)=(s,t) and
 s_{n+1} = s_n * sigma_n, t_{n+1} = squarefree part of t_n+1  (sigma_n^2 || t_n+1, i.e. sigma = 2 exactly when t_n = 3, else 1):
 (i) x_n = s_n^2 t_n/g is in lowest terms, t_n in {1,2,3};
 (ii) D(x_n) = {d | s_n : d >= 2, d = 1 mod g}, lcm D(x_n) = s_n, G(x_n) = g;
 (iii) x_{n+3} = 4 x_n, and G(x_n)=g for ALL n: the orbit never reaches G=1.
*Proof.* Induction on n. Suppose (i) with 2^{k_n} || s_n, k_n >= k, odd part m (unchanged: sigma in {1,2}). Since t_n squarefree, d^2 | s_n^2 t_n iff d | s_n; gcd(x_n numerator, g)=1 (gcd(s,g)=gcd(t,g)=1), b_n = g, so D(x_n) is as stated. lcm D = s_n: for 2^{k_n}: by (H1) pick u | m with u = 2^{-k_n} mod g, then d = 2^{k_n} u is in D; for q^e || m: (H2). G: g | G because every d = 1 mod g; G(x_n) | G(x_0) (T31); and G(x_0) = g by (H3). Hence Delta_coll = L^2/G = s_n^2/g (already reduced, T30), x_{n+1} = s_n^2 (t_n+1)/g = s_{n+1}^2 t_{n+1}/g, and t_{n+1} in {2,3,1}, coprime to g. QED
**Proposition T38a (existence for every such g).** Let q be the least odd prime with q = 2 mod g (Dirichlet), o = ord_g(2), g+1 = 2^v w with w odd, m = w q^o, k = max(v,1). Then (H1)-(H3) hold. *Proof.* q does not divide g+1 (a prime divisor of g+1 that is = 2 mod g is 2 or >= g+2), so gcd(m,g)=1. (H1): the divisors q^i are 2^i mod g. (H2): q^o = 2^o = 1; every prime power of w divides d = g+1 | s, d = 1 mod g. (H3): d = g+1 has (d-1)/g = 1. QED
*Instances.* g = 5 (s=504=2^3*63, also the natural seed 45828/5), 7, 11, 13, 17, 19, 23, 25, 29, 35, 49, 55, 65, 77 (K10.3, direct forward iteration).

## T39 (Universal G-collapse is false)
There are collective orbits with G(x_n) = g > 1 for every n, for every g >= 5 coprime to 6 (T38, T38a). Consequently the statement 'G_n > 1 implies G_k < G_n for some k > n' is false, and the conjecture K3.6 of v005 and the open problem L7.OPEN1 of v006 are settled in the negative. The modular exclusions (G = 2, 3, 6) remain the only proved collapses; they are consistent: P_g needs gcd(g,6)=1 because t must stay in {1,2,3} coprime to the denominator.
**Why random sweeps missed it.** Natural seeds with G=5 persist rarely (10 of 557 for a<25000, K10.5) and no other g appeared; v005's 290 seeds contained none.

## T40 (Reach set and growth in P_g)
In P_g the reach set is U = {d >= 2 : d | s_N 2^k for some k, d = 1 mod g} (N = 0 when the seed is already in the family), so U contains no multiple of g, none of 2,3,...,g, nor any modulus with an odd prime outside the odd part of s; its counting function is O(log X) (density 0), R(x_n) = #{d | s_n, d>=2, d = 1 mod g} grows linearly, +(number of divisors of m in the right classes) per three steps. Non-universality (v005 T33) is therefore verified for G_inf=g>1 without appealing to the weaker density bound of v006 L5.

## T41 (status of other g)
G=2,3,6 cannot be G_inf (v005 T34, v006 L2). P_g exists for gcd(g,6)=1, g >= 5. For 2|g or 3|g (g=4, 8, 9, 10, 12, ...) nothing is proved: L is odd or coprime to 3, y mod 4g advances by unit squares that are not forced to be 1, the t-cycle meets the denominator, and growth events exist (K8.4: G=4 and G=12 show preserving steps). **OPEN (K10.6).**
