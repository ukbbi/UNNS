# TokaMark One-Shot Array Probe — Shot 12069

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12069.zarr/`

## Load status

- loaded arrays: `16`
- failed arrays: `0`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (1351,)        | (1351,)      |         0.945226  |     -2.17518     |     -0.563845    |     -0.0428251   |      2.65723     |    -0.0284 |     0.3091 |                   1 |                0 |
| summary_ip                      | (1351,)        | (1351,)      |         1         | -28916.3         | 182560           | 194229           | 477404           |    -0.0284 |     0.3091 |                   1 |                0 |
| interferometer_n_e_line         | (1351,)        | (1351,)      |         0.945226  |     -3.67789e+18 |      5.93514e+19 |      5.01107e+19 |      1.1732e+20  |    -0.0284 |     0.3091 |                   1 |                0 |
| dalpha_voltage                  | (3, 16881)     | (16881,)     |         0.945442  |     -0.012207    |      0.141602    |      0.330102    |      4.31152     |    -0.0284 |     0.3092 |                   2 |                0 |
| soft_x_lower                    | (18, 16881)    | (16881,)     |         0.945442  |     -0.00844955  |      5.72205e-05 |      0.00360659  |      0.100098    |    -0.0284 |     0.3092 |                   8 |                0 |
| soft_x_upper                    | (18, 16881)    | (16881,)     |         0.945442  |     -0.0780869   |      0           |      0.00188974  |      0.0865173   |    -0.0284 |     0.3092 |                   8 |                0 |
| thomson_t_e                     | (120, 68)      | (68,)        |         0.384436  |      4.68875     |    315.719       |    346.62        |  14276.5         |    -0.0284 |     0.3066 |                   1 |                0 |
| thomson_n_e                     | (120, 68)      | (68,)        |         0.384436  |      9.90531e+16 |      1.54752e+19 |      1.60421e+19 |      4.74722e+19 |    -0.0284 |     0.3066 |                   1 |                0 |
| equilibrium_q95                 | (68,)          | (68,)        |         0.0882353 |      6.3439      |     10.1782      |      9.44773     |     11.8211      |    -0.0284 |     0.3066 |                   1 |                0 |
| equilibrium_elongation          | (68,)          | (68,)        |         0.0882353 |      1.12521     |      1.25107     |      1.26488     |      1.41837     |    -0.0284 |     0.3066 |                   1 |                0 |
| equilibrium_triangularity_upper | (68,)          | (68,)        |         0.0882353 |      0.088146    |      0.174314    |      0.14587     |      0.175151    |    -0.0284 |     0.3066 |                   1 |                0 |
| equilibrium_triangularity_lower | (68,)          | (68,)        |         0.0882353 |      0.174314    |      0.17481     |      0.174758    |      0.175151    |    -0.0284 |     0.3066 |                   1 |                0 |
| equilibrium_minor_radius        | (68,)          | (68,)        |         0.0882353 |      0.349772    |      0.385669    |      0.386074    |      0.422781    |    -0.0284 |     0.3066 |                   1 |                0 |
| equilibrium_beta_normal         | (68,)          | (68,)        |         0.0882353 |     -0.0558154   |     -0.00218687  |     -0.0179478   |      0.00415895  |    -0.0284 |     0.3066 |                   1 |                0 |
| equilibrium_beta_pol            | (68,)          | (68,)        |         0.0882353 |     -4.4016      |     -0.106919    |     -1.4348      |      0.204123    |    -0.0284 |     0.3066 |                   1 |                0 |
| equilibrium_whmd                | (68,)          | (68,)        |         0.0882353 |    681.309       |   4664.88        |   3653.36        |   5613.89        |    -0.0284 |     0.3066 |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |          min |        median |          mean |           max |           std |
|:------------------------------------|------------------:|-------------:|--------------:|--------------:|--------------:|--------------:|
| dalpha_median_across_channels       |          0.945442 | -0.00732422  |   0.13916     |   0.244051    |   1.33789     |   0.271855    |
| soft_x_lower_median_across_channels |          0.945442 | -0.00408173  |   0.000228882 |   0.00026444  |   0.00785828  |   0.000705048 |
| soft_x_upper_median_across_channels |          0.945442 | -0.00259399  |   2.86102e-05 |   0.0008802   |   0.0184631   |   0.00252014  |
| thomson_t_e_edge_median             |          0.441176 | 13.5204      | 105.038       | 127.473       | 553.318       | 105.749       |
| thomson_t_e_core_median             |          0.661765 |  8.14295     | 164.115       | 158.224       | 353.085       |  70.8887      |
| thomson_t_e_edge_core_ratio         |          0.411765 |  0.0823836   |   0.553181    |   2.23392     |  32.5757      |   6.20387     |
| thomson_t_e_profile_gradient_proxy  |          0.691176 |  0.173663    |   9.6134      |  19.5983      | 311.247       |  48.0658      |
| thomson_n_e_edge_median             |          0.441176 |  2.73713e+17 |   6.51049e+18 |   6.89325e+18 |   1.64889e+19 |   4.40673e+18 |
| thomson_n_e_core_median             |          0.661765 |  1.12608e+17 |   8.79064e+18 |   1.25917e+19 |   4.55891e+19 |   1.02571e+19 |
| thomson_n_e_edge_core_ratio         |          0.411765 |  0.0350964   |   0.806898    |   1.02221     |   3.80624     |   0.910039    |
| thomson_n_e_profile_gradient_proxy  |          0.691176 |  6.77756e+15 |   4.53752e+17 |   4.68875e+17 |   1.52503e+18 |   2.81351e+17 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.