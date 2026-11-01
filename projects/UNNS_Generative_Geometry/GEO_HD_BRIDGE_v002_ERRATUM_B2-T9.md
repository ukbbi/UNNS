# Erratum (append-only) to GEO_HD_BRIDGE_v002 — B2-T9

Release GEO_HD_BRIDGE_v002 is unchanged and remains the frozen baseline. This note is a separate record.

## What was wrong
`theory/EVENT_CORRESPONDENCE.md`, B2-T9, states that `D(m) ⊊ D(m')` on every SELECT-II edge `m --N--> m' = m(N+1)²/N`, and that `σ | σ'`.
Both are false. Counterexample: `4 --N=2--> 18`, `D(4)={2}`, `D(18)={3}` (σ: 2 → 3). The sets are incomparable.
The B2-T9 proof only gives `σ'/σ = (N+1)/c > 1` with `c ≤ N`; that is a statement about σ as a rational ratio, not about divisibility or inclusion.

## Correct statement
**B2-T9 (corrected).** On every SELECT-II edge `σ(m') = σ(m)(N+1)/c > σ(m)`, where `c = ∏_{p|N} p^{l_p}` and `c ≤ N`. Hence `σ(m') ≠ σ(m)` and `D(m') ≠ D(m)` (D determines σ = max D): every edge is an occurrence event (no silent step). **Not implied:** `D(m) ⊆ D(m')`, `σ(m) | σ(m')`, or persistence of earlier occurrences.
Status unchanged: PROVED.

## Check (this erratum, edges m ≤ 3000 with N | m, 24 495 edges)
* `σ' > σ` and `D' ≠ D` on all edges: 0 exceptions.
* `D(m) ⊆ D(m')` holds on 13 893 edges and fails on 10 602 (first failure: m=4, N=2).

## Scope of the error
* The verifier check Z5 "event saturation" tests only `σ' > σ` / `D' ≠ D`, so it is correct as written; only the prose of T9 overstates.
* B2-T8 (collective regime I: σ_n | σ_{n+1}, D non-decreasing) is a different claim about the collective map and is unaffected (verified by Z4).
* T10, T11, T14 use T9 only through "every edge changes D"; no dependence on inclusion was found.
Same-author caveat applies; C3 not claimed; novelty not assessed.
