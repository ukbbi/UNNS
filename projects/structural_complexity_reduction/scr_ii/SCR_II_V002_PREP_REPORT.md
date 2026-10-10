# SCR-II v002 Prep Validation Report

- v002 preregistration: PASS
- multiplicity calibration cells: 24
- primary seeds inspected: NO
- accepted solution-count ranges: {"10": [21, 39], "12": [86, 141], "8": [6, 10]}
- calibration exact-preservation diagnostic passes: 0/24
- implementation/design audit: PASS
- design-audit cells: 6
- design exact-preservation diagnostic passes: 0/6

## Interpretation

The v002 benchmark successfully removes the v001 single-solution degeneracy.

The preservation diagnostic is intentionally not a tuning criterion. If it is negative, that is evidence about transfer of the frozen structural filter to an independently defined arithmetic exact-solution set; it is not permission to alter the frozen benchmark.
