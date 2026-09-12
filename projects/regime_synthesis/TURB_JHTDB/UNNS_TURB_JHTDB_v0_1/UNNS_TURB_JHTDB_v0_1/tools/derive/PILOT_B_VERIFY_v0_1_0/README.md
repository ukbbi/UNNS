# Pilot B Adapter Result Verifier v0.1.0

This verifier is for the completed Pilot-B adapter run that ended with a Windows
`PermissionError [WinError 5]` while deleting the temporary `PB_STAGE` directory.

The scientific adapter run had already completed, and the canonicalization step
had already run before the cleanup error occurred.

Place this folder at:

`tools/derive/PILOT_B_VERIFY_v0_1_0/`

Run:

`VERIFY_RESULT.bat`

The verifier does not regenerate or overwrite Pilot-B data. It checks:

- `PILOT_B_ADAPTER_RUN.json` status;
- Pilot-B source and selection identities;
- canonical object and relation tables;
- route manifest;
- route ZIP bundle;
- physical statistics;
- raw and canonical adapter reports;
- SHA-256 hashes recorded by the completed run.

A successful result ends with:

`[VERIFIED] Pilot-B adapter result is complete and canonical.`

If verification passes, do not rerun the adapter. Proceed to the frozen
STRUC-ROUTE-I v0.1.2 stage.

The abandoned temporary `PB_STAGE` and the earlier deep `_adapter_stage`
directories may be left untouched until the replication chain is safely closed.
