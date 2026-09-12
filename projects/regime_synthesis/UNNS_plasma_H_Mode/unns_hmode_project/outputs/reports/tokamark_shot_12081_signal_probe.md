# TokaMark One-Shot Array Probe — Shot 12081

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12081.zarr/`

## Load status

- loaded arrays: `2`
- failed arrays: `14`

### Failed arrays

- `summary_power_nbi`: `KeyError('Missing array metadata: summary/power_nbi/.zarray')`
- `summary_ip`: `KeyError('Missing array metadata: summary/ip/.zarray')`
- `interferometer_n_e_line`: `KeyError('Missing array metadata: interferometer/n_e_line/.zarray')`
- `dalpha_voltage`: `KeyError('Missing array metadata: spectrometer_visible/filter_spectrometer_dalpha_voltage/.zarray')`
- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`
- `equilibrium_q95`: `KeyError('Missing array metadata: equilibrium/q95/.zarray')`
- `equilibrium_elongation`: `KeyError('Missing array metadata: equilibrium/elongation/.zarray')`
- `equilibrium_triangularity_upper`: `KeyError('Missing array metadata: equilibrium/triangularity_upper/.zarray')`
- `equilibrium_triangularity_lower`: `KeyError('Missing array metadata: equilibrium/triangularity_lower/.zarray')`
- `equilibrium_minor_radius`: `KeyError('Missing array metadata: equilibrium/minor_radius/.zarray')`
- `equilibrium_beta_normal`: `KeyError('Missing array metadata: equilibrium/beta_normal/.zarray')`
- `equilibrium_beta_pol`: `KeyError('Missing array metadata: equilibrium/beta_pol/.zarray')`
- `equilibrium_whmd`: `KeyError('Missing array metadata: equilibrium/whmd/.zarray')`

## Signal summaries

| label        | values_shape   | time_shape   |   finite_fraction |        min |      median |      mean |      max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:-------------|:---------------|:-------------|------------------:|-----------:|------------:|----------:|---------:|-----------:|-----------:|--------------------:|-----------------:|
| soft_x_lower | (18, 19470)    | (19470,)     |          0.848433 | -0.0094223 | 0.000190735 | 0.0159321 | 0.3125   |     -0.069 |    0.32038 |                   8 |                0 |
| soft_x_upper | (18, 19470)    | (19470,)     |          0.848433 | -0.0780869 | 0.00043869  | 0.0109159 | 0.290222 |     -0.069 |    0.32038 |                   8 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |       mean |       max |        std |
|:------------------------------------|------------------:|------------:|------------:|-----------:|----------:|-----------:|
| soft_x_lower_median_across_channels |          0.848433 | -0.00511169 | 0.000972748 | 0.00219522 | 0.0262833 | 0.00326213 |
| soft_x_upper_median_across_channels |          0.848433 | -0.00404358 | 0.000476837 | 0.00213989 | 0.0138855 | 0.00354806 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.