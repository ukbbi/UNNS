# Theorem register — GEO_HD_BRIDGE_v002 (B2-T1 … B2-T14)

Status: **PROVED** (proof in the linked document) · **FINITE-EXACT** (exhaustive over a stated range) · **OPEN**. Verifier checks new theorems (Z1–Z6) separately from regressions/integrity (Z0, Z7).

| id | statement | status | doc |
|---|---|---|---|
| B2-T1 | integer state geometry collapses to `D`; closed forms; contractible; persistence ⇔ `q≤q'` | PROVED (+ frozen-engine check, 260 states) | GEOMETRIC_HISTORIES §2 |
| B2-T2 | SELECT-II box transport `Δq_p = w − l_p` | PROVED | §3 |
| B2-T3 | gain–loss balance; rewrite law `ΔΛ=½ΔH` | PROVED | §4, RECOMBINATION |
| B2-T4 | parity conservation of loss steps (`v_p(N)≤1`) | PROVED under restriction | RECOMBINATION |
| B2-T5 | mixed-index forcing (primes 2,3) | PROVED for contents `2^α3^β`; OPEN for k>2 | RECOMBINATION |
| B2-T6 | regime-I reduction `(σ,t)→(σu, sqf(t+1))`; rigid set {1,2,3} | PROVED | FIELD_REGIMES |
| B2-T7 | eventual rigidity; entry time depends on `t` only; G2-Q1: rigidity iff `G∞=1` | PROVED + FINITE-EXACT (G=11, census) | FIELD_REGIMES |
| B2-T8 | collective occurrence changes only at carries | PROVED | CARRY_TRANSITIONS |
| B2-T9 | SELECT-II event saturation (no silent step) | PROVED (+24 496 edges) | EVENT_CORRESPONDENCE |
| B2-T10 | rigid event correspondence (Level 3/4) | PROVED | EVENT_CORRESPONDENCE |
| B2-T11 | birth-endpoint classification `x_m=4^jx_n` | PROVED (birth endpoints); FINITE-EXACT (all endpoints, 16 028 pairs) | EVENT_CORRESPONDENCE |
| B2-T12 | coincidence family `C^k(Ns²)=T_N` | PROVED family; FINITE-EXACT scan x<4000 | EVENT_CORRESPONDENCE |
| B2-T13 | scaling obstruction: `R(N)∈ℤ ⇒ N=1` | PROVED | EVENT_CORRESPONDENCE |
| B2-T14 | σ-transport as common carrier; loss-budget blindness; Level 3 ⇒ Level 4 for integers | PROVED + FINITE-EXACT | GLOBAL_SYNTHESIS, HIGH_DIMENSIONAL |

OPEN items are in `OPEN_PROBLEMS.md`. Nothing here is a claim about C3 or novelty.
