# TC_PHYS_v001 — Result Summary

## Baseline result

Status: **PASS_PHYSICS_RECONSTRUCTION**

Using the paper's stated baseline thresholds (`W0 = 0.15`, `Wf/W0 = 2/3`), the reconstruction gives:

- raw discrete variance maximum: epsilon = **0.090**
- grid-derived smoothed variance peak: epsilon = **0.0755**
- segmented depolarization break: epsilon = **0.080**
- two-indicator consensus: epsilon = **0.07775**
- published reference: epsilon_c approximately **0.075**
- absolute consensus difference: **0.00275**

The representative epsilon=0.05 standard run retains a strong late 2T response, while the epsilon=0.50 run depolarizes rapidly. The reconstructed half-frequency response ratio is approximately **31.53**.

## Important qualification

The raw discrete critical-fluctuation maximum is at epsilon=0.09; the value near 0.075 emerges after a light smoothing whose bandwidth is generated from the epsilon grid rather than set to the published answer.

Threshold sensitivity is exported in `outputs/mitigation_sensitivity.csv`. The subharmonic-variance peak is comparatively stable; the reconstructed decay-break location is more threshold-sensitive. This is why the package reports all raw, smoothed, and sensitivity results rather than only the favorable number.

No UNNS quantity has been calculated yet.
