# TokaMark One-Shot Array Probe — Shot 11908

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11908.zarr/`

## Load status

- loaded arrays: `14`
- failed arrays: `2`

### Failed arrays

- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (2189,)        | (2189,)      |          0.906807 |  -8939.09        | 944095           | 626147           |      1.3474e+06  |    -0.0608 |    0.4862  |                   1 |                0 |
| summary_ip                      | (2189,)        | (2189,)      |          1        | -20237.8         | 462786           | 423934           | 784489           |    -0.0608 |    0.4862  |                   1 |                0 |
| interferometer_n_e_line         | (2189,)        | (2189,)      |          0.898127 |     -7.08552e+17 |      8.55513e+19 |      8.48782e+19 |      1.63759e+20 |    -0.0608 |    0.4862  |                   1 |                0 |
| dalpha_voltage                  | (3, 27360)     | (27360,)     |          0.907127 |     -0.012207    |      0.368652    |      0.451303    |      4.01611     |    -0.0608 |    0.48638 |                   4 |                0 |
| soft_x_lower                    | (18, 27360)    | (27360,)     |          0.907127 |     -0.00986099  |      0.000267029 |      0.00897365  |      0.0566101   |    -0.0608 |    0.48638 |                   8 |                0 |
| soft_x_upper                    | (18, 27360)    | (27360,)     |          0.907127 |     -0.0780869   |      0.00152588  |      0.0080159   |      0.0625992   |    -0.0608 |    0.48638 |                   8 |                0 |
| equilibrium_q95                 | (110,)         | (110,)       |          0.654545 |      2.21565     |      6.77899     |      8.32976     |     15.9411      |    -0.0608 |    0.4842  |                   1 |                0 |
| equilibrium_elongation          | (110,)         | (110,)       |          0.654545 |      1.21638     |      1.74146     |      1.76489     |      2.11385     |    -0.0608 |    0.4842  |                   1 |                0 |
| equilibrium_triangularity_upper | (110,)         | (110,)       |          0.654545 |      0.116133    |      0.368838    |      0.333541    |      0.439968    |    -0.0608 |    0.4842  |                   1 |                0 |
| equilibrium_triangularity_lower | (110,)         | (110,)       |          0.654545 |      0.192803    |      0.453491    |      0.393152    |      0.481749    |    -0.0608 |    0.4842  |                   1 |                0 |
| equilibrium_minor_radius        | (110,)         | (110,)       |          0.654545 |      0.39536     |      0.614493    |      0.584695    |      0.646037    |    -0.0608 |    0.4842  |                   1 |                0 |
| equilibrium_beta_normal         | (110,)         | (110,)       |          0.654545 |    -21.8658      |      1.19253     |      0.835707    |      2.26239     |    -0.0608 |    0.4842  |                   1 |                0 |
| equilibrium_beta_pol            | (110,)         | (110,)       |          0.654545 |     -5.51284     |      0.253611    |      0.157532    |      0.375771    |    -0.0608 |    0.4842  |                   1 |                0 |
| equilibrium_whmd                | (110,)         | (110,)       |          0.654545 |   4287.35        | 152787           | 127004           | 200981           |    -0.0608 |    0.4842  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |     median |       mean |       max |        std |
|:------------------------------------|------------------:|------------:|-----------:|-----------:|----------:|-----------:|
| dalpha_median_across_channels       |          0.907127 | -0.00732422 | 0.410156   | 0.373034   | 3.81592   | 0.188807   |
| soft_x_lower_median_across_channels |          0.907127 | -0.00637054 | 0.00450134 | 0.0092325  | 0.0356293 | 0.0107203  |
| soft_x_upper_median_across_channels |          0.907127 | -0.00511169 | 0.00217438 | 0.00666102 | 0.0260544 | 0.00776656 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.