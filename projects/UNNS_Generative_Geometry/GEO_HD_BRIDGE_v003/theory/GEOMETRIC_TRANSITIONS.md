# R3-G  What collective transitions do to rational geometry

## Theorem R3-T6 (geometry along a class orbit) — PROVED + FINITE-EXACT tables
Inside the class `G(x)=b` (COLLECTIVE_REGIMES R3-T5a):
1. **Realised geometry changes only at occurrence events.** Between events `D` is constant (R3-T5a(iii)); by R3-T1a `K_axis, K_move`, their cells, components and homology are functions of `D`. So they are constant on every run of non-event steps. (PROVED)
2. **Arithmetic carries need not be geometric events.** In the ℓ=11 tower the box coordinate `q_2` jumps `2 → 3` at `t=4` and `t=8` (the numerator gains `2²`; `(σ,t)`-style "carry") but `D` — hence the realised complex — does not change, because the new exponent `a=3` is odd and `2^3·(QR) ≢ 1 (mod 11)`. (PROVED; verifier Z6.) The box, the ambient dimension and the dormant Graver set are therefore *not* what drives the realised geometry; they change silently.
3. **No dormant moves on the tower** (ℓ=11, k=0,1, t=1..10): `Gr` equals the F-only moves; so the full record is determined by `D` there. (FINITE-EXACT; builder + independent Z7.)
4. **Betti vectors at period starts, ℓ=11 tower** (GF(2) = GF(p), `K_move`; one component; `K_axis` is a discrete set of `|D|=2k+7` points):

| k | q | \|D\| | Betti (b0,b1,b2,b3) | χ |
|---|---|---|---|---|
| 0 | (2,3,4) | 7 | (1,6,0) | −5 |
| 1 | (2,4,4) | 9 | (1,7,1,0) | −5 |
| 2 | (2,5,4) | 11 | (1,8,4,0) | −3 |
| 3 | (2,6,4) | 13 | (1,8,7,0) | 0 |
| 4 | (2,7,4) | 15 | (1,8,13,0) | 6 |
| 5 | (2,8,4) | 17 | (1,8,16,0) | 9 |
| 6–8 | | 19–23 | (1,8,17,0) | 10 |
| 9–10 | | 25–27 | (1,8,17,4) | 6 |
| 11 | (2,14,4) | 29 | (1,8,17,7) | 3 |
(Own implementation agrees with the frozen engine for k ≤ 4.) Each period start is an event: the Betti vector changes at carries; integers would give `(1,0,..)` always (B2-T1).  
Each period is one event: `|D|` grows by exactly 2 (R3-T5b'), but the topology grows irregularly: `b1` saturates at 8, `b2` at 17 for several periods, `b3` appears at k=9. No closed form is claimed (O3-2).
5. **ℓ=5 tower** (`S=126`): within one period `t=1..4` the realised records are those of `D` (1 or 2 new indices per event, depending on `-(k+2) mod 4`).

## What this does and does not say
Arithmetic scaling (`x_{n+8}=9x_n`) says nothing about geometric recurrence: the Betti vector does *not* recur with the arithmetic period (it changes every period for k≤11). Geometric periodicity is neither implied nor observed.
