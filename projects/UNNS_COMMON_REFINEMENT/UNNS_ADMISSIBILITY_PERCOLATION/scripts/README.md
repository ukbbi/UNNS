# Scripts

The build scripts reproduce the frozen v0.1 corpus and ladder inputs.

Windows:

```text
scripts\RUN_BUILD.bat
```

Sequence:

1. `BUILD_CORPUS.py` — regenerates the 30 exact algebraic source systems and annotations.
2. `BUILD_LADDERS.py` — builds the label-blind 128-level `SYSTEM_SPECTRUM` ladders.
3. `FREEZE.py` — records SHA-256 hashes of the original frozen protocol, adapter, chamber files and chamber inputs.
4. `VERIFY.py` — verifies the frozen hashes.

These scripts do **not** run STRUC-I or STRUC-PERC-I.

## Rename note

The scripts were created under the provisional project identifier
`UNNS_TRACEABILITY_PHENOTYPE`.

Do not edit the frozen-build logic merely to rename that historical identifier.

The current project identity is documented at the top level by:

`README.md`
`RENAME_RECORD.md`
`PROTOCOL_AMENDMENT_001.md`


## Post-batch audit

`AUDIT_PERC_CONNECTIVITY.py`

Deterministically audits the STRUC-PERC-I full-pairwise gap graph and reproduces the chamber's
adaptive-extension behavior without modifying the chamber file.

It writes:

`outputs/records/PERC_CONNECTIVITY_AUDIT.csv`
`outputs/records/PERC_CONNECTIVITY_AUDIT.json`
