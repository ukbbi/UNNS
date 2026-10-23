# CONTEXT — FIELD-I v009 (read this first when continuing)

## Where the project is
FIELD-I studies the fixed-nest rule: occurrence r=(M,N), d=N+1, v=M d²/N. The collective map C(x)=x+L²/G (L=lcm D(x), G=gcd{d−1}) is a **chosen** interaction (nonselection theorem, v002), not derived.
Invariants: G_n is non-increasing in divisibility (v005). G_∞=1 ⇒ regime I, x_{n+3}=4x_n. G_∞=g>1 ⇒ "persistent orbit", x=γL²/g (v008 T44).

## What v009 established (all in THEOREMS.md)
1. **T49 one-step law.** D(x')={d | L·sqrtpart(w/h) : d≥2, d≡1 mod g/h}, w=γ+1, h=gcd(g,w); persistent iff all such d ≡1 mod g; γ'=w/r², r=L'/L.
2. **T50 eight-step theorem (G=11)** proved by hand (x_{8k+j}=(j+1)S_k²/11, S_k=2²3^{3+k}5⁴, x_{n+8}=9x_n, R+2 per 8 steps).
3. **T51** finite-state closure: class = (γ, exponent classes mod ord_g(p)); a repeated class ⇒ periodic forever; therefore **every persistent orbit is eventually x_{n+P}=ρ²x_n**, and every orbit of C is (with v005 T32).
4. **T52 window**: odd g ⇒ 2|L and g∤γ+1; complete carries need M²<g (so a q-carry needs g>q²). Even g: 4g∤γ+1.
5. **T53 absorption criterion**: new part M(d); d available iff M(d)²|w; r=lcm of available M(d). Complete ⇒ gcd(g,w)=1.
6. **T54 completeness**: γ'≤γ_s/4+1 ⇒ after finitely many carries γ=1 and ALL later carries are complete (w=M², cycle length M²−1). Partial absorption = finite transient.
7. **T55 prime-power carries**: recurring carries are p^j (composite M never minimal once its primes are saturated). **T56 decoupled odometers**: carry = min_p p^{j_p}, j_p from Abs_p⊂Z/ord_g(p).
8. **T57 general q-carry theorem** (hand proof under finite hypotheses Q1–Q4): γ-cycle 1..q²−1, x_{n+q²−1}=q²x_n. Instances q=3 (g=11), 5 (g=31 and 71), 7 (g=367).
9. **T58 erratum**: v008 M4a, M4b FALSE; T48 equivalence corrected: x_{n+3}=4x_n ⇔ γ_{n+3}L_{n+3}²=4γ_nL_n² ⇔ γ_{n+3}=4γ_n/ρ², ρ=L_{n+3}/L_n.
10. Extra: persistent orbits with **even** g exist (g=68, direct verified), nonstandard mixed-carry cycles are explained by T56 (e.g. g=31: carries 2²,2²,2¹, P=33, ρ=32).

## Tools
- `field9.py`: residue machine (`mstep`, `minit`, `run_cycle`, `reduce_cycle`) + `direct_orbit` (independent). `machine_orbit(g,Eseed,γ0,N)`. `q_hyp(q,g)` builds a T57 seed.
- Seed format: `Eseed` = dict prime→exponent of an auxiliary L; `minit` renormalises to L=lcm D(x₀) and returns γ; `checkG=True` demands G(x₀)=g exactly.
- To explore: `FIELD9_QUICK=1 python field9.py` (~minutes); for a new g use `run_cycle(g,E,γ0,maxn)`; the class period can be much longer than the γ-period (q=7: 2928 = 61·48).

## Open items for v010 (suggested, in priority order)
- **O9.2** No eventual cycle with two active primes has been found; T56's multi-prime clause is proved but untested. Try combining two T57 templates (q and q') on the same g.
- **O9.1** Is (Q1)–(Q4) solvable for every prime q (Chebotarev/Kummer on a cyclic quotient)? A proof would give an infinite family of distinct carry sizes.
- Which g>1 admit persistent orbits at all? Known: g=11,13,17,… primes (many), composite odd g (15,39,51,57,87 via v008 P*), even g=68. Necessary: gcd(g, 24) conditions (v008 T45). Characterise via T52/T56 (the residue structure of (Z/g)* is the whole story).
- Distribution question: which carry word does a "natural" seed (e.g. x₀ = s²/g with s from the v007 construction, or random x₀) fall into? T54 says γ reaches 1; T56 says the rest is odometers. The initial prime support decides which odometers can run.
- Transients: bound the number of partial carries before γ=1 (T54 gives γ_s→γ_s/4+1 per carry, so ≤ log₄ γ₀+1 carries).
- Connect: M-carry cycles give x_{n+M²−1}=M²x_n; do these have a "physical" reading (multi-clock recurrence, v009 sibling documents in the project)? Not attempted here.

## Hazards (environment)
Never `pkill -f`/grep-kill a pattern that appears in the shell command itself (kills the shell). Pure-Python factoring (no sympy). Long foreground runs time out at ~600 s: run in the background and stream to a file.
