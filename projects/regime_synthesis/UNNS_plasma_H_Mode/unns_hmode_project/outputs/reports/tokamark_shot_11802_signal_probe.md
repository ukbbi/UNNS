# TokaMark One-Shot Array Probe — Shot 11802

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11802.zarr/`

## Load status

- loaded arrays: `14`
- failed arrays: `2`

### Failed arrays

- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (1981,)        | (1981,)      |          0.883392 |    -18.1924      |      1.14214     |      3.10058     |     35.687       |    -0.0676 |     0.4274 |                   1 |                0 |
| summary_ip                      | (1981,)        | (1981,)      |          1        | -87533.1         | 519527           | 366184           | 586443           |    -0.0676 |     0.4274 |                   1 |                0 |
| interferometer_n_e_line         | (1981,)        | (1981,)      |          0.883392 |      8.77874e+17 |      1.10657e+20 |      1.02756e+20 |      2.04216e+20 |    -0.0676 |     0.4274 |                   1 |                0 |
| dalpha_voltage                  | (3, 24761)     | (24761,)     |          0.883648 |     -0.012207    |      0.378418    |      0.509756    |      3.59619     |    -0.0676 |     0.4276 |                   4 |                0 |
| soft_x_lower                    | (18, 24761)    | (24761,)     |          0.883648 |     -0.00650406  |      0.000114441 |      0.00646018  |      0.201874    |    -0.0676 |     0.4276 |                   8 |                0 |
| soft_x_upper                    | (18, 24761)    | (24761,)     |          0.883648 |     -0.0780869   |      0.000209808 |      0.00463138  |      0.180359    |    -0.0676 |     0.4276 |                   8 |                0 |
| equilibrium_q95                 | (100,)         | (100,)       |          0.64     |      5.6464      |      8.76271     |      8.64291     |     13.1976      |    -0.0676 |     0.4274 |                   1 |                0 |
| equilibrium_elongation          | (100,)         | (100,)       |          0.64     |      1.55525     |      1.71414     |      1.75065     |      2.0239      |    -0.0676 |     0.4274 |                   1 |                0 |
| equilibrium_triangularity_upper | (100,)         | (100,)       |          0.64     |      0.248203    |      0.354392    |      0.349112    |      0.428697    |    -0.0676 |     0.4274 |                   1 |                0 |
| equilibrium_triangularity_lower | (100,)         | (100,)       |          0.64     |      0.214575    |      0.385962    |      0.386638    |      0.453491    |    -0.0676 |     0.4274 |                   1 |                0 |
| equilibrium_minor_radius        | (100,)         | (100,)       |          0.64     |      0.560299    |      0.595962    |      0.600801    |      0.667417    |    -0.0676 |     0.4274 |                   1 |                0 |
| equilibrium_beta_normal         | (100,)         | (100,)       |          0.64     |      0.104638    |      0.776837    |      0.725559    |      1.33911     |    -0.0676 |     0.4274 |                   1 |                0 |
| equilibrium_beta_pol            | (100,)         | (100,)       |          0.64     |      0.0294488   |      0.197141    |      0.181349    |      0.330246    |    -0.0676 |     0.4274 |                   1 |                0 |
| equilibrium_whmd                | (100,)         | (100,)       |          0.64     |  38056.4         |  86045.5         |  86070.2         | 107868           |    -0.0676 |     0.4274 |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |        mean |       max |        std |
|:------------------------------------|------------------:|------------:|------------:|------------:|----------:|-----------:|
| dalpha_median_across_channels       |          0.883648 | -0.00732422 | 0.378418    | 0.411752    | 2.65381   | 0.321181   |
| soft_x_lower_median_across_channels |          0.883648 | -0.00421524 | 0.000400543 | 0.000949674 | 0.0135803 | 0.00236458 |
| soft_x_upper_median_across_channels |          0.883648 | -0.00465393 | 0.000276566 | 0.0013      | 0.0126648 | 0.00270844 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.