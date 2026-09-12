# TokaMark One-Shot Array Probe — Shot 12063

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12063.zarr/`

## Load status

- loaded arrays: `16`
- failed arrays: `0`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |             max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (1712,)        | (1712,)      |          0.863902 |     -1.58195     |     -0.410069    |     -0.0143583   |     2.37293     |     -0.068 |    0.35975 |                   1 |                0 |
| summary_ip                      | (1712,)        | (1712,)      |          1        | -30424.3         | 533124           | 422036           |     1.09056e+06 |     -0.068 |    0.35975 |                   1 |                0 |
| interferometer_n_e_line         | (1712,)        | (1712,)      |          0.863902 |     -9.43505e+18 |      5.17497e+19 |      4.2655e+19  |     8.35795e+19 |     -0.068 |    0.35975 |                   1 |                0 |
| dalpha_voltage                  | (3, 21400)     | (21400,)     |          0.864439 |     -0.012207    |      0.136719    |      0.297777    |     1.85791     |     -0.068 |    0.35998 |                   4 |                0 |
| soft_x_lower                    | (18, 21400)    | (21400,)     |          0.864439 |     -0.00867844  |      0.000152588 |      0.0122899   |     0.181885    |     -0.068 |    0.35998 |                   8 |                0 |
| soft_x_upper                    | (18, 21400)    | (21400,)     |          0.864439 |     -0.0780869   |      0.000610352 |      0.0088695   |     0.154572    |     -0.068 |    0.35998 |                   8 |                0 |
| thomson_t_e                     | (120, 86)      | (86,)        |          0.421512 |      1.69646     |    566.322       |    589.542       |  1944.15        |     -0.068 |    0.357   |                   1 |                0 |
| thomson_n_e                     | (120, 86)      | (86,)        |          0.421512 |      1.43788e+17 |      1.17177e+19 |      1.34884e+19 |     3.30007e+19 |     -0.068 |    0.357   |                   1 |                0 |
| equilibrium_q95                 | (86,)          | (86,)        |          0.27907  |      6.60229     |      7.33359     |      7.64875     |    10.5101      |     -0.068 |    0.357   |                   1 |                0 |
| equilibrium_elongation          | (86,)          | (86,)        |          0.27907  |      1.53669     |      1.67092     |      1.72933     |     1.97605     |     -0.068 |    0.357   |                   1 |                0 |
| equilibrium_triangularity_upper | (86,)          | (86,)        |          0.27907  |      0.197949    |      0.242472    |      0.255715    |     0.366803    |     -0.068 |    0.357   |                   1 |                0 |
| equilibrium_triangularity_lower | (86,)          | (86,)        |          0.27907  |      0.197949    |      0.242472    |      0.252487    |     0.331861    |     -0.068 |    0.357   |                   1 |                0 |
| equilibrium_minor_radius        | (86,)          | (86,)        |          0.27907  |      0.434919    |      0.465046    |      0.482708    |     0.547053    |     -0.068 |    0.357   |                   1 |                0 |
| equilibrium_beta_normal         | (86,)          | (86,)        |          0.27907  |      0.0015782   |      0.00356961  |      0.00371898  |     0.00837878  |     -0.068 |    0.357   |                   1 |                0 |
| equilibrium_beta_pol            | (86,)          | (86,)        |          0.27907  |      0.0528466   |      0.0808708   |      0.0887838   |     0.188386    |     -0.068 |    0.357   |                   1 |                0 |
| equilibrium_whmd                | (86,)          | (86,)        |          0.27907  |  22087.8         |  51204.7         |  53787.6         | 95270.6         |     -0.068 |    0.357   |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |          min |        median |          mean |           max |           std |
|:------------------------------------|------------------:|-------------:|--------------:|--------------:|--------------:|--------------:|
| dalpha_median_across_channels       |          0.864439 | -0.00732422  |   0.090332    |   0.130248    |   1.44043     |   0.127262    |
| soft_x_lower_median_across_channels |          0.864439 | -0.00535965  |   0.00144958  |   0.00248548  |   0.0226784   |   0.00347418  |
| soft_x_upper_median_across_channels |          0.864439 | -0.00400543  |   0.00106812  |   0.00324847  |   0.0244904   |   0.00521353  |
| thomson_t_e_edge_median             |          0.360465 |  7.81743     | 177.316       | 194.526       | 590.428       | 128.163       |
| thomson_t_e_core_median             |          0.651163 | 21.3805      | 391.699       | 415.271       | 660.595       | 135.642       |
| thomson_t_e_edge_core_ratio         |          0.348837 |  0.0242326   |   0.378018    |   0.468726    |   1.49959     |   0.307893    |
| thomson_t_e_profile_gradient_proxy  |          0.662791 |  1.95986     |  14.1349      |  14.5933      |  30.6255      |   5.87292     |
| thomson_n_e_edge_median             |          0.360465 |  1.61641e+17 |   4.87797e+18 |   4.71113e+18 |   1.09487e+19 |   2.62166e+18 |
| thomson_n_e_core_median             |          0.651163 |  3.22478e+18 |   9.85051e+18 |   1.06473e+19 |   1.65401e+19 |   2.6315e+18  |
| thomson_n_e_edge_core_ratio         |          0.348837 |  0.0119414   |   0.551535    |   0.512369    |   1.03498     |   0.253777    |
| thomson_n_e_profile_gradient_proxy  |          0.662791 |  7.95609e+16 |   3.194e+17   |   3.13318e+17 |   6.2905e+17  |   1.66276e+17 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.