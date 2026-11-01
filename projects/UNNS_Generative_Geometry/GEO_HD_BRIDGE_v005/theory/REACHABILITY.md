# A5-T1 / A5-T2' — Exact reachability decider, proper-divisor obstruction, family scans

Target question (inherited from v004 O4-1…O4-3): for an activation-family pair `x=P²/ℓ`, `y=(Pq)²/ℓ` (P=∏p_i, k primes, k|ℓ−1), is `y` on the FIELD-I orbit of `x`?

## Algorithm (FINITE-EXACT, `src/reachability.py::decide`)
Follow the orbit stage by stage with the stage sieve (FIRST_EVENT.md). Inside a stage the states are `x₀+jL²/G`, so landing on the target is the integrality of `(y−x₀)L⁻²G`, and the first event is read from linear congruences. Outcomes: REACHED(steps) / OVERSHOT / BLOCKED / D_EMPTY / STAGE_CAP.
BLOCKED uses **Lemma M**: `D` is monotone along an orbit, so if some state's `D` is not ⊆ `D(y)` then `y` is never reached. No step cap is needed. Exact, but not a proof of termination for every input (STAGE_CAP exists; it never occurred in the scans reported here).
`resolve_family` = `decide` + `line_scan` (fast scan of the family line `x_u=P²u/(P−1)`, u=m+j, for the first u with `D≠{P}`) + a bounded simulation fallback.

## Theorem A5-T1.1 (proper-divisor obstruction) — PROVED (sufficient condition for BLOCKED)
Let P=p₁⋯p_k (distinct primes), ℓ|P−1, N=P−1, m=N/ℓ. While `D={P}` the orbit is `x_u=P²u/N` (u=m+j). Then:
* for a proper divisor `1<d₀<P` of P: **d₀ ∈ D(x_u) ⇔ r(d₀) | u**, `r(d₀)=N/gcd(d₀−1,N)`.
* for an A4 candidate `d=p_iq`: it joins (at the earliest) at `u_i = least multiple of lcm(r_i, q^{2+v_q(N)}) above m` (Prop. A5-T2.4).
Put `u_f=min_{d₀}(least multiple of r(d₀) above m)` and `u_a=min_i u_i`. **If `u_f ≤ u_a` and `u_f < q²m` then `y` is not reachable.**
*Proof.* y has `D(y)={P}∪{p_iq}` (A4-T1). A proper divisor d₀ of P is not in it. Consider the orbit up to u=u_f (u_f<q²m, so y, which sits at u=q²m, has not been reached; the orbit is increasing). Either some event happened at u<u_f, or not. An event before u_f cannot consist of A4 candidates only (they join at ≥u_a≥u_f), so it contains an element outside D(y). If no event occurred before u_f, then at u_f the divisor d₀ joins (the equivalence above: `d₀²|P²u` holds because P is squarefree; `b | d₀−1` is `r(d₀)|u`), and it is outside D(y). In both cases some state has D⊄D(y), hence by Lemma M y is never reached. ∎
Proof of the equivalence: reduced denominator `b_u=N/gcd(u,N)`; `b_u|d₀−1 ⇔ N/g | gcd(d₀−1,N) ⇔ r(d₀)|g ⇔ r(d₀)|u` (r|N). ∎

*Audit (Z6, FINITE-EXACT):* on the 993-row v004 table the criterion flags 945 rows: 923 BLOCKED, 22 of the 24 step-capped cases (all later decided BLOCKED), **0 of the 40 REACHED**; independent simulation of flagged small blocked members meets a forbidden occurrence before y in every case (table: `results/OBSTRUCTION_TABLE.json`). The criterion is only sufficient: 6 BLOCKED rows are not flagged (other forbidden occurrences, e.g. the line_scan finds a non-divisor d).

## Resolution of the 24 step-capped v004 cases (B5-4) — FINITE-EXACT
All 24 re-decided exactly (`results/UNRESOLVED24.json`): **22 BLOCKED, 2 REACHED** — (k=3, ℓ=7, q=2, ps=(67,151,179), 45666 steps) and (151,179,193; 67756 steps). 0 OVERSHOT.

## Extended family scans (k=2) — FINITE-EXACT, `data/FAMILY_SCAN_k2_l3.json`, `…_l5.json`, `results/FAMILY_SCAN_SUMMARY.json`
Parameter ranges: primes p≡c (mod ℓ), p<2000, P≤300000, q prime ≡c⁻¹ (mod ℓ), q<90; no budget skips.
| family | pairs | proper-divisor blocked | other BLOCKED | REACHED | reached q |
|---|---|---|---|---|---|
| k=2, ℓ=3 | 52,997 | 51,373 | 493 | **1,131** | 2 (989), 5 (115), 11 (24), 17 (3) |
| k=2, ℓ=5 | 4,010 | 4,009 | 0 | **1** | 19 (ps=(89,1709), 2239 steps) |
Observations (finite data; **not** extrapolated):
* **COUNTEREXAMPLE to the v004 reading “reached members only occur for q∈{2,5}”**: q=11,17 (ℓ=3) and q=19 (ℓ=5) are reached. The v004 statement was a finite-sample artefact of a small table. (O4-3 is reformulated, not resolved.)
* The proper-divisor obstruction explains 96.9 % (ℓ=3) and 99.98 % (ℓ=5) of all pairs; the reached members are the ones for which the first event of the line is exactly an A4-type event.
* Event structure (ℓ=3): all 989 reached members with q=2 arrive after a single event stage; all 142 with q∈{5,11,17} have a second event one step before arrival (the final A4-type event), i.e. an earlier non-final event occurs first (data: `later_events`).
* Infinitude of reached members is **not proved** (O4-1): the scan is a finite census; the pairs found do not follow a proved closed form.

## What is and is not claimed
PROVED: the obstruction theorem (sufficient for BLOCKED), the exact decision procedure when it terminates. FINITE-EXACT: all tables above. **OPEN:** infinite reached subfamily; a necessary-and-sufficient reachability criterion; no-overshoot for non-blocked members (none observed in 55,000+ undecided-by-obstruction pairs, but no proof).
