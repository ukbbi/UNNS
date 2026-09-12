# TC_P01_C003 v001 — Adapter Method

## Purpose

C003 is the first deliberate quasi-periodic boundary test of
`TIME-CRYSTAL-I v1.1.0`.

## Source

`rawdata.xls`, sheet `Fig. 1`.

The source workbook contains representative signed polarization dynamics from
a quasi-periodically driven interacting NV-spin ensemble.

## Fixed candidate/control mapping

Before chamber evaluation:

- neutral candidate `TC_P01_C003` was fixed to the robust long-interaction
  representative dynamics;
- neutral control `TC_P01_C003_CTRL` was fixed to the short-interaction
  breakdown regime.

The physical figure identities are stored only in separate ground-truth files.

## Why a dual-clock adapter is required

The source experiment has two incommensurate drive clocks and no single
ordinary Floquet stroboscopic time.

The frozen TIME-CRYSTAL-I closure implementation requires at least two
simultaneous coordinates.

A one-observable direct ingestion was therefore rejected by the chamber input
contract before any scientific verdict was produced.

The frozen C003 adapter consequently uses the physical two-clock structure
already present in the experiment:

```text
X_n = [ Sx(n tau1), Sx(n tau2) ]
```

using only measured samples that exist in the workbook.

The source workbook stores the union of these pulse-event times in units of
`tau1`, with the documented ratio `tau2/tau1 = 1.618`.

## No synthetic interpolation

For each common event index `n`, the adapter pairs:

- the stored measurement at the `n`th `tau1` event;
- the stored measurement at the `n`th `tau2` event.

No values are interpolated.

No response frequency is supplied.

## Adapter firewall

The adapter does not:

- resample onto a uniform time grid;
- insert an expected DTQC frequency;
- Fourier filter;
- align signs;
- synthesize missing observations;
- select a favorable sub-window;
- modify `qmax`;
- modify any TIME-CRYSTAL-I threshold.

The exact same transform is applied to candidate and control.
