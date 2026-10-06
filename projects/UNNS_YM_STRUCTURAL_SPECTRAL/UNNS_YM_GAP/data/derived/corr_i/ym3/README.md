# YM-3A Input Build

**Project:** `UNNS_YM_GAP`  
**Preregistration:** `YM3-PREREG v0.1.0`  
**Build status:** inputs constructed; full scientific CORR-I batch not run  
**Frozen chamber:** CORR-I v0.1.2

## Built material

- `common/` — eight Class C massive controls on the frozen common physical-time grid, plus `massive_all.csv`.
- `native/` — eight Class C native-lattice diagnostic controls, plus `massive_all.csv`.
- `fixed_gapless/` — the frozen YM-2 Gamma references transformed by units only.
- `matched_gapless/` — the preregistered 8 × 5 Gamma sensitivity panel, with per-β files and `matched_all.csv`.
- `scripts/ym3/` — deterministic builders and verification scripts with Windows batch launchers.
- `output/ym3/checksum/` — input verification and the β=6.50 checksum only.

## Frozen primary grid

`u = t*sqrt(sigma)`, `du = 0.10383`, 11 points, `0 <= u <= 1.0383`.

## β=6.50 checksum

The generated β=6.50 common-grid samples reproduce the frozen YM-2 massive-control samples after coordinate conversion. The checksum mirror of the frozen CORR-I equations reproduces `R_contract` within numerical serialization tolerance. See `output/ym3/checksum/b650_checksum.json`.

## Important

No eight-β CORR-I result has been generated here. This package completes preregistration steps 2–7 (construction/verification) and stops before scientific batch execution (step 8).
