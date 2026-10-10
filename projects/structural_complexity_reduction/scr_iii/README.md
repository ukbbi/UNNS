# SCR-III-A engine

`SCR_III_ENGINE_v001` implements the ratified `ROUTE_CSP_C v001` coupling ruler without modifying `scr_ii/` or `SCR_I_PREREG_v003/`.

Run order from the project root:

1. `RUN_SCR_III_VALIDATE.bat`
2. `RUN_SCR_III_AUDIT.bat`
3. Inspect the audit result. If and only if it emits `AUDIT_PASS_v001.json`, run `RUN_SCR_III_FREEZE_AUDIT.bat`.
4. `RUN_SCR_III_PRIMARY.bat`
5. `RUN_SCR_III_NULLS.bat`
6. `RUN_SCR_III_ESTIMATORS.bat`
7. `RUN_SCR_III_SUMMARY.bat`

The primary runner refuses to start without the audit-pass file. The validator does not run audit or primary.
