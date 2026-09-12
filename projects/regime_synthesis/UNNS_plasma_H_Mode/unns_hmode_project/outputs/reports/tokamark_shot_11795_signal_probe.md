# TokaMark One-Shot Array Probe — Shot 11795

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11795.zarr/`

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
| summary_power_nbi               | (1980,)        | (1980,)      |          0.884848 |    -27.1766     |      0.0512527   |     -0.64853    |     29.9087   |    -0.0668 |    0.42795 |                   1 |                0 |
| summary_ip                      | (1980,)        | (1980,)      |          1        | -47670.9        | 520622           | 356740          | 577358        |    -0.0668 |    0.42795 |                   1 |                0 |
| dalpha_voltage                  | (3, 24741)     | (24741,)     |          0.88517  |     -0.012207   |      0.349121    |      0.480871   |      3.25928  |    -0.0668 |    0.428   |                   4 |                0 |
| soft_x_lower                    | (18, 24741)    | (24741,)     |          0.88517  |     -0.00896454 |      0.000114441 |      0.00442197 |      0.128784 |    -0.0668 |    0.428   |                   8 |                0 |
| soft_x_upper                    | (18, 24741)    | (24741,)     |          0.88517  |     -0.0780869  |      0.000190735 |      0.00294737 |      0.111694 |    -0.0668 |    0.428   |                   8 |                0 |
| equilibrium_q95                 | (99,)          | (99,)        |          0.646465 |      6.1113     |      8.87386     |      8.68124    |     12.9587   |    -0.0668 |    0.4232  |                   1 |                0 |
| equilibrium_elongation          | (99,)          | (99,)        |          0.646465 |      1.54734    |      1.71966     |      1.75446    |      2.0065   |    -0.0668 |    0.4232  |                   1 |                0 |
| equilibrium_triangularity_upper | (99,)          | (99,)        |          0.646465 |      0.217874   |      0.360612    |      0.348875   |      0.40814  |    -0.0668 |    0.4232  |                   1 |                0 |
| equilibrium_triangularity_lower | (99,)          | (99,)        |          0.646465 |      0.217874   |      0.421459    |      0.392242   |      0.449641 |    -0.0668 |    0.4232  |                   1 |                0 |
| equilibrium_minor_radius        | (99,)          | (99,)        |          0.646465 |      0.48474    |      0.596421    |      0.593602   |      0.625259 |    -0.0668 |    0.4232  |                   1 |                0 |
| equilibrium_beta_normal         | (99,)          | (99,)        |          0.646465 |      0.140376   |      0.810543    |      0.746633   |      1.24163  |    -0.0668 |    0.4232  |                   1 |                0 |
| equilibrium_beta_pol            | (99,)          | (99,)        |          0.646465 |      0.0416388  |      0.213397    |      0.189866   |      0.327323 |    -0.0668 |    0.4232  |                   1 |                0 |
| equilibrium_whmd                | (99,)          | (99,)        |          0.646465 |  23032.7        |  84007.9         |  83747.9        | 109860        |    -0.0668 |    0.4232  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |        mean |        max |         std |
|:------------------------------------|------------------:|------------:|------------:|------------:|-----------:|------------:|
| dalpha_median_across_channels       |           0.88517 | -0.00488281 | 0.34668     | 0.366349    | 2.27783    | 0.286402    |
| soft_x_lower_median_across_channels |           0.88517 | -0.00435829 | 0.000505447 | 0.000345684 | 0.00623703 | 0.000884855 |
| soft_x_upper_median_across_channels |           0.88517 | -0.00375748 | 0.000305176 | 0.000436749 | 0.0069809  | 0.00132265  |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.