# TokaMark One-Shot Array Probe — Shot 11946

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11946.zarr/`

## Load status

- loaded arrays: `16`
- failed arrays: `0`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (2181,)        | (2181,)      |          0.910133 | -13670.2         | 957185           | 790795           |      1.68383e+06 |    -0.0588 |     0.4862 |                   1 |                0 |
| summary_ip                      | (2181,)        | (2181,)      |          1        | -21902.4         | 488602           | 354414           | 703250           |    -0.0588 |     0.4862 |                   1 |                0 |
| interferometer_n_e_line         | (2181,)        | (2181,)      |          0.901421 |     -2.94715e+18 |      7.48403e+19 |      7.40426e+19 |      1.76918e+20 |    -0.0588 |     0.4862 |                   1 |                0 |
| dalpha_voltage                  | (3, 27251)     | (27251,)     |          0.910425 |     -0.012207    |      0.26123     |      0.401614    |      4.99756     |    -0.0588 |     0.4862 |                   4 |                0 |
| soft_x_lower                    | (18, 27251)    | (27251,)     |          0.910425 |     -0.0107002   |      0.000343323 |      0.00956684  |      0.0944519   |    -0.0588 |     0.4862 |                   8 |                0 |
| soft_x_upper                    | (18, 27251)    | (27251,)     |          0.910425 |     -0.0780869   |      0.000762939 |      0.00829292  |      0.0823975   |    -0.0588 |     0.4862 |                   8 |                0 |
| thomson_t_e                     | (120, 110)     | (110,)       |          0.522727 |      0.753082    |    423.617       |    547.722       | 167809           |    -0.0588 |     0.4862 |                   1 |                0 |
| thomson_n_e                     | (120, 110)     | (110,)       |          0.522727 |      8.05867e+17 |      3.04067e+19 |      3.17817e+19 |      7.2172e+19  |    -0.0588 |     0.4862 |                   1 |                0 |
| equilibrium_q95                 | (110,)         | (110,)       |          0.690909 |      5.32767     |      7.05867     |      9.45657     |     16.8695      |    -0.0588 |     0.4862 |                   1 |                0 |
| equilibrium_elongation          | (110,)         | (110,)       |          0.690909 |      1.21158     |      1.73254     |      1.75215     |      2.25522     |    -0.0588 |     0.4862 |                   1 |                0 |
| equilibrium_triangularity_upper | (110,)         | (110,)       |          0.690909 |      0.107939    |      0.346649    |      0.327338    |      0.427166    |    -0.0588 |     0.4862 |                   1 |                0 |
| equilibrium_triangularity_lower | (110,)         | (110,)       |          0.690909 |      0.179214    |      0.404269    |      0.374306    |      0.455099    |    -0.0588 |     0.4862 |                   1 |                0 |
| equilibrium_minor_radius        | (110,)         | (110,)       |          0.690909 |      0.397452    |      0.5843      |      0.569326    |      0.605773    |    -0.0588 |     0.4862 |                   1 |                0 |
| equilibrium_beta_normal         | (110,)         | (110,)       |          0.690909 |     -0.265114    |      1.22235     |      1.41155     |      3.09723     |    -0.0588 |     0.4862 |                   1 |                0 |
| equilibrium_beta_pol            | (110,)         | (110,)       |          0.690909 |     -0.190101    |      0.309648    |      0.329779    |      0.645226    |    -0.0588 |     0.4862 |                   1 |                0 |
| equilibrium_whmd                | (110,)         | (110,)       |          0.690909 |   3736.11        |  95906.9         |  82385.2         | 125644           |    -0.0588 |     0.4862 |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |           min |        median |           mean |             max |             std |
|:------------------------------------|------------------:|--------------:|--------------:|---------------:|----------------:|----------------:|
| dalpha_median_across_channels       |          0.910425 |  -0.00732422  |   0.368652    |    0.315295    |     1.81396     |     0.179386    |
| soft_x_lower_median_across_channels |          0.910425 |  -0.00621796  |   0.00137329  |    0.00750867  |     0.0491333   |     0.0109547   |
| soft_x_upper_median_across_channels |          0.910425 |  -0.00473022  |   0.00110626  |    0.00542374  |     0.0298309   |     0.00789891  |
| thomson_t_e_edge_median             |          0.681818 |  13.864       | 153.148       | 1520.09        | 98876.6         | 11318.6         |
| thomson_t_e_core_median             |          0.7      | 122.737       | 235.79        |  235.116       |   350.728       |    56.0592      |
| thomson_t_e_edge_core_ratio         |          0.681818 |   0.0603516   |   0.620574    |   10.3404      |   713.266       |    81.7162      |
| thomson_t_e_profile_gradient_proxy  |          0.7      |   6.29179     |  13.3656      |   14.0335      |    27.8672      |     6.14357     |
| thomson_n_e_edge_median             |          0.681818 |   1.22716e+18 |   2.11045e+19 |    2.15287e+19 |     4.18358e+19 |     1.37667e+19 |
| thomson_n_e_core_median             |          0.7      |   8.37618e+18 |   2.0856e+19  |    2.04819e+19 |     3.54984e+19 |     8.58637e+18 |
| thomson_n_e_edge_core_ratio         |          0.681818 |   0.0492607   |   1.05376     |    0.9781      |     1.44156     |     0.396445    |
| thomson_n_e_profile_gradient_proxy  |          0.7      |   2.15825e+17 |   6.30488e+17 |    6.4652e+17  |     1.48483e+18 |     1.96168e+17 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.