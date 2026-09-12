# TC_P01_C001 v001

First prospective TIME-CRYSTAL-I campaign candidate built from the uploaded
large-period DTC archive.

## Place this folder

Extract `TC_P01_C001_v001` inside:

`TC_PROSPECTIVE_01_research_folder`

The runner expects these siblings one level above that research folder:

- `4T-DTC_upload.tar`
- `TIME-CRYSTAL-I_v1_1_0`

## Run

Double-click:

`RUN_C001_WINDOWS.bat`

The script rebuilds the neutral candidate and the independent no-recompilation
control, then runs both through TIME-CRYSTAL-I Blind Mode.

## Read first

1. `reports/RECON_REPORT.md`
2. `locked_runs/C001/EVIDENCE_AUDIT.md`
3. `locked_runs/C001/blind_verdict.json`
4. `locked_runs/C001/analysis_lock.json`
5. `locked_runs/NRCTRL/blind_verdict.json`

Do not run the reveal step until the blind results have been preserved.

## Ground truth

`ground_truth/TC_P01_C001_GT.json`

is intentionally outside the candidate ZIP.

No expected final chamber level is imposed in that file because the source
archive may not contain every sector required for Level 4.
