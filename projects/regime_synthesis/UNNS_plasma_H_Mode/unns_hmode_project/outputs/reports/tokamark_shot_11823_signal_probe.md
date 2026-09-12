# TokaMark One-Shot Array Probe — Shot 11823

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11823.zarr/`

## Load status

- loaded arrays: `16`
- failed arrays: `0`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |               min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|------------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (1913,)        | (1913,)      |          0.880293 |      -2.57695     |      0.0585771   |     -0.0104722   |      2.10911     |     -0.067 |    0.411   |                   1 |                0 |
| summary_ip                      | (1913,)        | (1913,)      |          1        | -118607           | 512228           | 362827           | 556251           |     -0.067 |    0.411   |                   1 |                0 |
| interferometer_n_e_line         | (1913,)        | (1913,)      |          0.880293 |       1.53711e+18 |      1.40795e+20 |      1.22747e+20 |      2.81833e+20 |     -0.067 |    0.411   |                   1 |                0 |
| dalpha_voltage                  | (3, 23910)     | (23910,)     |          0.880761 |      -0.012207    |      0.50293     |      0.57324     |      4.99756     |     -0.067 |    0.41118 |                   4 |                0 |
| soft_x_lower                    | (18, 23910)    | (23910,)     |          0.880761 |      -0.00787735  |     -3.8147e-05  |      0.00529534  |      0.186768    |     -0.067 |    0.41118 |                   8 |                0 |
| soft_x_upper                    | (18, 23910)    | (23910,)     |          0.880761 |      -0.0780869   |      0.000419617 |      0.00706201  |      0.202179    |     -0.067 |    0.41118 |                   8 |                0 |
| thomson_t_e                     | (120, 96)      | (96,)        |          0.4625   |       0.854644    |    265.508       |    248.945       |    523.484       |     -0.067 |    0.408   |                   1 |                0 |
| thomson_n_e                     | (120, 96)      | (96,)        |          0.4625   |       2.50472e+17 |      2.61087e+18 |      2.61645e+18 |      5.27662e+18 |     -0.067 |    0.408   |                   1 |                0 |
| equilibrium_q95                 | (96,)          | (96,)        |          0.635417 |       4.31273     |      6.33577     |      7.09519     |     10.6815      |     -0.067 |    0.408   |                   1 |                0 |
| equilibrium_elongation          | (96,)          | (96,)        |          0.635417 |       1.4945      |      1.61237     |      1.63243     |      1.82483     |     -0.067 |    0.408   |                   1 |                0 |
| equilibrium_triangularity_upper | (96,)          | (96,)        |          0.635417 |       0.225384    |      0.277485    |      0.2807      |      0.406666    |     -0.067 |    0.408   |                   1 |                0 |
| equilibrium_triangularity_lower | (96,)          | (96,)        |          0.635417 |       0.234621    |      0.389183    |      0.363614    |      0.420284    |     -0.067 |    0.408   |                   1 |                0 |
| equilibrium_minor_radius        | (96,)          | (96,)        |          0.635417 |       0.538471    |      0.570193    |      0.567379    |      0.636357    |     -0.067 |    0.408   |                   1 |                0 |
| equilibrium_beta_normal         | (96,)          | (96,)        |          0.635417 |      -0.166013    |      0.452292    |      0.415643    |      0.844677    |     -0.067 |    0.408   |                   1 |                0 |
| equilibrium_beta_pol            | (96,)          | (96,)        |          0.635417 |      -0.0343437   |      0.099631    |      0.0970824   |      0.15922     |     -0.067 |    0.408   |                   1 |                0 |
| equilibrium_whmd                | (96,)          | (96,)        |          0.635417 |    4308.62        |  90637.4         |  86904.7         | 117764           |     -0.067 |    0.408   |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |           min |        median |          mean |           max |          std |
|:------------------------------------|------------------:|--------------:|--------------:|--------------:|--------------:|-------------:|
| dalpha_median_across_channels       |          0.880761 |  -0.00732422  |   0.483398    |   0.511782    |   4.99756     |  0.412118    |
| soft_x_lower_median_across_channels |          0.880761 |  -0.00390053  |   0.000143051 |   0.000248002 |   0.00823021  |  0.000894652 |
| soft_x_upper_median_across_channels |          0.880761 |  -0.00528336  |   0.0021553   |   0.00191966  |   0.0113297   |  0.00249829  |
| thomson_t_e_edge_median             |          0.458333 |   4.37477     |  11.3339      |  16.21        |  60.344       | 14.545       |
| thomson_t_e_core_median             |          0.666667 | 112.729       | 134.363       | 152.843       | 236.466       | 40.1935      |
| thomson_t_e_edge_core_ratio         |          0.458333 |   0.0330414   |   0.0705518   |   0.105045    |   0.374995    |  0.0924339   |
| thomson_t_e_profile_gradient_proxy  |          0.666667 |   2.02473     |   5.97939     |   5.50159     |  10.1502      |  2.25051     |
| thomson_n_e_edge_median             |          0.458333 |   4.00289e+17 |   4.97054e+17 |   7.85235e+17 |   1.55842e+18 |  4.0399e+17  |
| thomson_n_e_core_median             |          0.666667 |   1.10324e+18 |   2.39424e+18 |   2.39904e+18 |   3.58357e+18 |  8.61404e+17 |
| thomson_n_e_edge_core_ratio         |          0.458333 |   0.126049    |   0.374905    |   0.388826    |   0.747554    |  0.180313    |
| thomson_n_e_profile_gradient_proxy  |          0.666667 |   8.1333e+15  |   4.22859e+16 |   4.24112e+16 |   8.08936e+16 |  1.9819e+16  |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.