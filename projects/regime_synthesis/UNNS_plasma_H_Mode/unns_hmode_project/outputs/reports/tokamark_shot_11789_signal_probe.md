# TokaMark One-Shot Array Probe — Shot 11789

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11789.zarr/`

## Load status

- loaded arrays: `13`
- failed arrays: `3`

### Failed arrays

- `interferometer_n_e_line`: `KeyError('Missing array metadata: interferometer/n_e_line/.zarray')`
- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |             min |           median |            mean |           max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|----------------:|-----------------:|----------------:|--------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (2020,)        | (2020,)      |          0.886634 |    -61.5268     |      0           |     -0.879171   |     55.6671   |    -0.0672 |    0.43755 |                   1 |                0 |
| summary_ip                      | (2020,)        | (2020,)      |          1        | -44484.1        | 526924           | 360434          | 577952        |    -0.0672 |    0.43755 |                   1 |                0 |
| dalpha_voltage                  | (3, 25250)     | (25250,)     |          0.886693 |     -0.012207   |      0.266113    |      0.427971   |      2.80518  |    -0.0672 |    0.43778 |                   4 |                0 |
| soft_x_lower                    | (18, 25250)    | (25250,)     |          0.886693 |     -0.00682831 |      0.000133514 |      0.00489865 |      0.13092  |    -0.0672 |    0.43778 |                   8 |                0 |
| soft_x_upper                    | (18, 25250)    | (25250,)     |          0.886693 |     -0.0780869  |      0.000228882 |      0.0033259  |      0.110626 |    -0.0672 |    0.43778 |                   8 |                0 |
| equilibrium_q95                 | (101,)         | (101,)       |          0.643564 |      6.32548    |      8.95988     |      8.72233    |     12.7395   |    -0.0672 |    0.4328  |                   1 |                0 |
| equilibrium_elongation          | (101,)         | (101,)       |          0.643564 |      1.56315    |      1.73042     |      1.7665     |      2.02029  |    -0.0672 |    0.4328  |                   1 |                0 |
| equilibrium_triangularity_upper | (101,)         | (101,)       |          0.643564 |      0.220788   |      0.353331    |      0.343809   |      0.398247 |    -0.0672 |    0.4328  |                   1 |                0 |
| equilibrium_triangularity_lower | (101,)         | (101,)       |          0.643564 |      0.213822   |      0.424794    |      0.392355   |      0.453613 |    -0.0672 |    0.4328  |                   1 |                0 |
| equilibrium_minor_radius        | (101,)         | (101,)       |          0.643564 |      0.487159   |      0.597072    |      0.5932     |      0.622475 |    -0.0672 |    0.4328  |                   1 |                0 |
| equilibrium_beta_normal         | (101,)         | (101,)       |          0.643564 |      0.128474   |      0.866709    |      0.772332   |      1.24471  |    -0.0672 |    0.4328  |                   1 |                0 |
| equilibrium_beta_pol            | (101,)         | (101,)       |          0.643564 |      0.0383363  |      0.225612    |      0.197145   |      0.342465 |    -0.0672 |    0.4328  |                   1 |                0 |
| equilibrium_whmd                | (101,)         | (101,)       |          0.643564 |  26369.4        |  84368.1         |  82938.2        | 103312        |    -0.0672 |    0.4328  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |        mean |        max |        std |
|:------------------------------------|------------------:|------------:|------------:|------------:|-----------:|-----------:|
| dalpha_median_across_channels       |          0.886693 | -0.00488281 | 0.26123     | 0.290459    | 2.23633    | 0.243477   |
| soft_x_lower_median_across_channels |          0.886693 | -0.00530243 | 0.000610352 | 0.000423021 | 0.00991821 | 0.00101306 |
| soft_x_upper_median_across_channels |          0.886693 | -0.00547409 | 0.000448227 | 0.000681956 | 0.00766754 | 0.00160878 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.