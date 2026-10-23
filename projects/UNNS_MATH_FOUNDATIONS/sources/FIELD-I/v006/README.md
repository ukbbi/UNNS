# FIELD-I v006 — G-Collapse and Arithmetic Phase Transitions

This ZIP extends the full frozen FIELD-I v005 tree with a new `v006/` folder. Earlier versions and their generated records have not been edited. All files are standard text, Python 3.10+, Windows batch scripts, and machine-readable reports.

## Windows CMD

1. Unzip `FIELD-I_v006.zip` into `UNNS_ENTANGLE_I/`, merging only by adding `FIELD-I/v006/`. Existing `FIELD-I/v002/`–`v005/` are byte-identical to v005, so no source changes are needed.
2. Open `UNNS_ENTANGLE_I\FIELD-I\v006` in File Explorer, type `cmd` in the address bar, Enter.
3. Run `python field6.py` to check the new v006 results and write `output/field6_report.json`.
4. Run `RUN_TESTS.bat` to replay earlier suites and v006, leaving their newly generated logs under `v006\output\` only.
5. Run `certutil -hashfile field6.py SHA256` if you wish to compare against `output\MANIFEST.sha256`.

`RUN_TESTS.bat` calls `python`; make sure Python is available on PATH. It exits with a nonzero code if any verifier reports FAIL. For a shorter v006 run in CMD: `set FIELD6_QUICK=1` followed by `python field6.py`. The main regression launcher runs previous versions under their own quick-mode flags only when set; full regression execution can be slower than the stand-alone v006 checks.

## Scientific status

- Proved: parity-sensitive modular plateau bound; G=2,3,6 finite collapse; exact eventual G=1 scaling; corrected reach-set counting statement.
- Open: universal G-collapse and persistent-G counterexamples.
- All claims concern the explicitly selected collective map C, not a physically established interaction or a uniquely mandated original UNNS operation.
