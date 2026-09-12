# STITCH-MECH Pilot B runner v0.1.3

Underlying frozen instrument: **STITCH-MECH v0.1.1**

Place this folder at:

`tools/analyze/STITCH_MECH_PB_v011/`

Do not run the original `STITCH_MECH_v0_1_1/RUN_WINDOWS.bat` for Pilot B,
because its frozen configuration points to Pilot A and its normal output
locations would overwrite the Pilot-A mechanism records.

## 1. Preflight

Run:

`CHECK_PB.bat`

This verifies the frozen STITCH-MECH instrument and the canonical primary
Pilot-B ROUTE-I payload. It generates no mechanism nulls.

## 2. Full mechanism run

Run:

`RUN_PB.bat`

The wrapper copies the frozen Pilot-A STITCH-MECH configuration at runtime and
changes only:

- pilot identity;
- transport ZIP path/hash for the already verified Pilot-B ROUTE-I payload;
- output locations.

All scientific settings remain identical, including:

- N0 imported from the frozen ROUTE-I run;
- N1 count 100, seed 20260905, swaps/edge 5, distance bins 5;
- N2 count 100, seed 20261905, swaps/edge 5, distance bins 4, feature bins 4;
- null-quality gates;
- 5000 mechanism permutations;
- upper-10% tail;
- viscosity 0.000185;
- all partial-rank controls.

The run is resumable. Its short working stage is:

`%LOCALAPPDATA%\UNNS\PBM`

Do not delete that stage while N1/N2 are running.

## Canonical outputs

`analysis/mechanism/jhtdb_pilot_b/stitch_mech_v01/`

`outputs/tables/pilot_b/`

`outputs/records/pilot_b/`

The frozen HTML writer hardcodes “Pilot A” in its heading. The wrapper preserves
that raw HTML as `REPORT_RAW.html` and creates `REPORT.html` with that heading
changed to “Pilot B”. No scientific value is modified.

## v0.1.2 repair

The previous wrapper stopped before STITCH-MECH itself started because the generated
Python wrapper contained literal `\\n` text in places where Python required the
normal newline escape `\n`. In particular, `Path.open(..., newline="\\n")`
raised:

`ValueError: illegal newline value: \\n`

The same generation error would also have made the staged JSON configuration end
with literal backslash-n text.

v0.1.2 corrects those wrapper-only newline encodings. The frozen
`STITCH_MECH_v0_1_1` instrument, Pilot-B primary ROUTE-I payload, N0/N1/N2
definitions, seeds, null counts, mechanism permutations, thresholds, and all
scientific settings are unchanged.

The failed attempt generated no Pilot-B mechanism nulls, so the full run can
start normally.

## v0.1.3 repair

The v0.1.2 run reached the frozen STITCH-MECH instrument successfully and
reproduced the real-data geometry and D_square value. It then stopped during
N1 progress reporting because the Windows Python process used the cp1251
console encoding, which cannot encode the Unicode approximately-equal sign
(U+2248) used in the frozen progress text.

v0.1.3 forces UTF-8 only for subprocess standard I/O:

- `PYTHONIOENCODING=utf-8`
- `PYTHONUTF8=1`
- wrapper-side subprocess decoding explicitly uses UTF-8

No frozen STITCH-MECH source file is modified and no scientific setting,
seed, null count, swapping rule, distance/feature binning rule, mechanism
permutation count, or threshold changes.

The short stage `%LOCALAPPDATA%\UNNS\PBM` is deliberately preserved.
Run `RUN_PB.bat` again without deleting it; STITCH-MECH v0.1.1 is resumable
and can reuse any completed N1 work already present.
