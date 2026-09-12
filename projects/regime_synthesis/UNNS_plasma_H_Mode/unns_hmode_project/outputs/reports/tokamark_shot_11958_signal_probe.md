# TokaMark One-Shot Array Probe — Shot 11958

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11958.zarr/`

## Load status

- loaded arrays: `14`
- failed arrays: `2`

### Failed arrays

- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (1808,)        | (1808,)      |          0.893252 |  -7179.38        |      1.50441e+06 | 934038           |      1.64498e+06 |     -0.058 |    0.39375 |                   1 |                0 |
| summary_ip                      | (1808,)        | (1808,)      |          1        | -21421.7         | 390792           | 317173           | 933913           |     -0.058 |    0.39375 |                   1 |                0 |
| interferometer_n_e_line         | (1808,)        | (1808,)      |          0.893252 |     -7.63916e+18 |      4.95136e+19 |      5.44762e+19 |      1.44379e+20 |     -0.058 |    0.39375 |                   1 |                0 |
| dalpha_voltage                  | (3, 22600)     | (22600,)     |          0.893761 |     -0.012207    |      0.241699    |      0.365925    |      2.37549     |     -0.058 |    0.39398 |                   4 |                0 |
| soft_x_lower                    | (18, 22600)    | (22600,)     |          0.893761 |     -0.0110817   |      0.000190735 |      0.00758126  |      0.0767517   |     -0.058 |    0.39398 |                   8 |                0 |
| soft_x_upper                    | (18, 22600)    | (22600,)     |          0.893761 |     -0.0780869   |      0.000305176 |      0.00602897  |      0.0639725   |     -0.058 |    0.39398 |                   8 |                0 |
| equilibrium_q95                 | (91,)          | (91,)        |          0.626374 |      5.94347     |      8.99975     |     10.0874      |     16.8552      |     -0.058 |    0.392   |                   1 |                0 |
| equilibrium_elongation          | (91,)          | (91,)        |          0.626374 |      1.23571     |      1.74528     |      1.7546      |      2.42189     |     -0.058 |    0.392   |                   1 |                0 |
| equilibrium_triangularity_upper | (91,)          | (91,)        |          0.626374 |      0.107397    |      0.317361    |      0.292645    |      0.362226    |     -0.058 |    0.392   |                   1 |                0 |
| equilibrium_triangularity_lower | (91,)          | (91,)        |          0.626374 |      0.177701    |      0.37113     |      0.340939    |      0.454174    |     -0.058 |    0.392   |                   1 |                0 |
| equilibrium_minor_radius        | (91,)          | (91,)        |          0.626374 |      0.392771    |      0.574781    |      0.55985     |      0.606549    |     -0.058 |    0.392   |                   1 |                0 |
| equilibrium_beta_normal         | (91,)          | (91,)        |          0.626374 |     -0.206953    |      0.727183    |      1.15697     |      3.04002     |     -0.058 |    0.392   |                   1 |                0 |
| equilibrium_beta_pol            | (91,)          | (91,)        |          0.626374 |     -0.146215    |      0.202394    |      0.271575    |      0.628857    |     -0.058 |    0.392   |                   1 |                0 |
| equilibrium_whmd                | (91,)          | (91,)        |          0.626374 |   3848.28        |  80830.2         |  72479.3         | 124046           |     -0.058 |    0.392   |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |       mean |       max |       std |
|:------------------------------------|------------------:|------------:|------------:|-----------:|----------:|----------:|
| dalpha_median_across_channels       |          0.893761 | -0.00732422 | 0.358887    | 0.295746   | 1.62109   | 0.197457  |
| soft_x_lower_median_across_channels |          0.893761 | -0.0051403  | 0.000667572 | 0.00490318 | 0.0519562 | 0.0081074 |
| soft_x_upper_median_across_channels |          0.893761 | -0.00364304 | 0.000162125 | 0.00349384 | 0.0231934 | 0.0057897 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.