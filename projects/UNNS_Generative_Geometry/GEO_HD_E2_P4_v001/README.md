# GEO_HD_E2_P4_v001 -- Arithmetic obstruction theory for nonrectangular targets: coupled-target transport preflight

Executes spec phases P4-E0..E2 (section 14).  Extract next to the earlier releases; nothing existing is modified.  Python >= 3.8, standard library only (matplotlib only for src/make_figures.py).

* Result: P4-F110 (2*110^(4m)/9 -> 110^(4m)/3) is SOURCE_CONTAINED for every m >= 1 between two *nonrectangular* lattices; proved via an E_3 hull theorem (P4-T1).  See results/P4_REPORT.md.
* Not started: planar CP3-A search (E3), coupled 3D census (E4), full novelty audit (E5).  No C3 claim.
* Verify (each shard < 3 min): `python RUN_VERIFY.py --shard S0` ... `S5`;  `--fast` = S0,S1,S2,S3,S5;  `--full` adds the heavy corner replay S4.  Windows: RUN_WINDOWS.bat.
* Rebuild: `python src/build_p4.py` (stages are resumable; `--stage m2` runs the opt-in direct m=2 check, ~4-5 min); then `python src/finalize_p4.py`.
* Layout: src/engine = byte-identical pinned E2-P3/E2-P2 engine; src/*.py = new E2-P4 code (loaded via src/_boot.py because some names coincide with engine modules).
