# TokaMark One-Shot Array Probe — Shot 11768

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/11768.zarr/`

## Load status

- loaded arrays: `13`
- failed arrays: `3`

### Failed arrays

- `summary_power_nbi`: `KeyError('Missing array metadata: summary/power_nbi/.zarray')`
- `thomson_t_e`: `KeyError('Missing array metadata: thomson_scattering/t_e/.zarray')`
- `thomson_n_e`: `KeyError('Missing array metadata: thomson_scattering/n_e/.zarray')`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |             max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_ip                      | (1662,)        | (1662,)      |          1        | -29712.6         | 460811           | 299284           | 561194          |    -0.0672 |    0.34805 |                   1 |                0 |
| interferometer_n_e_line         | (1662,)        | (1662,)      |          0.862214 |     -7.00668e+17 |      5.46982e+19 |      4.21224e+19 |      6.6021e+19 |    -0.0672 |    0.34805 |                   1 |                0 |
| dalpha_voltage                  | (3, 20770)     | (20770,)     |          0.862253 |     -0.012207    |      0.136719    |      0.279731    |      3.16162    |    -0.0672 |    0.34818 |                   4 |                0 |
| soft_x_lower                    | (18, 20770)    | (20770,)     |          0.862253 |     -0.007267    |      5.72205e-05 |      0.00556317  |      0.107422   |    -0.0672 |    0.34818 |                   8 |                0 |
| soft_x_upper                    | (18, 20770)    | (20770,)     |          0.862253 |     -0.0780869   |      0.000114441 |      0.0035918   |      0.0933838  |    -0.0672 |    0.34818 |                   8 |                0 |
| equilibrium_q95                 | (84,)          | (84,)        |          0.571429 |      6.48252     |      7.11842     |      7.55742     |      9.69964    |    -0.0672 |    0.3478  |                   1 |                0 |
| equilibrium_elongation          | (84,)          | (84,)        |          0.571429 |      1.43885     |      1.56728     |      1.5713      |      1.71193    |    -0.0672 |    0.3478  |                   1 |                0 |
| equilibrium_triangularity_upper | (84,)          | (84,)        |          0.571429 |      0.218276    |      0.327192    |      0.312485    |      0.433903   |    -0.0672 |    0.3478  |                   1 |                0 |
| equilibrium_triangularity_lower | (84,)          | (84,)        |          0.571429 |      0.218276    |      0.325382    |      0.322701    |      0.448882   |    -0.0672 |    0.3478  |                   1 |                0 |
| equilibrium_minor_radius        | (84,)          | (84,)        |          0.571429 |      0.485762    |      0.568311    |      0.568901    |      0.617757   |    -0.0672 |    0.3478  |                   1 |                0 |
| equilibrium_beta_normal         | (84,)          | (84,)        |          0.571429 |      0.123931    |      0.410226    |      0.419492    |      0.714086   |    -0.0672 |    0.3478  |                   1 |                0 |
| equilibrium_beta_pol            | (84,)          | (84,)        |          0.571429 |      0.0322189   |      0.0877781   |      0.0947559   |      0.171786   |    -0.0672 |    0.3478  |                   1 |                0 |
| equilibrium_whmd                | (84,)          | (84,)        |          0.571429 |  25734.8         |  70351.3         |  65708           |  74720.3        |    -0.0672 |    0.3478  |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |         min |      median |        mean |        max |         std |
|:------------------------------------|------------------:|------------:|------------:|------------:|-----------:|------------:|
| dalpha_median_across_channels       |          0.862253 | -0.00732422 | 0.180664    | 0.151159    | 1.34033    | 0.11876     |
| soft_x_lower_median_across_channels |          0.862253 | -0.00392914 | 0.000419617 | 0.000533689 | 0.0156403  | 0.00112078  |
| soft_x_upper_median_across_channels |          0.862253 | -0.00328064 | 0.000209808 | 0.000165157 | 0.00623703 | 0.000788726 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.