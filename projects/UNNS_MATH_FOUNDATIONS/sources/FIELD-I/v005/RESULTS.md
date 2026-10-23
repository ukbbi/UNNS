# FIELD-I v005 — Results: Collective Orbit Universality

field5.py: 20 PASS, 2 DATA, 2 OPEN, 0 FAIL. Predecessors re-run unchanged: field2, g_checks, field3, field4 all PASS.

## Primary answer
**No collective orbit is universal.** Every orbit omits infinitely many nest moduli (T33), regardless of the open G-collapse question.
- If G_inf > 1 the orbit never reaches 2 or any d not = 1 mod G_inf.
- If G_inf = 1 (reached by all 290 sampled orbits) the orbit is eventually in regime I (x integer, 4|x), where Delta_coll = s^2 and (s,t) -> (s*sigma, sqf(t+1)); t falls into the cycle 1 -> 2 -> 3 -> 1 and s only doubles every 3 steps. The reach set is {d | s_N 2^k}: every odd prime not dividing s_N is never reached. Counting function O(log X).
- The orbit of 4 (4, 8, 12, 16, 32, 48, 64, ...) reaches only powers of 2.

Mapped onto the v004-review table: outcome (i) is false for all orbits; (iii) — "G -> 1 but moduli remain absent" — is what happens; (ii) is not excluded by theorem but G = 2 is (T34); (iv) applies only to G-collapse.

## What grows, and how
Collective multiplicity R(x_n) -> infinity (v004) but in regime I it is only linear: R = tau(s_n) - 1, +1 exponent of 2 per three steps. Diversity is unbounded in number, bounded in arithmetic content.

## J1 closure (T29)
Rigid <=> the three signatures (L_ij, g_ij) are pairwise distinct, because gcd(g,L)=1 makes g/L^2 reduced. Reproduced: antichains with 3/2/1 distinct LCMs: rigid 47/15/8, non-rigid 0/88/186 (70/274); signature rule == direct rational rigidity on all 3042 rational primitive fibres and 1955 integer three-route fibres. Correction noted: the v004 output has 12 PASS rows.

## Data
- 290 seed orbits (x = M d^2/N, plus 8 denominators 2..12), <=250 steps: all reach G = 1; median 22 steps, max 239 (seed 3721/60). Pre-collapse steps: 11712 without D-growth, 369 growth with G lowered, 1 growth with G unchanged (153/2 -> 81, G 2 -> 2).
- Theorem U exclusion check (K3.5b): for all 290 collapsed orbits the smallest odd prime not dividing s_N never appears in 70 further steps.

## Open
- **G-collapse (K3.6).** Proved for G = 2 (<= 7 steps); general G open. Not proved that no orbit stalls above G = 1; no counter-example found.
- **K3.7.** How large the odd part of s_N is, and which seeds end with only powers of 2.

## Caveats
A larger search (20000 steps, 2400 seeds) was started and stopped before producing output; it is not part of the evidence. All numerical claims above are from field5.py, K3 samples are finite and not a proof of G-collapse.
