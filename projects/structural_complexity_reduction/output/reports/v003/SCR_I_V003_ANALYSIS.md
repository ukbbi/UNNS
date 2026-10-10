# SCR-I v003 Analysis

## Executive conclusion

SCR-I-A v003 produced a positive **structural-compression** result with a clear sampling-density threshold.

Across all 15 primary cells, G1→G4 removed a median **92.03%** of the nominal mechanism candidates. At N=10,000 and N=40,000, all ten cells retained the independently identified target basin/class representation under every frozen v003 preservation criterion. The median end-to-end timing gain was **8.39×**, and the median operation-count gain was **6.73×**.

The result is not simply “92% pruning.” The gates also strongly enrich independently viable mechanisms: the viable fraction rises from a median **52.52%** in the full population to **99.15%** among survivors.

## 1. Compression is large and stable

Candidate reduction spans only a narrow range:

- minimum: **91.40%**
- median: **92.03%**
- maximum: **92.68%**

The contraction therefore remains near ~92% across all primary seeds and all three pool sizes.

This is important because the result is not carried by a single favorable seed or by one scale.

## 2. Representation preservation has a finite-sample floor

| Pool | Preserved | Representation loss | Median reduction | Min basin recall | Median geometric coverage | Median time gain |
|---:|---:|---:|---:|---:|---:|---:|
| 2,500 | 0/5 | 5/5 | 92.36% | 1.000 | 86.98% | 9.22× |
| 10,000 | 5/5 | 0/5 | 92.03% | 1.000 | 98.13% | 8.39× |
| 40,000 | 5/5 | 0/5 | 92.02% | 1.000 | 99.83% | 7.88× |

The N=2,500 cells reveal the failure mode cleanly. Basin identity itself is never lost: basin recall remains 1.0 in all five small-pool cells. What fails is representation quality.

The worst N=2,500 cell reaches only **65.38%** geometric coverage and a maximum centroid drift of **0.1418**. One cell contains a second small target basin with only two surviving target-positive representatives. This is not basin annihilation; it is undersampling of basin geometry.

At N=10,000, median geometric coverage rises to **98.13%** and all five cells cross the frozen 95% threshold.

At N=40,000, median coverage reaches **99.83%**, and all five cells again pass.

The v003 result is therefore best described as:

> Strong structural contraction preserves the target basin/class representation once the candidate population is sufficiently dense; below that density the same contraction can preserve class identity while losing internal representation fidelity.

## 3. The gates are selective, not merely destructive

The most informative diagnostic is target enrichment.

The independent viability oracle labels about half the nominal candidate population as target-positive:

- overall median baseline target fraction: **52.52%**

After structural filtering:

- overall median target fraction among survivors: **99.15%**

Thus, the gate chain maps a roughly 52.5%-viable nominal pool into a roughly 99%-viable survivor pool while retaining only ~8% of candidates.

Candidate-level target recall itself is modest (~15.04%), but v003 deliberately does not require identity-level recall. The structural question is whether the viable class/basin is represented after compression.

## 4. Computational gain

Across the 15 cells:

- time gain range: **7.73×–9.86×**
- median time gain: **8.39×**
- operation-count gain range: **6.42×–7.08×**
- median operation-count gain: **6.73×**

The filter cost is included in the SCR timing.

The gate audit explains why preprocessing remains cheap. At N=40,000, most rejections occur at G1 and G2, and short-circuit evaluation uses only **1.785** gate primitives per candidate on average rather than evaluating all four gates for every candidate.

## 5. What the result means for Structural Complexity Reduction

SCR-I-A v003 supports the core SCR proposition in a controlled calibration domain:

\[
S_0 \rightarrow G_1 \rightarrow G_2 \rightarrow G_3 \rightarrow G_4 \rightarrow S_\mathrm{effective}
\]

can produce a large reduction in candidate space before downstream processing while preserving the independently defined viable basin/class structure.

The key empirical combination is:

\[
\text{~92% candidate reduction}
+
\text{basin/class preservation at adequate N}
+
\text{~99% target concentration among survivors}
+
\text{~8.4× median end-to-end time gain}.
\]

## 6. What the result does not mean

The experiment does **not** show that UNNS uniquely preserves geometry under pruning. The rate-matched random nulls preserve the single broad basin well once N is large. This is expected in a densely sampled, structurally redundant basin.

Nor does the experiment establish that an exponential search has become polynomial, or imply any P/NP result.

The positive result is narrower and stronger:

> The frozen UNNS gate chain performs highly selective compression: it preserves the independently identified viable basin/class representation at sufficient sampling density while enriching viable targets far beyond rate-matched random pruning and reducing downstream computational work.

## 7. Recommended status

SCR-I-A v003 should be marked **COMPLETE / POSITIVE WITH SCALE THRESHOLD**.

Recommended summary label:

`STRUCTURAL_COMPRESSION_CONFIRMED_ABOVE_REPRESENTATION_FLOOR`
