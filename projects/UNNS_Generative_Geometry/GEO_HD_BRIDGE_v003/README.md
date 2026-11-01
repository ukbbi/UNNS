# GEO_HD_BRIDGE_v003 — Rational geometry, history invariants, collective dynamics beyond G=1

Builds on the frozen GEO_HD_BRIDGE_v002 (and its accepted B2-T9 erratum). Nothing frozen is edited.

Headlines (proofs in `theory/`, register in `theory/THEOREMS.md`):
* **Rational geometry.** Realised geometry of a rational state is a function of `D` (R3-T1a); but the full region-Graver set is not: infinite families with equal `D` and Graver sizes 2 vs 4 (and 2 vs k(k−1)+2, root system A_{k−1}) (R3-T1). Complete two-prime classification: one extra bit (R3-T2). Rational complexes can have non-trivial homology.
* **History invariant.** For source 4 and contents {2,4}∪A, the first occurrence event separates swap components; infinite disconnected family (R3-T3). General topology law (R3-T4) is **open**.
* **Collective G>1.** Exact reduction for the class G(x)=b, event-time law, dichotomy, two explicit towers proved for all k, stage law with census (R3-T5). One of the towers (G=5, x_{n+3}=4x_n) **falsifies** v002's "rigid iff G∞=1": see `GEO_HD_BRIDGE_v002_ERRATUM_B2-T7.md`.
* **Geometry along collective orbits** (R3-T6) and **multiplier coincidences with SELECT-II** (R3-T7).
* No common law, no Level-5 correspondence. C3 not claimed; novelty not assessed; same-author caveat.

Run: `python RUN_VERIFY.py --fast` (or `--full`, `--shard Z3`, `--list`); Windows: `RUN_WINDOWS.bat`. Rebuild results: `python src/build_v003.py [rational|history|collective|geometry|corr|gcensus]`.
Layout: `theory/`, `src/` (`src/frozen/` pinned engine), `results/`, `data/`, `tests/`.
