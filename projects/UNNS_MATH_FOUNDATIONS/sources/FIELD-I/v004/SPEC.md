# FIELD-I v004 — Rational Rigidity and Collective Growth Structure (SPEC)

v003 is preserved unchanged (also v002, the G1–G3 memo, manuscript v3, SELECT-I/II). Decision from the v003 review: centerpiece = classification of rational three-route fibres (J1); also J2 growth lower bound, J3 exact growth-time minimum, J4 collective-versus-route-aware comparison.
Status labels: proved / checked / data / open. C = collective map of v003 (G1-C + G2 j=1 + G3-V), an experimental grammar branch, not a derived law.

## Objects
Fibre of x=a/b: D(x) = {d>=2 : d^2|a, d=1 mod b}. Rendezvous weights of a triple T={d1,d2,d3}: w_ij = gcd(d_i-1,d_j-1)/lcm(d_i,d_j)^2, pair index h_ij = x*w_ij. **Rigid** (weighted rendezvous triangle has trivial automorphism group) iff the three w_ij are pairwise distinct.
Divisibility shape of T: chain, Lambda (d1|d3, d2|d3), V (d1|d2, d1|d3), one comparable pair, antichain.
Primitive configuration: (lambda, b) with lambda = lcm(D) and D = D(lambda, b).

## Tasks
J1 classify rational three-route fibres (reduction to (s,b), shape theorem, rigidity law, infinite families). J2 lower bound for R(x_n). J3 exact global minimum of K_d. J4 laws of the collective branch absent for route-aware interaction.

## Verifier
field4.py: exact arithmetic, independent enumerations (divisor-based primitive search vs direct (a,b) enumeration), PASS/FAIL/DATA/OPEN, exit 0 iff no FAIL, FIELD4_QUICK=1 for small bounds.
