# TokaMark One-Shot Array Probe — Shot 11780

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11780.zarr/`

## Load status

- loaded arrays: `13`
- failed arrays: `3`

### Failed arrays

- `summary_power_nbi`: `KeyError('Missing array metadata: summary/power_nbi/.zarray')`
- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |            mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_ip                      | (1994,)        | (1994,)      |          1        | -61618.9         | 530713           | 363963          | 585676           |    -0.0672 |    0.43105 |                   1 |                0 |
| interferometer_n_e_line         | (1994,)        | (1994,)      |          0.885155 |     -6.53352e+16 |      9.97763e+19 |      8.6875e+19 |      1.76072e+20 |    -0.0672 |    0.43105 |                   1 |                0 |
| dalpha_voltage                  | (3, 24921)     | (24921,)     |          0.885197 |     -0.012207    |      0.458984    |      0.519819   |      3.48633     |    -0.0672 |    0.4312  |                   4 |                0 |
| soft_x_lower                    | (18, 24921)    | (24921,)     |          0.885197 |     -0.00692368  |      7.62939e-05 |      0.00579416 |      0.16449     |    -0.0672 |    0.4312  |                   8 |                0 |
| soft_x_upper                    | (18, 24921)    | (24921,)     |          0.885197 |     -0.0780869   |      0.000267029 |      0.00400211 |      0.14328     |    -0.0672 |    0.4312  |                   8 |                0 |
| equilibrium_q95                 | (100,)         | (100,)       |          0.64     |      5.8309      |      8.81239     |      8.65341    |     13.273       |    -0.0672 |    0.4278  |                   1 |                0 |
| equilibrium_elongation          | (100,)         | (100,)       |          0.64     |      1.55015     |      1.73242     |      1.76837    |      2.01747     |    -0.0672 |    0.4278  |                   1 |                0 |
| equilibrium_triangularity_upper | (100,)         | (100,)       |          0.64     |      0.230533    |      0.355119    |      0.348295   |      0.396448    |    -0.0672 |    0.4278  |                   1 |                0 |
| equilibrium_triangularity_lower | (100,)         | (100,)       |          0.64     |      0.22125     |      0.417979    |      0.392622   |      0.454578    |    -0.0672 |    0.4278  |                   1 |                0 |
| equilibrium_minor_radius        | (100,)         | (100,)       |          0.64     |      0.492992    |      0.600871    |      0.596357   |      0.627582    |    -0.0672 |    0.4278  |                   1 |                0 |
| equilibrium_beta_normal         | (100,)         | (100,)       |          0.64     |      0.126808    |      0.811241    |      0.768193   |      1.30066     |    -0.0672 |    0.4278  |                   1 |                0 |
| equilibrium_beta_pol            | (100,)         | (100,)       |          0.64     |      0.0372281   |      0.214294    |      0.192902   |      0.327398    |    -0.0672 |    0.4278  |                   1 |                0 |
| equilibrium_whmd                | (100,)         | (100,)       |          0.64     |  27497.4         |  86133.5         |  85586          | 108502           |    -0.0672 |    0.4278  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |        mean |        max |        std |
|:------------------------------------|------------------:|------------:|------------:|------------:|-----------:|-----------:|
| dalpha_median_across_channels       |          0.885197 | -0.00488281 | 0.495605    | 0.497582    | 1.72363    | 0.303382   |
| soft_x_lower_median_across_channels |          0.885197 | -0.0048542  | 0.000610352 | 0.000405109 | 0.00524521 | 0.00103938 |
| soft_x_upper_median_across_channels |          0.885197 | -0.00507355 | 0.000476837 | 0.000657269 | 0.00696182 | 0.00144228 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.