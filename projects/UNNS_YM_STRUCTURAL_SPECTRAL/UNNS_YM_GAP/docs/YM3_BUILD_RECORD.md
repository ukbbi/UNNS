# YM3_BUILD_RECORD.md

## UNNS Yang–Mills Gap / Vacuum Boundary Non-Crossability
### YM-3A Input Construction Record

**Build:** `YM3_BUILD_v001`  
**Date:** 2026-09-30  
**Preregistration:** `YM3-PREREG v0.1.0`  
**Frozen chamber:** CORR-I v0.1.2  
**Scientific batch status:** **NOT RUN**

## Completed preregistered construction steps

1. Built all eight Class C massive inputs on the frozen common physical-time grid `u=t√σ`, `Δu=0.10383`, 11 points.
2. Verified the β = 6.50 unit-coordinate checksum against the frozen YM-2 massive plateau control.
3. Built all eight native-lattice diagnostic inputs (`n=0..10`).
4. Carried forward the frozen YM-2 Gamma reference family by a unit-only transformation to the common `u` coordinate.
5. Built the preregistered 8 × 5 β-matched Gamma sensitivity panel (`p=0.5,1,2,4,8`).
6. Added deterministic `build_inputs.py` / `verify_inputs.py` scripts and Windows `RUN_BUILD.bat` / `RUN_VERIFY.bat`.

## β = 6.50 checksum

- sampled correlator max absolute difference from frozen YM-2 control: `4.9960036108132044e-15`
- baseline: `POSITIVE-SPECTRAL CONSISTENT`
- plateau: PASS
- α = 0 identity null: PASS
- frozen YM-2 `R_contract`: `0.0076876493747382773`
- common-grid checksum `R_contract`: `0.0076876493747381931`
- absolute difference: `8.4134088584875144e-17`
- checksum: **PASS**

The checksum is limited to β = 6.50 as preregistered. No full eight-β CORR-I scientific batch was run during input construction.

## Next action

Run the complete preregistered YM-3A CORR-I batch, then calculate `S_fixed`, `S_match`, family ordering, and the native-grid window-sensitivity comparison before assigning a YM-3A outcome.
