# A4-T5 / A4-T6 — Betti evolution on the G=11 and G=5 towers

States at period starts: `x_k=S_k²/11`, `S_k=2²·3^{3+k}·5⁴` (period 8, multiplier 9); `x_k=S_k²/5`, `S_k=126·2^k` (period 3, multiplier 4). Computed with the frozen engine (builder) and re-computed by independent code for sample `k` (Z6). **No extrapolation beyond k=45 is claimed.**

## G=11 (mechanism, PROVED)
Box `(2, k+3, 4)` on primes `(2,3,5)`; discrete logs mod 11 (base 2): `3=2^8`, `5=2^4`, so `F_k={(a,c,e): a∈[0,2], c∈[0,k+3], e∈[0,4], a+8c+4e≡0 (10)}∖0`. Parity forces `a∈{0,2}`; then `4c+2e+a/2 ≡0 (5)`. For fixed `a`, as `e` runs over 0..4 the residue of `c` mod 5 runs over all classes once, so the count over `c∈[0,k+3]` is exactly `k+4`: `|F_k|=2(k+4)−1=2k+7` (this is v003 R3-T5b'). Because `3` has order 5 mod 11, the slice structure of `F_k` in the `c`-direction is **5-periodic**; each increment of `k` appends one more slice, so the complex grows by a periodic block pattern.
| quantity (FINITE-EXACT, k=0..45) | value |
|---|---|
| dormant Graver moves | 0 for all k; `|Gr|=22` for `k≥3` |
| `β₁` | 6, 7, then 8 for `2≤k≤45` |
| `β₂` | 0,1,4,7,13,16 then 17 for `6≤k≤45` |
| `β₃` | 0 for `k≤8`; from k=9: 4,4,7,8,9,13,13,16,17,18,22,… increments `(0,3,1,1,4)` repeating, `β₃(k+5)=β₃(k)+9` |
| `χ` | `10−β₃` for `k≥6` |
Statement: **no activation occurs in this tower** (no dormant relation exists); all Betti changes are creation-realisations from new D-elements (two per period). Whether `β₁=8`, `β₂=17` persist for all `k`, and whether the period-5 law for `β₃` persists, is **OPEN** (a proof would need the periodic-slice homology of a cubical complex; not attempted).

## G=5 (FINITE-EXACT)
Box `(k+1,2,1)` on `(2,3,7)`; `3=2^3`, `7≡2` mod 5 → `a+3c+f≡0 (4)`: `|F_k|≈1.5k`. Betti vector `(1,6,5,0)` for `7≤k≤45`; `|Gr|=18` for `k≥3`; dormant `2,6` at `k=0,1`, then 0. Within a period (`126²/5`, b=5) step-level activation occurs (5→6: `β₁ 1→4`).

## G=5 versus G=11 (A4-T6)
Same engine, same kind of rigid-looking tower (scaling `x_{n+P}=ρ²x_n`), yet: the *scaling law fixes* the occurrence sets and hence the realised complex (R3-T1a); it does **not** fix the lattice/dormancy pattern or the Betti vector. G=11: no dormant relations, `β₃` unbounded-looking (67 at k=45); G=5: dormant relations early and activated within the first period, topology bounded at `(1,6,5,0)` (k≤45). The multiplier (9 vs 4) and period (8 vs 3) do not predict either. ℓ=29 (`G=29`, `(P,ρ²)=(35,900)`) remains finite-exact: first 24 steps `D={30,378}`, then `175` joins and `β₁ 0→1`.
