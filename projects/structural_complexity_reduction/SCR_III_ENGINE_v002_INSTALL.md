# SCR_III_ENGINE_v002 — Install

Extract this ZIP directly into the existing `structural_complexity_reduction\` project root.

The package is additive. It creates v002 runners and modules and does not replace v001 runners or v001 audit results.

Required before installation:
- root `SCR_III_COUPLING_SPEC_v002.md`
- root `SCR_III_STRUCTURE_v002.md`
- root `SHA256SUMS_SCR_III_v002.txt`
- `scr_iii\SCR_III_PREREG_v002\SCR_III_PREREG_v002.md`
- `scr_iii\SCR_III_PREREG_v002\SEEDS_v002.json`
- `scr_iii\SCR_III_PREREG_v002\SOURCE_LOCK_v002.md`

The stale file `scr_iii\SCR_III_COUPLING_SPEC_v001.md`, if still present, is noncanonical and should be deleted manually. The engine does not delete user files.

First run only:

```text
RUN_SCR_III_V002_VALIDATE.bat
```

The v002 batch files pause on both success and failure so the terminal result remains visible.
