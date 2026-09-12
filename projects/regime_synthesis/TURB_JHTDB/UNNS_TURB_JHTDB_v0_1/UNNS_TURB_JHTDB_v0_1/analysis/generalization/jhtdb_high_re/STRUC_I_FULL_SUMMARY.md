# High-Re STRUC-I Primary vs Contrast

**Status:** STRUC-I PRIMARY + CONTRAST FROZEN

## Primary conclusion

The preregistered high-Re endpoint remains:

`PILOT_A_SCALE_REGIME_RECURRENCE`

At 10,000 Monte Carlo runs:
- 4/5 isotropic8192 primary snapshots are **Structural Instability / Random Structure**.
- isotropic32768 snapshot 0 is **Structural Instability / Random Structure**.
- isotropic8192 snapshot 2 is the robust exception: **Structural Boundary / Near-Critical Structure**.

## Prespecified low-Re contrast

`i8192_s05_P_SCALE` is:

- **Structural Boundary**
- **Transitional Structure**
- mean Aκ = 0.764437
- min Aκ = 0.7317
- Aκ(κ=1) = 0.8828
- mean ρ = 0.948833
- n = 26

The contrast mean Aκ is 0.174437
above the six-sample primary mean.

## Interpretation

The low-Re contrast is structurally separated from the dominant high-Re result:
the primary group is overwhelmingly in **Structural Instability**, while the
prespecified contrast lies in **Structural Boundary / Transitional Structure**.

This strengthens the high-Re recurrence result as an internal contrast, but it
does **not** establish a general monotonic Reynolds-number law. There is only one
low-Re contrast snapshot, and it is much smaller (`n=26`) than the primary ladders.

## Next locked step

Run all seven frozen `P_SCALE` ladders through canonical **STRUC-PERC-I v2.5.0**
with its generic adapter unchanged. Because the ladders are strongly quantized
and the generic adapter deduplicates exact values, this stage is secondary /
descriptive and must not be repaired with jitter or altered multiplicities.
