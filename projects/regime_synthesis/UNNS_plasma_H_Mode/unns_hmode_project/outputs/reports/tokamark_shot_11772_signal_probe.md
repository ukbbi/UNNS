# TokaMark One-Shot Array Probe — Shot 11772

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11772.zarr/`

## Load status

- loaded arrays: `13`
- failed arrays: `3`

### Failed arrays

- `summary_power_nbi`: `KeyError('Missing array metadata: summary/power_nbi/.zarray')`
- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_ip                      | (1912,)        | (1912,)      |          1        | -29222.7         | 475117           | 341382           | 585586           |    -0.0674 |    0.41035 |                   1 |                0 |
| interferometer_n_e_line         | (1912,)        | (1912,)      |          0.879707 |     -7.83524e+18 |      4.15053e+19 |      3.38352e+19 |      5.64748e+19 |    -0.0674 |    0.41035 |                   1 |                0 |
| dalpha_voltage                  | (3, 23891)     | (23891,)     |          0.879829 |     -0.012207    |      0.13916     |      0.304531    |      2.91016     |    -0.0674 |    0.4104  |                   4 |                0 |
| soft_x_lower                    | (18, 23891)    | (23891,)     |          0.879829 |     -0.00883102  |      7.62939e-05 |      0.00275075  |      0.0390625   |    -0.0674 |    0.4104  |                   8 |                0 |
| soft_x_upper                    | (18, 23891)    | (23891,)     |          0.879829 |     -0.0780869   |      0.000228882 |      0.00160847  |      0.0464249   |    -0.0674 |    0.4104  |                   8 |                0 |
| equilibrium_q95                 | (96,)          | (96,)        |          0.635417 |      6.45248     |      8.51844     |      8.77365     |     12.5064      |    -0.0674 |    0.4076  |                   1 |                0 |
| equilibrium_elongation          | (96,)          | (96,)        |          0.635417 |      1.5174      |      1.71022     |      1.72672     |      2.02298     |    -0.0674 |    0.4076  |                   1 |                0 |
| equilibrium_triangularity_upper | (96,)          | (96,)        |          0.635417 |      0.219395    |      0.330458    |      0.324313    |      0.400069    |    -0.0674 |    0.4076  |                   1 |                0 |
| equilibrium_triangularity_lower | (96,)          | (96,)        |          0.635417 |      0.219395    |      0.350969    |      0.351741    |      0.423218    |    -0.0674 |    0.4076  |                   1 |                0 |
| equilibrium_minor_radius        | (96,)          | (96,)        |          0.635417 |      0.486982    |      0.576569    |      0.576722    |      0.61651     |    -0.0674 |    0.4076  |                   1 |                0 |
| equilibrium_beta_normal         | (96,)          | (96,)        |          0.635417 |      0.0953231   |      0.409056    |      0.398297    |      0.664035    |    -0.0674 |    0.4076  |                   1 |                0 |
| equilibrium_beta_pol            | (96,)          | (96,)        |          0.635417 |      0.0291492   |      0.107919    |      0.105599    |      0.166765    |    -0.0674 |    0.4076  |                   1 |                0 |
| equilibrium_whmd                | (96,)          | (96,)        |          0.635417 |  26172.3         |  73694.4         |  72852.2         |  89475.6         |    -0.0674 |    0.4076  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |        mean |        max |        std |
|:------------------------------------|------------------:|------------:|------------:|------------:|-----------:|-----------:|
| dalpha_median_across_channels       |          0.879829 | -0.00732422 | 0.17334     | 0.154188    | 2.07031    | 0.105701   |
| soft_x_lower_median_across_channels |          0.879829 | -0.00574112 | 0.000333786 | 0.000319976 | 0.0206757  | 0.00100232 |
| soft_x_upper_median_across_channels |          0.879829 | -0.00404358 | 0.000295639 | 0.000451017 | 0.00854492 | 0.00105255 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.