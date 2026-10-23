# FIELD-I v008 — Persistent-Regime Classification (SPEC)

Frozen: v002–v007 and the G1–G3 memo (byte-identical copies are in the zip). v008 adds `field8.py` (standalone; helpers copied from v005).

## Objects
Unchanged: x=a/b, D(x), g=G(x), L=lcm D, y=gx, collective map C. New in v008: the **gamma-integer** gamma(x)=y/L^2 (v003's gamma generalised to the G-aware setting), the ratio r=L'/L at a growth event, the collapse modulus M (4g if L odd, g if L even), persistent orbit = G(x_n)=g>1 for all n>=n0.

## Tracks
- **M1** elementary construction s=(g+1)(g+2)^o, x0=s^2/g, hypotheses of T38 verified separately (no Dirichlet).
- **M2** periodic-increment law R(x_{n+3o})-R(x_n)=A_g(m), non-vacuous tests (>= 2 complete 3o-periods, reported as counts, built to FAIL when fewer).
- **M3** G=4 and G=12 (and G with gcd(G,6)>1 in general): gamma-framework, descent theorem, extension P* with 3 | g.
- **M4** eventual scaling x_{n+3}=4x_n: exact statement, what is proved, data, open conditions.

## Verification design
Exact arithmetic. Orbits are produced by direct iteration of C via factorisation (Dx), never by the (s,t) recursion; the recursion is used only as the claim being tested. Hypotheses (H1)-(H4) are finite checks done separately from the orbit check. Adversarial tests: random integer states for the prime-class lemma (M3.4), nonvacuity guards (M2.2), natural-seed collapse data (M3.6).

## Run
`RUN_TESTS.bat` runs field2, g_checks, field3, field4, field5, field6, field7, field8. `FIELD8_QUICK=1` shrinks ranges.
