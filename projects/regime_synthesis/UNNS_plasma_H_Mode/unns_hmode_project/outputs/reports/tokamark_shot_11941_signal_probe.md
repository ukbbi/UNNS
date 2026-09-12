# TokaMark One-Shot Array Probe — Shot 11941

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11941.zarr/`

## Load status

- loaded arrays: `16`
- failed arrays: `0`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |               min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|------------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (2089,)        | (2089,)      |          0.905697 | -139647           |      1.71314     | 206710           |      1.51423e+06 |     -0.059 |     0.463  |                   1 |                0 |
| summary_ip                      | (2089,)        | (2089,)      |          1        |  -47672.4         | 365823           | 315230           | 574875           |     -0.059 |     0.463  |                   1 |                0 |
| interferometer_n_e_line         | (2089,)        | (2089,)      |          0.905697 |      -1.24747e+19 |      6.8287e+19  |      6.62431e+19 |      1.32851e+20 |     -0.059 |     0.463  |                   1 |                0 |
| dalpha_voltage                  | (3, 26111)     | (26111,)     |          0.906132 |      -0.012207    |      0.292969    |      0.385732    |      4.99756     |     -0.059 |     0.4632 |                   4 |                0 |
| soft_x_lower                    | (18, 26111)    | (26111,)     |          0.906132 |      -0.030098    |      0.000114441 |      0.00419968  |      0.062561    |     -0.059 |     0.4632 |                   8 |                0 |
| soft_x_upper                    | (18, 26111)    | (26111,)     |          0.906132 |      -0.0780869   |      0.000228882 |      0.00323598  |      0.0587082   |     -0.059 |     0.4632 |                   8 |                0 |
| thomson_t_e                     | (120, 105)     | (105,)       |          0.530238 |       4.57578     |    358.505       |    580.327       |  77755.7         |     -0.059 |     0.461  |                   1 |                0 |
| thomson_n_e                     | (120, 105)     | (105,)       |          0.530238 |       1.46141e+17 |      3.09121e+19 |      3.16747e+19 |      6.68234e+19 |     -0.059 |     0.461  |                   1 |                0 |
| equilibrium_q95                 | (105,)         | (105,)       |          0.647619 |       5.77122     |      7.89273     |      9.53246     |     15.3076      |     -0.059 |     0.461  |                   1 |                0 |
| equilibrium_elongation          | (105,)         | (105,)       |          0.647619 |       1.22896     |      1.72347     |      1.6991      |      1.98218     |     -0.059 |     0.461  |                   1 |                0 |
| equilibrium_triangularity_upper | (105,)         | (105,)       |          0.647619 |       0.0866835   |      0.340216    |      0.314047    |      0.402461    |     -0.059 |     0.461  |                   1 |                0 |
| equilibrium_triangularity_lower | (105,)         | (105,)       |          0.647619 |       0.159709    |      0.415535    |      0.362404    |      0.446427    |     -0.059 |     0.461  |                   1 |                0 |
| equilibrium_minor_radius        | (105,)         | (105,)       |          0.647619 |       0.399496    |      0.590293    |      0.566837    |      0.610544    |     -0.059 |     0.461  |                   1 |                0 |
| equilibrium_beta_normal         | (105,)         | (105,)       |          0.647619 |      -0.286845    |      1.01074     |      0.857625    |      2.04501     |     -0.059 |     0.461  |                   1 |                0 |
| equilibrium_beta_pol            | (105,)         | (105,)       |          0.647619 |      -0.19079     |      0.246296    |      0.224495    |      0.665208    |     -0.059 |     0.461  |                   1 |                0 |
| equilibrium_whmd                | (105,)         | (105,)       |          0.647619 |    4415.66        |  81613.7         |  68957.3         | 117190           |     -0.059 |     0.461  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |          min |        median |          mean |           max |          std |
|:------------------------------------|------------------:|-------------:|--------------:|--------------:|--------------:|-------------:|
| dalpha_median_across_channels       |          0.906132 | -0.00732422  |   0.385742    |   0.322792    |   0.874023    |  0.15939     |
| soft_x_lower_median_across_channels |          0.906132 | -0.00619888  |   0.000638962 |   0.00125977  |   0.00963211  |  0.00198485  |
| soft_x_upper_median_across_channels |          0.906132 | -0.00400543  |   0.00125885  |   0.00138075  |   0.00900269  |  0.0023527   |
| thomson_t_e_edge_median             |          0.685714 |  6.64956     | 130.892       | 125.228       | 449.456       | 86.663       |
| thomson_t_e_core_median             |          0.72381  | 23.5399      | 192.551       | 191.281       | 333.728       | 74.5187      |
| thomson_t_e_edge_core_ratio         |          0.685714 |  0.0199251   |   0.676598    |   1.10898     |   7.94743     |  1.64059     |
| thomson_t_e_profile_gradient_proxy  |          0.72381  |  6.02336     |  11.8187      |  13.7871      |  55.8356      |  9.19832     |
| thomson_n_e_edge_median             |          0.685714 |  1.03283e+18 |   2.56401e+19 |   2.36784e+19 |   4.61377e+19 |  1.20084e+19 |
| thomson_n_e_core_median             |          0.72381  |  9.37719e+18 |   1.98806e+19 |   1.96837e+19 |   3.10756e+19 |  7.2806e+18  |
| thomson_n_e_edge_core_ratio         |          0.685714 |  0.0460278   |   1.14361     |   1.22152     |   3.0041      |  0.63914     |
| thomson_n_e_profile_gradient_proxy  |          0.72381  |  3.61132e+17 |   6.4662e+17  |   6.72916e+17 |   1.3533e+18  |  1.82592e+17 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.