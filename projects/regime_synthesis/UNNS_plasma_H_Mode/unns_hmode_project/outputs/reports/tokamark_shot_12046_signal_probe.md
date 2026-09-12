# TokaMark One-Shot Array Probe — Shot 12046

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12046.zarr/`

## Load status

- loaded arrays: `16`
- failed arrays: `0`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |               min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|------------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (1817,)        | (1817,)      |          0.871767 |     -18.4604      |     -0.439318    |      0.0225987   |      9.22872     |     -0.068 |      0.386 |                   1 |                0 |
| summary_ip                      | (1817,)        | (1817,)      |          1        |  -28915.2         | 569374           | 434470           |      1.05245e+06 |     -0.068 |      0.386 |                   1 |                0 |
| interferometer_n_e_line         | (1817,)        | (1817,)      |          0.871767 |      -6.91607e+18 |      7.34853e+19 |      5.78768e+19 |      1.11591e+20 |     -0.068 |      0.386 |                   1 |                0 |
| dalpha_voltage                  | (3, 22701)     | (22701,)     |          0.872208 |      -0.012207    |      0.224609    |      0.367581    |      2.1875      |     -0.068 |      0.386 |                   4 |                0 |
| soft_x_lower                    | (18, 22701)    | (22701,)     |          0.872208 |      -0.00799179  |      0.000267029 |      0.0206483   |      0.3125      |     -0.068 |      0.386 |                   8 |                0 |
| soft_x_upper                    | (18, 22701)    | (22701,)     |          0.872208 |      -0.0780869   |      0.00120163  |      0.0164248   |      0.3125      |     -0.068 |      0.386 |                   8 |                0 |
| thomson_t_e                     | (120, 91)      | (91,)        |          0.325916 |       3.37535     |    498.892       |    496.035       |   1088.34        |     -0.068 |      0.382 |                   1 |                0 |
| thomson_n_e                     | (120, 91)      | (91,)        |          0.325916 |       7.78148e+17 |      1.65809e+19 |      1.67405e+19 |      3.53807e+19 |     -0.068 |      0.382 |                   1 |                0 |
| equilibrium_q95                 | (91,)          | (91,)        |          0.648352 |       5.00447     |      6.14598     |      6.49088     |     11.2486      |     -0.068 |      0.382 |                   1 |                0 |
| equilibrium_elongation          | (91,)          | (91,)        |          0.648352 |       1.48531     |      1.79939     |      1.77583     |      1.9894      |     -0.068 |      0.382 |                   1 |                0 |
| equilibrium_triangularity_upper | (91,)          | (91,)        |          0.648352 |       0.176632    |      0.310254    |      0.29323     |      0.371665    |     -0.068 |      0.382 |                   1 |                0 |
| equilibrium_triangularity_lower | (91,)          | (91,)        |          0.648352 |       0.176632    |      0.355494    |      0.32849     |      0.429191    |     -0.068 |      0.382 |                   1 |                0 |
| equilibrium_minor_radius        | (91,)          | (91,)        |          0.648352 |       0.424112    |      0.562331    |      0.532094    |      0.590083    |     -0.068 |      0.382 |                   1 |                0 |
| equilibrium_beta_normal         | (91,)          | (91,)        |          0.648352 |       0.15312     |      0.60654     |      0.528581    |      0.841882    |     -0.068 |      0.382 |                   1 |                0 |
| equilibrium_beta_pol            | (91,)          | (91,)        |          0.648352 |       0.0517251   |      0.10792     |      0.103131    |      0.185238    |     -0.068 |      0.382 |                   1 |                0 |
| equilibrium_whmd                | (91,)          | (91,)        |          0.648352 | -271677           | 150015           | 117100           | 330830           |     -0.068 |      0.382 |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |          min |        median |          mean |           max |          std |
|:------------------------------------|------------------:|-------------:|--------------:|--------------:|--------------:|-------------:|
| dalpha_median_across_channels       |          0.872208 | -0.00732422  |   0.231934    |   0.230367    |   1.66992     |  0.20878     |
| soft_x_lower_median_across_channels |          0.872208 | -0.00619888  |   0.00125885  |   0.00410768  |   0.0397301   |  0.00580633  |
| soft_x_upper_median_across_channels |          0.872208 | -0.00350952  |   0.000495911 |   0.00653956  |   0.0317383   |  0.00900236  |
| thomson_t_e_edge_median             |          0.230769 |  7.7989      | 137.34        | 114.173       | 241.436       | 68.6414      |
| thomson_t_e_core_median             |          0.505495 | 91.2732      | 378.568       | 372.763       | 556.95        | 96.1563      |
| thomson_t_e_edge_core_ratio         |          0.230769 |  0.0183528   |   0.322815    |   0.386489    |   2.3558      |  0.47592     |
| thomson_t_e_profile_gradient_proxy  |          0.505495 |  4.19521     |  11.672       |  11.4983      |  21.8835      |  4.26572     |
| thomson_n_e_edge_median             |          0.230769 |  2.23924e+18 |   7.87159e+18 |   7.89099e+18 |   1.52753e+19 |  3.02323e+18 |
| thomson_n_e_core_median             |          0.505495 |  2.50303e+18 |   1.35345e+19 |   1.33909e+19 |   2.20217e+19 |  3.28718e+18 |
| thomson_n_e_edge_core_ratio         |          0.230769 |  0.204587    |   0.573941    |   0.59233     |   0.917451    |  0.177646    |
| thomson_n_e_profile_gradient_proxy  |          0.505495 |  1.11057e+16 |   3.46547e+17 |   3.65959e+17 |   7.77189e+17 |  1.84997e+17 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.