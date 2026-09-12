# JHTDB High-Re Spatial Generalization — Workflow v0.1

1. Merge this package into `UNNS_TURB_JHTDB_v0_1`.
2. Verify `analysis/generalization/jhtdb_high_re/FREEZE_SHA256.txt` before extracting field values.
3. In SciServer, use the already mounted `turbulence-ceph` volume.
4. Run `INSPECT_SCISERVER.py` first. It reads Zarr metadata only (shape/chunks/dtype); it does not read selected field values.
5. Run `EXTRACT_SCISERVER.py` once the metadata checks pass.
6. Download the generated `HIGH_RE_EXPORT` folder to the local project.
7. Place files under:
   - `data/raw/jhtdb/high_re/isotropic8192/`
   - `data/raw/jhtdb/high_re/isotropic32768/`
8. Verify every downloaded HDF5 SHA-256 against its `SOURCE_RECORD.json`.
9. Implement/run the frozen scale-only adapter exactly as specified in `PROTOCOL.md`; no time relations are allowed.
10. Run the scale-persistence null test (100 nulls, frozen settings).
11. Extract `P_SCALE` ladders without deduplication/jitter/smoothing/rescaling.
12. Run canonical STRUC-I and STRUC-PERC-I independently on each frozen snapshot ladder.
13. Apply the interpretation matrix in `CRITERIA.md` without threshold retuning.
14. Freeze all outputs before synthesis.

Pilot B remains untouched and pending acquisition.
