# BAKE-OFF v001 — FINDINGS

## Status

**DIAGNOSTIC ONLY — NO GRAMMAR FROZEN**

The three planned representations were evaluated on the 13 neutral ingestion records.
No admission threshold or verdict was defined.

## Finding 1 — The frequency lattice is the strongest of the three first-pass representations, but it is not sufficient

For Luo's DTQC development records, the 2D lattice reduces spectral residual strongly relative to a 1D harmonic family:

- LUO_M_N32: lattice gain = 23.6635 Fourier-bin units
- LUO_F_N40: lattice gain = 23.7627
- LUO_EE_DTQC_N32: lattice gain = 19.0464

The low-frequency aperiodic control is much weaker:

- LUO_EE_LOW_N32: lattice gain = 2.5947

However, the high-frequency decoupled control remains strongly two-frequency/lattice organized:

- LUO_EE_HIGH_N32: lattice gain = 16.4302

Therefore, a 2D spectral lattice detects a real multi-frequency organization axis, but it does not by itself distinguish coupled DTQC organization from two effectively decoupled DTC responses.

## Finding 2 — Observable-derived torus predictability fails specificity

For the entanglement-entropy triplet (N=32):

- low-frequency control: torus R^2 = 0.9254
- DTQC regime: torus R^2 = 0.7171
- high-frequency decoupled control: torus R^2 = 0.9235

The proper DTQC regime does not maximize the observable-derived torus score.

Conclusion: inferring a phase torus from the scalar observable's own strongest spectral basis is not an admissible successor grammar in this form.

A physically defined torus should instead use source-defined drive phases/event coordinates.

## Finding 3 — Vector recurrence also fails as a standalone discriminator

For the entanglement-entropy triplet (N=32):

- low-frequency control: best pair recurrence = 0.4433
- DTQC regime: best pair recurrence = 0.7153
- high-frequency decoupled control: best pair recurrence = 0.8849

Again, the decoupled control can exceed the DTQC regime.

In Huang Figure 2 the recurrence-pair diagnostic is also almost saturated for both the quasi-periodic and chaotic records:

- HUANG_QP = 0.9991
- HUANG_CHAOS = 0.9990

Thus carrier recurrence is too easy to obtain and is not a sufficient signature of organized multi-clock order.

## Finding 4 — The negative result is reproducible across Luo system sizes

The paired N=12 / N=32 entanglement records give nearly identical bake-off values within each regime.

This means the failure of specificity above is not an obvious finite-size or numerical accident.

## Structural interpretation

The first bake-off suggests at least two separable axes:

1. **multi-frequency / lattice organization**
2. **inter-subsystem coupling / collective organization**

The high-frequency Luo control preserves strong two-frequency organization while the physical system becomes effectively decoupled. A successful multi-clock grammar therefore cannot be purely spectral or purely recurrent.

This parallels the previous TIME-CRYSTAL-I lesson that recurrence alone is not equivalent to many-body time-crystalline admissibility.

## Next method target

Do NOT tune any of the v001 scores into a threshold.

The next development step is to construct a **source-defined drive-phase torus** for Luo, using the independently specified two-drive relation, and pair it with a coupling-sensitive coordinate rather than deriving both clocks from the measured scalar observable.

Huang remains an adjacent-domain challenge: it should not determine a DTQC threshold.
