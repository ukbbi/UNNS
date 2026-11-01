# G2-T4 — Carry and non-rigid transitions

## Reduction
In regime I the whole dynamics is `(σ,t) ↦ (σ·u, sqf(t+1))` with `u²‖(t+1)` square part. A transition is **rigid** if `u=1` for both of the first two steps and `u=2` (t=3) at the third; it is a **carry** whenever `u>1`.

## B2-T8 (collective event structure) — PROVED
Along a regime-I orbit `D(x_n)` is non-decreasing (cited FIELD-I T31), the occurrence fibre changes **only at carries**, and at a carry with square part `u²` the new indices are the divisors `d·σ'`-chain created by multiplying `σ` by `u`: the number of new indices equals `|D(σu)|−|D(σ)|`. For `u=2`, `σ` even this is `τ(odd part of σ)` (one for σ=2^a, two for σ=6, …; table in `results/REGIME_I.json`). Hence **between carries the occurrence geometry is constant** (same `D`, same box); at a carry the box grows from `q` to `q'` with `q'−q ≥ 1` on the support of `u`.

## Beyond rigid carries
`t+1` with larger square factors (`u ≥ 3`): reachable from non-rigid `t` before the descent to {1,2,3}; the entry-time table gives the full list for `t ≤ T`. Since the entry time depends on `t` only, the **σ-part of the history is a product of multipliers `u_i` which depend only on the `t`-trajectory**; the geometry (box of `σ`) then evolves by explicit multiplication of `σ`. This is the proved part of G2-T4 for regime I.
**Not proved:** the classification of `G>1` transitions (class closure, carry cycles) — FIELD-I T49–T58/T69–T73 cited. We add exactly one thing there: the T50 re-derivation and the census above.
