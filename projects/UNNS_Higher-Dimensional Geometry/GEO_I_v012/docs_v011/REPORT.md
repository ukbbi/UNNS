# GEO-I v011 — Report

## 1. Outcome
| Programme | Result | Status |
|---|---|---|
| B — W2 | `n_2 ≥ p−1` for `p ≥ 9`; `k=7,p=8` impossible; `k ≤ 6` classified ⇒ **W2 holds universally** | PROVED+CHECKED |
| C — rank | `r_min = 3` for every non-embedded binary 0/1 box; no rank-4 minimal box | PROVED |
| A — cap | one-sided cap: explicit cell family, exact cover d≤60 (39,590), 544 certificates; arithmetic lemma G11-A CHECKED d≤150 | CHECKED |
| A — cap | mixed boxes, universal G11-C1/T1, stabilization G11-T2 | **OPEN** |
| D — certificates | PARTITION (231) and CAPCOVER (544) formats, standalone `checker11.py`, tamper tests | PROVED+CHECKED |

The two programmes were independent, and W2 is reported without waiting for the cap.

## 2. Programme B in one paragraph
The partitions of `1` into circuits give a vector-space partition of `F_2^{k−1}` (rigidity); with the counting identity and a Parseval identity for the weight enumerator, Cauchy–Schwarz and `m ≤ p/2` force `n_2 ≥ p−1` once `p ≥ 9` (the inequality `p(2^m/m−2) ≥ 2^m−2` is exact at `p=9, m=3`, and the bound is attained by `X = AG(k−1,2)`). Small `p` reduce to `k ≤ 6` (inherited classification; fresh brute force over all subsets for `k ≤ 5`: 19,373 minimal subsets at `k=5`, min `n_2 = 8`) and the single case `(k,p) = (7,8)` (`E_8`, not minimal). Details: `MATHEMATICS.md` §1.

## 3. Programme A in one paragraph
For `Q = (d+u, d)` the cap `K = W_u + (d,0)` is swept by horizontal Graver cells along the right boundary of `W_u` plus one bottom cell; the bottom cell works iff `cr(g,M) ≥ x_m y_m` for `g ∈ {(1,s−d),(d−t,−1)}`, an arithmetic statement verified on 657,526 triples but not proved. For `u,v ≥ 1` the horizontal/vertical sweeps cover the side regions; a corner pentagon and the top triangle remain; the non-degenerate corner is CHECKED for `d ≤ 15`, the rest is not resolved. **The cap theorem is not claimed.**

## 4. New vs inherited checks
New: `tests/test_geo11.py` (20), the v011 block of `verify.py`, `checker11.py`. Inherited: the unchanged v010 verifier (`verify_v010.py`: only document paths and the report name changed) re-runs every v005–v010 check as a gate; its counts are reported separately in `output/reports/verify_*.json` (`inherited_v010_*`).

## 5. Limits
Frozen binary 0/1 geometric model only. Parseval/knapsack scans and random nullity-7/8 samples are supplementary evidence, not part of any proof. No external literature beyond two abstract pages was consulted (`PRIOR_ART.md`); no priority claim.
