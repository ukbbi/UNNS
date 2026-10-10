# SCR_III_ENGINE_v001 — installation

## Destination

Extract this ZIP **into the root of** `structural_complexity_reduction/` — the folder that already contains `scr_ii/`, `scr_iii/`, `SCR_I_PREREG_v003/`, and the ratified SCR-III design files.

The archive is a drop-in package. It will:

- merge engine files into `scr_iii/`;
- complete `scr_iii/SCR_III_PREREG_v001/` with config, schemas, validation and freeze files;
- add the root Windows runners `RUN_SCR_III_*.bat`;
- **not** modify `scr_ii/` or `SCR_I_PREREG_v003/`.

If Windows asks whether to replace the two files already present under `scr_iii/SCR_III_PREREG_v001/` (`SCR_III_PREREG_v001.md` and `SEEDS_v001.json`), replacement is safe: the package carries the frozen canonical copies used to build the engine.

## First action only

Run:

```text
RUN_SCR_III_VALIDATE.bat
```

A successful local preflight creates:

```text
scr_iii/output/audit/PREFLIGHT_PASS_v001.json
```

Do **not** run the primary directly.

## Authorized sequence

```text
RUN_SCR_III_VALIDATE.bat
RUN_SCR_III_AUDIT.bat
# inspect AUDIT_RESULT_v001.json
RUN_SCR_III_FREEZE_AUDIT.bat
RUN_SCR_III_PRIMARY.bat
RUN_SCR_III_NULLS.bat
RUN_SCR_III_ESTIMATORS.bat
RUN_SCR_III_SUMMARY.bat
```

`RUN_SCR_III_PRIMARY.bat` verifies the frozen audit hashes and refuses to run if the audit was not frozen or changed after freezing.
