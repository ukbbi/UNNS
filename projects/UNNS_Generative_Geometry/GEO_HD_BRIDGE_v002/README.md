# GEO_HD_BRIDGE_v002 — Geometric evolution, recombination and collective boundary laws

Builds on the frozen GEO_HD_BRIDGE_v001 (nothing frozen is edited). Organised by mathematics, not by programme names:
Generation → Relationships → Geometry → General laws; each arrow is a theorem or an obstruction (see `theory/THEOREMS.md`).

Headlines (details and proofs in `theory/`):
* Integer states: the full GEO-I record collapses onto `D(m)`; K(m) is contractible (B2-T1). Transport/balance/rewrite laws for histories (T2–T5).
* Collective regime I: reduction `(σ,t)→(σu, sqf(t+1))`, rigid set exactly {1,2,3}, eventual rigidity, G2-Q1 answered (T6–T8).
* Events: SELECT-II has no silent step; rigid Level-3/4 correspondence; birth-endpoint classification; coincidence family; scaling obstruction (T9–T13).
* **No common law and no Level-5 correspondence are claimed.** C3 not claimed; novelty not assessed; same-author caveat.

Run: `python RUN_VERIFY.py --fast` (or `--full`, `--shard Z3`, `--list`); Windows: `RUN_WINDOWS.bat`. Rebuild results: `python src/build_v002.py` (the `beyond` section takes ~1 min).
Layout: `theory/` documents, `src/` code (`src/frozen/` pinned engine), `results/` JSON, `figures/`, `tests/`, `data/`.
