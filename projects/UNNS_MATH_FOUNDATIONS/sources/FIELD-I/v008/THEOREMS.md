# FIELD-I v008 — Theorems (T42–T48). Continues v007 (T35–T41).

Notation: x=a/b reduced, D=D(x), g=G(x), L=lcm D, y=gx (integer), x'=C(x)=(y+L^2)/g. A *persistent* orbit has G(x_n)=g>1 for n>=n0 (by v005 T31, G_inf is attained, so 'G_inf=g' means persistent from some n0). All growth events after n0 are then G-preserving (T35a).

## T42 (Elementary construction; strengthens v007 T38a — Dirichlet not needed)
Let g>=5, gcd(g,6)=1, o=ord_g(2), s=(g+1)(g+2)^o, x0=s^2/g. Then x_n=s_n^2 t_n/g with t_n in {1,2,3}, G(x_n)=g and x_{n+3}=4x_n for all n.
*Proof.* Put k=v2(g+1)>=1, m=s/2^k=odd(g+1)(g+2)^o; m is odd, gcd(m,g)=1 because g is odd and gcd(g+1,g)=gcd(g+2,g)=gcd(2,g)=1. Verify the hypotheses of T38.
(H1) the divisors (g+2)^j of m satisfy (g+2)^j = 2^j (mod g), so their residues contain <2>.
(H2) a prime power q^e || m divides either g+1 or (g+2)^o (coprime): in the first case it divides d=g+1 | s, d=1 (mod g); in the second it divides d=(g+2)^o = 2^o = 1 (mod g). For the power of 2: 2^{k'}(g+2)^j = 2^{k'+j}=1 (mod g) for j = -k' mod o.
(H3) d=g+1 is in D(x0), (d-1)/g=1, so gcd{(d-1)/g}=1.
T38 gives the conclusions. QED
(Observation: s = 1 (mod g), because (g+1) = 1 and (g+2)^o = 2^o = 1.) Verified: hypotheses separately for 42 values of g, direct orbits for g <= 77 (M1.1–M1.3).

## T43 (Periodic increment of the fibre size)
In any orbit satisfying T38 (or T46 below), with s_n=2^{k_n}m (m odd, fixed), o=ord_g(2), A_g(m)=#{a | m : a mod g in <2>}:
 R(x_n) = #{(a,j) : a | m, 0<=j<=k_n, 2^j a = 1 (mod g)} - 1,   k_{n+3o}=k_n+o,   R(x_{n+3o}) - R(x_n) = A_g(m)  for every n.
*Proof.* D(x_n)={d | s_n, d>=2, d=1 mod g} and d=2^j a is a unique pair (a odd | m, j<=k_n); minus 1 removes d=1. The step t:1->2->3->1 (any phase) multiplies s by exactly 2 per three steps, so k_{n+3o}=k_n+o. The new pairs are those with j in (k_n,k_n+o]. Because 2^j mod g has exact period o, as j runs over o consecutive values 2^j meets every element of <2> exactly once; hence for each a with a mod g in <2> exactly one j gives 2^j a = 1, and for other a none. QED
*Tests.* 12 values of g (incl. 13,19,25,55 and P* g=15), each over >= 2 complete 3o-periods (comparisons: 27–171 per g, listed in M2.1), plus the counting identity against brute-force divisor enumeration (M2.3).

## T44 (The gamma-framework; valid for every orbit)
Let D(x) nonempty, g=G(x), L, y=gx. Then
 (a) L^2 | y; gamma:=y/L^2 is a positive integer, x=gamma L^2/g;
 (b) b | g and gcd(L,g)=1; x is an integer divisible by 4 (equivalently G=1, v005 T30) iff 4g | gamma L^2, i.e. iff 4g | gamma (L odd) or g | gamma (L even, g odd);
 (c) if the step x->x' is G-preserving and r=L'/L (an integer, L | L' by D subset D'), then gamma'=(gamma+1)/r^2; on a plateau (D'=D) gamma'=gamma+1;
 (d) (congruence advance) if g is even then r is odd and gamma' = gamma+1 (mod 8); if 3 | g and 3 does not divide r then gamma' = gamma+1 (mod 3); if 6 | g, gamma' = gamma+1 (mod 24);
 (e) the denominator of x is b = g/gcd(g,gamma), so gamma = 0 (mod g) iff x is an integer.
*Proof.* (a) For d in D, d^2 | a and gcd(d,g)=1 (d=1 mod g), y = a(g/b), so d^2 | y; take lcm. (b) as stated, using gcd(L^2,4g)=1 or the factor 4. (c) y'=y+L^2 for G'=g; gamma'=y'/L'^2=(y+L^2)/L'^2=(gamma+1)L^2/L'^2. (d) r^2=1 (mod 8) for odd r, r^2=1 (mod 3) for 3 not| r. If g is even every d is odd so r is odd; if 6 | g every prime of r is coprime to 6. (e) L^2 is a unit mod g. QED
Verified on 850+ preserving steps and 1013 states (M3.1–M3.3).

## T45 (Theorem E: G_inf cannot divide 24) — answers K10 for g=4 and 12
If g>1 divides 24 then no collective orbit is persistent at G=g. In particular G_inf is not in {2,3,4,6,8,12,24}.
*Proof.* g=3: L is even (otherwise all d-1 even), collapse iff 3 | gamma; by T44(d) gamma mod 3 advances by 1 each step (every prime of r is coprime to 3), so 3 | gamma within 3 steps — contradiction. Let g be even (g | 24, g != 3). L is odd, collapse modulus M=4g, and every prime of r is coprime to g.
 Step 1 (prime classes). Let n>n0 and q a prime with q | L_n. By T44(d), gamma advances by 1 mod 8 (g | 8) or mod 24 (g | 24, 3 not| r), so some m>=n has g | gamma_m, so x_m is an integer (T44(e)) and b_m=1. q | d0 for some d0 in D(x_m) (D is monotone), so q^2 | a_m and, as b_m=1, q in D(x_m). Then G(x_m)=g divides q-1: q = 1 (mod g).
 Step 2 (growth is large). Every growth ratio r_n has all prime factors = 1 (mod g), so r_n >= g+1 and r_n^2 >= (g+1)^2 > 4g = M.
 Step 3 (descent). Plateaus have fewer than M steps (M consecutive integers contain a multiple of M, i.e. collapse); so there are infinitely many growth events. Let a_k be gamma right after the k-th growth. The run a_k, a_k+1, ..., a_k+j avoids multiples of M, so j <= M-2 and the next growth takes gamma_before <= a_k+M-2 to a_{k+1}=(gamma_before+1)/r^2 <= (a_k+M-1)/(g+1)^2. Since (g+1)^2-1 > M-1, this is < a_k for every a_k>=1. A strictly decreasing infinite sequence of positive integers does not exist. QED
(Consistency: reproves v005 T34 (g=2), v006 L2 (g=3,6).) For g=4 the mechanism is: every prime of L must be 1 mod 4 (so r>=5, 25>16); for g=12: every prime of L is 1 mod 12.
*Remarks on the method.* The mod-8 advance is the reason 'unit squares' (L^2 = 1 mod 8) never made the modular escape work for g=4 directly; the descent argument replaces it.

## T46 (Theorem P*: persistent regimes with gcd(g,6)>1)
Let g>=5 be odd (3 | g allowed), s=2^k m with m odd, gcd(m,g)=1, o=ord_g(2). Assume H1, H2, H3 of T38 and
 (H4) for t in {1,2,3} and b_t=g/gcd(g,t): every divisor d=2^j a (a | m, j>=0) with d = 1 (mod b_t) satisfies d = 1 (mod g).
Then for x0=s^2/g the conclusions of T38 hold: x_n=s_n^2 t_n/g, G(x_n)=g, D(x_n)={d | s_n, d>=2, d=1 (mod g)}, lcm D=s_n, x_{n+3}=4x_n; T43 holds.
*Proof.* As T38; the only new point: x_n=s_n^2 t_n/g reduced has denominator b_t=g/gcd(g,t) (gcd(s,g)=1, t squarefree), so D(x_n)={d | s_n : d = 1 (mod b_t)}, which equals {d | s_n : d=1 (mod g)} by H4 (residues of d depend only on j mod o). G(x_n) | G(x_0)=g and b | G give G=g; then Delta_coll=s_n^2/g. QED
Instances (direct iteration, M3.7, M3.9): g=15 (s = 16*17^4 = (g+1)(g+2)^o, and s=4*17*19), 39, 51, 57, 87 by the elementary form. **Hence G_inf>1 does occur with gcd(G_inf,6)=3, and the statement of v007 T39/T41 that P needs gcd(g,6)=1 was too strong (erratum).**
*Why 3 | g works but 2 | g does not.* For g=15, gamma=3 gives b=5, and the divisors of s all lie in <2> mod 15, on which reduction mod 5 is injective (ord_5(2)=ord_15(2)=4), so no new d appears. For even g, 2-power divisors are never in D (d=1 mod g forces d odd), so L != s and the (s,t) dynamics breaks.

## T47 (Persistent orbits live in a bounded gamma-window)
In a persistent orbit with collapse modulus M, gamma_n <= 2M for all large n.
*Proof.* Plateaus last at most M-1 steps (else gamma = 0 mod M), r>=2 at every growth, so a_{k+1} <= (a_k+M-1)/4, hence limsup a_k <= (M-1)/3 and gamma_n <= a_k + M-1 <= 2M eventually. QED
*Meaning.* x_n = gamma_n L_n^2/g is, up to a bounded factor, the square of the lcm. A persistent orbit is a finite-state gamma-process driven by arithmetic coincidences. In every known regime the process is the cycle 1,2,3.

## T48 (Precise form of the scaling question)
M4a: for every realised x0 there is n0 with x_{n+3}=4x_n (n>=n0). M4b: every orbit is eventually x=s^2 t/g with t in {1,2,3}. PROVED: G_inf=1 (v005 T32); P_g and P*_g (T38, T42, T46). Equivalent reformulation via T44: x_{n+3}=4x_n iff gamma_{n+3}=gamma_n and L_{n+3}=2L_n.
A counterexample to M4a would be a persistent orbit with a gamma-cycle other than 1,2,3. The cycle 1,2,3 arises because gamma+1 = 4 forces the carry r=2; a different cycle needs a prime square dividing gamma+1 which is *not* absorbed (not a divisor = 1 mod g). Nothing here excludes it. OPEN.
