# SCR-II v002 Analysis

## Executive conclusion

SCR-II v002 is a decisive negative transfer test.

The structural filter reduced search effort spectacularly, but failed the primary preservation condition in **all 30 frozen primary instances**. Median node reduction was **99.94%** and median runtime gain was **151.691×**, yet median exact-solution recall was **0.00%**.

The correct conclusion is therefore not that SCR-II achieved a huge speedup. The correct conclusion is:

> **Compression without target preservation is computational invalidation, not computational reduction.**

## 1. The negative result is systematic

Failure occurs at every tested transfer depth:

| Depth | Preservation | Median baseline solutions | Median SCR solutions | Median solution recall | Max recall | Median node reduction | Median SCR time gain | Median C1 time gain |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 14 | 0/10 | 472.5 | 0.0 | 0.0000% | 0.8876% | 99.67% | 30.362× | 2.535× |
| 16 | 0/10 | 2192.5 | 0.5 | 0.0196% | 0.1548% | 99.94% | 151.691× | 2.193× |
| 18 | 0/10 | 7836.0 | 0.0 | 0.0000% | 0.0235% | 99.98% | 719.956× | 2.752× |

There is no recovery of preservation with increasing depth. Instead, the structural search becomes more aggressive while exact-solution retention remains essentially zero.

Across all 30 cells, the baseline contains **106,417** exact solutions. The SCR arm returns only **17**, a weighted retention of **0.0160%**. Twenty cells return zero exact solutions; the other ten return only a few. The maximum per-cell exact-solution recall is **0.888%**.

## 2. Why the timing gain cannot count as success

The structural arm achieves:

- median node reduction: **99.94%**
- median leaf reduction: **99.99%**
- median runtime gain: **151.691×**

At depth 18, the median runtime gain rises to **719.956×**.

But those numbers result from refusing to explore nearly all of the space containing the arithmetic solutions. They measure how quickly the filter discards the problem, not how efficiently it solves the same problem.

This is precisely why SCR-II preregistered exact set equality as H1.

## 3. C1 is an important internal control

The conventional solver-native arithmetic control preserves the baseline exact solution set in **30/30 cells**.

This matters because it rules out the interpretation that exact preservation is impossible under any pruning strategy. Constraint-aligned pruning can reduce work while retaining all exact arithmetic solutions.

The contrast is therefore:

\[
\text{problem-aligned arithmetic pruning} \rightarrow \text{exact preservation},
\]

while

\[
\text{unrelated structural pruning} \rightarrow \text{extreme contraction + solution loss}.
\]

That contrast is one of the strongest scientific gains of SCR-II.

## 4. Intersection interpretation

The few exact arithmetic solutions that survive G1→G4 can be interpreted as the small intersection

\[
S_{arith} \cap S_{struct}.
\]

Across the entire frozen grid, only **17** of **106,417** arithmetic exact solutions lie in the returned structural set, with no extra false solutions emitted by the SCR arm.

This does not make the structural filter erroneous. It shows that the two notions of admissibility encode different structures.

## 5. Gate behavior

First-rejection events are distributed approximately as:

- G1: 70.08%
- G2: 24.82%
- G3: 3.03%
- G4: 2.06%

Most search-space contraction is therefore imposed by generability and boundary continuity before later gates become relevant.

## 6. Scaling result is subordinated to preservation

The stored fit gives `delta_alpha = 1.062424`, superficially suggesting dramatic asymptotic search contraction.

But the preregistered hierarchy correctly reports no scaling success because exact preservation already failed.

This is an important methodological lesson: a favorable scaling exponent is meaningless if the algorithm is no longer solving the same problem.

## 7. Scientific status

Recommended status:

`SCR_II_V002_COMPLETE_NON_TRANSFER`

The result should be retained as a positive contribution to the SCR program because it sharply constrains the theory:

> Structural Complexity Reduction is not justified by compression alone. Transfer requires a demonstrable relation between the structural grammar used for pruning and the target structure that must be preserved.

The next phase should test **structurally coupled but independently measured targets**, not arbitrary independent arithmetic targets and not targets constructed to guarantee preservation.
