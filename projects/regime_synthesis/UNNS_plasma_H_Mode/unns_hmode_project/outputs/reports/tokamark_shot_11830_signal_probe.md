# TokaMark One-Shot Array Probe — Shot 11830

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11830.zarr/`

## Load status

- loaded arrays: `14`
- failed arrays: `2`

### Failed arrays

- `soft_x_lower`: `KeyError('Missing array metadata: soft_x_rays/horizontal_cam_lower/.zarray')`
- `soft_x_upper`: `KeyError('Missing array metadata: soft_x_rays/horizontal_cam_upper/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |               min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|------------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (1513,)        | (1513,)      |          0.848645 |   -9618.47        |      1.43454e+06 | 999589           |      1.72446e+06 |    -0.0672 |    0.3108  |                   1 |                0 |
| summary_ip                      | (1513,)        | (1513,)      |          1        | -112849           | 507165           | 321118           | 709891           |    -0.0672 |    0.3108  |                   1 |                0 |
| interferometer_n_e_line         | (1513,)        | (1513,)      |          0.848645 |      -5.35905e+17 |      8.81371e+19 |      8.17649e+19 |      1.55671e+20 |    -0.0672 |    0.3108  |                   1 |                0 |
| dalpha_voltage                  | (3, 18910)     | (18910,)     |          0.848704 |      -0.012207    |      0.505371    |      0.540018    |      4.99756     |    -0.0672 |    0.31098 |                   2 |                0 |
| thomson_t_e                     | (120, 76)      | (76,)        |          0.413596 |       3.04413     |    337.671       |    872.272       | 673789           |    -0.0672 |    0.3078  |                   1 |                0 |
| thomson_n_e                     | (120, 76)      | (76,)        |          0.413596 |       3.21422e+12 |      7.1264e+17  |      7.16409e+17 |      1.30293e+18 |    -0.0672 |    0.3078  |                   1 |                0 |
| equilibrium_q95                 | (76,)          | (76,)        |          0.539474 |       5.42433     |      8.46795     |      8.62561     |     10.7027      |    -0.0672 |    0.3078  |                   1 |                0 |
| equilibrium_elongation          | (76,)          | (76,)        |          0.539474 |       1.4961      |      1.67874     |      1.68523     |      1.93062     |    -0.0672 |    0.3078  |                   1 |                0 |
| equilibrium_triangularity_upper | (76,)          | (76,)        |          0.539474 |       0.154638    |      0.362308    |      0.342756    |      0.456091    |    -0.0672 |    0.3078  |                   1 |                0 |
| equilibrium_triangularity_lower | (76,)          | (76,)        |          0.539474 |       0.223795    |      0.291398    |      0.307784    |      0.38325     |    -0.0672 |    0.3078  |                   1 |                0 |
| equilibrium_minor_radius        | (76,)          | (76,)        |          0.539474 |       0.466104    |      0.569779    |      0.574654    |      0.61461     |    -0.0672 |    0.3078  |                   1 |                0 |
| equilibrium_beta_normal         | (76,)          | (76,)        |          0.539474 |       0.122527    |      0.810279    |      0.917793    |      1.91501     |    -0.0672 |    0.3078  |                   1 |                0 |
| equilibrium_beta_pol            | (76,)          | (76,)        |          0.539474 |       0.0344723   |      0.212594    |      0.221408    |      0.436638    |    -0.0672 |    0.3078  |                   1 |                0 |
| equilibrium_whmd                | (76,)          | (76,)        |          0.539474 |   46615.4         |  80945.4         |  82710.1         | 108069           |    -0.0672 |    0.3078  |                   1 |                0 |

## Raw proxy summaries

| proxy                              |   finite_fraction |          min |        median |           mean |              max |             std |
|:-----------------------------------|------------------:|-------------:|--------------:|---------------:|-----------------:|----------------:|
| dalpha_median_across_channels      |          0.848704 | -0.00732422  |   0.480957    |    0.478016    |      4.99756     |     0.368557    |
| thomson_t_e_edge_median            |          0.473684 |  6.49079     |  45.0399      |   51.294       |    104.031       |    35.4583      |
| thomson_t_e_core_median            |          0.592105 | 55.8384      | 206.385       | 8873.16        | 390089           | 57470.5         |
| thomson_t_e_edge_core_ratio        |          0.473684 |  7.38672e-05 |   0.21881     |    0.341733    |      1.51556     |     0.395614    |
| thomson_t_e_profile_gradient_proxy |          0.592105 |  0.348562    |   9.23827     |    9.31785     |     16.7499      |     4.10502     |
| thomson_n_e_edge_median            |          0.473684 |  4.9842e+12  |   2.83512e+17 |    2.68161e+17 |      4.66394e+17 |     1.44193e+17 |
| thomson_n_e_core_median            |          0.592105 |  1.58345e+16 |   6.36824e+17 |    5.82845e+17 |      7.97568e+17 |     1.63881e+17 |
| thomson_n_e_edge_core_ratio        |          0.473684 |  1.34429e-05 |   0.489595    |    0.450215    |      1.5604      |     0.254636    |
| thomson_n_e_profile_gradient_proxy |          0.592105 |  2.65142e+15 |   1.31604e+16 |    1.17091e+16 |      1.9505e+16  |     5.08021e+15 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.