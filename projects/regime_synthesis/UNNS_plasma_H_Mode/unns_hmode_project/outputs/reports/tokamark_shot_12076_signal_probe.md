# TokaMark One-Shot Array Probe — Shot 12076

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12076.zarr/`

## Load status

- loaded arrays: `16`
- failed arrays: `0`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |             max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (1490,)        | (1490,)      |          0.84094  |     -2.63678     |     -0.292879    |     -0.0376392   |     1.75698     |     -0.069 |    0.30325 |                   1 |                0 |
| summary_ip                      | (1490,)        | (1490,)      |          1        | -76591.1         | 439130           | 372319           |     1.07253e+06 |     -0.069 |    0.30325 |                   1 |                0 |
| interferometer_n_e_line         | (1490,)        | (1490,)      |          0.84094  |     -1.10786e+19 |      8.87772e+19 |      7.46763e+19 |     1.48321e+20 |     -0.069 |    0.30325 |                   1 |                0 |
| dalpha_voltage                  | (3, 18620)     | (18620,)     |          0.841515 |     -0.012207    |      0.266113    |      0.378614    |     3.96973     |     -0.069 |    0.30338 |                   2 |                0 |
| soft_x_lower                    | (18, 18620)    | (18620,)     |          0.841515 |     -0.00829697  |      0.000114441 |      0.0223321   |     0.3125      |     -0.069 |    0.30338 |                   8 |                0 |
| soft_x_upper                    | (18, 18620)    | (18620,)     |          0.841515 |     -0.0780869   |      0.000572205 |      0.018917    |     0.3125      |     -0.069 |    0.30338 |                   8 |                0 |
| thomson_t_e                     | (120, 75)      | (75,)        |          0.370444 |      2.15969     |    439.658       |    412.11        |   807.208       |     -0.069 |    0.301   |                   1 |                0 |
| thomson_n_e                     | (120, 75)      | (75,)        |          0.370444 |      2.34324e+17 |      2.37709e+19 |      2.44524e+19 |     5.77072e+19 |     -0.069 |    0.301   |                   1 |                0 |
| equilibrium_q95                 | (75,)          | (75,)        |          0.16     |      7.42199     |      8.21538     |      8.90973     |    12.1806      |     -0.069 |    0.301   |                   1 |                0 |
| equilibrium_elongation          | (75,)          | (75,)        |          0.16     |      1.55321     |      1.59557     |      1.59556     |     1.65078     |     -0.069 |    0.301   |                   1 |                0 |
| equilibrium_triangularity_upper | (75,)          | (75,)        |          0.16     |      0.180256    |      0.206913    |      0.205765    |     0.232473    |     -0.069 |    0.301   |                   1 |                0 |
| equilibrium_triangularity_lower | (75,)          | (75,)        |          0.16     |      0.180256    |      0.206913    |      0.205765    |     0.232473    |     -0.069 |    0.301   |                   1 |                0 |
| equilibrium_minor_radius        | (75,)          | (75,)        |          0.16     |      0.430911    |      0.444762    |      0.458476    |     0.537239    |     -0.069 |    0.301   |                   1 |                0 |
| equilibrium_beta_normal         | (75,)          | (75,)        |          0.16     |      0.00164868  |      0.00239257  |      0.00260537  |     0.0036584   |     -0.069 |    0.301   |                   1 |                0 |
| equilibrium_beta_pol            | (75,)          | (75,)        |          0.16     |      0.0536696   |      0.0732217   |      0.0736233   |     0.0918523   |     -0.069 |    0.301   |                   1 |                0 |
| equilibrium_whmd                | (75,)          | (75,)        |          0.16     |  23545.8         |  30242.9         |  31559           | 41304.2         |     -0.069 |    0.301   |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |          min |        median |          mean |           max |           std |
|:------------------------------------|------------------:|-------------:|--------------:|--------------:|--------------:|--------------:|
| dalpha_median_across_channels       |          0.841515 | -0.00732422  |   0.234375    |   0.251771    |   2.54639     |   0.194594    |
| soft_x_lower_median_across_channels |          0.841515 | -0.00556946  |   0.000648499 |   0.00216255  |   0.0219154   |   0.00381554  |
| soft_x_upper_median_across_channels |          0.841515 | -0.0037384   |   0.000286102 |   0.00800759  |   0.0533104   |   0.0119964   |
| thomson_t_e_edge_median             |          0.346667 |  2.21524     |  69.1174      | 105.008       | 689.736       | 150.913       |
| thomson_t_e_core_median             |          0.586667 | 96.0621      | 321.104       | 311.027       | 459.215       |  71.257       |
| thomson_t_e_edge_core_ratio         |          0.333333 |  0.00593789  |   0.216507    |   0.291104    |   1.69223     |   0.391196    |
| thomson_t_e_profile_gradient_proxy  |          0.586667 |  2.32663     |  10.0214      |   9.80082     |  18.2804      |   3.23275     |
| thomson_n_e_edge_median             |          0.346667 |  3.04953e+17 |   3.11695e+18 |   4.8705e+18  |   1.30835e+19 |   4.22525e+18 |
| thomson_n_e_core_median             |          0.586667 |  9.62361e+18 |   1.9203e+19  |   1.83055e+19 |   2.55062e+19 |   3.67931e+18 |
| thomson_n_e_edge_core_ratio         |          0.333333 |  0.0155579   |   0.188357    |   0.259902    |   0.758825    |   0.225371    |
| thomson_n_e_profile_gradient_proxy  |          0.586667 |  1.12831e+17 |   5.80163e+17 |   5.62605e+17 |   1.03561e+18 |   2.42521e+17 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.