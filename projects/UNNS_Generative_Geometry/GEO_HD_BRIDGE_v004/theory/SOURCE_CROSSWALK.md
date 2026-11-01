# Source crosswalk — GEO_HD_BRIDGE_v004

| v004 item | built on | note |
|---|---|---|
| state record `D, F, Gr, b`, hull rule, positive-primitive / edge-realised / dormant split | GEO_HD_BRIDGE_v003 `rational_geometry.py` (R3-T1a, R3-T1) | copied unchanged; frozen engine copies pinned in `results/PINS.json` (equal to v002/v003) |
| collective map `C(x)=x+L²/G`, class `G=b`, event-time law, ℓ=11 / ℓ=5 / ℓ=29 towers | v003 R3-T5a…R3-T5d, R3-T6 | only the actual map is used |
| history complexes, Junction Lemma, pair-order bit | v003 R3-T3 | `history_invariants.py` copied |
| SELECT-II rule `T_N(m)=m(N+1)²/N, N|m` | frozen integer rule only | **no** rational extension of SELECT-II is used anywhere |
| family `x=P²/ℓ, y=(Pq)²/ℓ` | the v003 assessment (6c2c5ad7) | treated as a *candidate*; re-derived and machine-checked here (A4-T1/T2) |

**Wording correction.** The v004 specification speaks of a "(G=35), period-29 candidate". The v003 finding is ℓ=29, **G=29**, stage-law pair `(P,ρ²)=(35,900)` for S=1890 (`P=Σ(τ_i−1)=35`, `ρ²=Πτ_i=900`, `τ=(25,4,9)`). v004 documents use this form.

**Not touched:** GEO_HD_1D v001–v004, GEO_HD_E2_P4 v005, GEO_HD_BRIDGE v001–v003 and both v002 errata remain exactly as released. Inherited verification is **NOT_RERUN** (hash integrity only). C3 NOT claimed; novelty NOT assessed; same-author line.
