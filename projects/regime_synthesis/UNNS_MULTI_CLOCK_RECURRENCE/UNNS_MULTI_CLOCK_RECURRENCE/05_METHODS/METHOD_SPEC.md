# MULTI-CLOCK REPRESENTATION BAKE-OFF v001

## Status
DIAGNOSTIC ONLY. No admission threshold, no classifier, no frozen grammar, no C003 use.

## Purpose
Compare three candidate representations on the neutral ingestion corpus before any one of them is promoted into a UNNS multi-clock grammar.

## Input
Only records marked `INGESTED` in `04_CORPUS/CORPUS_v001.csv`.

No publisher-provided FFT columns are used. No smoothing or interpolation is applied.

For cross-record comparability inside the diagnostics only, each observable is centered and divided by its own standard deviation. This does not modify the canonical ingested CSVs.

## Representation A — Vector recurrence

A biased FFT autocorrelation is computed from the centered/scaled observable:

`A(q) = <z_t z_(t+q)> / <z_t^2>`

and the recurrence coherence is:

`R(q) = |A(q)|`.

To avoid the trivial near-unity coherence at adjacent samples of a smooth trajectory, the search starts at one quarter of the strongest signal-derived carrier period.

The strongest local recurrence lags are retained. For lag pair `(q1,q2)`, the diagnostic parallelogram score is the geometric mean of coherence at:

- `q1`
- `q2`
- `|q2-q1|`
- `q1+q2`

when all are inside the fixed search horizon.

This is a representation diagnostic, not a DTQC order parameter.

## Representation B — Observable-derived phase torus

This first bake-off intentionally asks whether a usable two-phase chart can be inferred from the observable alone.

A fixed signal-derived basis is used:
1. `f1` = strongest non-zero local spectral peak.
2. `f2` = strongest local peak that is not a low-order harmonic/subharmonic of `f1` within three Fourier bins.

The phases are:

`theta_1(t) = 2*pi*f1*t mod 2*pi`
`theta_2(t) = 2*pi*f2*t mod 2*pi`.

The observable is predicted from nearest neighbors on the embedded torus:
`(cos theta1, sin theta1, cos theta2, sin theta2)`.

Reported diagnostics:
- 2D torus prediction R^2
- gain over the better one-phase model
- excess over a fixed-seed shuffled-observable null

Important: this is NOT yet the source-defined physical drive torus.

## Representation C — Frequency lattice

Using the same fixed `(f1,f2)` basis, the strongest observed peaks are compared with:

1D family:
`k*f1`, `k=1..12`

2D family:
`|m*f1+n*f2|`, `m,n in [-5,5]`, excluding `(0,0)`.

Reported diagnostics:
- weighted residual in Fourier-bin units for 1D and 2D fits
- 2D gain over 1D
- weighted peak coverage within two Fourier bins
- basis ratio and distance to the nearest rational with denominator <= 8

No numerical cutoff is used to label a record.

## Firewall
- C003 is not loaded.
- ZHU_2026 is not loaded.
- MOON_2025 is not loaded while access remains restricted.
- Physical source roles are retained only for post-diagnostic comparison.
- No representation is declared successful merely because a known positive scores highly.

## Reproducibility
Fixed random seed: 20260826.
