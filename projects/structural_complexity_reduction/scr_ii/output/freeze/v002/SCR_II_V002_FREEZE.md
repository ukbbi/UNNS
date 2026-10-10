# SCR-II v002 Freeze Record

**Status:** `FROZEN`  
**Scientific status:** `SCR_II_V002_COMPLETE_NON_TRANSFER`  
**Primary verdict:** `PRESERVATION_FAIL`  
**Benchmark:** `ROUTE_CSP_I/v002`  
**Preregistration:** `SCR_II_PREREG_v002`

## Canonical interpretation

SCR-II v002 is complete and frozen as a **non-transfer result**.

The frozen structural filter achieved extreme search contraction and runtime reduction, but exact-solution preservation failed across the primary grid. This phase therefore establishes a transfer boundary rather than a valid solver acceleration.

## Immutable scientific records

- `SCR_II_V002_RESULT_RECORD.md`
- `SCR_II_V002_ANALYSIS.md`
- `SCR_II_TRANSFER_BOUNDARY.md`
- `SCR_II_V002_FINAL.json`

## Canonical placement

```text
scr_ii/
└── output/
    ├── reports/
    │   └── v002/
    │       ├── SCR_II_V002_RESULT_RECORD.md
    │       ├── SCR_II_V002_ANALYSIS.md
    │       └── SCR_II_TRANSFER_BOUNDARY.md
    ├── exports/
    │   └── v002/
    │       └── SCR_II_V002_FINAL.json
    └── freeze/
        └── v002/
            ├── SCR_II_V002_FREEZE.md
            ├── SCR_II_V002_FREEZE.json
            └── SHA256SUMS.txt
```

## Freeze rules

1. Do not rerun the v002 primary.
2. Do not modify its preregistration, seeds, thresholds, primary verdict, or consolidated records.
3. Preserve the raw primary output and completed checkpoint as provenance.
4. Any continuation must use a new version or a new research phase.

## Immutable-file SHA-256

- `5085293b822b3bccd10d6e728fe51d113157eab7ee946f09c4854e72ea0d053b`  `output/reports/v002/SCR_II_V002_RESULT_RECORD.md`
- `94e5e516dee64d9fbc2238797fd2853231607b2150999ca46afed6ebd92a6188`  `output/reports/v002/SCR_II_V002_ANALYSIS.md`
- `d6eb8fdbadd73e4666c52bfd68d5000d585751a2e4d323abb209b0c1d22717a3`  `output/reports/v002/SCR_II_TRANSFER_BOUNDARY.md`
- `1a46b16aeee11affa1073f14c3bae1bcf496e8f6eaf721d2e150860a28298c6f`  `output/exports/v002/SCR_II_V002_FINAL.json`
