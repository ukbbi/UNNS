# Reproducible Synthesis Build

Run on Windows:

```text
scripts\RUN_SYNTHESIS.bat
```

Or directly:

```text
python scripts/BUILD_SYNTHESIS.py
```

Check without rewriting:

```text
python scripts/BUILD_SYNTHESIS.py --check
```

The builder validates pinned canonical evidence from the integer baseline, rank-one failures,
affine controls, and the Conway/PDS source audit, then regenerates the approved five synthesis
artifacts byte-for-byte.

Pinned inputs:
`scripts/SYNTHESIS_INPUTS.json`

Build record:
`outputs/records/SYNTHESIS_BUILD.json`

Reproducibility report:
`outputs/reports/SYNTHESIS_REPRODUCIBILITY.md`

If any pinned input changes, the build stops and requires a fresh evidence audit before repinning.
