# MALZ–SMITH SPECIFICITY VALIDATION PROTOCOL v001

## Status

**PRE-ANALYSIS LOCK**

This protocol is written before reading any numerical data file or source-code content
inside `qubit-topological-floquet-v2.0.zip`.

The archive filenames/extensions were inventoried only to establish data availability.
No trajectory values, spectra, simulation outputs, or code logic were inspected before lock.

## Purpose

Challenge `FRACTIONAL_COVER_v003` with an independent physical system that has:

- two externally imposed incommensurate clocks,
- genuine time-domain dynamics,
- no DTQC claim,
- multiple physical regimes under the same two-clock drive.

This is a **specificity / falsification test**, not a positive-DTQC validation.

The central question is:

> Does v003 merely detect generic two-clock quasiperiodic organization, or does its
> fractional-cover sector remain structurally distinct when the system is organized by
> two clocks for a different physical reason?

## Frozen v003 method

The following are immutable:

- parent depth: `d = 1`
- fractional depths: `d = 2,3,4`
- first-order basis only
- integer parent basis:
  - `1`
  - `r`
  - `|r-1|`
  - `r+1`
- fractional axis basis at depth d:
  - `1/d`
  - `r/d`
- fractional mixed basis at depth d:
  - `|r-1|/d`
  - `(r+1)/d`
- deterministic contiguous 5-fold cross-validation
- ridge alpha `1e-9`
- descriptive fractional depth:
  `argmax_{d>=2} frac_total_gain(d)`
- no classification threshold
- no verdict

Reported quantities:

- `parent_full_r2_cv`
- `parent_mixed_gain`
- `frac_axis_gain(d)`
- `frac_mixed_gain(d)`
- `frac_total_gain(d)`
- `best_fractional_depth`

## Source-defined clocks

The Malz–Smith experiment is driven by two externally specified incommensurate angular
frequencies `omega1` and `omega2`, with source ratio fixed by the experiment.

The adapter must use the **published/source-defined clock ratio only**.

No response peak, FFT maximum, fitted oscillation frequency, or optimized ratio may be used
to define the torus.

The actual source frequency values and time units will be taken directly from the supplied
metadata/code/data only after this protocol is locked.

## Observable policy

Primary admissible inputs are genuine source time-domain observables, preferably measured
tomographic components such as:

- `<sigma_x(t)>`
- `<sigma_y(t)>`
- `<sigma_z(t)>`

If the archive contains both experiment and simulation, they must remain separate records.

No inverse Fourier reconstruction is permitted.

No interpolation is permitted unless the source representation itself requires a fixed grid
and the interpolation rule is documented before the metric run.

## Physical-regime policy

The validation should exploit source-native regime labels/control parameters, especially the
same two-clock drive across distinct physical regimes.

The archive must be inspected after lock to identify which records correspond to:

- topologically non-trivial regimes,
- trivial regimes,
- transition/near-gap-closing regimes,
- experiment versus simulation if both are present.

No regime may be renamed according to v003 output.

## Predeclared specificity expectations

Because this system is genuinely quasiperiodically driven, substantial integer-parent
organization is allowed and expected.

The test is **not** failed merely because:

- `parent_full_r2_cv` is large,
- fractional cover gain is positive,
- `d=2` is selected.

Instead, v003 specificity is challenged if the non-DTQC system reproduces the complete
Luo-DTQC pattern without meaningful regime discrimination.

The principal predeclared questions are:

1. Does `frac_total_gain` vary systematically across the system's native physical regimes?
2. Is `frac_mixed_gain` specifically enhanced in only part of the phase structure, or is it
   generically large everywhere?
3. Does `best_fractional_depth` remain stable across all regimes regardless of physical state?
4. Does v003 distinguish parent-lattice organization from fractional-cover organization?
5. Does the trivial/non-trivial transition create a structural change in the v003 coordinates?

## Falsification / weakening conditions

v003 specificity is weakened if:

- all regimes exhibit essentially the same strong fractional-cover signature,
- the fractional coordinates track only generic drive quasiperiodicity and ignore the
  native phase structure,
- results depend on retuning the source ratio, cover depths, basis order, or CV rule,
- interpretation requires introducing a threshold after seeing the data.

## Positive outcome

A useful result does NOT require this non-DTQC system to have zero fractional gain.

A strong specificity result would be:

- integer-parent organization persists broadly,
- fractional-cover structure changes with physical regime,
- the coordinate pattern differs materially from the Luo DTQC / controls,
- no DTQC-like admissibility claim is produced from temporal structure alone.

## Firewall

- no C003 data
- no Zhu-derived retuning
- no Luo-derived threshold
- no response-frequency fitting
- no target-frequency injection
- no synthetic reconstruction
- no publisher FFT as time-series input
- quantitative outputs must be hashed before interpretation
