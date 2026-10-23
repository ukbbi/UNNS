# RGG-2 exact results and proofs

All results below are **mathematical consequences of the candidate definitions**, not discoveries that the earlier UNNS nest grammar selects `J_join`.

## T1. Join semilattice on anchor routes

Let `A={(k,d): k>=1, d>=2}` with coordinatewise divisibility `(a,b)≼(c,e)` iff `a|c` and `b|e`. The componentwise lcm is in `A`, and is the least upper bound in the coordinatewise divisibility order. Associativity, commutativity and idempotence follow from lcm. **Status: proved.**

## T2. Strict separation in every nontrivial value fibre

Take `r=(k,d) != r'=(k',d')` with `k d² = k' d'² = m`. Let `u=J_join(r,r')`. Then each coordinate of `r,r'` divides the corresponding coordinate of `u`, so `v(u)` is a positive-integer multiple of `m`. If `v(u)=m`, both coordinates of `u` must equal the corresponding coordinates of `r` (their coordinatewise ratios are positive integers with product weighted as `ratio_k ratio_d²=1`). Thus `u=r`; likewise `u=r'`, a contradiction. Hence `v(u)>m`. With probe `s=r`, idempotence gives `v(J_join(r,s))=m`, while `v(J_join(r',s))>m`. **Status: proved.**

## T3. Exact lift formula and fibre metric

Write `g=gcd(d,d')`, `L=lcm(d,d')`. Since `k=m/d²` and `k'=m/d'²`,

`lcm(k,k') = m/g²`.

For each prime this follows because `min(v_p(d),v_p(d'))` is the exponent of `g` and `max(v_p(k),v_p(k'))=v_p(m)-2min(v_p(d),v_p(d'))`. Therefore

`v(J_join(r,r')) = (m/g²)L² = m(L/g)²`.

Define within a **single value fibre** `D(r,r')=2 log(L/g)`. With `a_p=v_p(d)`, `b_p=v_p(d')`, this is `2 sum_p |a_p-b_p| log p`. The formula makes nonnegativity, symmetry, positive definiteness (same d implies same k in a fixed fibre), and the triangle inequality immediate. **Status: proved.** Exact ratios are used in the software; floats occur only in logarithmic display.

## T4. Nonlinear observable quotient criterion

For an arbitrary deterministic `J:A×A→A` and observation `v:A→S`, there exists `j:v(A)×v(A)→S` satisfying `v(J(r,s))=j(v(r),v(s))` for all `r,s` iff `(v(r)=v(r') and v(s)=v(s'))` implies `v(J(r,s))=v(J(r',s'))`. This is the definition of a well-defined function on equivalence classes, proved by choosing representatives. For `J_mul`, `j(a,b)=ab`. For `J_join`, T2 supplies a counterexample using `s=r`, so descent fails whenever a nontrivial fibre exists. **Status: proved.** This does not require a bilinear `B`.

## T5. Simultaneous refinement covariance (partial)

For positive integer q with `q²|k_r` and `q²|k_s`, define `T_q(k,d)=(k/q²,qd)`. Since `lcm(a/q²,b/q²)=lcm(a,b)/q²` and `lcm(qa,qb)=q lcm(a,b)`, `J_join(T_qr,T_qs)=T_q J_join(r,s)`. Independent invariance need not hold: `r=(4,2)`, `T_2r=(1,4)`, `s=(1,4)`; join values are `64` and `16` respectively. **Status: proved.**

## Important limitation

Neither T4 nor T5 proves that `J_join` is forced by nest arithmetic, unique among candidate continuations, physically effective, or responsible for quantum entanglement. A derived property of a deliberately selected operation is mathematically valid but cannot substitute for independent mechanism selection.
