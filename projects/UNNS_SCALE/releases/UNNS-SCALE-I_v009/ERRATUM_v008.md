# ERRATUM to UNNS-SCALE-I v008 (recorded in v009; v008 archive preserved unchanged)

Two mathematical corrections, both from external review, both verified numerically in v009 (`code/verify_all_v009.py`).

## E1. Constant-ratio shape = ONE residue class modulo P·v′·w′ (two congruences)
v008 THEORY §5 listed a single congruence and the period "lcm(v′P, w′)". Correct statement: a shape (v′,w′,c,d,P,Q) routes n iff
 v′ | n, w′ | n+1, **P | c·n/v′ + 1 and P | d·(n+1)/w′ + 1** (gcd(P,Q)=1; both are needed), and q=Q·u/P ≥ 2, r=Q·u′/P ≥ 2.
With gcd(v′,w′)=1 the first pair of conditions is n ≡ v′a₁ (mod v′P), n ≡ w′a₂−1 (mod w′P) (a₁ ≡ −c⁻¹, a₂ ≡ −d⁻¹ mod P; for P=1 just n≡0 mod v′, n≡−1 mod w′), consistent via CRT iff the gcd condition holds; the set is one class mod **lcm(v′P, w′P) = P·v′·w′**, for n ≥ n0 (q,r ≥ 2). Small n below n0 are exceptions handled separately.
Counterexample to the one-congruence form: (v′,w′,c,d)=(1,2,1,1), ρ=2, n=3: u=4≡0 but u′=3≢0 (mod 2), so r=3/2 — no route.

## E2. Converse of Theorem L′ needs B | Q²·a·N
v008 stated the integer system (S1),(S2) as equivalent to a route; the converse requires in addition that n = Q²aN/B be an integer.
Counterexample: N=M=1, (P,Q)=(2,3), (P′,Q′)=(1,2), a=600000, a′=1600000, B=10⁶: S2 (Q′²a′M−Q²aN=B) and S1 hold, but n=27/5.
The forward direction (route ⇒ system) is unaffected. Nothing else in v008 depended on the converse.
