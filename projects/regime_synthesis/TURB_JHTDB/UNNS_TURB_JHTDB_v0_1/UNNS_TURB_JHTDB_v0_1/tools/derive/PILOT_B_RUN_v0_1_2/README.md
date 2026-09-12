# JHTDB Pilot B Frozen-Adapter Runner v0.1.2

## Purpose

This package runs the preregistered Pilot B physical-adapter stage **without modifying the frozen `JHTDB_ROUTE_ADAPTER_v0_1_0` scientific code**.

It exists because the frozen adapter is scientifically reusable but its original launcher/output layer is Pilot-A-specific:

- the default config is `config/pilot_a.json`;
- `manifest.json` hardcodes the Pilot-A project name and run ID;
- three top-level output names are hardcoded for Pilot A.

Running the original `RUN_ADAPTER_WINDOWS.bat` directly for Pilot B would therefore risk overwriting Pilot-A records and would mislabel the Pilot-B route manifest.

This runner solves only that execution/provenance problem. It does not alter segmentation, derivatives, scales, relation rules, null settings, or any other scientific setting.

## Install location

Place the entire folder here:

`tools/derive/JHTDB_PILOT_B_RUN_v0_1_0/`

Do not replace or edit:

`tools/derive/JHTDB_ROUTE_ADAPTER_v0_1_0/`

## Files

- `CHECK_PILOT_B.bat` — preflight only; generates no derived Pilot-B result.
- `RUN_PILOT_B_ADAPTER.bat` — performs the full Pilot-B adapter run.
- `run_pilot_b.py` — verification, isolated execution, and provenance wrapper.
- `PILOT_B_CONFIG.json` — Pilot-A scientific settings with only Pilot identity, source path, and source SHA-256 substituted.
- `SHA256SUMS.txt` — package checksums.
- `MANIFEST.json` — package manifest.

## Preflight

Run:

`CHECK_PILOT_B.bat`

It verifies:

1. all 118 files in the preregistered `FREEZE_SHA256.txt`;
2. `SOURCE_RECORD.json` readiness;
3. the frozen selection SHA-256;
4. Pilot-B HDF5 presence and byte size;
5. that the Pilot-B config differs from `pilot_a.json` in exactly three non-scientific source/identity fields;
6. that no prior canonical Pilot-B adapter result will be overwritten.

Expected final line:

`[PREFLIGHT PASS] No Pilot-B derived data were generated.`

## Full run

After preflight passes, run:

`RUN_PILOT_B_ADAPTER.bat`

The runner:

1. creates an isolated staging root under `PB_STAGE`;
2. creates a zero-copy NTFS hard link to the local ~2 GiB HDF5;
3. runs the original frozen adapter code with `PYTHONDONTWRITEBYTECODE=1`;
4. lets the frozen adapter verify the Pilot-B HDF5 SHA-256 itself;
5. copies the derived Pilot-B tables into canonical project locations;
6. changes only the two hardcoded Pilot-A identity labels in the route manifest;
7. preserves the raw frozen-adapter report;
8. creates a canonical Pilot-B route bundle and an explicit adapter-run provenance record;
9. removes the recognized staging area only after successful completion.

No scientific array is altered during the metadata canonicalization step.

## Canonical outputs

Derived objects:

`data/derived/objects/jhtdb_pilot_b/`

Native route project:

`ladders/native/jhtdb_pilot_b/route_project/`

Pilot-B records:

`outputs/records/pilot_b/`

including:

- `JHTDB_PILOT_B_ROUTE.zip`
- `JHTDB_ADAPTER_REPORT_RAW.json`
- `JHTDB_ADAPTER_REPORT.json`
- `PILOT_B_ADAPTER_RUN.json`
- `ADAPTER_RUN_LOG.txt`

Physical statistics:

`outputs/tables/pilot_b/JHTDB_PHYS_STATS.csv`

## Frozen scientific settings

The Pilot-B configuration preserves Pilot A exactly for:

- block factors `[1,2,4,8,16]`;
- exact non-overlapping block mean;
- native boundary margin `16`;
- boundary-touching object rejection;
- Q-based segmentation;
- Q RMS multiplier `1.5`;
- connectivity `26`;
- minimum native voxels `64`;
- minimum coarse voxels `2`;
- positive-overlap candidate relations;
- overlap/IoU eligibility thresholds;
- route edge/object weights;
- 100 primary nulls;
- null seed `20260904`;
- mobility gates;
- alpha `0.05`;
- minimum nulls `20`;
- stored `dt=0.002`;
- viscosity `0.000185`.

Only these three config fields differ from Pilot A:

- `adapter.pilot`
- `source.relative_path`
- `source.expected_sha256`

## Important

Do **not** run the original:

`tools/derive/JHTDB_ROUTE_ADAPTER_v0_1_0/RUN_ADAPTER_WINDOWS.bat`

for Pilot B.

The next preregistered stage after a successful run is **STRUC-ROUTE-I v0.1.2**.

## v0.1.1 repair

Version 0.1.0 used the staging path:

`analysis/replication/jhtdb_pilot_b/_adapter_stage`

In the current Windows project location, the resulting hard-link destination was 266 characters long, exceeding the traditional Windows `MAX_PATH` limit of 260 characters. The run therefore failed at `os.link()` before the frozen adapter started and before any Pilot-B derived data were generated.

Version 0.1.1 changes only the temporary staging location to:

`PB_STAGE`

at the project root. This reduces the corresponding HDF5 link path to approximately 225 characters. No scientific configuration, frozen adapter code, thresholds, source selection, or output interpretation is changed.

## v0.1.2 repair

Version 0.1.1 correctly shortened the active staging path to `PB_STAGE`, but it also attempted to delete the abandoned deep v0.1.0 staging tree before starting. On the current Windows project path, removal of that old tree itself failed with `PermissionError [WinError 5]` before any Pilot-B adapter computation began.

Version 0.1.2 simply leaves that abandoned v0.1.0 staging tree untouched and proceeds with the independent short `PB_STAGE` staging root.

This is an execution-path repair only. No scientific setting, source selection, frozen adapter file, threshold, scale, segmentation rule, relation rule, or null setting is changed.
