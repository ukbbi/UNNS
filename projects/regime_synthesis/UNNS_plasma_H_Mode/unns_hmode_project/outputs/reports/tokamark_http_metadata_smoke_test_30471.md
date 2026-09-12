# TokaMark HTTP Metadata Smoke Test — Shot 30471

Status: `PASS`

## Metadata URL

`https://s3.echo.stfc.ac.uk/mast/tokamark/v1/30471.zarr/.zmetadata`

## Required signal availability

- signals present: `9/15`
- signals with values metadata: `9/15`
- signals with time metadata: `9/15`

| signal | present | values | time | values_shape | time_shape |
|---|---:|---:|---:|---|---|
| `summary-power_nbi` | True | True | True | `[1284]` | `[1284]` |
| `summary-ip` | True | True | True | `[1284]` | `[1284]` |
| `pulse_schedule-i_plasma` | False | False | False | `` | `` |
| `pulse_schedule-n_e_line` | False | False | False | `` | `` |
| `interferometer-n_e_line` | True | True | True | `[1284]` | `[1284]` |
| `spectrometer_visible-filter_spectrometer_dalpha_voltage` | True | True | True | `[3, 16041]` | `[16041]` |
| `thomson_scattering-t_e` | False | False | False | `` | `` |
| `thomson_scattering-n_e` | False | False | False | `` | `` |
| `soft_x_rays-horizontal_cam_lower` | False | False | False | `` | `` |
| `soft_x_rays-horizontal_cam_upper` | False | False | False | `` | `` |
| `equilibrium-q95` | True | True | True | `[65]` | `[65]` |
| `equilibrium-elongation` | True | True | True | `[65]` | `[65]` |
| `equilibrium-triangularity_upper` | True | True | True | `[65]` | `[65]` |
| `equilibrium-triangularity_lower` | True | True | True | `[65]` | `[65]` |
| `equilibrium-minor_radius` | True | True | True | `[65]` | `[65]` |

## Interpretation

The public metadata is reachable, but some required candidate signals are absent in this shot.