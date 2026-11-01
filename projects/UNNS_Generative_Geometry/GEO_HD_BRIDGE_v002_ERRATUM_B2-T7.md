# Erratum 2 (append-only) to GEO_HD_BRIDGE_v002 — B2-T7 / G2-Q1 wording

GEO_HD_BRIDGE_v002 is unchanged and remains the frozen baseline (together with `GEO_HD_BRIDGE_v002_ERRATUM_B2-T9.md`).

## What was overstated
`theory/FIELD_REGIMES.md` (G2-Q1) and the `THEOREMS.md` row for B2-T7 say that 3-step rigidity `x_{n+3}=4x_n` holds **iff** `G∞=1`
("For G>1 the orbit scales with another period and multiplier").
Only the direction `G∞=1 ⇒ eventually x_{n+3}=4x_n` (FIELD-I T32, cited, and B2-T6/T7 for the regime-I reduction) is supported.
The converse is **false**.

## Counterexample (exact, re-derived with independent code)
`x_0 = 126²/5 = 15876/5`.  `D(x_0)={6,21,126}`, `L=126`, `G=5`; the orbit keeps `G=5` forever, `L` doubles every three steps
(126, 252, 504, 1008, 2016 …) and `x_{n+3}=4x_n` for every `n` (12 consecutive ratios checked equal to 4).
Proof for the whole tower `S_k = 126·2^k`, `ℓ=5`: see `GEO_HD_BRIDGE_v003/theory/COLLECTIVE_REGIMES.md` (R3-T5c).

## Correct statement
* `G∞=1 ⇒` eventually `x_{n+3}=4x_n` (unchanged).
* For `G∞>1` the scaling `(P,ρ²)` can be the rigid pair `(3,4)` (e.g. `ℓ=5`, `S=126·2^k`) or different, e.g. `(8,9)` for `ℓ=11` (T50 family, re-proved for all `k` in v003).
* So the answer to G2-Q1 "is 3-step rigidity universal?" remains **no** (the G=11 family), but rigidity is **not** characterized by `G∞=1`.
Nothing else in v002 depends on the "only if" direction (B2-T10, T11–T14 use regime I, `4|x`, only).
Same-author caveat applies; C3 not claimed; novelty not assessed.
