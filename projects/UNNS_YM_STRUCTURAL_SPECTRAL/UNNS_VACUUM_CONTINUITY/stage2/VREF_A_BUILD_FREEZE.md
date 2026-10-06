# VREF_A_BUILD_FREEZE.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Branch:** VREF-I/A  
**Status:** **FROZEN — IMPLEMENTATION ADDENDUM, BEFORE EXECUTION**  
**Date:** 2026-09-30

## Purpose

`PREREG_VREF_I.md` froze the VREF-I/A geometry, source, primary interpolation, PCHIP sensitivity, metrics, and allowed calibration verdicts.

This addendum freezes the remaining implementation-level decision needed for an automatic reproducible calibration verdict. It does not change the physical scope or any primary metric.

## Executable freeze

Canonical executable configuration:

```text
chambers/vref_i/VREF_A_CONFIG.json
SHA-256: fbac5d1ae3a9e16ddba9380b88d5849cbd391f075c7d7ab72699262195ed45dd
```

Canonical chamber implementation at build time:

```text
chambers/vref_i/vref_a.py
SHA-256: 1620c1f82b0f714d1c5011dc5265ac6bd3c003e7966dd615b8f6bcb66f8b0392
```

## Frozen qualitative sensitivity rule

`CALIBRATION-SENSITIVE` is assigned if, and only if, the preregistered PCHIP central-profile sensitivity changes at least one of the following relative to the primary linear interpolation:

1. the sign classification of any common-grid profile value;
2. the direction signature of consecutive \(D_{RMS}(s)\) values for any refinement level;
3. the classification \(C(s)<1\), \(C(s)=1\), or \(C(s)>1\) for any fixed window;
4. the pairwise ordering of \(R_{12}(s)\), \(R_{23}(s)\), and \(R_{13}(s)\) for any fixed window.

If all mandatory source/integrity checks pass and none of these qualitative changes occurs, the automatic result is:

```text
CALIBRATION-VALID
```

A mandatory source/hash/support/unit/symmetry/ordering failure yields:

```text
CALIBRATION-INVALID
```

## Leave-one-out diagnostic

The preregistered leave-one-out linear interpolation diagnostic is recorded quantitatively, including residual/error and residual/signal ratios.

No post-hoc numerical threshold from that diagnostic is allowed to change the VREF-I/A verdict. It is descriptive and may inform the separately preregistered VREF-I/B design.

## Error envelope

For each fixed VREF window, the exact RMS extrema over the independent pointwise boxes

\[
z_j-\epsilon_j\le z_j'\le z_j+\epsilon_j
\]

are calculated using the nearest-to-zero and farthest-from-zero magnitude at every point.

These are sensitivity envelopes, not confidence intervals.

## Scope

This build remains calibration-only.

It cannot issue or imply either:

```text
CONTINUITY-SUPPORTED
ISOLATION-SUPPORTED
```

A separate VREF-I/B source and preregistration remain mandatory for Structural Vacuum Accessibility.
