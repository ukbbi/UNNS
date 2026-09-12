# TokaMark One-Shot Array Probe — Shot 12055

## Purpose

This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.

It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.

## Source

- base URL: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1`
- shot store: `https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12055.zarr/`

## Load status

- loaded arrays: `16`
- failed arrays: `0`

## Signal summaries

| label                           | values_shape   | time_shape   |   finite_fraction |              min |           median |             mean |              max |   time_min |   time_max |   downloaded_chunks |   missing_chunks |
|:--------------------------------|:---------------|:-------------|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------:|-----------:|--------------------:|-----------------:|
| summary_power_nbi               | (1377,)        | (1377,)      |          0.882353 |  -4597.32        |      4.03356     | 174380           |      1.24971e+06 |    -0.0504 |     0.2936 |                   1 |                0 |
| summary_ip                      | (1377,)        | (1377,)      |          1        | -31100.6         | 170895           | 158327           | 334098           |    -0.0504 |     0.2936 |                   1 |                0 |
| interferometer_n_e_line         | (1377,)        | (1377,)      |          0.882353 |     -3.9761e+17  |      6.67364e+19 |      5.55178e+19 |      1.00997e+20 |    -0.0504 |     0.2936 |                   1 |                0 |
| dalpha_voltage                  | (3, 17211)     | (17211,)     |          0.882575 |     -0.012207    |      0.336914    |      0.362274    |      3.24463     |    -0.0504 |     0.2938 |                   2 |                0 |
| soft_x_lower                    | (18, 17211)    | (17211,)     |          0.882575 |     -0.0100899   |      0           |      0.00212283  |      0.119781    |    -0.0504 |     0.2938 |                   8 |                0 |
| soft_x_upper                    | (18, 17211)    | (17211,)     |          0.882575 |     -0.0780869   |      0           |     -0.00017148  |      0.113983    |    -0.0504 |     0.2938 |                   8 |                0 |
| thomson_t_e                     | (120, 69)      | (69,)        |          0.358092 |      4.76532     |    240.007       |    238.247       |   1613.19        |    -0.0504 |     0.2896 |                   1 |                0 |
| thomson_n_e                     | (120, 69)      | (69,)        |          0.358092 |      1.18159e+17 |      1.65134e+19 |      1.74119e+19 |      3.69729e+19 |    -0.0504 |     0.2896 |                   1 |                0 |
| equilibrium_q95                 | (69,)          | (69,)        |          0.594203 |      6.81132     |     10.0609      |     10.3769      |     15.5764      |    -0.0504 |     0.2896 |                   1 |                0 |
| equilibrium_elongation          | (69,)          | (69,)        |          0.594203 |      1.16026     |      1.50553     |      1.48654     |      1.86179     |    -0.0504 |     0.2896 |                   1 |                0 |
| equilibrium_triangularity_upper | (69,)          | (69,)        |          0.594203 |      0.152166    |      0.290336    |      0.275298    |      0.384147    |    -0.0504 |     0.2896 |                   1 |                0 |
| equilibrium_triangularity_lower | (69,)          | (69,)        |          0.594203 |      0.187088    |      0.317108    |      0.322878    |      0.472551    |    -0.0504 |     0.2896 |                   1 |                0 |
| equilibrium_minor_radius        | (69,)          | (69,)        |          0.594203 |      0.400756    |      0.537418    |      0.527352    |      0.638425    |    -0.0504 |     0.2896 |                   1 |                0 |
| equilibrium_beta_normal         | (69,)          | (69,)        |          0.594203 |     -2.17101     |      0.5716      |      0.314628    |      1.24137     |    -0.0504 |     0.2896 |                   1 |                0 |
| equilibrium_beta_pol            | (69,)          | (69,)        |          0.594203 |     -1.98082     |      0.212584    |      0.0472217   |      0.697767    |    -0.0504 |     0.2896 |                   1 |                0 |
| equilibrium_whmd                | (69,)          | (69,)        |          0.594203 |   3887.79        |  20594.4         |  22154           |  35991.1         |    -0.0504 |     0.2896 |                   1 |                0 |

## Raw proxy summaries

| proxy                               |   finite_fraction |          min |       median |          mean |           max |          std |
|:------------------------------------|------------------:|-------------:|-------------:|--------------:|--------------:|-------------:|
| dalpha_median_across_channels       |          0.882575 | -0.00488281  |  0.332031    |   0.302319    |   1.43555     |  0.215014    |
| soft_x_lower_median_across_channels |          0.882575 | -0.00646591  |  0.000190735 |   0.000159504 |   0.078125    |  0.00111848  |
| soft_x_upper_median_across_channels |          0.882575 | -0.0050354   | -3.8147e-05  |   0.000441509 |   0.078125    |  0.00158776  |
| thomson_t_e_edge_median             |          0.289855 | 10.5488      | 72.0124      |  88.3973      | 214.491       | 61.1623      |
| thomson_t_e_core_median             |          0.623188 |  7.66696     | 99.1801      | 111.848       | 287.832       | 69.3438      |
| thomson_t_e_edge_core_ratio         |          0.275362 |  0.080125    |  1.37587     |   2.02912     |   9.32791     |  2.22481     |
| thomson_t_e_profile_gradient_proxy  |          0.652174 |  0.267872    |  8.45119     |   9.35227     |  55.7345      |  8.16305     |
| thomson_n_e_edge_median             |          0.289855 |  3.7764e+17  |  8.47249e+18 |   8.68503e+18 |   1.99142e+19 |  5.80714e+18 |
| thomson_n_e_core_median             |          0.623188 |  1.63694e+18 |  1.1478e+19  |   1.11763e+19 |   1.55695e+19 |  2.86674e+18 |
| thomson_n_e_edge_core_ratio         |          0.275362 |  0.0293762   |  0.889897    |   1.16295     |   5.83085     |  1.29122     |
| thomson_n_e_profile_gradient_proxy  |          0.652174 |  1.51088e+16 |  5.49927e+17 |   5.30731e+17 |   1.06934e+18 |  2.63536e+17 |

## Interpretation

This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.

If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:

```text
components/
  tokamark_m_edge_t_probe.py
```

This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.