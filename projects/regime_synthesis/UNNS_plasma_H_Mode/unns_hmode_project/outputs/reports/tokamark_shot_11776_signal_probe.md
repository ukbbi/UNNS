# TokaMark One-Shot Array Probe — Shot 11776

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11776.zarr/`

## Load status

- loaded arrays: `12`
- failed arrays: `4`

### Failed arrays

- `summary_power_nbi`: `KeyError('Missing array metadata: summary/power_nbi/.zarray')`
- `dalpha_voltage`: `KeyError('Missing array metadata: spectrometer_visible/filter_spectrometer_dalpha_voltage/.zarray')`
- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_ip                      | (2088,)        | (2088,)      |          1        | -26636.1         | 527574           | 357313           | 583437           |    -0.0672 |    0.45455 |                   1 |                0 |
| interferometer_n_e_line         | (2088,)        | (2088,)      |          0.890326 |     -9.88704e+18 |      4.50606e+19 |      3.65339e+19 |      5.93145e+19 |    -0.0672 |    0.45455 |                   1 |                0 |
| soft_x_lower                    | (18, 26091)    | (26091,)     |          0.890345 |     -0.00740051  |      9.53674e-05 |      0.00289168  |      0.0370789   |    -0.0672 |    0.4546  |                   8 |                0 |
| soft_x_upper                    | (18, 26091)    | (26091,)     |          0.890345 |     -0.0780869   |      0.000152588 |      0.00178929  |      0.0706863   |    -0.0672 |    0.4546  |                   8 |                0 |
| equilibrium_q95                 | (105,)         | (105,)       |          0.657143 |      5.9721      |      8.88474     |      8.60787     |     12.3566      |    -0.0672 |    0.4528  |                   1 |                0 |
| equilibrium_elongation          | (105,)         | (105,)       |          0.657143 |      1.58017     |      1.73318     |      1.7704      |      2.01955     |    -0.0672 |    0.4528  |                   1 |                0 |
| equilibrium_triangularity_upper | (105,)         | (105,)       |          0.657143 |      0.21377     |      0.348746    |      0.339238    |      0.391289    |    -0.0672 |    0.4528  |                   1 |                0 |
| equilibrium_triangularity_lower | (105,)         | (105,)       |          0.657143 |      0.21377     |      0.407837    |      0.386147    |      0.448101    |    -0.0672 |    0.4528  |                   1 |                0 |
| equilibrium_minor_radius        | (105,)         | (105,)       |          0.657143 |      0.482383    |      0.594605    |      0.589981    |      0.61882     |    -0.0672 |    0.4528  |                   1 |                0 |
| equilibrium_beta_normal         | (105,)         | (105,)       |          0.657143 |      0.103499    |      0.608415    |      0.548081    |      1.33144     |    -0.0672 |    0.4528  |                   1 |                0 |
| equilibrium_beta_pol            | (105,)         | (105,)       |          0.657143 |      0.0316248   |      0.154437    |      0.148955    |      0.563285    |    -0.0672 |    0.4528  |                   1 |                0 |
| equilibrium_whmd                | (105,)         | (105,)       |          0.657143 |  19448           |  85762.1         |  79418.2         | 100861           |    -0.0672 |    0.4528  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |        mean |        max |        std |
|:------------------------------------|------------------:|------------:|------------:|------------:|-----------:|-----------:|
| soft_x_lower_median_across_channels |          0.890345 | -0.00538826 | 0.000648499 | 0.000484844 | 0.00761032 | 0.0011454  |
| soft_x_upper_median_across_channels |          0.890345 | -0.00370026 | 0.000267029 | 0.000427001 | 0.00837326 | 0.00125686 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.