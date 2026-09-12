# TokaMark One-Shot Array Probe — Shot 12034

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12034.zarr/`

## Load status

- loaded arrays: `14`
- failed arrays: `2`

### Failed arrays

- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |               min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|------------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (2412,)        | (2412,)      |          0.921642 | -155575           |     17.644       | 551919           |      1.76081e+06 |    -0.0572 |    0.54555 |                   1 |                0 |
| summary_ip                      | (2412,)        | (2412,)      |          1        |  -18818.8         | 431272           | 342808           | 564035           |    -0.0572 |    0.54555 |                   1 |                0 |
| interferometer_n_e_line         | (2412,)        | (2412,)      |          0.815091 |      -3.59077e+17 |      1.1124e+20  |      1.17134e+20 |      2.9703e+20  |    -0.0572 |    0.54555 |                   1 |                0 |
| dalpha_voltage                  | (3, 30150)     | (30150,)     |          0.921692 |      -0.012207    |      0.378418    |      0.508736    |      4.99756     |    -0.0572 |    0.54578 |                   4 |                0 |
| soft_x_lower                    | (18, 30150)    | (30150,)     |          0.921692 |      -0.00925064  |      0.000305176 |      0.00552594  |      0.0749207   |    -0.0572 |    0.54578 |                   8 |                0 |
| soft_x_upper                    | (18, 30150)    | (30150,)     |          0.921692 |      -0.0780869   |      0.000305176 |      0.00408167  |      0.0489426   |    -0.0572 |    0.54578 |                   8 |                0 |
| equilibrium_q95                 | (121,)         | (121,)       |          0.727273 |       5.09564     |      6.74462     |      8.62848     |     16.5887      |    -0.0572 |    0.5428  |                   1 |                0 |
| equilibrium_elongation          | (121,)         | (121,)       |          0.727273 |       1.20135     |      1.71154     |      1.69498     |      2.28843     |    -0.0572 |    0.5428  |                   1 |                0 |
| equilibrium_triangularity_upper | (121,)         | (121,)       |          0.727273 |       0.104607    |      0.34683     |      0.324862    |      0.417922    |    -0.0572 |    0.5428  |                   1 |                0 |
| equilibrium_triangularity_lower | (121,)         | (121,)       |          0.727273 |       0.179914    |      0.402826    |      0.373709    |      0.463865    |    -0.0572 |    0.5428  |                   1 |                0 |
| equilibrium_minor_radius        | (121,)         | (121,)       |          0.727273 |       0.394317    |      0.585563    |      0.568811    |      0.608101    |    -0.0572 |    0.5428  |                   1 |                0 |
| equilibrium_beta_normal         | (121,)         | (121,)       |          0.727273 |      -2.35459     |      1.17649     |      0.975378    |      2.66106     |    -0.0572 |    0.5428  |                   1 |                0 |
| equilibrium_beta_pol            | (121,)         | (121,)       |          0.727273 |      -0.727202    |      0.278901    |      0.221951    |      0.589169    |    -0.0572 |    0.5428  |                   1 |                0 |
| equilibrium_whmd                | (121,)         | (121,)       |          0.727273 |    2728.51        |  69405.9         |  61922.2         |  94584.6         |    -0.0572 |    0.5428  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |       mean |       max |        std |
|:------------------------------------|------------------:|------------:|------------:|-----------:|----------:|-----------:|
| dalpha_median_across_channels       |          0.921692 | -0.00732422 | 0.444336    | 0.464566   | 4.99756   | 0.362104   |
| soft_x_lower_median_across_channels |          0.921692 | -0.00555038 | 0.00119209  | 0.00365535 | 0.021286  | 0.00548714 |
| soft_x_upper_median_across_channels |          0.921692 | -0.00431061 | 0.000591278 | 0.00240182 | 0.0172997 | 0.00382872 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.