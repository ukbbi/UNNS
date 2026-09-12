# TokaMark One-Shot Array Probe — Shot 12017

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12017.zarr/`

## Load status

- loaded arrays: `16`
- failed arrays: `0`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (2181,)        | (2181,)      |          0.891334 |     -2.48884     |     -0.439356    |     -0.0756283   |      2.48884     |    -0.0692 |    0.4758  |                   1 |                0 |
| summary_ip                      | (2181,)        | (2181,)      |          1        | -32421.6         | 536102           | 440595           | 773199           |    -0.0692 |    0.4758  |                   1 |                0 |
| interferometer_n_e_line         | (2181,)        | (2181,)      |          0.891334 |     -1.88089e+18 |      1.26178e+20 |      1.24707e+20 |      3.05681e+20 |    -0.0692 |    0.4758  |                   1 |                0 |
| dalpha_voltage                  | (3, 27260)     | (27260,)     |          0.891379 |     -0.012207    |      0.483398    |      0.591041    |      2.35596     |    -0.0692 |    0.47598 |                   4 |                0 |
| soft_x_lower                    | (18, 27260)    | (27260,)     |          0.891379 |     -0.00867844  |      0.000419617 |      0.0111825   |      0.190125    |    -0.0692 |    0.47598 |                   8 |                0 |
| soft_x_upper                    | (18, 27260)    | (27260,)     |          0.891379 |     -0.0780869   |      0.00106812  |      0.00932396  |      0.162964    |    -0.0692 |    0.47598 |                   8 |                0 |
| thomson_t_e                     | (120, 110)     | (110,)       |          0.469318 |      1.32559     |    406.863       |    424.051       |    976.256       |    -0.0692 |    0.4758  |                   1 |                0 |
| thomson_n_e                     | (120, 110)     | (110,)       |          0.469318 |      2.21269e+17 |      3.28856e+19 |      3.22731e+19 |      6.40502e+19 |    -0.0692 |    0.4758  |                   1 |                0 |
| equilibrium_q95                 | (110,)         | (110,)       |          0.681818 |      2.71527     |      6.02587     |      6.43322     |     13.2105      |    -0.0692 |    0.4758  |                   1 |                0 |
| equilibrium_elongation          | (110,)         | (110,)       |          0.681818 |      1.29986     |      1.77965     |      1.70649     |      1.9627      |    -0.0692 |    0.4758  |                   1 |                0 |
| equilibrium_triangularity_upper | (110,)         | (110,)       |          0.681818 |      0.148831    |      0.328167    |      0.304727    |      0.404686    |    -0.0692 |    0.4758  |                   1 |                0 |
| equilibrium_triangularity_lower | (110,)         | (110,)       |          0.681818 |      0.178567    |      0.378269    |      0.343691    |      0.443944    |    -0.0692 |    0.4758  |                   1 |                0 |
| equilibrium_minor_radius        | (110,)         | (110,)       |          0.681818 |      0.317351    |      0.567325    |      0.532623    |      0.601207    |    -0.0692 |    0.4758  |                   1 |                0 |
| equilibrium_beta_normal         | (110,)         | (110,)       |          0.681818 |    -14.523       |      0.969345    |      0.303076    |      1.98633     |    -0.0692 |    0.4758  |                   1 |                0 |
| equilibrium_beta_pol            | (110,)         | (110,)       |          0.681818 |     -3.47003     |      0.176186    |      0.0842381   |      1.12331     |    -0.0692 |    0.4758  |                   1 |                0 |
| equilibrium_whmd                | (110,)         | (110,)       |          0.681818 |   5772.53        | 138727           | 119429           | 195806           |    -0.0692 |    0.4758  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |          min |        median |          mean |           max |          std |
|:------------------------------------|------------------:|-------------:|--------------:|--------------:|--------------:|-------------:|
| dalpha_median_across_channels       |          0.891379 | -0.00976562  |   0.458984    |   0.54857     |   1.75537     |  0.361333    |
| soft_x_lower_median_across_channels |          0.891379 | -0.00567436  |   0.00123978  |   0.00344282  |   0.0292206   |  0.00474013  |
| soft_x_upper_median_across_channels |          0.891379 | -0.00335693  |   0.00278473  |   0.00372981  |   0.0216293   |  0.0045456   |
| thomson_t_e_edge_median             |          0.481818 |  1.64914     |  59.5451      |  76.052       | 346.504       | 74.4572      |
| thomson_t_e_core_median             |          0.718182 | 50.6655      | 290.526       | 287.515       | 460.991       | 85.2461      |
| thomson_t_e_edge_core_ratio         |          0.481818 |  0.00636237  |   0.21374     |   0.26592     |   1.34933     |  0.261102    |
| thomson_t_e_profile_gradient_proxy  |          0.727273 |  2.64567     |   9.90149     |  11.2115      |  83.3278      |  9.29507     |
| thomson_n_e_edge_median             |          0.481818 |  7.44348e+17 |   7.09269e+18 |   9.73104e+18 |   2.50237e+19 |  7.15413e+18 |
| thomson_n_e_core_median             |          0.718182 |  8.00389e+18 |   2.76645e+19 |   2.84597e+19 |   5.09476e+19 |  1.1345e+19  |
| thomson_n_e_edge_core_ratio         |          0.481818 |  0.0326822   |   0.246275    |   0.323773    |   0.748178    |  0.226545    |
| thomson_n_e_profile_gradient_proxy  |          0.727273 |  8.40884e+16 |   4.43111e+17 |   4.65744e+17 |   1.27666e+18 |  2.01666e+17 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.