# YM1A-G0.1 — Vacuum-Anchored Adversarial Family

**Status:** frozen correction to YM1A-G0  
**Input:** `ladders/ym1a_refinement.csv`  
**Primary chamber:** canonical STRUC-I v1.0.4  
**Secondary diagnostic:** STRUC-PERC-I v2.5.0

## Why G0.1 is necessary

The original G0 common-offset deformation translated all five positive spectral
levels together. STRUC-I operates on the ordered ladder's adjacent gaps. A
uniform translation of every ladder element leaves all adjacent gaps unchanged
and is therefore invisible to the chamber.

G0.1 makes the vacuum an explicit structural node:

\[
L_i^{YM}=(0,x_1,x_2,x_3,x_4,x_5).
\]

The first ordered gap is now the physical separation from the vacuum:

\[
\Delta_{vac}=x_1-0.
\]

The vacuum is fixed under every deformation.

## Primary adversary

For

\[
\epsilon=2^{-k},\qquad k=0,\ldots,10,
\]

and

\[
s=(1-\epsilon)x_1,
\]

define

\[
L_i^{offset}(\epsilon)
=
(0,x_1-s,x_2-s,x_3-s,x_4-s,x_5-s).
\]

Then

\[
\Delta_{vac}(\epsilon)=\epsilon x_1\to0^+,
\]

while every pairwise spacing among the five positive spectral coordinates is
preserved exactly.

## Matched massive control

\[
L_i^{up}(\epsilon)
=
(0,x_1+s,x_2+s,x_3+s,x_4+s,x_5+s).
\]

The same deformation magnitude moves the positive spectrum away from the
vacuum while preserving its internal additive geometry.

## Null N1 — homogeneous scale collapse

\[
L_i^{scale}(\epsilon)
=
(0,\epsilon x_1,\epsilon x_2,\epsilon x_3,\epsilon x_4,\epsilon x_5).
\]

This preserves ratios among positive spectral coordinates. It tests generic
sensitivity to absolute scale.

## Null N2 — gap-only deformation

\[
L_i^{gaponly}(\epsilon)
=
(0,\epsilon x_1,x_2,x_3,x_4,x_5).
\]

This isolates the mass-gap coordinate and tests whether a detected effect is
coordinate-local rather than a collective vacuum-offset effect.

## Frozen 0+ grid

The primary grid remains:

\[
1,\frac12,\frac14,\ldots,\frac1{1024}.
\]

The formal epsilon=0 endpoint is retained for documentation only and is not a
primary chamber input because c1 becomes degenerate with the vacuum.

## Chamber-ready representation

Every G1 input file is a one-column CSV with header `value` and exactly six
sorted scalar values. The same file is valid for both supplied canonical
chambers.

No chamber source code is altered.

## Supersession

`YM1A-G0` remains part of the project record but is superseded for the
vacuum-boundary test by `YM1A-G0.1`.
