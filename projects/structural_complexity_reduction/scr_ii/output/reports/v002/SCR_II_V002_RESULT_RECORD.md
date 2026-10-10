# SCR-II v002 Result Record

**Project:** Structural Complexity Reduction (SCR)  
**Phase:** SCR-II — solution-preserving computational transfer  
**Benchmark:** `ROUTE_CSP_I/v002`  
**Engine:** `SCR_II_ENGINE_v002_PRIMARY_v001`  
**Preregistration:** `SCR_II_PREREG_v002`  
**Status:** `COMPLETE`  
**Primary verdict:** `PRESERVATION_FAIL`

## Provenance integrity

- Primary grid: **30/30 cells complete**
- Checkpoint: **30/30 cells complete**
- Primary result SHA-256: `d42d2f72d5e392f6732128583e0b4d9d07a34e381c81c8faca2a00c60d8d2d22`
- Declared primary SHA-256: **MATCH**
- Completed checkpoint SHA-256: `ef96d6150a78cfea4b2e5ea77b09c14a70fb12b121b9a9d8cea6ebfc40332a3d`
- Uploaded primary archive SHA-256: `029503f16922c4dafc61276dde5214513bfc436c1ac199ce27ad43be6c5c63af`
- Checkpoint records are byte-value equivalent to the 30 primary records: **PASS**
- Checkpoint preflight object equals final-result preflight object: **PASS**

Frozen preflight hashes:

- calibration: `7f5f4ad85dfe53fa1eb627ad424eec468fc878419fee22203100650bdde3eef9`
- preregistration config: `2ecb6bf35dc1db76fa44da5e0d3f3d2c2889f95daf1919a7a8cb5bd03ab180f3`
- design audit: `fbd0116987622ef99e29bc5d6c830f58e32844bacdc99a6f8bd875bc15c684f0`
- seeds: `0e4ccc6c4116c22febc3934c95f5f0d0afbcc9e2771a2a93c07fbfaf3226b600`

## Primary outcome

The exact-preservation hypothesis failed in every primary cell:

\[
S_{SCR} \ne S_{baseline} \quad \text{for 30/30 cells}.
\]

Accordingly, the frozen primary verdict is:

`PRESERVATION_FAIL`

Overall:

- preservation passes: **0/30**
- preservation failures: **30/30**
- median exact-solution recall: **0.00%**
- maximum exact-solution recall: **0.888%**
- baseline exact solutions across all cells: **106,417**
- SCR-returned exact solutions across all cells: **17**
- weighted exact-solution retention: **0.0160%**
- cells returning zero exact solutions after structural filtering: **20/30**
- cells returning at least one exact solution: **10/30**
- extra/non-baseline SCR solutions: **0**

## Search contraction and timing

Despite preservation failure:

- median node reduction: **99.94%**
- median leaf reduction: **99.99%**
- median SCR time gain: **151.691×**
- aggregate expanded nodes, baseline: **3,440,610**
- aggregate expanded nodes, SCR: **1,781**

The apparent acceleration is therefore not a valid solver acceleration under the preregistered SCR-II criterion, because the exact solution set is not preserved.

## Conventional C1 control

The solver-native arithmetic control preserved the exact baseline solution set in **30/30 cells**.

Across all cells:

- baseline exact-solution total: **106,417**
- C1 exact-solution total: **106,417**
- C1 exact preservation: **30/30**
- aggregate C1 expanded nodes: **1,111,466**

C1 therefore demonstrates that large reductions in search effort can coexist with exact solution preservation when the pruning rule is aligned with the arithmetic problem constraints.

## Depth-resolved record

| Depth | Preservation | Median baseline solutions | Median SCR solutions | Median solution recall | Max recall | Median node reduction | Median SCR time gain | Median C1 time gain |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 14 | 0/10 | 472.5 | 0.0 | 0.0000% | 0.8876% | 99.67% | 30.362× | 2.535× |
| 16 | 0/10 | 2192.5 | 0.5 | 0.0196% | 0.1548% | 99.94% | 151.691× | 2.193× |
| 18 | 0/10 | 7836.0 | 0.0 | 0.0000% | 0.0235% | 99.98% | 719.956× | 2.752× |

## Gate rejection profile

Across all recorded first-rejection events:

- G1: **1,087** (70.08%)
- G2: **385** (24.82%)
- G3: **47** (3.03%)
- G4: **32** (2.06%)

The contraction is dominated by G1 and G2.

## Scaling note

The stored exploratory node-scaling fit is:

- baseline alpha: **1.000021**
- SCR alpha: **-0.062403**
- delta alpha: **1.062424**
- exploratory scaling signal: **FALSE**

Because H1 preservation failed, this apparent scaling advantage has no positive computational-transfer status. The preregistered hierarchy correctly blocks escalation.

## Frozen interpretation

SCR-II v002 establishes a **non-transfer result** for this benchmark:

> The frozen route-structural grammar can collapse the nominal search tree extremely strongly, but it does not preserve an independently generated arithmetic exact-solution set. Therefore search reduction and runtime reduction alone are insufficient evidence of valid Structural Complexity Reduction.

This result does not negate SCR-I. It defines a boundary on transfer: a structural grammar cannot be assumed to preserve targets that are independent of the structure encoded by that grammar.
