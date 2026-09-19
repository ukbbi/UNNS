# Corpus

The frozen v0.1 corpus contains **30 exact algebraic systems**:

- 6 `INT_FREE`
- 6 `R1_FREE`
- 6 `R1_FAIL`
- 6 `AFF_FREE`
- 6 `AFF_FAIL`

The corpus was inherited from the common-refinement investigation and frozen before any chamber run.

## Algebraic annotations

The machine labels:

```text
TRACEABLE
NON_TRACEABLE
```

are exact algebraic annotations derived from the parent project.

In the current `UNNS_ADMISSIBILITY_PERCOLATION` project they are **not chamber verdicts** and are
not treated as the definition of admissibility or percolation.

They are controlled external metadata that may help interpret chamber behavior.

## Files

- `CORPUS_INDEX.csv` — compact index.
- `CORPUS_AUDIT.json` — build/validation audit.
- `cases/` — full machine-readable exact system definitions and witnesses.
- `LADDER_INDEX.csv` — primary spectrum generation metadata.
- `ladders/` — canonical system spectra and detailed enumeration records.

The corpus was generated reproducibly by `scripts/BUILD_CORPUS.py`.
