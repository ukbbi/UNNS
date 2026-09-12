# TokaMark One-Shot Array Probe — Shot 11996

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11996.zarr/`

## Load status

- loaded arrays: `16`
- failed arrays: `0`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |               min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|------------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (2172,)        | (2172,)      |          0.914825 | -203516           |  10461.1         | 806859           |      1.80557e+06 |    -0.0562 |    0.48655 |                   1 |                0 |
| summary_ip                      | (2172,)        | (2172,)      |          1        |  -35481           | 534031           | 360582           | 683425           |    -0.0562 |    0.48655 |                   1 |                0 |
| interferometer_n_e_line         | (2172,)        | (2172,)      |          0.905157 |      -2.43917e+17 |      7.19755e+19 |      7.07761e+19 |      1.33641e+20 |    -0.0562 |    0.48655 |                   1 |                0 |
| dalpha_voltage                  | (3, 27140)     | (27140,)     |          0.914849 |      -0.012207    |      0.205078    |      0.354682    |      2.90771     |    -0.0562 |    0.48658 |                   4 |                0 |
| soft_x_lower                    | (18, 27140)    | (27140,)     |          0.914849 |      -0.00968933  |      0.00112534  |      0.0211602   |      0.151215    |    -0.0562 |    0.48658 |                   8 |                0 |
| soft_x_upper                    | (18, 27140)    | (27140,)     |          0.914849 |      -0.0780869   |      0.00335693  |      0.0190077   |      0.139008    |    -0.0562 |    0.48658 |                   8 |                0 |
| thomson_t_e                     | (120, 109)     | (109,)       |          0.272783 |       1.35684     |    470.869       |    490.179       |   1323.55        |    -0.0562 |    0.4838  |                   1 |                0 |
| thomson_n_e                     | (120, 109)     | (109,)       |          0.272783 |       5.8107e+13  |      7.87429e+18 |      9.34584e+18 |      3.2483e+19  |    -0.0562 |    0.4838  |                   1 |                0 |
| equilibrium_q95                 | (109,)         | (109,)       |          0.688073 |       4.94325     |      6.91913     |      8.87944     |     16.7966      |    -0.0562 |    0.4838  |                   1 |                0 |
| equilibrium_elongation          | (109,)         | (109,)       |          0.688073 |       1.23821     |      1.7282      |      1.71657     |      2.05927     |    -0.0562 |    0.4838  |                   1 |                0 |
| equilibrium_triangularity_upper | (109,)         | (109,)       |          0.688073 |       0.0794107   |      0.339816    |      0.320005    |      0.433271    |    -0.0562 |    0.4838  |                   1 |                0 |
| equilibrium_triangularity_lower | (109,)         | (109,)       |          0.688073 |       0.188116    |      0.402568    |      0.368962    |      0.452161    |    -0.0562 |    0.4838  |                   1 |                0 |
| equilibrium_minor_radius        | (109,)         | (109,)       |          0.688073 |       0.411948    |      0.588445    |      0.571353    |      0.607375    |    -0.0562 |    0.4838  |                   1 |                0 |
| equilibrium_beta_normal         | (109,)         | (109,)       |          0.688073 |      -0.150866    |      1.28188     |      1.43127     |      2.96532     |    -0.0562 |    0.4838  |                   1 |                0 |
| equilibrium_beta_pol            | (109,)         | (109,)       |          0.688073 |      -0.0965307   |      0.319645    |      0.337231    |      0.620501    |    -0.0562 |    0.4838  |                   1 |                0 |
| equilibrium_whmd                | (109,)         | (109,)       |          0.688073 |    4443.6         | 107686           |  86522.2         | 124567           |    -0.0562 |    0.4838  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |           min |        median |          mean |           max |           std |
|:------------------------------------|------------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| dalpha_median_across_channels       |          0.914849 |  -0.00732422  |   0.275879    |   0.249336    |   1.66992     |   0.144665    |
| soft_x_lower_median_across_channels |          0.914849 |  -0.00894547  |   0.00818253  |   0.0134092   |   0.0592232   |   0.0158665   |
| soft_x_upper_median_across_channels |          0.914849 |  -0.00490189  |   0.00543594  |   0.012415    |   0.0508499   |   0.0150945   |
| thomson_t_e_edge_median             |          0.33945  |   1.38306     | 123.997       | 165.452       | 471.422       | 138.674       |
| thomson_t_e_core_median             |          0.394495 | 128.357       | 233.739       | 225.189       | 401.881       |  55.0938      |
| thomson_t_e_edge_core_ratio         |          0.33945  |   0.00878297  |   0.482831    |   0.701908    |   1.94944     |   0.571631    |
| thomson_t_e_profile_gradient_proxy  |          0.394495 |   6.89148     |  14.8757      |  15.6685      |  27.8519      |   4.32156     |
| thomson_n_e_edge_median             |          0.33945  |   4.35608e+15 |   1.04681e+18 |   6.38285e+18 |   2.44048e+19 |   8.14954e+18 |
| thomson_n_e_core_median             |          0.394495 |   2.4788e+17  |   8.23615e+18 |   6.42799e+18 |   1.74546e+19 |   6.15512e+18 |
| thomson_n_e_edge_core_ratio         |          0.33945  |   0.0081036   |   0.853669    |   0.803609    |   1.62923     |   0.45019     |
| thomson_n_e_profile_gradient_proxy  |          0.394495 |   1.14275e+16 |   2.89752e+17 |   2.74872e+17 |   7.7424e+17  |   2.56954e+17 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.