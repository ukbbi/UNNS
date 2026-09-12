# TokaMark One-Shot Array Probe — Shot 12082

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12082.zarr/`

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

| label        | values_shape   | time_shape   |   finite_fraction |         min |       median |       mean |     max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:-------------|:---------------|:-------------|------------------:|------------:|-------------:|-----------:|--------:|-----------:|-----------:|--------------------:|-----------------:|
| soft_x_lower | (18, 12650)    | (12650,)     |          0.765929 | -0.00816345 |  0           | 0.00919394 | 0.16861 |    -0.0692 |    0.18378 |                   4 |                0 |
| soft_x_upper | (18, 12650)    | (12650,)     |          0.765929 | -0.0780869  | -9.53674e-05 | 0.00597041 | 0.15625 |    -0.0692 |    0.18378 |                   4 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |        mean |        max |         std |
|:------------------------------------|------------------:|------------:|------------:|------------:|-----------:|------------:|
| soft_x_lower_median_across_channels |          0.765929 | -0.00440598 | 0.000228882 | 0.000289033 | 0.00667572 | 0.000748608 |
| soft_x_upper_median_across_channels |          0.765929 | -0.00408173 | 0           | 0.000267116 | 0.0162697  | 0.00209164  |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.