# GIG-INFO v006 — synthesis report

## How little of the dead-set nerve decides beta_2 > 0 ?

Exhaustive over the census: 338851 regimes (full mask excluded), 219145 distinct dead-set patterns, 151 with beta_2>0 (158 regimes). Exact H1 via strong-collapse cores (homotopy-preserving; checked against the full nerve on 355 patterns, 0 mismatches).

| observation O | H(Y|O) natural | H(Y|O) balanced | classes |
|---|---|---|---|
| V | 0.004917 | 0.512211 | 57 |
| (V,E) | 0.003667 | 0.241804 | 388 |
| (V,E,Tr) | 0.000599 | 0.005155 | 20595 |
| euler V-E+Tr | 0.001997 | 0.10732 | 10930 |
| (V,E,Hol) | 0.000599 | 0.005155 | 20595 |
| Hol | 0.003769 | 0.191923 | 2639 |
| (Hol,comp) | 0.002694 | 0.087528 | 8411 |
| (V,comp,Hol) | 0.000599 | 0.005155 | 20595 |
| core size | 0.000936 | 0.031851 | 57 |
| (V,E,Tr,Hol,comp) | 0.000599 | 0.005155 | 20595 |
| (core,Hol) | 2e-05 | 7.1e-05 | 11468 |
| (b0,Euler 2-skeleton) | 0.001997 | 0.107317 | 10931 |

* Positive cores (S6 types: 83) have sizes {'3': 105, '5': 23, '6': 6, '7': 1, '8': 2, '14': 5, '19': 1, '20': 3, '21': 3, '33': 2} vertices; the commonest is the bare hollow triangle.
* 148096 negative patterns collapse to a point (no homology to compute); negative core size quantiles {'0.5': 1.0, '0.9': 41.0, '0.99': 51.0, '1.0': 57.0}.
* Hollow triangles are common among negatives (184032 patterns) so their count is not a test.

No tested count-level statistic of the nerve (V,E,triangles,hollow count,components, Euler characteristic) gives H(Y|O)=0 on the census; the strong-collapse core does (it is the nerve up to homotopy) and is small for positives. Residual (V,E,Tr): 0.0052 bit balanced.