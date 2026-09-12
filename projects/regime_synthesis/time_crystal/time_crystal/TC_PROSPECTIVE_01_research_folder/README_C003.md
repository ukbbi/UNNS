# TC_P01_C003 v001

Third prospective candidate in `TC_PROSPECTIVE_01`.

C003 is the first deliberate quasi-periodic boundary test of
`TIME-CRYSTAL-I v1.1.0`.

## Source already in your campaign

```text
candidates\C003_source\rawdata.xls
```

## Install

Copy the setup ZIP contents directly into the campaign root, merging the shared
folders by adding C003-specific files.

Do not replace or delete C001/C002 files.

## Run

```text
RUN_C003_WINDOWS.bat
```

The adapter has no third-party dependency. It reads the legacy XLS using the
Python standard library.

## Inspect before reveal

```text
locked_runs\C003\RUN_LOG.txt
locked_runs\C003\EVIDENCE_AUDIT.md
locked_runs\C003\blind_verdict.json
locked_runs\C003\analysis_lock.json

locked_runs\C003_CTRL\blind_verdict.json
```

Then refresh the campaign shell with:

```text
OPEN_TC_P01.bat
```

Do not reveal C003 until its locally reproduced blind result has been inspected.
