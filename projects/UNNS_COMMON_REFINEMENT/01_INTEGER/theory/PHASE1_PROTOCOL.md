# PHASE 1 FROZEN PROTOCOL

## Domain
Positive integers only.

## Endpoint condition
`a*b = c*d`.

## Primary chamber
`REF-I` determines endpoint equivalence, constructs the canonical gcd witness, and verifies all four refinement identities.

## Canonical witness
- `e = gcd(a,c)`
- `f = a/e`
- `g = c/e`
- `h = b/g = d/f`

## Refinement classes
- `E`: endpoint equivalent (`ab=cd`)
- `R`: endpoint equivalent and a valid witness exists
- `NR`: endpoint equivalent and no admissible witness exists
- `D_R = 0` for R, `D_R = 1` for NR

## Canonical Phase-1 ladder encoding
With the frozen ascending prime basis `p_1,...,p_m`:
`L_x(k) = sum_{i<=k} v_{p_i}(x) log(p_i)`.

The adapter may generate:
- route AB signatures
- route CD signatures
- refinement signatures from E,F,G,H

## Secondary chambers
STRUC-I v1.0.4 and STRUC-PERC-I v2.5.0 are used unchanged.
Their outputs are secondary diagnostics and cannot override REF-I's exact refinement verdict.

## Freeze rule
Do not change the witness construction or ladder encoding during Phase 1.
Any alternative encoding belongs to a separately versioned comparison experiment.
