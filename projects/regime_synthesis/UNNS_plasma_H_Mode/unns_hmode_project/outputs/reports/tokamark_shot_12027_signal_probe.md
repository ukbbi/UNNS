# TokaMark One-Shot Array Probe — Shot 12027

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12027.zarr/`

## Load status

- loaded arrays: `13`
- failed arrays: `3`

### Failed arrays

- `interferometer_n_e_line`: `KeyError('Missing array metadata: interferometer/n_e_line/.zarray')`
- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |            min |           median |            mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|---------------:|-----------------:|----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (1849,)        | (1849,)      |          0.897783 |  -7269.76      |      1.46878e+06 | 974032          |      1.73033e+06 |    -0.0572 |     0.4048 |                   1 |                0 |
| summary_ip                      | (1849,)        | (1849,)      |          1        | -28505.8       | 408053           | 324864          | 928386           |    -0.0572 |     0.4048 |                   1 |                0 |
| dalpha_voltage                  | (3, 23111)     | (23111,)     |          0.897841 |     -0.012207  |      0.234375    |      0.367961   |      2.55859     |    -0.0572 |     0.405  |                   4 |                0 |
| soft_x_lower                    | (18, 23111)    | (23111,)     |          0.897841 |     -0.010128  |      0.000305176 |      0.00933658 |      0.0869751   |    -0.0572 |     0.405  |                   8 |                0 |
| soft_x_upper                    | (18, 23111)    | (23111,)     |          0.897841 |     -0.0780869 |      0.000610352 |      0.00802668 |      0.0817871   |    -0.0572 |     0.405  |                   8 |                0 |
| equilibrium_q95                 | (93,)          | (93,)        |          0.634409 |      5.78875   |      8.88091     |     10.0065     |     16.7141      |    -0.0572 |     0.4028 |                   1 |                0 |
| equilibrium_elongation          | (93,)          | (93,)        |          0.634409 |      1.21183   |      1.73651     |      1.74698    |      2.41686     |    -0.0572 |     0.4028 |                   1 |                0 |
| equilibrium_triangularity_upper | (93,)          | (93,)        |          0.634409 |      0.0976894 |      0.347549    |      0.303011   |      0.404521    |    -0.0572 |     0.4028 |                   1 |                0 |
| equilibrium_triangularity_lower | (93,)          | (93,)        |          0.634409 |      0.175708  |      0.391294    |      0.349689   |      0.449785    |    -0.0572 |     0.4028 |                   1 |                0 |
| equilibrium_minor_radius        | (93,)          | (93,)        |          0.634409 |      0.392002  |      0.584408    |      0.562586   |      0.604373    |    -0.0572 |     0.4028 |                   1 |                0 |
| equilibrium_beta_normal         | (93,)          | (93,)        |          0.634409 |     -0.317541  |      1.26931     |      1.37831    |      3.18164     |    -0.0572 |     0.4028 |                   1 |                0 |
| equilibrium_beta_pol            | (93,)          | (93,)        |          0.634409 |     -0.225641  |      0.337164    |      0.323073   |      0.654957    |    -0.0572 |     0.4028 |                   1 |                0 |
| equilibrium_whmd                | (93,)          | (93,)        |          0.634409 |   3733.34      |  86226.3         |  75705.4        | 126485           |    -0.0572 |     0.4028 |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |       mean |       max |        std |
|:------------------------------------|------------------:|------------:|------------:|-----------:|----------:|-----------:|
| dalpha_median_across_channels       |          0.897841 | -0.00732422 | 0.349121    | 0.292053   | 1.93115   | 0.192343   |
| soft_x_lower_median_across_channels |          0.897841 | -0.00610352 | 0.00106812  | 0.00762887 | 0.0408936 | 0.0110635  |
| soft_x_upper_median_across_channels |          0.897841 | -0.00469208 | 0.000476837 | 0.00580996 | 0.0332832 | 0.00843224 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.