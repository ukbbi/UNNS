# RGG-2 Specification v0.1

**Status:** explicit candidate operation, restricted to positive-integer anchor routes. No field rule and no bilinear pairing `B` are assumed.

## Source primitive and domain

For positive integers `M,N`, the established nest value is `M ⟂ N = M(N+1)^2/N`. The integer anchor condition is `N | M`. Set `k=M/N` and `d=N+1 >= 2`. Then `r=(k,d)`, `v(r)=k d^2`, and conversely `(M,N)=(k(d-1),d-1)`.

## Operations (candidate, not previously established UNNS laws)

- `J_mul(r,s)=(k_r k_s,d_r d_s)`: original RGG-1 control.
- `J_join(r,s)=(lcm(k_r,k_s),lcm(d_r,d_s))`: primary proposed joint continuation.
- `J_gcd(r,s)`: componentwise gcd when the second coordinate remains >=2, otherwise **undefined**; adversarial comparator.
- `J_mixed(r,s)=(lcm(k_r,k_s), gcd(d_r,d_s))` only when gcd(d_r,d_s)>=2; comparator (partial).
- `J_blind(r,s)={t : v(t)=v(r)v(s)}`: RGG-1 value-only baseline, not a control matched to `J_join`'s output value.

## Theorem targets and status

1. **[Proved, conditional on proposed `J_join`]** Closure, commutativity, associativity, idempotence; the pointwise coordinate-divisibility order makes `J_join` the least upper bound.
2. **[Proved]** For distinct anchors `r != r'` of identical value `m`, `v(J_join(r,r')) > m` and the value of the join distinguishes them with probe `s=r`.
3. **[Proved]** For equal-value anchors, `v(J_join(r,r'))/m = (lcm(d,d')/gcd(d,d'))^2`; twice the log of that ratio's positive square root defines a weighted L1 fibre metric.
4. **[Proved]** An output observation `v∘J` descends to a two-argument operation on observed values exactly when value equivalence is a congruence in each argument. `J_mul` passes; `J_join` fails.
5. **[Proved on valid partial domain]** `J_join(T_q r,T_q s)=T_q J_join(r,s)` whenever both refinements are defined; independent refinement can alter its observed output.
6. **[Not established]** Any uniquely preferred operation, physical mechanism, interaction `B`, evolution `F`, or entanglement correlation.

## Refine without over-claiming

`T_q(k,d)=(k/q^2,qd)` is only defined when `q^2 | k` and is an affine translation by `(-2e_p,e_p)` in prime-exponent coordinates for prime `q=p`. It is **not** a globally defined linear endomorphism of the positive anchor set. Before applying the manuscript's Theorem 7.1 verbatim, introduce and justify an appropriate linear extension.

## Gate after Phase I–II

Do not reinterpret `J_join` as an independently grounded physical interaction. The next decision is whether its proofs, boundary behavior, and adversarial alternatives provide sufficient **nontrivial** constraints to motivate extensions.
