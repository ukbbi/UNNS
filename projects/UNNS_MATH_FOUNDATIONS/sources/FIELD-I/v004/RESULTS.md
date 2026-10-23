# FIELD-I v004 — Results

`python field4.py`: exit 0, ALL PASS, 0 FAIL (output/field4_output.txt). v003, v002, memo, manuscript untouched.

## J1 — Classification of rational three-route fibres (centerpiece)
- **Reduction (T22).** D(a/b) = {d | s, d≥2, d≡1 mod b} with s = square-root part of a. A fibre is determined by (s,b); the numerator's squarefree part t only scales all indices (h = t·H0). Squarefree scaling is a corollary: the v003 review's infinite family (20736/5, 145152/5, …) is the case t = 1, 7, 11, 13, …
- **Shape theorem (T24).** A three-route fibre (b ≥ 2) is exactly one of: chain {q,q²,q³} (non-rigid); Lambda {d1,d2,d1d2} (non-rigid); one comparable pair {q,q²,e} (**always rigid**); antichain with pairwise gcd ≥ 2, ≢ 1 mod b (rigid or not). The V shape is impossible. Integer fibres (b = 1) only have chain/Lambda: non-rigidity there is the same law.
- **Data.** 3,042 primitive configurations with λ ≤ 4000: Lambda 2,649; antichain 344 (70 rigid); one-pair 25 (all rigid); chain 24; no V. An independent (a,b) enumeration (b ≤ 40, a ≤ 60,000, 574 fibres) agrees with every law.
- **Infinite families (T25).** Scaled copies of every rigid configuration; and a primitive family b = 3, s = 22r, r prime ≡ 23 mod 63 (D = {22, 2r, 11r}, gcd values 3, 21, 9; rigid), proved.
- **Open.** Arithmetic criterion separating rigid from non-rigid antichains.

## J3 — Exact growth-time minimum
T26 gives a finite search for min over all d ∉ D of K_d. On 1,244 events the exact minimum improves the v003 truncated one in only 2; T = exact bound in 202.

## J2 — Growth of R
Proved: G(x_n) non-increasing, d_min ≤ R+2, hence R(x_n) ≳ (3n/G0)^{1/3} (T27, 726 checks). The sampled orbits grow far faster; the true rate is open.

## J4 — Collective versus route-aware
Fibre monotonicity D(x_n) ⊆ D(x_{n+1}) is a law of the collective branch; along route-aware pair orbits R is not monotone (x=36, pair (2,3): R = 3,3,3,5,3,3,3,5; decreases somewhere in 118/118 sampled pair orbits). This does not select C; it identifies a structural difference between the two branches.

## Status
Proved and checked: T22–T28. Data: shape counts, improvement rates. Open: antichain rigidity criterion, growth rate, whether every d ≥ 2 enters D(x_n).
