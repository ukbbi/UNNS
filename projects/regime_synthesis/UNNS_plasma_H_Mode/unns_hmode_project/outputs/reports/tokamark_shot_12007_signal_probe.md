# TokaMark One-Shot Array Probe — Shot 12007

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12007.zarr/`

## Load status

- loaded arrays: `16`
- failed arrays: `0`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (1781,)        | (1781,)      |          0.866929 |     -2.56202     |     -0.366127    |     -0.0597477   |      2.56202     |    -0.0692 |    0.3758  |                   1 |                0 |
| summary_ip                      | (1781,)        | (1781,)      |          1        | -28768.6         | 563248           | 431548           |      1.08639e+06 |    -0.0692 |    0.3758  |                   1 |                0 |
| interferometer_n_e_line         | (1781,)        | (1781,)      |          0.866929 |     -2.23265e+18 |      1.06681e+20 |      8.05001e+19 |      1.44162e+20 |    -0.0692 |    0.3758  |                   1 |                0 |
| dalpha_voltage                  | (3, 22260)     | (22260,)     |          0.866981 |     -0.012207    |      0.415039    |      0.508982    |      3.43506     |    -0.0692 |    0.37598 |                   4 |                0 |
| soft_x_lower                    | (18, 22260)    | (22260,)     |          0.866981 |     -0.00871658  |      0.000343323 |      0.0127089   |      0.269775    |    -0.0692 |    0.37598 |                   8 |                0 |
| soft_x_upper                    | (18, 22260)    | (22260,)     |          0.866981 |     -0.0780869   |      0.000572205 |      0.00927131  |      0.237427    |    -0.0692 |    0.37598 |                   8 |                0 |
| thomson_t_e                     | (120, 90)      | (90,)        |          0.428056 |      2.15665     |    434.439       |    414.443       |    922.093       |    -0.0692 |    0.3758  |                   1 |                0 |
| thomson_n_e                     | (120, 90)      | (90,)        |          0.428056 |      1.85835e+17 |      2.4919e+19  |      2.43777e+19 |      5.13051e+19 |    -0.0692 |    0.3758  |                   1 |                0 |
| equilibrium_q95                 | (90,)          | (90,)        |          0.6      |      4.99381     |      6.15416     |      6.28385     |      8.37412     |    -0.0692 |    0.3758  |                   1 |                0 |
| equilibrium_elongation          | (90,)          | (90,)        |          0.6      |      1.53101     |      1.8155      |      1.79237     |      1.98437     |    -0.0692 |    0.3758  |                   1 |                0 |
| equilibrium_triangularity_upper | (90,)          | (90,)        |          0.6      |      0.183792    |      0.316692    |      0.296768    |      0.367113    |    -0.0692 |    0.3758  |                   1 |                0 |
| equilibrium_triangularity_lower | (90,)          | (90,)        |          0.6      |      0.183792    |      0.359986    |      0.331771    |      0.435019    |    -0.0692 |    0.3758  |                   1 |                0 |
| equilibrium_minor_radius        | (90,)          | (90,)        |          0.6      |      0.427527    |      0.558993    |      0.534869    |      0.590377    |    -0.0692 |    0.3758  |                   1 |                0 |
| equilibrium_beta_normal         | (90,)          | (90,)        |          0.6      |      0.223779    |      0.745114    |      0.685057    |      1.06284     |    -0.0692 |    0.3758  |                   1 |                0 |
| equilibrium_beta_pol            | (90,)          | (90,)        |          0.6      |      0.0660678   |      0.135321    |      0.131828    |      0.23716     |    -0.0692 |    0.3758  |                   1 |                0 |
| equilibrium_whmd                | (90,)          | (90,)        |          0.6      |  27856.3         | 152243           | 126178           | 185226           |    -0.0692 |    0.3758  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |          min |        median |          mean |           max |           std |
|:------------------------------------|------------------:|-------------:|--------------:|--------------:|--------------:|--------------:|
| dalpha_median_across_channels       |          0.866981 | -0.00488281  |   0.444336    |   0.456184    |   2.75391     |   0.342338    |
| soft_x_lower_median_across_channels |          0.866981 | -0.00494003  |   0.0015831   |   0.00222195  |   0.0137901   |   0.00290086  |
| soft_x_upper_median_across_channels |          0.866981 | -0.0050354   |   0.00116348  |   0.00280404  |   0.0151062   |   0.00447907  |
| thomson_t_e_edge_median             |          0.355556 |  2.23766     |  46.2423      |  95.1629      | 636.625       | 147.603       |
| thomson_t_e_core_median             |          0.666667 | 47.2001      | 311.761       | 311.876       | 454.146       |  71.5456      |
| thomson_t_e_edge_core_ratio         |          0.355556 |  0.00811649  |   0.168296    |   0.30323     |   1.82315     |   0.430215    |
| thomson_t_e_profile_gradient_proxy  |          0.666667 |  3.36399     |   9.84084     |  10.03        |  28.1827      |   3.79341     |
| thomson_n_e_edge_median             |          0.355556 |  2.21612e+17 |   4.47141e+18 |   7.66508e+18 |   2.58548e+19 |   6.82498e+18 |
| thomson_n_e_core_median             |          0.666667 |  1.26216e+18 |   1.98566e+19 |   1.94291e+19 |   2.77609e+19 |   4.31897e+18 |
| thomson_n_e_edge_core_ratio         |          0.355556 |  0.0142418   |   0.25051     |   0.389299    |   1.58818     |   0.350122    |
| thomson_n_e_profile_gradient_proxy  |          0.666667 |  1.33123e+17 |   4.19457e+17 |   4.85332e+17 |   9.05995e+17 |   2.3597e+17  |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.