# TokaMark One-Shot Array Probe — Shot 11876

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11876.zarr/`

## Load status

- loaded arrays: `14`
- failed arrays: `2`

### Failed arrays

- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (2144,)        | (2144,)      |          0.888993 |    -28.6556      |     -0.98846     |     -1.23119     |     17.4568      |    -0.0694 |    0.46635 |                   1 |                0 |
| summary_ip                      | (2144,)        | (2144,)      |          1        | -30413.2         | 556857           | 444875           | 756611           |    -0.0694 |    0.46635 |                   1 |                0 |
| interferometer_n_e_line         | (2144,)        | (2144,)      |          0.888993 |     -1.83546e+17 |      1.10285e+20 |      1.08077e+20 |      2.19718e+20 |    -0.0694 |    0.46635 |                   1 |                0 |
| dalpha_voltage                  | (3, 26800)     | (26800,)     |          0.889142 |     -0.012207    |      0.603027    |      0.586453    |      4.99756     |    -0.0694 |    0.46658 |                   4 |                0 |
| soft_x_lower                    | (18, 26800)    | (26800,)     |          0.889142 |     -0.00925064  |      7.62939e-05 |      0.00990669  |      0.277557    |    -0.0694 |    0.46658 |                   8 |                0 |
| soft_x_upper                    | (18, 26800)    | (26800,)     |          0.889142 |     -0.0780869   |      0.00274658  |      0.0112933   |      0.248566    |    -0.0694 |    0.46658 |                   8 |                0 |
| equilibrium_q95                 | (108,)         | (108,)       |          0.675926 |      2.6649      |      3.75189     |      4.75122     |      8.83793     |    -0.0694 |    0.4656  |                   1 |                0 |
| equilibrium_elongation          | (108,)         | (108,)       |          0.675926 |      1.42279     |      1.51765     |      1.58469     |      1.95872     |    -0.0694 |    0.4656  |                   1 |                0 |
| equilibrium_triangularity_upper | (108,)         | (108,)       |          0.675926 |      0.196661    |      0.258979    |      0.271276    |      0.39611     |    -0.0694 |    0.4656  |                   1 |                0 |
| equilibrium_triangularity_lower | (108,)         | (108,)       |          0.675926 |      0.166403    |      0.384192    |      0.363428    |      0.447772    |    -0.0694 |    0.4656  |                   1 |                0 |
| equilibrium_minor_radius        | (108,)         | (108,)       |          0.675926 |      0.481415    |      0.591559    |      0.579272    |      0.6358      |    -0.0694 |    0.4656  |                   1 |                0 |
| equilibrium_beta_normal         | (108,)         | (108,)       |          0.675926 |     -5.29783     |      0.160841    |     -0.671704    |      0.87054     |    -0.0694 |    0.4656  |                   1 |                0 |
| equilibrium_beta_pol            | (108,)         | (108,)       |          0.675926 |     -0.881119    |      0.0354149   |     -0.0872527   |      0.22125     |    -0.0694 |    0.4656  |                   1 |                0 |
| equilibrium_whmd                | (108,)         | (108,)       |          0.675926 |  36826.1         | 140561           | 132916           | 204034           |    -0.0694 |    0.4656  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |        mean |        max |        std |
|:------------------------------------|------------------:|------------:|------------:|------------:|-----------:|-----------:|
| dalpha_median_across_channels       |          0.889142 | -0.00732422 | 0.554199    | 0.570177    | 4.99756    | 0.358933   |
| soft_x_lower_median_across_channels |          0.889142 | -0.00441551 | 0.000305176 | 0.000393431 | 0.00650406 | 0.00101615 |
| soft_x_upper_median_across_channels |          0.889142 | -0.00364304 | 0.00484467  | 0.00562117  | 0.0268555  | 0.0067668  |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.