# TokaMark One-Shot Array Probe — Shot 11851

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11851.zarr/`

## Load status

- loaded arrays: `14`
- failed arrays: `2`

### Failed arrays

- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (1658,)        | (1658,)      |          0.859469 |     -5.05423     |      0.219678    |     -0.078676    |      4.76046     |     -0.068 |    0.34625 |                   1 |                0 |
| summary_ip                      | (1658,)        | (1658,)      |          1        | -50258           | 493168           | 406748           |      1.07064e+06 |     -0.068 |    0.34625 |                   1 |                0 |
| interferometer_n_e_line         | (1658,)        | (1658,)      |          0.859469 |     -1.03503e+19 |      6.52057e+19 |      5.87207e+19 |      1.207e+20   |     -0.068 |    0.34625 |                   1 |                0 |
| dalpha_voltage                  | (3, 20721)     | (20721,)     |          0.859997 |     -0.012207    |      0.327148    |      0.38797     |      3.05176     |     -0.068 |    0.3464  |                   4 |                0 |
| soft_x_lower                    | (18, 20721)    | (20721,)     |          0.859997 |     -0.012207    |      0.000305176 |      0.0144059   |      0.23941     |     -0.068 |    0.3464  |                   8 |                0 |
| soft_x_upper                    | (18, 20721)    | (20721,)     |          0.859997 |     -0.0780869   |      0.000762939 |      0.010989    |      0.215454    |     -0.068 |    0.3464  |                   8 |                0 |
| equilibrium_q95                 | (83,)          | (83,)        |          0.578313 |      4.90503     |      5.92139     |      6.17264     |      7.86437     |     -0.068 |    0.342   |                   1 |                0 |
| equilibrium_elongation          | (83,)          | (83,)        |          0.578313 |      1.51628     |      1.72055     |      1.70233     |      1.84249     |     -0.068 |    0.342   |                   1 |                0 |
| equilibrium_triangularity_upper | (83,)          | (83,)        |          0.578313 |      0.191664    |      0.320481    |      0.298328    |      0.419952    |     -0.068 |    0.342   |                   1 |                0 |
| equilibrium_triangularity_lower | (83,)          | (83,)        |          0.578313 |      0.185549    |      0.331995    |      0.320751    |      0.426484    |     -0.068 |    0.342   |                   1 |                0 |
| equilibrium_minor_radius        | (83,)          | (83,)        |          0.578313 |      0.432478    |      0.565826    |      0.536729    |      0.60125     |     -0.068 |    0.342   |                   1 |                0 |
| equilibrium_beta_normal         | (83,)          | (83,)        |          0.578313 |     -0.748295    |      0.540686    |      0.510453    |      0.905066    |     -0.068 |    0.342   |                   1 |                0 |
| equilibrium_beta_pol            | (83,)          | (83,)        |          0.578313 |     -0.148767    |      0.0984045   |      0.0966469   |      0.151361    |     -0.068 |    0.342   |                   1 |                0 |
| equilibrium_whmd                | (83,)          | (83,)        |          0.578313 |  28188.3         | 145893           | 122774           | 190571           |     -0.068 |    0.342   |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |     median |       mean |       max |        std |
|:------------------------------------|------------------:|------------:|-----------:|-----------:|----------:|-----------:|
| dalpha_median_across_channels       |          0.859997 | -0.00732422 | 0.334473   | 0.3023     | 1.51123   | 0.216433   |
| soft_x_lower_median_across_channels |          0.859997 | -0.00461578 | 0.00116348 | 0.00411273 | 0.0357246 | 0.00566188 |
| soft_x_upper_median_across_channels |          0.859997 | -0.00480652 | 0.00164032 | 0.00345385 | 0.0253296 | 0.00509857 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.