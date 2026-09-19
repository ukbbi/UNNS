# Patch Notes — v2.5.0 to Audit/Repair v2.5.1

## Change 1 — numerical IQR fallback

Added:

```text
IQR_REL_ZERO_TOL = 1e-12
```

`resolveEpsScale()` selects the median fallback when the raw IQR is zero or only numerical residue relative to the median gap.

## Change 2 — nonterminal plateau

The adaptive-extension plateau is now a marker only.

The extension continues until:

- full connectivity is verified; or
- all scheduled probes are exhausted; or
- the exact threshold is above the safety probe cap; or
- the user stops the run.

## Change 3 — exact threshold reporting

Added `exactConnectivityThreshold()`.

The exact threshold and max adjacent sorted-gap separation are retained in the single-run and batch exports.

## Output changes

Batch CSV/JSON now include:

- `base_verdict`
- `verdict`
- `kappa_connect`
- `kappa_connect_exact`
- `iqr_raw`
- `eps_scale`
- `scale_mode`
- `iqr_effective_zero`
- `kappa_plateau_marker`
- `exact_probe_attempted`
- `exact_probe_connected`

## Provenance

The parent v2.5.0 chamber is not modified.
