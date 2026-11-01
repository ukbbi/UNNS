# GEO_HD_E2_P4_v002 -- E2-P4 continuation (P4-C1 correction, P4-E3, P4-E4)

Preserves GEO_HD_E2_P4_v001 (carried over; v001 zip unchanged).  Superseded in this folder: STATUS.json, MANIFEST.json, README.md, RUN_VERIFY.py (v001 shards S0-S7 retained).

Read first: `results/P4_REPORT_V002.md`, `theory/THEOREMS_V002.md`, `theory/THEOREM_AUDIT_V002.md`, `theory/COUNTEREXAMPLES_V002.md`, `ERRATA/E2_P4_ADDENDUM_V002_P4C1_CORRECTION.md`.

New code: `src/lattice_model.py`, `src/zero_vertex.py`, `src/slab_law.py`, `src/build_p4_v002.py` (stages), `src/build_slab.py`, `src/slab_consistency.py`, `src/audit_v002.py` (independent verifier), `src/make_figures_v002.py`.
New data: `data/P4_C1_CORRECTION.json`, `data/SEARCH_LIMITS_V002.json`, `results/P4_{PLANAR_LATTICE,PLANAR_CORE,PLANAR_WINDOW,LATTICE3,FIELDI3,SLAB,SLAB_CONSISTENCY}.json`.
Verify (each shard < ~3 min): `python RUN_VERIFY.py --fast` (S0,S1,S2,S3,S5,S9,S10,S11,S12) then `--shard S13`, `--shard S14`, `--shard S8` (~2 min), `--shard S6`, `--shard S4` (~2-3 min).
Rebuild stages: `python src/build_p4_v002.py --stage planar_core` (etc.; resumable; existing results are kept unless --force).
C3 is NOT claimed.  Builder and verifier were written by the same author (not external verification).
