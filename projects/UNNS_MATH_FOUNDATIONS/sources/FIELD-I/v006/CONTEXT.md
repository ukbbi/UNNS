# CONTEXT — FIELD-I v006

## Background

Original 2017 UNNS fixed-nest S_N(M)=M(N+1)^2/N. Rational occurrences x=a/b (coprime) have D(x)={d>=2:d²|a,d≡1 mod b}. The G1–G3 grammar explicitly allows choosing the collective first-rendezvous value map C(x)=x+L(x)²/G(x), L=lcm D, G=gcd(d-1). This interaction is an experimental choice, not forced by the founding nest rule.

Versions 002–005 and grammar memo unchanged. v003 proved R(C^n(x))→∞; v005 disproved universal reachability for every orbit and established a G=1 absorbing regime with an eventual t-cycle 1→2→3→1.

## v006 proofs

- For unchanged D with G=g>1 and L fixed, y=gx satisfies y+=L². A modular inverse forces x into 4ℤ within ≤4g (L odd) or ≤g (L even); so D must grow within that time.
- G=2 collapses in ≤7 steps (mod 8).
- G=3 collapses in ≤2 steps (mod 3 on y/4).
- G=6 collapses in ≤29 steps (mod 24, with possible descent to 2/3).
- After G=1 and t∈{1,2,3}, x_(n+3)=4x_n, gamma repeats 1,2,3, R grows by tau(odd_part(s)) every third step.
- Exact G=1 reach-set count and correction: v005 T33 zero-density claim only proved for G=1, but infinite omission of moduli holds for all orbits.

## Open

Does G always reach1? Proofs eliminate stable G=2,3,6, but other G possible under current bounds. Does a useful invariant govern growth events preserving G? Does a non-collapsing infinite orbit exist? No physical claim.

## Workflow

Use `python field6.py` in `FIELD-I/v006`, then optionally `RUN_TESTS.bat`. Do not overwrite v002–v005. Keep GitHub unchanged. Primary next task: classify G-preserving fibre-growth transitions, preferably symbolically; report DATA vs theorems distinctly.
