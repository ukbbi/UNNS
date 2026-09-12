# ROUTE_EXTRACT_PB_v011

Pilot-B execution wrapper for the frozen `ROUTE_LADDER_EXTRACT_v0_1_1` logic.

## Why this wrapper exists

The frozen extractor is Pilot-A-specific in its source hash, run ID, expected counts, and output paths. This wrapper does **not** modify the frozen extractor file. It verifies that file by SHA-256, imports it, substitutes only Pilot-B identity-validation constants at runtime, and executes the same extraction function in a short temporary stage.

The scientific extraction definitions remain unchanged.

## Before running

The **primary** Pilot-B ROUTE-I archive, not the `[1,2,4,8]` sensitivity archive, must be available as either:

`outputs\route_i\pilot_b\PB_PRIMARY.zip`

or:

`outputs\route_i\pilot_b\jhtdb_pilot_b_20260907_145640.zip`

Expected primary archive SHA-256:

`405bc1acd99bec9c48b3aef47ed375991cf4ee4e83807e54ea491f2d55b6bd87`

## Placement

Put this folder at:

`tools\derive\ROUTE_EXTRACT_PB_v011\`

## Run

Double-click:

`RUN_EXTRACT.bat`

## Expected ladder populations

- `D_STITCH`: 3,962
- `P_TIME`: 8,806
- `P_SCALE`: 4,830

## Outputs

Canonical:

`ladders\route_i\pilot_b\primary\`

STRUC-I-facing:

`ladders\struc_i\pilot_b\`

STRUC-PERC-I-facing:

`ladders\struc_perc_i\pilot_b\`

Records:

`outputs\records\pilot_b\ROUTE_EXTRACT.json`

`outputs\records\pilot_b\ROUTE_LADDERS.zip`

## Frozen rules preserved

- duplicates preserved;
- no deduplication;
- no jitter;
- no smoothing;
- no normalization;
- no rescaling;
- full binary64 precision written with 17 significant digits;
- ascending stable sort only;
- STRUC-I and STRUC-PERC-I copies are byte-identical to the canonical ladder CSVs.

The sensitivity run is **not** used for downstream ladder extraction. It remains a separate robustness record.

## v0.1.3 correction

`PB_PRIMARY.zip` no longer needs to be created.

The previous wrapper incorrectly treated the ZIP container SHA-256 as the
scientific identity after instructing the user to recompress the already
verified run folder. Recompressing identical files normally changes ZIP bytes
because ZIP metadata and compression details change.

v0.1.2 instead reads the canonical primary run directly from:

`outputs/route_i/pilot_b/jhtdb_pilot_b_20260907_145640/`

It verifies the SHA-256 of every scientific payload file against the previously
verified primary archive, then creates a temporary transport ZIP only because
the frozen extractor accepts ZIP input. The frozen extraction rules themselves
remain unchanged.

You may leave or delete the locally created `PB_PRIMARY.zip`; v0.1.2 does not
use it.

## v0.1.3 correction

The primary `RESULT.json` stores `verdict` as an object:

`{"class":"CONSTRAINED_ROUTING", ...}`

rather than as the bare string `"CONSTRAINED_ROUTING"`.

v0.1.2 correctly verified every primary scientific payload file, but then
incorrectly compared the entire verdict object with a string and stopped before
the frozen extractor ran.

v0.1.3 validates `verdict.class` instead. No extraction rule, expected count,
source file, frozen extractor, chamber setting, or scientific value is changed.
