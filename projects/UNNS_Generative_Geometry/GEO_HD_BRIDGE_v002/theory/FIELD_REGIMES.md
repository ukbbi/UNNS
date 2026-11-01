# G2-C/D — Collective arithmetic: regime I

Collective map (applied exactly, `fibre_q`/`Cstep` of the frozen engine): `C(x)=x+L^2/G`, `L=lcm D(x)`, `G=gcd{d−1: d∈D(x)}`.

## B2-T6 (regime-I reduction and rigid set) — PROVED
**Regime I** := `4 | x`.  Claim: `4|x ⇔ G=1 ⇔ L=σ(x)` (for integers `D(x)` = divisors ≥2 of `σ`, `d^2|x`).
*Proof.* `2∈D` iff `4|x`; then `1∈{d−1}` so `G=1`. If `4∤x` every `d∈D` is odd, so every `d−1` is even and `G≥2`. For integers `D(x)` is the set of divisors ≥2 of `σ` (`d²|x`, `d≡1 mod 1`), so `L=lcm D=σ`. ∎
Write `x = σ² t` (`σ=σ(x)`, `t` squarefree). Then `C(x)=σ²t+σ²=σ²(t+1)`; with `t+1 = u² t'` (`t'` squarefree) this is the reduction
`(σ, t) ↦ (σ u, t')`, i.e. `t → sqf(t+1)`, `σ → σ·u`. A **carry** is a step with `u>1`.
**Rigid set.** Suppose `x_{n+3}=4x_n`. Squarefreeness forces `t_{n+3}=t_n` and `σ_{n+3}=2σ_n`, so `u_1u_2u_3=2`: exactly one step has `u=2` and the others `u=1`. Solving `t_{n+3}=t_n` in the three positions of the carry: (1,1,2): `t_1=t+1, t_2=t+2, t_3=(t+3)/4=t ⇒ t=1`; (1,2,1): `t_1=t+1, t_2=(t+2)/4, t_3=t_2+1=t ⇒ t=2`; (2,1,1): `t_1=(t+1)/4, t_3=t_1+2=t ⇒ t=3`. Conversely `t=1,2,3` give `t:1→2→3→1`, `2→3→1→2`, `3→1→2→3` with the single `u=2`. Hence the rigid set is exactly `{1,2,3}` and there `x_{n+3}=4x_n`, one carry (with one birth step) per period. ∎

## B2-T7 (eventual rigidity; G2-Q1 answer) — PROVED + FINITE-EXACT
Every regime-I orbit eventually enters the rigid set with entry time `e(t)` depending **only on `t`** (σ is irrelevant to the dynamics of `t`). Entry times for `t<=T` computed by sieve (`entry_time_table`); the FIELD-I reset-descent bound `4κ₃(t)` (v012 T72(iv), cited) is satisfied in all tested cases. Birth count at a rigid carry `= τ(odd part of σ)` (checked for σ=2,4,6,…, `results/REGIME_I.json`).
**G2-Q1 (is 3-step rigidity universal?):** *No.* It holds iff `G∞=1` (FIELD-I T32). For `G>1` the orbit scales with another period and multiplier; the finite-exact witness is the T50 orbit `G=11`, `L=67500`: `x_{n+8}=9x_n`, carry steps 8,16,24,32,40, `|D|` at the period starts 7,9,11,13,15 (`results/BEYOND_REGIME_I.json`, re-derived from the definition). A census of 84 non-regime-I integers `x<600` all reach `G=1` (max 66 steps) — evidence, not proof (the general T51 is cited).
