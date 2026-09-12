# FRACTIONAL COVER v003 — FINDINGS

## Status

**Diagnostic development result. Not a frozen grammar.**

## Main result

The parent-vs-fractional decomposition resolves the specific v002 depth-selection defect
without deleting or redefining the integer source sector.

All six Luo development records select `best_fractional_depth = 2`.

For N=32:

| Regime | Parent R2 | Fractional axis gain | Fractional mixed gain | Fractional total gain | Mean S |
|---|---:|---:|---:|---:|---:|
| LOW | 0.002072 | 0.076870 | 0.051774 | 0.128645 | 0.585326 |
| DTQC | 0.012515 | 0.717709 | 0.224366 | 0.942075 | 0.242481 |
| HIGH | 0.035786 | 0.598050 | 0.100526 | 0.698576 | 0.071881 |

The DTQC regime has the strongest fractional total gain and strongest fractional mixed gain,
but the high-frequency decoupled control also retains substantial d=2 fractional structure.

Therefore fractional cover organization alone is not DTQC admissibility.

The coupling/collective sector remains independent and necessary.

## Zhu retrospective check

Because Zhu motivated v003, this is not an independent validation.

Both Zhu records retrospectively select d=2 after conditioning on the integer parent lattice:

| Record | Parent R2 | Fractional axis gain | Fractional mixed gain | Fractional total gain |
|---|---:|---:|---:|---:|
| C1 | 0.600458 | -0.043640 | 0.138611 | 0.094971 |
| C3 | 0.522323 | -0.011398 | 0.300533 | 0.289135 |

## Structural interpretation

v003 now separates three questions:

1. How much of the observable belongs to the integer source/mixing lattice?
2. What additional structure appears on a fractional cover?
3. Is there independent collective/coupling evidence?

This is a better chart architecture than allowing d=1 and d>=2 to compete for a single
maximum explained-variance score.

## What is not yet established

- no admission threshold;
- no null-model significance gate;
- no independent external validation of v003;
- no prospective validation;
- no C003 test.

The next scientific requirement is a fresh independent multi-clock dataset or a previously
untouched source with legitimate time-domain controls. Only after that should v003 be considered
for grammar freeze.
