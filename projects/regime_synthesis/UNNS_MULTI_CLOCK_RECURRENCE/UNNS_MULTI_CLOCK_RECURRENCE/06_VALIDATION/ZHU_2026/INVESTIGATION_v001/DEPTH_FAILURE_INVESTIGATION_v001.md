# DEPTH FAILURE INVESTIGATION v001

## Status

**POST-VALIDATION DIAGNOSTIC ONLY.**

This investigation does not modify, reinterpret, or replace the locked result
`ZHU_VALIDATION_v001 = PARTIAL_TRANSFER_WITH_COVER_DEPTH_FAILURE`.

## Diagnosis

The v002 depth optimizer compared physically different sectors with one objective:
maximum cross-validated explained variance.

For the Zhu source clocks `f1 = 88 kHz` and `f2 = 54.387 kHz`:

### d = 1

The v002 basis is

- `f2`
- `f1`
- `|f1-f2|`
- `f1+f2`

This is the **integer source/mixing lattice**. It does not represent a broken
subharmonic cover.

### d = 2

The basis is

- `f2/2`
- `f1/2`
- `|f1-f2|/2`
- `(f1+f2)/2`

This is the first **fractional cover sector**, matching the half-integer
combination structure relevant to the published Z2 x Z2 DTQC response.

Therefore selecting `argmax_d full_r2_cv(d)` allows strong parent-drive or
integer-mixing content to defeat the physically emergent fractional sector.

## Why Luo hid the problem

For the Luo DTQC entanglement record N=32:

- d=1 full R2 ~ 0.0125
- d=2 full R2 ~ 0.9409

The entanglement observable contains little direct source-synchronous content,
so the selector naturally chose d=2.

For Zhu transmission, direct source/mixing components remain strong.

## Zhu mode decomposition

`ZHU_FIG1_C1` is primarily source-axis dominated at d=1.

`ZHU_FIG1_C3` is primarily integer-difference dominated at d=1:
the single `|f1-f2|` mode alone gives cross-validated R2 ~ 0.4706.

Nevertheless, the d=2 half-difference sector remains real.

The publisher-supplied paired spectra show:

- C1/C2: integer difference peak ~ 0.07696; half-difference peak ~ 0.02359
- C3/C4: integer difference peak ~ 0.10382; half-difference peak ~ 0.06155

The second trajectory therefore carries substantially stronger fractional
content, even though total variance is still maximized by the integer sector.

## Nested fractional-cover diagnostic

Define the integer parent basis:

`B_Z = B(d=1)`

and, for d >= 2,

`Delta_frac(d) = R2_CV(B_Z union B(d)) - R2_CV(B_Z)`.

This asks whether a fractional cover contributes predictive structure
**beyond what the source/mixing lattice already explains**.

Results:

### Zhu

- C1: Delta_frac(2) = 0.094971
- C3: Delta_frac(2) = 0.289135

For both records d=3 and d=4 are negative.

The d=2 gain remains positive under every frozen v002 robustness perturbation.

### Luo N=32

- LOW:  Delta_frac(2) = 0.128645
- DTQC: Delta_frac(2) = 0.942075
- HIGH: Delta_frac(2) = 0.698576

Again, d=3 and d=4 are negative.

## Interpretation

The external validation did **not** show that the d=2 sector disappeared.

It showed that `maximum total torus predictability` is the wrong selector for
subharmonic cover depth when the measured observable retains strong integer
source/mixing components.

The portable phenomenon is better described as:

1. integer source/mixing organization,
2. additional fractional-cover organization,
3. independent collective/coupling evidence.

The high-frequency decoupled Luo control still has a large d=2 fractional-cover
gain, so fractional temporal structure alone remains insufficient for DTQC
admissibility. The independent coupling/collective sector remains necessary.

## Consequence for the next method

A future v003 is scientifically justified, but should not simply hard-code d=2
or delete d=1.

The principled candidate architecture is:

`integer parent lattice -> fractional cover gain -> coupling/collective sector`

with d=1 treated as the parent/source sector and d>=2 as candidate broken-symmetry
cover sectors.

Any v003 thresholds/null tests must be developed separately. C003 remains
quarantined.
