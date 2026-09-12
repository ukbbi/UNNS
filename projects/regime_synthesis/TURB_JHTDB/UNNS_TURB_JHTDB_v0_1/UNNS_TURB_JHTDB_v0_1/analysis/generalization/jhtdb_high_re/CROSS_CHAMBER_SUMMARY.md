# High-Re Spatial-Generalization — Cross-Chamber Synthesis

**Status:** HIGH-RE GENERALIZATION BRANCH COMPLETE

## Primary result — STRUC-I v1.0.4

The preregistered high-Re endpoint is met:

`PILOT_A_SCALE_REGIME_RECURRENCE`

At 10,000 MC:
- i8192_s00 — Structural Instability / Random Structure
- i8192_s01 — Structural Instability / Random Structure
- i8192_s02 — Structural Boundary / Near-Critical Structure
- i8192_s03 — Structural Instability / Random Structure
- i8192_s04 — Structural Instability / Random Structure
- i32768_s00 — Structural Instability / Random Structure

Thus 4/5 isotropic8192 primary snapshots recur in the Pilot-A instability regime,
and the isotropic32768 extreme-Re snapshot also recurs in that regime.

The prespecified low-Re contrast i8192_s05 is:
**Structural Boundary / Transitional Structure**.

## Secondary result — STRUC-PERC-I v2.5.0

All seven frozen P_SCALE ladders return:
- FULL_PERCOLATION
- giant ratio = 1.0
- isolated vertices = 0
- κ_connect = 0.01
- 17/17 layers complete

Because the canonical Generic adapter reduces these strongly quantized ladders to
only 3–4 gap vertices, this stage is descriptive rather than inferential.

## Cross-chamber interpretation

The result sharpens a recurring UNNS distinction:

`CONNECTIVITY ≠ ADMISSIBILITY`

Every high-Re and contrast ladder remains fully connected in STRUC-PERC-I, while
STRUC-I separates them into Structural Instability and Structural Boundary states.
Therefore percolation/connectivity alone does not determine the structural regime.

The high-Re branch supports recurrence of the Pilot-A scale regime across a very
large increase in Reynolds number / grid resolution. It does not support the
alternative high-Re stabilization hypothesis.

No monotonic Reynolds-number law is claimed from the single low-Re contrast.

## Status of the larger program

This completes the preregistered high-Re spatial-generalization branch.
Pilot B remains separately frozen and pending acquisition of its isotropic1024coarse
spatiotemporal source window.
