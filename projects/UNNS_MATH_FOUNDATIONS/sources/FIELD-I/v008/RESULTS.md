# FIELD-I v008 — Results: Persistent-Regime Classification

field8.py: 14 PASS, 4 DATA, 3 OPEN, 0 FAIL (`output/field8_output.txt`). Predecessors v002–v007 rerun unchanged; all earlier files byte-identical.

## Headline
1. **Which G can persist is now largely classified** (table below). G = 4 and G = 12 cannot persist (T45), nor G = 8 and 24; and **G_inf > 1 does occur with gcd(G_inf, 6) > 1**: G = 15, 39, 51, 57, 87 (T46, direct orbits). This answers the decisive question of the v007 review: yes.
2. A **gamma-framework** (T44) governs every orbit: gamma = gL^-2 y is an integer, gamma' = (gamma+1)/r^2 at a preserving step (r = L'/L), and gamma advances by exactly 1 modulo 8 (g even), 3 (3 | g) or 24 (6 | g). The old modular escape arguments (G=2,3,6) and the new G = 4, 12 are all instances.
3. **Elementary construction** s = (g+1)(g+2)^o (T42): no Dirichlet; **periodic increment law** R(x_{n+3o}) = R(x_n) + A_g(m) (T43), proved and tested non-vacuously over >= 2 complete 3o-periods for 12 values of g.
4. **Scaling x_{n+3} = 4x_n** holds in every regime known; it is not proved for every orbit (M4a OPEN). Natural seeds: 400 of 400 reach it within 300 steps (median entry step 4, max 114), none ends with G > 1.

## Classification of the possible limits G_inf (status)
| G_inf | status | where |
|---|---|---|
| 1 | scaling regime, proved | v005 T32 |
| g > 1, g divides 24 (2,3,4,6,8,12,24) | cannot persist, PROVED | T45 (new for 4, 8, 12, 24) |
| g >= 5, gcd(g,6) = 1 | persists, PROVED (explicit orbits) | T38, T42 |
| g odd, 3 divides g, hypotheses H1–H4 hold | persists, PROVED; instances 15, 39, 51, 57, 87 | T46 (new) |
| odd 3 \| g without an instance found (21, 27, 33, 45, 63, 69, 75, 93, 99 in the bounded search) | OPEN (search negative is not a proof) | M3.8 |
| even g > 24 not dividing 24 (10, 16, 20, 28, ...) | OPEN; natural seeds with g = 20 collapsed after 64 steps | M3.10 |

## M1 — elementary construction (T42)
s = (g+1)(g+2)^o, x0 = s^2/g. The lemma (s = 1 mod g, coprimality) is checked for all 49 g in [5,150) with gcd(g,6)=1; the hypotheses H1–H3 are verified separately from the orbit for the 42 of them with g <= 130; direct orbits for every g <= 77 coprime to 6 (G = g and x_(n+3) = 4 x_n at all 30 steps). v007's Dirichlet-based T38a stays unchanged and valid; T42 strengthens it.

## M2 — periodic increment (T43)
Rows (g, o, A_g, comparisons, complete 3o-periods): (5,4,10,27,2) (7,3,4,21,2) (11,10,22,63,2) (13,12,338,75,2) (15,4,5,27,2) (17,8,18,51,2) (19,18,722,111,2) (23,11,24,69,2) (25,20,122,123,2) (29,28,116,171,2) (35,12,26,75,2) (55,20,442,123,2); zero violations of R- and k-increments; the guard fails if fewer than 6o comparisons are made. The law gives, e.g., +4 every 9 steps for g=7 and +5 every 12 steps for g=15.

## M3 — G = 4, 12 (T45) and beyond
Mechanism for G=4: once x is an integer (gamma = 0 mod 4, forced by the mod-8 advance) every prime of L is in D, hence = 1 mod 4, so growth ratios satisfy r >= 5 and 25 > M = 16; gamma then strictly decreases at each growth, impossible forever. For G=12 the same with primes = 1 mod 12 (r >= 13, 169 > 48). Natural data (M3.6): longest stay 27 (g=4), 3 (g=8), 60 (g=12), 5 (g=24) steps, all collapse, consistent with the theorem but not used as evidence.
The failed expectation: v007 K10.6 said the P-construction cannot apply when gcd(g,6)>1. It does for odd g with 3 | g when relaxed denominators (gamma = 3) admit no extra divisors (H4).

## M4 — eventual scaling
Reformulated (T44): x_{n+3} = 4x_n iff gamma_{n+3} = gamma_n and L_{n+3} = 2 L_n. A persistent orbit has gamma <= 2M eventually (T47), so it is a finite-state process; the cycle (1,2,3) is forced whenever the square dividing gamma+1 is absorbed. A counterexample needs an unabsorbed square. OPEN, with sharp conditions.

## Erratum (historical record kept)
- v007 T39 and T41/K10.6 say P_g needs gcd(g,6)=1. Superseded by T46: odd g with 3 | g can persist. The v007 theorem itself (existence for gcd(g,6)=1) is unaffected.
- The v007 'asymptotic-form conjecture' K11.3 is now split into M4a/M4b.

## Caveats
Theorem E is a proof (T45), tested only through its ingredients (M3.1–M3.5). T46 is hypothesis-based (H1–H4 are finite checks; instances verified by direct orbits, 120 steps). The classification of even g > 24 and of the remaining odd multiples of 3 is open. Nothing here selects the collective operator as the rule of UNNS.
